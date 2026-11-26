---
title: Notice When You Are Wrong
layout: module
module: notice-when-you-are-wrong
question: How do you find out you're wrong, early enough to change course?
setting: sensors that monitor factory equipment
one_thing: In your next plan, write down one way it could be wrong and the early signal you'd watch for.
do_minutes: 30

last_time:
  - q: Autoplay lifts hours watched on a video app. Before you call it a win, who do you look for?
    a: Whoever pays for it, such as the viewer up later than they meant to be. A product can earn by helping people or by making it hard for them to leave, and autoplay may be doing the second.
  - q: Everyone on a launch could say "the business asked for it." What's your share?
    a: You're one of the many hands. If what you did was a cause, and you could have done otherwise, part of it is yours. Name who owns each harm you can foresee before it lands.

steps:
  - id: batista
    kind: read
    title: 'Ed Batista, "Racing Up the Ladder of Inference"'
    minutes: 10
    where: A blog post. Free at edbatista.com.
    links:
      - text: "Racing Up the Ladder of Inference"
        url: https://www.edbatista.com/2014/02/racing-up-the-ladder-of-inference.html
    look: "The simplest way back down: find the rung you're on, pause and drop a step. At a belief, say, you'd \"clarify the meaning we're imposing upon the data at hand.\" Judgments feel like facts because you climb so fast."
    trust: "Experience. Batista is an executive coach who taught for years at Stanford's business school. The ladder is Chris Argyris's, so this is a practitioner retelling it."
    only: Questions to ask yourself in a meeting before you act on a conclusion.
  - id: card-double-loop-learning
    kind: card
    card: cards/double-loop-learning
    minutes: 5
    look: The difference between fixing the method and questioning the goal, and how Product X's bad news got cut down on the way up.
  - id: edmondson
    kind: read
    title: 'Amy Edmondson, "How Fearless Organizations Succeed"'
    minutes: 15
    where: An article. Free at strategy-business.com.
    links:
      - text: "How Fearless Organizations Succeed"
        url: https://www.strategy-business.com/article/How-Fearless-Organizations-Succeed
    look: "What psychological safety isn't. People say what they see, and the bar stays high: \"It is not about becoming 'comfortable' at work.\""
    trust: "An argument. Edmondson is the Harvard Business School professor whose research on teams made the idea widely known, and this excerpt from her book draws on company cases."
    only: What lets bad news reach you, from the researcher behind the idea.
  - id: do
    kind: do
    title: Run a premortem, and review your log
    where: The Do, on this page, below. Asking the people who'd see it break can come later.
    look: The reasons you'd usually keep to yourself.
  - id: check
    kind: check
    title: Check yourself
    where: The Check, on this page, below.
    look: The answers you missed, and why you missed them.

example:
  body: |
    **It's June, and the bearing alert failed.** Why, by how likely and how bad:

    - Technicians tuned it out after a week of false alarms. High, high.
    - It fired too late to book a repair. Medium, high.
    - Older pumps read hot all summer. Medium, medium.
    - Plant managers took it as a check on their crews. Low, high.
    - The threshold was set to look good in the demo. Medium, medium.

    **Top risk:** false alarms.

    **Stop rule, agreed with the operations director:** watch the share of alerts marked "nothing found." Look on March 15. Over half, and it pauses at both pilot plants to be retuned.

    **Log review:** 3 right, 2 wrong, 4 not known yet. Two dates passed without a look.
  good:
    - Its reasons include the awkward ones, like the threshold set for the demo.
    - Each reason is rated twice, for how likely and how bad, so the top risk isn't only the scariest.
    - The stop rule has a signal, a date and a result, and someone who can stop the work agreed to it.

check:
  - q: The dashboard shows alerts at one plant taking twice as long to clear as anywhere else, and the planning doc now says, "That plant's technicians don't take the alerts seriously." Which rung is that sentence on, and what takes it back down?
    a: "The third rung, a belief. Go back down to the data: which alerts, on which shifts, and what else is different there. It may come down to two technicians covering a whole shift, through a week of false alarms."
  - q: Technicians' time to clear alerts is flat. One lead coaches them to clear alerts faster. Another asks whether clearing fast is what keeps the machines running. Which is the double loop?
    a: The second. The first changes the method to hit the same goal. Only the second asks whether the goal is right.
  - q: Decide and Set Direction asks you to decide on purpose and keep to a not-doing list. Here you keep looking for how you're wrong. When do you hold a call, and when do you reopen it?
    against: decide-and-set-direction
    a: Hold it until a signal you named before the bet shows up, then reopen it. A bad day that isn't that signal is no reason to.
  - q: "**Beyond this module.** You've found out a call was wrong, but it's your manager's call, or your team's. What now?"
    a: Say so in a way they can weigh, and if they still go the other way, commit to it. [Bring People With You](/pm/bring-people-with-you/) takes that up, with disagreeing and committing.

