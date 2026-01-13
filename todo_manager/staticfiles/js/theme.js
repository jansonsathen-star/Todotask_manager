// Theme toggle: persist to localStorage and set body class
(function(){
  const btn = document.getElementById('theme-toggle');
  const icon = document.getElementById('theme-icon');
  function setIcon(dark){
    if(!icon) return;
    if(dark){
      // sun icon
      icon.innerHTML = '<path d="M12 3v2"></path><path d="M12 19v2"></path><path d="M3 12h2"></path><path d="M19 12h2"></path><path d="M5 5l1.5 1.5"></path><path d="M17.5 17.5L19 19"></path><path d="M5 19l1.5-1.5"></path><path d="M17.5 6.5L19 5"></path><circle cx="12" cy="12" r="4"></circle>';
    } else {
      // moon icon
      icon.innerHTML = '<path d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z"></path>';
    }
  }
  function applyTheme(dark){
    if(dark) document.body.classList.add('dark-mode'); else document.body.classList.remove('dark-mode');
    setIcon(dark);
  }
  // read pref
  let pref = localStorage.getItem('site-theme');
  if(pref===null){
    // default: match system
    pref = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }
  applyTheme(pref==='dark');
  if(btn){
    btn.addEventListener('click', function(){
      const isDark = document.body.classList.toggle('dark-mode');
      localStorage.setItem('site-theme', isDark? 'dark':'light');
      setIcon(isDark);
    });
  }
  // nav underline: animate left->right when clicked, keep it briefly before navigation
  try{
    const navLinks = document.querySelectorAll('.navbar .nav-link');
    navLinks.forEach(a => {
      a.addEventListener('click', (ev)=>{
        // add underline class to clicked link, remove from others
        navLinks.forEach(x=>x.classList.remove('underline-active'));
        a.classList.add('underline-active');
        // allow animation to show before navigation (if same-page anchor, keep it)
        setTimeout(()=>{ a.classList.remove('underline-active'); }, 1200);
      });
    });
  }catch(e){ /* ignore in non-browser environments */ }
})();
