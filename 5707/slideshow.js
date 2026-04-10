/* slideshow.js — shared slideshow logic for TimothySkinnerHouse site */
(function () {
  'use strict';

  function initSlideshow(wrap) {
    const stage   = wrap.querySelector('.slideshow-stage');
    const slides  = Array.from(wrap.querySelectorAll('.slide'));
    const prevBtn = wrap.querySelector('.slide-btn.prev');
    const nextBtn = wrap.querySelector('.slide-btn.next');
    const dotsWrap = wrap.querySelector('.slide-dots');
    const captionEl = wrap.querySelector('.slideshow-caption > .caption-text');
    const counterEl = wrap.querySelector('.slide-counter');

    if (!stage || slides.length === 0) return;

    let current = 0;
    let autoTimer = null;
    const AUTO_MS = 5000;

    // build dots
    let dots = [];
    if (dotsWrap) {
      dotsWrap.innerHTML = '';
      slides.forEach((_, i) => {
        const d = document.createElement('button');
        d.className = 'slide-dot';
        d.setAttribute('aria-label', 'Go to slide ' + (i + 1));
        d.addEventListener('click', () => go(i));
        dotsWrap.appendChild(d);
        dots.push(d);
      });
    }

    function update(idx) {
      slides[current].classList.remove('active');
      if (dots[current]) dots[current].classList.remove('active');
      current = (idx + slides.length) % slides.length;
      slides[current].classList.add('active');
      if (dots[current]) dots[current].classList.add('active');
      if (captionEl) {
        const cap = slides[current].dataset.caption || '';
        captionEl.textContent = cap;
      }
      if (counterEl) {
        counterEl.textContent = (current + 1) + ' / ' + slides.length;
      }
    }

    function go(idx) {
      stopAuto();
      update(idx);
      startAuto();
    }

    function startAuto() {
      if (slides.length <= 1) return;
      autoTimer = setInterval(() => update(current + 1), AUTO_MS);
    }

    function stopAuto() {
      clearInterval(autoTimer);
      autoTimer = null;
    }

    if (prevBtn) prevBtn.addEventListener('click', () => go(current - 1));
    if (nextBtn) nextBtn.addEventListener('click', () => go(current + 1));

    // keyboard
    wrap.setAttribute('tabindex', '0');
    wrap.addEventListener('keydown', e => {
      if (e.key === 'ArrowLeft')  { e.preventDefault(); go(current - 1); }
      if (e.key === 'ArrowRight') { e.preventDefault(); go(current + 1); }
    });

    // touch / swipe
    let touchStartX = 0;
    stage.addEventListener('touchstart', e => { touchStartX = e.touches[0].clientX; }, { passive: true });
    stage.addEventListener('touchend',   e => {
      const dx = e.changedTouches[0].clientX - touchStartX;
      if (Math.abs(dx) > 40) go(dx < 0 ? current + 1 : current - 1);
    }, { passive: true });

    // pause on hover
    wrap.addEventListener('mouseenter', stopAuto);
    wrap.addEventListener('mouseleave', startAuto);

    // init first slide
    slides[0].classList.add('active');
    if (dots[0]) dots[0].classList.add('active');
    if (captionEl) captionEl.textContent = slides[0].dataset.caption || '';
    if (counterEl) counterEl.textContent = '1 / ' + slides.length;

    startAuto();
  }

  // init all slideshows when DOM is ready
  function initAll() {
    document.querySelectorAll('.slideshow-wrap').forEach(initSlideshow);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAll);
  } else {
    initAll();
  }

  // mobile nav toggle
  function initNav() {
    const toggle = document.querySelector('.nav-toggle');
    const drawer = document.querySelector('.nav-drawer');
    if (!toggle || !drawer) return;
    toggle.addEventListener('click', () => {
      const open = drawer.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    // close drawer on link click
    drawer.querySelectorAll('a').forEach(a => {
      a.addEventListener('click', () => {
        drawer.classList.remove('open');
        toggle.setAttribute('aria-expanded', 'false');
      });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initNav);
  } else {
    initNav();
  }
})();
