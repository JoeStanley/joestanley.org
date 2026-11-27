---
title: Change Safely
layout: module
module: change-safely
question: How good does it have to be, and how do we change it quickly when mistakes are expensive?
setting: a ticketing app for concerts
one_thing: Propose your next rollout on one page, with the level where you'd stop it, and ask whoever leads on call for their view.
do_minutes: 30

last_time:
  - q: Stewart Brand says "Fast learns, slow remembers." Why not push a slow layer to move at a fast layer's pace?
    a: The slow layer holds what the rest depends on, such as a school's record of grades or a contract. Forced to another layer's pace, it ends badly, whichever way the push goes.
  - q: Two parts of a system are coupled "with respect to a particular change." What does that let you do as a PM?
    a: Name the change you expect next, and ask whether it would make both parts move. You often know better than anyone which changes are coming.

steps:
  - id: sre
    kind: read
    title: 'Google SRE book, "Embracing Risk"'
    minutes: 10
    where: A chapter. Free at sre.google. Read "Managing Risk," then "Motivation for Error Budgets."
    links:
      - text: "Embracing Risk"
        url: https://sre.google/sre-book/embracing-risk/
    look: Why 100 percent is the wrong target, and who sets the reliability target, the service level objective (SLO).
    trust: "Experience. Google's site reliability engineers describe their own practice."
    only: One shared number to settle arguments between product and reliability.
  - id: hodgson
    kind: read
    title: 'Pete Hodgson, "Feature Toggles (aka Feature Flags)"'
    minutes: 15
    where: An article from 2016. Free at martinfowler.com. Read "A Toggling Tale," then, under "Categories of toggles," "Release Toggles," "Experiment Toggles" and "Ops Toggles."
    links:
      - text: "Feature Toggles (aka Feature Flags)"
        url: https://martinfowler.com/articles/feature-toggles.html
    look: "How deploying a change differs from releasing it: one puts it into production switched off, the other turns it on for customers, a few at first. Then how an ops toggle switches it off fast."
    trust: "Experience. Hodgson, a software delivery consultant long at Thoughtworks, writes from his work with teams. He's frank that every toggle adds complexity."
    only: The mechanics behind "released to 1 percent of customers," enough to ask your engineers sharp questions.
  - id: dora
    kind: read
    title: 'DORA, "DORA''s software delivery performance metrics"'
    minutes: 10
    where: A guide. Free at dora.dev.
    links:
      - text: "DORA's software delivery performance metrics"
        url: https://dora.dev/guides/dora-metrics/
    look: Which of the five measures show throughput, meaning how fast changes get out, and which show instability, and why smaller changes help both.
    trust: "A review of studies. DORA, a research program Google Cloud now runs, has surveyed software teams every year for more than a decade. The answers are self-reported, and the evidence is in the yearly reports."
    only: The measures as DORA uses them today, so you can ask for your own team's numbers.
  - id: card-error-budgets
    kind: card
    card: cards/error-budgets
    minutes: 5
    look: How a reliability target turns into minutes you can spend.
  - id: pair
    kind: read
    title: 'People + AI Research, "Errors + Graceful Failure"'
    minutes: 15
    where: A chapter of Google's People + AI Guidebook. Free at pair.withgoogle.com. Read from "What's new when working with AI" through "Weigh situational stakes & error risk," then "Provide paths forward from failure."
    links:
      - text: "Errors + Graceful Failure"
        url: https://pair.withgoogle.com/chapter/errors-failing/
    look: Why a feature that's useful 60 percent of the time can be a success or a failure, and the errors that neither the user nor the system notices.
    trust: "Experience. Google's People + AI Research team wrote it from dozens of the company's user research studies, which it doesn't publish."
    only: How good a feature built on a model has to be, asked from the user's side, and what it should do when it's wrong.
  - id: card-read-the-errors
    kind: card
    card: cards/read-the-errors
    minutes: 5
    look: Why you read a model's mistakes before you trust it, and how to tell what a change did.
  - id: do
    kind: do
    title: Propose one rollout, and log it
    where: The Do, on this page, below. Showing it to your tech lead and whoever leads on call can come later.
    look: The level at which you'd stop, for the customers it could hurt most.
  - id: check
    kind: check
    title: Check yourself
    where: The Check, on this page, below.
    look: The answers you missed, and why you missed them.

