---
title: Find the Constraint
layout: module
module: find-the-constraint
question: Where is the work actually stuck, and are we measuring the right thing?
setting: a fitness app
one_thing: Play the dice game below to get the key point, then identify where your team's work waits.
game: dice
do_minutes: 35

last_time:
  - q: In Meadows's list of places to intervene in a system, which has more leverage, changing a number such as a price, or changing the goal?
    a: The goal. Meadows ranks numbers lowest of her twelve, because they rarely change how a system behaves. The goal sits third from the top.
  - q: Richard Cook says a major failure never has one root cause. Why not?
    a: It takes several small faults lining up, each of which looked harmless alone. Naming one cause says more about the need to blame than about how the failure happened.

steps:
  - id: dice
    kind: play
    title: Play the dice game
    minutes: 10
    where: It's on this page, just below this list.
    look: The line falls short of its averages, and work piles up midway.
  - id: forte
    kind: read
    title: Tiago Forte, "Theory of Constraints 101"
    minutes: 15
    where: Three short posts. Free at fortelabs.com.
    links:
      - text: "101: Applying the Principles of Flow to Knowledge Work"
        url: https://fortelabs.com/blog/theory-of-constraints-101/
      - text: "102: The Illusion of Local Optima"
        url: https://fortelabs.com/blog/theory-of-constraints-102-local-optima/
      - text: "108: Identifying the Constraint"
        url: https://fortelabs.com/blog/theory-of-constraints-108-optimizing-the-constraint/
    look: Post 102 shows why keeping everyone busy makes delivery slower. Post 108 shows why a rule or a policy can be the most damaging constraint, and the easiest to change.
    trust: "Experience. Forte runs a productivity training firm, so this is a practitioner retelling Goldratt, not Goldratt. You can check it against the novel on the full path."
    only: It carries the idea from the factory floor into knowledge work, a few minutes at a time.
  - id: card-steps
    kind: card
    card: cards/five-focusing-steps
    minutes: 5
    look: The order. Steps 2 and 3 cost little, and they come before any spending.
  - id: card-goodhart
    kind: card
    card: cards/goodharts-law
    minutes: 5
    look: What a target on one step does to that step's number, and to the whole flow.
  - id: do
    kind: do
    title: Map one flow, and log your constraint
    where: The Do, on this page, below. Asking whoever tracks delivery can come later.
    look: The step where work waits longest.
  - id: check
    kind: check
    title: Check yourself
    where: The Check, on this page, below.
    look: The answers you missed, and why you missed them.

example:
  body: |
    **Flow:** a new workout plan, the last five, in average days waiting and worked.

    - **Draft,** writer: 3 waiting, 2 worked.
    - **Coach review:** 9 waiting, 1 worked.
    - **Filming,** studio: 14 waiting, 2 worked. The studio books one week a month.
    - **Edit:** 2 waiting, 3 worked.
    - **Publish,** app team: 4 waiting, half a day worked.

    About 40 days in all, 8 of them work. Ticket dates and the studio calendar; publish from memory.

    **Candidate constraint:** filming.

    **Decision log:** if the studio books every two weeks, expect new plans live in about 33 days, not 40. 60 percent sure: five plans is a small sample, and one waited a month on its own. Find out after the next five, about May 15.
  good:
    - Each step's days are split into waiting and worked, so the waiting shows as most of the time.
    - It says where each number came from, and which one is from memory.
    - The log expects the whole flow to speed up, by a date, rather than the step's own number.

