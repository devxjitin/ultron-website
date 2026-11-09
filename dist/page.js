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
async function playUc(c,tok,delay){
  c.cls.remove('done');
  c.say.set(0);if(c.does)c.does.set(0);
  await wait(delay,tok);if(tok.dead)return;
  if(!await typeTo(c.say,30,tok))return;
  if(c.does){
    await wait(250,tok);if(tok.dead)return;
    c.does.el.classList.add('think');await wait(750,tok);c.does.el.classList.remove('think');
    if(tok.dead)return;
    if(!await typeTo(c.does,13,tok))return;
  }
  c.cls.add('done');
}
if(!still){
  const cards=[];
  $$('.uc').forEach((el,i)=>{
    const say=prep($('.uc-say',el)),does=prep($('.uc-does',el));
    if(say&&does)cards.push({el,cls:el.classList,say,does,i:i%3});
  });
  $$('.tool .try').forEach(el=>{
    const say=prep(el);if(say)cards.push({el:el.closest('.tool'),cls:el.classList,say,does:null,i:0});
  });
  const aio=new IntersectionObserver(es=>es.forEach(e=>{
    const c=cards.find(x=>x.el===e.target);if(!c)return;
    if(e.isIntersecting){
      if(c.tok&&!c.tok.dead)return;
      c.tok={dead:false};playUc(c,c.tok,c.i*350);
    }else if(c.tok){
      // off screen: stop and show the full text again, so it is never empty when you scroll back
      c.tok.dead=true;c.say.set(c.say.full.length);if(c.does)c.does.set(c.does.full.length);
      c.say.el.classList.remove('live');if(c.does){c.does.el.classList.remove('live','think')}
      c.cls.add('done');
    }
  }),{threshold:.6});
  cards.forEach(c=>aio.observe(c.el));
}

// pause motion
const mb=$('.motion');
if(mb)mb.addEventListener('click',()=>{
  const p=mb.getAttribute('aria-pressed')!=='true';
  mb.setAttribute('aria-pressed',p);mb.textContent=p?'Resume motion':'Pause motion';document.body.classList.toggle('paused',p);
});
})();
