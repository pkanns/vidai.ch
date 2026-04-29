/* ============================================================
   ANIMATIONS.JS — Scroll-triggered fade-up observer
   Vidai AG · vidai.ch
   ============================================================ */

(function () {
  'use strict';

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry, i) => {
        if (entry.isIntersecting) {
          setTimeout(() => {
            entry.target.classList.add('visible');
          }, i * 90);
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.1 }
  );

  document.querySelectorAll('.fade-up').forEach((el) => observer.observe(el));
})();
