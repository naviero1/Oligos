import subprocess, msgpack, json, unicodedata, time, sys
BASE='https://vigiaccess.org/protocol/IProtocol/'
def raw(method, body):
    r=subprocess.run(['curl','-sS','-w','\n__%{http_code}','--max-time','150','-X','POST',
        '-H','Content-Type: application/json; charset=utf-8','-H','x-remoting-proxy: true',
        '--data-binary', body, BASE+method], capture_output=True)
    out=r.stdout; code=out.rsplit(b'__',1)[-1].decode(errors='replace')
    payload=out.rsplit(b'\n__',1)[0]
    if code!='200': raise RuntimeError(f'{method} HTTP {code}: {payload[:150]!r}')
    return msgpack.unpackb(payload, raw=False, strict_map_key=False)
def clean(s):
    return ''.join(ch for ch in s if unicodedata.category(ch) not in ('Cf','Mn')) if isinstance(s,str) else s
def search(term): return raw('search', json.dumps([term]))
def drugid_json(entry): return {"DrugId":{"Encrypted": entry[0][1][1]}}
def socid_json(row):    return {"SocId":{"Encrypted": row[0][1][1]}}
def distribution(entry): return raw('distribution', json.dumps([drugid_json(entry)]))
def primary_terms(entry, socrow, maxpages=40):
    pts=[]; page=0
    while page < maxpages:
        req={"DrugId":drugid_json(entry), "SocId":socid_json(socrow), "Page":page}
        resp=raw('primaryTerm', json.dumps([req]))
        chunk=resp[0]; page_no=resp[1]; more=resp[2]
        for item in chunk:
            pts.append((clean(item[0][1]), item[1]))
        if not more: break
        page+=1; time.sleep(0.3)
    return pts
