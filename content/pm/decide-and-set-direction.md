---
title: Decide and Set Direction
layout: module
module: decide-and-set-direction
question: Which decisions matter, whose are they, and what are we choosing not to do?
setting: a travel booking app
one_thing: Write three things your team won't do this quarter, each with a one-sentence reason.
do_minutes: 35

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
    trust: "Experience. Harmel-Law is a technology principal at Thoughtworks, writing up a practice he's run with teams."
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

check:
  - q: Weigh the Evidence asked who's missing from your evidence before you lean on it. Here you decide on purpose, with what you have. When do you stop gathering and decide?
    against: weigh-the-evidence
    a: When more evidence wouldn't change the call, or when waiting costs more than being wrong. A two-way door can be decided on thin evidence and fixed later. A one-way door, such as a change to the loyalty points members have saved for years, earns the extra weeks.
  - q: A decision has stalled because five people each think they can say no. What do you change?
    a: "Get one person named to decide, with everyone else an adviser and nobody holding a veto. If naming them isn't your call, ask the group, \"Who decides this?\""
  - q: Your team's strategy reads "Delight travelers with a fast, reliable app," and nobody objects. What's wrong with it?
    a: Nobody would argue for the opposite, so it isn't a choice. It's a goal, with no diagnosis or guiding policy behind it.
  - q: "**Beyond this module.** Once you've chosen, what's left to do?"
    a: Finding out whether you chose well, early enough to change course. Notice When You Are Wrong takes that up, starting from your decision log.

deeper:
  - title: What Is Strategy?
    by: Michael Porter (Harvard Business Review, 1996)
    url: https://hbr.org/1996/11/what-is-strategy
    where: A long article.
    note: "At hbr.org, which counts free articles and may ask you to subscribe. Read section III, on trade-offs, and section V, \"Rediscovering Strategy: The Failure to Choose,\" most closely."
    trust: "An argument. It's a Harvard Business School professor's own short statement of his theory, drawn from company cases."
    only: "Straddling in full: Continental Lite copied Southwest while staying a full-service airline, and lost hundreds of millions of dollars."
  - title: Lean Software Development
    by: Mary and Tom Poppendieck
    url: https://ptgmedia.pearsoncmg.com/images/9780321150783/samplepages/0321150783.pdf
    where: A book.
    note: "Free at pearsoncmg.com, in the publisher's sample. Read chapter 3, \"Decide as Late as Possible.\""
    trust: "An argument. It's the book that brought the last responsible moment, a term from lean construction, to software teams."
    only: "When to decide: hold off while waiting costs less than deciding wrong, and do the work that makes waiting possible. \"Procrastinating is not the same as making decisions at the last responsible moment,\" they add."
  - title: Warfighting (MCDP 1)
    by: U.S. Marine Corps (1997)
    url: https://www.marines.mil/News/Publications/MCPEL/Electronic-Library-Display/Article/899837/mcdp-1/
    where: A book.
    note: "Free at marines.mil. Read it whole. Chapter 4, \"The Conduct of War,\" holds commander's intent and mission tactics."
    trust: "An argument. It's doctrine, an institution's experience written down, and its notes credit John Boyd for the loop and for implicit communication."
    only: "Commander's intent at its source. The task says what to do and the intent says why, and when the situation makes the task obsolete, \"the intent is more lasting and continues to guide our actions.\""
  - title: Science, Strategy and War
    by: Frans Osinga
    url: https://hdl.handle.net/1887/4211793
    where: A book.
    note: "Free at Leiden University, as the doctoral thesis it grew from. Read chapter 7: the part on \"Organic Design for Command and Control,\" then from \"The Essence of Winning and Losing\" to \"Beyond the rapid OODA loop idea.\""
    trust: "A study. Osinga, a Dutch Air Force F-16 pilot turned strategy scholar, works through Boyd's own briefings slide by slide, in a thesis Routledge later published."
    only: Why Boyd's loop is about orientation, not speed, and why a team that shares one can act on intent without being told what to do.
  - title: Ocean's Eleven
    by: directed by Steven Soderbergh, written by Ted Griffin (Warner Bros., 2001)
    where: A film.
    note: "Danny's briefing hands each of ten specialists one part of the job, and the plan says only how the parts fit. {{< pm/voice \"oceans-eleven\" >}}"
    only: "Each specialist decides how to do his own part. Watch, too, how much of what looks improvised was planned."
---

## Why this matters

A roadmap is a set of decisions, and on most teams many of them get made by default: by adding, by deferring, or by never deciding. Make them on purpose. That means working out which decisions deserve care, such as the {{< pm/term "one-way-doors" "one-way doors" >}} that are hard to undo, and saying what you're choosing not to do. "The essence of strategy is choosing what not to do," as Michael Porter puts it. A travel app built both for business travelers who want every fare rule and for families who want one simple price serves neither well. Porter calls that {{< pm/term "straddling" >}}, and it's expensive.

Saying no to something your team already does has a catch. Find out first why it started and what leans on it. G. K. Chesterton made the point in 1929 with a fence across a road: don't clear it away until you can say why someone put it up.

Then ask whose decision it is. A few decisions need a view of the whole, and most are better made by the people doing the work. Either way, name one person to decide. If that isn't your call, ask who decides. Input shapes a decision, but it isn't a veto. When a view makes no sense to you, get curious about why someone holds it, as Gary Klein advises. If the call is yours, give your view last: Daniel Kahneman warns that a leader's opinion sways a room, the way the first guess at the coins in a jar sways the next (Kahneman and Klein, 2010). And think of the people it lands on who'll never be in the room. Werner Ulrich, from See the System's full path, puts it as a question: "Who is witness to the interests of those affected but not involved?"

Handing a decision out works only when the person deciding sees the situation as you do. John Boyd, a fighter pilot who became a military strategist, described every decision as a loop, his {{< pm/term "ooda-loop" "OODA loop" >}}: observe, orient, decide, act. It's often taught as a race to loop faster. His own stress was on orientation, the picture you act from, since "orientation shapes the way we observe, the way we decide, the way we act." A team that shares your picture can act on your {{< pm/term "commanders-intent" "intent" >}}, the why behind the task, when the task goes stale. It's the "in order to" of Own Your Role, given with each task. That's where the team's tempo comes from: it doesn't have to stop and ask.

[//]: # (short-path)

## Do

**Write a kernel and a not-doing list (25 minutes).** Write one sentence for the diagnosis, the main challenge facing your product area, and one for the guiding policy, your approach to it. Add two or three actions that carry it out together: with them, that's Rumelt's {{< pm/term "kernel-of-a-strategy" "kernel of a strategy" >}}. Then list three things you won't do this quarter, whether someone asked for them or your team does them now, each with a sentence tying the no to your diagnosis. Beside each, write who it leaves waiting, and whether they'll hear it from you. Before you stop anything your team does now, find out why it started and what leans on it, like the fence above. That may take a conversation after the 25 minutes. Test each line: would a reasonable colleague argue for the opposite? If not, it isn't a choice yet. And if the list isn't yours to set, bring it as a proposal to whoever sets it.

**For your decision log.** Pick one line from your not-doing list. Write what you expect to happen because you said no, how sure you are, and the date you'll check.

**Optional: take apart a stalled decision (10 minutes).** Pick a decision from last quarter that stalled. Who had to be consulted, and who could say no? Was there one named decider, and a {{< pm/term "decision-record" "decision record" >}}? Write two lines on what the {{< pm/term "advice-process" "advice process" >}} would have changed.
