import sys, re
sys.path.insert(0,'/home/user/oligos/notes/cns/work')
from fpo_parse import load
from seqbuild import rawrows

CARET = '{circumflex over ( )}'

def parse_seq_table(tb):
    """Rows -> [(name, raw, seqid)]; a new record starts at a row with a SEQ ID."""
    rows = [[c.strip() for c in r] for r in rawrows(tb)]
    recs, cur = [], None
    for r in rows:
        name = r[0] if len(r) > 0 else ''
        raw  = r[1] if len(r) > 1 else ''
        sid  = r[2] if len(r) > 2 else ''
        if raw.startswith('Sequence') or sid.startswith('ID NO') or sid=='SEQ': continue
        if name in ('Oligonucleotide','name','') and not raw and not sid: continue
        if raw.startswith('Uppercase') or name.startswith('Uppercase') or \
           name.startswith('Lowercase') or name.startswith(CARET) or raw.startswith(CARET[:6]):
            continue
        if sid:
            cur = dict(name=name, raw=raw, sid=sid)
            recs.append(cur)
        elif cur is not None and (raw or name):
            if name: cur['name'] += ' ' + name
            cur['raw'] += raw
    return recs

TOK = re.compile(r'([ACGTUacgtu])(\(L\)|\(M\))?')

def decode(raw):
    """Return (residues, seq_string). Case as printed: upper+(L)=LNA, upper=RNA,
    lower=DNA, upper+(M)=2'-O-Me RNA."""
    s = raw.replace(CARET, '^')
    body = re.sub(r'[\s]', '', s)
    res = []
    i = 0
    while i < len(body):
        ch = body[i]
        if ch == '^': i += 1; continue
        m = TOK.match(body, i)
        if not m: raise ValueError('unparsed char %r in %r' % (ch, raw))
        res.append((m.group(1), m.group(2) or ''))
        i = m.end()
    return res, ''.join(r[0] for r in res)

if __name__ == '__main__':
    soup = load('/home/user/oligos/sources/cns/fpo/US11851654.html')
    tbs = soup.find_all('table')
    for ti in (3, 13, 23, 33):
        print('=== T%d' % ti)
        for rec in parse_seq_table(tbs[ti]):
            res, seq = decode(rec['raw'])
            m = re.search(r'(\d+)mer', rec['name'])
            decl = int(m.group(1)) if m else None
            ps = rec['raw'].count(CARET)
            ok = 'OK' if (decl is None or decl == len(seq)) else 'LENGTH-MISMATCH'
            print('  %-42s len=%2d decl=%-4s %s ps_bonds=%2d  %s'
                  % (rec['name'][:42], len(seq), decl, ok, ps, seq))
