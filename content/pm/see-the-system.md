---
title: See the System
layout: module
module: see-the-system
question: What's the system, and why does it behave this way?
one_thing: Read the card, then draw one thing that piles up in your own work as a bathtub.
do_minutes: 30

last_time:
  - q: A customer says they'd use a new feature "all the time." What do you ask instead?
    a: About the last time the problem came up, what they did about it and what it cost them. What they did is evidence, and what they say they'd do is a forecast.
  - q: On a grocery app, an adult child orders for an aging parent. Whose problem is a bad substitution, and why does it matter which of them you hear from?
    a: The parent's, who eats it, though the child pays and is the one who writes in. A team that hears only from the buyer drifts toward the buyer.

steps:
  - id: card-stocks
    kind: card
    card: cards/stocks-flows-feedback
    minutes: 5
    look: The picture. Most of Meadows's examples are versions of it.
  - id: meadows-1
    kind: read
    title: Donella Meadows, "Leverage Points," first half
    minutes: 25
    where: An essay. Free at donellameadows.org. Stop at the section headed "6. The structure of information flows," which opens with a story about an electricity meter.
    links:
      - text: "Leverage Points: Places to Intervene in a System"
        url: https://donellameadows.org/archives/leverage-points-places-to-intervene-in-a-system/
    look: Why numbers such as prices and standards come last of her twelve, even though they get most of the attention.
    trust: Meadows was a systems scientist and lead author of The Limits to Growth (1972). The ranking is her own judgment from experience, and she calls it tentative herself.
    only: Twelve places to change a system, ranked, with examples.
  - id: meadows-2
    kind: read
    title: Donella Meadows, "Leverage Points," the rest
    continues: meadows-1
    minutes: 20
    where: The same essay, from the meter story to the end.
    look: Why the houses with the meter in the front hall used less electricity. Then her last section, on why the highest leverage is the hardest to use.
    only: Why information, rules and goals outrank numbers.
  - id: cook
    kind: read
    title: Richard Cook, "How Complex Systems Fail"
    minutes: 10
    where: A short paper of key points. Free at how.complexsystems.fail.
    links:
      - text: "How Complex Systems Fail"
        url: https://how.complexsystems.fail/
    look: Points 3, 7 and 8. A failure needs several small faults to line up, so one root cause explains little, and hindsight makes it all look obvious.
    trust: Cook was a physician and safety researcher at the University of Chicago. He gives you the points without the evidence behind them.
    only: "A better question to ask after a failure: \"what had to line up?\""

check:
  - q: A clinic sees more patients each month than it did last year, yet its waiting list keeps growing. What does that tell you?
    a: More is still coming in than going out. A stock rises whenever its inflow is larger than its outflow.
  - q: Own Your Role asked you to act where nobody assigned you. This module says the structure, not the people, drives what a system does. When does one person's push win, and when does the structure?
    against: own-your-role
    a: "Against the structure, a push wins for a while, then the system drifts back. So aim it at the structure itself: a goal, a rule, or who sees the feedback, all of which Meadows ranks above any number. That's where one person's push lasts."
  - q: A review of a failed release names one person's skipped step as the root cause. Give two reasons from Cook to doubt it.
    a: A failure needs several faults to line up, so naming one explains little. And hindsight makes the danger look more obvious than it was at the time.
  - q: "**Beyond this module.** Your bathtub shows what piles up, and why. What can't a drawing tell you?"
    a: Where to act first. A drawing shows the structure, not which step holds the rest back, and finding that takes timing how long work waits at each one. Find the Constraint has you do it.

deeper:
  - title: Thinking in Systems
    by: Donella Meadows, edited by Diana Wright
    where: A book.
    note: "Read chapters 1, 4 and 5: \"The Basics,\" \"Why Systems Surprise Us\" and \"System Traps . . . and Opportunities.\""
    trust: It's Meadows's own primer on her field, from the lead author of The Limits to Growth.
    only: Chapter 1 teaches stocks, flows and loops with diagrams. Chapter 5 names common traps, such as chasing the wrong goal, and a way out of each.
  - title: The Field Guide to Understanding 'Human Error'
    by: Sidney Dekker
    where: A book.
    note: "Read chapter 1, \"Two Views of 'Human Error,'\" and chapter 5, \"Understanding Your Accident Model.\""
    trust: Dekker is a safety scientist who also flew airliners, writing for people who investigate failures. It's a practitioner's guide built on safety research, not a study of its own.
    only: Cook's point at book length. Chapter 1 sets the bad-apple view of error against the view that error is a symptom of trouble in the system, and chapter 5 shows how your model of accidents decides what you'll find.
  - title: A Brief Introduction to Critical Systems Heuristics (CSH)
    by: Werner Ulrich (2005)
    url: https://wulrich.com/downloads/ulrich_2005f.pdf
    where: A paper.
    note: Free at wulrich.com. Read it whole, and keep its checklist of boundary questions nearby.
    trust: Ulrich, a philosopher of social planning, developed the method, so this is his own account of it, not a test of how well it works.
    only: Questions to put to any plan's boundary, from whose interests it serves to who speaks for the people it affects but doesn't involve.
  - title: Chernobyl
    by: written by Craig Mazin, directed by Johan Renck (HBO and Sky, 2019)
    where: A TV series.
    note: "A terrifyingly gripping narrative of the Chernobyl disaster, split in three main stages: the event, the brilliance and sacrifice needed to solve it, and the investigation after. And through it all, the structural incentives that not only led to the original problem, but informed all that followed."
    only: "Cook's question, put to a disaster: what had to line up? The show answers with a system built to hide its own flaw: \"No one in the room that night knew the shutdown button could act as a detonator.\""
---

## Why this matters

When something keeps going wrong, the first move is usually to find who caused it. It's the wrong first move, and seeing why is where product judgment starts. Look at the structure instead: what builds up, what fills and drains it, and what holds it in place. You've got two guides here. Donella Meadows, a systems scientist, ranks the places you can change a system, which she calls {{< pm/term "leverage-point" "leverage points" >}}. Richard Cook, a physician who studied accidents, argues that a failure in a complex system never has just one cause.

Where you draw the system's edge matters too, because it decides whose costs you'll see. Draw it around your support team's queue, and the customers who gave up before they ever filed a ticket fall outside it: the ones Know Who It's For said you most need to hear. In another essay, "Dancing With Systems," Meadows lists "Expand the boundary of caring" among her lessons: your company can't succeed, she writes, "if your workers fail."

[//]: # (short-path)

## Do

**Draw one stock (20 minutes).** Pick one thing that piles up in your team's work: open defects, customers waiting to be onboarded, orders held for review. Draw it as a bathtub, with what flows in and what flows out. Three months of counts from your ticket tool will do, and estimates are fine if that's all you have. Note who sees the level, and how late they see it. Then take the last attempt to shrink the pile and find it on Meadows's list of twelve, near the top of her essay. Was it aimed at a number, or at something higher up?

**Reread one failure (10 minutes).** Take a missed date or a failed release on your team that got pinned on one cause. List three other things that had to be true for it to happen.

**For your decision log.** Write the change you'd make to the stock you drew, what you expect its level to do, and how sure you are. Add the date you'll look again.
