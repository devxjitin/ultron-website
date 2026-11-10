(()=>{
'use strict';
const $=(s,r=document)=>r.querySelector(s),$$=(s,r=document)=>[...r.querySelectorAll(s)];
const still=matchMedia('(prefers-reduced-motion: reduce)').matches;
const clamp=(v,a,b)=>Math.min(b,Math.max(a,v));

// mobile menu
const tg=$('.menu-toggle'),links=$('#nav-links');
if(tg&&links){
  const close=()=>{links.classList.remove('open');tg.setAttribute('aria-expanded','false')};
  tg.addEventListener('click',()=>{const o=links.classList.toggle('open');tg.setAttribute('aria-expanded',o)});
  $$('a',links).forEach(a=>a.addEventListener('click',close));
}

// docs menu: open on wide screens, collapsed behind a button on phones
const dm=$('.dside-m');
if(dm){
  // wide screens always show the menu; phones start with it collapsed behind the button
  let narrow=null;
  const fit=()=>{const n=innerWidth<=1020;if(n===narrow)return;narrow=n;dm.open=!n};
  fit();addEventListener('resize',fit);
}
const cur=$('.dside a[aria-current=page]');
const side=$('.dside');
if(cur&&side&&side.scrollHeight>side.clientHeight)side.scrollTop=Math.max(0,cur.offsetTop-160);

// smooth scrolling, same feel as the home page
let lenis=null;
if(window.Lenis&&!still){
  lenis=new Lenis({duration:1.25,easing:t=>Math.min(1,1.001-Math.pow(2,-10*t)),smoothWheel:true});
  const raf=t=>{lenis.raf(t);requestAnimationFrame(raf)};requestAnimationFrame(raf);
  $$('a[href^="#"]').forEach(a=>a.addEventListener('click',e=>{
    const id=a.getAttribute('href');if(id.length<2)return;
    const el=$(id);if(!el)return;
    e.preventDefault();lenis.scrollTo(el,{offset:-76,duration:1.5});
  }));
}

// reading progress
const prog=$('#progress');
const work=()=>{
  const max=document.documentElement.scrollHeight-innerHeight;
  if(prog)prog.style.transform=`scaleX(${max>0?clamp(scrollY/max,0,1):0})`;
};
if(lenis)lenis.on('scroll',work);else addEventListener('scroll',()=>requestAnimationFrame(work),{passive:true});
addEventListener('resize',work);work();

// reveal on scroll, two-way like the home page
const rio=new IntersectionObserver(es=>es.forEach(e=>{
  const t=e.target;
  if(e.intersectionRatio>=.12||(e.isIntersecting&&e.intersectionRect.height>=innerHeight*.5)){
    t.classList.add('in');
  }else if(!e.isIntersecting&&!still){
    t.classList.remove('in');
    t.classList.toggle('from-top',e.boundingClientRect.bottom<=0);
  }
}),{threshold:[0,.12],rootMargin:'0px 0px -6% 0px'});
$$('.rv').forEach(el=>rio.observe(el));

// phone demo: the real voice screen, and for automation the app screens Ultron works, one example after another
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
const isPaused=()=>document.body.classList.contains('paused');
const DEAD=new Error('dead');
const wait=async(ms,tok)=>{await sleep(ms);while(isPaused()&&!tok.dead)await sleep(200);if(tok.dead)throw DEAD};
// split an element's own text into a typed part and a hidden rest, so the layout never jumps
function prep(el){
  const tn=[...el.childNodes].find(n=>n.nodeType===3&&n.textContent.trim());
  if(!tn)return null;
  const full=tn.textContent,a=document.createElement('span'),b=document.createElement('span');
  a.className='ty';b.className='ty-h';a.textContent=full;tn.replaceWith(a,b);
  return {el,a,b,full,set(n){a.textContent=full.slice(0,n);b.textContent=full.slice(n)}};
}
const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const ico=n=>`<svg class="ic"><use href="#i-${n}"/></svg>`;
const CUR='<span class="p-cur"><svg viewBox="0 0 24 24"><use href="#i-cursor"/></svg></span>';
const rowsHtml=(a,x='')=>a.map(r=>`<div class="p-row ${x}">${esc(r)}</div>`).join('');

// the screens: html(p) builds the markup, run(el,p,w) plays the automation. w(ms) waits and stops the run when the page leaves.
const K={};
const pcur=(el,x,y,tap)=>{const c=$('.p-cur',el);c.style.left=x+'%';c.style.top=y+'%';if(tap)setTimeout(()=>{c.classList.remove('tap');void c.offsetWidth;c.classList.add('tap')},720)};
// Move the cursor onto a real element, so it lands right whatever height the phone screen has.
const pcurOn=(el,t,tap)=>{const sc=$('.kscr',el)||el,r=sc.getBoundingClientRect(),b=t.getBoundingClientRect();pcur(el,(b.left+b.width/2-r.left)/r.width*100,(b.top+b.height/2-r.top)/r.height*100,tap)};
const reveal=async(els,w,gap=160)=>{for(const e of els){e.classList.add('show');await w(gap)}};
const typeText=async(node,text,w,ms=70)=>{node.textContent='';for(const ch of text){node.textContent+=ch;await w(ms)}};

K.search={
  html:p=>`<div class="p-hd"><b>${esc(p.app)}</b></div><div class="p-pad"><div class="p-fld"><span class="ph">Search</span><span class="tx"></span></div></div><div class="p-list">${rowsHtml(p.results)}</div>${CUR}`,
  async run(el,p,w){
    const f=$('.p-fld',el),tx=$('.tx',el),ph=$('.ph',el);
    pcur(el,60,20);await w(500);pcur(el,62,19,true);await w(900);
    f.classList.add('act');ph.style.display='none';await typeText(tx,p.text,w);
    await w(400);pcur(el,86,19,true);await w(900);
    await reveal($$('.p-row',el),w,220);await w(1100);
  }};
K.chat={
  html:p=>`<div class="p-hd"><i></i><b>${esc(p.name)}<small>online</small></b></div><div class="p-msgs"><p>${esc(p.incoming)}</p><p class="out"></p></div><div class="p-comp"><div class="p-fld"><span class="tx"></span></div><span class="p-send">${ico('send')}</span></div>${CUR}`,
  async run(el,p,w){
    const f=$('.p-fld',el),tx=$('.tx',el),out=$('.p-msgs .out',el),sd=$('.p-send',el);
    out.textContent=p.reply;pcur(el,40,60);await w(600);pcurOn(el,f);await w(800);pcurOn(el,f,true);await w(400);
    f.classList.add('act');await typeText(tx,p.reply,w,55);await w(400);
    pcurOn(el,sd);await w(800);sd.classList.add('press');pcurOn(el,sd,true);await w(300);sd.classList.remove('press');
    tx.textContent='';f.classList.remove('act');out.classList.add('show');await w(1400);
  }};
// WhatsApp, opened the way the WhatsApp skill does it: open_app, open the chat, check the header, then the task's own steps.
// p.flow picks the task: text, file, loc, live, call, vcall, read, search, statuses, view, ptext, pfile.
K.wa={
  html:p=>{
    const nm=p.name||'Rohan';
    const names=[nm,...['Rohan','Mummy','Papa','Priya','Family group'].filter(n=>n!==nm)].slice(0,5);
    const last={Rohan:'Kab tak aa rahe ho?',Mummy:'Khana kha liya?',Papa:'Ok beta',Priya:'Thanks!','Family group':'Papa: Sunday ko aana'};
    const rows=names.map((n,i)=>`<div class="wa-row" data-n="${esc(n)}"><i></i><div><b>${esc(n)}</b><small>${esc(last[n]||'Hi')}</small></div><em>${i?'Yesterday':'10:42'}</em></div>`).join('');
    const sts=['Rahul','Mummy','Priya'].map(n=>`<div class="wa-row wa-st" data-n="${n}"><i class="ring"></i><div><b>${n}</b><small>Today, 9:${n.length}0</small></div></div>`).join('');
    const apps=['Phone','Messages','Camera','Gallery','WhatsApp','Maps','Clock','Settings'].map(a=>`<div class="wa-ic${a==='WhatsApp'?' wa-app':''}"><i>${a==='WhatsApp'?ico('msg'):''}</i><small>${a}</small></div>`).join('');
    return `<div class="wa">
<div class="wa-step"></div>
<div class="wa-v" data-v="home"><div class="wa-grid">${apps}</div></div>
<div class="wa-v" data-v="list"><div class="wa-top"><b>WhatsApp</b></div><div class="wa-rows">${rows}</div><div class="wa-tabs"><span class="t-ch on">Chats</span><span class="t-up">Updates</span><span>Calls</span></div></div>
<div class="wa-v" data-v="chat"><div class="wa-top wa-chd"><i></i><b>${esc(nm)}<small>online</small></b><span class="wa-hi h-call">${ico('phone')}</span><span class="wa-hi h-vid">${ico('play')}</span><span class="wa-hi h-srch">${ico('search')}</span></div>
<div class="wa-sb"><span class="sb-tx"></span></div><div class="wa-msgs"></div>
<div class="wa-comp"><span class="wa-clip">${ico('files')}</span><div class="wa-fld"><span class="tx"></span></div><span class="wa-snd">${ico('send')}</span></div>
<div class="wa-sheet"></div>
<div class="wa-prev"><div class="wa-th"></div><div class="wa-capt"></div><span class="wa-snd wa-pgo">${ico('send')}</span></div></div>
<div class="wa-v wa-call" data-v="call"><i class="big"></i><b>${esc(nm)}</b><small class="cs">Calling</small><span class="wa-end"></span></div>
<div class="wa-v" data-v="upd"><div class="wa-top"><b>Updates</b></div><div class="wa-lab">Status</div><div class="wa-row wa-my"><i class="me"></i><div><b>My status</b><small class="my-s">Tap to add status update</small></div></div><div class="wa-lab">Recent updates</div><div class="wa-rows">${sts}</div><span class="wa-pen">${ico('spark')}</span><div class="wa-tabs"><span>Chats</span><span class="on">Updates</span><span>Calls</span></div></div>
<div class="wa-v wa-stv" data-v="stat"><div class="wa-bar"><span></span></div><div class="wa-sh"><i></i><b>${esc(nm)}<small>Today</small></b></div><div class="wa-sc"></div></div>
<div class="wa-v wa-cmp" data-v="cmp"><div class="wa-ct"><span class="tx"></span></div><span class="wa-snd">${ico('send')}</span></div>
<div class="wa-v" data-v="to"><div class="wa-top"><b>Send to</b></div><div class="wa-lab">Status</div><div class="wa-row wa-tos"><i class="me"></i><div><b>My status</b></div><span class="wa-tick"></span></div><div class="wa-lab">Recent chats</div><div class="wa-rows">${rows}</div><span class="wa-snd wa-tog">${ico('send')}</span></div>
${CUR}</div>`;
  },
  async run(el,p,w){
    const q=s=>$(s,el),nm=p.name||'Rohan',fk=p.fkind||'photo',file=p.file||'Photo';
    const view=n=>$$('.wa-v',el).forEach(v=>v.classList.toggle('on',v.dataset.v===n));
    const step=(t,a)=>{const s=q('.wa-step');s.innerHTML=`<b>${esc(t)}</b><span>${esc(a||'')}</span>`;s.classList.add('on')};
    const tap=async e=>{pcurOn(el,e);await w(750);pcurOn(el,e,true);await w(500)};
    const row=n=>$$('.wa-rows .wa-row',q('[data-v=list]')).find(r=>r.dataset.n===n);
    const out=(h,cls='')=>{const m=q('.wa-msgs');m.insertAdjacentHTML('beforeend',h);return m.lastElementChild};
    const bub=(t,cls='out')=>out(`<p class="${cls} show">${esc(t)}${cls==='out'?'<small>✓✓</small>':''}</p>`);
    const type=async t=>{const f=q('.wa-fld'),x=q('.wa-fld .tx');f.classList.add('act');await typeText(x,t,w,55);await w(350)};
    const sendNow=async()=>{step('click_on_text','Send');await tap(q('.wa-comp .wa-snd'));q('.wa-fld .tx').textContent='';q('.wa-fld').classList.remove('act')};
    const sheet=(items,pick)=>{const s=q('.wa-sheet');s.innerHTML=items.map((t,i)=>`<span class="${i===pick?'pk':''}">${esc(t)}</span>`).join('');s.classList.add('on');return $$('span',s)[pick]};
    const thumb=k=>k==='photo'?'<div class="wa-img"></div>':k==='video'?'<div class="wa-img v"><b>▶</b></div>':k==='doc'?`<div class="wa-doc"><b>PDF</b>${esc(file)}</div>`:`<div class="wa-aud"><b>▶</b><u></u>0:42</div>`;
    const status=['statuses','view','ptext','pfile'].includes(p.flow);

    q('.wa-msgs').innerHTML='';
    // 1. open_app WhatsApp
    step('open_app','WhatsApp');view('home');pcur(el,50,75);await w(800);
    await tap(q('.wa-app'));
    view('list');step('read_screen','chat list');await w(900);
    if(status){
      step('click_on_text','Updates');await tap(q('.t-up'));view('upd');step('read_screen','Recent updates');await w(1000);
    }else{
      // 2. open the person's chat and check the header
      step('click_on_text',nm);await tap(row(nm));
      view('chat');
      if(['text','read','reply','search'].includes(p.flow))out(`<p class="in">${esc(p.incoming||'Kab tak aa rahe ho?')}</p>`);
      step('read_screen','header shows '+nm);q('.wa-chd').classList.add('ok');await w(1300);q('.wa-chd').classList.remove('ok');
    }

    if(p.flow==='text'){
      step('type_text',p.text);await type(p.text);
      await sendNow();bub(p.text);step('read_screen','message is the newest bubble');await w(1500);
    }else if(p.flow==='read'){
      step('read_screen','new messages');(p.msgs||[]).forEach(m=>out(`<p class="in">${esc(m)}</p>`));
      q('.wa-msgs').classList.add('speak');await w(2600);
    }else if(p.flow==='file'){
      step('search_files',`${fk}: "${file}"`);await w(1100);
      step('share_file','WhatsApp, to '+nm);q('.wa-th').innerHTML=thumb(fk);q('.wa-capt').textContent=file;q('.wa-prev').classList.add('on');await w(1300);
      step('click_on_text','Send');await tap(q('.wa-pgo'));q('.wa-prev').classList.remove('on');
      out(`<p class="out show wa-file">${thumb(fk)}<small>✓✓</small></p>`);
      step('read_screen','file is the newest bubble');await w(1500);
    }else if(p.flow==='loc'||p.flow==='live'){
      step('click_on_text','Attach');await tap(q('.wa-clip'));
      let t=await sheet(['Document','Camera','Gallery','Audio','Location','Contact'],4);
      step('click_on_text','Location');await tap(t);
      t=await sheet(p.flow==='loc'?['Send your current location','Share live location']:['Send your current location','Share live location'],p.flow==='loc'?0:1);
      step('click_on_text',p.flow==='loc'?'Send your current location':'Share live location');await tap(t);
      if(p.flow==='live'){t=await sheet(['15 minutes','1 hour','8 hours'],1);step('click_on_text',p.dur||'1 hour');await tap(t);t=await sheet(['Send'],0);await tap(t)}
      q('.wa-sheet').classList.remove('on');
      out(`<p class="out show wa-loc"><span class="map"><b></b></span>${p.flow==='live'?'<em>Live for '+esc(p.dur||'1 hour')+'</em>':''}<small>✓✓</small></p>`);
      step('read_screen','location is the newest bubble');await w(1600);
    }else if(p.flow==='call'||p.flow==='vcall'){
      step('click_on_text',p.flow==='call'?'Voice call':'Video call');await tap(q(p.flow==='call'?'.h-call':'.h-vid'));
      view('call');q('.wa-call').classList.toggle('vid',p.flow==='vcall');step('read_screen','call screen');await w(1100);
      q('.cs').textContent='Ringing';await w(1700);
    }else if(p.flow==='search'){
      step('click_on_text','Search');await tap(q('.h-srch'));
      q('.wa-sb').classList.add('on');step('type_text',p.q);await typeText(q('.sb-tx'),p.q,w,70);
      out(`<p class="in hit">${esc(p.found)}</p>`);step('read_screen','match found');await w(2000);
    }else if(p.flow==='statuses'){
      $$('.wa-st',q('[data-v=upd]')).forEach(r=>r.classList.add('hl'));
      step('read_screen','names under Recent updates');await w(2800);
    }else if(p.flow==='view'){
      step('click_on_text',nm);await tap($$('.wa-st',q('[data-v=upd]')).find(r=>r.dataset.n===nm));
      view('stat');q('.wa-sc').textContent=p.caption||'Weekend';q('.wa-bar span').classList.remove('go');void q('.wa-bar').offsetWidth;q('.wa-bar span').classList.add('go');
      step('look_at_screen','describe the status');await w(3200);
    }else if(p.flow==='ptext'){
      step('click_screen_item','pencil');await tap(q('.wa-pen'));
      view('cmp');step('type_text',p.text);await typeText(q('.wa-ct .tx'),p.text,w,70);await w(400);
      step('click_on_text','Send');await tap(q('[data-v=cmp] .wa-snd'));
      view('upd');q('.my-s').textContent='Just now';q('.wa-my').classList.add('hl');step('read_screen','My status shows a recent time');await w(2000);
    }else if(p.flow==='pfile'){
      step('search_files',`${fk}: "${file}"`);await w(1000);
      step('share_file','WhatsApp, no phone number');view('to');await w(1200);
      step('click_on_text','Status');await tap(q('.wa-tos'));q('.wa-tos').classList.add('sel');await w(300);
      step('click_on_text','Send');await tap(q('.wa-tog'));
      view('upd');q('.my-s').textContent='Just now';q('.wa-my').classList.add('hl');step('read_screen','My status shows a recent time');await w(2000);
    }
  }};
K.scan={
  html:p=>`<div class="p-hd"><b>Screen</b></div><div class="p-list p-rel" style="padding-top:12px">${p.rows.map((r,i)=>`<div class="p-row show" style="position:relative">${esc(r)}<span class="p-tag" data-i="${i}">${i+1}</span></div>`).join('')}<div class="p-scan"></div></div><p class="p-note"></p>`,
  async run(el,p,w){
    const sc=$('.p-scan',el),note=$('.p-note',el);
    await w(500);sc.classList.add('go');await w(1500);
    await reveal($$('.p-tag',el),w,260);
    note.textContent=`Finds ${p.rows.length} things it can press`;note.classList.add('show');await w(1500);
  }};
K.scroll={
  html:p=>`<div class="p-hd"><b>Feed</b></div><div style="overflow:hidden;flex:1"><div class="p-list p-long" style="padding-top:10px">${rowsHtml(p.rows,'show')}</div></div>`,
  async run(el,p,w){
    const l=$('.p-long',el);await w(600);l.style.transform='translateY(-62%)';await w(1900);
  }};
K.shot={
  html:p=>`<div class="p-hd"><b>Home</b></div><div class="p-list" style="padding-top:12px">${rowsHtml(p.rows,'show')}</div><div class="p-flash"></div><div class="p-thumb"><i></i><span>Screenshot saved</span></div>`,
  async run(el,p,w){
    await w(700);$('.p-flash',el).classList.add('go');await w(500);$('.p-thumb',el).classList.add('show');await w(1700);
  }};
K.back={
  html:p=>`<div class="p-hd"><b>${esc(p.app)}</b></div><div class="p-list" style="padding-top:12px">${rowsHtml(['Wi-Fi','Bluetooth','Display'],'show')}</div><div class="p-page"><div class="p-hd"><b>← ${esc(p.page)}</b></div><div class="p-list" style="padding-top:12px">${rowsHtml(['HomeNet','Office','Guest'],'show')}</div></div>${CUR}`,
  async run(el,p,w){
    const pg=$('.p-page',el);await w(700);pcur(el,16,13);await w(800);pcur(el,16,13,true);await w(500);pg.classList.add('out');await w(1500);
  }};
K.ytdl={
  html:p=>`<div class="p-hd"><b>YouTube</b></div><div class="p-card"><div class="p-vid">${ico('tri')}</div><b>${esc(p.title)}</b><span>${esc(p.quality)}</span><span class="p-chip">Downloading</span><div class="p-bar"><i></i></div><small class="pc" style="color:var(--dim)">0%</small></div><div class="p-title">Downloads / Ultron</div><div class="p-list"><div class="p-row">${esc(p.file)}<small>${esc(p.size)}</small></div></div>`,
  async run(el,p,w){
    const bar=$('.p-bar i',el),pc=$('.pc',el);await w(600);bar.style.width='100%';
    for(let i=1;i<=10;i++){await w(220);pc.textContent=i*10+'%'}
    $('.p-chip',el).textContent='Saved';await w(250);$('.p-row',el).classList.add('show','pick');await w(1400);
  }};
K.alarm={
  html:p=>`<div class="p-hd"><b>Alarms</b></div><div class="p-al" style="opacity:.55"><div><b>7:00 AM</b><small>Mon to Fri</small></div><span class="p-tog on"></span></div><div class="p-al new" style="opacity:0;transition:opacity .5s"><div><b class="tm">${esc(p.old||p.time)}</b><small>${esc(p.label)}</small></div><span class="p-tog"></span></div><div class="p-al" style="opacity:.55"><div><b>9:30 PM</b><small>Every day</small></div><span class="p-tog"></span></div>`,
  async run(el,p,w){
    const nw=$('.p-al.new',el),tm=$('.tm',el),tg=$('.p-tog',nw);await w(600);nw.style.opacity=1;await w(800);
    if(p.old){tm.style.textDecoration='line-through';await w(700);tm.style.textDecoration='none';tm.textContent=p.time;await w(500)}
    tg.classList.add('on');await w(1500);
  }};
K.timer={
  html:p=>`<div class="p-hd"><b>Timer</b></div><div class="p-ring"><span class="tm"></span></div><p class="p-sub">Counting down</p>`,
  async run(el,p,w){
    const tm=$('.tm',el);const f=s=>String(Math.floor(s/60)).padStart(2,'0')+':'+String(s%60).padStart(2,'0');
    let s=p.start;tm.textContent=f(s);await w(900);for(let i=0;i<5;i++){s--;tm.textContent=f(s);await w(700)}await w(500);
  }};
K.calendar={
  html:p=>`<div class="p-hd"><b>Tomorrow</b></div>${['10 AM','12 PM','2 PM','4 PM','6 PM'].map(t=>`<div class="p-slot" data-t="${t}"><span>${t}</span><div>${p.events&&p.events[t]?`<div class="p-ev">${esc(p.events[t])}</div>`:''}</div></div>`).join('')}`,
  async run(el,p,w){
    await reveal($$('.p-slot',el),w,200);await w(400);
    const add=(t,txt,cls)=>{const d=$(`.p-slot[data-t="${t}"]>div`,el);d.innerHTML=`<div class="p-ev ${cls}">${esc(txt)}</div>`};
    if(p.free){add(p.free,'Free','free')}
    if(p.new){for(const t in p.new)add(t,p.new[t],'new')}
    await w(1800);
  }};
K.tiles={
  html:p=>`<div class="p-hd"><b>Quick settings</b></div><div class="p-tiles">${['Wi-Fi','Bluetooth','Flashlight','Do Not Disturb','Auto-rotate','Battery saver'].map(t=>`<div class="p-tile${t==='Wi-Fi'||t==='Bluetooth'?' on':''}" data-t="${t}">${esc(t)}<small>${t==='Wi-Fi'||t==='Bluetooth'?'On':'Off'}</small></div>`).join('')}</div>${CUR}`,
  async run(el,p,w){
    const t=$(`.p-tile[data-t="${p.tile}"]`,el);const r=t.getBoundingClientRect(),h=el.getBoundingClientRect();
    pcur(el,70,50);await w(500);pcur(el,(r.left-h.left+r.width/2)/h.width*100,(r.top-h.top+r.height/2)/h.height*100,true);await w(1000);
    t.classList.add('on');$('small',t).textContent='On';await w(1500);
  }};
K.slider={
  html:p=>`<div class="p-hd"><b>${esc(p.label)}</b></div><div class="p-big"><span class="pv">${p.start}</span>%</div><div class="p-slider"><div class="tr"><i style="width:${p.start}%"></i></div></div>`,
  async run(el,p,w){
    const i=$('.tr i',el),pv=$('.pv',el);await w(600);i.style.width=p.to+'%';
    const n=12,a=p.start,b=p.to;for(let k=1;k<=n;k++){await w(120);pv.textContent=Math.round(a+(b-a)*k/n)}await w(900);
  }};
K.call={
  html:p=>`<div class="p-hd"><b>Phone</b></div>${p.ask?`<div class="p-title">Which one?</div><div class="p-list">${rowsHtml(p.ask)}</div>`:''}<div class="p-callv"${p.ask?' style="opacity:0;height:0;overflow:hidden"':''}><div class="p-av">${esc((p.name||'?')[0])}</div><div class="p-ok">${esc(p.name)}</div><p class="p-sub st">Calling...</p><div class="p-call"><i>${ico('mic')}</i><i class="end">${ico('phone')}</i></div></div>`,
  async run(el,p,w){
    if(p.ask){await reveal($$('.p-row',el),w,220);await w(500);$$('.p-row',el)[0].classList.add('pick');await w(900);$('.p-list',el).style.display='none';$('.p-title',el).style.display='none';const v=$('.p-callv',el);v.style.opacity=1;v.style.height='auto'}
    await w(900);const st=$('.st',el);await w(1200);st.textContent='00:01';await w(1000);st.textContent='00:02';await w(1000);
  }};
K.route={
  html:p=>`<div class="p-map"><svg viewBox="0 0 100 200" preserveAspectRatio="none"><path d="M20 170 C 30 120, 60 130, 55 80 S 78 40, 80 22"/></svg></div><div class="p-dest"><b style="color:#fff">${esc(p.dest)}</b><span style="color:var(--mute)">Navigation started</span></div>`,
  async run(el,p,w){await w(600);$('.p-map',el).classList.add('go');await w(1700);$('.p-dest',el).classList.add('show');await w(1500)}
};
K.launch={
  html:p=>`<div class="p-grid">${['Phone','Mail','Maps','Photos',p.app,'Music','Notes','Clock'].map((a,i)=>`<div class="p-app" data-i="${i}"><i></i>${esc(a)}</div>`).join('')}</div><div class="p-open"><i></i>${esc(p.app)}</div>${CUR}`,
  async run(el,p,w){
    const t=$(`.p-app[data-i="${p.index}"]`,el),r=t.getBoundingClientRect(),h=el.getBoundingClientRect();
    pcur(el,60,70);await w(500);pcur(el,(r.left-h.left+r.width/2)/h.width*100,(r.top-h.top+r.height/2)/h.height*100,true);await w(1000);
    $('.p-open',el).classList.add('show');await w(1700);
  }};
K.list={
  html:p=>`<div class="p-title">${esc(p.title)}</div><div class="p-list">${p.rows.map(r=>`<div class="p-row">${esc(r)}</div>`).join('')}</div><p class="p-note">${esc(p.note||'')}</p>`,
  async run(el,p,w){
    const rows=$$('.p-row',el);await reveal(rows,w,230);await w(500);
    if(p.pick!=null)rows[p.pick].classList.add('pick');if(p.note)$('.p-note',el).classList.add('show');await w(1500);
  }};
K.weather={
  html:p=>`<div class="p-hd"><b>${esc(p.city)}</b></div><div class="p-wx"><div class="t">${esc(p.temp)}°</div><div style="color:var(--mute);margin-top:4px">${esc(p.cond)}</div><div class="days">${p.days.map(d=>`<span>${esc(d)}°</span>`).join('')}</div></div>`,
  async run(el,p,w){await w(500);$('.p-wx',el).classList.add('show');await w(2200)}
};
K.photo={
  html:p=>`<div class="p-hd"><b>Pictures</b></div><div class="p-photo">${esc(p.caption)}</div>`,
  async run(el,p,w){await w(600);$('.p-photo',el).classList.add('show');await w(2200)}
};
K.wait={
  html:p=>`<div class="p-hd"><b>Checkout</b></div><div class="p-spin"></div><p class="p-ok">${esc(p.busy)}</p>`,
  async run(el,p,w){
    await w(1800);const s=$('.p-spin',el);s.classList.add('done');$('.p-ok',el).textContent=p.text;await w(1700);
  }};
K.notif={
  html:p=>`<div class="p-lock">${esc(p.time)}</div><div class="p-ntf">${ico('bell')}<div><b>${esc(p.title)}</b>${esc(p.text)}</div></div>`,
  async run(el,p,w){await w(700);$('.p-ntf',el).classList.add('show');await w(2200)}
};

const STAGES=['s-hear','s-tool','s-do','s-say'];
$$('.demo').forEach(el=>{
  let items;try{items=JSON.parse(el.dataset.demo)}catch(_){return}
  el.classList.add('js');
  const sub=$('.v-sub',el),src=$('.ty-src',sub),chip=$('.v-chip',el),chipTxt=$('span',chip),reply=$('.v-reply',el);
  const ks=$('.kscr',el),cap=$('.dcap',el),dots=$$('.dots button',el);
  let say=prep(src),idx=0,tok=null,visible=false;
  const stage=k=>{
    STAGES.concat('s-fin').forEach(c=>el.classList.remove(c));
    if(k>=0&&k<4)el.classList.add(STAGES[k]);
    if(k>=4)el.classList.add('s-fin');
  };
  // show example i as a finished picture (used for reduced motion, off screen and clicks)
  const show=i=>{
    idx=i;const it=items[i];
    src.textContent=it.say;say=prep(src);
    chipTxt.textContent=it.tool;reply.textContent=it.reply;cap.textContent=it.title;
    ks.classList.remove('on');ks.innerHTML='';
    dots.forEach((d,k)=>d.setAttribute('aria-current',k===i));
    chip.classList.add('ok');stage(4);
  };
  const play=async(i,t)=>{
    const w=ms=>wait(ms,t);
    try{
      while(true){
        show(i);const it=items[i];
        stage(-1);chip.classList.remove('ok');say.set(0);
        await w(600);
        stage(0);say.el.classList.add('live');
        for(let n=1;n<=say.full.length;n++){say.set(n);await w(32)}
        say.el.classList.remove('live');await w(350);
        stage(1);await w(900);chip.classList.add('ok');await w(300);
        const k=K[it.kind];
        if(k){
          stage(2);ks.innerHTML=k.html(it);ks.classList.remove('on');void ks.offsetWidth;ks.classList.add('on');
          await w(500);await k.run(ks,it,w);
          ks.classList.remove('on');await w(500);
        }
        stage(3);await w(2400);
        stage(4);await w(900);
        i=(i+1)%items.length;
      }
    }catch(err){if(err!==DEAD)throw err}
  };
  const start=i=>{if(tok)tok.dead=true;tok={dead:false};play(i,tok)};
  show(0);
  dots.forEach((d,k)=>d.addEventListener('click',()=>{if(still||!visible)show(k);else start(k)}));
  if(still)return;
  new IntersectionObserver(es=>es.forEach(e=>{
    visible=e.isIntersecting;
    if(visible)start(idx);
    else{if(tok)tok.dead=true;say.el.classList.remove('live');show(idx)}
  }),{threshold:.3}).observe(el);
});

// pause motion
const mb=$('.motion');
if(mb)mb.addEventListener('click',()=>{
  const p=mb.getAttribute('aria-pressed')!=='true';
  mb.setAttribute('aria-pressed',p);mb.textContent=p?'Resume motion':'Pause motion';document.body.classList.toggle('paused',p);
});
})();