deeper:
  - title: The Fearless Organization
    by: Amy C. Edmondson
    where: A book.
    note: "Read chapter 1, \"The Underpinning,\" chapter 4, \"Dangerous Silence,\" and chapter 7, \"Making it Happen.\""
    trust: "An argument. It's the researcher behind the idea writing for managers, from her studies and from company cases. A 2017 review, pooling more than a hundred samples, backed the idea's links to learning and to performance."
    only: What it costs when people stay quiet about what they see, and what a leader can do so they speak up.
  - title: "Overcoming Organizational Defenses: Facilitating Organizational Learning"
    by: Chris Argyris
    where: A book.
    note: Read chapters 4 to 6. Schön, his partner in this work, wrote *The Reflective Practitioner*, on [Own Your Role](/pm/own-your-role/)'s full path.
    trust: "An argument. Argyris developed these ideas, with Donald Schön, over decades of work inside companies, and he writes for managers from field cases and his own interventions."
    only: The ladder, the double loop and the left-hand column from their source, with the routines that keep a team from saying what it sees. Chapter 4 has a manager's left-hand column, chapter 5 ends on the ladder, and chapter 6 is double-loop learning.
  - title: Arrival
    by: directed by Denis Villeneuve, written by Eric Heisserer from Ted Chiang's "Story of Your Life" (Paramount, 2016)
    where: A film.
    note: "Early on, the linguist Louise Banks tells a colonel that \"kangaroo\" first meant \"I don't understand,\" then admits the story isn't true. Later the aliens' answer translates as \"offer weapon,\" and she warns the room, \"We don't know if they understand the difference between a weapon and a tool.\" China reads it as \"use weapon\" and breaks off talks, other nations go dark, and China gives the aliens 24 hours to leave."
    only: A whole government's conclusion resting on one translated word, the ladder of inference climbed in a day, with the world at stake.
---

## Why this matters

Every plan rests on assumptions, and some of yours are probably wrong today: that technicians will trust a new alert, say, or that a sensor's readings mean what you think. You don't know which yet, and you won't find out by feel. As the writer [Kathryn Schulz puts it](https://www.ted.com/talks/kathryn_schulz_on_being_wrong), being wrong "feels like being right." So stop asking how to show you're right, and ask how you'd find out you're wrong.

The cheapest way is to decide what wrong looks like before you start. [Change Safely](/pm/change-safely/) had you name a guardrail and the level at which you'd stop, before a rollout. Do the same for every bet. Before the new alert ships, write down the result you expect and by when, say technicians acting on most alerts within a month, and the result that would make you stop or change course. That's a stop rule. Once the bet is live you'll want to be right, so a line drawn afterward tends to move. A stop rule also catches the bet that never quite fails and never quite works, and drifts on for a year.

Silence isn't proof that you're right. Low numbers can mean people stopped telling you. US colleges publish their counts of sexual assault on campus, under a law called the Clery Act. *Data Feminism*, on [Weigh the Evidence](/pm/weigh-the-evidence/)'s full path, tells what happened when students set those counts beside anonymous surveys: the truth was "closer to the reverse" of what the counts suggested. Many of the colleges with higher counts were the ones putting more into support for survivors, where survivors had more reason to come forward. So when technicians stop reporting false alarms, ask them why before you count it as good news.

Finding out also takes habits, in your thinking and your team's. Start by climbing down from a conclusion to what you saw. Chris Argyris's {{< pm/term "ladder-of-inference" "ladder of inference" >}} has four rungs, as Ed Batista tells it: you select some of the data, interpret it, form beliefs from it, and act. Say the dashboard shows technicians dismissing a third of the new alerts. By lunch someone has read that as warnings nobody acted on, decided the technicians don't trust the alerts, and proposed pulling the feature. Climbing down means asking which alerts were dismissed, at which sites, and what happened to the machines afterward.

Question the goal as well as the method. The thermostat on [See the System](/pm/see-the-system/)'s card is a balancing loop, and single-loop learning is the same loop at work: it corrects the method and never asks about the goal. And make it safe for bad news to reach you, which researchers call {{< pm/term "psychological-safety" "psychological safety" >}}: thank whoever brings it before you ask what they'd do about it. Once you've found something, telling the people who decide is the next module, [Bring People With You](/pm/bring-people-with-you/).

[//]: # (short-path)

## Do

**Run a {{< pm/term "premortem" >}} on your own work (20 minutes).** It's a technique of Gary Klein's, whose advice on hunches you met in [Weigh the Evidence](/pm/weigh-the-evidence/). Imagine your main initiative has failed, badly: say, a new alert meant to warn technicians before a machine breaks down. Write down every plausible reason it failed, especially the ones you'd usually keep to yourself. Asking what did go wrong, not what might, turns doubting the plan into helping with it. If you run it with your team, have everyone write alone before anyone talks, so nobody's list shapes anyone else's. Rate each one low, medium or high, for how likely it is and how much damage it would do, as Simon Brown's [risk-storming](https://riskstorming.com/) does. For the top one, write a stop rule, and agree it with whoever can stop the work: the signal you'll watch, the date you'll look, and the result that would make you stop or change course. Outside the 20 minutes, ask the people who'd see it break first, such as a field technician, and the support lead who'd hear from the customers it failed: "If this failed, what would you bet the reason was?"

**Review your decision log.** Read back the calls you've logged since [Know Who It's For](/pm/know-who-its-for/), and mark each one right, wrong or not known yet. Where a date has passed, did you look when you said you would? Where you were sure and wrong, what did you miss, and what signal would have told you sooner? Then log this premortem's top risk, with its stop rule.

{{< pm/example >}}

**Optional: write a {{< pm/term "left-hand-column" "left-hand column" >}} (10 minutes).** The exercise is Chris Argyris and Donald Schön's. Take a meeting where you held back a concern. Down the right of a page, write what was said, and down the left, what you thought but didn't say. Take one left-hand thought down the ladder, and rewrite it as a sentence you could have said, starting from what you saw.
