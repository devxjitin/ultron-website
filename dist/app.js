(()=>{
'use strict';
const $=(s,r=document)=>r.querySelector(s),$$=(s,r=document)=>[...r.querySelectorAll(s)];
const still=matchMedia('(prefers-reduced-motion: reduce)').matches;
const clamp=(v,a,b)=>Math.min(b,Math.max(a,v));
let paused=still;
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
// wait ms, then keep waiting while motion is paused or the scene is off screen
const nap=async(el,ms)=>{await sleep(ms);while(paused||(el&&!el._vis))await sleep(250)};
const show=(el,on=true)=>el&&el.classList.toggle('show',on);
async function typeInto(el,text,ms,host,tok){
  el.textContent='';
  for(const ch of Array.from(text)){
    if(tok&&tok.dead)return false;
    el.textContent+=ch;await nap(host,ms);
  }
  return true;
}

/* ---------- page chrome ---------- */
const tg=$('.menu-toggle'),links=$('#nav-links');
const closeNav=()=>{links.classList.remove('open');tg.setAttribute('aria-expanded','false')};
tg.addEventListener('click',()=>{const o=links.classList.toggle('open');tg.setAttribute('aria-expanded',o)});
$$('a',links).forEach(a=>a.addEventListener('click',closeNav));

/* smooth inertial scrolling (Lenis); native scrolling if it fails to load or motion is reduced */
let lenis=null;
if(window.Lenis&&!still){
  lenis=new Lenis({duration:1.25,easing:t=>Math.min(1,1.001-Math.pow(2,-10*t)),smoothWheel:true});
  const raf=t=>{lenis.raf(t);requestAnimationFrame(raf)};requestAnimationFrame(raf);
  $$('a[href^="#"]').forEach(a=>a.addEventListener('click',e=>{
    const id=a.getAttribute('href');if(id.length<2)return;
    const el=$(id);if(!el)return;
    e.preventDefault();lenis.scrollTo(el,{offset:-76,duration:1.7});
  }));
}

/* scroll-linked effects: word-by-word text scrub and the install line */
const prog=$('#progress'),stepsEl=$('#steps');
function splitScrub(el){
  const ws=[];
  const walk=n=>[...n.childNodes].forEach(c=>{
    if(c.nodeType===3){
      const frag=document.createDocumentFragment();
      c.textContent.split(/(\s+)/).forEach(tok=>{
        if(!tok)return;
        if(/^\s+$/.test(tok))frag.appendChild(document.createTextNode(tok));
        else{const s=document.createElement('span');s.className='w';s.textContent=tok;frag.appendChild(s);ws.push(s)}
      });
      c.replaceWith(frag);
    }else walk(c);
  });
  walk(el);return ws;
}
const scrubs=$$('[data-scrub]').map(el=>({el,ws:splitScrub(el)}));
if(still)scrubs.forEach(s=>s.ws.forEach(w=>w.classList.add('lit')));
function fx(){
  const vh=innerHeight,y=scrollY;
  if(!still){
    // read phase first, write phase after, so the browser lays out once per frame
    const sr=stepsEl?stepsEl.getBoundingClientRect():null;
    const scr=scrubs.map(s=>s.el.getBoundingClientRect().top);
    scrubs.forEach((s,k)=>{
      const lit=Math.ceil(clamp((vh*.9-scr[k])/(vh*.55),0,1)*s.ws.length);
      if(lit!==s.lit){s.ws.forEach((w,i)=>w.classList.toggle('lit',i<lit));s.lit=lit}
    });
    if(sr)stepsEl.style.setProperty('--sp',clamp((vh*.72-sr.top)/sr.height,0,1).toFixed(3));
  }
}
const work=()=>{
  const max=document.documentElement.scrollHeight-innerHeight;
  prog.style.transform=`scaleX(${max>0?clamp(scrollY/max,0,1):0})`;
  fx();
};
let tick=false;
const onScroll=()=>{
  if(tick)return;tick=true;
  requestAnimationFrame(()=>{tick=false;work()});
};
// with Lenis, work in the same frame it moves the page; otherwise throttle native scroll events
if(lenis)lenis.on('scroll',work);else addEventListener('scroll',onScroll,{passive:true});
addEventListener('resize',onScroll);

// nav highlight
const navA=$$('.nav-links a');
const secIO=new IntersectionObserver(es=>es.forEach(e=>{
  if(!e.isIntersecting)return;
  navA.forEach(a=>a.classList.toggle('on',a.getAttribute('href')==='#'+e.target.id));
}),{rootMargin:'-45% 0px -50% 0px'});
navA.forEach(a=>{const s=$(a.getAttribute('href'));if(s)secIO.observe(s)});

const hero=$('#top'),hph=$('#hphone');

// reveal on scroll
// two-way: animates in from whichever edge it enters, and resets once fully out of view so it replays
const rio=new IntersectionObserver(es=>es.forEach(e=>{
  const t=e.target;
  if(e.intersectionRatio>=.12||(e.isIntersecting&&e.intersectionRect.height>=innerHeight*.5)){
    t.classList.add('in');
  }else if(!e.isIntersecting&&!still){
    t.classList.remove('in');
    t.classList.toggle('from-top',e.boundingClientRect.bottom<=0);
  }
}),{threshold:[0,.12],rootMargin:'0px 0px -6% 0px'});
const observeRv=el=>rio.observe(el);
$$('.rv').forEach(observeRv);

// count up
const cio=new IntersectionObserver(es=>es.forEach(e=>{
  if(!e.isIntersecting)return;cio.unobserve(e.target);
  const b=e.target,n=+b.dataset.count,suf=b.dataset.suffix||'';
  if(still){b.textContent=n+suf;return}
  const t0=performance.now(),d=1400;
  const step=t=>{const p=Math.min(1,(t-t0)/d);b.textContent=Math.round(n*(1-Math.pow(1-p,3)))+(p===1?suf:'');if(p<1)requestAnimationFrame(step)};
  requestAnimationFrame(step);
}),{threshold:.6});
$$('[data-count]').forEach(b=>cio.observe(b));

/* ---------- ribbons (canvas waves like the app's voice ribbon) ---------- */
const ribbons=[];
function makeRibbon(canvas,host,o){
  const r={c:canvas,x:canvas.getContext('2d'),host,amp:o.amp,a:o.amp,mid:o.mid,layers:o.layers,seed:Math.random()*10,grad:null,w:0,h:0,dpr:1};
  const fit=()=>{r.dpr=Math.min(1.5,devicePixelRatio||1);r.w=canvas.width=Math.max(2,Math.round(canvas.clientWidth*r.dpr));r.h=canvas.height=Math.max(2,Math.round(canvas.clientHeight*r.dpr));
    const g=r.x.createLinearGradient(0,0,r.w,0);g.addColorStop(0,'rgba(255,77,63,0)');g.addColorStop(.3,'rgba(255,77,63,1)');g.addColorStop(.7,'rgba(227,48,59,1)');g.addColorStop(1,'rgba(227,48,59,0)');r.grad=g};
  fit();new ResizeObserver(fit).observe(canvas);
  ribbons.push(r);return r;
}
function drawRibbon(r,t){
  const {x,w,h}=r;x.clearRect(0,0,w,h);
  r.a+=(r.amp-r.a)*.07;
  const mid=h*r.mid;
  x.lineWidth=1.3*r.dpr;x.strokeStyle=r.grad;
  for(let k=0;k<r.layers;k++){
    const f=k/r.layers;
    x.globalAlpha=Math.pow(1-f,1.6)*.85+.04;
    x.beginPath();
    for(let i=0;i<=w;i+=12){
      const u=i/w,env=Math.pow(Math.sin(Math.PI*u),1.2);
      const y=mid+env*h*r.a*(Math.sin(u*5.2+t*1.05+f*.9+r.seed)*.62+Math.sin(u*9.1-t*.8+f*1.4)*.26+Math.sin(u*2.3+t*.45)*.5)+f*h*.05*env*(1+r.a*3);
      i?x.lineTo(i,y):x.moveTo(i,y);
    }
    x.stroke();
  }
  x.globalAlpha=1;
}
const rbVoice=makeRibbon($('#wave'),$('[data-scene=voice]'),{amp:.1,mid:.5,layers:16});
if(still){ribbons.forEach(r=>drawRibbon(r,1))}
else{
  const loop=ms=>{if(!paused)for(const r of ribbons)if(r.host._vis)drawRibbon(r,ms/1000);requestAnimationFrame(loop)};
  requestAnimationFrame(loop);
}

/* ---------- scene runner ---------- */
const S={};
const sio=new IntersectionObserver(es=>es.forEach(e=>{
  const el=e.target;el._vis=e.isIntersecting;
  if(e.isIntersecting&&!el._started){el._started=true;boot(el)}
}),{rootMargin:'-6% 0px -6% 0px'});
async function boot(el){
  const f=S[el.dataset.scene];if(!f)return;
  if(still){f.still&&f.still(el);return}
  if(f.init){f.init(el);return}
  for(;;){try{await f.play(el)}catch(err){console.error(err);return}}
}
$$('[data-scene]').forEach(el=>{el._vis=false;sio.observe(el)});

/* hero: typed example commands; the phone shows the listening screen while one is typed */
const CMDS=['Turn on the flashlight','Set an alarm for 6:30 tomorrow','Save this song as audio',"What's the weather tomorrow?",'Message Ria that I am on my way','Remind me about the 4 pm meeting','What did I say on Tuesday?','When is my chemistry exam?'];
const typed=$('#typed');
let hi=0;
S.hero={
  still(){typed.textContent=CMDS[0]},
  async play(el){
    const c=CMDS[hi++%CMDS.length];
    hph.classList.add('listening');
    await typeInto(typed,c,38,el);
    await nap(el,1600);
    hph.classList.remove('listening');
    await nap(el,900);
  }
};

/* voice scene */
S.voice={
  still(s){$('#vy').textContent='Turn the brightness down.';$('#va').textContent='Done. Brightness is at 30%.';show($('#vy'));show($('#va'));$('#vst').textContent='Speaking';$('#vtm').textContent='0:06'},
  async play(s){
    const st=$('#vst'),tm=$('#vtm'),y=$('#vy'),a=$('#va');
    const rounds=[
      {u:'Turn the brightness down.',a:'Done. Brightness is at 30%.'},
      {u:"What's the weather tomorrow?",a:'Tomorrow looks sunny, with a high of 3',cut:'Wait, set a timer for ten minutes.',a2:'Timer set. Ten minutes, starting now.'}
    ];
    let sec=0;tm.textContent='0:00';
    const clock=setInterval(()=>{if(!paused&&s._vis){sec++;tm.textContent='0:'+String(sec%60).padStart(2,'0')}},1000);
    for(const r of rounds){
      show(y,false);show(a,false);y.textContent=a.textContent='';
      st.textContent='Listening';rbVoice.amp=.1;await nap(s,900);
      show(y);rbVoice.amp=.3;await typeInto(y,r.u,34,s);
      rbVoice.amp=.08;st.textContent='Thinking';await nap(s,900);
      st.textContent='Speaking';rbVoice.amp=.36;show(a);await typeInto(a,r.a,38,s);
      if(r.cut){
        await nap(s,500);st.textContent='Interrupted';rbVoice.amp=.5;await nap(s,500);
        show(a,false);y.textContent='';rbVoice.amp=.3;st.textContent='Listening';await typeInto(y,r.cut,34,s);
        rbVoice.amp=.1;st.textContent='Thinking';await nap(s,700);
        st.textContent='Speaking';rbVoice.amp=.36;a.textContent='';show(a);await typeInto(a,r.a2,38,s);
      }
      rbVoice.amp=.1;await nap(s,2000);
    }
    clearInterval(clock);
  }
};

/* phone control scene */
S.phone={
  still(){$('#mout').classList.add('show');$$('#plog li').forEach(l=>l.classList.add('done'))},
  async play(s){
    const cur=$('#cur'),field=$('#mfield'),send=$('#msend'),out=$('#mout'),scan=$('#scanl'),tags=['#tg1','#tg2','#tg3'].map(q=>$(q)),log=$$('#plog li');
    const mark=i=>{log.forEach((l,k)=>{l.classList.toggle('on',k===i);l.classList.toggle('done',k<i)})};
    const tap=async()=>{cur.classList.remove('tap');void cur.offsetWidth;cur.classList.add('tap');await nap(s,350)};
    show(out,false);field.textContent='';field.classList.remove('act');tags.forEach(t=>show(t,false));log.forEach(l=>l.classList.remove('on','done'));
    cur.style.left='150px';cur.style.top='120px';scan.classList.remove('go');
    await nap(s,700);
    mark(0);void scan.offsetWidth;scan.classList.add('go');
    for(const t of tags){await nap(s,380);show(t)}
    await nap(s,900);
    mark(1);cur.style.left='84px';cur.style.top='324px';await nap(s,800);await tap();field.classList.add('act');
    mark(2);await typeInto(field,'On my way',70,s);await nap(s,500);
    mark(3);cur.style.left='186px';cur.style.top='324px';await nap(s,800);send.classList.add('press');await tap();send.classList.remove('press');
    field.textContent='';field.classList.remove('act');show(out);
    log.forEach(l=>{l.classList.remove('on');l.classList.add('done')});
    cur.style.left='120px';cur.style.top='190px';
    await nap(s,3200);
  }
};

/* knowledge / ObjectBox scene */
S.know={
  still(s){s.dataset.step='5';$$('.st5 li',s).forEach((l,i)=>l.classList.toggle('on',i===4))},
  async play(s){
    const lis=$$('.st5 li',s);
    const set=n=>{s.dataset.step=n;lis.forEach((l,i)=>l.classList.toggle('on',i===n-1))};
    set(0);await nap(s,700);
    for(const [n,d] of [[1,1500],[2,2000],[3,2100],[4,2100],[5,5200]]){set(n);await nap(s,d)}
    set(0);await nap(s,1100);
  }
};

/* memory scene */
S.mem={
  still(s){['#m1','#m2','#m3','#m4','#m5','#fact'].forEach(q=>show($(q)));$('#brain').classList.add('glow')},
  async play(s){
    const q=i=>$('#m'+i),fact=$('#fact'),brain=$('#brain');
    [1,2,3,4,5].forEach(i=>show(q(i),false));show(fact,false);brain.classList.remove('glow');
    await nap(s,600);show(q(1));await nap(s,1500);show(q(2));await nap(s,700);
    brain.classList.add('glow');show(fact);await nap(s,1900);
    show(q(3));await nap(s,1300);show(q(4));await nap(s,1400);show(q(5));await nap(s,4200);
  }
};

/* YouTube downloads scene */
S.yt={
  still(){['#y1','#y2','#y3','#y4','#y5','#y6'].forEach(q=>show($(q)));$('#yq').classList.add('pick');$('#ybar').style.width='100%';$('#ypc').textContent='100%';$('#ypl').textContent='Saved'},
  async play(s){
    const ids=['#y1','#y2','#y3','#y4','#y5','#y6'].map(q=>$(q)),bar=$('#ybar'),pc=$('#ypc'),pl=$('#ypl'),yq=$('#yq');
    ids.forEach(e=>show(e,false));yq.classList.remove('pick');bar.style.width='0';pc.textContent='0%';pl.textContent='Downloading…';
    await nap(s,600);show(ids[0]);await nap(s,1000);show(ids[1]);await nap(s,1100);show(ids[2]);await nap(s,1000);
    yq.classList.add('pick');await nap(s,800);
    show(ids[3]);
    for(let p=0;p<=100;p+=2){bar.style.width=p+'%';pc.textContent=p+'%';pl.textContent=`Downloading… ${(58.4*p/100).toFixed(1)} MB`;await nap(s,34)}
    pl.textContent='Saved';await nap(s,400);
    show(ids[4]);await nap(s,500);show(ids[5]);
    const f=ids[5].getBoundingClientRect(),b=s.getBoundingClientRect();
    for(let i=0;i<14;i++){
      const sp=document.createElement('i');sp.className='spark';
      sp.style.left=(f.left-b.left+f.width-30)+'px';sp.style.top=(f.top-b.top+f.height/2)+'px';
      const a=Math.random()*Math.PI*2,d=40+Math.random()*60;
      sp.style.setProperty('--x',Math.cos(a)*d+'px');sp.style.setProperty('--y',Math.sin(a)*d+'px');
      s.appendChild(sp);void sp.offsetWidth;sp.classList.add('go');setTimeout(()=>sp.remove(),1000);
    }
    await nap(s,4200);
  }
};

/* personalities scene */
const PERS=[
  {c:'#e3303b',d:'Cold, savage and menacing. The original Ultron.',a:'Done. Six a.m. Do not make me repeat the hour.'},
  {c:'#34d399',d:'Warm, cheerful and encouraging, like a close friend.',a:"Done! Alarm's set for 6 am. Rise and shine, champ!"},
  {c:'#60a5fa',d:'Calm, precise and to the point. No small talk.',a:'Alarm set for 6:00 a.m.'},
  {c:'#fbbf24',d:'Witty, playful, and serious only when the matter is serious.',a:'Alarm set. Ab snooze mat dabana, champion.'}
];
S.pers={
  still(s){pShow(s,0)},
  init(s){
    const tabs=$$('#ptabs button');
    s._i=0;pShow(s,0);
    tabs.forEach((b,i)=>b.addEventListener('click',()=>{s._i=i;pShow(s,i);s._t=0}));
    s._t=0;
    setInterval(()=>{if(paused||!s._vis)return;s._t+=1;if(s._t>=6){s._t=0;s._i=(s._i+1)%PERS.length;pShow(s,s._i)}},1000);
  }
};
function pShow(s,i){
  const P=PERS[i],tabs=$$('#ptabs button'),dots=$$('#pdots i'),a=$('#pa');
  s.style.setProperty('--pc',P.c);
  tabs.forEach((b,k)=>b.classList.toggle('on',k===i));
  dots.forEach((d,k)=>{d.classList.remove('on');if(k===i){void d.offsetWidth;d.classList.add('on')}});
  $('#pd').textContent=P.d;
  show(a,false);
  if(s._tok)s._tok.dead=true;
  const tok=s._tok={dead:false};
  if(still){a.textContent=P.a;show(a);return}
  setTimeout(async()=>{if(tok.dead)return;a.textContent='';show(a);await typeInto(a,P.a,30,s,tok)},260);
}

/* skills: code editor typing + Ultron following it */
const CODE=['---','name: morning-brief','description: Reads my day out loud when I say good morning.','---','# Morning brief','','1. Check the weather for today.',"2. List today's calendar events.",'3. Read my unread notifications.','4. Offer to set a reminder for the first meeting.'];
const esc=t=>t.replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
function paintCode(lines){
  return lines.map(l=>{
    if(l==='---')return '<span class="k">---</span>';
    let m=l.match(/^(name|description):\s?(.*)$/);
    if(m)return `<span class="h">${m[1]}:</span> <span class="${m[1]==='name'?'n':'v'}">${esc(m[2])}</span>`;
    if(l.startsWith('# '))return `<span class="h">${esc(l)}</span>`;
    m=l.match(/^(\d+\.)(.*)$/);
    if(m)return `<span class="n">${m[1]}</span>${esc(m[2])}`;
    return esc(l);
  }).join('\n');
}
let codeDone=Promise.resolve();
const pre=$('#codepre');
S.code={
  still(){pre.innerHTML=paintCode(CODE)},
  async play(s){
    let res;codeDone=new Promise(r=>res=r);
    const full=CODE.join('\n');let n=0;
    while(n<full.length){
      n+=full[n]==='\n'?1:2;n=Math.min(n,full.length);
      pre.innerHTML=paintCode(full.slice(0,n).split('\n'))+'<i class="caret"></i>';
      await nap(s,26);
    }
    pre.innerHTML=paintCode(CODE)+'<i class="caret"></i>';
    res();await nap(s,9000);
    pre.innerHTML='<i class="caret"></i>';await nap(s,700);
  }
};
S.run={
  still(){show($('#r1'));show($('#r2'));$$('#rsteps li').forEach(l=>l.classList.add('on','done'))},
  async play(s){
    const r1=$('#r1'),r2=$('#r2'),st=$$('#rsteps li'),sk=$('#skm');
    show(r1,false);show(r2,false);st.forEach(l=>l.classList.remove('on','done'));
    await Promise.race([codeDone,sleep(9000)]);await nap(s,500);
    show(r1);await nap(s,900);
    sk.classList.remove('pulse');void sk.offsetWidth;sk.classList.add('pulse');await nap(s,700);
    for(const l of st){l.classList.add('on');await nap(s,850);l.classList.add('done')}
    show(r2);await nap(s,6000);
  }
};

/* ---------- connectors ---------- */
const CONN=[
  ['device_info','Device info','ess','i-phone','On your phone','Battery, storage, network, time and more.','How much battery is left?',1],
  ['device_controls','Device controls','ess','i-sun','On your phone','Flashlight, volume, brightness and phone modes.','Turn on the flashlight.',1],
  ['alarms','Alarms & timers','ess','i-clock','On your phone','Set alarms and timers.','Set an alarm for 6:30.',1],
  ['reminders','Reminders','ess','i-bell','On your phone','Get reminded at a time, with a sound that rings until you dismiss it.','Remind me on Friday at 5.',0],
  ['apps_settings','Apps & settings','ess','i-grid','On your phone','Open apps and settings, use the clipboard.','Open the camera.',1],
  ['weather','Weather','ess','i-cloud','Free, no sign-in','Weather now and for the next few days.','Will it rain tomorrow?',1],
  ['duckduckgo','Web search','web','i-search','No sign-in','Search the web, with sources.','Search for the best laptop deals.',1],
  ['web_reader','Web pages','web','i-globe','Free, no sign-in','Read any web page or link, and summarise it by voice.','Summarise this page for me.',1],
  ['youtube','YouTube Search','web','i-play','Online','Search videos and playlists, get details, transcripts and channel uploads.','Find a lo-fi playlist.',0],
  ['youtube_downloads','YouTube Downloads','web','i-down','On your phone','List qualities and save video or audio to Downloads/Ultron.','Save this video as audio.',0],
  ['images','Pictures','web','i-img','On your phone','Show pictures you saved in Ultron, or photos from your phone.','Show the picture I saved.',0],
  ['calendar','Calendar','data','i-cal','On your phone','Check your schedule, spot conflicts and add events.','What is on my calendar today?',0],
  ['contacts','Contacts','data','i-user','On your phone','Find contacts, birthdays and save new contacts.',"When is Ria's birthday?",0],
  ['location','Location','data','i-pin','On your phone','Know where you are and get directions.','Directions to the airport.',0],
  ['files','Files','data','i-files','On your phone','Browse folders, find any file and open it.','Find my latest PDF.',0],
  ['app_usage','App usage','data','i-chart','On your phone','See which apps you use most, and for how long.','Which app do I use the most?',0],
  ['notifications','Notifications','data','i-msg','On your phone','Read and reply to notifications.','Read my notifications.',0],
  ['navigation','Phone navigation','phone','i-compass','On your phone','Back, home, recents, quick settings, scroll, lock screen and screenshots.','Go back, then scroll down.',1],
  ['screen','Screen control','phone','i-touch','On your phone','Read what is on screen, tap, type and wait for text.','Tap Send and type “On my way”.',1]
];
const CATS={all:'Everything Ultron can reach, in one place.',ess:'Everyday phone info and controls. Nothing here reads your personal data.',web:'Web search, web pages, pictures and YouTube.',data:'Reads private data from your phone, such as contacts, calendar, location, files and notifications. What you ask about is sent to Gemini.',phone:'Lets the assistant operate other apps through Android accessibility. It can tap, type and read the screen, so turn it on only if you understand that.'};
const hub=$('#hub'),grid=$('#cgrid'),tip=$('#tip'),NS='http://www.w3.org/2000/svg';
const state=new Map(CONN.map(c=>[c[0],!!c[7]]));
const nodes=new Map(),cards=new Map(),lines=new Map();
const polar=(r,deg)=>[50+r*Math.cos(deg*Math.PI/180),50+r*Math.sin(deg*Math.PI/180)];
(function buildHub(){
  const svg=document.createElementNS(NS,'svg');svg.setAttribute('viewBox','0 0 100 100');svg.setAttribute('class','lines');svg.setAttribute('aria-hidden','true');
  svg.innerHTML='<circle class="rg" cx="50" cy="50" r="24"/><circle class="rg rg2" cx="50" cy="50" r="41"/>';
  hub.prepend(svg);
  const core=document.createElement('div');core.className='hcore';core.innerHTML='<img src="assets/mark.svg" alt="" width="80" height="80">';hub.appendChild(core);
  CONN.forEach((c,i)=>{
    const inner=i<7,idx=inner?i:i-7,count=inner?7:12,r=inner?24:41,deg=-90+idx*(360/count)+(inner?0:15);
    const [x,y]=polar(r,deg);
    const ln=document.createElementNS(NS,'line');ln.setAttribute('x1',50);ln.setAttribute('y1',50);ln.setAttribute('x2',x);ln.setAttribute('y2',y);svg.insertBefore(ln,svg.children[2]||null);lines.set(c[0],{ln,x,y});
    const n=document.createElement('button');n.className='hn';n.style.left=x+'%';n.style.top=y+'%';n.dataset.id=c[0];n.dataset.c=c[2];n.setAttribute('aria-label',c[1]);
    n.innerHTML=`<svg class="ic"><use href="#${c[3]}"/></svg>`;hub.appendChild(n);nodes.set(c[0],n);
    n.addEventListener('mouseenter',()=>hint(c));n.addEventListener('focus',()=>hint(c));
    n.addEventListener('click',()=>toggle(c[0]));
  });
})();
function hint(c){tip.innerHTML=`<b>${c[1]}</b> · ${c[4]}<br><q>Say: “${c[6]}”</q>`}
(function buildCards(){
  CONN.forEach((c,i)=>{
    const a=document.createElement('article');a.className='conn sp rv';a.style.setProperty('--d',(i%4)*.06+'s');a.dataset.id=c[0];a.dataset.c=c[2];
    a.innerHTML=`<div class="conn-top"><div class="ci"><svg class="ic"><use href="#${c[3]}"/></svg></div><h3>${c[1]}<small>${c[4]}</small></h3><button class="sw" role="switch" aria-checked="false" aria-label="Connect ${c[1]}"></button></div><p>${c[5]}</p><div class="say-s"><svg class="ic"><use href="#i-mic"/></svg><span>“${c[6]}”</span></div><span class="status">Not connected</span>`;
    grid.appendChild(a);observeRv(a);cards.set(c[0],a);
    $('.sw',a).addEventListener('click',()=>toggle(c[0]));
    a.addEventListener('mouseenter',()=>{nodes.get(c[0]).classList.add('hl');hint(c)});
    a.addEventListener('mouseleave',()=>nodes.get(c[0]).classList.remove('hl'));
  });
})();
function paint(id){
  const on=state.get(id),n=nodes.get(id),a=cards.get(id),L=lines.get(id);
  n.classList.toggle('on',on);a.classList.toggle('is-on',on);
  const sw=$('.sw',a);sw.setAttribute('aria-checked',on);$('.status',a).textContent=on?'Connected':'Not connected';
  L.ln.classList.toggle('on',on);
  if(L.pk){L.pk.remove();L.pk=null}
  if(on&&!still){
    const c=document.createElementNS(NS,'circle');c.setAttribute('class','pk');c.setAttribute('r','.9');
    const m=document.createElementNS(NS,'animateMotion');m.setAttribute('dur',(1.6+Math.random()*1.2).toFixed(2)+'s');m.setAttribute('repeatCount','indefinite');m.setAttribute('path',`M50 50L${L.x} ${L.y}`);
    c.appendChild(m);L.ln.parentNode.appendChild(c);L.pk=c;
  }
}
let shownN=0;
function meter(){
  const n=[...state.values()].filter(Boolean).length;
  $('#cbar').style.width=(n/CONN.length*100)+'%';
  $('#clabel').textContent=`of ${CONN.length} connectors connected`;
  const el=$('#cnum'),from=shownN;shownN=n;
  if(still){el.textContent=n;return}
  const t0=performance.now();const step=t=>{const p=clamp((t-t0)/450,0,1);el.textContent=Math.round(from+(n-from)*p);if(p<1)requestAnimationFrame(step)};requestAnimationFrame(step);
}
function toggle(id){state.set(id,!state.get(id));paint(id);meter();const c=CONN.find(x=>x[0]===id);hint(c);
  if(state.get(id)&&(c[2]==='phone'||c[2]==='data'))tip.innerHTML=`<b>${c[1]}</b> connected<br><q>Android asks for its permission first</q>`}
CONN.forEach(c=>paint(c[0]));meter();
$('#call').addEventListener('click',()=>{CONN.forEach(c=>{state.set(c[0],true);paint(c[0])});meter()});
$('#creset').addEventListener('click',()=>{CONN.forEach(c=>{state.set(c[0],!!c[7]);paint(c[0])});meter()});
$$('#cfilters button').forEach(b=>b.addEventListener('click',()=>{
  $$('#cfilters button').forEach(x=>x.classList.toggle('on',x===b));
  const f=b.dataset.f;$('#catsum').textContent=CATS[f];
  cards.forEach(a=>{a.hidden=!(f==='all'||a.dataset.c===f)});
  nodes.forEach(n=>n.classList.toggle('dim',!(f==='all'||n.dataset.c===f)));
}));

/* ---------- app screens gallery ---------- */
(function gallery(){
  const sw=$('#tsw'),btns=$$('button',sw),track=$('#track');
  btns.forEach(b=>b.addEventListener('click',()=>{
    const t=b.dataset.theme;sw.dataset.t=t;
    btns.forEach(x=>{x.classList.toggle('on',x===b);x.setAttribute('aria-pressed',x===b)});
    $$('img[data-shot]').forEach((img,k)=>{
      const n=new Image();n.onload=()=>{img.classList.add('swap');setTimeout(()=>{img.src=n.src;img.classList.remove('swap')},180)};n.src=`assets/app/${t}-${img.dataset.shot}.webp`;
    });
  }));
  let down=false,sx=0,sl=0;
  track.addEventListener('pointerdown',e=>{if(e.pointerType!=='mouse')return;down=true;sx=e.clientX;sl=track.scrollLeft;track.classList.add('drag')});
  addEventListener('pointermove',e=>{if(down)track.scrollLeft=sl-(e.clientX-sx)});
  addEventListener('pointerup',()=>{down=false;track.classList.remove('drag')});
  const by=d=>track.scrollBy({left:d*(track.firstElementChild.offsetWidth+26)*2,behavior:still?'auto':'smooth'});
  $('#tprev').addEventListener('click',()=>by(-1));$('#tnext').addEventListener('click',()=>by(1));
})();

onScroll();

/* ---------- pause motion ---------- */
const mb=$('.motion');
mb.addEventListener('click',()=>{paused=!paused;mb.setAttribute('aria-pressed',paused);mb.textContent=paused?'Resume motion':'Pause motion';document.body.classList.toggle('paused',paused)});
if(still)mb.hidden=true;

/* ---------- plan buttons: WhatsApp when a number is set, otherwise the email already in each link ---------- */
(()=>{
  // Orders go to this WhatsApp number. Country code first, digits only, for example "919876543210". Empty: orders use email.
  const BUY_WHATSAPP='917078710389';
  const number=BUY_WHATSAPP.replace(/\D/g,'');
  if(!number)return;
  const wa=text=>`https://wa.me/${number}?text=${encodeURIComponent(text)}`;
  $$('.buy').forEach(a=>{
    const {plan,price}=a.dataset;
    a.href=wa(`Hi, I want the Ultron ${plan} plan (₹${Number(price).toLocaleString('en-IN')}).`);
    a.target='_blank';a.rel='noopener';
  });
  const card=$('[data-wa]');
  if(card){
    card.hidden=false;
    const link=$('[data-wa-link]',card);
    link.href=wa('Hi, I have a question about Ultron.');link.target='_blank';link.rel='noopener';
  }
})();
})();
