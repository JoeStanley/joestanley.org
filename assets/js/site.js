/* joestanley.org: the site's menu on a phone (spec R9). Every page loads this; the syllabus adds pm.js.
   Without it, every section shows in the header, wrapping where it must. With it, below 46rem, the header shows the
   current section and a Menu button, which opens every section in a list under the header. The list stays open
   until the button is pressed again, Escape (focus goes back to the button), a tap or click outside the menu, the
   course bar's included, focus leaving it, or the page scrolling. A scroll leaves it open while focus is inside it,
   or when it ran past the window's foot as it opened, so a reader tabbing through it or reading large text never
   loses it. */
(function () {
  "use strict";
  var doc = document;
  Array.prototype.forEach.call(doc.querySelectorAll("[data-site-nav]"), function (nav) {
    var btn = nav.querySelector(".nav-open"), list = nav.querySelector(".nav-list");
    if (!btn || !list) return;
    var from = 0, tall = false;
    function isOpen() { return btn.getAttribute("aria-expanded") === "true"; }
    function open(on, refocus) {
      btn.setAttribute("aria-expanded", on ? "true" : "false");
      list.classList.toggle("is-open", on);
      /* A list that runs past the window's foot when it opens needs the page scrolled to reach it all. */
      if (on) { from = window.scrollY; tall = list.getBoundingClientRect().bottom > window.innerHeight; }
      if (!on && refocus) btn.focus();
    }
    btn.addEventListener("click", function () { open(!isOpen()); });
    nav.addEventListener("keydown", function (e) {
      if ((e.key === "Escape" || e.key === "Esc") && isOpen()) { e.preventDefault(); open(false, true); }
    });
    doc.addEventListener("click", function (e) { if (isOpen() && !nav.contains(e.target)) open(false); });
    nav.addEventListener("focusout", function (e) { if (isOpen() && e.relatedTarget && !nav.contains(e.relatedTarget)) open(false); });
    window.addEventListener("scroll", function () {
      if (!isOpen() || (nav.contains(doc.activeElement) && doc.activeElement !== btn)) return;
      if (tall) return;
      if (Math.abs(window.scrollY - from) > 8) open(false);
    }, { passive: true });
    /* A wide screen shows every section on the line, so a list left open there would stand in for nothing. */
    var wide = window.matchMedia("(min-width: 46rem)");
    function onWide() { if (wide.matches && isOpen()) open(false); }
    if (wide.addEventListener) wide.addEventListener("change", onWide); else if (wide.addListener) wide.addListener(onWide);
    btn.hidden = false;
    nav.classList.add("has-menu");
  });
})();
