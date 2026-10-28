from pathlib import Path
import html,json,re,urllib.parse
BASE=Path(__file__).resolve().parent
SITE=BASE/'website';PAGE=SITE/'teaching/courses/advanced-linear-algebra.html'
config_path=BASE/'advanced-linear-algebra-links.json'
if not config_path.exists():
 config_path.write_text(json.dumps({'course_folder':'','lectures':'','labs':'','data':''},indent=2)+'\n')
links=json.loads(config_path.read_text())
for key,value in links.items():
 if value:
  parsed=urllib.parse.urlsplit(value)
  if parsed.scheme!='https' or parsed.hostname not in ('drive.google.com','docs.google.com'):
   raise ValueError('Use an HTTPS Google Drive or Google Docs URL for '+key)
def action(key,label):
 url=links.get(key,'')
 if url:return f'<a class="button secondary" href="{html.escape(url,quote=True)}" target="_blank" rel="noopener noreferrer">{label} <span aria-hidden="true">↗</span><span class="sr-only"> (opens in a new tab)</span></a>'
 return '<span class="resource-pending">Folder link coming soon</span>'
folder_icon='''<svg viewBox="0 0 32 32" width="32" height="32" aria-hidden="true" fill="none"><path d="M4 10V8a2 2 0 0 1 2-2h7l3 4h10a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V10Z" stroke="currentColor" stroke-width="1.7"/><path d="M4 12h24" stroke="currentColor" stroke-width="1.7"/></svg>'''
lecture_icon='''<svg viewBox="0 0 32 32" width="32" height="32" aria-hidden="true" fill="none"><path d="M6 5h20v22H6zM11 11h10M11 16h10M11 21h6" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/></svg>'''
lab_icon='''<svg viewBox="0 0 32 32" width="32" height="32" aria-hidden="true" fill="none"><rect x="4" y="5" width="24" height="18" rx="2" stroke="currentColor" stroke-width="1.7"/><path d="M10 11l-3 3 3 3m12-6 3 3-3 3m-4-8-4 10M11 28h10m-5-5v5" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/></svg>'''
data_icon='''<svg viewBox="0 0 32 32" width="32" height="32" aria-hidden="true" fill="none"><ellipse cx="16" cy="7" rx="11" ry="4" stroke="currentColor" stroke-width="1.7"/><path d="M5 7v17c0 2 5 4 11 4s11-2 11-4V7M5 15c0 2 5 4 11 4s11-2 11-4" stroke="currentColor" stroke-width="1.7"/></svg>'''
categories=[('lectures','Lecture materials','Slides, notes &amp; readings','Explore lecture notes, presentation slides, handouts and supporting readings.',lecture_icon,'Notes and slides','Use this folder to find material shared for lectures and review the associated readings.'),('labs','Lab materials','Exercises, notebooks &amp; code','Find practical exercises, lab guides, notebooks and supporting code.',lab_icon,'Practical activities','Use the lab instructions together with any referenced notebooks, scripts and datasets.'),('data','Data materials','Datasets &amp; documentation','Access datasets and supporting documentation for course activities.',data_icon,'Data for your activities','Check each dataset’s accompanying documentation and use it with the relevant lecture or lab.')]
cards=[]
for key,title,kicker,description,icon,detail,body in categories:
 cards.append(f'''<article class="material-card" data-category="{key}" id="{key}"><div class="material-card-head"><span class="material-icon">{icon}</span><span class="material-type">{kicker}</span></div><h3>{title}</h3><p>{description}</p><details><summary>About this folder</summary><div><strong>{detail}</strong><p>{body}</p></div></details><div class="material-action">{action(key,'Open '+title.lower())}</div></article>''')
master=action('course_folder','Advanced Linear Algebra')
pending='' if links.get('course_folder') else '<p class="folder-status">The Google Drive folder will be linked here when available.</p>'
main='''<main id="main" class="course-hub"><div class="page-heading"><a class="breadcrumb" href="../../teaching.html">← Teaching</a><p class="eyebrow">Teaching / Course materials</p><h1>Advanced Linear Algebra</h1><p class="intro">Your course materials, organised in one place. Explore lecture resources, practical activities and datasets.</p></div>
<section class="course-folder" aria-labelledby="course-folder-title"><div class="course-folder-icon">'''+folder_icon+'''</div><div class="course-folder-copy"><p class="eyebrow">Google Drive resource library</p><h2 id="course-folder-title">Advanced Linear Algebra</h2><p>Open the full course folder, or browse a material category below.</p>'''+pending+'''</div><div class="course-folder-action">'''+master+'''</div></section>
<section class="course-library" aria-labelledby="materials-heading"><div class="library-heading"><div><p class="eyebrow">Explore the library</p><h2 id="materials-heading">Choose your materials</h2></div><a class="text-link" href="../../teaching/courses.html">All courses →</a></div><div class="material-filters" role="group" aria-label="Filter course material categories" hidden><button type="button" data-material-filter="all" aria-pressed="true">All materials</button><button type="button" data-material-filter="lectures" aria-pressed="false">Lectures</button><button type="button" data-material-filter="labs" aria-pressed="false">Labs</button><button type="button" data-material-filter="data" aria-pressed="false">Data</button></div><noscript><p class="profile-links"><a href="#lectures">Lecture materials</a><a href="#labs">Lab materials</a><a href="#data">Data materials</a></p></noscript><p class="sr-only" id="material-filter-status" aria-live="polite">Showing all three material categories.</p><div class="material-grid">'''+''.join(cards)+'''</div></section>
<section class="course-help" aria-labelledby="course-help-title"><div><h2 id="course-help-title">Need help finding a resource?</h2><p>If a folder requests access or you cannot find a referenced file, contact Dr. Zaman with the course name and activity.</p></div><a class="button secondary" href="mailto:babar.zaman@giki.edu.pk?subject=Advanced%20Linear%20Algebra%20materials">Ask about a resource <span aria-hidden="true">↗</span></a></section></main>'''
s=PAGE.read_text();s=re.sub(r'<main\b.*?</main>',main,s,flags=re.S)
if 'course-materials.css' not in s:s=s.replace('</head>','<link rel="stylesheet" href="../../assets/course-materials.css"><script defer src="../../assets/course-materials.js"></script></head>')

if 'assets/midnight-gold.css' not in s:s=s.replace('</head>','<link rel="stylesheet" href="../../assets/midnight-gold.css"></head>')

if 'assets/editorial-layout.css' not in s:s=s.replace('</head>','<link rel="stylesheet" href="../../assets/editorial-layout.css"></head>')
s=s.replace('<h1>Advanced Linear Algebra</h1>','<h1>Advanced Linear <span class="gold-word">Algebra</span></h1>')
PAGE.write_text(s)
print('Updated Advanced Linear Algebra materials hub.')
