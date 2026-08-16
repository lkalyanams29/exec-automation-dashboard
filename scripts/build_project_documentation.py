from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.section import WD_SECTION
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'deliverables'/'Katalon_Automation_Dashboard_Project_Documentation.docx'
SHOT=ROOT/'deliverables'/'video-assets'/'dashboard-overview.png'
BLUE=RGBColor(46,116,181); NAVY=RGBColor(24,35,58); MUTED=RGBColor(103,115,133); PURPLE=RGBColor(107,89,223); LIGHT='F2F4F7'

def font(run,size=11,bold=False,color=NAVY,italic=False):
    run.font.name='Calibri'; run._element.get_or_add_rPr().rFonts.set(qn('w:ascii'),'Calibri'); run._element.rPr.rFonts.set(qn('w:hAnsi'),'Calibri'); run.font.size=Pt(size); run.bold=bold; run.italic=italic; run.font.color.rgb=color
def spacing(p,before=0,after=6,line=1.1):
    p.paragraph_format.space_before=Pt(before);p.paragraph_format.space_after=Pt(after);p.paragraph_format.line_spacing=line
def add_p(doc,text='',bold_lead=None,after=6):
    p=doc.add_paragraph();spacing(p,after=after)
    if bold_lead and text.startswith(bold_lead): font(p.add_run(bold_lead),bold=True);text=text[len(bold_lead):]
    font(p.add_run(text));return p
def heading(doc,text,level=1):
    p=doc.add_paragraph(style=f'Heading {level}');p.paragraph_format.keep_with_next=True
    p.paragraph_format.space_before=Pt(16 if level==1 else 12);p.paragraph_format.space_after=Pt(8 if level==1 else 6)
    for r in p.runs: font(r,16 if level==1 else 13,bold=True,color=BLUE)
    return p
def bullet(doc,text):
    p=doc.add_paragraph(style='List Bullet');spacing(p,after=5,line=1.167);p.paragraph_format.left_indent=Inches(.5);p.paragraph_format.first_line_indent=Inches(-.25);font(p.add_run(text) if not p.runs else p.runs[0]);return p
def number(doc,text):
    p=doc.add_paragraph(style='List Number');spacing(p,after=5,line=1.167);p.paragraph_format.left_indent=Inches(.5);p.paragraph_format.first_line_indent=Inches(-.25);font(p.add_run(text) if not p.runs else p.runs[0]);return p
def shade(cell,fill):
    shd=OxmlElement('w:shd');shd.set(qn('w:fill'),fill);cell._tc.get_or_add_tcPr().append(shd)
def table(doc,headers,rows,widths):
    t=doc.add_table(rows=1,cols=len(headers));t.alignment=WD_TABLE_ALIGNMENT.CENTER;t.autofit=False
    for i,(h,w) in enumerate(zip(headers,widths)):
        t.rows[0].cells[i].width=Inches(w);shade(t.rows[0].cells[i],LIGHT);p=t.rows[0].cells[i].paragraphs[0];spacing(p,after=0);font(p.add_run(h),10,bold=True,color=NAVY)
    for row in rows:
        cells=t.add_row().cells
        for i,(value,w) in enumerate(zip(row,widths)):
            cells[i].width=Inches(w);cells[i].vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER;p=cells[i].paragraphs[0];spacing(p,after=0);font(p.add_run(str(value)),9.5)
    tPr=t._tbl.tblPr;tw=tPr.first_child_found_in('w:tblW');tw.set(qn('w:w'),'9360');tw.set(qn('w:type'),'dxa')
    for row in t.rows:
        for c in row.cells:
            tcPr=c._tc.get_or_add_tcPr();mar=OxmlElement('w:tcMar')
            for side,val in [('top','80'),('bottom','80'),('start','120'),('end','120')]: el=OxmlElement(f'w:{side}');el.set(qn('w:w'),val);el.set(qn('w:type'),'dxa');mar.append(el)
            tcPr.append(mar)
    doc.add_paragraph().paragraph_format.space_after=Pt(0);return t
def page_break(doc): doc.add_page_break()

doc=Document();sec=doc.sections[0];sec.top_margin=sec.bottom_margin=sec.left_margin=sec.right_margin=Inches(1);sec.header_distance=sec.footer_distance=Inches(.492)
styles=doc.styles;normal=styles['Normal'];normal.font.name='Calibri';normal.font.size=Pt(11);normal.font.color.rgb=NAVY
for name,size,before,after,color in [('Heading 1',16,16,8,BLUE),('Heading 2',13,12,6,BLUE),('Heading 3',12,8,4,RGBColor(31,77,120))]:
    st=styles[name];st.font.name='Calibri';st.font.size=Pt(size);st.font.bold=True;st.font.color.rgb=color;st.paragraph_format.space_before=Pt(before);st.paragraph_format.space_after=Pt(after)
