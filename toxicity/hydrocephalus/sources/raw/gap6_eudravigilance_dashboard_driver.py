import re, sys, json, subprocess, os, urllib.parse, html as H, time

UA='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36'
ROOT='https://dap.ema.europa.eu/analytics/'

def curl(cj, url, data=None, out=None):
    cmd=['curl','-sS','-L','--max-time','300','-A',UA,'-b',cj,'-c',cj,'-H','Accept: */*','-D','-']
    if data is not None:
        for k,v in data.items(): cmd += ['--data-urlencode', f'{k}={v}']
    cmd.append(url)
    r=subprocess.run(cmd, capture_output=True, text=True, errors='replace')
    body=r.stdout; hdrs=''
    while True:
        m=re.match(r'(HTTP/[^\n]*\n(?:[^\n]*\n)*?)\r?\n', body)
        if not m: break
        hdrs=m.group(1); body=body[m.end():]
    code=re.search(r'HTTP/\S+ (\d+)', hdrs)
    if out: open(out,'w',encoding='utf-8').write(body)
    return (code.group(1) if code else '?'), body

def parse_meta(b):
    m=re.search(r'\{i:"pageMetadata",t:4\}\S*?(\{.*)$', b, re.S)
    if not m: return None
    try: return json.JSONDecoder().raw_decode(m.group(1))[0]
    except Exception: return None

def navigate(portalpath, page, params, tag, rounds=4, cj=None):
    cj = cj or f'jar_{tag}.txt'
    if os.path.exists(cj): os.remove(cj)
    q = dict(params); q['PortalPath']=portalpath; q['Action']='Navigate'
    if page: q['Page']=page
    url = ROOT+'saw.dll?PortalPages&'+urllib.parse.urlencode(q)
    c,b = curl(cj, url, out=f'dap_{tag}_s1.html')
    m=re.search(r"onLoggingInPageLoad\('([^']+)',(\{.*?\})\);", b, re.S)
    if m: c,b = curl(cj, ROOT+m.group(1), data=json.loads(m.group(2)), out=f'dap_{tag}_s2.html')
    print(f'[{tag}] nav {c} len {len(b)}')
    out=[b]
    mr=re.search(r'id="idEmbedFrameDiv" src="([^"]+)"', b)
    if mr:
        src=H.unescape(mr.group(1))
        c,body = curl(cj, ROOT+src, out=f'dap_{tag}_r0.html')
        print(f'[{tag}] r0 {c} len {len(body)}')
        out.append(body)
        qs=urllib.parse.parse_qsl(src.split('?',1)[1], keep_blank_values=True)
        baseform={k:v for k,v in qs if k!='ReloadDashboard'}; baseform.pop('ViewState',None)
        for i in range(1,rounds+1):
            meta=parse_meta(body)
            if not meta: break
            secs=meta.get('reloadSections','')
            if not secs: break
            form=dict(baseform); form['ViewState']=meta['viewEnv']['viewState']; form['reloadTargets']=secs
            c,body = curl(cj, ROOT+'saw.dll?ReloadDashboard', data=form, out=f'dap_{tag}_r{i}.html')
            print(f'[{tag}] r{i} {c} len {len(body)}')
            out.append(body)
            time.sleep(0.5)
    return out

SUBPARAMS=lambda code: {'P0':'1','P1':'eq','P2':'"Line Listing Objects"."Substance High Level Code"','P3':'1 '+str(code)}

if __name__=='__main__':
    pp=sys.argv[1]; code=sys.argv[2]; tag=sys.argv[3]; page=sys.argv[4] if len(sys.argv)>4 else ''
    navigate(pp, page, SUBPARAMS(code), tag)
