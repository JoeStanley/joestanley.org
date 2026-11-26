---
title: See the System
layout: module
module: see-the-system
question: What's the system, and why does it behave this way?
setting: a ride-hailing app
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
    trust: "Experience. Meadows was a systems scientist and lead author of The Limits to Growth (1972). The ranking is her own judgment, and she calls it tentative herself."
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
    trust: "Experience. Cook was a physician and safety researcher at the University of Chicago. He gives you the points without the evidence behind them."
    only: "A better question to ask after a failure: \"what had to line up?\""
  - id: do
    kind: do
    title: Draw one stock, and log a change
    where: The Do, on this page, below.
    look: Who sees the level, and how late they see it.
  - id: check
    kind: check
    title: Check yourself
    where: The Check, on this page, below.
    look: The answers you missed, and why you missed them.

example:
  body: |
    **Stock:** drivers waiting for a background check, about 2,400 now.

    - **In:** about 900 a week finish their documents.
    - **Out:** about 750 a week cleared, and about 50 give up. Net: up 100 a week.

    Three months of tickets; the give-ups are guessed.

    **Who sees it:** ops, in the vendor's Monday report, a week late. Drivers see "pending." Riders see fewer cars, weeks later.

    **Last fix:** faster checks, paid for. A number, 12th of 12. Still growing.

    **Decision log:** drivers moving cities keep a clear check under a year old: about 150 a week. Expect the level to fall about 50 a week. 60 percent sure: some cities may require one. Look again March 1.
  good:
    - The flows in and out have counts and a source, so the level's rise follows from the arithmetic.
    - It says who sees the level and how late, which is where the delay hides.
    - The change aims at a rule, higher on the list than the last fix, and expects the slow fall a big stock gives.

check:
  - q: Your app clears more drivers' background checks each month than it did last year, yet the queue waiting for one keeps growing. What does that tell you?
    a: More is still coming in than going out. A stock rises whenever its inflow is larger than its outflow.
  - q: Own Your Role asked you to act where nobody assigned you. This module says the structure, not the people, drives what a system does. When does one person's push win, and when does the structure?
    against: own-your-role
    a: "Against the structure, a push wins for a while, then the system drifts back. So aim it at the structure itself: a goal, a rule, or who sees the feedback, all of which Meadows ranks above any number. That's where one person's push lasts."
  - q: A review of a failed release of the rider app names one person's skipped step as the root cause. Give two reasons from Cook to doubt it.
    a: A failure needs several faults to line up, so naming one explains little. And hindsight makes the danger look more obvious than it was at the time.
  - q: "**Beyond this module.** Your bathtub shows what piles up, and why. What can't a drawing tell you?"
    a: Where to act first. A drawing shows the structure, not which step holds the rest back, and finding that takes timing how long work waits at each one. [Find the Constraint](/pm/find-the-constraint/) has you do it.

deeper:
  - title: Thinking in Systems
    by: Donella Meadows, edited by Diana Wright
    where: A book.
    note: "Read chapters 1, 4 and 5: \"The Basics,\" \"Why Systems Surprise Us\" and \"System Traps . . . and Opportunities.\""
    trust: "Experience. It's Meadows's own primer on her field, from the lead author of The Limits to Growth."
    only: Chapter 1 teaches stocks, flows and loops with diagrams. Chapter 5 names common traps, such as chasing the wrong goal, and a way out of each.
  - title: The Field Guide to Understanding 'Human Error'
    by: Sidney Dekker
    where: A book.
    note: "Read chapter 1, \"Two Views of 'Human Error,'\" and chapter 5, \"Understanding Your Accident Model.\""
    trust: "Experience. Dekker is a safety scientist who also flew airliners, writing for people who investigate failures, and his guide is built on safety research."
    only: Cook's point at book length. Chapter 1 sets the bad-apple view of error against the view that error is a symptom of trouble in the system, and chapter 5 shows how your model of accidents decides what you'll find.
  - title: A Brief Introduction to Critical Systems Heuristics (CSH)
    by: Werner Ulrich (2005)
    url: https://wulrich.com/downloads/ulrich_2005f.pdf
    where: A paper.
    note: Free at wulrich.com. Read it whole, and keep its checklist of boundary questions nearby.
    trust: "An argument. Ulrich, a philosopher of social planning, developed the method, and this is his own account of it."
    only: Questions to put to any plan's boundary, from whose interests it serves to who speaks for the people it affects but doesn't involve.
  - title: Chernobyl
    by: written by Craig Mazin, directed by Johan Renck (HBO and Sky, 2019)
    where: A TV series.
    note: "{{< pm/voice \"chernobyl\" >}}"
    only: "Cook's question, put to a disaster: what had to line up? The show answers with a system built to hide its own flaw: \"No one in the room that night knew the shutdown button could act as a detonator.\""
---

## Why this matters

When something keeps going wrong, the first move is usually to find who caused it. It's the wrong first move, and seeing why is where product judgment starts. Look at the structure instead: what builds up, what fills and drains it, and what holds it in place. You've got two guides here. Donella Meadows, a systems scientist, ranks the places you can change a system, which she calls {{< pm/term "leverage-point" "leverage points" >}}. Richard Cook, a physician who studied accidents, argues that a failure in a complex system never has just one cause.

Where you draw the system's edge matters too, because it decides whose costs you'll see. Draw it around a ride-hailing app's support queue, and the riders who gave up before they ever filed a ticket fall outside it: the ones [Know Who It's For](/pm/know-who-its-for/) said you most need to hear. In her essay "Dancing With Systems," Meadows lists "Expand the boundary of caring" among her lessons: your company can't succeed, she writes, "if your workers fail."

[//]: # (short-path)

## Do

**Draw one stock (20 minutes).** Pick one thing that piles up in your team's work. On a ride-hailing app it might be drivers waiting for their background checks, lost-item reports or disputed fares. Draw it as a bathtub, with what flows in and what flows out. Three months of counts from your ticket tool will do, and estimates are fine if that's all you have. Note who sees the level, and how late they see it. Then take the last attempt to shrink the pile and find it on Meadows's list of twelve, near the top of her essay. Was it aimed at a number, or at something higher up?

**Reread one failure (10 minutes).** Take a missed date or a failed release on your team that got pinned on one cause. List three other things that had to be true for it to happen.

**For your decision log.** Write the change you'd make to the stock you drew, what you expect its level to do, and how sure you are. Add the date you'll look again.

{{< pm/example >}}
