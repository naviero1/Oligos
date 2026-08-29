import re, subprocess, urllib.parse, json, os, sys, time
import dap8

UA='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36'
ROOT='https://dap.ema.europa.eu/analytics/saw.dll?'
COL_SUB='"Line Listing Objects"."Substance High Level Code"'
COL_SOC='"Line Listing Objects"."Reaction SOC  (not linked to ID)"'
COL_PT ='"Line Listing Objects"."Reaction PT (not linked to ID - 2nd)"'
PATH_AGESEX='/shared/PHV DAP/DAP/DAP_Individual Cases by AgeGroup And Sex SOC PT SUB'
PATH_OUTCOME='/shared/PHV DAP/DAP/DAP_Individual Cases by Reaction Outcome SOC PT SUB'
PATH_REPORTER='/shared/PHV DAP/DAP/DAP_Individual Cases by ReporterGroup SOC PT SUB'
PATH_TOTAL='/shared/PHV DAP/DAP/DAP_NO_OF_CASES_SUB'
JAR='harvest_jar.txt'

def ensure_session():
    dap8.navigate('/shared/PHV DAP/_portal/DAP','', dap8.SUBPARAMS('12676156'),'sess', rounds=0, cj=JAR)

def go_csv(path, filters):
    """filters: list of (column, value). Builds P0..Pn."""
    q={'Go':'','Path':path,'Action':'Extract','Format':'csv','P0':str(len(filters))}
    i=1
    for col,val in filters:
        q[f'P{i}']='eq'; q[f'P{i+1}']=col; q[f'P{i+2}']='1 '+val; i+=3
    url=ROOT+'Go&'+urllib.parse.urlencode({k:v for k,v in q.items() if k!='Go'})
    r=subprocess.run(['curl','-sS','--max-time','240','-A',UA,'-b',JAR,'-c',JAR,url],
                     capture_output=True, text=True, errors='replace')
    return r.stdout

def pt_list(subcode, soc, tag):
    p={'P0':'2','P1':'eq','P2':COL_SUB,'P3':'1 '+str(subcode),
       'P4':'eq','P5':COL_SOC,'P6':'1 '+soc}
    dap8.navigate('/shared/PHV DAP/_portal/DAP','Number of Individual Cases for a selected Reaction',p,tag,rounds=0)
    fn=f'dap_{tag}_r0.html'
    if not os.path.exists(fn): return []
    h=open(fn,encoding='utf-8',errors='replace').read()
    caps=[c for c,v in re.findall(r'\{"caption":"([^"]*)","codeValue":"([^"]*)"', h)]
    # first block is SOC list, PTs follow; drop empties and the SOC name itself
    return [c for c in caps if c.strip() and c!=soc]

def csv_total(txt):
    tot=0; rows=0
    for ln in txt.splitlines()[1:]:
        f=ln.split(',')
        if f and f[0].strip().lstrip('﻿').isdigit():
            tot+=int(f[0]); rows+=1
    return tot, rows
