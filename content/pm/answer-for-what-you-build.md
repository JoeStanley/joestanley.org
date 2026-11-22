---
title: Answer for What You Build
layout: module
module: answer-for-what-you-build
question: Who benefits and who is harmed by what we build, and what's our share of the responsibility?
one_thing: Run a consequence scan on one feature you own, and write down one change you'd propose.
do_minutes: 35

last_time:
  - q: Your team still sends a weekly report nobody seems to read. Before you stop it, what do you find out?
    a: Why it started and what leans on it. Someone may still depend on it, which is Chesterton's point about the fence.
  - q: Why can a team that shares your picture of a situation act without asking you first?
    a: It knows the intent behind the task, so it can still act when the task goes stale. Boyd put orientation, that shared picture, at the center of his loop.

steps:
  - id: doteveryone
    kind: read
    title: 'Doteveryone, "Consequence Scanning"'
    minutes: 10
    where: A web page and a manual. Free at adalovelaceinstitute.org. Read the page, then the manual's steps for running a session.
    links:
      - text: "Consequence Scanning"
        url: https://www.adalovelaceinstitute.org/resource/doteveryone-consequence-scanning/
    look: The three questions you'll use in the Do, and how a session runs.
    trust: It's from the method's designers at Doteveryone, a responsible technology think tank that ran from 2015 to 2020. It describes a tool rather than testing one.
    only: A conversation to run with your team in under an hour, before a feature is built.
  - id: reichheld-markey
    kind: read
    title: 'Fred Reichheld and Rob Markey, "Blowing the whistle on bad profits"'
    minutes: 10
    where: An article. Free at bain.com.
    links:
      - text: "Blowing the whistle on bad profits"
        url: https://www.bain.com/insights/blowing-whistle-on-bad-profits
    look: "What they count as bad profits, \"profits earned at the expense of customer relationships\". Then ask how much of your product's revenue comes from value it created, and how much from making it hard to leave."
    trust: Two Bain consultants arguing for their own customer survey, so read it as a case for a method.
    only: The business case against capturing value, taking it from customers rather than creating it for them, ready for your next pricing review.
  - id: card-many-hands
    kind: card
    card: cards/many-hands
    minutes: 5
    look: The phrases people reach for to feel less responsible.
  - id: schneier
    kind: read
    title: 'Bruce Schneier, "Data Is a Toxic Asset, So Why Not Throw It Out?"'
    minutes: 10
    where: An essay. Free at schneier.com.
    links:
      - text: "Data Is a Toxic Asset, So Why Not Throw It Out?"
        url: https://www.schneier.com/essays/archives/2016/03/data_is_a_toxic_asse.html
    look: "Why he treats stored data as a liability. Then put one test to every field you collect: which decision will it change?"
    trust: "A security writer's opinion essay, first published by CNN: an argument, not a study."
    only: A reason to collect less that rests on risk.

check:
  - q: A change lifts hours watched on your streaming service by starting the next episode without asking. Has it created value?
    a: Ask whether viewers are better off, or only up later than they meant to be. If they'd switch it off given a plain choice, those hours were captured, not created.
  - q: To meet sales targets, Wells Fargo employees opened accounts customers hadn't asked for. Which idea from this module explains it, and which from Find the Constraint?
    a: "Many Hands: each employee could say they were only following the targets. And Goodhart's Law: once accounts opened became a target, the count stopped showing what customers wanted."
  - q: A teammate wants a new sign-up field "in case we need it". What do you ask?
    a: Which decision will it change? If none does yet, leave it out. Every field you keep is something to secure, and something to find when a customer asks you to erase it.

