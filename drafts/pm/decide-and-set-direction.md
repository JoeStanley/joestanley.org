## Why this matters

A roadmap is a set of decisions, and on most teams many get made by default: by adding, by deferring, or by never deciding. Make them on purpose. That means telling which decisions deserve care, weighing what each option gains and costs, and saying what you're choosing not to do. It comes late because it draws on the earlier modules, from seeing the system to knowing what's costly to change.

## Short path (about two hours of reading, plus an hour for the exercises)

The deck is a 514-page set of workshop slide notes written for software architects, not a book, so don't try to read it through. Read only the pages named here, and only the parts named. Any term you don't know is defined under "Terms you will meet", below. If you split the path across two sittings, stop after step 4.

1. The **Strategy as Forsaking** concept card (10 minutes).
2. Deck p. 154 (5 minutes). Read the left-hand column beneath the slide, headed "Strategy: About Not To": short quotes from Porter, Bezos and Rumelt on choosing. Skip the rest.
3. Michael Porter, ["What Is Strategy?"](https://hbr.org/1996/11/what-is-strategy) (*Harvard Business Review*, November to December 1996), the whole article (about 45 minutes). It's on hbr.org and may need a subscription or a library login. No access? The Rumelt article in step 5 makes the same case for choosing. Give most of your attention to section III, "A Sustainable Strategic Position Requires Trade-offs", and section V, "Rediscovering Strategy: The Failure to Choose".
4. Deck p. 177 (5 minutes). Look at the map on the slide: Porter's picture of how Southwest Airlines' choices support each other. Then read the last paragraph beneath it, which begins "Notice that the use of a standardized 737 fleet". Skip the rest.
5. Deck p. 164, then Rumelt's article (25 minutes). On p. 164, read the three columns beneath the slide: Rumelt's diagnosis, guiding policy and coherent action. Skip the rest. Then read Richard Rumelt, ["The perils of bad strategy"](https://www.mckinsey.com/capabilities/strategy-and-corporate-finance/our-insights/the-perils-of-bad-strategy) (*McKinsey Quarterly*, 2011), about 15 minutes. Free at mckinsey.com.
6. Deck pp. 82 and 104 (10 minutes). On p. 82, read the quote on the slide, then the last two paragraphs beneath it, beginning "Each option considered" and "While we're at it". On p. 104, read the three questions on the slide and the note on the right that begins "decision (n.) from decidere". Skip the rest of both pages.
7. Deck pp. 111 and 112 (10 minutes). On p. 111, read the numbered tips under "Attending to Irreversible, Consequential Decisions". On p. 112, read the short "Reversible Decisions" paragraph and its two takeaways. Skip the rest.
8. The **Last Responsible Moment** concept card (10 minutes).
9. Deck p. 236 (5 minutes). Read the "Guidelines" list on the right, and the paragraph at the bottom left that begins "A principle is worth stating". Skip the rest.

## Full path

The full path adds to the short path, and all of it takes roughly 11 hours. If you have two more hours, spend them here: Rumelt's chapters 4 and 5 (about 80 minutes), then deck pp. 79 to 88 (about 45 minutes).

- Richard Rumelt, *Good Strategy Bad Strategy: The Difference and Why It Matters* (Crown Business, 2011), chapter 3, "Bad Strategy", chapter 4, "Why So Much Bad Strategy?", and chapter 5, "The Kernel of Good Strategy" (about two hours). Chapter 4 opens with a senior team at Digital Equipment Corporation that couldn't choose a direction.
- Decisions: deck pp. 79 to 88 (making a decision explicit, with a one-page record template on p. 88), pp. 89 to 103 (trade-offs, with a Spotify example on pp. 90 to 93) and pp. 105 to 107 (structured group conversations such as force field analysis), about 2 hours. Then pp. 108 to 110, 113 to 117 and 119 to 129 (which decisions matter, irreversibility, the last responsible moment, and "time span of discretion" on p. 121), about 85 minutes.
- Strategy and the landscape: deck pp. 146 to 163 (why strategy matters to system design; differentiation, moats and switching costs on pp. 155 to 159), about an hour; pp. 165 to 181 (a worked diagnosis, Wardley's strategy cycle, strategy at every level, and the whole Southwest example), about 65 minutes; pp. 182 to 201 (context maps, the business model canvas and Wardley maps), about an hour; pp. 203 to 214 (technology radars, futures and scenarios), about 40 minutes.
- Principles: deck pp. 215 to 228 (what principles are and how they narrow the decision space; start with p. 224, a template that includes the arguments against a principle, and p. 227), about 50 minutes. For the engineering view: pp. 69 to 78 (complexity, and how constraints restrict and enable), about 35 minutes, and pp. 229 to 242 (published sets of design principles), about 45 minutes.

## Terms you will meet

- **Strategy:** a set of choices about where you'll focus and how you'll win there, including what you will not do.
- **Trade-off:** a choice where getting more of one thing means accepting less of another.
- **Operational effectiveness:** Porter's term for doing the same activities as rivals, but better: faster, cheaper, with fewer errors. You need it, but rivals can copy it, so it isn't a strategy.
- **Strategic position:** Porter's term for a distinct choice of which customers, needs or channels you serve, and how.
- **Fit:** how a company's activities support each other, so the whole is harder to copy than any one part.
- **Diagnosis, guiding policy and coherent action:** Rumelt's three parts of a strategy, which he calls its kernel. What is going on; the overall approach, which rules many actions out; and coordinated steps that carry it out.
- **Dog's dinner and blue-sky objectives:** two kinds of bad strategic objective Rumelt names (deck p. 153). The first is a jumbled list of things to do; the second restates a wish with no route to it.
- **One-way and two-way doors:** Jeff Bezos's terms for decisions that can't be undone and decisions that can (deck pp. 111 and 112).
- **Decision record:** a short note of one significant decision: its context, the decision, its status and its consequences (deck p. 88). Engineers call it an architecture decision record (ADR), and the format works for product decisions too.
- **Principle:** a standing agreement that guides many later decisions. A useful one has a counterargument that someone could reasonably hold (deck p. 236).
- **Cost of change:** what it would take to undo or redo a decision later. See Module 4, Design for Change.

## What to look for

- **Operational effectiveness is not strategy.** In section I, Porter separates doing the same things better from choosing to do different things. Goals like faster delivery or fewer defects are the first kind. Pursue them, but don't count them as a choice.
- **Trade-offs come from real incompatibility.** Section III gives three sources: reputation, the activities themselves, and the limits of coordination. On deck p. 177, notice that the single aircraft type behind Southwest's low costs also left it exposed when that aircraft had problems.
- **A guiding policy rules things out.** On deck p. 164, Rumelt's guiding policy narrows the field of possible actions, and a vision with no method isn't one. His kernel starts with a diagnosis, and you can tell a diagnosis as a story too; the SCR card covers that.
- **Match the care to the door.** Deck pp. 111 and 112 build on Module 4's cost of change: go fast on decisions you can undo, and slow down for the ones that are hard to undo and high in consequence. Where you can, make a decision reversible, for example by piloting a new checkout flow in one market before it goes to all of them.
- **Name what you're avoiding, and what you rejected.** Deck p. 104 asks what your group is avoiding talking about. Write down the options you rejected, and why (p. 82). It makes the choice visible, and it saves you from arguing it again.

## Apply it to your own work

1. Write your kernel and a draft not-doing list in about 25 minutes. Start with one sentence for the diagnosis (the main challenge facing your product area) and one for the guiding policy (your overall approach to it), then list two or three coordinated actions (deck p. 164). Next, list three things you've been asked for and wouldn't do this quarter, each with one sentence tying the "no" to your diagnosis. Treat the list as a draft to take to your manager, because you may not have the authority to say no on your own. Then test each line: would a reasonable colleague argue for the opposite? If nobody would, it isn't a choice yet.
2. Sort five decisions by how hard they are to undo, in about 20 minutes. Take five decisions you made recently or face now, and place each on a two-by-two grid: easy or hard to undo, low or high consequence (deck p. 111). Which ones got heavy process even though they were easy to undo, and which hard-to-undo ones were rushed? A first pass from what you already know is fine. For a technical choice, check with a tech lead. You could open with "If we got this wrong, what would it take to undo it in six months?"
3. Record one decision with the options you rejected, in about 20 minutes. Pick a decision you face now and write it up on one page, using the template on deck p. 88: context, decision, status and consequences. Include at least three options (p. 82), and give each rejected option one sentence on why it lost. Then share the page with the person who owns the decision, or with your manager, so the "no" gets explained once, in writing.

## Check your own thinking

The shift this module is after is from "how do we fit all of this in?" to "what are we choosing not to do, and why?" Here's a way to test yourself. After your next planning session, count the requests you declined with a written reason tied to your diagnosis, plus the ones you deferred with both a date and a reason. If the count is zero, every request got a yes or a silent maybe. If you'd like a sounding board, take your kernel and your not-doing list to your manager or a mentor.

> Deck page references are to Ruth Malan's System Design and Software Architecture workshop notes, February to March 2025 edition. This guide is an independent companion; it has not been reviewed or endorsed by Ruth Malan.

# Strategy as Forsaking

## The idea

Strategy is what you choose to give up, and why. Michael Porter's "What Is Strategy?" (*Harvard Business Review*, 1996) argues that a lasting position rests on trade-offs: some activities can't be combined, so choosing one means forsaking another. Richard Rumelt's *Good Strategy Bad Strategy* (2011) traces much bad strategy to being unable to choose: every interest survives, and the plan turns into a list.

## Why a PM should care

- **What you leave off a roadmap is part of the plan.** In Porter's words, "the essence of strategy is choosing what not to do", and a clear choice tells staff how to make daily calls. A written not-doing list does that for your team. Without one, the roadmap becomes a jumbled list of objectives (Rumelt, deck p. 153).
- **Straddling is expensive.** Porter's case is Continental Lite, which copied parts of Southwest's low-cost model while staying a full-service airline, and lost hundreds of millions of dollars. The product version is one analytics tool for analysts who want every control and executives who want one chart. It serves neither group well.
- **Growth is the usual pressure.** Porter singles out the wish to grow as the most damaging force on a strategy. Each added segment or feature looks cheap alone, but together they erase the position.
- **A no protects the work you must do.** On a developer platform you can't skip security fixes, promised uptime or announced migrations, and every discretionary yes competes with them. A yes written into a public API or a customer contract is a one-way door, a decision you can't easily undo (deck p. 111), so the cheapest no comes before the commitment.

## How to spot it at work

- The roadmap grows every quarter, and nothing ever comes off it.
- Requests never get declined, only parked as "later", with no date and no reason.
- Two goals that can't both win are each labeled top priority, and the clash only shows up in delivery.
- The strategy statement could belong to any team, and nobody would argue for its opposite.

## What it does not say

It does not make improvement optional: Porter calls operational effectiveness, doing the same things better, necessary but not sufficient. Not every tension is a trade-off, either. Until you hit a real limit you can often improve both, so check that first (Donald Reinertsen, quoted on deck p. 94). And you forsake options, not obligations: a public service has to meet accessibility standards, though how it meets them is still a choice.

## One question to carry into your work

What's your team choosing not to do this quarter, and could you give the reason for each in one sentence?

## Go deeper

- Porter, ["What Is Strategy?"](https://hbr.org/1996/11/what-is-strategy) (*Harvard Business Review*, 1996), section III on trade-offs and section V, "Rediscovering Strategy: The Failure to Choose".
- Rumelt, ["The perils of bad strategy"](https://www.mckinsey.com/capabilities/strategy-and-corporate-finance/our-insights/the-perils-of-bad-strategy) (*McKinsey Quarterly*, 2011), on a senior team that couldn't choose. Free at mckinsey.com.
- Rumelt, *Good Strategy Bad Strategy* (2011), chapter 4, "Why So Much Bad Strategy?", and chapter 5, "The Kernel of Good Strategy".
- Deck p. 154 (Porter and Rumelt on what not to do), p. 177 (Southwest's activity system) and p. 104 (the root of "decision" means to cut off).

> Deck page references are to Ruth Malan's System Design and Software Architecture workshop notes, February to March 2025 edition, a 514-page set of slide notes; read only the pages cited. This card is an independent companion; it has not been reviewed or endorsed by Ruth Malan.

# Last Responsible Moment

## The idea

The last responsible moment is the point where not deciding takes away an important option: a path you could still take, but don't have to. Mary and Tom Poppendieck made it a tool in *Lean Software Development: An Agile Toolkit* (2003), and they note that the Lean Construction Institute coined the term. In cost terms: wait as long as waiting costs less than deciding wrong, keep your options open in the meantime, and decide before the cost of waiting overtakes the cost of deciding.

## Why a PM should care

- **Your roadmap is a sequence of decisions.** For each open decision, ask what depends on it and what's risky to defer (deck p. 117). Pull forward the decisions others rest on, and push out the ones you still need to learn about.
- **Deciding early by default locks in guesses.** Fixing scope, vendors or designs at kickoff feels responsible, but that's when you know the least you ever will. The Poppendiecks treat premature commitment as a design failure.
- **Deciding late by default is no better.** Once the moment has passed, the choice gets made for you: by a deadline, a supplier's lead time, or a release that leaves without you (deck p. 115).
- **The clock is often outside your team.** An app store's review queue, the start of a school year and a customer's contract renewal all set the moment from outside. Work back from dates like these, so the calendar doesn't decide for you.

## How to spot it at work

- A decision "made" at kickoff gets quietly reopened every few sprints, because nobody had the facts back then.
- The team waits for final requirements that never arrive, and the deadline decides instead.
- A vendor or platform choice is rushed to meet a planning date, even though nothing depends on it yet.
- Nobody can say what date a pending decision has to be made by, or which option disappears if it slips.

## What it does not say

It isn't permission to procrastinate: "Procrastinating is not the same as making decisions at the last responsible moment," the Poppendiecks write. Choices that set constraints and are costly to change belong early (Module 4, deck p. 28), such as the core platform or vendor a product is built on. Waiting defers benefits too, so the deck pairs this idea with an "earliest responsible moment", the first point at which deciding pays off (p. 116).

## One question to carry into your work

What's the biggest decision your team hasn't made yet, and on what date does waiting start to cost you an option?

## Go deeper

- Mary and Tom Poppendieck, *Lean Software Development: An Agile Toolkit* (Addison-Wesley, 2003), chapter 3, "Decide as Late as Possible" (about an hour). The chapter is in the publisher's [free sample](https://ptgmedia.pearsoncmg.com/images/9780321150783/samplepages/0321150783.pdf). Free at pearsoncmg.com.
- Mary Poppendieck, ["Lean Construction"](https://www.leanessays.com/2002/03/lean-construction.html) (2002), a short post on where she met the idea. Free at leanessays.com.
- Deck p. 115 (the definition and its warnings), p. 116 (the earliest responsible moment) and p. 117 (what a decision holds up, and what is risky to defer).
- Module 4, Design for Change: deck p. 28 on cost of change, and *How Buildings Learn*, chapter 11, "The Scenario-buffered Building", on keeping options open.

> Deck page references are to Ruth Malan's System Design and Software Architecture workshop notes, February to March 2025 edition, a 514-page set of slide notes; read only the pages cited. This card is an independent companion; it has not been reviewed or endorsed by Ruth Malan.
