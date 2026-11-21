---
title: See the System
layout: module
module: see-the-system
question: What's the system, and why does it behave this way?
one_thing: Read the card, then draw one thing that piles up in your own work as a bathtub.
do_minutes: 30

last_time:
  - q: Fred Brooks traded something away to save the schedule. What, and how?
    a: The system's conceptual integrity. He let 150 implementers write the specifications, which by his estimate added a year to debugging.
  - q: Engineers write the test before they write the code. What's the same move in a PM's work?
    a: Naming the destination first, "we're building this in order to ...", then working back to what would have to be true to get there.

steps:
  - id: card-stocks
    kind: card
    card: cards/stocks-flows-feedback
    minutes: 5
    look: The picture. Most of Meadows's examples are versions of it.
  - id: meadows-1
    kind: read
    title: Donella Meadows, "Leverage Points", first half
    minutes: 25
    where: An essay. Free at donellameadows.org. Stop at the section headed "6. The structure of information flows", which opens with a story about an electricity meter.
    links:
      - text: "Leverage Points: Places to Intervene in a System"
        url: https://donellameadows.org/archives/leverage-points-places-to-intervene-in-a-system/
    look: Why numbers such as prices and standards come last of her twelve, even though they get most of the attention.
    trust: Meadows was a systems scientist and lead author of The Limits to Growth (1972). The ranking is her own judgment from experience, and she calls it tentative herself.
    only: Twelve places to change a system, ranked, with examples.
  - id: meadows-2
    kind: read
    title: Donella Meadows, "Leverage Points", second half
    minutes: 20
    where: The same essay, from the meter story to the end.
    look: Why the houses with the meter in the front hall used less electricity. Then her last section, on why the highest leverage is the hardest to use.
    trust: The same essay, so the same reasons hold. Her politics show in the examples, so judge the reasoning apart from them.
    only: Why information, rules and goals outrank numbers.
  - id: cook
    kind: read
    title: Richard Cook, "How Complex Systems Fail"
    minutes: 10
    where: A short paper, eighteen points on one page. Free at how.complexsystems.fail.
    links:
      - text: "How Complex Systems Fail"
        url: https://how.complexsystems.fail/
    look: Points 3, 7 and 8. A failure needs several small faults to line up, so one root cause explains little, and hindsight makes it all look obvious.
    trust: Cook was a physician and safety researcher at the University of Chicago. He gives you the points without the evidence behind them.
    only: "A better question to ask after a failure: \"what had to line up?\""

check:
  - q: A clinic sees more patients each month than it did last year, yet its waiting list keeps growing. What does that tell you?
    a: More is still coming in than going out. A stock rises whenever its inflow is larger than its outflow.
  - q: Why does Meadows rank putting an electricity meter where people can see it above changing a number?
    a: It adds a feedback loop that wasn't there. People see what they use as they use it. A new number leaves the same people acting on the same information.
  - q: A review of a failed release names one person's skipped step as the root cause. Give two reasons from Cook to doubt it.
    a: A failure needs several faults to line up, so naming one explains little. And hindsight makes the danger look more obvious than it was at the time.

deeper:
  - title: Thinking in Systems
    by: Donella Meadows, edited by Diana Wright
    where: A book.
    note: "Read chapters 1, 4 and 5: \"The Basics\", \"Why Systems Surprise Us\" and \"System Traps . . . and Opportunities\"."
    trust: It's Meadows's own primer on her field, from the lead author of The Limits to Growth. Diana Wright edited it from her draft after her death.
    only: Chapter 1 teaches stocks, flows and loops with diagrams. Chapter 5 names common traps, such as chasing the wrong goal, and a way out of each.
  - title: The Field Guide to Understanding 'Human Error'
    by: Sidney Dekker
    where: A book.
    note: "Read chapter 1, \"Two Views of 'Human Error'\", and chapter 5, \"Understanding Your Accident Model\"."
    trust: Dekker is a safety scientist who also flew airliners, writing for people who investigate failures. It's a practitioner's guide built on safety research, not a study of its own.
    only: Cook's point at book length. Chapter 1 sets the bad-apple view of error against the view that error is a symptom of trouble in the system, and chapter 5 shows how your model of accidents decides what you'll find.
  - title: Chernobyl
    by: written by Craig Mazin, directed by Johan Renck (HBO and Sky, 2019)
    where: A TV series.
    note: "In episode 1, a dosimeter reads 3.6 roentgen, the top of its scale, and the deputy chief engineer takes the number as the level: \"Not great, not terrible.\" In episode 5, the trial walks back through the chain: a safety test signed off as done when it wasn't, a ten-hour delay that handed it to an untrained night shift, and a shutdown button whose rods had graphite tips, because \"It's cheaper.\""
    only: "Cook's question, put to a disaster: what had to line up? The show answers with a system built to hide its own flaw: \"No one in the room that night knew the shutdown button could act as a detonator.\" It sharpens some real officials into villains, so look past them to the chain."
---

## Why this matters

When something keeps going wrong, the first move is usually to find who caused it. It's the wrong first move, and seeing why is where product judgment starts. Look at the structure instead: what builds up, what fills and drains it, and what holds it in place. You've got two guides here. Donella Meadows, a systems scientist, ranks the places you can change a system, which she calls {{< pm/term "leverage-point" "leverage points" >}}. Richard Cook, a physician who studied accidents, argues that a failure in a complex system never has just one cause.

[//]: # (short-path)

## Do

**Draw one stock (20 minutes).** Pick one thing that piles up in your team's work: open defects, customers waiting to be onboarded, orders held for review. Draw it as a bathtub, with what flows in and what flows out. Three months of counts from your ticket tool will do, and estimates are fine if that's all you have. Note who sees the level, and how late they see it. Then take the last attempt to shrink the pile and find it on Meadows's list of twelve, near the top of her essay. Was it aimed at a number, or at something higher up?

**Reread one failure (10 minutes).** Take a missed date or a failed release on your team that got pinned on one cause. List three other things that had to be true for it to happen.
