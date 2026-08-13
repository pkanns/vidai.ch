/* ============================================================
   NAV.JS — Navigation behaviour
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

  /* NOTE: the #kontakt-form handler that used to live here was removed —
     the Kontakt section now uses a Calendly embed, so that form element
     no longer exists in the DOM. Removing dead code per site cleanup
     rules. */

})();
