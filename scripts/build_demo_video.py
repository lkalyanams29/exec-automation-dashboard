from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageFilter
import subprocess,sys,wave,json

ROOT=Path(__file__).resolve().parents[1];ASSETS=ROOT/'deliverables'/'video-assets';WORK=ROOT/'work'/'demo-video';OUT=ROOT/'deliverables'/'Katalon_Automation_Dashboard_Demo.mp4';WORK.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(ROOT/'work'/'video-deps'));import imageio_ffmpeg
FFMPEG=imageio_ffmpeg.get_ffmpeg_exe();W,H=1920,1080
NAVY=(18,31,57);PURPLE=(107,89,223);WHITE=(255,255,255);MUTED=(191,201,219);GREEN=(41,163,111)
def f(size,bold=False):
    choices=['C:/Windows/Fonts/segoeuib.ttf' if bold else 'C:/Windows/Fonts/segoeui.ttf','C:/Windows/Fonts/arial.ttf'];return ImageFont.truetype(next(x for x in choices if Path(x).exists()),size)
def fit(img,box):
    img=img.copy();img.thumbnail((box[2],box[3]),Image.Resampling.LANCZOS);return img
def base(kicker,title,subtitle):
    im=Image.new('RGB',(W,H),(246,248,252));d=ImageDraw.Draw(im);d.rounded_rectangle((55,45,W-55,H-45),32,fill=WHITE,outline=(226,231,240),width=2);d.rounded_rectangle((55,45,250,H-45),32,fill=NAVY);d.rectangle((210,45,250,H-45),fill=NAVY);d.rounded_rectangle((95,95,175,175),18,fill=PURPLE);d.text((123,104),'K',font=f(44,True),fill=WHITE);d.text((300,90),kicker.upper(),font=f(22,True),fill=PURPLE);d.text((300,130),title,font=f(52,True),fill=NAVY);d.text((300,205),subtitle,font=f(24),fill=(91,105,129));return im,d
def add_footer(d,idx): d.text((300,H-90),'Katalon TestOps Automation Management Dashboard',font=f(17),fill=(128,139,157));d.text((W-150,H-90),f'{idx}/6',font=f(17,True),fill=PURPLE)
def add_caption(d,text):
    d.rounded_rectangle((285,H-215,W-90,H-125),18,fill=(22,33,58));d.text((325,H-190),text,font=f(25,True),fill=WHITE)

overview=Image.open(ASSETS/'dashboard-overview.png').convert('RGB');full=Image.open(ASSETS/'dashboard-full.png').convert('RGB');imp=Image.open(ASSETS/'csv-import.png').convert('RGB')
scenes=[]
im,d=base('Project demo','Automation health, without manual reporting','A management-ready dashboard for growth, execution quality, stability, and project performance.');pic=fit(overview,(0,0,1450,680));im.paste(pic,(325,280));add_caption(d,'Live, source-backed portfolio reporting in one view');add_footer(d,1);scenes.append(im)
im,d=base('Executive overview','Start with the questions leadership asks first','Coverage, new tests, pass rate, and run volume are visible before technical execution detail.');pic=fit(overview,(0,0,1470,720));im.paste(pic,(310,270));add_caption(d,'144 automated tests  •  94.4% pass rate  •  39 runs');add_footer(d,2);scenes.append(im)
im,d=base('Trends and health','See growth and execution quality over time','Weekly trends, result distribution, and project execution volume make changes easy to explain.');crop=full.crop((0,330,1264,1120));pic=fit(crop,(0,0,1470,660));im.paste(pic,(310,290));add_caption(d,'The reporting window follows the latest date in the active dataset');add_footer(d,3);scenes.append(im)
im,d=base('Project and failure analysis','Move from portfolio health to action','Project comparisons identify where leadership should celebrate and where teams should investigate.');crop=full.crop((0,850,1264,1741));pic=fit(crop,(0,0,1470,650));im.paste(pic,(310,300));add_caption(d,'Project performance  •  repeat failures  •  flaky tests  •  duration');add_footer(d,4);scenes.append(im)
im,d=base('Monthly CSV workflow','Refresh future months without code changes','A guided import validates the Katalon schema, recalculates every metric, and preserves the last valid source.');pic=fit(imp,(0,0,1470,720));im.paste(pic,(310,270));add_caption(d,'Drag, drop, validate, calculate, and retain');add_footer(d,5);scenes.append(im)
im,d=base('AI-assisted delivery','From a detailed prompt to a deployed application','AI coding tools accelerated the UI, data model, metric engine, tests, documentation, and private deployment.');steps=[('1','Prompt & scope'),('2','Build slices'),('3','Reconcile data'),('4','Test & migrate'),('5','Publish')];x=330
for num,label in steps:d.rounded_rectangle((x,370,x+250,545),22,fill=(245,243,255),outline=(214,208,248),width=3);d.ellipse((x+18,392,x+70,444),fill=PURPLE);d.text((x+36,399),num,font=f(24,True),fill=WHITE,anchor='mm');d.text((x+20,475),label,font=f(23,True),fill=NAVY);x+=285
d.text((330,640),'Key learning',font=f(24,True),fill=GREEN);d.text((330,685),'Vibe coding worked best as an evidence-driven loop: prompt → build → inspect → test → correct → publish.',font=f(29,True),fill=NAVY);d.text((330,790),'Live application',font=f(18,True),fill=PURPLE);d.text((330,825),'katalon-automation-health.satyamlowhitha.chatgpt.site',font=f(25),fill=(75,88,112));add_footer(d,6);scenes.append(im)

