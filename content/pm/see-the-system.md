---
title: See the System
layout: module
module: see-the-system
question: What's the system here, and why does it behave this way?
one_thing: Read the card, then draw one thing that piles up in your own work as a bathtub.
do_minutes: 30
last_time_note: Own Your Role isn't rebuilt yet, so take these two as a preview of it.

last_time:
  - q: You start a new role and you're handed a narrow scope. What do the best PMs do with it?
    a: They accept it, then grow it without waiting to be told.
  - q: Engineers write the test before they write the code. What's the same move in a PM's work?
    a: Deciding what success looks like before you start a role or an objective. A tool from one discipline carries over to another.

steps:
  - id: card-stocks
    kind: card
    card: cards/stocks-flows-feedback
    minutes: 2
    look: The picture. Most of Meadows's examples are versions of it.
  - id: meadows-1
    kind: read
    title: Donella Meadows, "Leverage Points", first half
    minutes: 24
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
    minutes: 16
    where: The same essay, from the meter story to the end.
    look: Why the houses with the meter in the front hall used less electricity. Then her last section, on why the highest leverage is the hardest to use.
    trust: Her politics show in the examples. Judge the reasoning on its own, whichever way that pulls you.
    only: Why information, rules and goals outrank numbers.
  - id: cook
    kind: read
    title: Richard Cook, "How Complex Systems Fail"
    minutes: 8
    where: Eighteen short points on one page. Free at how.complexsystems.fail.
    links:
      - text: "How Complex Systems Fail"
        url: https://how.complexsystems.fail/
    look: Points 3, 7 and 8. A failure needs several small faults to line up, so one root cause explains little, and hindsight makes it all look obvious.
    trust: Cook was a physician and safety researcher at the University of Chicago. He gives you the points without the evidence behind them.
    only: A better question after a failure. Not "who caused this?" but "what had to line up?"

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
    where: A book of about 240 pages. Borrow it or buy it.
    note: "Read chapters 1, 4 and 5: The Basics, Why Systems Surprise Us, and System Traps and Opportunities."
    trust: Her primer for general readers, drafted in 1993. Colleagues edited and published it in 2008, after her death.
    only: Chapter 1 teaches stocks, flows and loops with diagrams. Chapter 5 names common traps, such as chasing the wrong goal, and a way out of each.
  - title: The Wire
    by: created by David Simon (HBO, 2002 to 2008)
    where: A TV series, 60 hour-long episodes over five seasons.
    note: "Start with season 1, or jump to season 3. There a police major makes three zones where drug dealing is tolerated, and his district grows peaceful, until the institutions around him shut it down. In season 4, episode 9, a former detective now teaching math sees his old job in the new one: \"You juke the stats, and majors become colonels. I've been here before.\""
    only: Structure driving behavior, at the scale of a city. The police, the drug trade, the port, city hall and the schools each run on their own rules, and the people inside them, doing what makes sense where they stand, keep each one making what nobody wants.
---

## Why this matters

When something keeps going wrong, the first move is usually to find who caused it. It's the wrong first move, and seeing why is where product judgment starts. Look at the structure instead: what builds up, what fills and drains it, and what holds it in place. You've got two guides here. Donella Meadows, a systems scientist, ranks the places you can change a system, which she calls {{< pm/term "leverage-point" "leverage points" >}}. Richard Cook, a physician who studied accidents, argues that a failure never has just one cause.

[//]: # (short-path)

## Do

**Draw one stock (20 minutes).** Pick one thing that piles up in your team's work: open defects, customers waiting to be onboarded, orders held for review. Draw it as a bathtub, with what flows in and what flows out. Three months of counts from your ticket tool will do, and estimates are fine if that's all you have. Note who sees the level, and how late they see it. Then take the last attempt to shrink the pile and find it on Meadows's list of twelve, near the top of her essay. Was it aimed at a number, or at something higher up?

**Reread one failure (10 minutes).** Take a missed date or a failed release on your team that got pinned on one cause. List three other things that had to be true for it to happen.
