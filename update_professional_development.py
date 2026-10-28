# -*- coding: utf-8 -*-
"""Show optional resources only when configured and valid."""
from pathlib import Path
from urllib.parse import urlsplit
from bs4 import BeautifulSoup
import json,re
from datetime import date
root=Path(__file__).resolve().parent;website=root/'website';page=website/'teaching/professional-learning.html'
records=json.loads((root/'professional-development-resources.json').read_text());soup=BeautifulSoup(page.read_text(),'html.parser')
for key,record in records.items():
 if soup.select_one(f'[data-development-card="{key}"]') is None:raise ValueError('Unknown card: '+key)
 year=record.get('completion_year','').strip()
 if year and not re.fullmatch(r'\d{4}',year):raise ValueError('Use a four-digit completion year')
 for date_field in ['completed_on','attended_on']:
  if record.get(date_field):date.fromisoformat(record[date_field])
 for field in ['course_url','certificate_document','credential_url']:
  value=record.get(field,'').strip()
  if not value:continue
  u=urlsplit(value)
  if field=='certificate_document' and not u.scheme:
   target=(page.parent/value).resolve()
   if not target.is_relative_to(website.resolve()) or not target.is_file():raise ValueError('Certificate document not found: '+value)
  elif u.scheme!='https' or not u.hostname:raise ValueError('Use an HTTPS resource URL')
for key,record in records.items():
 card=soup.select_one(f'[data-development-card="{key}"]')
 for tag in card.select('.development-year,.development-date,.development-resources'):tag.decompose()
 year=record.get('completion_year','').strip()
 completed=record.get('completed_on','');attended=record.get('attended_on','')
 if completed or attended:
  tag=soup.new_tag('p');tag['class']='development-date';tag.string=('Completed' if completed else 'Attended')+' \u00b7 '+date.fromisoformat(completed or attended).strftime('%d %B %Y').lstrip('0');card.append(tag)
 elif year:
  tag=soup.new_tag('p');tag['class']='development-year';tag.string='Completion year: '+year;card.append(tag)
 resources=[(record.get(field,'').strip(),label) for field,label in [('course_url','View Course'),('certificate_document','View Certificate'),('credential_url','Verify Credential')] if record.get(field,'').strip()]
 if resources:
  div=soup.new_tag('div');div['class']='development-resources'
  for value,label in resources:
   a=soup.new_tag('a',href=value,target='_blank',rel='noopener noreferrer');a['class']='button secondary';a.string=label+' \u2197';a['aria-label']=label+' (opens in a new tab)';div.append(a)
  card.append(div)
page.write_text(str(soup));print('Professional-development resources updated.')
