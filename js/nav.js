/* ============================================================
   NAV.JS — Navigation behaviour + contact form handler
   Vidai AG · vidai.ch
   ============================================================ */

(function () {
  'use strict';

  /* ── SCROLL SHADOW ── */
  const nav = document.querySelector('nav');

  window.addEventListener('scroll', () => {
    if (window.scrollY > 20) {
      nav.classList.add('scrolled');
    } else {
      nav.classList.remove('scrolled');
    }
  }, { passive: true });

  /* ── MOBILE HAMBURGER ── */
  const hamburger = document.querySelector('.nav-hamburger');
  const navLinks  = document.querySelector('.nav-links');

  if (hamburger && navLinks) {
    hamburger.addEventListener('click', () => {
      hamburger.classList.toggle('open');
      navLinks.classList.toggle('open');
    });

    // Close on link click
    navLinks.querySelectorAll('a').forEach((link) => {
      link.addEventListener('click', () => {
        hamburger.classList.remove('open');
        navLinks.classList.remove('open');
      });
    });
  }

  /* ── CONTACT FORM ── */
  const form    = document.getElementById('kontakt-form');
  const success = document.getElementById('form-success');

  if (form) {
    form.addEventListener('submit', (e) => {
      e.preventDefault();

      const data = {
        name:    form.querySelector('[name="name"]').value.trim(),
        email:   form.querySelector('[name="email"]').value.trim(),
        company: form.querySelector('[name="company"]').value.trim(),
        message: form.querySelector('[name="message"]').value.trim(),
      };

      // Basic validation
      if (!data.name || !data.email || !data.message) return;

      // Encode as mailto for now — can be replaced with Formspree/Netlify Forms
      const subject = encodeURIComponent('Vidai AG — Kontaktanfrage von ' + data.name);
      const body    = encodeURIComponent(
        'Name: '      + data.name    + '\n' +
        'E-Mail: '    + data.email   + '\n' +
        'Unternehmen: '+ data.company + '\n\n' +
        data.message
      );

      window.location.href = 'mailto:info@vidai.ch?subject=' + subject + '&body=' + body;

      // Show success message
      form.style.display = 'none';
      if (success) success.classList.add('visible');
    });
  }

})();