narrations=[
"Welcome to the Katalon TestOps Automation Management Dashboard. I built this application to give quality engineering leadership one place to understand automation coverage, execution health, stability, and project performance. The dashboard is designed for screenshots and management reviews, while still supporting drill-down when technical detail is needed.",
"The first screen answers the questions leadership asks most often. The active dataset contains one hundred forty-four automated tests across four projects. For the latest thirty-day reporting window, the dashboard shows thirty-nine distinct runs, one thousand one hundred seventeen test results, and a ninety-four point four percent pass rate. Every card includes comparison context, and the portfolio status uses configurable green, yellow, and red thresholds.",
"Below the key indicators, weekly views explain what changed. The automation growth chart uses test creation dates and shows cumulative coverage. Result distribution separates passed, failed, and skipped outcomes. Pass rate follows the documented formula of passed divided by passed plus failed, so skipped tests do not distort the quality signal. Execution volume is also broken down by project, making changes visible without reading raw test logs.",
"The project table provides the next level of detail. It compares automated tests, executions, passes, failures, pass rate, duration, and management status for WebOps, Salesforce, BSP Services, and MyKC. The failure section surfaces repeated failures and the most frequently failing tests. The data model also supports product, automation, environment, and unknown failure categories, so teams can extend classification later.",
"For this version, I used the supplied Katalon TestOps CSV containing two thousand sixty-three execution records. I added a monthly import feature so future reporting does not require code changes. Users can drag and drop a CSV, and the application validates required columns before updating anything. A successful import recalculates all metrics and becomes the source for future visits. An invalid import leaves the current dashboard unchanged.",
"I used AI coding tools throughout the workflow. The initial prompt described the executive metrics, architecture, data model, filters, trends, and phased delivery. I then iterated in bounded slices: first the management interface, then API and storage foundations, then source-backed calculations, monthly imports, tests, and publishing. The most important lesson was that vibe coding still needs evidence. I reconciled row counts and key metrics against the CSV, generated database migrations, ran production builds, corrected defects, and only then deployed. The result is a reusable proof of concept that can move from CSV reporting to live Katalon synchronization without redesigning the application."
]
ps='C:/Windows/System32/WindowsPowerShell/v1.0/powershell.exe';parts=[];durations=[]
for i,(im,text) in enumerate(zip(scenes,narrations),1):
    img=WORK/f'scene-{i}.png';txt=WORK/f'narration-{i}.txt';wav=WORK/f'narration-{i}.wav';mp4=WORK/f'part-{i}.mp4';im.save(img,quality=95);txt.write_text(text,encoding='utf-8')
    subprocess.run([ps,'-NoProfile','-ExecutionPolicy','Bypass','-File',str(ROOT/'scripts'/'render_narration.ps1'),'-TextPath',str(txt),'-OutputPath',str(wav)],check=True)
    with wave.open(str(wav),'rb') as w: dur=w.getnframes()/w.getframerate()
    durations.append(round(dur,1));subprocess.run([FFMPEG,'-y','-loop','1','-i',str(img),'-i',str(wav),'-t',str(dur+.4),'-r','30','-vf','scale=1920:1080,format=yuv420p','-c:v','libx264','-preset','medium','-crf','20','-c:a','aac','-b:a','160k','-shortest',str(mp4)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);parts.append(mp4)
concat=WORK/'concat.txt';concat.write_text('\n'.join(f"file '{p.as_posix()}'" for p in parts),encoding='utf-8');subprocess.run([FFMPEG,'-y','-f','concat','-safe','0','-i',str(concat),'-c','copy',str(OUT)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
print(json.dumps({'output':str(OUT),'seconds':round(sum(durations),1),'segments':durations,'bytes':OUT.stat().st_size}))
