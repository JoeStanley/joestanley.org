---
title: Decide and Set Direction
layout: module
module: decide-and-set-direction
question: Which decisions matter, whose are they, and what are we choosing not to do?
setting: a travel booking app
one_thing: Write three things your team won't do this quarter, each with a one-sentence reason.
do_minutes: 30

last_time:
  - q: A number on your dashboard moved last month. Before you act on it, what do you go and read?
    a: A few of the cases behind it. If what happened to those people doesn't match the number, the number isn't measuring what you think.
  - q: Why break a number down by more than one thing at once?
    a: A harm can be far worse where two lines cross than either line shows alone, as Gender Shades found for darker-skinned women.

steps:
  - id: bezos
    kind: read
    title: 'Jeff Bezos, "2015 Letter to Shareholders"'
    minutes: 5
    where: A shareholder letter. Free at sec.gov. Read the section headed "Invention Machine."
    links:
      - text: "2015 Letter to Shareholders"
        url: https://www.sec.gov/Archives/edgar/data/1018724/000119312516530910/d168744dex991.htm
    look: "Which decisions deserve the slow process: the \"one-way doors,\" hard or impossible to undo. Most decisions are two-way doors, and Bezos wants those made quickly, by people with good judgment or small groups."
    trust: "Experience. It's a chief executive's rule for his own company."
    only: "What it costs to run every decision through the slow process: \"slowness, unthoughtful risk aversion, failure to experiment sufficiently, and consequently diminished invention.\""
  - id: card-agency-coherence
    kind: card
    card: cards/agency-and-coherence
    minutes: 5
    look: What to hold strict, and when to take a decision away from a team.
  - id: harmel-law
    kind: read
    title: 'Andrew Harmel-Law, "Scaling the Practice of Architecture, Conversationally"'
    minutes: 5
    where: An article. Free at martinfowler.com. Read the section on the advice process.
    links:
      - text: "Scaling the Practice of Architecture, Conversationally"
        url: https://martinfowler.com/articles/scaling-architecture-conversationally.html
    look: "One rule and one qualifier: anyone can decide, after asking everyone the decision affects and people with expertise in it. The decider is \"in no way obliged to agree with the advice,\" but has to seek it out, listen and write it down."
    trust: "Experience. Harmel-Law is a technology principal at Thoughtworks, writing up a practice he's run."
    only: A way to spread decisions out and still know who's accountable.
  - id: rumelt
    kind: read
    title: 'Richard Rumelt, "The perils of bad strategy"'
    minutes: 15
    where: An article. Free at mckinsey.com.
    links:
      - text: "The perils of bad strategy"
        url: https://www.mckinsey.com/capabilities/strategy-and-corporate-finance/our-insights/the-perils-of-bad-strategy
    look: "DEC's senior team in 1992, asked for a consensus, settling on a sentence that chose nothing. Then his kernel of a strategy: a diagnosis, a guiding policy, and coherent actions."
    trust: "An argument. Rumelt is a strategy professor at UCLA, and he was in DEC's room himself. It's the short form of his book."
    only: "Two questions for any strategy you're handed: does it say what's going on, and does it rule anything out?"
  - id: do
    kind: do
    title: Write a kernel and a not-doing list, and log one no
    where: The Do, on this page, below. A conversation to check a fence can come later.
    look: Whether a reasonable colleague would argue for the opposite.
  - id: check
    kind: check
    title: Check yourself
    where: The Check, on this page, below.
    look: The answers you missed, and why you missed them.

example:
  body: |
    **Diagnosis:** families quit at business travelers' fare rules; half their support calls concern bags.

    **Guiding policy:** families first, one price they can trust.

    **Actions:** bags and seats in the fare; families seated together; fare rules behind "Details."

    **Not this quarter:**

    - Corporate travel policies for two accounts: nothing for families. Sales would argue for them: a real no, told in person Monday.
    - Loyalty redesign: families pay no less. The product lead tells marketing.
    - The expense export: business travelers only. Fence: built for one account, still its main user. Stops only if that account can do without; sales asks.

    **Decision log:** no corporate policies. Expect both to ask again, neither to leave. 70 percent sure; one renews in May. Check June 30.
  good:
    - The first no names who would argue for it, sales, which makes it a choice and not a goal.
    - "The export it would stop gets its fence checked first: who it was built for, who still uses it, and what would let it go."
    - The log bets on what the no will cost, and checks after the one renewal that could prove it wrong.

check:
  - q: Weigh the Evidence asked who's missing from your evidence before you lean on it. Here you decide on purpose, with what you have. When do you stop gathering and decide?
    against: weigh-the-evidence
    a: When more evidence wouldn't change the call, or when waiting costs more than being wrong. A two-way door can be decided on thin evidence and fixed later. A one-way door, such as a change to the loyalty points members have saved for years, earns the extra weeks.
  - q: A decision has stalled because five people each think they can say no. What do you change?
    a: "Get one person named to decide, with everyone else an adviser and no vetoes except the ones the law gives. If naming them isn't your call, ask the group, \"Who decides this?\""
  - q: Your team's strategy reads "Delight travelers with a fast, reliable app," and nobody objects. What's wrong with it?
    a: Nobody would argue for the opposite, so it isn't a choice. It's a goal, with no diagnosis or guiding policy behind it.
  - q: "**Beyond this module.** You've said no and logged it. What would make you change your mind?"
    a: A result you name now, before you want to be right. [Notice When You Are Wrong](/pm/notice-when-you-are-wrong/) calls it a stop rule, and has you review your decision log.

deeper_one:
  title: "Warfighting (MCDP 1)"
  why: "It's free, and its chapter 4 sets out commander's intent, the why that outlasts the task, as doctrine a whole service works by."
