About 48 minutes: 18 reading, 30 doing (a 20-minute exercise and a 10-minute optional one).

**If you only do one thing:** Write a one-page rollout plan for your next change, and include how you'd switch it off.

## Why this matters

When a failure would be expensive, as on a payments service or an insurance claims system, the usual answer is more sign-offs and bigger, rarer releases. That feels careful. The research points the other way. DORA, Google Cloud's research program, finds that speed and stability aren't trade-offs: its top performers do well on both. Richard Cook, from Module 1, gives part of the reason: "Change introduces new forms of failure."

First, though, know how good it has to be, in words engineers can test: "When 500 students submit their exams in the same minute at the deadline, the submission service confirms 99 in 100 within 3 seconds." An average hides the customers who wait, so when someone quotes you one, ask for the 99th percentile.

## The short path

1. **Google SRE book, "Embracing Risk" (Chapter 3)**

   8 minutes. Free at sre.google. Read "Managing Risk", "Target level of availability" under consumer services, and "Motivation for Error Budgets".

   **Look for:** Why 100 percent is the wrong target, and who sets the reliability target, the service level objective (SLO).

   **Why trust it:** Google's site reliability engineers describe their own practice. It's a practitioner's account, not an independent study.

   **What you'll get:** One shared number to settle disputes between product and reliability.
2. **Pete Hodgson, "Feature Toggles" (martinfowler.com, 2017)**

   8 minutes. Free at martinfowler.com. Read "A Toggling Tale", then "Release Toggles" and "Experiment Toggles" under "Categories of toggles".

   **Look for:** How deploying a change, putting it into production switched off, differs from releasing it to customers, a few at first.

   **Why trust it:** Hodgson is an engineer explaining how the thing works, on Martin Fowler's site. It's practice, not research.

   **What you'll get:** The mechanics behind "released to 1 percent of customers", so you can ask your engineers sharp questions.
3. **Error Budgets**

   Concept card. 2 minutes.

   **Look for:** How a reliability target turns into minutes you can spend.

## Do

**Plan one rollout (20 minutes).** Pick a change that's coming up on your product, such as a new search ranking. Write a one-page plan in five lines.

1. The cohort: who gets it first, and how many.
2. The goal measure you hope it raises.
3. The guardrail metrics, which must not get worse, such as failed payments per thousand checkouts, and the level at which you'd stop.
4. Who can switch it off, and how fast.
5. The error budget it might spend. If your team has no reliability target, name who could set one.

Then, outside the 20 minutes, ask whoever's on call, "What do you fix by hand that this could break?"

**Optional: write one quality as a test (10 minutes).** Pick a quality your users would notice if it slipped, such as how long a player waits for a match, and write it as engineers would: what triggers it, under which conditions, what responds, and how you'd measure the response.

## Questions to bring to engineers

- Do we measure this quality today, and what's its 99th percentile?
- Who agreed our reliability target, and what happens when the error budget runs out?
- What can go wrong, and what are we going to do about it?
- If this model were quietly wrong next month, what would tell us?

## Check yourself

Answer in your head, then check.

Your team has error budget left this quarter. What does that let you do, and what happens once it's spent?

**Answer:** You can keep releasing, because the budget is room you've already agreed to spend. Once it's spent, releases slow or stop: Google's example policy, on the card, halts changes except urgent fixes.

What's the difference between deploying a change and releasing it?

**Answer:** Deploying puts the code into production, and releasing turns the feature on for customers. A toggle separates the two, so you can release to a small cohort and switch it off without redeploying.

On a marketplace, a new search ranking raises orders per visit in a test. Why might you still stop the test?

**Answer:** A guardrail metric got worse, such as returns, late deliveries or page load time.

## Go deeper: the full path

Optional, and not counted in the time above.

