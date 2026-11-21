# Module 2: Find the Constraint

*Built, and on the site.*

**The question:** Where is the work actually stuck, and are we measuring the right thing?

About 62 minutes: 27 reading and playing, 35 doing.

**If you only do one thing:** Play the dice game below, then count where work is waiting in your own team.

## Last time

Two questions on See the System. Answer in your head, then check.

In Donella Meadows's list of places to intervene in a system, which has more leverage, changing a number such as a price or a standard, or changing the system's goal?

**Answer:** The goal. Meadows ranks numbers lowest of her twelve, because they rarely change how a system behaves. The goal sits third from the top.

Richard Cook says a major failure never has one root cause. Why not?

**Answer:** It takes several small faults lining up, each of which looked harmless alone. Naming one cause says more about the need to blame than about how the failure happened.

## Why this matters

When delivery is slow, the usual fix is to ask every step to go faster and to have each one report its own numbers. It rarely works. Your job is to find the one place where work waits longest, the constraint, because speeding up anywhere else won't speed up the whole. The idea is Eliyahu Goldratt's, and he called it the theory of constraints. Knowing where a push will count is a large part of judgment.

## The short path

1. **Play the dice game**

   10 minutes. It's on this page, just below this list.

   **Look for:** The line finishes less than its averages promise, and work piles up in the middle.
