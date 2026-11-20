/* PM Syllabus. Small, dependency-free behaviour for the /pm/ section.
   Everything here is an extra: the pages read fine with JavaScript off.
   1. Progress: ticks on the short path, saved in this browser only.
   2. Single-document view: show one unit at a time (used by the preview and the print page).
   3. The dice game.
   4. A line edit stays on its line. */
(function () {
  "use strict";
  var doc = document, body = doc.body;
  body.classList.add("js");

  /* ---- storage that never throws ---- */
  var mem = {}, ls = null;
  try { ls = window.localStorage; ls.setItem("pm:test", "1"); ls.removeItem("pm:test"); } catch (e) { ls = null; }
  function get(k) { if (ls) { try { return ls.getItem(k); } catch (e) {} } return mem[k] || null; }
  function set(k, v) { if (v === null) delete mem[k]; else mem[k] = v; if (ls) { try { if (v === null) ls.removeItem(k); else ls.setItem(k, v); } catch (e) {} } }
  function all(sel, root) { return Array.prototype.slice.call((root || doc).querySelectorAll(sel)); }

  /* ---- 1. progress ---- */
  function tally(unit) {
    if (!unit) return;
    var boxes = all("[data-step] input", unit), out = unit.querySelector("[data-progress]");
    if (!out || !boxes.length) return;
    var n = boxes.filter(function (b) { return b.checked; }).length;
    out.hidden = false;
    out.textContent = n === 0 ? boxes.length + " stops. Tick each one off as you go."
      : n === boxes.length ? "All " + n + " stops done."
      : n + " of " + boxes.length + " stops done.";
  }
  function markMap() {
    all("[data-map-unit]").forEach(function (el) {
      var unit = el.getAttribute("data-map-unit"), total = +el.getAttribute("data-map-steps") || 0;
      var ids = (el.getAttribute("data-map-ids") || "").split(" ").filter(Boolean);
      var n = ids.filter(function (id) { return get("pm:" + unit + ":" + id) === "1"; }).length;
      var out = el.querySelector("[data-map-status]");
      if (!out || !total) return;
      out.textContent = n === 0 ? "Ready. Not started." : n >= total ? "Done." : "Started: " + n + " of " + total + " stops done.";
      el.classList.toggle("is-done", n >= total);
    });
  }
  all("[data-step]").forEach(function (li) {
    var box = li.querySelector("input[type=checkbox]"); if (!box) return;
    var key = "pm:" + li.getAttribute("data-step");
    box.checked = get(key) === "1";
    box.addEventListener("change", function () { set(key, box.checked ? "1" : null); tally(li.closest("[data-unit]")); markMap(); });
  });
  all("[data-unit]").forEach(tally);
  markMap();

  /* The full path is folded on screen. Open it for printing, then put it back. */
  var reopened = [];
  window.addEventListener("beforeprint", function () {
    reopened = all(".deeper details").filter(function (d) { return !d.open; });
    reopened.forEach(function (d) { d.open = true; });
  });
  window.addEventListener("afterprint", function () { reopened.forEach(function (d) { d.open = false; }); reopened = []; });

  /* ---- glossary terms: links to the glossary that open a modal dialog in place where dialogs are supported.
     The browser keeps focus inside the dialog and returns it to the term when the dialog closes. ---- */
  if (window.HTMLDialogElement && HTMLDialogElement.prototype.showModal) {
    all("a.term[data-term]").forEach(function (a) {
      var dlg = doc.getElementById("term-" + a.getAttribute("data-term"));
      if (!dlg || !dlg.showModal) return;
      a.setAttribute("aria-haspopup", "dialog");
      a.addEventListener("click", function (e) { e.preventDefault(); dlg.showModal(); });
    });
    /* A tap on the dimmed page around the dialog closes it, as Escape and Close do. */
    all("dialog.gloss").forEach(function (dlg) {
      dlg.addEventListener("click", function (e) {
        if (e.target !== dlg) return;
        var r = dlg.getBoundingClientRect();
        if (e.clientX < r.left || e.clientX > r.right || e.clientY < r.top || e.clientY > r.bottom) dlg.close();
      });
    });
  }

  /* ---- 2. one unit at a time in the single document ---- */
  if (body.classList.contains("pm-all")) {
    var units = all(".unit");
    /* When the reader picks a unit, focus moves to its title, so keyboard and screen reader users land on what they chose. */
    var show = function (picked) {
      var id = (location.hash || "").slice(1), target = id ? doc.getElementById(id) : null;
      var unit = target ? target.closest(".unit") : null;
      if (!unit) { unit = units[0]; target = null; }
      units.forEach(function (u) { u.classList.toggle("is-current", u === unit); });
      all(".unit-nav a").forEach(function (a) {
        if (a.getAttribute("href") === "#" + unit.id) a.setAttribute("aria-current", "page"); else a.removeAttribute("aria-current");
      });
      if (target && target !== unit) target.scrollIntoView(); else window.scrollTo(0, 0);
      var title = unit.querySelector("h1");
      if (picked === true && title && !(target && target !== unit)) { title.setAttribute("tabindex", "-1"); title.focus({ preventScroll: true }); }
    };
    window.addEventListener("hashchange", function () { show(true); });
    show(false);
  }

  /* ---- 4. a line edit stays on its line (spec H2) ----
     The new words start where the pen starts, just before the old word, and run to the right. Where the old word ends
     a line, they would run past it, so they shift left to end with the line, as a writer's hand would. In print the
     CSS sets them back where they start. */
  var edits = all(".edit ins");
  function fitEdits() {
    edits.forEach(function (ins) {
      ins.style.translate = "";
      var block = ins.parentNode.closest("p, li, dd, td, blockquote") || body, cs = getComputedStyle(block);
      var r = doc.createRange(); r.selectNodeContents(ins);
      var over = r.getBoundingClientRect().right - (block.getBoundingClientRect().right - parseFloat(cs.paddingRight) - parseFloat(cs.borderRightWidth));
      if (over > 0) ins.style.translate = (-Math.ceil(over)) + "px 0";
    });
  }
  if (edits.length) {
    var fitting = false;
    var refit = function () { if (fitting) return; fitting = true; requestAnimationFrame(function () { fitting = false; fitEdits(); }); };
    fitEdits();
    if (doc.fonts && doc.fonts.ready) doc.fonts.ready.then(fitEdits);
    window.addEventListener("resize", refit);
    window.addEventListener("hashchange", refit);
  }

  /* ---- 3. the dice game ---- */
  all("[data-game]").forEach(function (game) {
    var dataEl = game.querySelector("[data-game-setups]"); if (!dataEl) return;
    var setups; try { setups = JSON.parse(dataEl.textContent); } catch (e) { return; }
    var ROUNDS = 20, current = "equal", timer = null, state, running = false;
    var el = {
      stations: all(".st", game), round: game.querySelector("[data-round]"), finished: game.querySelector("[data-finished]"),
      waiting: game.querySelector("[data-waiting]"), promise: game.querySelector("[data-promise]"), note: game.querySelector("[data-setup-note]"),
      result: game.querySelector("[data-result]"), play: game.querySelector("[data-play]"), takeaway: game.querySelector("[data-takeaway]"),
      setupButtons: all("[data-setup]", game)
    };
    var playedOnce = false;

    function fresh() { return { round: 0, out: 0, inbox: [0, 0, 0, 0, 0], roll: [null, null, null, null, null] }; }
    function waitingTotal() { return state.inbox.reduce(function (a, b) { return a + b; }, 0); }

    // One round: each station in turn rolls, then passes on what it rolled or what it has, whichever is fewer.
    function round() {
      var dice = setups[current].dice;
      for (var i = 0; i < 5; i++) {
        var lo = dice[i][0], hi = dice[i][1];
        var roll = lo + Math.floor(Math.random() * (hi - lo + 1));
        var have = i === 0 ? roll : state.inbox[i];
        var move = Math.min(roll, have);
        state.roll[i] = roll;
        if (i > 0) state.inbox[i] -= move;
        if (i < 4) state.inbox[i + 1] += move; else state.out += move;
      }
      state.round++;
    }

    function draw() {
      var dice = setups[current].dice;
      el.stations.forEach(function (st, i) {
        var n = state.inbox[i], pile = st.querySelector(".pile");
        pile.style.height = (Math.min(n, 44) * 0.15) + "rem";
        pile.classList.toggle("has", n > 0);
        st.querySelector(".pile-n").textContent = i === 0 || n === 0 ? "" : n;
        st.querySelector(".die").textContent = state.roll[i] === null ? "" : state.roll[i];
        st.querySelector(".st-range").textContent = dice[i][0] + " to " + dice[i][1];
        st.classList.toggle("is-changed", !(dice[i][0] === 1 && dice[i][1] === 6));
      });
      el.round.textContent = state.round;
      el.finished.textContent = state.out;
      el.waiting.textContent = waitingTotal();
      el.promise.textContent = setups[current].promise;
    }

    /* While a run plays, Play is marked busy rather than disabled, so it keeps keyboard and screen reader focus. */
    function busy(on) { running = on; if (on) el.play.setAttribute("aria-disabled", "true"); else el.play.removeAttribute("aria-disabled"); }

    function reset() {
      clearTimeout(timer); state = fresh(); draw(); busy(false);
      el.result.textContent = "";
      el.play.textContent = playedOnce ? "Play 20 rounds again" : "Play 20 rounds";
    }

    /* Where the work waits, in words: the board is hidden from screen readers, so the result says what it shows. */
    function wherePiled() {
      var parts = [];
      for (var i = 1; i < 5; i++) parts.push(state.inbox[i] + " at station " + (i + 1));
      return parts.slice(0, -1).join(", ") + " and " + parts[parts.length - 1];
    }

    function finish() {
      var s = setups[current], picked = game.querySelector("input[name=dice-guess]:checked"), text = "", w = waitingTotal();
      if (!playedOnce && current === "equal" && picked) text = "You guessed " + picked.value + ". ";
      text += "This run finished " + state.out + ", against the " + s.promise + " the averages promised. "
        + (w === 1 ? "1 item was" : w + " items were") + " still waiting in the line: " + wherePiled() + ". Over 400,000 simulated runs this setup averages " + s.average + ". " + s.after;
      el.result.textContent = text;
      playedOnce = true;
      busy(false); el.play.textContent = "Play 20 rounds again";
      if (el.takeaway) el.takeaway.hidden = false;
    }

    function play() {
      if (running) return;
      clearTimeout(timer); state = fresh(); draw(); el.result.textContent = ""; busy(true);
      var still = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
      if (still) { while (state.round < ROUNDS) round(); draw(); finish(); return; }
      (function tick() { round(); draw(); if (state.round < ROUNDS) timer = setTimeout(tick, 180); else finish(); })();
    }

    el.setupButtons.forEach(function (b) {
      b.addEventListener("click", function () {
        current = b.getAttribute("data-setup");
        el.setupButtons.forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
        el.note.textContent = setups[current].note;
        reset();
      });
    });
    el.play.addEventListener("click", play);

    game.classList.add("is-live");
    if (el.takeaway) el.takeaway.hidden = true;
    reset();
  });
})();