header=sec.header.paragraphs[0];header.alignment=WD_ALIGN_PARAGRAPH.LEFT;spacing(header,after=0);font(header.add_run('KATALON TESTOPS AUTOMATION MANAGEMENT DASHBOARD'),8,bold=True,color=MUTED)
footer=sec.footer.paragraphs[0];footer.alignment=WD_ALIGN_PARAGRAPH.RIGHT;run=footer.add_run('Project documentation  |  ');font(run,8,color=MUTED);fld=OxmlElement('w:fldSimple');fld.set(qn('w:instr'),'PAGE');footer._p.append(fld)

p=doc.add_paragraph();spacing(p,before=10,after=2);font(p.add_run('PROJECT DOCUMENTATION'),9,bold=True,color=PURPLE)
p=doc.add_paragraph();spacing(p,after=5);font(p.add_run('Katalon TestOps Automation\nManagement Dashboard'),26,bold=True,color=NAVY)
p=doc.add_paragraph();spacing(p,after=15);font(p.add_run('An executive view of automation growth, execution health, stability, and project performance.'),13,color=MUTED)
meta=[('Prepared','August 16, 2026'),('Application','Private hosted dashboard'),('Primary source','katalon_testops_sample_dataset.csv'),('Technology','React/Vinext, TypeScript, Python, SQLite/D1')]
for label,value in meta:
    p=doc.add_paragraph();spacing(p,after=2);font(p.add_run(f'{label}: '),10,bold=True);font(p.add_run(value),10,color=MUTED)
if SHOT.exists():
    p=doc.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER;spacing(p,before=15,after=4);p.add_run().add_picture(str(SHOT),width=Inches(6.25))
    p=doc.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER;spacing(p,after=0);font(p.add_run('Figure 1. Live executive dashboard using the supplied CSV dataset.'),8,italic=True,color=MUTED)

page_break(doc);heading(doc,'1. Project overview')
add_p(doc,'The dashboard centralizes Katalon TestOps automation reporting across WebOps, Salesforce, BSP Services, and MyKC. It replaces manual weekly reporting with a management-level view that can answer how much automation exists, whether coverage is growing, how often tests run, which projects are healthy, and where stability requires attention.')
heading(doc,'Business outcomes',2)
for x in ['One portfolio view for QE leadership instead of project-by-project spreadsheets.','Consistent definitions for pass rate, failure rate, growth, and flakiness.','Historical weekly and monthly trends that support period-over-period conversations.','Screenshot- and PDF-friendly presentation with low-level technical detail available through drill-down.','Extensible ingestion: Katalon API connectivity plus repeatable monthly CSV imports.']:bullet(doc,x)
heading(doc,'Final application capabilities',2)
table(doc,['Area','What was built'],[
('Executive summary','Portfolio health, automated tests, new tests, pass rate, runs, comparisons, and refresh state.'),('Growth','Weekly new-test bars, cumulative context, and project-level additions.'),('Execution health','Passed/failed/skipped distribution, weekly pass-rate trend, and execution volume.'),('Project performance','Per-project tests, execution outcomes, duration, status, and drill-down entry point.'),('Stability & failures','Flaky-test counts, repeat failures, top failing tests, and extensible failure categories.'),('Data management','API-ready integration, normalized analytics schema, snapshots, and CSV import with validation.'),('Sharing','Print/PDF export, responsive layout, private hosted URL, and social preview asset.')],[1.45,5.05])

page_break(doc);heading(doc,'2. Datasets used')
heading(doc,'Primary dataset',2)
add_p(doc,'The active source is katalon_testops_sample_dataset.csv, supplied for the project and copied into the repository under sources/. A SHA-256 comparison confirmed the repository copy matches the supplied file.')
table(doc,['Property','Observed value'],[('Rows','2,063 execution-result records'),('Projects','4: BSP Services, MyKC, Salesforce, WebOps'),('Distinct automated tests','144'),('Distinct runs','96 across the full file'),('Execution date range','May 26 through August 15, 2026'),('Latest 30-day window','1,117 results; 1,021 passed; 61 failed; 35 skipped'),('Latest-window pass rate','94.4% using Passed / (Passed + Failed)'),('Stability signals','27 flaky tests and 27 repeat-failure rows in the latest window')],[2.15,4.35])
heading(doc,'Important fields',2)
add_p(doc,'The dataset contains execution and test identifiers, project and suite names, test creation timestamps, execution timestamps, environment, browser, status, duration, retry attempts, flakiness flags, repeat-failure indicators, failure category, agent name, and Katalon version. These fields support both executive aggregates and later drill-down.')
heading(doc,'Future monthly imports',2)
for x in ['CSV files are validated before replacing the active source.','Required fields include execution_id, run_id, project_name, test_case_id, test_case_created_at, execution_started_at, status, and duration_seconds.','Optional flakiness and failure-category fields enrich the management view.','Successful imports retain the original CSV and a calculated summary; the latest successful import is loaded on future visits.','Invalid files never replace the current dataset.']:bullet(doc,x)

