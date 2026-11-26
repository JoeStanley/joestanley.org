---
title: The Compass
layout: closing
# The two versions of the walked-through call (spec S21), in the order their buttons show; the first shows first.
walks:
  - id: product
    label: A customer-facing product
  - id: platform
    label: An internal platform
question: Which question does the call in front of you need?
do_minutes: 30
---

{{< pm/voice "compass-framing" "paragraph" >}}

[//]: # (compass)

## One call, walked through

Real calls need several questions at once. Here's one, walked through twice: once for a product customers use, and once for a platform other teams build on. Pick the one closer to your work.

{{< pm/walk-toggle >}}

{{< pm/walk "product" >}}
On [Own Your Role](/pm/own-your-role/)'s music streaming app: should you retire the old version of the app, the one that still runs on older phones?

Start with who it's for. Ask the people still on it about the last time they tried to update, not whether they'd mind ([Know Who It's For](/pm/know-who-its-for/)). Then look at the system. The old version's support tickets pile up like water in a tub ([See the System](/pm/see-the-system/)), and if the engineers who answer them are the ones every release waits on ([Find the Constraint](/pm/find-the-constraint/)), retiring it speeds up everything behind it.

Check what the evidence leaves out. The dashboard says few people still use the old version. [Weigh the Evidence](/pm/weigh-the-evidence/) would ask how that number was collected, whether the old version sends usage data at all, and who's on it: people who can't afford a new phone, or who were handed down an old one.

Ask what kind of door it is. Switching the old version off can be undone. But the data a feature creates outlives the feature ([Design for Change](/pm/design-for-change/)), and listeners' downloads and playlists, once lost, may not come back. Treat that part as a one-way door ([Decide and Set Direction](/pm/decide-and-set-direction/)), and give people a way to keep it before anything goes dark.

Here two questions collide. Know Who It's For says waiting is expensive. [Answer for What You Build](/pm/answer-for-what-you-build/) asks who pays: here, the people with the oldest phones and the least say, as Design for Change warned. Neither wins by rule. Ask whether the cost can be designed away rather than passed on: a longer notice, a web player that runs on old phones, an export for what they saved. If it can, retire the old version in small steps, on a date, with a guardrail for those listeners, such as how many stop listening altogether ([Change Safely](/pm/change-safely/)). If it can't, say so plainly, and decide with the cost in view.

Last, decide who hears it, and when ([Bring People With You](/pm/bring-people-with-you/)): the listeners on the old version, from the app, with a date, and the support team who'll answer them. Then log the call, with what you expect, how sure you are and the result that would make you reopen it ([Notice When You Are Wrong](/pm/notice-when-you-are-wrong/)).
{{< /pm/walk >}}

{{< pm/walk "platform" >}}
Now the same app from the inside. You run the service that keeps every listener's library, their saved songs and playlists, and the app teams build on it. Should you retire version 1 of its API, which a few teams' services still call?

Start with who it's for. Your customers are the teams that call it, so ask each about the last time they tried to move to version 2, and what stopped them ([Know Who It's For](/pm/know-who-its-for/)). Then trace each one back to the listeners it serves: a call behind every play counts for more than a script nobody remembers writing. Then look at the system. Version 1's pages to whoever's on call and its one-off fixes pile up ([See the System](/pm/see-the-system/)), and if that time is what your next release waits on ([Find the Constraint](/pm/find-the-constraint/)), retiring it speeds up everything behind it.

Check what the evidence leaves out. The logs say three services still call version 1. [Weigh the Evidence](/pm/weigh-the-evidence/) would ask what the logs can't see: a job that runs once a quarter, a partner's integration, a team that calls version 1 through a shared library without knowing it.

Ask what kind of door it is. Switching version 1 off can be undone. But the data a feature creates outlives the feature ([Design for Change](/pm/design-for-change/)): if version 1 records something version 2 doesn't, the reports and models built on it will have a gap that never fills. Treat that part as a one-way door ([Decide and Set Direction](/pm/decide-and-set-direction/)), and settle where that data goes first.

Here two questions collide. Know Who It's For says waiting is expensive. [Answer for What You Build](/pm/answer-for-what-you-build/) asks who pays: here, the team with the least time to migrate, and the listeners behind its feature. [Mind the Seams](/pm/mind-the-seams/) would add that the migration sits in the seam between your team and theirs, where it's easy for nobody to own it. Neither wins by rule. Ask whether the cost can be designed away rather than passed on: a shim that keeps version 1's calls working, a migration your team does for them, a later date. If it can, retire it in small steps, with a guardrail for each calling team, such as its error rate ([Change Safely](/pm/change-safely/)). If it can't, say so plainly, and decide with the cost in view.

Last, decide who hears it, and when ([Bring People With You](/pm/bring-people-with-you/)): each calling team, with a date, and whoever answers for the features they run. Then log the call, with what you expect, how sure you are and the result that would make you reopen it ([Notice When You Are Wrong](/pm/notice-when-you-are-wrong/)).
{{< /pm/walk >}}

## Do

**Review your decision log (20 minutes).** [Notice When You Are Wrong](/pm/notice-when-you-are-wrong/) had you mark each call right or wrong. Now read them all back, from [Know Who It's For](/pm/know-who-its-for/) on. For each one, write what you predicted, how sure you were, and what happened. This time, judge each call by what you knew when you made it, not by how it turned out: a good call can end badly, and poker players have a word for mixing up the two, "resulting" (Annie Duke, [*Thinking in Bets*](https://www.penguinrandomhouse.com/books/552885/thinking-in-bets-by-annie-duke/9780735216372/excerpt), chapter 1). Philip Tetlock, who studies forecasting, puts the next step in a line: ["make explicit probability judgments, score them against reality."](https://www.edge.org/conversation/philip_tetlock-how-to-win-at-forecasting) Of five calls you were 80 percent sure of, about four should have held. Mark the ones you can't judge yet, and look again in a month. Where were you sure and wrong? Where were you right for a reason that turned out not to matter? For each miss, find the module whose question would have changed the call, and write that question beside it.

**Walk one call of your own (10 minutes).** Walk a call in front of you now, the way the call above was walked. Which questions does it need, and where do two of them collide? Log it, with what you expect.

## Where to go from here

Come back to a module when its question keeps coming up in your work, and take its full path then.

Data ran through the course well beyond [Weigh the Evidence](/pm/weigh-the-evidence/). It shows what people did but not why ([Know Who It's For](/pm/know-who-its-for/)), it outlives the feature that made it ([Design for Change](/pm/design-for-change/)), and a model learns from data someone else gathered (the [Many Hands](/pm/cards/many-hands/) card). So carry three questions to any call that touches it: what data does this create, who depends on it, and what would it take to change it?

One judgment came back under several names: where to draw the line. Rule Zero drew it around your own job. [See the System](/pm/see-the-system/) drew it around a system, and asked whose costs fall outside it. [Mind the Seams](/pm/mind-the-seams/) drew it between teams and between the categories people are sorted into, and Design for Change around what's likely to change. Wherever you draw a line, ask what it leaves out.

### What the course leaves out

This course drew its own line too, and left much of the craft to others. When one of these is the work in front of you, start here. Each is free to read, though some sell courses beside it.

- **Discovery method,** the whole of it, from interviews to testing ideas: [Teresa Torres's guides](https://www.producttalk.org/product-discovery/), by the coach who drew the opportunity solution tree, and the GOV.UK Service Manual's [guides to user research](https://www.gov.uk/service-manual/user-research), usability testing among them.
- **Pricing and go-to-market:** the free material is thinner here. For pricing, [Catherine Tucker's MIT course notes](https://ocw.mit.edu/courses/15-818-pricing-spring-2010/pages/lecture-notes/), from 2010: start with lecture 2, on pricing to what a customer gets. For selling software, [Patrick McKenzie's guide for Stripe](https://stripe.com/guides/atlas/business-of-saas), which is also an ad.
- **Experiments:** [Ron Kohavi and Roger Longbotham's overview of A/B tests](https://exp-platform.com/encyclopediamldm/), short and recent, by two of the team behind Microsoft's experiments.
- **Design craft:** [Nielsen Norman Group's study guide to UX basics](https://www.nngroup.com/articles/ux-basics-study-guide/). Start with the ten usability heuristics.
- **Accessibility:** [the W3C's introduction to web accessibility](https://www.w3.org/WAI/fundamentals/accessibility-intro/), from the people who write the standard the laws point to.
- **Regulation:** for privacy, [the UK regulator's guide to data protection by design](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/accountability-and-governance/guide-to-accountability-and-governance/data-protection-by-design-and-by-default/), UK law, though the EU's rule on design is much the same. For AI in Europe, [the European Commission's service desk for the AI Act](https://ai-act-service-desk.ec.europa.eu/en). Wherever you work, ask your own lawyers early.