deeper:
  - title: What Is Strategy?
    by: Michael Porter (Harvard Business Review, 1996)
    url: https://hbr.org/1996/11/what-is-strategy
    where: A long article.
    note: "At hbr.org, which may ask you to subscribe. Read sections III, on trade-offs, and V, \"Rediscovering Strategy: The Failure to Choose,\" most closely."
    trust: "An argument. Porter's own short statement of his theory, drawn from company cases."
    only: "Straddling in full: Continental Lite copied Southwest while staying a full-service airline, and lost hundreds of millions of dollars."
  - title: Lean Software Development
    by: Mary and Tom Poppendieck
    url: https://ptgmedia.pearsoncmg.com/images/9780321150783/samplepages/0321150783.pdf
    where: A book.
    note: "Free at pearsoncmg.com, in the publisher's sample. Read chapter 3, \"Decide as Late as Possible.\""
    trust: 'An argument. It''s the book that brought the {{< pm/term "last-responsible-moment" >}}, a term from lean construction, to software teams.'
    only: "When to decide: hold off while waiting costs less than deciding wrong, and do the work that makes waiting possible."
  - title: Warfighting (MCDP 1)
    by: U.S. Marine Corps (1997)
    url: https://www.marines.mil/News/Publications/MCPEL/Electronic-Library-Display/Article/899837/mcdp-1/
    where: A book.
    note: "Free at marines.mil. Read it whole. Chapter 4, \"The Conduct of War,\" holds commander's intent and mission tactics."
    trust: "An argument. It's doctrine, an institution's experience written down, and credits John Boyd for the loop."
    only: "Commander's intent at its source. The task says what to do and the intent says why, and when the situation makes the task obsolete, \"the intent is more lasting and continues to guide our actions.\""
  - title: Ocean's Eleven
    by: directed by Steven Soderbergh, written by Ted Griffin (Warner Bros., 2001)
    where: A film.
    note: "Danny's briefing hands each of ten specialists one part of the job, and the plan says only how the parts fit. {{< pm/voice \"oceans-eleven\" >}}"
    only: "Each specialist decides how to do his own part. Watch, too, how much of what looks improvised was planned."
---

## Why this matters

A roadmap is a set of decisions, and on most teams many get made by default: by adding, by deferring, or by never deciding. Make them on purpose. {{< pm/term "cost-of-delay" "Cost of delay" >}}, from [Know Who It's For](/pm/know-who-its-for/), tells you what to do first. This module is about the rest: which decisions deserve care, such as the {{< pm/term "one-way-doors" "one-way doors" >}} that are hard to undo, and what you're choosing not to do. "The essence of strategy is choosing what not to do," as Michael Porter puts it. A travel app built both for business travelers who want every fare rule and for families who want one simple price serves neither well. Porter calls that {{< pm/term "straddling" >}}, and it's expensive.

Saying no to something your team already does has a catch. Find out first why it started and what leans on it. G. K. Chesterton made the point in 1929 with a fence across a road: don't clear it away until you can say why someone put it up.

Then ask whose decision it is. A few need a view of the whole, and most are better made by the people doing the work. Either way, name one person to decide, and if that isn't your call, ask who decides. Input shapes a decision, but it isn't a veto. If the call is yours, give your view last: Daniel Kahneman warns, in [a 2010 interview alongside Gary Klein](https://www.mckinsey.com/capabilities/strategy-and-corporate-finance/our-insights/strategic-decisions-when-can-you-trust-your-gut), that a leader's opinion sways a room the way the first guess at the coins in a jar sways the next. And think of the people it lands on who'll never be in the room. Werner Ulrich, from [See the System](/pm/see-the-system/)'s full path, asks: "Who is witness to the interests of those affected but not involved?"

Handing a decision out works only when the person deciding sees the situation as you do. John Boyd, a fighter pilot turned strategist, described every decision as a loop, his {{< pm/term "ooda-loop" "OODA loop" >}}: observe, orient, decide, act. It's often taught as a race to loop faster, but Boyd put the weight on orientation, the picture you act from. A team that shares yours can act on your {{< pm/term "commanders-intent" "intent" >}}, the why behind the task, when the task goes stale, without stopping to ask. It's [Own Your Role](/pm/own-your-role/)'s "in order to." And when you're the one handed a task, ask what it's in order to.

[//]: # (short-path)

## Do

**Write a kernel and a not-doing list (30 minutes).** Write one sentence for the diagnosis, the main challenge facing your product area, and one for the guiding policy, your approach to it. Add two or three actions that carry it out together. Those three parts make Rumelt's {{< pm/term "kernel-of-a-strategy" "kernel of a strategy" >}}. Then list three things you won't do this quarter, whether someone asked for them or your team does them now, each with a sentence tying the no to your diagnosis. Beside each, write who's waiting on it, and whether they'll hear it from you. List it now, but before you stop anything your team does, check the fence, even if that takes a conversation after the 30 minutes. Test each line: would a reasonable colleague argue for the opposite? If not, it isn't a choice yet. And if the list isn't yours to set, bring it as a proposal to whoever sets it.

**For your decision log.** Pick one line from your not-doing list. Write what you expect to happen because you said no, how sure you are, and the date you'll check.

{{< pm/example >}}

**Optional: give your advice on one decision (15 minutes).** Find a decision your team's engineers are still making, in a {{< pm/term "decision-record" "decision record" >}} or design doc; if none is open, ask your tech lead what's next. Write your advice as the {{< pm/term "advice-process" "advice process" >}} asks: what it changes for customers, and which trade-off matters most to them. Outside the 15 minutes, ask whoever's deciding if they'd like a product view, and send it before they decide. The call stays theirs.
