  (function () {
    function makeStepper(opts) {
      var slides = Array.prototype.slice.call(document.querySelectorAll(opts.stageSel + ' .slide'));
      var current = 0;
      var timer = null;

      function render() {
        slides.forEach(function (s, i) {
          s.classList.toggle('active', i === current);
        });
        var buttons = document.querySelectorAll(opts.navSel + ' [data-goto]');
        buttons.forEach(function (b) {
          var isActive = Number(b.dataset.goto) === current;
          b.classList.toggle('active', isActive);
          if (isActive && b.scrollIntoView) {
            b.scrollIntoView({ behavior: 'smooth', inline: 'nearest', block: 'nearest' });
          }
        });
      }

      function goto(i) {
        current = (i + slides.length) % slides.length;
        render();
      }

      function next() { goto(current + 1); }
      function prev() { goto(current - 1); }

      function resetAuto() {
        if (!opts.autoplay) return;
        if (timer) clearInterval(timer);
        timer = setInterval(next, opts.interval || 7000);
      }

      var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      if (!reduceMotion) resetAuto();

      return { goto: goto, next: next, prev: prev, resetAuto: resetAuto };
    }

    // ---- FIELD STEPPER ----
    var fieldLabels = ['IT Produkte', 'IT Services', 'Business Services', 'Last Mile Services'];
    var fieldDots = document.getElementById('fieldDots');
    fieldLabels.forEach(function (label, i) {
      var b = document.createElement('button');
      b.className = 'dot' + (i === 0 ? ' active' : '');
      b.type = 'button';
      b.textContent = label;
      b.dataset.goto = i;
      b.setAttribute('role', 'tab');
      b.setAttribute('aria-label', label);
      fieldDots.appendChild(b);
    });

    var fieldStepper = makeStepper({
      stageSel: '#fieldStage',
      navSel: '#fieldDots',
      autoplay: false
    });

    fieldDots.addEventListener('click', function (e) {
      var btn = e.target.closest('[data-goto]');
      if (!btn) return;
      fieldStepper.goto(Number(btn.dataset.goto));
    });
    document.getElementById('fieldNext').addEventListener('click', function () {
      fieldStepper.next();
    });
    document.getElementById('fieldPrev').addEventListener('click', function () {
      fieldStepper.prev();
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight') { fieldStepper.next(); }
      if (e.key === 'ArrowLeft') { fieldStepper.prev(); }
    });

    // ---- CRITERIA TABS ----
    var critLabels = ['Grösse & Struktur', 'Charakter','Zeitraum', 'Nicht gesucht'];
    var critTabs = document.getElementById('critTabs');
    critLabels.forEach(function (label, i) {
      var b = document.createElement('button');
      b.className = 'crit-tab' + (i === 0 ? ' active' : '');
      b.type = 'button';
      b.textContent = label;
      b.dataset.goto = i;
      b.setAttribute('role', 'tab');
      critTabs.appendChild(b);
    });

    var critStepper = makeStepper({
      stageSel: '#critStage',
      navSel: '#critTabs',
      autoplay: false
    });

    critTabs.addEventListener('click', function (e) {
      var btn = e.target.closest('[data-goto]');
      if (!btn) return;
      critStepper.goto(Number(btn.dataset.goto));
    });

    // Arrow buttons for the Kriterien panel — mirrors the Felder stepper's
    // fieldPrev/fieldNext wiring above.
    document.getElementById('critNext').addEventListener('click', function () {
      critStepper.next();
    });
    document.getElementById('critPrev').addEventListener('click', function () {
      critStepper.prev();
    });
  })();
