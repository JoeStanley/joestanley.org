/* PM Syllabus. Small, dependency-free behaviour for the /pm/ section.
   Everything here is an extra: the pages read fine with JavaScript off.
   1. Progress: ticks on the short path, saved in this browser only.
   2. Single-document view: show one unit at a time (used by the preview and the print page).
   3. The games: the dice game, the waiting game and the ranking game.
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

  /* ---- 3. the games (spec J5): the dice game, the waiting game and the ranking game ---- */
  var still = function () { return !!(window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches); };
  var money = function (n) { return "$" + Math.round(n).toLocaleString("en-US"); };
  /* While a run plays, Play is marked busy rather than disabled, so it keeps keyboard and screen reader focus. */
  var busyOn = function (btn, on) { if (on) btn.setAttribute("aria-disabled", "true"); else btn.removeAttribute("aria-disabled"); };

  function diceGame(game) {
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
  }

  /* The waiting game: three jobs built one at a time. Each week a job isn't live costs what it's really worth, the
     weeks it's being built included. What each is worth is drawn fresh for every run: the reader sees only estimates,
     and may test one while the team builds. Its answer comes in at the end of week test_weeks. A pick that isn't made
     yet falls due when the job before it goes live, and the run waits there. */
  function waitingGame(game) {
    var dataEl = game.querySelector("[data-game-setups]"); if (!dataEl) return;
    var d; try { d = JSON.parse(dataEl.textContent); } catch (e) { return; }
    var jobs = d.jobs, T = d.test_weeks, by = {}, places = ["1st", "2nd", "3rd"];
    jobs.forEach(function (j) { by[j.id] = j; });
    var el = {
      tests: all("[data-test]", game), picks: all("[data-pick]", game), rules: all("[data-setup]", game), note: game.querySelector("[data-setup-note]"),
      report: game.querySelector("[data-report]"), week: game.querySelector("[data-week]"), live: game.querySelector("[data-live]"), cost: game.querySelector("[data-cost]"),
      play: game.querySelector("[data-play]"), result: game.querySelector("[data-result]"), takeaway: game.querySelector("[data-takeaway]"), rows: {}
    };
    all("[data-row]", game).forEach(function (r) { el.rows[r.getAttribute("data-row")] = all(".wk", r); });
    var rule = "est", test = "none", order = d.rules.est.order.slice();
    var wk = 0, worth = null, outcome = null, started = false, paused = false, running = false, timer = null, playedOnce = false, pickedAt = [];

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
      jobs.forEach(function (j) {
        el.rows[j.id].forEach(function (cell, i) {
          var w = i + 1, s = "", q = p[j.id];
          if (started && w <= wk) s = !q || w <= q.start ? " is-wait" : w <= q.live ? " is-build" : " is-live";
          cell.className = "wk" + s;
        });
      });
      el.week.textContent = wk;
      el.live.textContent = started ? order.filter(function (id) { return p[id].live <= wk; }).length : 0;
      el.cost.textContent = money(started ? costTo(wk) : 0);
    }
    function said(ids) { return ids.map(function (id) { return by[id].short; }).join(", then "); }
    function cap(t) { return t.charAt(0).toUpperCase() + t.slice(1); }
    function showState() {
      el.tests.forEach(function (b) { b.setAttribute("aria-pressed", b.getAttribute("data-test") === test ? "true" : "false"); });
      el.picks.forEach(function (b) {
        var i = order.indexOf(b.getAttribute("data-pick"));
        b.setAttribute("aria-pressed", i >= 0 ? "true" : "false");
        b.querySelector("[data-place]").textContent = i >= 0 ? places[i] : "";
      });
      el.rules.forEach(function (b) { b.setAttribute("aria-pressed", b.getAttribute("data-setup") === rule ? "true" : "false"); });
      var what = test === "none" ? "No test. " : test === "all" ? "" : "Testing " + by[test].short + ". ";
      if (rule) el.note.textContent = d.rules[rule].label + ". " + (rule === "stop" ? "The team waits for all three answers, then builds the cheapest order."
        : rule === "test" ? "First " + by[order[0]].short + ", then the next pick, made on the test's answer." : cap(said(order)) + ".");
      else if (paused) el.note.textContent = what + cap(by[order[order.length - 1]].short) + " went live after week " + wk + ". Pick the next job, then play on.";
      else el.note.textContent = what + (!order.length ? "Pick the job to build first." : complete() ? "Your order: " + said(order) + "." : "First, " + said(order) + ". Pick the next now, or play and pick it when it falls due.");
    }
    function reset() {
      clearTimeout(timer); wk = 0; started = false; paused = false; running = false; worth = null; pickedAt = [];
      busyOn(el.play, false); el.result.textContent = ""; el.report.textContent = "";
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
    function report() {
      if (test === "none") return;
      var ids = test === "all" ? jobs.map(function (j) { return j.id; }) : [test];
      el.report.textContent = "Week " + T + ": " + (test === "all" ? "all three answers are in. " : "the test's answer is in. ") + ids.map(function (id) {
        var j = by[id], line = j.values ? j.report : outcome.report;
        return line.replace("{value}", money(worth[id]));
      }).join(" ");
    }
    function known(id) { return test === "all" || id === test ? (wk >= T ? worth[id] : estimate(id)) : estimate(id); }
    function finish() {
      var p = plan(), total = costTo(wk), best = d.best, text = "";
      var picked = game.querySelector("input[name=waiting-guess]:checked"), b = bet();
      if (!playedOnce && picked) text = "You guessed " + picked.value + ". ";
      var others = jobs.filter(function (j) { return j.values; });
      text += b.tag + " " + outcome.said + ": it was worth " + money(worth[b.id]) + " a week. "
        + others.map(function (j, i) { return (i === 0 ? cap(by[j.id].short) + " was worth " : by[j.id].short + " ") + money(worth[j.id]) + (i === 0 ? " a week" : ""); }).join(" and ") + ". ";
      var when = order.map(function (id, i) { return by[id].short + (i === 0 ? " went live after week " : " after week ") + p[id].live; });
      text += "In this order, " + when.slice(0, -1).join(", ") + " and " + when[when.length - 1] + ". The waiting cost " + money(total) + ". ";
      var ideal = (function () { var keep = order, keepTest = test; order = []; test = "none"; var o = bestRest(function (id) { return worth[id]; }); order = o; var c = costTo(Infinity); order = keep; test = keepTest; return c; })();
      text += total === ideal ? "Had you known every number from the start, you couldn't have done better. "
        : "Knowing every number from the start, the cheapest order would have cost " + money(ideal) + ", so this one cost " + money(total - ideal) + " more. ";
      if (rule) text += d.rules[rule].after + " Over every outcome this plan averages " + money(d.rules[rule].average) + (d.rules[rule].average === best.average ? ", as little as knowing everything would." : ".");
      else if (test === "none") text += "Nothing was tested, so every pick rested on the estimates.";
      else if (by[test].values) text += "Testing " + by[test].short + " told you little the estimate hadn't: no answer inside its range could change the order.";
      else if (order[0] === test) text += "The test's answer came in while " + by[test].short + " was already being built, too late for the pick it could have changed.";
      else if (pickedAt[1] >= T) text += "The test's answer was in by the time the next pick fell due, so the pick could use it.";
      else text += "The test's answer came in at week " + T + ", but you had picked the order before it did.";
      el.result.textContent = text.trim();
      playedOnce = true; running = false; paused = false; busyOn(el.play, false);
      el.play.textContent = "Play again";
      if (el.takeaway) el.takeaway.hidden = false;
    }
    /* Play on until every job is live, or until a pick falls due that no plan makes. */
    function step() {
      wk++;
      if (test !== "none" && wk === T) report();
      if (!complete() && due() <= wk) {
        if (rule === "stop" || rule === "test") { var o = bestRest(known); order = order.concat(o); pickedAt.push(wk); }
        else { draw(); paused = true; running = false; busyOn(el.play, false); el.play.textContent = "Play on"; showState(); return false; }
      }
      draw();
      if (complete() && wk >= due()) { finish(); return false; }
      return true;
    }
    function play() {
      if (running) return;
      if (paused) { if (!complete()) { el.note.textContent = "Pick the next job, then play on."; return; } paused = false; }
      else {
        if (!order.length && rule !== "stop") { showState(); return; }
        clearTimeout(timer); wk = 0; started = true; draws(); pickedAt = order.map(function () { return 0; });
        el.result.textContent = ""; el.report.textContent = "";
      }
      running = true; busyOn(el.play, true); showState();
      if (still()) { while (step()) {} return; }
      (function tick() { if (step()) timer = setTimeout(tick, 260); })();
    }

    el.tests.forEach(function (b) {
      b.addEventListener("click", function () {
        test = b.getAttribute("data-test");
        if (rule) order = rule === "est" || rule === "biggest" ? d.rules[rule].order.slice() : [];
        rule = ""; reset();
      });
    });
    el.picks.forEach(function (b) {
      b.addEventListener("click", function () {
        var id = b.getAttribute("data-pick");
        if (paused) {
          if (order.indexOf(id) >= 0) return;
          order.push(id); pickedAt.push(wk); if (order.length === jobs.length - 1) { fill(); pickedAt.push(wk); }
          showState(); el.note.textContent = "Next, " + said(order.slice(order.indexOf(id))) + ". Play on."; return;
        }
        if (rule) { test = d.rules[rule].test === "all" ? "none" : d.rules[rule].test; rule = ""; order = []; }
        if (complete()) order = [id];
        else if (order.indexOf(id) < 0) { order.push(id); if (order.length === jobs.length - 1) fill(); }
        reset();
      });
    });
    el.rules.forEach(function (b) {
      b.addEventListener("click", function () { rule = b.getAttribute("data-setup"); test = d.rules[rule].test; order = d.rules[rule].order.slice(); reset(); });
    });
    el.play.addEventListener("click", play);
    game.classList.add("is-live");
    if (el.takeaway) el.takeaway.hidden = true;
    reset();
  }

  /* The ranking game: stores of three sizes, every one late on the same share of orders, ranked each week by their
     late rate. In the last two setups one large store really is worse, and the funnel shows the range chance allows. */
  function rankingGame(game) {
    var dataEl = game.querySelector("[data-game-setups]"); if (!dataEl) return;
    var d; try { d = JSON.parse(dataEl.textContent); } catch (e) { return; }
    var size = [], group = [];
    d.sizes.forEach(function (g, gi) { for (var i = 0; i < g.stores; i++) { size.push(g.orders); group.push(gi); } });
    var N = size.length, worse = N - 1, TOP = 0.4, current = "equal", week = 0, playedOnce = false;
    var rate = null, late = null, worst = [], best = [], prevWorst = null, out = [];
    var tr = { fix: [0, 0], rest: [0, 0] }, F = d.trial.stores;
    var el = {
      dots: all(".rk-dot", game), week: game.querySelector("[data-week]"), small: game.querySelector("[data-small]"), best: game.querySelector("[data-best]"),
      note: game.querySelector("[data-setup-note]"), result: game.querySelector("[data-result]"), play: game.querySelector("[data-play]"),
      takeaway: game.querySelector("[data-takeaway]"), setupButtons: all("[data-setup]", game)
    };
    var worldWorse = function () { return current === "worse" || current === "funnel"; };
    var inTrial = function (i) { return current === "trial" && i < F; };
    var pct = function (r) { return String(Math.round(r * 1000) / 10); };
    var ordinal = function (k) { var t = k % 100; return k + (t > 10 && t < 14 ? "th" : ["th", "st", "nd", "rd"][k % 10] || "th"); };

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

    function draw() {
      game.classList.toggle("shows-funnel", current === "funnel" && week > 0);
      el.dots.forEach(function (dot, i) {
        var has = rate !== null;
        dot.style.setProperty("--r", has ? Math.min(rate[i], TOP) / TOP : 0);
        dot.classList.toggle("is-shown", has);
        dot.classList.toggle("is-worst", has && worst.indexOf(i) >= 0);
        dot.classList.toggle("was-worst", has && current === "next" && !!prevWorst && prevWorst.indexOf(i) >= 0);
        dot.classList.toggle("is-worse", i === worse && worldWorse());
        dot.classList.toggle("is-out", has && current === "funnel" && out.indexOf(i) >= 0);
        dot.classList.toggle("is-trial", inTrial(i));
      });
      el.week.textContent = week;
      el.small.textContent = rate ? smallIn(worst) : 0;
      el.best.textContent = rate ? smallIn(best) : 0;
    }
    function reset() {
      el.result.textContent = "";
      if (current !== "next") prevWorst = null;
      rate = null; week = 0; tr = { fix: [0, 0], rest: [0, 0] }; draw();
      el.play.textContent = "Play a week";
    }

    function play() {
      var picked = game.querySelector("input[name=ranking-guess]:checked"), text = "";
      if (current === "next") {
        if (!prevWorst) { oneWeek(); prevWorst = worst.slice(); }
        else prevWorst = worst.slice();
      }
      var idx = oneWeek(); week++;
      if (current === "equal") prevWorst = worst.slice();
      draw();
      if (!playedOnce && picked) text = "You guessed " + picked.value + ". ";
      if (current === "next") {
        var stay = worst.filter(function (i) { return prevWorst.indexOf(i) >= 0; }).length;
        text += "Of last week's five worst, " + (stay === 0 ? "none is" : stay === 1 ? "1 is" : stay + " are") + " among the five worst again. ";
      }
      if (current === "trial") {
        var fix = [0, 0], rest = [0, 0];
        for (var t = 0; t < N; t++) if (group[t] === 0) { var g = t < F ? fix : rest; g[0] += late[t]; g[1] += size[t]; }
        tr.fix[0] += fix[0]; tr.fix[1] += fix[1]; tr.rest[0] += rest[0]; tr.rest[1] += rest[1];
        var n_ = worst.filter(function (i) { return i < F; }).length, others = d.sizes[0].stores - F;
        var word = function (k) { return ["no", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"][k] || String(k); };
        text += "Week " + week + " of the trial. This week the " + word(F) + " stores with the fix were late on " + pct(fix[0] / fix[1]) + " percent of their orders, and the " + word(others) + " small stores without it on " + pct(rest[0] / rest[1]) + " percent. "
          + "Of the five worst stores, " + (n_ === 0 ? "none has" : n_ === 1 ? "one has" : word(n_) + " have") + " the fix. "
          + (week > 1 ? "Over the " + week + " weeks so far, " + pct(tr.fix[0] / tr.fix[1]) + " percent with the fix and " + pct(tr.rest[0] / tr.rest[1]) + " without. " : "");
      } else {
        text += "This week the five worst stores were " + byGroup(worst) + ", late on " + span(worst) + " of their orders. "
          + "The five best were " + byGroup(best) + ", late on " + span(best) + ". ";
      }
      if (current === "worse" || current === "funnel") {
        var k = idx.indexOf(worse) + 1, small = 0, usual = Math.round(size[worse] * d.late);
        late.forEach(function (n, i) { if (group[i] === 0) small += n; });
        text += "The store that really is worse ranked " + ordinal(k) + ", late on " + pct(rate[worse]) + " percent"
          + (k > 1 ? ", behind " + (k === 2 ? "1 store" : (k - 1) + " stores") + " that only had an unlucky week" : "") + ". "
          + "Its " + late[worse].toLocaleString("en-US") + " late orders were about " + (late[worse] - usual).toLocaleString("en-US") + " more than a store its size usually has, while all " + d.sizes[0].stores + " small stores together had " + small + ". ";
      }
      if (current === "funnel") {
        var others = out.filter(function (i) { return i !== worse; }).length, found = out.indexOf(worse) >= 0;
        text += found
          ? "Outside the funnel this week: " + (others ? "the store that really is worse, and " + (others === 1 ? "1 other store" : others + " other stores") + " by chance. " : "only the store that really is worse. ")
          : "This week the store that really is worse stayed inside its band" + (others ? ", and " + (others === 1 ? "1 other store" : others + " other stores") + " fell outside by chance" : "") + ". At its size that almost never happens: play another week. ";
      }
      text += d.setups[current].after;
      if (current === "trial") text += " Run this trial many times, and after one week the stores with the fix look better than those without in " + d.averages.trial_better_one + " runs in 100, and worse in " + d.averages.trial_worse_one + ". After eight weeks they look better in " + d.averages.trial_better_eight + ".";
      el.result.textContent = text.trim();
      playedOnce = true;
      el.play.textContent = "Play another week";
      if (el.takeaway) el.takeaway.hidden = false;
    }

    el.setupButtons.forEach(function (b) {
      b.addEventListener("click", function () {
        current = b.getAttribute("data-setup");
        el.setupButtons.forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
        el.note.textContent = d.setups[current].note;
        reset();
      });
    });
    el.play.addEventListener("click", play);
    game.classList.add("is-live");
    if (el.takeaway) el.takeaway.hidden = true;
    reset();
  }

  all("[data-game]").forEach(function (game) {
    var kind = game.getAttribute("data-game");
    if (kind === "waiting") waitingGame(game);
    else if (kind === "ranking") rankingGame(game);
    else diceGame(game);
  });
})();
