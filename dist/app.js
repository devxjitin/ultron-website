const examples = {
  phone: ['Set a timer for 10 minutes.', 'ALARMS & TIMERS', 'A quick request becomes a timer on your phone. Keep your hands on what you’re doing.', 'Uses the enabled Alarms & timers connector.'],
  knowledge: ['What are the main points in my notes?', 'YOUR KNOWLEDGE', 'Ask about the text or PDFs you’ve added to Ultron, and bring relevant information into your conversation.', 'Requires documents added to your knowledge base.'],
  search: ['Find a beginner’s guide to astronomy.', 'WEB SEARCH', 'Explore a topic through the connected search tools and keep asking follow-up questions by voice.', 'Uses an enabled search connector and an internet connection.'],
  skills: ['Send a WhatsApp message to my friend.', 'SKILLS · MESSAGING', 'Use the WhatsApp skill to guide a voice-led messaging workflow on your phone.', 'Requires the skill, WhatsApp, and relevant phone-control permissions.']
};
document.querySelectorAll('[data-demo]').forEach(button => button.addEventListener('click', () => {
  document.querySelectorAll('[data-demo]').forEach(item => { item.classList.toggle('active', item === button); item.setAttribute('aria-pressed', String(item === button)); });
  ['demo-prompt', 'demo-tag', 'demo-answer', 'demo-note'].forEach((id, index) => { document.getElementById(id).textContent = examples[button.dataset.demo][index]; });
}));
const menu = document.querySelector('.menu-toggle');
const links = document.querySelector('.nav-links');
function closeMenu() { menu.setAttribute('aria-expanded', 'false'); menu.setAttribute('aria-label', 'Open navigation'); links.classList.remove('open'); }
menu.addEventListener('click', () => { const open = menu.getAttribute('aria-expanded') !== 'true'; menu.setAttribute('aria-expanded', String(open)); menu.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation'); links.classList.toggle('open', open); });
links.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
document.addEventListener('keydown', event => { if (event.key === 'Escape') closeMenu(); });
const wave = document.querySelector('.wave');
for (let i = 0; i < 45; i++) { const bar = document.createElement('i'); bar.style.setProperty('--height', `${12 + Math.pow(Math.sin(i * 0.36), 2) * 65 * Math.sin(Math.PI * i / 45)}px`); bar.style.setProperty('--delay', `${i * -0.08}s`); wave.appendChild(bar); }
