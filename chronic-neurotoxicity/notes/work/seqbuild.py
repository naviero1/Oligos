"""Reconstruct ISIS -> sequence from FPO patent HTML, joining wrapped cells,
and verifying every sequence against ALL independently printed length declarations
in the same row (start/stop span, chemistry string length, motif sum, linkage length+1).
A sequence is emitted ONLY if at least one declaration exists and every one agrees."""
import re, sys, collections
sys.path.insert(0,'/home/user/oligos/notes/cns/work')
from fpo_parse import load

FRAG  = re.compile(r'^[ACGT]{3,30}$')
ISIS  = re.compile(r'^\d{6}$')
CHEM  = re.compile(r'^(?=[edk]*[edk])(?![so]+$)[edk]{10,30}$')  # e=MOE d=DNA k=cEt
LINK  = re.compile(r'^[so]{9,29}$')
MOTIF = re.compile(r'^\d{1,2}-\d{1,2}-\d{1,2}$')
INT   = re.compile(r'^\d+$')

def rawrows(tb):
    out=[]
    for tr in tb.find_all('tr'):
        out.append([re.sub(r'\s+',' ',td.get_text(' ',strip=True)) for td in tr.find_all(['td','th'])])
    return out

def build(path, verbose=False):
    soup=load(path)
    recs=collections.defaultdict(list)
    for ti,tb in enumerate(soup.find_all('table')):
        rows=rawrows(tb)
        for ri,r in enumerate(rows):
            cells=[c.strip() for c in r]
            if not cells or not ISIS.match(cells[0] or ''): continue
            frags=[c for c in cells if FRAG.match(c)]
            if not frags: continue
            seq=frags[0]
            # absorb continuation rows (leading cells blank) that carry a bare [ACGT] fragment
            j=ri+1
            while j<len(rows):
                nxt=[c.strip() for c in rows[j]]
                if not nxt: break
                if nxt[0]: break                       # new record
                nf=[c for c in nxt if FRAG.match(c)]
                if not nf: break
                seq+=nf[0]; j+=1
            L=len(seq)
            chem =[c for c in cells if CHEM.match(c)]
            link =[c for c in cells if LINK.match(c)]
            motif=[c for c in cells if MOTIF.match(c)]
            ints =[c for c in cells if INT.match(c) and c!=cells[0]]
            decls={}
            if chem:  decls['chem']=len(chem[0])
            if link:  decls['link']=len(link[0])+1
            if motif: decls['motif']=sum(int(x) for x in motif[0].split('-'))
            # start/stop: first two consecutive ints whose span == some declared length
            span=None
            for a,b in zip(ints,ints[1:]):
                if int(b)>=int(a) and int(b)-int(a)+1==L: span=int(b)-int(a)+1; break
            if span: decls['span']=span
            if not decls: continue
            ok = all(v==L for v in decls.values())
            recs[cells[0]].append(dict(seq=seq,len=L,ok=ok,decls=decls,chem=chem[0] if chem else None,
                                       link=link[0] if link else None,motif=motif[0] if motif else None,table=ti))
    out={}; rejected={}
    for k,v in recs.items():
        good=[x for x in v if x['ok']]
        if good:
            seqs={x['seq'] for x in good}
            if len(seqs)>1:
                rejected[k]=('conflict',seqs); continue
            best=max(good,key=lambda x:len(x['decls']))
            best['n_support']=len(good)
            out[k]=best
        else:
            rejected[k]=('no verified row',{x['seq'] for x in v})
    return out, rejected

if __name__=='__main__':
    idx,rej=build(sys.argv[1])
    print('verified oligos:',len(idx),' rejected:',len(rej))
    for k,v in list(rej.items())[:15]: print('  REJ',k,v)
