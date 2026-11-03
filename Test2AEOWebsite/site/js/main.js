(function () {
  document.documentElement.classList.remove('no-js');

  // Mobile nav
  var toggle = document.querySelector('.nav-toggle');
  var links = document.getElementById('nav-links');
  if (toggle && links) {
    toggle.addEventListener('click', function () {
      var open = links.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  // Reveal on scroll
  var items = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px' });
    items.forEach(function (el) { io.observe(el); });
  } else {
    items.forEach(function (el) { el.classList.add('in'); });
  }

  // Footer year
  var y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();

  // Enquiry form
  var form = document.getElementById('enquiry-form');
  if (!form) return;
  var status = document.getElementById('form-status');
  var rules = {
    name: function (v) { return v.trim().length >= 2; },
    company: function (v) { return v.trim().length >= 2; },
    email: function (v) { return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v.trim()); },
    phone: function (v) { return /^[+()\d\s-]{7,20}$/.test(v.trim()); },
    message: function (v) { return v.trim().length >= 20; }
  };

  function check(input) {
    var fn = rules[input.name];
    if (!fn) return true;
    var ok = fn(input.value);
    input.closest('.field').classList.toggle('invalid', !ok);
    input.setAttribute('aria-invalid', ok ? 'false' : 'true');
    return ok;
  }

  form.addEventListener('blur', function (e) {
    if (e.target.name && rules[e.target.name]) check(e.target);
  }, true);

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    status.className = 'form-status';
    status.textContent = '';
    if (form.elements._gotcha && form.elements._gotcha.value) return;

    var valid = true, first = null;
    Object.keys(rules).forEach(function (k) {
      var el = form.elements[k];
      if (el && !check(el)) { valid = false; if (!first) first = el; }
    });
    if (!valid) { first.focus(); return; }

    // TODO(client): the endpoint is not connected yet. Create a free form at
    // https://formspree.io, then replace FORM_ID in the form's action attribute
    // in contact/index.html with your form ID.
    if (form.action.indexOf('FORM_ID') !== -1) {
      status.className = 'form-status fail';
      status.textContent = 'The enquiry form is not connected yet, so your message was not sent. Please try again later.';
      return;
    }

    var btn = form.querySelector('button[type="submit"]');
    btn.disabled = true;
    btn.textContent = 'Sending...';
    fetch(form.action, {
      method: 'POST',
      body: new FormData(form),
      headers: { Accept: 'application/json' }
    }).then(function (r) {
      if (!r.ok) throw new Error('bad status');
      form.reset();
      status.className = 'form-status ok';
      status.textContent = 'Thank you. Your request reached the Arnish AI team, and we will reply to the email address you gave us.';
    }).catch(function () {
      status.className = 'form-status fail';
      status.textContent = 'Your message could not be sent. Please check your connection and try again.';
    }).then(function () {
      btn.disabled = false;
      btn.textContent = 'Book a Free Consultation';
    });
  });
})();
