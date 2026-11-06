(() => {
  'use strict';
  const root = document.documentElement;
  const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)');
  const finePointer = matchMedia('(hover: hover) and (pointer: fine)');
  const motionToggle = document.querySelector('.motion-toggle');
  let manuallyPaused = false;
  let paused = reduceMotion.matches;
  let frameId = 0;
  root.classList.add('js-ready');

  const menu = document.querySelector('.menu-toggle');
  const links = document.querySelector('.nav-links');
  function closeMenu() {
    menu.setAttribute('aria-expanded', 'false');
    menu.setAttribute('aria-label', 'Open navigation');
    links.classList.remove('open');
  }
  menu.addEventListener('click', () => {
    const open = menu.getAttribute('aria-expanded') !== 'true';
    menu.setAttribute('aria-expanded', String(open));
    menu.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
    links.classList.toggle('open', open);
  });
  links.querySelectorAll('a').forEach(a => a.addEventListener('click', closeMenu));
  document.addEventListener('keydown', event => { if (event.key === 'Escape') closeMenu(); });

  const reveals = document.querySelectorAll('.reveal');
  document.querySelectorAll('.bento, .foundation-cards, .screen-gallery').forEach(group => {
    group.querySelectorAll('.reveal').forEach((el, index) => el.style.setProperty('--reveal-delay', `${Math.min(index * .09, .27)}s`));
  });
  if ('IntersectionObserver' in window) {
    const revealObserver = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) { entry.target.classList.add('visible'); revealObserver.unobserve(entry.target); }
      });
    }, { threshold: .08, rootMargin: '0px 0px -25px 0px' });
    reveals.forEach(el => revealObserver.observe(el));
  } else reveals.forEach(el => el.classList.add('visible'));

  const bars = document.querySelector('.voice-bars');
  for (let i = 0; i < 45; i++) {
    const bar = document.createElement('i');
    bar.style.setProperty('--bar-height', `${5 + Math.sin(i * .65) ** 2 * 29 * Math.sin(Math.PI * i / 45)}px`);
    bar.style.setProperty('--delay', `${i * -.07}s`);
    bars.appendChild(bar);
  }

  const examples = {
    phone: ['Set a timer for ten minutes.', 'ALARMS & TIMERS', 'A quick request becomes a timer on your phone. Keep your hands on what you’re doing.', 'Uses the enabled Alarms & timers connector.'],
    knowledge: ['What are the main points in my notes?', 'YOUR KNOWLEDGE', 'Bring the text or PDFs you’ve added into the conversation. Ask a question and follow the details that matter.', 'Requires documents added to your knowledge base.'],
    search: ['Find a beginner’s guide to astronomy.', 'WEB SEARCH', 'Explore a topic with a connected search tool. Ask follow-up questions without switching out of the conversation.', 'Requires a search connector and an internet connection.'],
    skills: ['Send a WhatsApp message to my friend.', 'SKILLS · MESSAGING', 'Use the WhatsApp skill to guide a voice-led messaging workflow on your phone.', 'Requires WhatsApp, the skill and relevant phone-control permissions.']
  };
  const conversation = document.querySelector('.conversation-body');
  document.querySelectorAll('[data-demo]').forEach(button => button.addEventListener('click', () => {
    document.querySelectorAll('[data-demo]').forEach(item => {
      const selected = item === button;
      item.classList.toggle('active', selected);
      item.setAttribute('aria-pressed', String(selected));
    });
    ['demo-prompt', 'demo-tag', 'demo-answer', 'demo-note'].forEach((id, index) => {
      document.getElementById(id).textContent = examples[button.dataset.demo][index];
    });
    conversation.classList.remove('switching');
    if (!paused) requestAnimationFrame(() => { requestAnimationFrame(() => conversation.classList.add('switching')); });
  }));

  document.querySelectorAll('.tilt-card').forEach(card => {
    card.addEventListener('pointermove', event => {
      if (paused || !finePointer.matches) return;
      const rect = card.getBoundingClientRect();
      const x = (event.clientX - rect.left) / rect.width;
      const y = (event.clientY - rect.top) / rect.height;
      card.style.setProperty('--rx', `${(y - .5) * -3}deg`);
      card.style.setProperty('--ry', `${(x - .5) * 3}deg`);
      card.style.setProperty('--mx', `${x * 100}%`);
      card.style.setProperty('--my', `${y * 100}%`);
    });
    card.addEventListener('pointerleave', () => { card.style.setProperty('--rx', '0deg'); card.style.setProperty('--ry', '0deg'); });
  });

  const product = document.querySelector('.product-reveal');
  const progress = document.querySelector('.scroll-progress');
  let scrollQueued = false;
  function updateScroll() {
    const maxScroll = root.scrollHeight - innerHeight;
    progress.style.transform = `scaleX(${maxScroll > 0 ? scrollY / maxScroll : 0})`;
    if (!paused && innerWidth > 720) product.style.transform = `translateY(${Math.min(scrollY, 900) * -.035}px)`;
    else product.style.transform = '';
    scrollQueued = false;
  }
  addEventListener('scroll', () => {
    if (!scrollQueued) { scrollQueued = true; requestAnimationFrame(updateScroll); }
  }, { passive: true });

  // A quiet field of drifting points. Density is capped, pixels are capped,
  // and the render loop stops when the page is hidden or motion is paused.
  const canvas = document.getElementById('atmosphere');
  const ctx = canvas.getContext('2d');
  let width = 0, height = 0, particles = [], lastFrame = 0;
  function resize() {
    width = innerWidth; height = innerHeight;
    const dpr = Math.min(devicePixelRatio || 1, 1.5);
    canvas.width = Math.round(width * dpr); canvas.height = Math.round(height * dpr);
    if (ctx) ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    const count = width < 720 ? 22 : 65;
    particles = Array.from({length: count}, (_, i) => ({
      x: Math.random() * width, y: Math.random() * height,
      radius: .35 + Math.random() * 1.05, speed: .1 + Math.random() * .19,
      phase: i * 2.3, alpha: .12 + Math.random() * .36
    }));
    updateScroll();
    draw(0, true);
  }
  function draw(time, staticFrame = false) {
    if (!ctx) return;
    ctx.clearRect(0, 0, width, height);
    for (const particle of particles) {
      if (!staticFrame) {
        particle.y -= particle.speed;
        particle.x += Math.sin(time * .00012 + particle.phase) * .08;
        if (particle.y < -3) particle.y = height + 3;
      }
      const edgeWeight = Math.abs(particle.x - width / 2) / (width / 2);
      const opacity = particle.alpha * (.25 + edgeWeight * .75) * (.75 + Math.sin(time * .0007 + particle.phase) * .25);
      ctx.fillStyle = `rgba(200,181,246,${opacity})`;
      ctx.beginPath(); ctx.arc(particle.x, particle.y, particle.radius, 0, Math.PI * 2); ctx.fill();
      if (particle.radius > 1.15) {
        ctx.fillStyle = `rgba(175,137,245,${opacity * .09})`;
        ctx.beginPath(); ctx.arc(particle.x, particle.y, particle.radius * 4, 0, Math.PI * 2); ctx.fill();
      }
    }
  }
  function animate(time) {
    frameId = 0;
    if (paused || document.hidden) return;
    if (time - lastFrame > 32) { draw(time); lastFrame = time; }
    frameId = requestAnimationFrame(animate);
  }
  function syncMotion() {
    paused = manuallyPaused || reduceMotion.matches;
    root.classList.toggle('motion-paused', paused);
    motionToggle.setAttribute('aria-pressed', String(paused));
    motionToggle.textContent = reduceMotion.matches ? 'Reduced motion enabled' : paused ? 'Resume motion' : 'Pause motion';
    motionToggle.disabled = reduceMotion.matches;
    cancelAnimationFrame(frameId); frameId = 0;
    if (!paused && !document.hidden) frameId = requestAnimationFrame(animate);
    updateScroll();
  }
  motionToggle.addEventListener('click', () => { manuallyPaused = !manuallyPaused; syncMotion(); });
  reduceMotion.addEventListener('change', syncMotion);
  document.addEventListener('visibilitychange', syncMotion);
  addEventListener('resize', resize, { passive: true });
  resize(); syncMotion();
})();
