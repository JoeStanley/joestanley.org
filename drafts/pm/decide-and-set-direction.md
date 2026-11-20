## Why this matters

A roadmap is a set of decisions, and on most teams many get made by default: by adding, by deferring, or by never deciding. Make them on purpose. That means telling which decisions deserve care, weighing what each option gains and costs, and saying what you're choosing not to do. It also means knowing whose decision it is. A few decisions need a view of the whole, and most are better made by the people doing the work. It comes late because it draws on the earlier modules, from seeing the system to knowing what's costly to change.

## Short path (about two and a half hours of reading, plus about an hour and a quarter for the exercises)

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
10. The **Agency and Coherence** concept card (10 minutes).
11. Ruth Malan and Dana Bredemeyer, ["Less is More with Minimalist Architecture"](https://www.bredemeyer.com/pdf_files/MinimalistArchitecture.PDF) (2002), 6 minutes. Three pages, free on the authors' site. It's an opinion column with no data, written for software architects, so read "architect" as whoever sets the rules that cross teams. Read it for the one reason they accept for taking a decision away from a team.
12. Deck p. 500 (5 minutes). Read "The Rule" and "The Qualifier" at the top: the advice process. Skip the rest.

## Full path

The full path adds to the short path, and all of it takes roughly 11 hours. If you have two more hours, spend them here: Rumelt's chapters 4 and 5 (about 80 minutes), then deck pp. 79 to 88 (about 45 minutes).

- Richard Rumelt, *Good Strategy Bad Strategy: The Difference and Why It Matters* (Crown Business, 2011), chapter 3, "Bad Strategy", chapter 4, "Why So Much Bad Strategy?", and chapter 5, "The Kernel of Good Strategy" (about two hours). Chapter 4 opens with a senior team at Digital Equipment Corporation that couldn't choose a direction.
- Decisions: deck pp. 79 to 88 (making a decision explicit, with a one-page record template on p. 88), pp. 89 to 103 (trade-offs, with a Spotify example on pp. 90 to 93) and pp. 105 to 107 (structured group conversations such as force field analysis), about 2 hours. Then pp. 108 to 110, 113 to 117 and 119 to 129 (which decisions matter, irreversibility, the last responsible moment, and "time span of discretion" on p. 121), about 85 minutes.
- Strategy and the landscape: deck pp. 146 to 163 (why strategy matters to system design; differentiation, moats and switching costs on pp. 155 to 159), about an hour; pp. 165 to 181 (a worked diagnosis, Wardley's strategy cycle, strategy at every level, and the whole Southwest example), about 65 minutes; pp. 182 to 201 (context maps, the business model canvas and Wardley maps), about an hour; pp. 203 to 214 (technology radars, futures and scenarios), about 40 minutes.
- Who decides: deck pp. 498 to 508 (who makes system decisions, advice forums, consensus and stewardship), about 40 minutes.
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
- **Cost of change:** what it would take to undo or redo a decision later. See Module 5, Design for Change.
- **Advice process:** anyone may make a decision, after asking the people it affects and the people with relevant expertise (deck p. 500). They don't have to follow the advice.

## What to look for

- **Operational effectiveness is not strategy.** In section I, Porter separates doing the same things better from choosing to do different things. Goals like faster delivery or fewer defects are the first kind. Pursue them, but don't count them as a choice.
- **Trade-offs come from real incompatibility.** Section III gives three sources: reputation, the activities themselves, and the limits of coordination. On deck p. 177, notice that the single aircraft type behind Southwest's low costs also left it exposed when that aircraft had problems.
- **A guiding policy rules things out.** On deck p. 164, Rumelt's guiding policy narrows the field of possible actions, and a vision with no method isn't one. His kernel starts with a diagnosis, and you can tell a diagnosis as a story too; the SCR card covers that.
- **Match the care to the door.** Deck pp. 111 and 112 build on Module 5's cost of change: go fast on decisions you can undo, and slow down for the ones that are hard to undo and high in consequence. Where you can, make a decision reversible, for example by piloting a new checkout flow in one market before it goes to all of them.
- **One decision, one decider.** Whoever decides, name one person, and say who gives input before the call. Input shapes a decision; it isn't a veto. That's the idea worth keeping from RACI, a grid teams use to assign who does what. Then compare the advice process on p. 500 with how decisions actually get made around you.
- **Name what you're avoiding, and what you rejected.** Deck p. 104 asks what your group is avoiding talking about. Write down the options you rejected, and why (p. 82). It makes the choice visible, and it saves you from arguing it again.

## Apply it to your own work

1. Write your kernel and a draft not-doing list in about 25 minutes. Start with one sentence for the diagnosis (the main challenge facing your product area) and one for the guiding policy (your overall approach to it), then list two or three coordinated actions (deck p. 164). Next, list three things you've been asked for and wouldn't do this quarter, each with one sentence tying the "no" to your diagnosis. Treat the list as a draft to take to your manager, because you may not have the authority to say no on your own. Then test each line: would a reasonable colleague argue for the opposite? If nobody would, it isn't a choice yet.
2. Sort five decisions by how hard they are to undo, in about 20 minutes. Take five decisions you made recently or face now, and place each on a two-by-two grid: easy or hard to undo, low or high consequence (deck p. 111). Which ones got heavy process even though they were easy to undo, and which hard-to-undo ones were rushed? A first pass from what you already know is fine. For a technical choice, check with a tech lead. You could open with "If we got this wrong, what would it take to undo it in six months?"
3. Record one decision with the options you rejected, in about 20 minutes. Pick a decision you face now and write it up on one page, using the template on deck p. 88: context, decision, status and consequences. Include at least three options (p. 82), and give each rejected option one sentence on why it lost. Then share the page with the person who owns the decision, or with your manager, so the "no" gets explained once, in writing.
4. In about 15 minutes, think back to a decision from the last quarter that stalled. Who had to be consulted, who could say no, and was any of that written down? Was there one named decider, and would they have named themselves?

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

It isn't permission to procrastinate: "Procrastinating is not the same as making decisions at the last responsible moment," the Poppendiecks write. Choices that set constraints and are costly to change belong early (Module 5, deck p. 28), such as the core platform or vendor a product is built on. Waiting defers benefits too, so the deck pairs this idea with an "earliest responsible moment", the first point at which deciding pays off (p. 116).

## One question to carry into your work

What's the biggest decision your team hasn't made yet, and on what date does waiting start to cost you an option?

## Go deeper

- Mary and Tom Poppendieck, *Lean Software Development: An Agile Toolkit* (Addison-Wesley, 2003), chapter 3, "Decide as Late as Possible" (about an hour). The chapter is in the publisher's [free sample](https://ptgmedia.pearsoncmg.com/images/9780321150783/samplepages/0321150783.pdf). Free at pearsoncmg.com.
- Mary Poppendieck, ["Lean Construction"](https://www.leanessays.com/2002/03/lean-construction.html) (2002), a short post on where she met the idea. Free at leanessays.com.
- Deck p. 115 (the definition and its warnings), p. 116 (the earliest responsible moment) and p. 117 (what a decision holds up, and what is risky to defer).
- Module 5, Design for Change: deck p. 28 on cost of change, and *How Buildings Learn*, chapter 11, "The Scenario-buffered Building", on keeping options open.

> Deck page references are to Ruth Malan's System Design and Software Architecture workshop notes, February to March 2025 edition, a 514-page set of slide notes; read only the pages cited. This card is an independent companion; it has not been reviewed or endorsed by Ruth Malan.

# Chesterton's Fence

## The idea

G. K. Chesterton pictured a reformer who finds a fence across a road and says, "I don't see the use of this; let us clear it away." The wiser reformer answers, "If you don't see the use of it, I certainly won't let you clear it away. Go away and think." Someone put it there for a reason. Until you know the reason, you can't judge it.

Two later lines say why. Systems "are the way they are, because they got that way" (Gerald Weinberg), so history explains them. They're also that way "because they fit that way" (Jessica Kerr), so an odd part may be holding something else up. Before you cut, ask two things. Why was it put here, and what leans on it now?

## Why a PM cares

- **You'll be asked to cut things all the time.** A feature few people use, an approval that slows every release, a legacy system nobody wants to own. From where you sit, each looks like pure cost.
- **Rules outlive the people who wrote them.** A delivery routing system keeps vans off one street every weekday afternoon, and nobody remembers why. There may be a school on it.
- **What breaks is usually somewhere else.** An insurer drops the second review on claims filed in a policy's first month, and a quarter later fraud losses climb in another team's report.
- **Asking is cheap.** Ten minutes with whoever added the step, or a search of old tickets and decision records, costs far less than an outage, and the people who built the fence are likelier to help take it down.

## How to spot it

- A cut is argued as "nobody uses this", and nobody has asked who added it.
- A cleanup ships, and a week later a team you didn't consult reports something broken.
- A step survives every review because nobody dares touch it, and nobody can say what it's for.

## What it does not say

It doesn't say the fence stays. Once you know how it arose, Chesterton says, you may find its purposes "were bad purposes, or that they have since become bad purposes, or that they are purposes which are no longer served." A factory's sensor alert threshold may have been set for a model the plant replaced years ago. Nor does asking become a reason never to change anything. Limit the search: if nobody finds the reason in a few days and the cut is easy to undo, a small trial you watch closely will tell you.

**One question to carry:** Before you cut it, can you say why it was put there and what leans on it now?

## Go deeper

**[The Thing](https://archive.org/details/in.ernet.dli.2015.475818), G. K. Chesterton (1929)**

Chapter 4, "The Drift from Domesticity", pages 29 and 30 of a 1946 reprint, about five minutes. Free at archive.org.

**Why trust it:** Chesterton was an English essayist, and this is an argument by analogy in a book defending his Catholic faith: common sense, not evidence. The chapter then turns to the family, so stop after the fence.

**What you'll get:** The passage in his own words, including the part retellings often drop: the reasons that let a fence go.

*To check: the Chesterton quotations were read in the linked scan's machine-read text, so check them against its page images. archive.org serves those from storage servers this environment can't reach, so they couldn't be opened on 20 November 2026. The Weinberg and Kerr lines are copied from deck p. 376, which names no work for either; nobody has opened their originals, and a search found none for Kerr. A search result says Weinberg credited his line to the economist Kenneth Boulding; if that holds, cite Boulding (S8).*

# Agency and Coherence

## The idea

Work that many people do at once needs two things that pull against each other. People need room to decide, or the work is slow and nobody much wants to do it. And the pieces need to fit, or the product doesn't work as one thing.

Jabe Bloom, in a talk to software designers, names both halves (2020). Requisite variety, after the cybernetician Ross Ashby, says a team needs as many different views as the world it faces. Requisite coherence says it also needs "just enough common concepts to make progress", and "not maximally but minimally". Bloom also separates autonomy, "the ability to choose which action to take", from agency, which adds being "able to observe the results of those actions in the system one acts within". Freedom isn't enough on its own. People also need to see what their choices did.

The philosopher Alicia Juarrero shows the way through. We think of constraints as limits, and some are. But constraints "also create alternatives": the rules of syntax are what let a sentence mean anything at all. A few shared rules, well chosen, let many people act on their own and still add up to one thing. So be strict about a few things and loose about the rest. Be strict about the purpose, and about the few decisions that need a view of the whole. Leave how each team gets there to the team. Ruth Malan and Dana Bredemeyer, writing for software architects, give the test for the strict list: the only good reason to take a decision away from the people doing the work is a benefit to the whole "that the organization could not otherwise achieve" (2002).

Other fields landed in the same place. Marine Corps doctrine seeks unity "not principally through imposed control, but through harmonious initiative" inside guidance from above (MCDP 1, *Warfighting*, 1997). The team researcher Richard Hackman tells leaders to be "insistent and unapologetic" about the ends, and just as insistent about leaving the means alone (*Leading Teams*, 2002).

## Why a PM should care

- **You often write the strict list, whether or not you call it that.** What a term means, which flows have to match, what "done" includes. Write each rule as something that makes work possible: one agreed meaning of "booking" lets the search, payments and support teams on a travel site build on their own without meeting about it. Agree a meaning where teams share a flow. Elsewhere a word can mean different things, as long as everyone knows where the line between meanings falls (the Bounded Context reading in Module 4, Map the Domain).
- **Freedom without feedback isn't agency.** A team that ships a change and never sees what it did to customers has autonomy and nothing to steer by. Get it the numbers, the support tickets and the user sessions for its own change.
- **Room to decide is part of why the work is worth doing.** In a survey of 658 employees across 62 jobs, freedom over how the work gets done went with higher motivation (Hackman and Oldham, 1976). Take it away and you lose effort you can't buy back with process.
- **A team can feel great and still be out of step.** In a study of 45 new-product teams, the ones that kept to themselves rated their own work highly, and management rated them poorly (Ancona and Caldwell, 1992). A team that's tight inside doesn't always fit with the teams around it.
- **Customers feel the gaps.** Two teams, two meanings of "account", two settings pages.
- **Every rule you add weakens the others.** Malan and Bredemeyer warn that each added decision "can potentially dilute the impact of all the other decisions". Keep the list short.

## How to spot it at work

- Too little agency: teams ask permission for small changes, work waits on a review that adds nothing, and people can tell you what they were told to build but not why.
- Too little coherence: every team's piece works and the whole doesn't. The same thing gets built twice. Meetings to "align" multiply.
- A team says it's doing well, and its neighbors disagree.
- There's a shared rule, and nobody can give the reason for it.

## What it does not say

It does not say more autonomy is always better. A review of the research found "substantial variance" in what autonomous work groups did for productivity and attitudes (Guzzo and Dickson, 1996). It doesn't say everyone has to agree, or build the same way: the aim is enough common ground to work together, and no more. It doesn't say autonomy means being left alone. In the motivation research, autonomy is "the feeling of volition that can accompany any act" (Ryan and Deci, 2000), so a shared rule you understand and accept can leave it intact. And it isn't a recipe. The best-known picture of "aligned autonomy" is Spotify's account of itself, which its authors called "only a snapshot of our current way of working" (Kniberg and Ivarsson, 2012).

## One question to carry into your work

Does this decision need a view of the whole? If it doesn't, whose is it?

## Go deeper

- U.S. Marine Corps, MCDP 1, *Warfighting* (1997), the sections "Philosophy of command", "Mission tactics" and "Commander's intent", about 8 minutes. A public manual. It's doctrine: how an organization means to work, not a study of how every unit does.
- Stephen Bungay, ["How to Make the Most of Your Company's Strategy"](https://hbr.org/2011/01/how-to-make-the-most-of-your-companys-strategy) (Harvard Business Review, 2011), and his book *The Art of Action* (2011): align on intent, leave the actions free. A consultant's model, with no outcome data. The site limits how many articles you can read free.
- Ancona and Caldwell, "Bridging the Boundary: External Activity and Performance in Organizational Teams" (Administrative Science Quarterly, 1992). The field study of 45 product teams, in five high-technology companies in the 1980s. The journal charges for it.
- Ryan and Deci, ["Self-Determination Theory and the Facilitation of Intrinsic Motivation, Social Development, and Well-Being"](https://selfdeterminationtheory.org/SDT/documents/2000_RyanDeci_SDT.pdf) (American Psychologist, 2000). Free on the authors' site. A review of their own theory, drawn mostly from schools, families and health care.
- Kniberg and Ivarsson, ["Scaling Agile @ Spotify"](https://blog.crisp.se/wp-content/uploads/2012/11/SpotifyScaling.pdf) (2012), 11 minutes. Free. A company describing itself.
- In this syllabus: the Concept Champion card, in Module 0, Own Your Role, uses the same commander's intent from the other side, as the vision one person holds for the whole.
- Jabe Bloom, talk to the Virtual DDD meetup (16 January 2020), on requisite variety and requisite coherence. A practitioner's talk, not a study.
- Alicia Juarrero, ["Complexity is not Complication"](https://www.youtube.com/watch?v=WmtjQZCIsqY) (Deliberate Complexity conference, 2022), a talk, free on YouTube; and her book *Context Changes Everything: How Constraints Create Coherence*, chapter 3. She's a philosopher of complex systems, and the book is her own theory, argued, not measured.

*To check: the sources on this card were opened and its quotations checked on 20 November 2026, with these gaps. MCDP 1 was read on an archive.org copy, and Hackman, Hackman and Oldham, Ancona and Caldwell, and Guzzo and Dickson on university course copies. Lawrence and Lorsch's 1967 study of differentiation and integration is the classic research on this tension, and nobody has opened it yet. Bloom's and Juarrero's words were added on 20 November 2026 from where Ruth Malan's workshop notes quote them (pp. 51 to 53 and 73 to 76), and nobody has opened their own talks or book: find Bloom's talk and its date, check his two definitions (the notes give no source for them), and check Juarrero's quote and its source, which the notes give as "Causality as Constraint". Her talk's link was confirmed on 20 November 2026 from YouTube's listing (Deliberate Complexity Conference 2022), but the talk couldn't be watched here. Her book is open access from MIT Press, on hosts this environment doesn't allow yet.*
