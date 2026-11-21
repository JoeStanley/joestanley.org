# Module 1: See the System

*Built, and on the site.*

**The question:** What's the system here, and why does it behave this way?

About 80 minutes: 50 reading, 30 doing.

**If you only do one thing:** Read the card, then draw one thing that piles up in your own work as a bathtub.

## Last time

Two questions on Own Your Role. Answer in your head, then check. Own Your Role isn't rebuilt yet, so take these two as a preview of it.

You start a new role and you're handed a narrow scope. What do the best PMs do with it?

**Answer:** They accept it, then grow it without waiting to be told.

Engineers write the test before they write the code. What's the same move in a PM's work?

**Answer:** Deciding what success looks like before you start a role or an objective. A tool from one discipline carries over to another.

## Why this matters

When something keeps going wrong, the first move is usually to find who caused it. It's the wrong first move, and seeing why is where product judgment starts. Look at the structure instead: what builds up, what fills and drains it, and what holds it in place. You've got two guides here. Donella Meadows, a systems scientist, ranks the places you can change a system, which she calls leverage points. Richard Cook, a physician who studied accidents, argues that a failure never has just one cause.

## The short path

1. **Stocks, Flows and Feedback**

   2 minutes. One page.

   **Look for:** The picture. Most of Meadows's examples are versions of it.
2. **Donella Meadows, "Leverage Points", first half**

   24 minutes. An essay. Free at donellameadows.org. Stop at the section headed "6. The structure of information flows", which opens with a story about an electricity meter.
   - [Leverage Points: Places to Intervene in a System](https://donellameadows.org/archives/leverage-points-places-to-intervene-in-a-system/)

   **Look for:** Why numbers such as prices and standards come last of her twelve, even though they get most of the attention.

   **Why trust it:** Meadows was a systems scientist and lead author of The Limits to Growth (1972). The ranking is her own judgment from experience, and she calls it tentative herself.

   **What you'll get:** Twelve places to change a system, ranked, with examples.
3. **Donella Meadows, "Leverage Points", second half**

   16 minutes. The same essay, from the meter story to the end.

   **Look for:** Why the houses with the meter in the front hall used less electricity. Then her last section, on why the highest leverage is the hardest to use.

   **Why trust it:** Her politics show in the examples. Judge the reasoning on its own, whichever way that pulls you.

   **What you'll get:** Why information, rules and goals outrank numbers.
4. **Richard Cook, "How Complex Systems Fail"**

   8 minutes. Eighteen short points on one page. Free at how.complexsystems.fail.
   - [How Complex Systems Fail](https://how.complexsystems.fail/)

   **Look for:** Points 3, 7 and 8. A failure needs several small faults to line up, so one root cause explains little, and hindsight makes it all look obvious.

   **Why trust it:** Cook was a physician and safety researcher at the University of Chicago. He gives you the points without the evidence behind them.

   **What you'll get:** A better question after a failure. Not "who caused this?" but "what had to line up?"

## Do

**Draw one stock (20 minutes).** Pick one thing that piles up in your team's work: open defects, customers waiting to be onboarded, orders held for review. Draw it as a bathtub, with what flows in and what flows out. Three months of counts from your ticket tool will do, and estimates are fine if that's all you have. Note who sees the level, and how late they see it. Then take the last attempt to shrink the pile and find it on Meadows's list of twelve, near the top of her essay. Was it aimed at a number, or at something higher up?

**Reread one failure (10 minutes).** Take a missed date or a failed release on your team that got pinned on one cause. List three other things that had to be true for it to happen.

## Check yourself

Answer in your head, then check.

A clinic sees more patients each month than it did last year, yet its waiting list keeps growing. What does that tell you?

**Answer:** More is still coming in than going out. A stock rises whenever its inflow is larger than its outflow.

Why does Meadows rank putting an electricity meter where people can see it above changing a number?

**Answer:** It adds a feedback loop that wasn't there. People see what they use as they use it. A new number leaves the same people acting on the same information.

A review of a failed release names one person's skipped step as the root cause. Give two reasons from Cook to doubt it.

**Answer:** A failure needs several faults to line up, so naming one explains little. And hindsight makes the danger look more obvious than it was at the time.

## Go deeper: the full path

Optional, and not counted in the time above.

- ***Thinking in Systems*, Donella Meadows, edited by Diana Wright**

  A book of about 240 pages. Borrow it or buy it.

  Read chapters 1, 4 and 5: The Basics, Why Systems Surprise Us, and System Traps and Opportunities.

  **Why trust it:** Her primer for general readers, drafted in 1993. Colleagues edited and published it in 2008, after her death.

  **What you'll get:** Chapter 1 teaches stocks, flows and loops with diagrams. Chapter 5 names common traps, such as chasing the wrong goal, and a way out of each.

- ***The Wire*, created by David Simon (HBO, 2002 to 2008)**

  A TV series, 60 hour-long episodes over five seasons.

  Start with season 1, or jump to season 3. There a police major makes three zones where drug dealing is tolerated, and his district grows peaceful, until the institutions around him shut it down. In season 4, episode 9, a former detective now teaching math sees his old job in the new one: "You juke the stats, and majors become colonels. I've been here before."

  **What you'll get:** Structure driving behavior, at the scale of a city. The police, the drug trade, the port, city hall and the schools each run on their own rules, and the people inside them, doing what makes sense where they stand, keep each one making what nobody wants.

---

# Stocks, Flows and Feedback

*Concept card for Module 1, See the System.*

*Picture: The water in the tub is the stock. The tap and the drain are its flows. Feedback is the level changing how far someone opens the tap.*

## The idea

A stock is anything that builds up and can be counted or measured at one moment: water in a tub, money in an account, requests in a backlog. Flows fill it and drain it. A stock changes only through its flows, so it rises whenever more comes in than goes out. A feedback loop forms when the level changes one of its own flows, as when a full tub makes you close the tap.

A **balancing** loop pulls a stock toward a goal, as a thermostat does. A **reinforcing** loop pushes it further the way it's going, as interest does. Meadows's essay calls them negative and positive, which doesn't mean bad and good.

## Why a PM cares

- **You're judged on stocks, and you change them through flows.** A backlog, a defect count and customer trust are all stocks. To move one, find what fills it and what drains it.
- **Big stocks move slowly.** A backlog that took a year to build won't clear in a sprint, and promising that it will is how you lose a quarter.

## How to spot it

- A number that rises or falls steadily is a stock with unequal flows.
- A number that swings above and below its target is a balancing loop that reacts late, like server capacity that lurches between too much and too little.
- A number that grows faster and faster is a reinforcing loop.

## What it does not say

It does not say that drawing a system lets you predict or control it. Real systems hold many stocks and loops. The drawing shows you where to look.

**One question to carry:** What's piling up here, what fills it, what drains it, and who can see the level?

## Go deeper

**[Dancing With Systems](https://donellameadows.org/archives/dancing-with-systems/), Donella Meadows**

An essay, about 17 minutes. Free at donellameadows.org.

**Why trust it:** Meadows on the limits of her own field. It's advice from experience, not a study.

**What you'll get:** Fourteen habits for working with a system you can't fully understand or control.
