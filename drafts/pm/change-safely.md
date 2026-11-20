About 83 minutes: 53 reading, 30 doing.

**If you only do one thing:** Write a one-page rollout plan for your next change, and include how you'd switch it off.

## Why this matters

The Design for Change module asks what should be easy to change. This one asks how to make those changes safely. When a failure would be expensive, as it is on a payments service or a hospital scheduling system, the usual answer is more sign-offs and bigger, rarer releases. That feels careful. The research points the other way: DORA, a research program run by Google Cloud, finds that speed and stability aren't trade-offs, and its top performers do well on both.

Six ideas make that possible. Separate putting a change into production (deploying) from turning it on for customers (releasing). Release first to a small group of customers, called a cohort. Agree up front how much unreliability you'll accept: that's an error budget, and it's built on a service level objective (SLO), a reliability target such as "available 99.9 percent of the time". Watch the guardrail metrics, the measures that must not get worse. Bring your security people in while the design can still move. And when a situation is complex, meaning you can't work out the answer ahead of time, run small experiments that are safe to fail, where a bad result does little harm.

## The short path

1. **Google SRE book, "Embracing Risk" (Chapter 3)**

   15 minutes. Free at sre.google. Read "Managing Risk", "Measuring Service Risk", the consumer services part of "Risk Tolerance of Services", and "Motivation for Error Budgets". You can skip the part on infrastructure services.

   **Look for:** Who sets the reliability target (the SLO), and what happens to releases once the error budget runs out. The budget is the amount of unreliability you've agreed to accept.

   **Why trust it:** It's a chapter of a book by Google's own site reliability engineers about how Google runs its services. That makes it a practitioner's account, not an independent study.

   **What you'll get:** The argument for why 100 percent reliability is the wrong target, and a way to settle disputes between product and reliability with one shared number.
2. **Pete Hodgson, "Feature Toggles" (martinfowler.com)**

   15 minutes. Free at martinfowler.com. A feature toggle is a switch in the software that turns a feature on or off without a new deployment. Read "A Toggling Tale", especially "Canary releasing" (releasing to a small group first) and "A/B testing" (comparing two versions on different groups). Then, under "Categories of toggles", read the four toggle types. Stop when you reach "Implementation Techniques".

   **Look for:** A release toggle and an experiment toggle do different jobs, and they don't live for the same length of time.

   **Why trust it:** The article appeared on Martin Fowler's site in 2016 and was revised in 2017. It's an engineer explaining how the thing works, not research.

   **What you'll get:** The plain mechanics behind "released to 1 percent of customers", so you can ask your engineers sharp questions about it.
3. **DORA software delivery metrics (the metrics guide and its history page)**

   8 minutes. Free at dora.dev.

   **Look for:** Which of the five measures count as throughput (how fast you deliver) and which as instability (how often delivery goes wrong), and why speed and stability aren't trade-offs.

   **Why trust it:** DORA is a research program run by Google Cloud, and its content is open under a Creative Commons license.

   **What you'll get:** Names for the five delivery measures, so you can go and ask for your own team's numbers.
4. **Threat Modeling Manifesto**

   5 minutes. Free at threatmodelingmanifesto.org.

   **Look for:** The four questions (what are we building, what could go wrong, what will we do about it, did we do a good enough job), and the principle of early and frequent analysis.

   **Why trust it:** A working group of 15 practitioners in security and privacy threat modeling wrote it. It's a set of values and principles, not a method.

   **What you'll get:** Four questions that need no security training, so you can use them to open a conversation with a security engineer. Threat modeling here means thinking through what could go wrong with a system before it's built or changed.
5. **Error Budgets**

   Concept card. 5 minutes.

   **Look for:** The budget is a product decision about how much unreliability customers will put up with, not an engineering rule.
6. **Guardrail Metrics**

   Concept card. 5 minutes.

   **Look for:** The difference between the measure you're hoping to move and the ones that must not get worse.