- **Trustworthy Online Controlled Experiments, Ron Kohavi, Diane Tang and Ya Xu (Cambridge University Press, 2020)** A book. Read its chapters on metrics. **Why trust it:** The authors led experimentation at Microsoft, Google and LinkedIn, and a university press published it. It's a practical guide to A/B testing, written from inside large online businesses. **What you'll get:** The full treatment of metrics for experiments: goal measures, guardrails, and how to combine them into one overall evaluation criterion.
- **"DORA's software delivery performance metrics," DORA (Google Cloud)** A short guide, about 6 minutes. Free at dora.dev. **Why trust it:** It sums up the findings of Google Cloud's research program and leaves the evidence to its yearly reports. **What you'll get:** Names for the five delivery measures, sorted into throughput and instability, so you can ask for your own team's numbers.
- **"A Leader's Framework for Decision Making," David Snowden and Mary Boone (Harvard Business Review, November 2007)** An article. **Why trust it:** Snowden created the Cynefin framework, and this is his account of it for managers, written with Boone. It argues from cases, so read it as a framework, not a finding. **What you'll get:** A way to tell a complex situation, where nobody can work out the answer ahead of time and small experiments that are safe to fail are the right move, from one where analysis or good practice will do.
- **Threat Modeling Manifesto** Free at threatmodelingmanifesto.org, about 5 minutes. Threat modeling means thinking through what could go wrong with a system before it's built or changed, and the manifesto puts it in four questions: "What are we working on?", "What can go wrong?", "What are we going to do about it?" and "Did we do a good enough job?" **Why trust it:** A working group of 15 practitioners in security and privacy threat modeling wrote it. It's a set of values and principles, not a method. **What you'll get:** Four questions that need no security training, to open a conversation with a security engineer while the design can still move.
- **"Hidden Technical Debt in Machine Learning Systems," D. Sculley and nine co-authors (NeurIPS, 2015)** A conference paper. Free at proceedings.neurips.cc. **Why trust it:** It was presented at NeurIPS, a machine learning conference, and all ten authors were at Google when it was published. The tools it mentions are dated, so skim past them. **What you'll get:** Names to ask your engineers about for the ways a model in production goes quietly wrong, such as feedback loops, where its choices shape the data it learns from next, and "changing anything changes everything".

*To check: before the rebuild cites a quality attribute scenario (the optional exercise), open the free Software Engineering Institute report, Barbacci and others, Quality Attribute Workshop Participants Handbook, or Michael Keeling's Design It!. Also check Hodgson's dates (2017, revised from 2016) and the Manifesto's wording of its last three questions. The trust lines for DORA, for Kohavi, Tang and Xu, and for Snowden and Boone were rewritten from what's widely known, so check the program's yearly reports, the three authors' roles at Microsoft, Google and LinkedIn, and that Snowden created Cynefin.*

## For the glossary

- **Service level objective (SLO):** A reliability target for a service, such as "up 99.9 percent of the time", agreed before anything goes wrong.
- **Error budget:** The amount of failure a service's SLO allows, treated as a budget. While some is left, releases go ahead.
- **Feature toggle:** A switch in the software that turns a feature on or off without a new deployment.
- **Guardrail metric:** A measure that must not get worse while you try to move another. You agree in advance the level at which you'd stop.
- **Percentile:** Where a case falls when all of them are ranked. If the 99th percentile wait is 3 seconds, 99 in 100 wait 3 seconds or less.

# Error Budgets

*Picture: A month as a long bar, nearly all of it uptime, with a thin slice at the end as the budget, which incidents eat into until releases stop.*

## The idea

No service is perfectly reliable, and chasing 100 percent costs more than customers will notice. So you agree on a reliability target, a service level objective (SLO) such as "up 99.9 percent of the time", and treat the gap below perfect as a budget. While some is left, releases go ahead. Once it's spent, they slow or stop until reliability recovers. A written policy says ahead of time what "stop" means, and who can make an exception.

## Why a PM cares

- **How much failure customers will accept is a product question.** It turns on what they expect, what the service earns and what competitors offer. In Google's account, product and reliability teams set the target together.
- **It puts a number on caution.** "We can't afford failures" becomes a figure you can spend. A 99.9 percent target over 30 days leaves about 43 minutes of downtime.

## How to spot it

- Arguments about reliability end in "it depends who you ask", not a number.
- Nobody can tell you your service's target, or who agreed to it.
- Releases freeze after every incident, however small, or never freeze at all.

## What it does not say

It does not say all failures are equal. As Google's chapter notes, a privacy leak is far worse than a brief display glitch. Some failures, such as a double charge on a card, don't belong in a budget at all: treat them as hard lines.

**One question to carry:** How much failure would our customers accept for this service, and who agreed to that?

## Go deeper

**[Example Error Budget Policy](https://sre.google/workbook/error-budget-policy/), Google SRE Workbook (Appendix B)**

An appendix. Free at sre.google.

**Why trust it:** Google's site reliability engineers wrote it from their own practice, as a template: one company's policy, ready for you to adapt.

**What you'll get:** What a team agrees to do once the budget is spent, and what the exceptions are.
