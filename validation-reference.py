from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import xml.etree.ElementTree as E,re,json,html
B=Path('/Users/babarzaman/.codex/visualizations/2026/10/14/01a13ab1-cd1d-73d1-9857-78895d72a14b')
ROOT=B/'statinsightlab-academic-refinement-2026-10-21/website'
OLD=B/'statinsightlab-professional-update-2026-10-21/website'
class Document(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.ids=[];self.h1=0;self.active=0;self.canonical=0
 def handle_starttag(self,t,a):
  d=dict(a)
  if t=='h1':self.h1+=1
  if d.get('aria-current')=='page':self.active+=1
  if t=='link' and d.get('rel')=='canonical':self.canonical+=1
  if 'id' in d:self.ids.append(d['id'])
  if t=='img':assert d.get('alt'),d
  for k in ('href','src'):
   if k in d:self.links.append(d[k])
pages={}
for f in ROOT.rglob('*.html'):
 c=Document();c.feed(f.read_text());pages[f.resolve()]=c
 assert (c.h1,c.active,c.canonical)==(1,1,1),(f,c.h1,c.active,c.canonical)
 assert len(set(c.ids))==len(c.ids),(f,'duplicate id')
 old=Document();old.feed((OLD/f.relative_to(ROOT)).read_text())
 assert set(old.links)<=set(c.links),(f,'original links lost',set(old.links)-set(c.links))
for f,c in pages.items():
 for link in c.links:
  u=urlsplit(link)
  if u.scheme or u.netloc:continue
  dest=(f.parent/unquote(u.path)).resolve() if u.path else f
  assert dest.exists(),(f,link)
  if u.fragment and dest in pages:assert u.fragment in pages[dest].ids,(f,link)
for filename in ('index.html','research.html'):
 s=(ROOT/filename).read_text()
 assert s.count('class="card research-card"')==5
 assert s.count('<figure class="research-visual">')==5
 assert not re.search(r'<span class="eyebrow">\d+\s*/',s)
for p in (ROOT/'assets/research').glob('*.svg'):E.parse(p)
s=(ROOT/'publications.html').read_text()
assert s.count('class="publication-entry"')==55
assert s.count('class="author-highlight"')==55
data=json.loads(Path('/private/tmp/sil-doi-verification.json').read_text())
verified=sum(x.get('status')=='verified' for x in data)
assert s.count('class="doi-link"')==verified
assert len(set(re.findall(r'href="(https://doi.org/[^"]+)"',s)))==verified
# Confirm every citation's author text, title, journal text and year survived the split.
def clean(s):return re.sub(r'[^a-z0-9]','',html.unescape(s).lower())
old=(OLD/'publications.html').read_text()
old_items=re.findall(r'<li data-year="(\d{4})"><span class="eyebrow">\d{4}</span><p>(.*?)</p></li>',old,re.S)
new_items=re.findall(r'<li class="publication-entry" data-year="(\d{4})">(.*?)</li>',s,re.S)
for (old_year,old_text),(year,new_html) in zip(old_items,new_items):
 assert year==old_year
 # A DOI adds text, so require all original alphanumeric citation content after separating the year.
 original=re.sub(r'\('+old_year+r'\)\.','',html.unescape(old_text),count=1)
 parts=re.findall(r'<(?:h3|p)\b[^>]*>(.*?)</(?:h3|p)>',new_html,re.S)
 title,authors,journal=parts
 reconstructed=re.sub('<[^>]+>','',authors+' '+title+' '+journal)
 assert clean(original)==clean(reconstructed),(old_text,reconstructed)
for value in ('55+','1,013','19','28'):assert '<strong>'+value+'</strong>' in (ROOT/'index.html').read_text()
assert len(E.parse(ROOT/'sitemap.xml').getroot())==len(pages)
assert (ROOT/'CNAME').read_text().strip()=='statinsightlab.com'
print(f'PASS: {len(pages)} pages, preserved links and all 55 citations, five SVG research visuals, 55 author highlights, {verified} verified DOI links and unchanged metrics.')
