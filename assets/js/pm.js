/* PM Syllabus. Small, dependency-free behaviour for the /pm/ section.
   Everything here is an extra: the pages read fine with JavaScript off.
   1. Progress: ticks on the short path, saved in this browser only.
   2. Single-document view: show one unit at a time (used by the preview and the print page).
   3. The games: the dice game, the waiting game and the ranking game.
   4. A line edit stays on its line.
   5. The Compass's two walks: two buttons pick which version of the call shows.
   6. The course bar: its place opens the list of modules, with saved progress.
   A finished game round ticks its step, and "Go deeper" opens the full path (G7). */
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
    out.textContent = n === 0 ? boxes.length + " steps. Tap a step's number to tick it off."
      : n === boxes.length ? "All " + n + " steps done."
      : n + " of " + boxes.length + " steps done.";
  }
  function markMap() {
    all("[data-map-unit]").forEach(function (el) {
      var unit = el.getAttribute("data-map-unit"), total = +el.getAttribute("data-map-steps") || 0;
      var ids = (el.getAttribute("data-map-ids") || "").split(" ").filter(Boolean);
      var n = ids.filter(function (id) { return get("pm:" + unit + ":" + id) === "1"; }).length;
      var out = el.querySelector("[data-map-status]");
      if (!out || !total) return;
      /* The course bar's list says it in a few words (G1): nothing until a step is ticked. */
      if (el.hasAttribute("data-map-short")) out.textContent = n === 0 ? "" : n >= total ? "Done" : n + " of " + total + " steps";
      /* Start's list, right after the module's title (S20): nothing until a step is ticked, then the count, then Done. */
      else out.textContent = n === 0 ? "" : n >= total ? "Done" : n + " of " + total + " steps done";
      el.classList.toggle("is-done", n >= total);
    });
  }
  all("[data-step]").forEach(function (li) {
    var box = li.querySelector("input[type=checkbox]"); if (!box) return;
    var key = "pm:" + li.getAttribute("data-step");
    box.checked = get(key) === "1";
    box.addEventListener("change", function () { set(key, box.checked ? "1" : null); tally(li.closest("[data-unit]")); markMap(); onward(); });
  });
  all("[data-unit]").forEach(tally);
  markMap();

  /* A game's way back goes to the first step still waiting after the game's own, coming round to the top if none
     after it waits: "Next: Do" or "Next: Check" when that's the Do or the Check, straight to it, or else "Back to the
     short path" to that step. With every step ticked, or without this script, it goes to the game's own step (G7). */
  function onward() {
    all("[data-back-from]").forEach(function (a) {
      var unit = a.closest("[data-unit]") || doc, own = a.getAttribute("data-own") || a.getAttribute("href");
      var steps = all("li[data-step]", unit), to = null, at = steps.findIndex(function (li) { return "#" + li.id === own; });
      steps.slice(at + 1).concat(steps.slice(0, at + 1)).some(function (li) {
        var b = li.querySelector("input[type=checkbox]"); if (b && !b.checked) { to = li; return true; } return false;
      });
      var link = to ? to.querySelector("h3 a") : null, down = link && /^#(do|check)$/.test(link.getAttribute("href"));
      if (!a.hasAttribute("data-own")) a.setAttribute("data-own", own);
      a.setAttribute("href", down ? link.getAttribute("href") : to ? "#" + to.id : own);
      a.textContent = down ? "Next: " + (link.getAttribute("href") === "#do" ? "Do" : "Check") : "Back to the short path";
    });
  }
  onward();

  /* The full path is folded on screen. Open it for printing, then put it back. */
  var reopened = [];
  window.addEventListener("beforeprint", function () {
    reopened = all(".deeper details").filter(function (d) { return !d.open; });
    reopened.forEach(function (d) { d.open = true; });
  });
  window.addEventListener("afterprint", function () { reopened.forEach(function (d) { d.open = false; }); reopened = []; });
  /* "Go deeper", in a module's line of links, opens the full path it lands on, as arriving at its address does (G7). */
  function openDeeper() { var d = doc.querySelector(".deeper details"); if (d) d.open = true; }
  all("[data-open-deeper]").forEach(function (a) { a.addEventListener("click", openDeeper); });
  function deeperByHash() { if (location.hash === "#go-deeper") openDeeper(); }
  /* A term reached from the glossary's "Used in" (spec G6) may sit in a fold, such as a source's reasons or the full
     path: open each fold around it, so the reader lands on the term itself. */
  function foldsByHash() {
    var t = location.hash.indexOf("#use-") === 0 ? doc.getElementById(location.hash.slice(1)) : null;
    for (var d = t ? t.closest("details") : null; d; d = d.parentElement && d.parentElement.closest("details")) d.open = true;
    if (t && t.closest("details")) t.scrollIntoView();
  }
  window.addEventListener("hashchange", function () { deeperByHash(); foldsByHash(); });
  deeperByHash(); foldsByHash();

  /* The glossary's A to Z rail (spec G6): a drag along it jumps to the letter under the finger or pointer, as a
     phone's contacts do, or to the nearest letter with terms where that one has none. A tap follows the link. */
  all("[data-az]").forEach(function (rail) {
    var items = all("li", rail), last = null, down = false; // down: the pointer pressed on the rail, or false
    /* Where the screen is too short for 26 letters at the reader's text size (36 root ems, as the short-screen rule in
       pm.css says), the rail lies flat. Checked again whenever the rail's size changes, as it does when the reader
       sets their text larger. */
    function fit() {
      var unit = rail.closest(".glossary"), rem = parseFloat(getComputedStyle(doc.documentElement).fontSize) || 16;
      var flat = window.innerHeight / rem < 36;
      if (rail.classList.contains("az-flat") !== flat) { rail.classList.toggle("az-flat", flat); if (unit) unit.classList.toggle("has-flat-az", flat); }
    }
    fit(); window.addEventListener("resize", fit);
    if (window.ResizeObserver) new ResizeObserver(fit).observe(rail);
    function jump(y) {
      var i = -1;
      items.forEach(function (li, k) { var r = li.getBoundingClientRect(); if (y >= r.top && y < r.bottom) i = k; });
      if (i < 0) return;
      for (var d = 0; d < items.length; d++) {
        var a = (items[i + d] || {}).querySelector ? items[i + d].querySelector("a") : null;
        if (!a && items[i - d]) a = items[i - d].querySelector("a");
        if (a) {
          if (a !== last) { last = a; var t = doc.getElementById(a.getAttribute("href").slice(1)); if (t) t.scrollIntoView({ block: "start" }); choose(a); }
          return;
        }
      }
    }
    rail.addEventListener("pointerdown", function (e) {
      if (getComputedStyle(rail).position === "static") return;
      down = e.pointerId; last = null;
    });
    // Captured only once the finger moves, so a plain tap still follows its letter's link.
    rail.addEventListener("pointermove", function (e) {
      if (down === false || down !== e.pointerId) return;
      if (rail.setPointerCapture && !rail.hasPointerCapture(e.pointerId)) rail.setPointerCapture(e.pointerId);
      e.preventDefault(); jump(e.clientY);
    });
    // The letter whose terms are under the bar turns orange on the rail as the list scrolls: where the reader is.
    var marks = items.map(function (li) { return li.querySelector("a"); }).filter(Boolean)
      .map(function (a) { return [a, doc.getElementById(a.getAttribute("href").slice(1))]; }), ticking = false;
    /* A letter tapped or dragged to stays marked until the reader scrolls on, even where the page ends before its
       heading can reach the top. */
    var chosen = null, at = 0;
    function choose(a) { chosen = a; at = window.scrollY; here(); }
    rail.addEventListener("click", function (e) {
      var a = e.target.closest && e.target.closest("a"); if (a) setTimeout(function () { choose(a); }, 60);
    });
    function here() {
      if (chosen && Math.abs(window.scrollY - at) < 24) { marks.forEach(function (m) { m[0].classList.toggle("is-here", m[0] === chosen); }); return; }
      chosen = null;
      // The group that fills the line just under the bar: the first whose end is below it, once the list has begun.
      var bar = doc.querySelector("[data-course-bar]"), y = (bar ? bar.getBoundingClientRect().bottom : 0) + 1, cur = null;
      for (var i = 0; i < marks.length; i++) {
        var r = marks[i][1] && marks[i][1].getBoundingClientRect();
        if (r && r.bottom > y) { if (r.top <= y + 48 || i > 0) cur = marks[i][0]; break; }
      }
      marks.forEach(function (m) { m[0].classList.toggle("is-here", m[0] === cur); });
    }
    window.addEventListener("scroll", function () { if (!ticking) { ticking = true; requestAnimationFrame(function () { ticking = false; here(); }); } }, { passive: true });
    here();
    rail.addEventListener("dragstart", function (e) { e.preventDefault(); });
    rail.addEventListener("pointerup", function () { down = false; });
    rail.addEventListener("pointercancel", function () { down = false; });
  });

  /* What a good one looks like waits for the reader's own try (J7). Where the Do is a step of the short path, opening
     the example before that step is ticked shows a message and a button that ticks it; once it's ticked, by the button
     or on the short path, the example. Without this script the line opens the example. */
  all("details.example[data-gate]").forEach(function (det) {
    var gate = det.querySelector("[data-example-gate]"), body = det.querySelector(".example-body");
    var li = (det.closest("[data-unit]") || doc).querySelector('[data-step="' + det.getAttribute("data-gate") + '"]');
    var box = li ? li.querySelector("input[type=checkbox]") : null, btn = gate ? gate.querySelector("[data-example-ungate]") : null;
    if (!body || !box || !btn) return;
    function show() { gate.hidden = box.checked; body.hidden = !box.checked; }
    show();
    box.addEventListener("change", show);
    btn.addEventListener("click", function () {
      if (!box.checked) { box.checked = true; box.dispatchEvent(new Event("change")); }
      show(); body.focus();
    });
  });

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

  /* ---- 3. the games (spec J5): the dice game, the waiting game and the ranking game ---- */
  var still = function () { return !!(window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches); };
  var money = function (n) { return "$" + Math.round(n).toLocaleString("en-US"); };
  /* While a run plays, Play is marked busy rather than disabled, so it keeps keyboard and screen reader focus. */
  var busyOn = function (btn, on) { if (on) btn.setAttribute("aria-disabled", "true"); else btn.removeAttribute("aria-disabled"); };

  /* A finished round ticks the game's own step on the short path, as ticking it by hand would, and says so beside
     the way back, so a reader landing on the step doesn't untick it by tapping it again (spec G7). */
  function played(game) {
    var a = game.id ? doc.querySelector('[data-step] h3 a[href="#' + game.id + '"]') : null;
    var box = a ? a.closest("[data-step]").querySelector("input[type=checkbox]") : null;
    if (!box) return;
    if (!box.checked) { box.checked = true; box.dispatchEvent(new Event("change")); }
    var back = doc.querySelector('[data-back-from="' + game.id + '"]'), said = back ? back.parentNode.querySelector("[data-ticked]") : null;
    if (said) said.textContent = "Its step on the short path is ticked.";
  }

  /* Playing a game (spec J8): the board brought into view under the bar when a run starts, at once with reduced
     motion; a row for each run in "Your runs"; and the takeaway held until the setups are played. */
  function toBoard(game) {
    var b = game.querySelector(".board"); if (!b) return;
    var bar = doc.querySelector("[data-course-bar]"), top = bar ? bar.getBoundingClientRect().bottom : 0, r = b.getBoundingClientRect();
    if (r.top >= top - 1 && r.top <= top + 24) return;
    b.scrollIntoView({ block: "start", behavior: still() ? "auto" : "smooth" });
  }
  function addRun(game, cells) {
    var t = game.querySelector("[data-runs]"); if (!t) return;
    var tr = doc.createElement("tr");
    cells.forEach(function (c, i) { var td = doc.createElement(i ? "td" : "th"); if (!i) td.setAttribute("scope", "row"); td.textContent = c; tr.appendChild(td); });
    var body = t.querySelector("tbody"); body.appendChild(tr);
    while (body.children.length > 12) body.removeChild(body.firstChild);
    t.hidden = false;
  }
  function holdTakeaway(game, open) {
    var t = game.querySelector("[data-takeaway]"), h = game.querySelector("[data-takeaway-hold]");
    if (t) t.hidden = !open;
    if (h) h.hidden = !!open;
  }

  function diceGame(game) {
    var dataEl = game.querySelector("[data-game-setups]"); if (!dataEl) return;
    var setups; try { setups = JSON.parse(dataEl.textContent); } catch (e) { return; }
    var ROUNDS = 20, current = "equal", timer = null, state, running = false, runs = 0, seen = {};
    var el = {
      stations: all(".st", game), round: game.querySelector("[data-round]"), finished: game.querySelector("[data-finished]"),
      waiting: game.querySelector("[data-waiting]"), promise: game.querySelector("[data-promise]"), note: game.querySelector("[data-setup-note]"),
      result: game.querySelector("[data-result]"), play: game.querySelector("[data-play]"),
      setupButtons: all("[data-setup]", game), move: game.querySelector("[data-next-move]"), next: game.querySelector("[data-next]"), done: game.querySelector("[data-next-done]")
    };
    var keys = el.setupButtons.map(function (b) { return b.getAttribute("data-setup"); });
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
      el.result.textContent = ""; el.move.hidden = true;
      el.play.textContent = playedOnce ? "Play 20 rounds again" : "Play 20 rounds";
    }

    /* Where the work waits, in words: the board is hidden from screen readers, so the result says what it shows. */
    function wherePiled() {
      var parts = [];
      for (var i = 1; i < 5; i++) parts.push(state.inbox[i] + " at station " + (i + 1));
      return parts.slice(0, -1).join(", ") + " and " + parts[parts.length - 1];
    }

    /* The result leads with what finished against the promise, answers the guess with the long run, then the lesson,
       and ends with where the work waits (J8, A8). */
    function finish() {
      var s = setups[current], picked = game.querySelector("input[name=dice-guess]:checked"), i = keys.indexOf(current);
      var text = "Finished " + state.out + " of the " + s.promise + " the averages promised. ";
      text += (!playedOnce && picked ? "You guessed " + picked.value + "; over" : "Over") + " 400,000 runs this line finishes " + s.average + " on average. ";
      text += s.after + " Left waiting: " + wherePiled() + ".";
      el.result.textContent = text;
      playedOnce = true; runs++; seen[current] = true;
      busy(false); el.play.textContent = "Play 20 rounds again";
      addRun(game, [(i + 1) + ". " + s.label, String(state.out), String(s.promise), String(waitingTotal()), String(s.average)]);
      var nk = keys[i + 1];
      el.move.hidden = false; el.next.hidden = !nk; el.done.hidden = !!nk;
      if (nk) el.next.textContent = "Next: " + (i + 2) + ". " + setups[nk].label;
      holdTakeaway(game, seen[keys[keys.length - 1]] || runs >= 3);
      played(game);
    }

    function play() {
      if (running) return;
      clearTimeout(timer); state = fresh(); draw(); el.result.textContent = ""; el.move.hidden = true; busy(true); toBoard(game);
      if (still()) { while (state.round < ROUNDS) round(); draw(); finish(); return; }
      (function tick() { round(); draw(); if (state.round < ROUNDS) timer = setTimeout(tick, 180); else finish(); })();
    }

    function choose(k) {
      current = k;
      el.setupButtons.forEach(function (x) { x.setAttribute("aria-pressed", x.getAttribute("data-setup") === k ? "true" : "false"); });
      el.note.textContent = setups[current].note;
      reset();
    }
    el.setupButtons.forEach(function (b) { b.addEventListener("click", function () { choose(b.getAttribute("data-setup")); }); });
    el.play.addEventListener("click", play);
    // Next picks the next line and plays it. Focus moves to Play first, which keeps it while the run plays (A9).
    el.next.addEventListener("click", function () {
      var nk = keys[keys.indexOf(current) + 1]; if (!nk || running) return;
      el.play.focus(); choose(nk); play();
    });

    game.classList.add("is-live");
    holdTakeaway(game, false);
    reset();
  }

  /* The waiting game: three jobs built one at a time. Each week a job isn't live costs what it's really worth, the
     weeks it's being built included. What each is worth is drawn fresh for every run: the reader sees only estimates,
     and may test one while the team builds. Its answer comes in at the end of week test_weeks. The reader's own call
     comes first, with nothing chosen: the guess is what the first run tests. A pick that isn't made yet is asked for
     when the team needs it, where the run stops, and the four plans follow the first run (spec J8). */
  function waitingGame(game) {
    var dataEl = game.querySelector("[data-game-setups]"); if (!dataEl) return;
    var d; try { d = JSON.parse(dataEl.textContent); } catch (e) { return; }
    var jobs = d.jobs, T = d.test_weeks, by = {}, places = ["1st", "2nd", "3rd"];
    jobs.forEach(function (j) { by[j.id] = j; });
    var el = {
      radios: all("input[name=waiting-guess]", game), legend: game.querySelector("[data-test-legend]"),
      picks: all("[data-pick]", game), rules: all("[data-setup]", game), note: game.querySelector("[data-setup-note]"), plans: game.querySelector("[data-plans]"),
      report: game.querySelector("[data-report]"), week: game.querySelector("[data-week]"), live: game.querySelector("[data-live]"), cost: game.querySelector("[data-cost]"),
      play: game.querySelector("[data-play]"), status: game.querySelector("[data-play-status]"), pause: game.querySelector("[data-pause]"), pauseList: game.querySelector("[data-pause-list]"),
      result: game.querySelector("[data-result]"), rows: {}, names: {}
    };
    all("[data-row]", game).forEach(function (r) { var k = r.getAttribute("data-row"); el.rows[k] = all(".wk", r); el.names[k] = r.querySelector(".wk-name"); });
    var rule = "", test = "none", order = [];
    var wk = 0, worth = null, outcome = null, started = false, paused = false, running = false, timer = null, playedOnce = false, pickedAt = [], ownDone = false, planDone = false;

    function start() { return test === "all" ? T : 0; }
    function complete() { return order.length === jobs.length; }
    function fill() { jobs.forEach(function (j) { if (order.indexOf(j.id) < 0) order.push(j.id); }); }
    function rest() { return jobs.filter(function (j) { return order.indexOf(j.id) < 0; }).map(function (j) { return j.id; }); }
    /* When each picked job starts and goes live. */
    function plan() {
      var t = start(), out = {};
      order.forEach(function (id) { out[id] = { start: t, live: t + by[id].weeks }; t += by[id].weeks; });
      return out;
    }
    function due() { return order.reduce(function (t, id) { return t + by[id].weeks; }, start()); }
    function estimate(id) { return by[id].estimate; }
    function costTo(w) {
      var p = plan();
      return jobs.reduce(function (c, j) { return c + worth[j.id] * Math.min(w, p[j.id] ? p[j.id].live : w); }, 0);
    }
    /* The cheapest order for the jobs not yet picked, by what's known: answers that are in, estimates for the rest. */
    function bestRest(known) {
      var left = rest(), best = null, bestCost = Infinity;
      (function perm(done, todo) {
        if (!todo.length) {
          var t = due(), c = 0;
          done.forEach(function (id) { t += by[id].weeks; c += known(id) * t; });
          if (c < bestCost) { bestCost = c; best = done; }
          return;
        }
        todo.forEach(function (id, i) { perm(done.concat([id]), todo.slice(0, i).concat(todo.slice(i + 1))); });
      })([], left);
      return best || [];
    }
    function draw() {
      var p = plan();
      el.rows.test.forEach(function (cell, i) { cell.className = "wk" + (started && test !== "none" && i < Math.min(wk, T) ? " is-build" : ""); });
      el.names.test.textContent = test === "none" ? "Test" : "Test, answer" + (test === "all" ? "s" : "") + " at the end of week " + T;
      jobs.forEach(function (j) {
        var q = p[j.id];
        el.rows[j.id].forEach(function (cell, i) {
          var w = i + 1, s = "";
          if (started && w <= wk) s = !q || w <= q.start ? " is-wait" : w <= q.live ? " is-build" : " is-live";
          cell.className = "wk" + s;
        });
        el.names[j.id].textContent = j.tag + (started && q && q.live <= wk ? ", live after week " + q.live : "");
      });
      el.week.textContent = wk;
      el.live.textContent = started ? order.filter(function (id) { return p[id].live <= wk; }).length : 0;
      el.cost.textContent = money(started ? costTo(wk) : 0);
    }
    function said(ids) { return ids.map(function (id) { return by[id].short; }).join(", then "); }
    function cap(t) { return t.charAt(0).toUpperCase() + t.slice(1); }
    function showState() {
      // A plan sets the test group to its test; otherwise it shows the reader's own choice, nothing on landing.
      if (rule) el.radios.forEach(function (r) { r.checked = r.value === test; });
      el.picks.forEach(function (b) {
        var i = order.indexOf(b.getAttribute("data-pick"));
        b.setAttribute("aria-pressed", i >= 0 ? "true" : "false");
        b.querySelector("[data-place]").textContent = i >= 0 ? places[i] : "";
      });
      el.rules.forEach(function (b) { b.setAttribute("aria-pressed", b.getAttribute("data-setup") === rule ? "true" : "false"); });
      if (rule) {
        el.note.textContent = d.rules[rule].label + ". " + (rule === "stop" ? "The team waits for all three answers, then builds the cheapest order."
          : rule === "test" ? "First " + by[order[0]].short + ", then the next pick, made on the test's answer." : cap(said(order)) + ".");
        el.status.textContent = "";
      } else {
        el.status.textContent = paused || !order.length ? "" : complete() ? "Your order: " + said(order) + "."
          : "First, " + by[order[0]].short + ". Pick the second now, or play: the run stops when the team needs it.";
      }
    }
    function reset() {
      clearTimeout(timer); wk = 0; started = false; paused = false; running = false; worth = null; pickedAt = [];
      busyOn(el.play, false); el.result.textContent = ""; el.report.textContent = ""; el.pause.hidden = true; el.play.hidden = false;
      showState(); draw();
      el.play.textContent = playedOnce ? "Play again" : "Play";
    }
    function draws() {
      worth = {}; outcome = null;
      jobs.forEach(function (j) {
        if (j.values) worth[j.id] = j.values[Math.floor(Math.random() * j.values.length)];
        else { outcome = j.outcomes[Math.floor(Math.random() * j.outcomes.length)]; worth[j.id] = outcome.value; }
      });
    }
    function bet() { return jobs.filter(function (j) { return !j.values; })[0]; }
    /* The week's report: the week, the job that just went live where the run stops, and the test's answer once it's in. */
    function report() {
      var p = plan(), text = "Week " + wk + ".", now = order.filter(function (id) { return p[id].live === wk; });
      if (now.length) text += " " + cap(by[now[0]].short) + " is live.";
      if (test !== "none" && wk >= T) {
        var ids = test === "all" ? jobs.map(function (j) { return j.id; }) : [test];
        text += (test === "all" ? " All three answers are in. " : " The test's answer is in. ") + ids.map(function (id) {
          var j = by[id], line = j.values ? j.report : outcome.report;
          return line.replace("{value}", money(worth[id]));
        }).join(" ");
      }
      el.report.textContent = text;
    }
    function known(id) { return test === "all" || id === test ? (wk >= T ? worth[id] : estimate(id)) : estimate(id); }
    function ideal() {
      var keep = order, keepTest = test; order = []; test = "none";
      order = bestRest(function (id) { return worth[id]; }); var c = costTo(Infinity);
      order = keep; test = keepTest; return c;
    }
    /* The result leads with what the order cost above the cheapest for these numbers, then the facts, then the lesson. */
    function finish() {
      var p = plan(), total = costTo(wk), best = d.best, text = "", b = bet(), low = ideal(), guess = game.querySelector("input[name=waiting-guess]:checked");
      text += total === low ? "No order could have done better with these numbers. "
        : (rule ? "This plan" : "Your order") + " cost " + money(total - low) + " more than the cheapest order for these numbers. ";
      if (!playedOnce) text += guess && guess.value !== "none" ? "You guessed " + by[guess.value].short + ", and your run tested it. " : "You guessed none of them, so your run tested nothing. ";
      var others = jobs.filter(function (j) { return j.values; });
      text += b.tag + " " + outcome.said + ": it was worth " + money(worth[b.id]) + " a week. "
        + others.map(function (j, i) { return (i === 0 ? cap(by[j.id].short) + " was worth " : by[j.id].short + " ") + money(worth[j.id]) + (i === 0 ? " a week" : ""); }).join(" and ") + ". ";
      var when = order.map(function (id) { return by[id].short + " after week " + p[id].live; });
      text += "Live: " + when.slice(0, -1).join(", ") + " and " + when[when.length - 1] + ". Cost of delay: " + money(total) + ". ";
      if (rule) text += d.rules[rule].after + " Over both outcomes this plan averages " + money(d.rules[rule].average) + (d.rules[rule].average === best.average ? ", as little as knowing everything would." : ".");
      else if (test === "none") text += "Nothing was tested, so every pick rested on the estimates.";
      else if (by[test].values) text += "Testing " + by[test].short + " told you little the estimate hadn't: no answer inside its range could change the order.";
      else if (order[0] === test) text += "The test's answer came in while " + by[test].short + " was already being built, too late for the pick it could have changed.";
      else if (pickedAt[1] >= T) text += "The test's answer was in by the time the team needed the next pick, so the pick could use it.";
      else text += "The test's answer came in at week " + T + ", but you had picked the order before it did.";
      el.result.textContent = text.trim();
      addRun(game, [test === "none" ? "None" : test === "all" ? "All three" : by[test].brief, order.map(function (id) { return by[id].brief; }).join(", "), cap(outcome.said), money(total), money(total - low)]);
      if (rule) planDone = true; else ownDone = true;
      if (!playedOnce) { el.plans.hidden = false; if (el.legend) el.legend.textContent = "1. What to test while the team builds."; }
      playedOnce = true; running = false; paused = false; busyOn(el.play, false);
      el.play.textContent = "Play again";
      holdTakeaway(game, ownDone && planDone);
      played(game);
    }
    /* Where the run stops for a pick: the question and a button for each job left, in Play's place, focus on the first. */
    function askNext() {
      el.pauseList.textContent = "";
      rest().forEach(function (id) {
        var li = doc.createElement("li"), b = doc.createElement("button");
        b.type = "button"; b.className = "setup pick"; b.setAttribute("data-next-pick", id); b.textContent = by[id].name;
        b.addEventListener("click", function () {
          order.push(id); pickedAt.push(wk); if (order.length === jobs.length - 1) { fill(); pickedAt.push(wk); }
          el.pause.hidden = true; el.play.hidden = false; el.play.focus(); showState(); play();
        });
        li.appendChild(b); el.pauseList.appendChild(li);
      });
      el.pause.hidden = false;
      var first = el.pauseList.querySelector("button"); if (first) first.focus();
      el.play.hidden = true;
    }
    /* Play on until every job is live, or until the team needs a pick that no plan makes. */
    function step() {
      wk++;
      if (!complete() && due() <= wk) {
        if (rule === "stop" || rule === "test") { var o = bestRest(known); order = order.concat(o); pickedAt.push(wk); }
        else { draw(); report(); paused = true; running = false; busyOn(el.play, false); el.play.textContent = "Play on"; showState(); askNext(); return false; }
      }
      draw();
      if ((test !== "none" && wk === T) || order.some(function (id) { return plan()[id].live === wk; })) report();
      if (complete() && wk >= due()) { finish(); return false; }
      return true;
    }
    function play() {
      if (running) return;
      if (paused) { if (!complete()) return; paused = false; }
      else {
        if (!order.length && rule !== "stop") { el.status.textContent = "Pick the job to build first, in step 2."; return; }
        clearTimeout(timer); wk = 0; started = true; draws(); pickedAt = order.map(function () { return 0; });
        el.result.textContent = ""; el.report.textContent = ""; toBoard(game);
      }
      running = true; busyOn(el.play, true); showState();
      if (still()) { while (step()) {} return; }
      (function tick() { if (step()) timer = setTimeout(tick, 260); })();
    }

    el.radios.forEach(function (r) {
      r.addEventListener("change", function () {
        if (!r.checked) return;
        test = r.value;
        if (rule) order = rule === "est" || rule === "biggest" ? d.rules[rule].order.slice() : rule === "test" ? d.rules.test.order.slice() : [];
        rule = ""; reset();
      });
    });
    el.picks.forEach(function (b) {
      b.addEventListener("click", function () {
        var id = b.getAttribute("data-pick");
        if (paused) return;
        if (rule) { test = d.rules[rule].test === "all" ? "none" : d.rules[rule].test; rule = ""; order = []; }
        var fresh = complete();
        if (fresh) order = [id];
        else if (order.indexOf(id) < 0) { order.push(id); if (order.length === jobs.length - 1) fill(); }
        reset();
        if (fresh) el.status.textContent = "A new order: " + by[id].short + " first. Pick the second now, or play: the run stops when the team needs it.";
      });
    });
    el.rules.forEach(function (b) {
      b.addEventListener("click", function () { rule = b.getAttribute("data-setup"); test = d.rules[rule].test; order = d.rules[rule].order.slice(); reset(); play(); });
    });
    el.play.addEventListener("click", play);
    game.classList.add("is-live");
    holdTakeaway(game, false);
    reset();
  }

  /* The ranking game: stores of three sizes, every one late on the same share of orders, ranked each week by their
     late rate. From the first setup's second week, last week's five worst are ringed. In the next two setups one large
     store really is worse, and the funnel shows the range chance allows; the trial runs eight weeks (spec J8). */
  function rankingGame(game) {
    var dataEl = game.querySelector("[data-game-setups]"); if (!dataEl) return;
    var d; try { d = JSON.parse(dataEl.textContent); } catch (e) { return; }
    var size = [], group = [];
    d.sizes.forEach(function (g, gi) { for (var i = 0; i < g.stores; i++) { size.push(g.orders); group.push(gi); } });
    var N = size.length, worse = N - 1, TOP = 0.4, current = "equal", week = 0, playedOnce = false, seen = {};
    var rate = null, late = null, worst = [], best = [], prevWorst = null, out = [], rank = 0;
    var tr = { fix: [0, 0], rest: [0, 0] }, F = d.trial.stores, W = d.trial.weeks;
    var el = {
      dots: all(".rk-dot", game), tally: game.querySelector("[data-tally]"), key: game.querySelector("[data-key]"),
      note: game.querySelector("[data-setup-note]"), result: game.querySelector("[data-result]"), play: game.querySelector("[data-play]"),
      setupButtons: all("[data-setup]", game), move: game.querySelector("[data-next-move]"), next: game.querySelector("[data-next]"), done: game.querySelector("[data-next-done]")
    };
    var keys = el.setupButtons.map(function (b) { return b.getAttribute("data-setup"); });
    var worldWorse = function () { return current === "worse" || current === "funnel"; };
    var inTrial = function (i) { return current === "trial" && i < F; };
    var pct = function (r) { return String(Math.round(r * 1000) / 10); };
    var ordinal = function (k) { var t = k % 100; return k + (t > 10 && t < 14 ? "th" : ["th", "st", "nd", "rd"][k % 10] || "th"); };
    var word = function (k) { return ["no", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"][k] || String(k); };
    var ringed = function () { return current === "equal" && !!prevWorst; };

    // One week: every order is late with the store's chance of lateness. Ties in the ranking break at random.
    function oneWeek() {
      late = []; rate = [];
      for (var i = 0; i < N; i++) {
        var p = i === worse && worldWorse() ? d.worse_late : inTrial(i) ? d.trial.late : d.late, n = 0;
        for (var k = 0; k < size[i]; k++) if (Math.random() < p) n++;
        late.push(n); rate.push(n / size[i]);
      }
      var tie = rate.map(function () { return Math.random(); });
      var idx = rate.map(function (r, i) { return i; }).sort(function (a, b) { return rate[b] - rate[a] || tie[b] - tie[a]; });
      worst = idx.slice(0, 5); best = idx.slice(-5);
      out = [];
      for (var j = 0; j < N; j++) { var f = d.funnel[group[j]], v = rate[j] * 100; if (v < f[0] || v > f[1]) out.push(j); }
      rank = idx.indexOf(worse) + 1;
      return idx;
    }
    function byGroup(list) {
      var n = d.sizes.map(function () { return 0; });
      list.forEach(function (i) { n[group[i]]++; });
      var parts = [];
      n.forEach(function (c, gi) { if (c) parts.push(c + " " + d.sizes[gi].label.toLowerCase()); });
      return parts.length > 1 ? parts.slice(0, -1).join(", ") + " and " + parts[parts.length - 1] : "all " + d.sizes[group[list[0]]].label.toLowerCase();
    }
    function smallIn(list) { return list.filter(function (i) { return group[i] === 0; }).length; }
    function span(list) {
      var rs = list.map(function (i) { return rate[i]; }), hi = Math.max.apply(null, rs), lo = Math.min.apply(null, rs);
      return hi === lo ? pct(hi) + " percent" : pct(lo) + " to " + pct(hi) + " percent";
    }
    function pooled(g) { return g[1] ? pct(g[0] / g[1]) : "0"; }

    function draw() {
      game.classList.toggle("shows-funnel", current === "funnel" && week > 0);
      el.dots.forEach(function (dot, i) {
        var has = rate !== null;
        dot.style.setProperty("--r", has ? Math.min(rate[i], TOP) / TOP : 0);
        dot.classList.toggle("is-shown", has);
        dot.classList.toggle("is-worst", has && worst.indexOf(i) >= 0);
        dot.classList.toggle("was-worst", has && ringed() && prevWorst.indexOf(i) >= 0);
        dot.classList.toggle("is-worse", i === worse && worldWorse());
        dot.classList.toggle("is-out", has && current === "funnel" && out.indexOf(i) >= 0);
        dot.classList.toggle("is-trial", inTrial(i));
      });
      var s = d.setups[current];
      el.key.textContent = ringed() && s.key_again ? s.key_again : s.key;
      // The tally, a line of short sentences (J8).
      if (current === "trial") el.tally.textContent = "Week " + week + " of " + W + "." + (week ? " With the fix: " + pooled(tr.fix) + "%. Without: " + pooled(tr.rest) + "%." : "");
      else el.tally.textContent = "Week " + week + "." + (rate ? " Five worst: " + smallIn(worst) + " small. Five best: " + smallIn(best) + " small." + (worldWorse() ? " Worse store: " + ordinal(rank) + "." : "") : "");
    }
    function playLabel() {
      if (current === "trial") return week >= W ? "Play the trial again" : "Play week " + (week + 1) + " of " + W;
      return playedOnce && week ? "Play another week" : "Play a week";
    }
    function reset() {
      el.result.textContent = ""; el.move.hidden = true;
      prevWorst = null;
      rate = null; week = 0; tr = { fix: [0, 0], rest: [0, 0] }; draw();
      el.play.textContent = playLabel();
    }

    function play() {
      if (current === "trial" && week >= W) reset();
      var picked = game.querySelector("input[name=ranking-guess]:checked"), text = "", stay = 0;
      if (current === "equal" && rate) prevWorst = worst.slice();
      var idx = oneWeek(); week++; toBoard(game);
      if (ringed()) stay = worst.filter(function (i) { return prevWorst.indexOf(i) >= 0; }).length;
      var also = "";
      if (current === "trial") {
        var fix = [0, 0], rest = [0, 0];
        for (var t = 0; t < N; t++) if (group[t] === 0) { var g = t < F ? fix : rest; g[0] += late[t]; g[1] += size[t]; }
        tr.fix[0] += fix[0]; tr.fix[1] += fix[1]; tr.rest[0] += rest[0]; tr.rest[1] += rest[1];
        var n_ = worst.filter(function (i) { return i < F; }).length;
        text += "Week " + week + " of the trial. With the fix: " + pct(fix[0] / fix[1]) + " percent late this week" + (week > 1 ? ", " + pooled(tr.fix) + " over " + week + " weeks" : "") + ". "
          + "Without: " + pct(rest[0] / rest[1]) + " percent" + (week > 1 ? " this week, " + pooled(tr.rest) + " over " + week + " weeks" : "") + ". "
          + "Of the five worst stores, " + (n_ === 0 ? "none has" : n_ === 1 ? "one has" : word(n_) + " have") + " the fix. ";
        if (week === 1) text += "Run this trial many times, and after one week the stores with the fix look better than those without in " + d.averages.trial_better_one + " runs in 100, and worse in " + d.averages.trial_worse_one + ". ";
        if (week >= W) text += d.setups.trial.after + " After eight weeks, the stores with the fix look better in " + d.averages.trial_better_eight + " trials in 100.";
        also = "Fix " + pooled(tr.fix) + "%, without " + pooled(tr.rest) + "%";
      } else {
        if (ringed()) text += "Of last week's five worst, " + (stay === 0 ? "none is" : stay === 1 ? "1 is" : stay + " are") + " among the five worst again. ";
        text += "This week the five worst stores were " + byGroup(worst) + ", late on " + span(worst) + " of their orders. "
          + "The five best were " + byGroup(best) + ", late on " + span(best) + ". ";
        // The guess loop closed, and one week weighed against many (J8).
        if (current === "equal" && week === 1)
          text += (!playedOnce && picked ? "You guessed " + picked.value + ". " : "") + "Over many weeks about " + Math.round(d.averages.small_worst) + " of the five worst are small, and about " + Math.round(d.averages.small_best) + " of the five best"
            + (smallIn(worst) < 3 ? ": one week can mislead, so play another. " : ". ");
        if (ringed()) also = stay + " of last week's five again";
      }
      if (worldWorse()) {
        var small = 0, usual = Math.round(size[worse] * d.late);
        late.forEach(function (n, i) { if (group[i] === 0) small += n; });
        text += "The store that really is worse ranked " + ordinal(rank) + ", late on " + pct(rate[worse]) + " percent"
          + (rank > 1 ? ", behind " + (rank === 2 ? "1 store" : (rank - 1) + " stores") + " that only had an unlucky week" : "") + ". "
          + "Its " + late[worse].toLocaleString("en-US") + " late orders were about " + (late[worse] - usual).toLocaleString("en-US") + " more than a store its size usually has, while all " + d.sizes[0].stores + " small stores together had " + small + ". ";
        also = "Worse store " + ordinal(rank);
      }
      if (current === "funnel") {
        var others = out.filter(function (i) { return i !== worse; }).length, found = out.indexOf(worse) >= 0;
        text += found
          ? "Outside the funnel this week: " + (others ? "the store that really is worse, and " + (others === 1 ? "1 other store" : others + " other stores") + " by chance. " : "only the store that really is worse. ")
          : "This week the store that really is worse stayed inside its band" + (others ? ", and " + (others === 1 ? "1 other store" : others + " other stores") + " fell outside by chance" : "") + ". At its size that almost never happens: play another week. ";
      }
      if (current !== "trial") text += ringed() ? d.setups.equal.again : d.setups[current].after;
      if (current === "equal" && week === 1) text += " Play another week to see where these five land.";
      draw();
      el.result.textContent = text.trim();
      playedOnce = true; seen[current] = true;
      el.play.textContent = playLabel();
      addRun(game, [(keys.indexOf(current) + 1) + ". " + d.setups[current].label, String(week), String(smallIn(worst)), also]);
      // The next setup, once this one has shown its point: the first after its second week, the trial after its last.
      var i = keys.indexOf(current), nk = keys[i + 1], shown = current === "equal" ? week >= 2 : current === "trial" ? week >= W : true;
      el.move.hidden = !shown; el.next.hidden = !nk; el.done.hidden = !!nk;
      if (nk) el.next.textContent = "Next: " + (i + 2) + ". " + d.setups[nk].label;
      holdTakeaway(game, seen.trial || Object.keys(seen).length >= 3);
      played(game);
    }

    function choose(k) {
      current = k;
      el.setupButtons.forEach(function (x) { x.setAttribute("aria-pressed", x.getAttribute("data-setup") === k ? "true" : "false"); });
      el.note.textContent = d.setups[current].note;
      reset();
    }
    el.setupButtons.forEach(function (b) { b.addEventListener("click", function () { choose(b.getAttribute("data-setup")); }); });
    el.play.addEventListener("click", play);
    // Next picks the next setup and plays its first week. Focus moves to Play, which stays in place (A9).
    el.next.addEventListener("click", function () {
      var nk = keys[keys.indexOf(current) + 1]; if (!nk) return;
      el.play.focus(); choose(nk); play();
    });
    game.classList.add("is-live");
    holdTakeaway(game, false);
    reset();
  }

  all("[data-game]").forEach(function (game) {
    var kind = game.getAttribute("data-game");
    if (kind === "waiting") waitingGame(game);
    else if (kind === "ranking") rankingGame(game);
    else diceGame(game);
  });

  /* ---- 5. The Compass's two walks (spec S21). Without this, both versions show, one after the other. ---- */
  all("[data-walk-toggle]").forEach(function (box) {
    var buttons = all("[data-walk-show]", box);
    var walks = all("[data-walk]", box.parentNode);
    if (!buttons.length || !walks.length) return;
    function show(id) {
      buttons.forEach(function (b) { b.setAttribute("aria-pressed", b.getAttribute("data-walk-show") === id ? "true" : "false"); });
      walks.forEach(function (w) { w.hidden = w.getAttribute("data-walk") !== id; });
    }
    buttons.forEach(function (b) { b.addEventListener("click", function () { show(b.getAttribute("data-walk-show")); }); });
    box.hidden = false;
    show(buttons[0].getAttribute("data-walk-show"));
  });

  /* ---- 6. The course bar (spec G1 to G4). Without this, its place is a plain link to Start's list of modules.
     With it, the place is a button that opens the list in place, at once (G2). Escape closes it and gives focus
     back to the button; a click or focus outside the bar closes it too, the site's Menu button included (R9). ---- */
  all("[data-course-bar]").forEach(function (bar) {
    var link = bar.querySelector("a.cb-place"), btn = bar.querySelector("button.cb-place"), menu = bar.querySelector(".cb-menu");
    if (!btn || !menu) return;
    /* The list fits the room under the bar, wherever the bar is, and scrolls inside itself when that's short (G3). */
    function fit() { menu.style.maxHeight = Math.max(120, window.innerHeight - bar.getBoundingClientRect().bottom) + "px"; }
    function open(on, refocus) {
      btn.setAttribute("aria-expanded", on ? "true" : "false");
      menu.hidden = !on;
      if (on) fit();
      if (!on && refocus) btn.focus();
    }
    /* Once the bar sticks at the top of the window, the text that scrolls under it fades short of its edge (G1). It
       appears and goes at once: nothing in the bar moves (G2). */
    var queued = false;
    function stuck() {
      queued = false;
      bar.classList.toggle("is-stuck", window.scrollY > 0 && bar.getBoundingClientRect().top <= 0.5);
    }
    function onScroll() {
      if (!menu.hidden) fit();
      if (!queued) { queued = true; window.requestAnimationFrame(stuck); }
    }
    window.addEventListener("resize", function () { if (!menu.hidden) fit(); onScroll(); });
    window.addEventListener("scroll", onScroll, { passive: true });
    stuck();
    btn.addEventListener("click", function () { open(btn.getAttribute("aria-expanded") !== "true"); });
    bar.addEventListener("keydown", function (e) {
      if ((e.key === "Escape" || e.key === "Esc") && !menu.hidden) { e.preventDefault(); open(false, true); }
    });
    doc.addEventListener("click", function (e) { if (!menu.hidden && !bar.contains(e.target)) open(false); });
    bar.addEventListener("focusout", function (e) { if (!menu.hidden && e.relatedTarget && !bar.contains(e.relatedTarget)) open(false); });
    btn.hidden = false;
    if (link) link.hidden = true;
    /* On Start, Continue, from saved progress, in place of Next (G1): the first module, in the map's order, that's
       started and not done; failing that, the first not done after the furthest one done, or else the first not
       done; once every module is done, The Compass. With nothing saved, no Continue. */
    var cont = bar.querySelector("[data-continue]");
    if (!cont) return;
    var mods = all(".cb-list [data-map-unit]", bar).map(function (li) {
      var unit = li.getAttribute("data-map-unit"), ids = (li.getAttribute("data-map-ids") || "").split(" ").filter(Boolean);
      var n = ids.filter(function (id) { return get("pm:" + unit + ":" + id) === "1"; }).length;
      /* It lands on the module's next unticked step (#step-N) once one is ticked, so a reader picks up where they
         left off; a module not yet started opens at its top, where its Why comes first. */
      var first = ids.findIndex(function (id) { return get("pm:" + unit + ":" + id) !== "1"; });
      return { a: li.querySelector("a"), n: n, done: ids.length > 0 && n >= ids.length, step: n > 0 && first >= 0 ? first + 1 : 0 };
    });
    var to = null, last = -1;
    var step = 0;
    mods.forEach(function (m, i) { if (m.done) last = i; if (!to && m.n > 0 && !m.done) { to = m.a; step = m.step; } });
    if (!to && last >= 0) {
      mods.slice(last + 1).concat(mods).some(function (m) { if (!m.done) { to = m.a; step = m.step; return true; } return false; });
      if (!to) to = bar.querySelector(".cb-more a");
    }
    if (!to) return;
    cont.setAttribute("href", to.getAttribute("href") + (step ? "#step-" + step : ""));
    cont.querySelector("[data-continue-to]").textContent = ": " + to.getAttribute("data-label");
    cont.hidden = false;
    var next = bar.querySelector(".cb-next");
    if (next) next.hidden = true;
  });
})();
