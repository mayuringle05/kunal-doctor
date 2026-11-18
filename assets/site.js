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
    form.addEventListener('submit', function (event) {
      event.preventDefault();
      const nameField = document.getElementById('patient-name');
      const phoneField = document.getElementById('patient-phone');
      const visitField = document.getElementById('visit-type');
      const status = document.getElementById('form-status');
      const name = nameField.value.trim();
      const phone = phoneField.value.trim();
      if (!name) { nameField.focus(); status.textContent = 'Please enter your name.'; return; }
      if (!/^[+\d() .-]{7,20}$/.test(phone) || phone.replace(/\D/g, '').length < 7) {
        phoneField.focus(); status.textContent = 'Please enter a valid contact number.'; return;
      }
      const doctor = form.dataset.doctorName || 'Doctor';
      const whatsappNumber = form.dataset.whatsappNumber;
      if (!/^\d{10,15}$/.test(whatsappNumber || '')) {
        status.textContent = 'Appointment contact has not been configured.';
        return;
      }
      const message = `Hello ${doctor}, I would like to enquire about an OPD appointment.\nName: ${name}\nContact: ${phone}\nCategory: ${visitField.value}\nPlease confirm the available day and clinic address.`;
      const url = 'https://wa.me/' + whatsappNumber + '?text=' + encodeURIComponent(message);
      status.textContent = 'Opening WhatsApp to send your appointment enquiry. No appointment is confirmed yet.';
      const newTab = window.open(url, '_blank', 'noopener,noreferrer');
      if (!newTab) window.location.assign(url);
    });
  }
  if ('IntersectionObserver' in window && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    const items = document.querySelectorAll('.care-card, .timeline-item, .journey-card, .education-row');
    const observer = new IntersectionObserver((entries, obs) => {
      for (const entry of entries) {
        if (entry.isIntersecting) { entry.target.classList.add('is-revealed'); obs.unobserve(entry.target); }
      }
    }, { threshold: .08 });
    items.forEach(item => { item.classList.add('will-reveal'); observer.observe(item); });
  }
})();