example:
  body: |
    **Change:** instant pay by bank.

    1. **Cohort:** 1 percent of buyers, between on-sales; then 10, 50, 100, each through a bigger on-sale.
    2. **Goal:** carts checked out, from 62 percent.
    3. **Guardrails,** overall and in social-app browsers, where redirects break: errors, not declines, 0.4 per thousand, stop at 1; money taken, no ticket: one stops it.
    4. **Off switch:** payments on-call, 10 minutes from alert; in on-sales, automatic, in seconds.
    5. **Error budget:** 1 per thousand: 43 minutes' worth at normal traffic. A 10-minute break at 1 percent: six seconds' worth; an on-sale minute, 45 times normal, at 100: the month's.

    **Decision log:** reaches everyone, never switched off. 65 percent sure: untested at on-sale load. Know by June 10.
  good:
    - "Its breakdown and its hard line come from how this change breaks: bank redirects in social-app browsers, and money taken with no ticket, a stop at one."
    - "It prices a break by when it lands as well as how wide, and lets that price argue for the off switch: automatic, in seconds, in on-sales."
    - Its log says why it might fail, untested at on-sale load, and its ramp tests just that, each step through a bigger on-sale.

check:
  - q: Your team has error budget left this month. What does that let you do, and what happens once it's spent?
    a: You can keep releasing, because the budget is room you've already agreed to spend. Once it's spent, releases slow or stop until reliability recovers.
  - q: "{{< pm/mod design-for-change words >}} said the records everything depends on, like a school's grades, move slowly on purpose. This module says small, frequent releases are safer than big, rare ones. Which holds for your record of which fan has which seat?"
    against: design-for-change
    a: Both, at different layers. Ship the code around the seat record in small steps, behind a toggle. Change its data and its contracts slowly, since every sale depends on them, and a toggle can't undo a seat sold twice.
  - q: On your ticketing app, a new seat map raises orders per visit in a test. Why might you still stop the test?
    a: A guardrail metric got worse, such as refunds, complaints about seats or page load time, overall or for one group of customers.
  - q: "**Beyond this module.** Most of this module guards against honest mistakes. What about someone breaking your product on purpose?"
    a: Abuse and attack, where a feature works as designed for someone you never designed it for, like a bot that buys the best seats to resell. Adam Shostack's *Threat Modeling*, on the full path below, starts there.

deeper_one:
  title: "Trustworthy Online Controlled Experiments"
  why: "It covers the two calls here you'll make most often: what an experiment answers to, and how fast a change reaches everyone."
deeper:
  - title: Trustworthy Online Controlled Experiments
    by: Ron Kohavi, Diane Tang and Ya Xu
    where: A book.
    note: Read chapters 6 and 7, on the measures an experiment answers to, then chapter 15, on ramping a change to everyone.
    trust: "Experience. Between them, the authors built experimentation at Microsoft, Google and LinkedIn, and wrote their practical guide from inside large online businesses."
    only: How to choose the measures an experiment answers to, guardrails among them, and fold those you want to move into one overall evaluation criterion. Then how to ramp a change to everyone without trading safety for speed.
  - title: Threat Modeling
    by: Adam Shostack
    where: A book.
    note: "Read Part I, \"Getting Started.\" The [Threat Modeling Manifesto](https://www.threatmodelingmanifesto.org/), which Shostack wrote with other practitioners, puts threat modeling in four questions: \"What are we working on?\" \"What can go wrong?\" \"What are we going to do about it?\" and \"Did we do a good enough job?\""
    trust: "Experience. Shostack spent nearly a decade at Microsoft, where he led the design of its threat modeling tool."
    only: Those four questions worked through at length, with no security training needed, so you can start the conversation with a security engineer while the design can still move.
  - title: AI Engineering
    by: Chip Huyen
    where: A book.
    note: "Read chapters 3 and 4, \"Evaluation Methodology\" and \"Evaluate AI Systems.\""
    trust: "Experience. Huyen taught machine learning systems design at Stanford and writes from real cases, many of them her own. She sticks to the fundamentals rather than any one tool."
    only: "How to tell whether output that varies is good enough, and stays so: graded examples, models as judges and their limits, and checks on each part of the system."
  - title: Ford v Ferrari
    by: directed by James Mangold (20th Century Fox, 2019)
    where: A film.
    note: "Called *Le Mans '66* in some countries. Carroll Shelby and the driver Ken Miles build a car to beat Ferrari by testing it, lap after lap. Yarn taped to the body shows the front lifting at speed, and a brake failure in testing ends in a crash and a fire before they find a fix the rules allow. Meanwhile every change has to pass up through Ford. \"You can't win a race by committee,\" Shelby tells Henry Ford II. The film makes more of a villain of one executive, Leo Beebe, than history does."
    only: Speed that comes from many small tests, each cheap to fail, set against a company trying to make change safe by adding sign-offs.
