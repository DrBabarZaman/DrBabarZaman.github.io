# Student card fields

Edit supervision-record-data.json and run update_student_research.py. Optional values remain hidden while blank.

- name, research, research_kind: full name and exact title; retain area for broader research descriptions.
- degree, university: existing confirmed identity fields.
- year: existing recorded year, never interpreted as a graduation date.
- status and status_confirmed: ongoing or graduate, shown only when confirmed.
- completion_year and completion_year_confirmed: a separately confirmed completion year; shown only for a confirmed graduate. Existing year is not automatically reused as completion year.
- research_summary: the student-supplied 2–3 sentence summary; omitted until supplied.
- links.linkedin and links.google_scholar: supplied HTTPS profiles.
- links.thesis and links.related_publication: supplied public resources. For multiple publications use related_publications with objects containing title and url.
- current_position and current_organisation: shown only for confirmed graduates, when supplied.
- supervision_role and role_confirmed: Supervisor or Co-supervisor, explicitly confirmed.
- research_tags: maximum three topic-based labels. GitHub remains optional under links.github as previously requested.

No new facts, roles, statuses, positions, organisations or URLs have been added. Refer to SUPERVISION-EDITING-NOTES.md for unresolved source verification.