## Do

**Plan one rollout (20 minutes).** Pick one change that's coming up on your product, such as a new rate limit on an API, a challenger search ranking in a champion and challenger test (a test where the current approach, the champion, runs against a new one, the challenger, on different customers), or a redesigned checkout step. Write a one-page plan with six lines.

1. The cohort: who gets it first, how many of them, and how they're chosen.
2. The goal measure: the one number you're hoping the change will raise.
3. The guardrail metrics, and the level at which you stop. For example: "stop if failed payments per thousand checkouts rise by more than a set amount over the control group." Pick your own number with your team.
4. The switch-off: who can turn it off and how fast, without a new deployment.
5. The error budget the change might spend: the worst plausible downtime or number of failed requests, set against your team's reliability target. If there's no target, write "none agreed" and name who could set one.
6. Your own first-draft answers to the four threat modeling questions.

When you're done, book 20 minutes with a security engineer (not counted in the time above) and go through line 6 together. Ask: "What would you most want to catch before this goes live?"

**Optional: probe a complex problem (10 minutes).** Name one situation on your product where nobody can say ahead of time what will work, such as how drivers on a delivery app will react to a new rule for batching orders. Design one small experiment that's safe to fail: what you'd try, on whom, and what result would make you stop.

## Check yourself

Answer in your head, then check.

Your team has error budget left this quarter. What does that let you do, and what happens once the budget is spent?

**Answer:** You can keep releasing, because the budget is room you've already agreed to spend. If it runs out, releases slow or stop until reliability recovers (Google's example policy, listed under Go deeper, halts changes except urgent fixes).

What's the difference between deploying a change and releasing it?

**Answer:** Deploying puts the code into production, and releasing makes the feature available to customers. A toggle, the switch described in item 2, lets you do the two at different times. That's how you can release to a small cohort and turn the feature off without redeploying.

On a marketplace, a challenger search ranking raises orders per visit. Why might you still stop the test?

**Answer:** Because a guardrail metric got worse, such as returns, late deliveries or page load time. Guardrails are there to catch harm while you chase the goal measure.

## Go deeper: the full path

Optional, and not counted in the time above.

- **"A Leader's Framework for Decision Making," David Snowden and Mary Boone (2007)** Harvard Business Review, November 2007. **Why trust it:** The article sets out the Cynefin framework for judging how to act in complex situations. **What you'll get:** A way to tell a complex situation, where small experiments that can safely fail are the right move, from one where analysis or good practice will do.
- **Trustworthy Online Controlled Experiments, Ron Kohavi, Diane Tang and Ya Xu (2020)** **Why trust it:** It's a published book from Cambridge University Press (2020), and its subtitle calls it a practical guide to A/B testing. **What you'll get:** The full treatment of metrics for experiments, including how to combine them into one overall evaluation criterion.
- **Error budget policy, Google SRE Workbook (Appendix B)** Free at sre.google. **Why trust it:** It's an example policy from Google's SRE Workbook, laid out as a template. **What you'll get:** A worked example of what a team agrees to do once the budget is spent, and what the exceptions are.

# Error Budgets

## The idea

No service is perfectly reliable, and chasing 100 percent costs more than customers will ever notice. So you agree on a reliability target, called a service level objective (SLO), such as "the service answers requests successfully 99.9 percent of the time", and you treat the gap below perfect as a budget. In Google's account, product and reliability teams set the budget together, each quarter, from the SLO. While there's budget left, releases go ahead. Once it's spent, they slow or stop until reliability recovers.

## Why a PM cares