page_break(doc);heading(doc,'3. Architecture and implementation')
add_p(doc,'The solution separates collection, storage, metric calculation, and presentation. The initial hosted application uses a React/Vinext interface and Cloudflare D1-compatible persistence, while the Python layer provides a reusable Katalon client and SQLite proof-of-concept path.')
for x in ['Katalon TestOps API or monthly CSV export','Defensive ingestion and validation layer','Normalized local analytics database and daily snapshots','Pure metric calculations with documented definitions','Dashboard API and executive React interface']:number(doc,x)
heading(doc,'Clean architecture choices',2)
table(doc,['Component','Responsibility','Representative assets'],[
('Integration','Authentication from environment variables, pagination, retry/backoff, shape discovery.','backend/katalon/'),('Analytics storage','Projects, tests, executions, results, daily metrics, CSV imports.','backend/database/, db/, drizzle/'),('Metrics','Pass/failure rates, growth, health thresholds, flakiness.','backend/metrics/, lib/csv-metrics.ts'),('Application API','Stores and retrieves monthly CSV imports.','app/api/imports/route.ts'),('Management UI','KPIs, trends, project health, failures, summary, imports.','app/Dashboard.tsx'),('Configuration','Projects, thresholds, refresh behavior, secret names.','config/projects.yaml, .env.example')],[1.2,2.65,2.65])
heading(doc,'Data-quality decisions',2)
for x in ['Pass rate excludes skipped and error statuses: Passed / (Passed + Failed).','Duplicate execution records are prevented through execution IDs and composite result keys.','Growth uses test creation timestamps; daily snapshots are the fallback when timestamps are unavailable.','Reporting windows are anchored to the maximum execution date in the active dataset, not the machine clock.','Failure category defaults to Unknown while retaining room for Product, Automation, and Environment classifications.']:bullet(doc,x)

page_break(doc);heading(doc,'4. Prompts used during vibe coding')
add_p(doc,'The build was driven through a sequence of natural-language prompts. The prompts below are concise records of the actual intent used during the workflow; the first prompt was substantially longer and supplied the complete metric, architecture, data-model, and UI specification.')
table(doc,['Stage','Prompt / instruction used'],[
('Initial build','“Build a Katalon TestOps Automation Management Dashboard” followed by detailed requirements for executive KPIs, weekly growth, project metrics, execution trends, failures, flakiness, duration, thresholds, filters, comparisons, drill-down, SQLite/PostgreSQL-ready storage, snapshots, exports, architecture, and phased delivery.'),('Data-source change','“Ensure you use this as data source. Also, add a feature to import CSV as source for future months.”'),('Social preview','“Create a polished executive automation quality dashboard social card” matching the dashboard’s navy, violet, white, green, amber, and red visual system, with exact text “AUTOMATION HEALTH” and “95.5% PASS RATE.”'),('Documentation & handoff','“Create project documentation explaining what you built,” including datasets, vibe-coding prompts, iterations, learnings, a short demo video, and a GitHub link.')],[1.25,5.25])
heading(doc,'How AI coding tools were used',2)
for x in ['Translated a broad management objective into a working application architecture and implementation plan.','Generated the UI, CSV parser, metric engine, API route, database schema, migrations, tests, documentation, and deployment package.','Inspected the supplied dataset to reconcile dashboard figures with source records.','Iterated from compilation and runtime feedback rather than treating generated code as final.','Captured and verified the live hosted interface for the demo and project handoff.']:bullet(doc,x)

