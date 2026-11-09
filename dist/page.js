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

// use-case animation: every example types out what you say, then Ultron "thinks" and answers
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
const isPaused=()=>document.body.classList.contains('paused');
const wait=async(ms,tok)=>{await sleep(ms);while(isPaused()&&!tok.dead)await sleep(200)};
// split an element's own text into a typed part and a hidden rest, so the layout never jumps
function prep(el){
  const tn=[...el.childNodes].find(n=>n.nodeType===3&&n.textContent.trim());
  if(!tn)return null;
  const full=tn.textContent,a=document.createElement('span'),b=document.createElement('span');
  a.className='ty';b.className='ty-h';a.textContent=full;tn.replaceWith(a,b);
  return {el,a,b,full,set(n){a.textContent=full.slice(0,n);b.textContent=full.slice(n)}};
}
async function typeTo(t,ms,tok){
  t.el.classList.add('live');
  for(let i=1;i<=t.full.length;i++){
    if(tok.dead)return false;
    t.set(i);await wait(ms,tok);
  }
  t.el.classList.remove('live');return true;
}
const STAGES=['s-hear','s-tool','s-do','s-say'];
function setStage(sc,k){
  // k: index into STAGES, or -1 reset, or 4 = finished (everything visible, steps all done)
  STAGES.concat('s-fin').forEach(c=>sc.el.classList.remove(c));
  if(k>=0&&k<4)sc.el.classList.add(STAGES[k]);
  if(k>=4)sc.el.classList.add('s-fin');
  sc.steps.forEach((li,i)=>{li.classList.toggle('on',i===k);li.classList.toggle('done',k>=0&&i<k||k>=4)});
  sc.status.textContent=['Listening','Thinking','Working','Speaking','Done'][k]||'Ready';
}
async function playScene(sc,tok,delay){
  setStage(sc,-1);sc.chip.classList.remove('ok');sc.say.set(0);
  await wait(delay,tok);if(tok.dead)return;
  while(!tok.dead){
    setStage(sc,0);sc.chip.classList.remove('ok');
    if(!await typeTo(sc.say,32,tok))return;
    await wait(350,tok);if(tok.dead)return;
    setStage(sc,1);await wait(1100,tok);if(tok.dead)return;
    sc.chip.classList.add('ok');await wait(250,tok);if(tok.dead)return;
    setStage(sc,2);await wait(1500,tok);if(tok.dead)return;
    setStage(sc,3);await wait(1700,tok);if(tok.dead)return;
    setStage(sc,4);await wait(3200,tok);if(tok.dead)return;
    setStage(sc,-1);sc.say.set(0);await wait(700,tok);
  }
}
function stopScene(sc){
  // off screen: stop, and leave the finished picture so nothing is ever blank
  if(sc.tok)sc.tok.dead=true;
  sc.say.el.classList.remove('live');
  sc.say.set(sc.say.full.length);sc.chip.classList.add('ok');setStage(sc,4);
}
if(!still){
  const scenes=$$('.sc').map(el=>{
    const bub=$('.bub',el),src=$('.ty-src',bub);
    const say=prep(src)||{set(){},full:"",el:src};
    const sc={el,say,bub,chip:$('.schip',el),status:$('.sst',el),steps:$$('.ss li',el),tok:null,i:0};
    return sc;
  });
  const tries=[];
  $$('.tool .try').forEach(el=>{const t=prep(el);if(t)tries.push({el:el.closest('.tool'),t,cls:el.classList})});
  const sio=new IntersectionObserver(es=>es.forEach(e=>{
    const sc=scenes.find(x=>x.el===e.target);if(!sc)return;
    if(e.isIntersecting){
      if(sc.tok&&!sc.tok.dead)return;
      sc.tok={dead:false};playScene(sc,sc.tok,300);
    }else stopScene(sc);
  }),{threshold:.45});
  scenes.forEach(sc=>{setStage(sc,4);sio.observe(sc.el)});
  const tio=new IntersectionObserver(es=>es.forEach(async e=>{
    const x=tries.find(y=>y.el===e.target);if(!x)return;
    if(e.isIntersecting){
      if(x.tok&&!x.tok.dead)return;
      x.tok={dead:false};x.cls.remove('done');x.t.set(0);
      if(await typeTo(x.t,26,x.tok))x.cls.add('done');
    }else if(x.tok){x.tok.dead=true;x.t.set(x.t.full.length);x.t.el.classList.remove('live');x.cls.add('done')}
  }),{threshold:.6});
  tries.forEach(x=>tio.observe(x.el));
}

// pause motion
const mb=$('.motion');
if(mb)mb.addEventListener('click',()=>{
  const p=mb.getAttribute('aria-pressed')!=='true';
  mb.setAttribute('aria-pressed',p);mb.textContent=p?'Resume motion':'Pause motion';document.body.classList.toggle('paused',p);
});
})();
