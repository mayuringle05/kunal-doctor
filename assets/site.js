(function () {
  const toggle = document.querySelector('.menu-toggle');
  const mobileNav = document.querySelector('.mobile-nav');
  if (toggle && mobileNav) {
    toggle.addEventListener('click', () => {
      const opening = toggle.getAttribute('aria-expanded') !== 'true';
      toggle.setAttribute('aria-expanded', String(opening));
      toggle.setAttribute('aria-label', opening ? 'Close menu' : 'Open menu');
      mobileNav.hidden = !opening;
    });
    mobileNav.querySelectorAll('a').forEach(link => link.addEventListener('click', () => {
      mobileNav.hidden = true;
      toggle.setAttribute('aria-expanded', 'false');
      toggle.setAttribute('aria-label', 'Open menu');
    }));
    document.addEventListener('keydown', event => {
      if (event.key === 'Escape' && !mobileNav.hidden) {
        mobileNav.hidden = true;
        toggle.setAttribute('aria-expanded', 'false');
        toggle.setAttribute('aria-label', 'Open menu');
        toggle.focus();
      }
    });
  }
  const form = document.getElementById('appointment-form');
  if (form) {
    const care = new URLSearchParams(window.location.search).get('care');
    const knownCare = {
      laparoscopic: 'Laparoscopic Surgery', gi: 'GI & Hepatobiliary Surgery',
      hernia: 'Hernia & Abdominal Wall Repair', sils: 'Single-Incision Surgery',
      proctology: 'Laser Proctology', general: 'General & Emergency Surgery'
    };
    if (care && Object.prototype.hasOwnProperty.call(knownCare, care)) {
      document.getElementById('patient-concern').value = 'Enquiry about ' + knownCare[care];
    }
    form.addEventListener('submit', function (event) {
      event.preventDefault();
      const nameField = document.getElementById('patient-name');
      const phoneField = document.getElementById('patient-phone');
      const concernField = document.getElementById('patient-concern');
      const status = document.getElementById('form-status');
      const name = nameField.value.trim();
      const phone = phoneField.value.trim();
      const concern = concernField.value.trim();
      status.textContent = '';
      if (!name) { nameField.focus(); status.textContent = 'Please enter your name.'; return; }
      if (!/^[+\d() .-]{7,20}$/.test(phone) || phone.replace(/\D/g, '').length < 7) {
        phoneField.focus(); status.textContent = 'Please enter a valid contact number.'; return;
      }
      if (!concern) { concernField.focus(); status.textContent = 'Please add a brief reason for the callback.'; return; }
      const whatsappNumber = form.dataset.whatsappNumber;
      if (!/^\d{10,15}$/.test(whatsappNumber || '')) {
        status.textContent = 'The clinic contact number is unavailable.';
        return;
      }
      // Normalise line breaks so that the prefilled message cannot be used to impersonate fields.
      const clean = value => value.replace(/[\r\n\t]+/g, ' ').replace(/\s{2,}/g, ' ').trim();
      const message = `Hello, I would like to request a callback about an OPD appointment with ${form.dataset.doctorName || 'Dr. Kumbhare'}.\nName: ${clean(name)}\nPhone: ${clean(phone)}\nConcern: ${clean(concern)}\nPlease call me when convenient.`;
      const url = 'https://wa.me/' + whatsappNumber + '?text=' + encodeURIComponent(message);
      status.textContent = 'WhatsApp is opening. Please press Send there to deliver your request. The clinic has not received it yet.';
      const newTab = window.open(url, '_blank', 'noopener,noreferrer');
      if (!newTab) window.location.assign(url);
    });
  }

  if ('IntersectionObserver' in window && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    const items = document.querySelectorAll('.motion-reveal, .care-card, .timeline-item, .journey-card, .education-row, .detail-education, .related-care__link');
    if (items.length) {
      // Opt in to hidden-first motion only after we know the observer exists.
      document.documentElement.classList.add('motion-ready');
      const observer = new IntersectionObserver((entries, obs) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-revealed');
            obs.unobserve(entry.target);
          }
        });
      }, { rootMargin: '0px 0px -36px 0px', threshold: 0.06 });
      items.forEach((item, index) => {
        item.classList.add('motion-item');
        item.style.setProperty('--reveal-delay', (index % 3) * 65 + 'ms');
        observer.observe(item);
      });
    }
  }
})();