page_break(doc);heading(doc,'5. Iterations tried')
table(doc,['Iteration','What changed','Why it mattered'],[
('1. Executive visual prototype','Built the first management screen with representative KPIs, growth, distribution, trends, projects, stability, and summary.','Established information hierarchy and leadership-ready visual direction before live integration.'),('2. Integration foundation','Added environment-based credentials, paginated Katalon client, retries, normalized storage, snapshots, and tested metrics.','Separated API uncertainty from analytics logic and avoided hard-coded credentials or project IDs.'),('3. Source-backed dashboard','Replaced representative values with aggregates from the supplied 2,063-row CSV.','Made the management story traceable to an actual dataset.'),('4. Monthly import workflow','Added drag/drop CSV upload, required-column validation, 5 MB limit, recalculation, durable storage, and latest-import loading.','Made future reporting repeatable without changing application code.'),('5. Data reconciliation','Anchored the default 30-day window to the latest execution date, validated 144 tests and 94.4% pass rate, and added source labels.','Prevented misleading results when sample data dates differ from the current clock.'),('6. Production hardening','Added D1 migration, build/tests, responsive/print styling, private deployment, and documentation.','Converted a prototype into a shareable proof of concept.')],[1.1,2.65,2.75])
heading(doc,'Notable implementation corrections',2)
for x in ['The first dependency setup path was not available in the Windows shell, so the equivalent bundled runtime path was used.','A CSV summary helper initially referenced an undeclared prior-week variable; source-level verification caught and corrected it.','Generated Python cache files were removed from version control and permanently ignored.','The first dashboard used sample values; these were intentionally replaced once the real CSV was provided.']:bullet(doc,x)

page_break(doc);heading(doc,'6. Learnings and observations')
heading(doc,'Product and data lessons',2)
for x in ['Management dashboards benefit from a strong first-screen hierarchy: four KPIs, two trend panels, project health, and a plain-language summary were easier to interpret than a dense execution table.','Metric definitions must be explicit. A pass rate that includes skipped tests would have told a different story from the documented Passed / (Passed + Failed) definition.','Growth is impossible to reconstruct reliably from only a current test count. Test creation dates or daily snapshots are essential.','A reporting window should be anchored to the dataset’s latest date for static or delayed exports; anchoring to today can create an empty dashboard.','CSV import is a practical bridge while TestOps endpoint shapes and tenant permissions are being validated. It also provides an auditable fallback for monthly leadership reporting.']:
    bullet(doc,x)
heading(doc,'AI-assisted development lessons',2)
for x in ['Large prompts are useful for establishing scope, but implementation quality improved when the work was divided into bounded slices: visual shell, integration, storage, metrics, live data, imports, and publishing.','AI-generated code still requires reconciliation against source data, builds, migrations, and targeted assertions. The most valuable verification was checking exact row counts and KPI totals.','A reusable parser and pure metric functions are safer than embedding calculations directly in UI components.','Clear file boundaries made later changes faster: swapping the data source did not require redesigning the dashboard.','The best vibe-coding workflow was conversational but evidence-driven: prompt, build, inspect, test, correct, and only then publish.']:bullet(doc,x)
heading(doc,'Current limitations and next steps',2)
for x in ['Complete Phase 1 against the organization’s live Katalon TestOps tenant and confirm endpoint/field mappings.','Add scheduled incremental synchronization and operational alerting for failed imports or stale data.','Add role-based access for import actions and an import-history screen with rollback.','Expand technical drill-down routes for suites, executions, and individual test cases.','Add server-generated Excel and management-report exports after live database queries are fully wired.']:bullet(doc,x)

page_break(doc);heading(doc,'7. Verification and final result')
add_p(doc,'The final application was validated through a production Vinext build, source-backed CSV assertions, UI content tests, metric checks, D1 migration generation, and a private deployment. The supplied CSV reconciled to 2,063 rows, 144 distinct tests, four projects, 1,117 results in the latest 30-day window, and a 94.4% pass rate.')
heading(doc,'What leadership can answer now',2)
for x in ['How many automated tests exist and how many were added this week?','Is execution volume increasing, and what is the overall pass rate?','Which project performs best and which needs attention?','Are failures, repeat failures, or flaky tests becoming a management concern?','How long do executions take, and which projects are slower?','What changed relative to the prior reporting period?','Which source file is active, and can next month’s data be imported safely?']:bullet(doc,x)
heading(doc,'Final links and assets',2)
table(doc,['Deliverable','Location'],[('Live dashboard','https://katalon-automation-health.satyamlowhitha.chatgpt.site'),('Source dataset','sources/katalon_testops_sample_dataset.csv'),('Setup and technical guide','README.md'),('Project documentation','deliverables/Katalon_Automation_Dashboard_Project_Documentation.docx'),('Demo video','deliverables/Katalon_Automation_Dashboard_Demo.mp4')],[1.8,4.7])

OUT.parent.mkdir(parents=True,exist_ok=True);doc.save(OUT);print(OUT)
