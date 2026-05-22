// Vision GO — interactions
(function () {
  'use strict';

  // — Nav scroll state + mobile toggle —
  const nav = document.querySelector('.nav');
  const toggle = document.querySelector('.nav__toggle');

  if (nav) {
    const setScrolled = () => nav.classList.toggle('nav--scrolled', window.scrollY > 8);
    setScrolled();
    window.addEventListener('scroll', setScrolled, { passive: true });
  }

  if (toggle && nav) {
    toggle.addEventListener('click', () => {
      const opened = nav.classList.toggle('nav--open');
      toggle.setAttribute('aria-expanded', opened ? 'true' : 'false');
      document.body.style.overflow = opened ? 'hidden' : '';
    });
    document.querySelectorAll('.nav__link').forEach((l) =>
      l.addEventListener('click', () => {
        nav.classList.remove('nav--open');
        toggle.setAttribute('aria-expanded', 'false');
        document.body.style.overflow = '';
      })
    );
  }

  // — Reveal on scroll —
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (e.isIntersecting) {
            e.target.classList.add('is-visible');
            io.unobserve(e.target);
          }
        });
      },
      { rootMargin: '0px 0px -60px 0px', threshold: 0.05 }
    );
    document.querySelectorAll('.reveal').forEach((el) => io.observe(el));
  } else {
    document.querySelectorAll('.reveal').forEach((el) => el.classList.add('is-visible'));
  }

  // — Cookie consent (DSGVO-friendly with explicit Accept/Reject) —
  const consent = document.querySelector('.consent');
  if (consent) {
    const KEY = 'vg_consent_v2';
    const stored = localStorage.getItem(KEY);
    if (!stored) {
      // Delay slightly so it doesn't pop up immediately
      setTimeout(() => consent.classList.add('is-visible'), 800);
    }
    consent.querySelectorAll('[data-consent]').forEach((btn) => {
      btn.addEventListener('click', () => {
        localStorage.setItem(KEY, btn.dataset.consent);
        localStorage.setItem(KEY + '_at', new Date().toISOString());
        consent.classList.remove('is-visible');
        // If user accepts and we add analytics later, fire window event
        if (btn.dataset.consent === 'all') {
          window.dispatchEvent(new CustomEvent('vg:consent', { detail: { level: 'all' } }));
        }
      });
    });
  }

  // — Year auto-update in footer —
  document.querySelectorAll('[data-year]').forEach((el) => (el.textContent = new Date().getFullYear()));

  // — Contact form (mailto fallback) —
  const form = document.querySelector('[data-contact-form]');
  if (form) {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const fd = new FormData(form);
      const name = fd.get('name') || '';
      const email = fd.get('email') || '';
      const company = fd.get('company') || '';
      const message = fd.get('message') || '';
      const subject = `Anfrage von ${name}${company ? ' (' + company + ')' : ''}`;
      const body = `Name: ${name}\nE-Mail: ${email}\nUnternehmen: ${company}\n\n${message}`;
      window.location.href = `mailto:info@visiongo.at?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
    });

    // Hide mobile CTA when form has focus
    form.addEventListener('focusin', () => document.body.classList.add('has-form-focus'));
    form.addEventListener('focusout', () => {
      setTimeout(() => {
        if (!form.contains(document.activeElement)) {
          document.body.classList.remove('has-form-focus');
        }
      }, 120);
    });
  }

  // — Newsletter form —
  const news = document.querySelector('[data-newsletter]');
  if (news) {
    news.addEventListener('submit', (e) => {
      e.preventDefault();
      const email = news.querySelector('input[type="email"]').value;
      if (!email) return;
      window.location.href = `mailto:info@visiongo.at?subject=Newsletter-Abonnement&body=${encodeURIComponent('Bitte tragen Sie mich in den Vision GO Newsletter ein: ' + email)}`;
    });
  }

  // — Blog search (client-side filter) —
  const blogSearch = document.querySelector('[data-blog-search]');
  if (blogSearch) {
    const noResults = document.querySelector('.blog-search__no-results');
    const cards = document.querySelectorAll('.post-card');
    blogSearch.addEventListener('input', (e) => {
      const q = e.target.value.trim().toLowerCase();
      let visibleCount = 0;
      cards.forEach((card) => {
        const text = card.textContent.toLowerCase();
        const matches = !q || text.includes(q);
        card.style.display = matches ? '' : 'none';
        if (matches) visibleCount++;
      });
      if (noResults) noResults.classList.toggle('is-visible', visibleCount === 0);
    });
  }

  // — Mobile CTA bar: hide on scroll up near top, show on scroll —
  const ctaBar = document.querySelector('.mobile-cta-bar');
  if (ctaBar) {
    let lastY = 0;
    let ticking = false;
    window.addEventListener(
      'scroll',
      () => {
        if (!ticking) {
          window.requestAnimationFrame(() => {
            const y = window.scrollY;
            const goingDown = y > lastY;
            // Hide at very top, show otherwise
            if (y < 100) ctaBar.style.transform = 'translateY(110%)';
            else ctaBar.style.transform = 'translateY(0)';
            lastY = y;
            ticking = false;
          });
          ticking = true;
        }
      },
      { passive: true }
    );
  }
})();
