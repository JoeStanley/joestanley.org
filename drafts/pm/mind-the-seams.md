## Why this matters

Much of the friction you fight as a PM (dependencies, handoffs, work waiting on another team, decisions that stall) looks like people being slow. It usually isn't. More often it comes from where the boundaries sit between teams, and how teams work across them. So treat the organization as a system you can read and help design, not as fixed scenery around your product.

## Short path (about two and a quarter hours of reading, plus about an hour for the exercises)

The deck is a 514-page set of workshop slide notes written for software architects, not a book, so don't read it like one. Read only the pages named here, and only the parts named. You'll find unfamiliar terms defined under "Terms you will meet", below. If you split the path across two sittings, stop after step 2.

1. The **Conway's Law** concept card (10 minutes).
2. *Team Topologies* (Skelton and Pais), the chapters "Conway's Law and Why It Matters" and "Team-First Thinking" (about an hour). Either edition will do; the 2025 second edition adds new case studies.
3. Deck p. 314 (10 minutes). Read the Conway quote, the paraphrase under it, and the sentence about managers deciding on teams. Skip the rest.
4. Deck p. 500 (5 minutes). Read "The Rule" and "The Qualifier" at the top. Skip the rest.
5. The **RACI** concept card (10 minutes).
6. Deck p. 319 (5 minutes). Read the quote about keeping an org chart, a diagram of how work actually flows, and a diagram of what the company does. Skip the rest.
7. Conway's original paper, "How Do Committees Invent?" (1968), about 20 minutes. It's four pages, free at melconway.com.
8. The **Agency and Coherence** concept card (10 minutes).
9. Ruth Malan and Dana Bredemeyer, ["Less is More with Minimalist Architecture"](https://www.bredemeyer.com/pdf_files/MinimalistArchitecture.PDF) (2002), 6 minutes. Three pages, free on the authors' site. It's an opinion column with no data, written for software architects, so read "architect" as whoever sets the rules that cross teams. Read it for the one reason they accept for taking a decision away from a team.

## Full path

- The rest of *Team Topologies*, especially the four team types, the three interaction modes, and evolving team structures through organizational sensing.
- *An Elegant Puzzle* (Larson), chapter 2, "Organizations": sizing teams, the states a team moves through, and the case against top-down global optimization. The rest of the book is a reference, so dip into it when you need it.
- For the force running the other way: Henderson and Clark, "Architectural Innovation" (1990), the classic study; Sosa, Eppinger and Rowles, "The Misalignment of Product Architecture and Organizational Structure in Complex Product Development" (2004), on how a product's design interfaces map onto who talks to whom; and Allan Kelly's short essay "Conway's Law v. Software Architecture", a practitioner's account of long-lived systems shaping teams.
- Deck pp. 52 to 61 (coherence, alignment, and how technology and the people who build and use it shape each other), pp. 462 to 463 (platforms run as internal products) and pp. 498 to 508 (who makes system decisions, advice forums, consensus and stewardship).
- Optional, if you want the evidence: Colfer and Baldwin, "The Mirroring Hypothesis: Theory, Evidence, and Exceptions" (2016).

## Terms you will meet

- **Cognitive load:** how much a team has to hold in its head to do its work. *Team Topologies* treats it as a limit on how much a team should own.
- **Interaction modes:** the three ways *Team Topologies* says two teams can work together.
  - **Collaboration:** working closely on something new, such as a routing team and a driver-app team designing live rerouting side by side. The learning is fast, the cost is high, and it's meant to be temporary.
  - **X-as-a-Service:** one team uses what another provides with little conversation, such as calling a well-documented internal API.
  - **Facilitating:** one team helps another learn or get unstuck, such as a testing specialist helping a team adopt automated tests.
- **Inverse Conway maneuver:** shaping teams and how they communicate on purpose, to get the system you want.
- **Advice process:** anyone may make a decision, after asking the people it affects and the people with relevant expertise (deck p. 500).
- **Responsible and accountable** (from RACI): responsible people do the work; the one accountable person owns the outcome and makes the final call. See the RACI card.

## What to look for

- **The force runs both ways.** The organization shapes the system (Conway), and the system shapes the organization right back. On deck p. 314, notice the point that whoever assigns work to teams is deciding the architecture, whether they mean to or not.
- **Hard-to-change systems hold teams in place.** When a system is costly to change, the communication around it tends to stay in the system's shape, and teams end up organized around the system they already have. Henderson and Clark (1990) found the same in one industry: architecture gets built into communication channels, and that helped explain why established firms stumbled when it had to change.
- **You can design for it, within limits.** The inverse Conway maneuver reshapes teams on purpose to get the system you want. Find the limits before you count on it: with a tech lead, work out which parts of your system could change fast enough to follow a new team design, and which would hold the old shape.
- **Cognitive load is a design limit.** Ask what your own team carries that it can't understand well.
- **Interaction is a choice, and usually a temporary one.** Each mode fits a different moment. Notice what it costs when collaboration quietly becomes the permanent default: every change needs a meeting.
- **Enough common ground, and no more.** Teams need just enough common ground to work together, such as shared terms and a shared definition of done. That doesn't mean forcing every team onto one plan. Deck pp. 52 to 53 make this case in denser language.
- **Decision rights are part of the design.** Compare the advice process with how decisions actually get made around you.

## Apply it to your own work

1. Give yourself about 30 minutes to sketch two pictures of your area, boxes and lines only. The first shows the teams and who actually talks to whom. The second shows the system's main parts and how they connect: services, data stores, and the screens or APIs customers touch. A first pass from what you already know is fine for the second picture. Then ask a tech lead to correct it, and open with "Which of these parts is hardest to change, and why?" Now lay the two side by side. Where do the boundaries line up, and where do they cut across each other? Check the mismatches against the symptoms on the Conway's Law card. Which of them couldn't move even if you wanted them to, because the system there is costly to change?
2. Take about 15 minutes and pick one dependency on another team that keeps coming back. Which interaction mode is it in today, and which should it be in? What would it take to move it?
3. Take about 15 minutes to think back to a decision from the last quarter that stalled. Who had to be consulted, who could say no, and was any of that written down?

## Check your own thinking

This module is trying to move you from "that team is slow" to "our boundary with that team is in the wrong place, or in the wrong mode". Test whether it has. If you could move one boundary, which would it be? What would you expect to change within one quarter, and which measure (for example, days a request waits) would you watch to find out whether it did? If you'd like a sounding board, take your two pictures and your answer to your manager or a mentor.

> Deck page references are to Ruth Malan's System Design and Software Architecture workshop notes, February to March 2025 edition. This guide is an independent companion; it has not been reviewed or endorsed by Ruth Malan.

# Conway's Law

## The idea

Organizations that design systems end up with designs that mirror their own communication structures. Mel Conway made the argument in 1968, and Fred Brooks later named it Conway's Law. The word that matters is communication. The system follows who actually talks to whom, and that isn't always what the org chart says. Ruth Malan's shorthand: when the system's architecture and the organization's architecture disagree, the organization's wins (deck p. 314).

## Why a PM should care

- **Team boundaries become product boundaries.** Each handoff between teams tends to become an interface in the system, and a place where work waits.
- **Whoever designs the teams is designing the architecture.** Deciding a team's scope, ownership or roadmap is an architecture decision, whether anyone calls it that or not.
- **Hard-to-change systems hold teams in place.** Once a system is costly to change, the teams around it tend to stay organized in its shape. A classic study of one industry found that architecture gets built into an organization's communication channels, and that helped explain why established firms struggled when the architecture had to change (Henderson and Clark, 1990).
- **You can use it on purpose.** Teams and their lines of communication can be shaped deliberately to get the system you want, a move called the inverse Conway maneuver. You'll rarely redraw teams yourself, but you can influence who owns what when work is planned, and name a mismatch to engineering leaders when you see one.
- **Customers feel the seams.** When two teams own two halves of one customer journey, the journey usually shows the join. A traveler books the flight in one flow, then starts over in another to add a bag.

## How to spot it at work

- A change that touches three teams takes far longer than one that touches one, whatever its size.
- The product has seams where the organization does: settings split across screens, APIs that follow department lines.
- A reorganization is announced, and the conversation about what it does to the system comes afterward, if it comes at all.

## What it does not say

It's a strong tendency, not a law of physics. Researchers who reviewed 142 studies found that an organization's structure usually does mirror the structure of what it builds, especially inside a single company. But not always: open, collaborative projects (mostly software) often broke the pattern, and digital coordination tools helped them do it (Colfer and Baldwin, 2016).

## One question to carry into your work

Where does a boundary between teams in your area cut through something a customer experiences as one thing?

## Go deeper

- Conway, "How Do Committees Invent?" (Datamation, 1968). Four pages, free at melconway.com.
- *Team Topologies*, the chapter "Conway's Law and Why It Matters".
- Deck p. 314 (Conway's thesis and what it implies for who decides the architecture) and p. 319 (org charts versus how work actually flows).
- Henderson and Clark, "Architectural Innovation" (1990), on systems shaping the organizations that build them.
- Colfer and Baldwin, "The Mirroring Hypothesis: Theory, Evidence, and Exceptions" (2016).

> Deck page references are to Ruth Malan's System Design and Software Architecture workshop notes, February to March 2025 edition, a 514-page set of slide notes; read only the pages cited. This card is an independent companion; it has not been reviewed or endorsed by Ruth Malan.

# RACI

## The idea

RACI is a grid that says who does what on a task or decision. Each person gets one letter per row. **Responsible:** does the work. **Accountable:** owns the outcome, signs off and has the final say. **Consulted:** gives input before sign-off. **Informed:** is told the result. The A may also do the work, so one person can be both A and R. When that happens, write A. Here's a grid for a hospital scheduling product.

| Decision | PM | Eng lead | Clinical lead | Director |
| --- | --- | --- | --- | --- |
| Choose a vendor | R | C | C | A |
| Change patient prep instructions | R | I | A | I |
| Plan the release | A | C | I | I |

## Why a PM should care

- **It names one decider.** [Mind Tools](https://www.mindtools.com/agn584l/the-raci-matrix) says each task needs exactly one accountable person, and [CIO.com](https://www.cio.com/article/287088/project-management-what-is-raci-and-how-does-it-improve-clarity.html) warns that two invite slow, contentious decisions.
- **It separates input from authority.** Consulted people shape the decision but don't own it, so a good opinion doesn't turn into a veto.
- **It can unstick a stalled decision.** Write the decision as one line and list the people involved. Agree who's the A, then ask who is truly C and move the rest to I. One practitioner on CIO.com reports that agreeing roles nearly always restarts a stuck project.
- **It protects required sign-offs.** When someone's approval is mandatory, you can't move them to I. That's the clinical lead on patient instructions in the grid above, or the accessibility lead on a public digital service. Show them as the A for their part of the decision, or list the sign-off beside the A.

## How to spot it at work

- A meeting ends with "let's align offline" and nobody can say who will make the call.
- Two leaders each believe the final say is theirs, or each believes it's the other's.
- Every review has the same long invite list, and the decision waits for the slowest reply.
- Someone who was never asked objects after the work is done.

## What it does not say

RACI records roles. It does not tell people how to decide. It fails in three familiar ways: everyone is made C, which CIO.com says slows the project; accountability is split between two people; or the grid turns into paperwork. So save it for decisions that are stuck or that cross teams. Atlassian's [DACI play](https://www.atlassian.com/team-playbook/plays/daci) uses Driver (the person who runs the process and gets a decision made), Approver (the one person who decides), Contributors (a voice, not a vote) and Informed, and it suits big cross-team decisions. The advice process (deck p. 500) has no assigned decider: anyone may decide after seeking advice from those affected and from experts, and they don't have to follow the advice. It matters to you because it spreads decisions out without losing track of who decides. RACI names the decider in advance. The advice process does not.

## One question to carry into your work

For the last decision that stalled in your area, who was the one accountable person, and would they have named themselves?

## Go deeper

- Mind Tools, ["The RACI Matrix"](https://www.mindtools.com/agn584l/the-raci-matrix), about 10 minutes. Free at mindtools.com.
- ["The RACI matrix: Your blueprint for project success"](https://www.cio.com/article/287088/project-management-what-is-raci-and-how-does-it-improve-clarity.html), CIO.com, about 10 minutes. Free at cio.com.
- Atlassian Team Playbook, ["DACI Decision Making Framework in action"](https://www.atlassian.com/team-playbook/plays/daci), about 10 minutes. Free at atlassian.com.
- Andrew Harmel-Law, ["Scaling the Practice of Architecture, Conversationally"](https://martinfowler.com/articles/scaling-architecture-conversationally.html) (2021), about 30 minutes. Free at martinfowler.com.
- Deck p. 500, "The Rule" and "The Qualifier" (5 minutes).

> Deck page references are to Ruth Malan's System Design and Software Architecture workshop notes, February to March 2025 edition, a 514-page set of slide notes; read only the pages cited. This card is an independent companion; it has not been reviewed or endorsed by Ruth Malan.

# Platform as a Product

*Picture: A platform team sits between many delivery teams and the plumbing they all need. Each team can use the platform, or build its own.*

## The idea

Evan Bottcher defines a digital platform as "a foundation of self-service APIs, tools, services, knowledge and support," arranged as an internal product. "Self-service" means a team can use it on its own, without filing a request. The teams that use it are its customers, and the aim is that they deliver features faster, with less coordination.

His central point is that a platform has to be compelling to use. It can't stand on a mandate alone, meaning a rule that says "you must use it." Using it should be easier than building and running your own.

## Why a PM cares

- **Your customers are other teams, and your platform is only worth what they get from it.** A team that can't get a new service into production without waiting on you will find another way, or wait.
- **Self-service removes the queue.** Bottcher cites a colleague's study at an Australian telecommunications company, where tasks that had to wait for another team were 10 to 12 times slower in elapsed time (the clock time from start to finish). Put a ticket queue in front of your platform and it can become the constraint for everyone downstream (see the card The Five Focusing Steps, on finding the one step that limits the whole flow).
- **A platform is more than software.** Documentation counts, and so do a quick first success, support, templates and a community. Bottcher lists a quick, cheap on-ramp (an easy way to get started) as part of what makes a platform compelling.
- **Start from proven needs.** Build what several application teams already need, not what you guess they'll need. He also wants a long-lived team that builds and runs the platform.

## How to spot it

- Routine requests arrive as tickets. On a platform that collects industrial sensor readings, that might be adding a device type or changing an alert threshold.
- "Self-service" exists, but real changes still need a ticket. Bottcher's example is a self-service tool for requisitioning compute instances from a fixed template, where any further change needed a ticket.
- Teams build their own copies or workarounds. That tells you the platform isn't compelling yet.
- Adoption comes from a rule. Ask yourself: if using the platform were optional, would your customers still choose it?

## What it does not say

It does not say you can never require anything. Some controls must apply to every team, such as encrypting card numbers on a payments platform. Bottcher's point is that a mandate isn't enough on its own, and that a compelling platform makes the safe way the easy way: his list includes secure and compliant by default. He also admits the balance is hard. Full team autonomy speeds delivery, but it brings duplicated infrastructure and per-team research overhead.

**One question to carry:** If your customer teams could choose, would they still choose your platform, and how would you know?

## Go deeper

**[What I Talk About When I Talk About Platforms](https://www.martinfowler.com/articles/talk-about-platforms.html), Evan Bottcher (2018)**

A long article. Free at martinfowler.com.

**Why trust it:** Bottcher describes himself as an experienced technical leader with over two decades in the field, and the article presents a model developed at Thoughtworks, a technology consultancy. It's one practitioner's view, not research, so weigh it that way.

**What you'll get:** A concrete list of what makes a platform compelling, plus the Netflix "paved road" idea (a central set of tools): teams may choose another way, but they carry the full cost of maintaining it.

# Agency and Coherence

## The idea

Work that many people do at once needs two things that pull against each other. People need room to decide, or the work is slow and nobody much wants to do it. And the pieces need to fit, or the product doesn't work as one thing.

Jabe Bloom, in a talk to software designers, names both halves (2020). Requisite variety, after the cybernetician Ross Ashby, says a team needs as many different views as the world it faces. Requisite coherence says it also needs "just enough common concepts to make progress", and "not maximally but minimally". Bloom also separates autonomy, "the ability to choose which action to take", from agency, which adds being "able to observe the results of those actions in the system one acts within". Freedom isn't enough on its own. People also need to see what their choices did.

The philosopher Alicia Juarrero shows the way through. We think of constraints as limits, and some are. But constraints "also create alternatives": the rules of syntax are what let a sentence mean anything at all. A few shared rules, well chosen, let many people act on their own and still add up to one thing. So be strict about a few things and loose about the rest. Be strict about the purpose, and about the few decisions that need a view of the whole. Leave how each team gets there to the team. Ruth Malan and Dana Bredemeyer, writing for software architects, give the test for the strict list: the only good reason to take a decision away from the people doing the work is a benefit to the whole "that the organization could not otherwise achieve" (2002).

Other fields landed in the same place. Marine Corps doctrine seeks unity "not principally through imposed control, but through harmonious initiative" inside guidance from above (MCDP 1, *Warfighting*, 1997). The team researcher Richard Hackman tells leaders to be "insistent and unapologetic" about the ends, and just as insistent about leaving the means alone (*Leading Teams*, 2002).

## Why a PM should care

- **You often write the strict list, whether or not you call it that.** What a term means, which flows have to match, what "done" includes. Write each rule as something that makes work possible: one agreed meaning of "booking" lets the search, payments and support teams on a travel site build on their own without meeting about it.
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
- Jabe Bloom, talk to the Virtual DDD meetup (16 January 2020), on requisite variety and requisite coherence. A practitioner's talk, not a study.
- Alicia Juarrero, ["Complexity is not Complication"](https://www.youtube.com/watch?v=WmtjQZCIsqY) (Deliberate Complexity conference, 2022), a talk, free on YouTube; and her book *Context Changes Everything: How Constraints Create Coherence*, chapter 3. She's a philosopher of complex systems, and the book is her own theory, argued, not measured.

*To check: the sources on this card were opened and its quotations checked on 20 November 2026, with these gaps. MCDP 1 was read on an archive.org copy, and Hackman, Hackman and Oldham, Ancona and Caldwell, and Guzzo and Dickson on university course copies. Lawrence and Lorsch's 1967 study of differentiation and integration is the classic research on this tension, and nobody has opened it yet. Bloom's and Juarrero's words were added on 20 November 2026 from where Ruth Malan's workshop notes quote them (pp. 51 to 53 and 73 to 76), and nobody has opened their own talks or book: find Bloom's talk and its date, check his two definitions (the notes give no source for them), and check Juarrero's quote and its source, which the notes give as "Causality as Constraint".*

# Architect Across the Interfaces

## The idea

"It is inadequate to architect up to the boundaries or interfaces of a system; one must architect across them." That's Robert Spinrad, a computer designer who later directed Xerox PARC, as reported by Mark Maier and Eberhardt Rechtin. Rechtin gave both halves of the reason: "The greatest leverage in system architecting is at the interfaces." And: "The greatest dangers are also at the interfaces."

Every team can do its own part well and the product can still fail, because the trouble sits between the parts. In Russell Ackoff's version, the best part of each kind, taken from every car, won't make the best car.

## Why a PM cares

- **Teams own their parts. Someone has to own what's between them.** At an insurer, intake and payout can each work perfectly while a claim sits stuck, because the two read "approved" differently. You're often the one person whose work spans both sides, so that join is part of your job.
- **Ask what could come across.** Rechtin's question: "What is the worst thing that other elements could do to you across the interface?" For a marketplace's search, it might be a seller sending a million price changes in an hour, or a feed that quietly stops. Ask it in design reviews.
- **A clear interface lets both sides move.** When what each side promises is written down, each team can change its own part without asking the other. Maier and Rechtin: "Make a system evolvable by paying attention to the interfaces."

## How to spot it

- Every team hits its target and customers still see the gap. On an analytics product, ingestion meets its throughput target, dashboards load fast, and the numbers are a day old.
- Nobody can show you what one side of an interface promises the other: what it sends, how fast, and what happens when it fails.
- Something breaks across a link nobody drew, like a nightly file another team quietly reads. Rechtin's warning: "Be prepared for reality to surface a few interfaces of its own."

## What it does not say

It doesn't say you design the interfaces, or that a central architect should take them from the teams. Whoever designs one has to look across it, at the whole. Nor does every seam need watching. Rechtin also advises drawing boundaries so that "local activity is high speed and global activity is slow change", and then most seams stay quiet.

**One question to carry:** Which interface in your product has no owner, and what's the worst thing that could come across it?

## Go deeper

**The Art of Systems Architecting, Mark W. Maier and Eberhardt Rechtin (1997)**

A textbook, revised in later editions. It isn't free.

**Why trust it:** Rechtin led the building of NASA's deep space tracking network, directed ARPA and founded a systems architecture program at the University of Southern California. The heuristics distill that experience. They weren't tested in studies.

**What you'll get:** These heuristics with the reasoning around them, and many more on where to draw a system's boundaries.

*To check: nobody has opened the book; the deck's link to it (sdincose.org, blocked here) doesn't match its title. Every quotation is from the deck (pp. 439, 465, 466, 478): check each against Maier and Rechtin or Rechtin's Systems Architecting (1991), with the edition. Ackoff's car is the deck's retelling (pp. 22, 472) of his talk "If Russ Ackoff had given a TED Talk". The backgrounds and the 1997 date are from Wikipedia, opened.*
