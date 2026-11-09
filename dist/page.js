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

// phone demo: plays this page's examples one after another (hear, pick the tool, do it, answer)
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
const STAGES=['s-hear','s-tool','s-do','s-say'];
$$('.demo').forEach(el=>{
  let items;try{items=JSON.parse(el.dataset.demo)}catch(_){return}
  el.classList.add('js');
  const bub=$('.bub',el),src=$('.ty-src',bub),chip=$('.schip',el),chipTxt=$('span',chip),res=$('.sres span',el);
  const status=$('.sst',el),cap=$('.dcap',el),dots=$$('.dots button',el);
  let say=prep(src),cur=0,tok=null,visible=false;
  const stage=k=>{
    STAGES.concat('s-fin').forEach(c=>el.classList.remove(c));
    if(k>=0&&k<4)el.classList.add(STAGES[k]);
    if(k>=4)el.classList.add('s-fin');
    status.textContent=['Listening','Thinking','Working','Speaking','Done'][k]||'Ready';
  };
  // show example i as a finished picture (used for reduced motion, off screen and clicks)
  const show=(i)=>{
    cur=i;const it=items[i];
    src.textContent=it.say;say=prep(src);
    chipTxt.textContent=it.tool;res.textContent=it.result;cap.textContent=it.title;
    dots.forEach((d,k)=>d.setAttribute('aria-current',k===i));
    chip.classList.add('ok');stage(4);
  };
  const play=async(i,t)=>{
    while(!t.dead){
      show(i);stage(-1);chip.classList.remove('ok');say.set(0);
      await wait(500,t);if(t.dead)return;
      stage(0);
      el.classList.add('typing');
      say.el.classList.add('live');
      for(let n=1;n<=say.full.length;n++){if(t.dead)return;say.set(n);await wait(32,t)}
      say.el.classList.remove('live');
      await wait(350,t);if(t.dead)return;
      stage(1);await wait(1000,t);if(t.dead)return;
      chip.classList.add('ok');await wait(250,t);if(t.dead)return;
      stage(2);await wait(1300,t);if(t.dead)return;
      stage(3);await wait(1700,t);if(t.dead)return;
      stage(4);await wait(2600,t);if(t.dead)return;
      i=(i+1)%items.length;
    }
  };
  const start=(i)=>{if(tok)tok.dead=true;tok={dead:false};play(i,tok)};
  show(0);
  dots.forEach((d,k)=>d.addEventListener('click',()=>{if(still||!visible){show(k)}else start(k)}));
  if(still)return;
  new IntersectionObserver(es=>es.forEach(e=>{
    visible=e.isIntersecting;
    if(visible)start(cur);
    else{if(tok)tok.dead=true;say.el.classList.remove('live');show(cur)}
  }),{threshold:.35}).observe(el);
});

// pause motion
const mb=$('.motion');
if(mb)mb.addEventListener('click',()=>{
  const p=mb.getAttribute('aria-pressed')!=='true';
  mb.setAttribute('aria-pressed',p);mb.textContent=p?'Resume motion':'Pause motion';document.body.classList.toggle('paused',p);
});
})();