check:
  - q: In the dice game every station averages 3.5 a round. Why does the line finish fewer than 3.5 a round?
    a: A station can only pass on what has reached it. A low roll starves everyone further down, and a high roll later is wasted when nothing's waiting. Bad luck gets passed on and good luck doesn't.
  - q: See the System said a failure never has one cause. Here, one step holds the whole flow back. Which is it?
    against: see-the-system
    a: Each answers its own question. When something has gone wrong, look for the several causes that lined up. When work is slow, look for the one step that sets its pace, and once you've helped it, look at the whole flow again, since the constraint moves.
  - q: Your fitness app's team hits its target for workouts reviewed per day, yet new ones reach users no faster. Give two explanations from this module.
    a: Review may not be the constraint, so its gains wait in a queue further on. Or the target has changed what counts as a completed review, which is [Goodhart's Law](/pm/cards/goodharts-law/).
  - q: "**Beyond this module.** Your map shows where work waits inside your team. Where else could the constraint be?"
    a: "Outside it: at a handoff to another team, in an approval, or in a rule nobody remembers making. [Mind the Seams](/pm/mind-the-seams/) looks at what falls between teams."

deeper:
  - title: The Principles of Product Development Flow
    by: Donald Reinertsen
    where: A book.
    note: "Read chapter 2, \"The Economic View,\" on putting a price on delay, then chapter 3, \"Managing Queues,\" and chapter 4, \"Exploiting Variability.\""
    trust: "An argument. Reinertsen, a consultant, sets it out as numbered principles drawn from queueing theory and economics."
    only: Why queues are the hidden cost in product work, and why cutting variability, a lesson taken from factories, can cost more than it saves. Watch where he parts with Goldratt.
  - title: "Accelerate: The Science of Lean Software and DevOps"
    by: Nicole Forsgren, Jez Humble and Gene Kim
    url: https://itrevolution.com/wp-content/uploads/2022/06/ACC_excerpt.pdf
    where: A book.
    note: Read chapter 1, "Accelerate," and chapter 2, "Measuring Performance." Both are free in the publisher's excerpt.
    trust: "A review of studies. It rests on four years of survey research, from thousands of organizations. The answers are self-reported, and the teams all build software."
    only: "[Goodhart's Law](/pm/cards/goodharts-law/) in practice: velocity used to judge a team gets gamed. Then why near-full utilization sends lead times toward infinity, and the four delivery measures the authors picked instead."
  - title: The Goal
    by: Eliyahu Goldratt and Jeff Cox
    where: A novel.
    note: "Read it whole, or start with the Boy Scout hike (chapters 13 to 15) and the chapter where the managers write out the five steps (chapter 36)."
    only: Goldratt first set out the theory of constraints in this novel, in 1984. You follow a plant manager as he works out where his plant is stuck, one step at a time, and the steps are easier to remember once you've watched someone find them.
---

## Why this matters

When delivery is slow, as when a fitness app's new workouts take months to reach anyone, most teams ask every step to go faster and to report its own numbers. It rarely works. Only one step, what Eliyahu Goldratt called the {{< pm/term "constraint" >}}, holds the whole flow back, and work piles up in front of it, a stock like the one you drew in [See the System](/pm/see-the-system/). Find it, since speeding up anywhere else won't help. That goes for a model, too. One that drafts new workouts in minutes helps only if drafting is where the work waits. If the wait is a coach checking each one, you get more drafts piled up in front of the coach.

The danger while you work on it is [Goodhart's Law](/pm/cards/goodharts-law/). Once a number becomes a target, people find the cheapest way to hit it, so the constraint's number can hit its target while nothing more reaches users.

A number can mislead with nobody gaming it, too. An algorithm a US hospital used to pick patients for extra care took the cost of their care as a stand-in for how sick they were. Less had been spent on Black patients who were just as sick, so at any given score they were sicker than White patients, and too few of them were picked (Obermeyer and colleagues, 2019). Before you trust a stand-in, ask whether it tracks the real thing equally well for everyone.

[//]: # (short-path)

## Do

**Map one flow (25 minutes).** Pick one kind of change your team ships again and again. On a fitness app, that might be a new workout plan, a price change or a tweak to sign-up. List every step from request to live, and who does each one. For your last five such changes, estimate the days spent waiting and the days spent being worked on at each step. Ticket dates and approval timestamps are enough, and memory will do for a first pass. Mark the step with the longest wait as your candidate constraint. Outside the 25 minutes, ask whoever tracks delivery for your team: "Where does work wait longest, and what is it waiting for?"

**For your decision log.** Name your candidate constraint and what you expect delivery to do if it gets help. Say how sure you are, and when you'll find out.

{{< pm/example >}}

**Optional: test your measures (10 minutes).** Make a three-column table: each number your team is judged on, the step it measures, and whether improving it would speed up the whole flow or only that step.
