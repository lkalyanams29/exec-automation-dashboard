export type ProjectMetric={name:string;tests:number;added:number;executed:number;passed:number;failed:number;skipped:number;rate:number;avgDurationSeconds:number;runs:number;flaky:number};
export type WeekMetric={week:string;executed:number;passed:number;failed:number;skipped:number;passRate:number;newTests:number;cumulativeTests:number};
export type FailureMetric={testCase:string;project:string;failures:number;lastFailure:string;category:string};
export type DashboardSummary={source:string;rowCount:number;periodStart:string;periodEnd:string;generatedAt:string;totalTests:number;newThisWeek:number;newLastWeek:number;growthPercent:number;runs:number;executed:number;passed:number;failed:number;skipped:number;passRate:number;passRateChange:number;executionChange:number;avgDurationSeconds:number;longestDurationSeconds:number;shortestDurationSeconds:number;flaky:number;repeatFailures:number;projects:ProjectMetric[];weeks:WeekMetric[];failures:FailureMetric[]};
type Row=Record<string,string>;

export function parseCsv(text:string):Row[]{
 const rows:string[][]=[];let row:string[]=[],cell="",quoted=false;
 for(let i=0;i<text.length;i++){const c=text[i];if(quoted){if(c==='"'&&text[i+1]==='"'){cell+='"';i++}else if(c==='"')quoted=false;else cell+=c}else if(c==='"')quoted=true;else if(c===','){row.push(cell);cell=""}else if(c==='\n'){row.push(cell.replace(/\r$/,""));rows.push(row);row=[];cell=""}else cell+=c}
 if(cell||row.length){row.push(cell.replace(/\r$/,""));rows.push(row)}
 const headers=(rows.shift()||[]).map(x=>x.trim());return rows.filter(r=>r.some(Boolean)).map(r=>Object.fromEntries(headers.map((h,i)=>[h,(r[i]||"").trim()])));
}
const monday=(d:Date)=>{const x=new Date(d);x.setUTCHours(0,0,0,0);x.setUTCDate(x.getUTCDate()-((x.getUTCDay()+6)%7));return x};
const iso=(d:Date)=>d.toISOString().slice(0,10);
const pct=(a:number,b:number)=>b?Math.round(a/b*1000)/10:0;
const mean=(a:number[])=>a.length?a.reduce((x,y)=>x+y,0)/a.length:0;

