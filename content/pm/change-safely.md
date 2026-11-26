---
title: Change Safely
layout: module
module: change-safely
question: How good does it have to be, and how do we change it quickly when mistakes are expensive?
setting: a ticketing app for concerts
one_thing: Write a one-page rollout plan for your next change, and include how you'd switch it off.
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
    where: A chapter. Free at sre.google. Read "Managing Risk"; then, under "Identifying the Risk Tolerance of Consumer Services," "Target level of availability" and "Types of failures"; then "Motivation for Error Budgets."
    links:
      - text: "Embracing Risk"
        url: https://sre.google/sre-book/embracing-risk/
    look: Why 100 percent is the wrong target, and who sets the reliability target, the service level objective (SLO).
    trust: "Experience. Google's site reliability engineers describe their own practice."
    only: One shared number to settle arguments between product and reliability.
  - id: hodgson
    kind: read
    title: 'Pete Hodgson, "Feature Toggles (aka Feature Flags)"'
    minutes: 10
    where: An article from 2016. Free at martinfowler.com. Read "A Toggling Tale," then, under "Categories of toggles," "Release Toggles," "Experiment Toggles" and "Ops Toggles."
    links:
      - text: "Feature Toggles (aka Feature Flags)"
        url: https://martinfowler.com/articles/feature-toggles.html
    look: "How deploying a change differs from releasing it: one puts it into production switched off, the other turns it on for customers, a few at first. Then how an ops toggle switches it off fast."
    trust: "Experience. Hodgson is a software delivery consultant who spent years at Thoughtworks, and he writes from his work with teams. He's frank that every toggle adds complexity."
    only: The mechanics behind "released to 1 percent of customers," enough to ask your engineers sharp questions.
  - id: dora
    kind: read
    title: 'DORA, "DORA''s software delivery performance metrics"'
    minutes: 10
    where: A guide. Free at dora.dev.
    links:
      - text: "DORA's software delivery performance metrics"
        url: https://dora.dev/guides/dora-metrics/
    look: Which of the five measures show throughput and which show instability, and why smaller changes help both. If you read *Accelerate* on [Find the Constraint](/pm/find-the-constraint/)'s full path, you've met four of them. DORA has since renamed one and added a fifth, rework rate.
    trust: "A review of studies. DORA, a research program Google Cloud now runs, has surveyed software teams every year for more than a decade, and the guide sums up what it keeps finding. The answers are self-reported, and the evidence is in the yearly reports."
    only: The measures as DORA uses them today, so you can ask for your own team's numbers.
  - id: card-error-budgets
    kind: card
    card: cards/error-budgets
    minutes: 5
    look: How a reliability target turns into minutes you can spend.
  - id: pair
    kind: read
    title: 'People + AI Research, "Errors + Graceful Failure"'
    minutes: 10
    where: A chapter of Google's People + AI Guidebook. Free at pair.withgoogle.com. Read from "What's new when working with AI" through "Weigh situational stakes & error risk," then "Provide paths forward from failure."
    links:
      - text: "Errors + Graceful Failure"
        url: https://pair.withgoogle.com/chapter/errors-failing/
    look: Why a feature that's useful 60 percent of the time can be a success or a failure, and the errors that neither the user nor the system notices.
    trust: "Experience. Google's People + AI Research team wrote it from dozens of the company's user research studies, which it doesn't publish."
    only: How good a feature built on a model has to be, asked from the user's side, and what it should do when it's wrong.
  - id: do
    kind: do
    title: Plan one rollout, and log it
    where: The Do, on this page, below. Asking whoever's on call can come later.
    look: The level at which you'd stop, for the customers it could hurt most.
  - id: check
    kind: check
    title: Check yourself
    where: The Check, on this page, below.
    look: The answers you missed, and why you missed them.

check:
  - q: Your team has error budget left this month. What does that let you do, and what happens once it's spent?
    a: You can keep releasing, because the budget is room you've already agreed to spend. Once it's spent, releases slow or stop until reliability recovers.
  - q: Design for Change said the records everything depends on, like a school's grades, move slowly on purpose. This module says small, frequent releases are safer than big, rare ones. Which holds for your record of which fan has which seat?
    against: design-for-change
    a: Both, at different layers. Ship the code around the seat record in small steps, behind a toggle. Change its data and its contracts slowly, since every sale depends on them, and a toggle can't undo a seat sold twice.
  - q: On your ticketing app, a new seat map raises orders per visit in a test. Why might you still stop the test?
    a: A guardrail metric got worse, such as refunds, complaints about seats or page load time, overall or for one group of customers.
  - q: "**Beyond this module.** Most of this module guards against honest mistakes. What about someone breaking your product on purpose?"
    a: Abuse and attack, where a feature works as designed for someone you never designed it for, like a bot that buys the best seats to resell. Adam Shostack's *Threat Modeling*, on the full path below, starts there.

