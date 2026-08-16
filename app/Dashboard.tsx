"use client";
import {useState} from "react";

const projects=[
 {name:"WebOps",abbr:"WO",tests:420,added:12,executed:"1,340",passed:"1,295",failed:45,rate:96.6,duration:"22m"},
 {name:"Salesforce",abbr:"SF",tests:315,added:8,executed:"980",passed:"941",failed:39,rate:96.0,duration:"31m"},
 {name:"BSP Services",abbr:"BS",tests:289,added:15,executed:"1,120",passed:"1,077",failed:43,rate:94.0,duration:"18m"},
 {name:"MyKC",abbr:"MK",tests:260,added:7,executed:"1,452",passed:"1,358",failed:94,rate:91.8,duration:"28m"},
];
const kpis=[
 {label:"Automated tests",value:"1,284",delta:"+3.4%",note:"vs last week",icon:"▤"},
 {label:"New tests",value:"+42",delta:"+35.5%",note:"31 last week",icon:"+"},
 {label:"Pass rate",value:"95.5%",delta:"+1.2%",note:"vs last week",icon:"✓"},
 {label:"Test runs",value:"186",delta:"+8.1%",note:"vs last week",icon:"▶"},
];
const weeks=[22,37,41,28,34,31,42];

export default function Dashboard(){
 const [period,setPeriod]=useState("Last 30 days"); const [project,setProject]=useState<string|null>(null); const [refreshed,setRefreshed]=useState("Aug 16, 2026 · 4:00 PM ET");
 return <main>
  <aside><div className="brand"><b>K</b><span><strong>TestOps</strong><small>Automation intelligence</small></span></div><nav>{[["⌂","Overview"],["↗","Automation growth"],["◎","Execution health"],["▦","Projects"],["◇","Stability"],["!","Failure analysis"]].map((x,i)=><a className={i===0?"on":""} href={`#${i}`} key={x[1]}><i>{x[0]}</i>{x[1]}</a>)}</nav><div className="sync"><i/><span><b>Data sync healthy</b><small>4 projects connected</small></span></div></aside>
  <section className="page">
   <header><div><p className="eyebrow">QUALITY ENGINEERING / PORTFOLIO</p><h1>Automation health</h1><p>A clear view of coverage, quality and execution across your automation portfolio.</p></div><div className="actions"><select value={period} onChange={e=>setPeriod(e.target.value)} aria-label="Date range">{["Today","Last 7 days","Last 30 days","This month","Last month","This quarter"].map(x=><option key={x}>{x}</option>)}</select><button onClick={()=>window.print()}>⇩ Export</button><button className="primary" onClick={()=>setRefreshed("Just now")}>↻ Refresh data</button></div></header>
   <div className="status"><b><i/> Portfolio health: Green</b><span>Last refreshed {refreshed}</span><button>Manage thresholds →</button></div>
   <section className="kpis">{kpis.map((k,i)=><article className="card kpi" key={k.label}><div><span>{k.label}</span><i className={`ki c${i}`}>{k.icon}</i></div><strong>{k.value}</strong><p><b>↑ {k.delta}</b> {k.note}</p></article>)}</section>
   <section className="grid wide" id="1">
    <article className="card growth"><Title over="AUTOMATION GROWTH" title="New tests added per week" extra={<span className="legend">■ New tests　━ Cumulative</span>}/><div className="metric"><b>+42</b><span>this week</span><em>↑ 35.5%</em></div><div className="bars">{weeks.map((v,i)=><div key={i}><span>{v}</span><i style={{height:v*2.2}}/><small>{["Jul 6","Jul 13","Jul 20","Jul 27","Aug 3","Aug 10","Aug 17"][i]}</small></div>)}</div>
    </article>
    <article className="card distribution"><Title over="EXECUTION HEALTH" title="Result distribution"/><div className="donut"><span><b>4,892</b><small>tests executed</small></span></div><div className="results">{[["Passed","4,671","95.5%","green"],["Failed","181","3.7%","red"],["Skipped","40","0.8%","amber"]].map(x=><div key={x[0]}><span><i className={x[3]}/>{x[0]}</span><b>{x[1]}</b><em>{x[2]}</em></div>)}</div></article>
   </section>
   <section className="grid wide second" id="2">
    <article className="card"><Title over="PASS RATE TREND" title="Weekly execution quality" extra={<span className="target">Target 95%</span>}/><div className="linechart"><div className="targetline">95%</div><div className="stroke"/>{[94.2,95.6,95.1,96.8,96.1,94.3,95.5].map((v,i)=><i key={i} style={{left:`${5+i*15}%`,bottom:`${20+(v-90)*13}px`}} title={`${v}%`}/>)}</div><div className="labels">{["Jul 6","Jul 13","Jul 20","Jul 27","Aug 3","Aug 10","Aug 17"].map(x=><small key={x}>{x}</small>)}</div></article>
    <article className="card volume"><Title over="EXECUTION VOLUME" title="Tests executed" extra={<span className="good">↑ 10.1%</span>}/><div className="metric"><b>4,892</b><span>this week</span></div>{[["WebOps",1340,"purple"],["Salesforce",980,"blue"],["BSP Services",1120,"teal"],["MyKC",1452,"orange"]].map(x=><div className="progress" key={x[0]}><span>{x[0]}</span><i><b className={x[2]} style={{width:`${Number(x[1])/15}px`}}/></i><strong>{Number(x[1]).toLocaleString()}</strong></div>)}</article>
   </section>
   <section className="card projects" id="3"><Title over="PROJECT PERFORMANCE" title="Portfolio overview" extra={<button>View all projects →</button>}/><div className="table"><table><thead><tr>{["Project","Automated tests","New this week","Tests executed","Passed","Failed","Pass rate","Avg duration","Status"].map(x=><th key={x}>{x}</th>)}</tr></thead><tbody>{projects.map(p=><tr key={p.name} onClick={()=>setProject(p.name)}><td><i>{p.abbr}</i><b>{p.name}</b></td><td>{p.tests}</td><td className="good">+{p.added}</td><td>{p.executed}</td><td>{p.passed}</td><td>{p.failed}</td><td><b>{p.rate}%</b><span className="track"><i className={p.rate>=95?"green":"amber"} style={{width:`${p.rate}%`}}/></span></td><td>{p.duration}</td><td><span className={`health ${p.rate>=95?"healthy":"watch"}`}><i/>{p.rate>=95?"Healthy":"Watch"}</span></td></tr>)}</tbody></table></div></section>
   <section className="bottom" id="4"><article className="card summary"><p className="eyebrow">WEEKLY MANAGEMENT SUMMARY</p><h2>Automation is healthy and growing</h2><p>Coverage continues to expand while execution stability remains above the portfolio target. <b>42 new tests</b> were added and pass rate improved by <b>1.2 points</b>.</p><div><span><small>BEST PERFORMING</small><b>WebOps · 96.6%</b></span><span><small>REQUIRES ATTENTION</small><b>MyKC · 91.8%</b></span></div></article>{[["◇","Flaky tests","14","↓ 3 this week"],["!","Failed tests","181","↑ 12 this week"],["◷","Avg duration","24m","↓ 1.4m faster"]].map((x,i)=><article className="card mini" key={x[1]}><i className={`m${i}`}>{x[0]}</i><span><small>{x[1]}</small><b>{x[2]}</b><em className={i===1?"bad":"good"}>{x[3]}</em></span></article>)}</section>
  </section>
  {project&&<div className="backdrop" onClick={()=>setProject(null)}><article className="modal" onClick={e=>e.stopPropagation()}><button onClick={()=>setProject(null)}>×</button><p className="eyebrow">PROJECT DRILL-DOWN</p><h2>{project}</h2><p>Suite-level execution details, failure patterns and individual test cases will appear here from the analytics store.</p><div><b>Organization</b> → <b>{project}</b> → Test suites → Executions</div><button className="primary">Open project dashboard</button></article></div>}
 </main>
}
function Title({over,title,extra}:{over:string,title:string,extra?:React.ReactNode}){return <div className="title"><div><p className="eyebrow">{over}</p><h2>{title}</h2></div>{extra}</div>}
