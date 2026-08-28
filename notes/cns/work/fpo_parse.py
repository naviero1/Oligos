import re, html, sys
from bs4 import BeautifulSoup

def load(path):
    s = open(path, encoding='utf-8', errors='replace').read()
    soup = BeautifulSoup(s, 'lxml')
    for t in soup(['script','style']): t.decompose()
    return soup

def tables(soup):
    """Return list of (index, caption_text_before, rows) for every <table> in the description div."""
    out=[]
    for i,tb in enumerate(soup.find_all('table')):
        rows=[]
        for tr in tb.find_all('tr'):
            cells=[re.sub(r'\s+',' ',td.get_text(' ',strip=True)) for td in tr.find_all(['td','th'])]
            cells=[c for c in cells]
            if any(c for c in cells): rows.append(cells)
        out.append((i,rows))
    return out

def fulltext(soup):
    t = soup.get_text('\n')
    t = re.sub(r'\n{2,}','\n',t)
    return t

if __name__=='__main__':
    soup=load(sys.argv[1])
    tbs=tables(soup)
    print('n tables', len(tbs))
    for i,rows in tbs:
        flat=' '.join(' '.join(r) for r in rows[:4])[:150]
        print(f'--- T{i} rows={len(rows)} :: {flat}')
