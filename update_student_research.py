# -*- coding: utf-8 -*-
"""Render student cards from supervision-record-data.json; unconfirmed fields stay private."""
from pathlib import Path
from urllib.parse import urlsplit
from bs4 import BeautifulSoup
import json
ROOT=Path(__file__).resolve().parent
LINKS=[('linkedin','LinkedIn'),('google_scholar','Google Scholar'),('thesis','View Thesis'),('related_publication','Related Publication'),('github','GitHub'),('orcid','ORCID')]
def validate(records):
 names=set()
 for d in records:
  if not d.get('name') or d['name'] in names:raise ValueError('Missing or duplicate name')
  names.add(d['name'])
  if d['degree'] not in ('MS','PhD'):raise ValueError('Degree must be MS or PhD')
  if len(d.get('research_tags',[]))>3:raise ValueError('Maximum three research tags')
  if d.get('status_confirmed') and d.get('status') not in ('ongoing','graduate'):raise ValueError('Confirmed status must be ongoing or graduate')
  if d.get('role_confirmed') and d.get('supervision_role') not in ('Supervisor','Co-supervisor'):raise ValueError('Confirmed role must be Supervisor or Co-supervisor')
  if d.get('completion_year') and (len(str(d['completion_year']))!=4 or not str(d['completion_year']).isdigit()):raise ValueError('Completion year must be four digits')
  for publication in d.get('related_publications',[]):
   url=urlsplit(publication.get('url',''));host=url.hostname or ''
   if url.scheme!='https' or not host or url.username or url.password:raise ValueError('Related publications require valid HTTPS URLs')
  for field,_ in LINKS:
   value=d.get('links',{}).get(field,'').strip()
   if not value:continue
   u=urlsplit(value);host=(u.hostname or '').lower()
   if u.scheme!='https' or not host or u.username or u.password:raise ValueError('Resource links must be valid HTTPS URLs')
   if host in ('example.com','example.org','example.net') or host.endswith('.example.com'):raise ValueError('Placeholder URLs are not allowed')
   allowed={'linkedin':'linkedin.com','google_scholar':'scholar.google.com','github':'github.com'}
   if field in allowed and not (host==allowed[field] or host.endswith('.'+allowed[field])):raise ValueError('Unexpected host for '+field)
def build_cards(soup,records):
 validate(records)
 grid=soup.select_one('.thesis-student-grid');grid.clear()
 def element(name,cls=None,text=None):
  t=soup.new_tag(name)
  if cls:t['class']=cls
  if text is not None:t.string=text
  return t
 for d in records:
  card=element('article','thesis-student-card');card['data-student-name']=d['name']
  heading=element('div','thesis-student-heading');heading.append(element('h2',text=d['name']));degree=element('span','thesis-degree',d['degree']);degree['aria-label']='Degree: '+d['degree'];heading.append(degree);card.append(heading)
  confirmed=d.get('status_confirmed') is True
  status=d.get('status','') if confirmed else ''
  if status:card.append(element('p','student-stage',d['degree']+(' Research Student' if status=='ongoing' else ' Graduate')))
  if d.get('research'):
   card.append(element('p','thesis-field-label','Thesis title' if d.get('research_kind')=='title' else 'Research area'))
   card.append(element('p','student-research-title',d['research']))
  if d.get('research_summary','').strip():card.append(element('p','student-research-summary',d['research_summary'].strip()))
  if d.get('research_tags'):
   group=element('ul','student-research-tags');group['aria-label']='Research topics'
   for topic in d['research_tags']:group.append(element('li',text=topic))
   card.append(group)
  details=element('div','student-card-details')
  if d.get('education_details'):
   qualification=d['education_details'][-1]
   details.append(element('p','student-degree-detail',qualification['degree']+' · '+qualification['period']))
  if d.get('university'):details.append(element('p','thesis-institution',d['university']))
  if d.get('role_confirmed') is True:details.append(element('p','student-supervision-role','My role: '+d['supervision_role']))
  if status=='graduate' and d.get('completion_year_confirmed') is True and d.get('completion_year'):details.append(element('p','thesis-year','Completion year: '+str(d['completion_year'])))
  elif d.get('year'):details.append(element('p','thesis-year','Year: '+d['year']))
  if status:details.append(element('p','thesis-status','Research status: '+('Ongoing' if status=='ongoing' else 'Completed')))
  if d.get('current_position') or d.get('current_organisation'):
   position=d.get('current_position','').strip();organisation=d.get('current_organisation','').strip()
   if position or organisation:details.append(element('p','student-current-position',('Current position: '+position if position else 'Current organisation: '+organisation)+(' \u00b7 '+organisation if position and organisation else '')))
  if details.contents:card.append(details)
  resource_values=[(d.get('links',{}).get(field,'').strip(),label) for field,label in LINKS if d.get('links',{}).get(field,'').strip()]
  resource_values.extend((item['url'],item.get('title','').strip() or 'Related Publication') for item in d.get('related_publications',[]))
  resource_values=list(dict.fromkeys(resource_values))
  if resource_values:
   actions=element('div','thesis-resources')
   for url,label in resource_values:
    a=soup.new_tag('a',href=url,target='_blank',rel='noopener noreferrer');a.string=label+' \u2197';a['aria-label']=label+' for '+d['name']+' (opens in a new tab)';actions.append(a)
   card.append(actions)
  grid.append(card)
 return soup
if __name__=='__main__':
 records=json.loads((ROOT/'supervision-record-data.json').read_text());page=ROOT/'website/supervision/record.html';soup=BeautifulSoup(page.read_text(),'html.parser');build_cards(soup,records)
 if not soup.select_one('link[href$="student-card-details.css"]'):soup.head.append(soup.new_tag('link',rel='stylesheet',href='../assets/student-card-details.css'))
 page.write_text(str(soup));print('Updated student research cards.')