- **The target is a product decision.** How much unreliability customers will put up with depends on what they expect, whether the service ties to revenue, and what competitors offer. Engineers can't settle that alone.
- **It ends arguments about opinion.** Product teams are often judged on how fast they ship, and reliability engineers on reliability. (Google calls them site reliability engineers, or SREs; your company may say operations or platform engineers.) So the two disagree about how much testing to do and how often to release. A shared number settles it with data.
- **It puts a number on caution.** "We can't afford failures" turns into a figure you can spend. A 99.9 percent target over 30 days leaves about 43 minutes of failure (simple arithmetic: 0.1 percent of 43,200 minutes).
- **It lets you innovate on purpose.** Google's chapter notes that a team can choose to loosen an SLO, which frees up room to innovate.

## How to spot it

- Arguments about reliability and releases end with "it depends who you ask" instead of a number.
- Nobody can tell you the availability target (how often the service is up) or the response target (how fast it answers) for your service, or who agreed to it.
- Releases freeze after every incident, however small, or they never freeze at all.
- Every part of the service has the same target, even though some failures cost far more than others.

## What it does not say

It does not say all failures are equal. Google's chapter notes that the type of failure matters: a privacy leak is far worse than a brief display glitch. Go one step further than the chapter. A double charge on a card or a missed alarm from a factory sensor is a different kind of failure: keep it outside the budget and treat it as a hard line. And the budget doesn't work without a neutral measure of what customers actually experience.

**One question to carry:** How much failure would our customers accept for this service, and who agreed to that?

## Go deeper

**[Embracing Risk](https://sre.google/sre-book/embracing-risk/), Google SRE book (Chapter 3)**

Free at sre.google.

**Why trust it:** Google's site reliability engineers wrote the book, and in this chapter they're describing their own practice.

**What you'll get:** The reasoning behind the budget, and how product and reliability teams share it.

# Guardrail Metrics

## The idea

A guardrail metric is a measure you agree must not get worse while you go after your goal. When you test a change, you watch two kinds of number: the goal measure, the one number you're hoping will rise, and the guardrails, which protect against harm you didn't intend. If a guardrail is breached (it crosses the level you agreed on in advance), the change is in trouble even if the goal measure improves. One summary of the book by Kohavi, Tang and Xu gives latency, crash rates and spam levels as examples; on a travel booking site, think booking errors and refund requests.

## Why a PM cares

- **It stops a win that's really a loss.** A pushier purchase prompt in a game can lift sales while uninstalls and one-star reviews rise too. Without a guardrail, you ship the harm.
- **It sets the stop rule before you're emotionally invested.** Agree on the level that stops the test while nobody knows the results yet.
- **It's Goodhart's Law applied.** The Goodhart's Law card in this syllabus covers the idea that when a measure becomes a target, it stops being a good measure, so a single target gets gamed. A guardrail pairs a goal with the measure that would show the gaming.
- **It makes known risks visible.** On a hospital scheduling system, double bookings, missed appointments and the wait for urgent cases are natural guardrails.

## How to spot it

- A test plan names one success measure and nothing that must not get worse.
- Results are reported as "bookings up" with no mention of refund requests, booking errors or support tickets.
- Nobody can tell you who's allowed to stop a test, or at what level.
- The cohort (the small group getting the change first) is small, yet the plan has no way to tell real harm from chance variation, which statisticians call noise.

## What it does not say

It does not say every metric needs a guardrail, or that a few guardrails make a test safe. Pick the few that match the harms you fear most, and agree on the stop level in advance. Keep in mind that a guardrail only tells you about what you thought to measure.

**One question to carry:** If this change worked on the goal measure but hurt a customer, what number would show it first?

## Go deeper

**[Trustworthy Online Controlled Experiments](https://www.cambridge.org/core/books/trustworthy-online-controlled-experiments/metrics-for-experimentation-and-the-overall-evaluation-criterion/4EA73D169EC43B58991D6824717E8FD3), Ron Kohavi, Diane Tang and Ya Xu (2020)**

A book from Cambridge University Press; the link is to its chapter on metrics.

**Why trust it:** It's a published book from Cambridge University Press (2020), and its subtitle calls it a practical guide to A/B testing.

**What you'll get:** How to choose and combine experiment metrics.