2. **Tiago Forte, "Theory of Constraints 101"**

   13 minutes. Three short posts. Free at fortelabs.com.
   - [101: Applying the Principles of Flow to Knowledge Work](https://fortelabs.com/blog/theory-of-constraints-101/)
   - [102: The Illusion of Local Optima](https://fortelabs.com/blog/theory-of-constraints-102-local-optima/)
   - [108: Identifying the Constraint](https://fortelabs.com/blog/theory-of-constraints-108-optimizing-the-constraint/)

   **Look for:** Post 102 shows why keeping everyone busy makes delivery slower. Post 108 shows why a rule or a policy can be the most damaging constraint, and the easiest to change.

   **Why trust it:** Forte runs a productivity training firm, so this is a practitioner retelling Goldratt, not Goldratt. You can check it against the novel on the full path.

   **What you'll get:** It carries the idea from the factory floor into knowledge work, a few minutes at a time.
3. **The Five Focusing Steps**

   2 minutes. One page.

   **Look for:** The order. Steps 2 and 3 cost little, and they come before any spending.
4. **Goodhart's Law**

   2 minutes. One page.

   **Look for:** What a target on one step does to that step's number, and to the whole flow.

## The dice game

Five people pass work down a line, left to right. Each round, everyone rolls a die in turn and passes on that many items, or everything they have if that is fewer. The first person never runs out.

A die averages 3.5, so over 20 rounds the averages promise 70 finished items.

*On the site the playable game sits here. Its words:*

Before you play, guess. How many will the line finish in 20 rounds? More than 70 / About 70 / Clearly fewer than 70.

Play 20 rounds. Then change the line, one move at a time, and play again.

- **All equal.** Every station rolls 1 to 6. *After a run:* Nobody did anything wrong. A low roll starves everyone further down the line, and a high roll later can't make it up, because there's nothing waiting to pass on.
- **Station 3 is slower.** Station 3 now rolls 1 to 4. The others still roll 1 to 6. *After a run:* Look at the pile in front of station 3. A pile that keeps growing in front of one step is how you find a constraint.
- **Speed up station 1.** Station 3 still rolls 1 to 4. Station 1 gets faster and rolls 3 to 8. *After a run:* One lucky run can mislead, so compare the averages. A faster station 1 adds about one finished item (46.5 against 45.4) and more than doubles the work left waiting.
- **Speed up station 3 instead.** Station 1 is back to 1 to 6. Station 3 gets the help and rolls 3 to 8. *After a run:* Compare the averages again. This setup finishes 54.4, against 45.4 with a slow station 3. Help at the constraint is the help that reaches the customer.

### One recorded run, all stations equal

| Station | 1 | 2 | 3 | 4 | 5 |
| --- | --- | --- | --- | --- | --- |
| Total of its rolls | 72 | 66 | 66 | 74 | 82 |
| Actually passed on | 72 | 62 | 54 | 54 | 54 |
| Waiting in front of it at the end | 0 | 10 | 8 | 0 | 0 |

The line finished 54 of the 70 the averages promised. Stations 4 and 5 rolled well above average, and it didn't help: they had nothing extra to pass on. Simulated 400,000 times, this line finishes 51.7 on average.

### What to take away

1. Equal capacity doesn't deliver the average, because each step can only pass on what has reached it.
2. The pile shows you where the constraint is.
3. Speed added anywhere else mostly becomes a queue, not output.

The game comes from the Boy Scout hike in *The Goal*, which is on the full path below.

## Do

**Map one flow (25 minutes).** Pick one kind of change your team ships again and again: a pricing update, a new report, a tweak to checkout. List every step from request to live, and who does each one. For your last five such changes, estimate the days spent waiting and the days spent being worked on at each step. Ticket dates and approval timestamps are enough, and memory will do for a first pass. Mark the step with the longest wait as your candidate constraint. Then ask whoever tracks delivery for your team: "Where does work wait longest, and what is it waiting for?"

**Optional: test your measures (10 minutes).** Make a three-column table: each number your team is judged on, the step it measures, and whether improving it would speed up the whole flow or only that step.

## Check yourself

Answer in your head, then check.

In the dice game every station averages 3.5 a round. Why does the line finish fewer than 3.5 a round?

**Answer:** A station can only pass on what has reached it. A low roll starves everyone further down, and a high roll later is wasted when nothing's waiting. Bad luck gets passed on and good luck doesn't.

You speed up a step that isn't the constraint. What happens to delivery?

**Answer:** Almost nothing. The extra work joins the queue in front of the constraint.

Your team hits its target for reviews completed per day, yet releases are no faster. Give two explanations from this module.

**Answer:** Review may not be the constraint, so its gains wait in a queue further on. Or the target has changed what counts as a completed review, which is Goodhart's Law.

## Go deeper: the full path

Optional, and not counted in the time above.

- ***The Goal*, Eliyahu Goldratt and Jeff Cox**

  A novel of about 400 pages. Borrow it or buy it.

  Short of time? Read the Boy Scout hike (chapters 13 to 15) and the chapter where the managers write out five steps (chapter 36), about an hour in all. Chapter numbers can differ by edition, so go by the scenes.

  **What you'll get:** Goldratt first set out the theory of constraints in this novel, in 1984. You watch a plant manager work out where his plant is stuck, one step at a time, and that makes the steps stick in a way no summary does.

---

# The Five Focusing Steps

*Concept card for Module 2, Find the Constraint.*

*Picture: Work piles up in front of the narrowest point. The five steps deal with that point first, then repeat.*

## The idea

Every system has one part that limits what the whole can deliver: its constraint. Eliyahu Goldratt's five steps tell you what to do about it, in this order:

1. **Identify** the constraint.
2. **Exploit** it: get the most from it as it is.
3. **Subordinate** every other step to it.
4. **Elevate** it: invest to raise its capacity.
5. **Repeat** from step 1 once the constraint has moved, and don't let old habits become the new constraint.

## Why a PM cares

- **Effort anywhere else buys little.** Speed up any other step and you mostly build a longer queue in front of the constraint.
- **The order saves money.** Steps 2 and 3 cost little. Step 4 costs budget, so it comes last. Ask for more people first and you've skipped the cheaper steps.
- **The constraint may be a rule.** An approval board that meets monthly, or a sign-off only one person can give, limits delivery as surely as a short-staffed team. It's often easier to change, too.

## How to spot it

- Work piles up in front of one step, while the steps after it wait for something to do.
- Everyone's busy and delivery is still slow.
- Knowledge work hides its queues in inboxes, tickets and approval calendars. Count the work in progress waiting at each step, using ticket or approval dates.

## What it does not say

It does not say the other steps don't matter. It says their pace should follow the constraint's. And it's a lens, not a proven law: a 2009 literature review found it had yet to show its effect in academic studies.

**One question to carry:** If this step did twice as much tomorrow, would customers get anything sooner?

## Go deeper

**[The Five Focusing Steps](https://www.tocinstitute.org/five-focusing-steps.html), Theory of Constraints Institute**

A short page. Free at tocinstitute.org.

**Why trust it:** The institute trains and advises on Goldratt's method, so read it as an advocate's account.

**What you'll get:** What each step asks you to do, in a few lines per step.

---

# Goodhart's Law

*Concept card for Module 2, Find the Constraint.*

*Picture: Before a number is a target, it moves with the thing you care about. Afterwards the number can keep climbing on its own.*

## The idea

Once people are judged by a number, they adapt to it, and it stops telling you what it used to. The economist Charles Goodhart made the point in 1975, about UK monetary policy. The well-known wording, "When a measure becomes a target, it ceases to be a good measure," is the anthropologist Marilyn Strathern's, from 1997.

## Why a PM cares

- **A target changes behavior before it changes results.** Tell a delivery team to raise its on-time rate, and it can start promising later dates. The number improves while parcels arrive no sooner.
- **OKRs make it easy.** A key result often ends in a bare number, and a bare number invites the cheapest way to reach it. When you write one, put the intent beside the number.
- **Local targets hide the constraint.** A target on one step, such as reviews completed per day, can lift that step's number while the whole flow stays slow.

## How to spot it

- A number jumps soon after it becomes a target, while complaints, rework or escalations don't improve.
- People can tell you how to hit the number, but not what it was meant to show.
- Definitions drift. What counts as "resolved" or "on time" quietly narrows or loosens.

## What it does not say

It does not say measures are bad, or that every target fails. The usual remedy is several measures, not none. Pair a speed measure with a quality check: the on-time rate with how far out the promised date was, say.

**One question to carry:** If people hit this number in the cheapest way open to them, would the customer still be better off?

## Go deeper

**[Categorizing Variants of Goodhart's Law](https://arxiv.org/abs/1803.04585), David Manheim and Scott Garrabrant (2018)**

A research paper. Free at arxiv.org.

**Why trust it:** It's a research preprint, so treat it as a careful argument and not a settled finding.

**What you'll get:** It separates the different ways a measure can fail, so you can tell which one you're looking at.
