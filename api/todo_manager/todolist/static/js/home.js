/** @format */

document.addEventListener('DOMContentLoaded', function () {
  // Left-side collapsible panel logic
  const panel = document.getElementById('left-panel');
  const openBtn = document.getElementById('left-panel-open');
  const closeBtn = document.getElementById('left-panel-close');
  if (!panel) return;

  function openPanel() {
    panel.classList.add('open');
    panel.setAttribute('aria-hidden', 'false');
    if (openBtn) openBtn.setAttribute('aria-expanded', 'true');
    document.body.style.overflow = 'hidden';
  }
  function closePanel() {
    panel.classList.remove('open');
    panel.classList.remove('panel-selected');
    panel.setAttribute('aria-hidden', 'true');
    if (openBtn) openBtn.setAttribute('aria-expanded', 'false');
    document.body.style.overflow = '';
  }

  if (openBtn) openBtn.addEventListener('click', openPanel);
  if (closeBtn) closeBtn.addEventListener('click', closePanel);

  // Close when clicking outside content
  panel.addEventListener('click', function (e) {
    if (e.target === panel) closePanel();
  });

  // Panel link animation + navigate
  const links = panel.querySelectorAll('.panel-link');
  links.forEach((a) => {
    a.addEventListener('click', function (ev) {
      // if href is same-page allow immediate
      ev.preventDefault();
      const href = a.getAttribute('href');
      // mark selected for animation
      links.forEach((x) => x.classList.remove('selected'));
      a.classList.add('selected');
      // mark panel as selected (changes background)
      panel.classList.add('panel-selected');
      // ensure panel open while animating
      openPanel();
      // after short animation, navigate
      setTimeout(() => {
        window.location.href = href;
      }, 380);
    });
  });
  // Aside toggle (page-specific)
  const asideToggle = document.getElementById('aside-toggle');
  const asideDetails = document.getElementById('aside-details');
  if (asideToggle && asideDetails) {
    asideToggle.addEventListener('click', function () {
      const shown = asideDetails.style.display !== 'none';
      asideDetails.style.display = shown ? 'none' : 'block';
      asideToggle.textContent = shown ? 'Toggle Details' : 'Hide Details';
    });
  }
});
