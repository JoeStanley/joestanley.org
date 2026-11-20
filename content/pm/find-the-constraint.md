---
title: Find the Constraint
layout: module
module: find-the-constraint
question: Where is the work actually stuck, and are we measuring the right thing?
one_thing: Play the dice game below, then count where work is waiting in your own team.
game: dice
do_minutes: 35

last_time:
  - q: In Donella Meadows's list of places to intervene in a system, which has more leverage, changing a number such as a price or a standard, or changing the system's goal?
    a: The goal. Meadows ranks numbers lowest of her twelve, because they rarely change how a system behaves. The goal sits third from the top.
  - q: Richard Cook says a major failure never has one root cause. Why not?
    a: It takes several small faults lining up, each of which looked harmless alone. Naming one cause says more about the need to blame than about how the failure happened.

steps:
  - id: dice
    kind: play
    title: Play the dice game
    minutes: 10
    where: It's on this page, just below this list.
    look: The line finishes less than its averages promise, and work piles up in the middle.
  - id: forte
    kind: read
    title: Tiago Forte, "Theory of Constraints 101"
    minutes: 13
    where: Three short posts. Free at fortelabs.com.
    links:
      - text: "101: Applying the Principles of Flow to Knowledge Work"
        url: https://fortelabs.com/blog/theory-of-constraints-101/
      - text: "102: The Illusion of Local Optima"
        url: https://fortelabs.com/blog/theory-of-constraints-102-local-optima/
      - text: "108: Identifying the Constraint"
        url: https://fortelabs.com/blog/theory-of-constraints-108-optimizing-the-constraint/
    look: Post 102 shows why keeping everyone busy makes delivery slower. Post 108 shows why a rule or a policy can be the most damaging constraint, and the easiest to change.
    trust: Forte runs a productivity training firm, so this is a practitioner retelling Goldratt, not Goldratt. You can check it against the novel on the full path.
    only: It carries the idea from the factory floor into knowledge work, a few minutes at a time.
  - id: card-steps
    kind: card
    card: cards/five-focusing-steps
    minutes: 2
    look: The order. Steps 2 and 3 cost little, and they come before any spending.
  - id: card-goodhart
    kind: card
    card: cards/goodharts-law
    minutes: 2
    look: What a target on one step does to that step's number, and to the whole flow.

check:
  - q: In the dice game every station averages 3.5 a round. Why does the line finish fewer than 3.5 a round?
    a: A station can only pass on what has reached it. A low roll starves everyone further down, and a high roll later is wasted when nothing's waiting. Bad luck gets passed on and good luck doesn't.
  - q: You speed up a step that isn't the constraint. What happens to delivery?
    a: Almost nothing. The extra work joins the queue in front of the constraint.
  - q: Your team hits its target for reviews completed per day, yet releases are no faster. Give two explanations from this module.
    a: Review may not be the constraint, so its gains wait in a queue further on. Or the target has changed what counts as a completed review, which is Goodhart's Law.

deeper:
  - title: The Goal
    by: Eliyahu Goldratt and Jeff Cox
    where: A novel of about 400 pages. Borrow it or buy it.
    note: "Short of time? Read the Boy Scout hike (chapters 13 to 15) and the chapter where the managers write out five steps (chapter 36), about an hour in all. Chapter numbers can differ by edition, so go by the scenes."
    trust: Goldratt introduced the theory of constraints in this 1984 novel, written with Jeff Cox.
    only: You watch a plant manager work out where his plant is stuck, one step at a time. That makes the steps stick in a way no summary does.
---

## Why this matters

When delivery is slow, the usual fix is to ask every step to go faster and to have each one report its own numbers. It rarely works. Your job is to find the one place where work waits longest, the {{< pm/term "constraint" >}}, because speeding up anywhere else won't speed up the whole. Knowing where a push will count is a large part of judgment. The idea is Eliyahu Goldratt's, and he called it the theory of constraints.

[//]: # (short-path)

## Do

**Map one flow (25 minutes).** Pick one kind of change your team ships again and again: a pricing update, a new report, a tweak to checkout. List every step from request to live, and who does each one. For your last five such changes, estimate the days spent waiting and the days spent being worked on at each step. Ticket dates and approval timestamps are enough, and memory will do for a first pass. Mark the step with the longest wait as your candidate constraint. Then ask whoever tracks delivery for your team: "Where does work wait longest, and what is it waiting for?"

**Optional: test your measures (10 minutes).** Make a three-column table: each number your team is judged on, the step it measures, and whether improving it would speed up the whole flow or only that step.