deeper:
  - title: Trustworthy Online Controlled Experiments
    by: Ron Kohavi, Diane Tang and Ya Xu
    where: A book.
    note: "Read chapters 6 and 7, \"Organizational Metrics\" and \"Metrics for Experimentation and the Overall Evaluation Criterion,\" then chapter 15, \"Ramping Experiment Exposure: Trading Off Speed, Quality, and Risk.\""
    trust: "Experience. Between them, the authors built experimentation at Microsoft, Google and LinkedIn, and a university press published their practical guide, written from inside large online businesses."
    only: How to choose the measures an experiment answers to, guardrails among them, and how to combine the ones you want to move into one overall evaluation criterion. Then how to ramp a change from a few users to everyone without trading safety for speed.
  - title: Threat Modeling
    by: Adam Shostack
    where: A book.
    note: "Read Part I, \"Getting Started.\" Threat modeling means thinking through what could go wrong with a system before it's built or changed. The [Threat Modeling Manifesto](https://www.threatmodelingmanifesto.org/), which Shostack wrote with other practitioners, puts it in four questions: \"What are we working on?\" \"What can go wrong?\" \"What are we going to do about it?\" and \"Did we do a good enough job?\""
    trust: "Experience. Shostack spent nearly a decade at Microsoft, where he led the design of its threat modeling tool."
    only: Those four questions worked through at length, with no security training needed, so you can start the conversation with a security engineer while the design can still move.
  - title: AI Engineering
    by: Chip Huyen
    where: A book.
    note: "Read chapter 3, \"Evaluation Methodology,\" its sections \"Challenges of Evaluating Foundation Models,\" \"Exact Evaluation\" and \"AI as a Judge,\" then chapter 4, \"Evaluate AI Systems,\" its sections \"Evaluation Criteria\" and \"Design Your Evaluation Pipeline.\""
    trust: "Experience. Huyen taught machine learning systems design at Stanford and writes from real cases, many of them her own. She sticks to the fundamentals rather than any one tool."
    only: "How to tell whether output that varies is good enough, and stays so: graded examples, models used as judges and where they fall short, and a pipeline that checks each part of the system."
  - title: Ford v Ferrari
    by: directed by James Mangold (20th Century Fox, 2019)
    where: A film.
    note: "Called *Le Mans '66* in some countries. Carroll Shelby and the driver Ken Miles build a car to beat Ferrari by testing it, lap after lap. Yarn taped to the body shows the front lifting at speed, and a brake failure in testing ends in a crash and a fire before they find a fix the rules allow. Meanwhile every change has to pass up through Ford. \"You can't win a race by committee,\" Shelby tells Henry Ford II. The film makes more of a villain of one executive, Leo Beebe, than history does."
    only: Speed that comes from many small tests, each cheap to fail, set against a company trying to make change safe by adding sign-offs.
---

## Why this matters

When a failure would be expensive, as on a ticketing app the morning a big tour goes on sale, the usual answer is more sign-offs and bigger, rarer releases. That feels careful. DORA, a research program on software delivery, points the other way. In its [research on change approval](https://dora.dev/capabilities/streamlining-change-approval/), teams that needed a change board or a senior manager to approve their changes were far more likely to be low performers, and it found no sign that the approvals made changes fail less often. DORA also finds that speed and stability aren't trade-offs. Its top performers do well on both.

Richard Cook, from [See the System](/pm/see-the-system/), gives part of the reason: "Change introduces new forms of failure." Take that one step further, and a big, rare release brings many of them at once. A small one brings few, and you find them while the change is fresh. Where nobody can work out ahead of time what a change will do, run what Dave Snowden and Mary Boone call "experiments that are safe to fail" (*Harvard Business Review*, 2007).

Before you change anything, know how good the service has to be, in words engineers can test: "When 50,000 fans try to buy in the first minute of an on-sale, checkout confirms 99 in 100 orders within 3 seconds." An average hides the customers who wait, so when someone quotes you one, ask for the 99th {{< pm/term "percentile" >}}.

That's harder to say when the output varies, as a model's does. So decide what the model judges and what stays a plain rule. On your ticketing app, a model can score how likely each buyer is to be a bot, a rule can say what happens at each score, and a person can review the orders it holds back. The model sees patterns nobody could write down, and the rule keeps what happens to a fan predictable and easy to explain. Keep checking after launch, too: a model's choices can shape the data it learns from next, and a change to one input can shift everything it does ([Sculley and colleagues, 2015](https://proceedings.neurips.cc/paper/2015/hash/86df7dcfd896fcaf2674f757a2463eba-Abstract.html)).

[//]: # (short-path)

## Do

**Plan one rollout (20 minutes).** Pick a change that's coming up on your product, such as a new way to pay at checkout. Write a one-page plan that answers five things.

1. The cohort: who gets it first, and how many.
2. The goal measure you hope it raises.
3. The {{< pm/term "guardrail-metric" "guardrail metrics" >}}, which must not get worse, such as failed payments per thousand checkouts, and the level at which you'd stop. Break each down for the customers the change could hurt most, such as people on older phones or using a screen reader: a guardrail can hold on average while it fails them.
4. Who can switch it off with a {{< pm/term "feature-toggle" "feature toggle" >}}, and how fast.
5. The error budget it might spend.

Then, outside the 20 minutes, ask whoever's on call, "What do you fix by hand that this could break?"

**For your decision log.** Write whether you expect the rollout to reach everyone without being switched off, and how sure you are. You'll know when the last group has it.

**Optional: write one quality as a test (10 minutes).** Pick a quality your users would notice if it slipped, such as how long a fan waits in the queue before choosing seats, and write it as engineers would: what triggers it, under which conditions, what responds, and how you'd measure the response. The Software Engineering Institute calls this a quality attribute scenario, and its [report on quality attribute workshops](https://www.sei.cmu.edu/library/quality-attribute-workshops-qaws-third-edition/) gives the full form, with a garage door that has to stop for a bicycle.

## Questions to bring to engineers

- Do we measure this quality today, and what's its 99th percentile?
- What can go wrong, and what are we going to do about it?
- If the model that spots bots in this release were quietly wrong next month, what would tell us?
