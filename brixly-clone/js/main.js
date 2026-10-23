(function () {
  const body = document.body;
  const items = document.querySelectorAll('[data-menu]');
  const menuBtn = document.querySelector('.menu-btn');
  const desktop = window.matchMedia('(min-width: 1024px)');

  const overlay = document.createElement('div');
  overlay.className = 'nav-overlay';
  body.appendChild(overlay);

  function closeAll(except) {
    items.forEach((item) => {
      if (item === except) return;
      item.classList.remove('open');
      item.querySelector('.menu-toggle').setAttribute('aria-expanded', 'false');
    });
    if (!except) body.classList.remove('menu-open');
  }

  function toggle(item) {
    const open = !item.classList.contains('open');
    closeAll(item);
    item.classList.toggle('open', open);
    item.querySelector('.menu-toggle').setAttribute('aria-expanded', String(open));
    body.classList.toggle('menu-open', open && desktop.matches);
  }

  items.forEach((item) => {
    item.querySelector('.menu-toggle').addEventListener('click', () => toggle(item));
  });

  overlay.addEventListener('click', () => closeAll());

  menuBtn.addEventListener('click', () => {
    const open = body.classList.toggle('nav-open');
    menuBtn.setAttribute('aria-expanded', String(open));
    menuBtn.setAttribute('aria-label', open ? 'Stäng menyn' : 'Öppna menyn');
  });

  document.addEventListener('keydown', (e) => {
    if (e.key !== 'Escape') return;
    closeAll();
    body.classList.remove('nav-open');
    menuBtn.setAttribute('aria-expanded', 'false');
  });

  // Close menus when following an in-page link
  document.querySelectorAll('.menu a').forEach((a) => {
    a.addEventListener('click', () => {
      closeAll();
      body.classList.remove('nav-open');
    });
  });

  desktop.addEventListener('change', () => {
    closeAll();
    body.classList.remove('nav-open');
  });

  // Reuse the header logo in the footer
  const footerLogo = document.querySelector('.logo-footer');
  const svg = document.querySelector('.site-header .logo svg');
  if (footerLogo && svg) footerLogo.appendChild(svg.cloneNode(true));

  document.getElementById('year').textContent = new Date().getFullYear();
})();