export function summarizeCsv(text:string,fileName="Imported CSV"):DashboardSummary{
 const all=parseCsv(text);if(!all.length)throw new Error("The CSV contains no data rows.");
 const required=["execution_id","run_id","project_name","test_case_id","test_case_created_at","execution_started_at","status","duration_seconds"];
 const missing=required.filter(k=>!(k in all[0]));if(missing.length)throw new Error(`Missing required columns: ${missing.join(", ")}`);
 const dates=all.map(r=>new Date(r.execution_started_at)).filter(d=>!Number.isNaN(d.valueOf()));if(!dates.length)throw new Error("No valid execution_started_at dates were found.");
 const maxDate=new Date(Math.max(...dates.map(d=>d.valueOf()))),periodStart=new Date(maxDate);periodStart.setUTCDate(periodStart.getUTCDate()-30);
 const currentWeek=monday(maxDate),lastWeek=new Date(currentWeek);lastWeek.setUTCDate(lastWeek.getUTCDate()-7);
 const inPeriod=all.filter(r=>new Date(r.execution_started_at)>=periodStart&&new Date(r.execution_started_at)<=maxDate);
 const priorStart=new Date(periodStart);priorStart.setUTCDate(priorStart.getUTCDate()-30);const prior=all.filter(r=>new Date(r.execution_started_at)>=priorStart&&new Date(r.execution_started_at)<periodStart);
 const unique=(rows:Row[],key:string)=>new Set(rows.map(r=>r[key]).filter(Boolean)).size;
 const newBetween=(start:Date,end:Date)=>unique(all.filter(r=>{const d=new Date(r.test_case_created_at);return d>=start&&d<end}),"test_case_id");
 const status=(rows:Row[],s:string)=>rows.filter(r=>r.status.toUpperCase()===s).length;
 const passed=status(inPeriod,"PASSED"),failed=status(inPeriod,"FAILED"),priorPassed=status(prior,"PASSED"),priorFailed=status(prior,"FAILED");
 const totalTests=unique(all,"test_case_id"),newThisWeek=newBetween(currentWeek,new Date(currentWeek.valueOf()+7*864e5)),newLastWeek=newBetween(lastWeek,currentWeek);
 const projectNames=[...new Set(all.map(r=>r.project_name).filter(Boolean))].sort();
 const projects=projectNames.map(name=>{const history=all.filter(r=>r.project_name===name),g=inPeriod.filter(r=>r.project_name===name),p=status(g,"PASSED"),f=status(g,"FAILED"),dur=g.map(r=>Number(r.duration_seconds)).filter(Number.isFinite);return{name,tests:unique(history,"test_case_id"),added:unique(history.filter(r=>new Date(r.test_case_created_at)>=currentWeek),"test_case_id"),executed:g.length,passed:p,failed:f,skipped:status(g,"SKIPPED"),rate:pct(p,p+f),avgDurationSeconds:Math.round(mean(dur)),runs:unique(g,"run_id"),flaky:unique(g.filter(r=>r.is_flaky==="1"),"test_case_id")}});
 const weekKeys=[...new Set(all.map(r=>r.execution_week_start||iso(monday(new Date(r.execution_started_at)))))] .filter(Boolean).sort();
 let cumulative=0;const createdByWeek=new Map<string,number>();for(const r of all){const k=r.creation_week_start||iso(monday(new Date(r.test_case_created_at)));if(!createdByWeek.has(`${k}|${r.test_case_id}`))createdByWeek.set(`${k}|${r.test_case_id}`,1)}
 const creationCounts=new Map<string,number>();for(const key of createdByWeek.keys()){const k=key.split("|")[0];creationCounts.set(k,(creationCounts.get(k)||0)+1)}
 const weeks=weekKeys.map(week=>{cumulative+=(creationCounts.get(week)||0);const g=all.filter(r=>(r.execution_week_start||iso(monday(new Date(r.execution_started_at))))===week),p=status(g,"PASSED"),f=status(g,"FAILED");return{week,executed:g.length,passed:p,failed:f,skipped:status(g,"SKIPPED"),passRate:pct(p,p+f),newTests:creationCounts.get(week)||0,cumulativeTests:cumulative}}).slice(-7);
 const failureGroups=new Map<string,Row[]>();for(const r of inPeriod.filter(r=>r.status.toUpperCase()==="FAILED")){const a=failureGroups.get(r.test_case_id)||[];a.push(r);failureGroups.set(r.test_case_id,a)}
 const failures=[...failureGroups.values()].map(g=>({testCase:g[0].test_case_name,project:g[0].project_name,failures:g.length,lastFailure:g.map(r=>r.execution_started_at).sort().at(-1)?.slice(0,10)||"",category:g.find(r=>r.failure_category)?.failure_category||"Unknown"})).sort((a,b)=>b.failures-a.failures).slice(0,5);
 const durations=inPeriod.map(r=>Number(r.duration_seconds)).filter(Number.isFinite),priorRate=pct(priorPassed,priorPassed+priorFailed);
 return{source:fileName,rowCount:all.length,periodStart:iso(periodStart),periodEnd:iso(maxDate),generatedAt:new Date().toISOString(),totalTests,newThisWeek,newLastWeek,growthPercent:pct(newThisWeek,totalTests-newThisWeek),runs:unique(inPeriod,"run_id"),executed:inPeriod.length,passed,failed,skipped:status(inPeriod,"SKIPPED"),passRate:pct(passed,passed+failed),passRateChange:Math.round((pct(passed,passed+failed)-priorRate)*10)/10,executionChange:pct(inPeriod.length-prior.length,prior.length),avgDurationSeconds:Math.round(mean(durations)),longestDurationSeconds:Math.max(...durations),shortestDurationSeconds:Math.min(...durations),flaky:unique(inPeriod.filter(r=>r.is_flaky==="1"),"test_case_id"),repeatFailures:inPeriod.filter(r=>r.repeat_failure_flag==="1").length,projects,weeks,failures};
}
