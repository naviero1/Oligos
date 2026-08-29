"""Build ISIS No -> sequence index from FPO patent HTML, with 4-way length verification."""
import re, sys, json
sys.path.insert(0,'/home/user/oligos/notes/cns/work')
from fpo_parse import load, tables

SEQRE = re.compile(r'^[ACGTU]{10,30}$')
NUM   = re.compile(r'^\d{5,7}$')

def build(path):
    soup=load(path)
    tbs=tables(soup)
    idx={}          # isis -> dict
    conflicts=[]
    for ti,rows in tbs:
        # find header row containing 'Sequence'
        hdr=None
        for r in rows[:6]:
            if any(c.strip().lower()=='sequence' for c in r): hdr=r; break
        for r in rows:
            cells=[c.strip() for c in r if c.strip()]
            if not cells: continue
            # need an isis number and a sequence
            isis=[c for c in cells if NUM.match(c)]
            seqs=[c for c in cells if SEQRE.match(c)]
            if len(isis)>=1 and len(seqs)==1:
                num=isis[0]; seq=seqs[0]
                rest=[c for c in cells if c!=seq]
                motif=[c for c in rest if re.match(r'^\d{1,2}-\d{1,2}-\d{1,2}$',c)]
                link =[c for c in rest if re.match(r'^[so]{9,29}$',c)]
                ints =[c for c in rest if re.match(r'^\d+$',c)]
                rec=dict(isis=num, seq=seq, len=len(seq),
                         motif=motif[0] if motif else None,
                         linkage=link[0] if link else None,
                         ints=ints, table=ti)
                if num in idx and idx[num]['seq']!=seq:
                    conflicts.append((num, idx[num]['seq'], seq, ti))
                else:
                    idx.setdefault(num,rec)
    return idx, conflicts

if __name__=='__main__':
    idx,conf=build(sys.argv[1])
    print('n oligos indexed', len(idx), 'conflicts', len(conf))
    for c in conf[:10]: print('CONFLICT',c)
    # verification summary
    ok=bad=0
    for k,v in idx.items():
        checks=[]
        if v['motif']:
            checks.append(sum(int(x) for x in v['motif'].split('-'))==v['len'])
        if v['linkage']:
            checks.append(len(v['linkage'])+1==v['len'])
        if all(checks) and checks: ok+=1
        elif checks: bad+=1; print('LENFAIL',v)
    print('verified',ok,'failed',bad,'no-check',len(idx)-ok-bad)
