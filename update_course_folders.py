"""Apply course-folder-links.json to the existing course pages without changing their design."""
from pathlib import Path
from urllib.parse import urlsplit
from bs4 import BeautifulSoup
import json
root=Path(__file__).resolve().parent
config=json.loads((root/'course-folder-links.json').read_text())
# Validate all links before writing any files.
for course in config.values():
 for key in ('course','lectures','labs','data'):
  value=course.get(key,'').strip()
  if value:
   url=urlsplit(value)
   if url.scheme!='https' or not (url.hostname in ('drive.google.com','onedrive.live.com','1drv.ms') or (url.hostname or '').endswith('.sharepoint.com')):
    raise ValueError(f'{course["name"]}: {key} must be an HTTPS Google Drive or OneDrive folder link')
for slug,course in config.items():
 page=root/'website/teaching/courses'/f'{slug}.html'
 soup=BeautifulSoup(page.read_text(),'html.parser')
 for key in ('course','lectures','labs','data'):
  slot=soup.select_one(f'[data-folder-slot="{key}"]');slot.clear();value=course.get(key,'').strip()
  if value:
   a=soup.new_tag('a',href=value,target='_blank',rel='noopener noreferrer');a['class']='button';a.string=('Open course folder' if key=='course' else 'Open '+{'lectures':'lecture','labs':'lab','data':'data'}[key]+' folder')+' ↗';slot.append(a)
  else:
   span=soup.new_tag('span');span['class']='drive-pending';span.string='Course folder link coming soon' if key=='course' else 'Folder link coming soon';slot.append(span)
 page.write_text(str(soup))
print('Course folder links updated.')