deeper:
  - title: Automating Inequality
    by: Virginia Eubanks
    where: A book.
    note: "Read chapter 4, \"The Allegheny Algorithm\", then chapter 2, \"Automating Eligibility in the Heartland\"."
    trust: "Eubanks is a political scientist at the University at Albany, and this is reporting with a point of view: she chose cases that let the families affected speak. The county answered her, its tool changed after the book, and evaluations since disagree on how fair it is."
    only: Who carries a system's mistakes, and who isn't in its data at all. Allegheny County's screening tool learned only from families who use public services, since families who pay privately for treatment never appear in its records.
  - title: Design Justice
    by: Sasha Costanza-Chock
    url: https://doi.org/10.7551/mitpress/12255.001.0001
    where: A book.
    note: "Free at direct.mit.edu, open access. Read the opening of the introduction, through the airport scanner and the network's principles, then chapter 2, \"Design Practices: 'Nothing about Us without Us'\"."
    trust: "Costanza-Chock was a research scientist at MIT and helps lead the Design Justice Network, whose principles the book sets out: an insider's case, argued from cases, and openly normative."
    only: "An airport scanner that flags a body for not matching the button the operator pressed, and who it fails most. Then who a team imagines as its user, and why \"Better for whom?\" is the question to put to every test."
  - title: Your Face Belongs to Us
    by: Kashmir Hill
    where: A book.
    note: Read it whole.
    trust: Hill is a New York Times technology reporter who broke the story of Clearview AI in 2020. It's reporting, not a study.
    only: A startup that built what Google and Facebook had held back, face search across billions of scraped photos, and sold it to police. Then a Black father in Detroit, arrested on a false match and held for nearly thirty hours.
  - title: "Pinto Fires and Personal Ethics: A Script Analysis of Missed Opportunities"
    by: Dennis Gioia (Journal of Business Ethics, 1992)
    url: https://doi.org/10.1007/BF00870550
    where: A journal article.
    trust: Gioia was Ford's recall coordinator in the early 1970s, and he writes about his own part in the Pinto case.
    only: A first-person account of how an ethical question never came up, because it wasn't part of how he understood the job.
  - title: The Good Place
    by: created by Michael Schur (NBC)
    where: A TV series.
    note: "A sitcom about moral philosophy. Watch \"The Book of Dougs\", in season 3. Nobody has gotten into the Good Place in more than 500 years. Long ago, one Doug gives his grandmother roses and earns 145 points. A modern Doug does the same and loses four, because his phone, his roses and the companies he paid each hurt someone he'll never see."
    only: "The Many Hands card's problem, with jokes: harm spread so thin across a supply chain that nobody in it feels responsible."
---

## Why this matters

Your choices land on people who were never in the meeting. On a delivery platform, small rules decide how many stops fit in a shift, which order waits when a van runs late, and what counts as delivered. Across millions of orders, a small rule becomes a large effect.

Some of those people live a world away. In 2017, Myanmar's military killed, raped and drove out Rohingya by the thousands, and [UN investigators](https://www.ohchr.org/sites/default/files/Documents/HRBodies/HRCouncil/FFM-Myanmar/A_HRC_39_64.pdf) called for its generals to be tried for genocide. Facebook, they found, had been "a useful instrument for those seeking to spread hate, in a context where, for most users, Facebook is the Internet." An assessment Facebook commissioned said it hadn't done enough, and Facebook promised more. Four years on, [Global Witness](https://globalwitness.org/en/campaigns/digital-threats/facebook-approves-adverts-containing-hate-speech-inciting-violence-and-genocide-against-the-rohingya/) submitted eight real examples of that hate speech to it as ads, in Burmese, and Facebook approved all eight. In 2023, Amnesty International found Meta's failures had contributed to abuses again, in Ethiopia's war. A fix announced after a disaster isn't proof the cause is gone.

You've met parts of this question already: whose costs fall outside a system's edge, in See the System; whom a stand-in measure misses, in Find the Constraint; who falls between two categories, in Mind the Seams. Here it's the whole module.

So ask two things of what you build. Who gains, and who pays? A product can earn by helping people or by making them hard to leave, and for a while the two look alike on a dashboard. Costs, too, can be designed away or passed on to parts of the system that are less visible or have less say, and both look like a win.

In life, there are rarely clear ethical matters of good and bad given to you in that manner. Instead, it's a thousand small choices of degree, like getting fitted for a prescription at the eye doctor. I will not tell you here what's right or wrong per se, that's for you to find your own line. But wherever you land, hold fast.

[//]: # (short-path)

## Do

**Scan one feature you own (25 minutes).** Pick a feature, such as a retry rule for failed card payments or a marketplace search ranking, and run a {{< pm/term "consequence-scanning" "consequence scan" >}} on it. On one page, answer the method's three questions in order:

1. What are the intended and unintended consequences? Name everyone affected, including the easiest to overlook, like the cardholder whose retried payment tips the account into overdraft. Then look where groups overlap. A harm that's rare for each group alone can be common for the people in both, which is what Kimberlé Crenshaw meant by {{< pm/term "intersectional" >}}.
2. Which positive consequences do you want to focus on?
3. Which do you want to mitigate? Beside each one, write who'd own the fix.

End with one change you'd propose. Afterwards, show it to someone in support and ask what you missed.

**Optional: list what the feature keeps (10 minutes).** List each data field it collects, next to the decision that uses it, and mark any field with no decision. Then pick one field. If a customer used their {{< pm/term "right-to-erasure" "right to erasure" >}}, could you find every copy, in the backups and at the companies you share it with?