---

## Why this matters

When a failure would be expensive, as on a ticketing app the morning a big tour goes on sale, the usual answer is more sign-offs and bigger, rarer releases. That feels careful. DORA, a research program on software delivery, points the other way. In its [research on change approval](https://dora.dev/capabilities/streamlining-change-approval/), teams that needed a change board or a senior manager to approve changes were far more likely to be low performers, and it found no sign that the approvals made changes fail less often.

Richard Cook, from {{< pm/mod see-the-system >}}, gives part of the reason: "Change introduces new forms of failure." So a big, rare release brings many of them at once. A small one brings few, and you find them while the change is fresh. Where nobody can tell ahead of time what a change will do, run what Dave Snowden and Mary Boone call "experiments that are safe to fail" (*Harvard Business Review*, 2007).

Before you change anything, know how good the service has to be, in words engineers can test: "When 50,000 fans try to buy in the first minute of an on-sale, checkout confirms 99 in 100 orders within 3 seconds." An average hides the customers who wait, so when someone quotes you one, ask for the 99th {{< pm/term "percentile" >}}.

That's harder to say when the output varies, as a model's does. So decide what the model judges and what stays a plain rule. On your ticketing app, a model can score how likely each buyer is to be a bot, a rule can say what happens at each score, and a person can review the orders it holds back. The model sees patterns nobody could write down, and the rule keeps what happens to a fan predictable and easy to explain. Keep checking after launch: a model's choices can shape the data it learns from next, and a change to one input can shift everything it does ([Sculley and colleagues, 2015](https://proceedings.neurips.cc/paper/2015/hash/86df7dcfd896fcaf2674f757a2463eba-Abstract.html)).

[//]: # (short-path)

## Do

**Propose one rollout (30 minutes).** Pick a change coming up on your product, such as letting fans resell tickets. Write a one-page proposal that answers five things. The call is yours. You set how much risk the change can take and who gets it first. Engineering proposes how fast it ramps and how it's switched off, within those limits, so give your view of those as a start.

1. The cohort: who gets it first, and how many.
2. The goal measure you hope it moves.
3. The {{< pm/term "guardrail-metric" "guardrail metrics" >}}, which must not get worse, such as failed payments per thousand checkouts, and the level at which you'd stop, or a hard line, where one case stops it, such as a seat sold twice. Break each down for the customers the change could hurt most, such as people on older phones or using a screen reader: a guardrail can hold on average while it fails them.
4. Who can switch it off with a {{< pm/term "feature-toggle" "feature toggle" >}}, and how fast.
5. The error budget it might spend. No target yet? Note it, and ask later who sets one.

Outside the 30 minutes, show it to your tech lead and whoever leads on call, and ask, "What do you fix by hand that this could break?" Then accept the plan they propose, or say which limit it misses.

**For your decision log.** Write whether you expect the rollout to reach all your users without being switched off, how sure you are, and why. You'll know when the last group has it.

{{< pm/example >}}

**Optional: read one incident write-up (15 minutes).** Find your team's latest postmortem, or post-incident review. If there's none, read "What happened" and "What went wrong" in Cloudflare's [account of its July 2019 outage](https://blog.cloudflare.com/details-of-the-cloudflare-outage-on-july-2-2019/), where one rule change went everywhere at once. Note when customers were first hurt, when the team knew, and how long switching it off took. Does it name one root cause, or the several that {{< pm/mod see-the-system >}} told you to expect? Outside the 15 minutes, ask your tech lead if you can sit quietly in the next incident review.

## To bring to engineers

Bring what your next change must not make worse, and for whom. Say when a break would cost most, like an on-sale morning.

- How long do the slowest 1 in 100 fans wait today, in the queue or at checkout?
- What can go wrong, and what are we going to do about it?
- If the model that spots bots in this release were quietly wrong next month, what would tell us?
