(()=>{
const $=(s,r=document)=>r.querySelector(s),$$=(s,r=document)=>[...r.querySelectorAll(s)];
const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;

// mobile nav
const tg=$('.menu-toggle'),links=$('#nav-links');
const closeNav=()=>{links.classList.remove('open');tg.setAttribute('aria-expanded','false')};
tg.addEventListener('click',()=>{const o=links.classList.toggle('open');tg.setAttribute('aria-expanded',o)});
$$('a',links).forEach(a=>a.addEventListener('click',closeNav));

// reveal on scroll
// two-way reveal: animates in when entering from either edge, resets when fully out of view
const io=new IntersectionObserver(es=>es.forEach(e=>{
  const t=e.target;
  if(e.intersectionRatio>=.12||(e.isIntersecting&&e.intersectionRect.height>=innerHeight*.5)){
    if(!t.classList.contains('in')){t.classList.add('in');setTimeout(()=>{t.style.transitionDelay=''},1200)}
  }else if(!e.isIntersecting&&!reduce){
    t.classList.remove('in');
    t.classList.toggle('from-top',e.boundingClientRect.bottom<=0);
  }
}),{threshold:[0,.12],rootMargin:'0px 0px -40px 0px'});
$$('.reveal').forEach(el=>{const sib=[...el.parentElement.children].filter(c=>c.classList.contains('reveal'));el.style.transitionDelay=Math.min(sib.indexOf(el),5)*70+'ms';io.observe(el)});

// count-up
const cio=new IntersectionObserver(es=>es.forEach(e=>{
  if(!e.isIntersecting)return;cio.unobserve(e.target);
  const b=e.target,n=+b.dataset.count,suf=b.dataset.suffix||'';
  if(reduce){b.textContent=n+suf;return}
  const t0=performance.now(),d=1200;
  const step=t=>{const p=Math.min(1,(t-t0)/d),v=Math.round(n*(1-Math.pow(1-p,3)));b.textContent=v+(p===1?suf:'');if(p<1)requestAnimationFrame(step)};
  requestAnimationFrame(step);
}),{threshold:.6});
$$('[data-count]').forEach(b=>cio.observe(b));

// connector filters
$$('.filters button').forEach(btn=>btn.addEventListener('click',()=>{
  $$('.filters button').forEach(b=>b.classList.toggle('on',b===btn));
  const f=btn.dataset.f;
  $$('.conn').forEach(c=>{c.hidden=!(f==='all'||c.dataset.c===f)});
}));

// dust canvas
const cv=$('#dust'),cx=cv.getContext('2d');let W,H,dots=[],paused=reduce,raf;
const size=()=>{const r=devicePixelRatio>1?1.5:1;W=cv.width=innerWidth*r;H=cv.height=innerHeight*r;
  dots=Array.from({length:Math.min(90,Math.round(innerWidth/14))},()=>({x:Math.random()*W,y:Math.random()*H,r:(Math.random()*1.3+.3)*r,s:Math.random()*.25+.05,a:Math.random()*.6+.2,p:Math.random()*6}))};
const draw=t=>{cx.clearRect(0,0,W,H);
  for(const d of dots){d.y-=d.s;if(d.y<-4){d.y=H+4;d.x=Math.random()*W}
    cx.globalAlpha=d.a*(.6+.4*Math.sin(t/900+d.p));cx.fillStyle='#b9b3ff';cx.beginPath();cx.arc(d.x,d.y,d.r,0,6.283);cx.fill()}
  raf=paused||document.hidden?0:requestAnimationFrame(draw)};
addEventListener('resize',size);size();draw(0);
document.addEventListener('visibilitychange',()=>{if(!document.hidden&&!paused&&!raf)raf=requestAnimationFrame(draw)});

// pause motion
const mb=$('.motion');
mb.addEventListener('click',()=>{paused=!paused;mb.setAttribute('aria-pressed',paused);mb.textContent=paused?'Resume motion':'Pause motion';document.body.classList.toggle('paused',paused);if(!paused)raf=requestAnimationFrame(draw)});
if(reduce){mb.hidden=true}
})();
// app theme switch: swap every real screenshot between dark and light captures
(()=>{
  const imgs=[...document.querySelectorAll('img[data-shot]')];
  const btns=[...document.querySelectorAll('.theme-switch button')];
  btns.forEach(b=>b.addEventListener('click',()=>{
    const t=b.dataset.theme;
    btns.forEach(x=>{x.classList.toggle('on',x===b);x.setAttribute('aria-pressed',x===b)});
    imgs.forEach(i=>{if(!i.closest('#app'))return;const n=new Image();n.onload=()=>{i.classList.add('swap');setTimeout(()=>{i.src=n.src;i.classList.remove('swap')},180)};n.src=`assets/app/${t}-${i.dataset.shot}.webp`});
  }));
})();

// smooth inertial scrolling (Lenis) + scroll-linked card spread
(()=>{
  const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
  const grid=document.getElementById('spread');
  const cards=grid?[...grid.children]:[];
  const ease=t=>1-Math.pow(1-t,3);
  const update=()=>{
    if(!grid)return;
    const r=grid.getBoundingClientRect(),vh=innerHeight;
    const p=Math.min(1,Math.max(0,(vh*0.95-r.top)/(vh*0.75)));
    const s=reduce?1:ease(p);
    cards.forEach(c=>c.style.setProperty('--s',s.toFixed(3)));
  };
  update();
  let lenis=null;
  if(window.Lenis&&!reduce){
    lenis=new Lenis({duration:1.15,easing:t=>Math.min(1,1.001-Math.pow(2,-10*t)),smoothWheel:true});
    lenis.on('scroll',update);
    const raf=t=>{lenis.raf(t);requestAnimationFrame(raf)};requestAnimationFrame(raf);
    document.querySelectorAll('a[href^="#"]').forEach(a=>a.addEventListener('click',e=>{
      const id=a.getAttribute('href');if(id.length<2)return;
      const el=document.querySelector(id);if(!el)return;e.preventDefault();lenis.scrollTo(el,{offset:-80});
    }));
  }else addEventListener('scroll',update,{passive:true});
  addEventListener('resize',update);
})();

// plan buttons: open a WhatsApp chat when a number is set, otherwise the email already in each link
(()=>{
  // Orders go to this WhatsApp number. Country code first, digits only, for example "919876543210". Empty: orders use email.
  const BUY_WHATSAPP='';
  const number=BUY_WHATSAPP.replace(/\D/g,'');
  if(!number)return;
  const wa=text=>`https://wa.me/${number}?text=${encodeURIComponent(text)}`;
  document.querySelectorAll('.buy').forEach(a=>{
    const {plan,price}=a.dataset;
    a.href=wa(`Hi, I want the Ultron ${plan} plan (₹${Number(price).toLocaleString('en-IN')}).`);
    a.target='_blank';a.rel='noopener';
  });
  const card=document.querySelector('[data-wa]');
  if(card){
    card.hidden=false;
    const link=card.querySelector('[data-wa-link]');
    link.href=wa('Hi, I have a question about Ultron.');link.target='_blank';link.rel='noopener';
  }
})();
