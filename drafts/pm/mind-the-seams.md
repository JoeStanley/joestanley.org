About 70 minutes: 35 reading, 35 doing (a 25-minute exercise and a 10-minute optional one).

**If you only do one thing:** Sketch who talks to whom in your area, then how the system's parts connect, and mark where the two pictures disagree.

## Why this matters

Much of the friction you fight as a PM looks like people being slow: the dependency, the handoff, the work waiting on another team. It usually isn't. More often it comes from where the boundaries sit between teams, and how teams work across them. Every team can do its own part well and the product can still fail, because the trouble sits between the parts. So treat the organization as a system you can read and help design, not as fixed scenery around your product.

## The short path

1. **Conway's Law**

   Concept card. 2 minutes.

   **Look for:** Why the system follows who actually talks to whom.
2. **Melvin Conway, "How Do Committees Invent?" (*Datamation*, 1968)**

   15 minutes. Free at [melconway.com](http://www.melconway.com/Home/pdf/committees.pdf).

   **Look for:** His advice for living with his law: since the first design is rarely the best, "flexibility of organization is important to effective design."

   **Why trust it:** It's the original, and it's an argument, not a study.

   **What you'll get:** The law in its author's words, with the reasoning a one-line summary leaves out.
3. **Allan Kelly, "Conway's Law v. Software Architecture" (allankelly.net, 2013)**

   5 minutes. Free at [allankelly.net](https://allankelly.net/archives/638/conway-law-v-software-architecture).

   **Look for:** The force running the other way: "Conway's Law is now working in reverse: the system is imposing structure on the organization."

   **Why trust it:** A practitioner's short post from his own experience of long-lived systems.

   **What you'll get:** Why a system that's costly to change can hold a whole company in its shape.
4. **Evan Bottcher, "What I Talk About When I Talk About Platforms" (martinfowler.com, 2018)**

   13 minutes. Free at [martinfowler.com](https://www.martinfowler.com/articles/talk-about-platforms.html).

   **Look for:** His definition, "a foundation of self-service APIs, tools, services, knowledge and support", run as an internal product. Its customers are the other teams, so it has to be worth choosing, not only required.

   **Why trust it:** Bottcher has over two decades as a technical leader, and the model was developed at Thoughtworks, a technology consultancy. It's one practitioner's view, not research.

   **What you'll get:** A checklist of what makes a platform worth choosing.

## Do

**Draw the two pictures (25 minutes).** Sketch two pictures of your area. The first shows the teams and who actually talks to whom. The second shows the system's main parts and how they connect: services, data stores, and the screens or APIs customers touch. Draw the second from memory, then ask a tech lead to correct it. Lay the two side by side. Where do the boundaries line up, and where do they cross?

**Optional: walk one seam (10 minutes).** Pick a place where a customer's journey crosses from one team's part to another's. Write what each side promises the other: what it sends, how fast, and what happens when it fails. Check that a word such as "approved" means the same thing on both sides.

## Questions to bring to engineers

- Which parts of our system are hardest to change, and why? Do our team boundaries follow them?
- At this interface between teams, what does each side promise the other, and what happens when that breaks?
- What's the worst thing that could come across this interface, and who would notice first?

## Check yourself

Answer in your head, then check.

Does a system mirror the org chart of the organization that builds it?

**Answer:** Not necessarily. It mirrors who actually talks to whom, and that often isn't what the chart shows.

A year after a reorganization, the system still has the old shape. Why?

**Answer:** A system that's costly to change holds the teams around it in its shape, which Kelly calls Conway's Law working in reverse.

Every team hits its target, and customers still see a gap. Where do you look?

**Answer:** Between the teams, at the joins: what one side sends isn't what the other expects, or nobody owns the handoff.

## Go deeper: the full path

Optional, and not counted in the time above.

- **Team Topologies, Matthew Skelton and Manuel Pais (IT Revolution, 2019)** A book. Either edition will do, and the 2025 second edition adds new case studies. Start with the chapters "Conway's Law and Why It Matters" and "Team-First Thinking", then read on for the four team types, the three ways teams work together, and evolving team structures. **Why trust it:** Two consultants' model, built from their work with software teams and widely used, but not tested in studies. **What you'll get:** A vocabulary for designing teams, with cognitive load, how much a team has to hold in its head, as a limit on what it should own.
- **"Architectural Innovation: The Reconfiguration of Existing Product Technologies and the Failure of Established Firms," Rebecca Henderson and Kim Clark (*Administrative Science Quarterly*, 1990)** A journal article. **Why trust it:** A peer-reviewed classic, from a study of one industry: the makers of photolithographic alignment equipment, used to make chips. **What you'll get:** Evidence that a product's architecture gets built into a firm's communication channels, which helps explain why established firms stumbled when it had to change.
- **"The Misalignment of Product Architecture and Organizational Structure in Complex Product Development," Manuel Sosa, Steven Eppinger and Craig Rowles (*Management Science*, 2004)** A journal article. **Why trust it:** Peer-reviewed, and built on data from a single large engineering project. **What you'll get:** How a product's design interfaces map onto who talks to whom, and what goes wrong where they don't.
- **The Art of Systems Architecting, Mark Maier and Eberhardt Rechtin (CRC Press, 1997)** A textbook, revised in later editions. It isn't free. **Why trust it:** Rechtin led the building of NASA's deep space tracking network, directed ARPA and founded a systems architecture program at the University of Southern California. Its heuristics are distilled from experience, and no study has tested them. **What you'll get:** Rules of thumb for the joins between parts: look across an interface, not only up to it, and draw boundaries so most change stays local.
- ***Apollo 13*, directed by Ron Howard (Universal, 1995)** A film, 140 minutes. Two companies built the two spacecraft, North American Aviation the command module and Grumman the lunar module. So when the crew has to live in the lunar module, the command module's square carbon dioxide canisters don't fit its round openings, and engineers on the ground are handed a table of what's on board: "We gotta find a way to make this fit into the hole for this, using nothing but that." **What you'll get:** A seam you could hold in your hand. Each company built its part well, and the trouble was where the parts met.

*To check: nobody has opened Maier and Rechtin. The link to it in Ruth Malan's workshop notes answers with a bot check, and archive.org has no copy. Check what the book says about interfaces and boundaries against it or Rechtin's Systems Architecting (1991), with the edition. Rechtin's background and the 1997 date are from Wikipedia, opened. Henderson and Clark's industry and the full path's publishers are given from memory. Nobody has opened Team Topologies or Sosa, Eppinger and Rowles in this round, so check each one's reasons. The free copy of Conway's paper is a scan, and his line on flexibility is as Malan's notes quote it (p. 314): check it against the paper.*

## For the glossary

- **Conway's Law:** A system's design tends to copy the communication structure of the organization that builds it.
- **Inverse Conway maneuver:** Shaping teams, and how they talk to each other, on purpose, to get the system you want.
- **Interface:** Where two parts of a system, or two teams, meet, and what each side promises the other there.
- **Platform:** Self-service tools and services that one team runs as an internal product for other teams.

# Conway's Law

*Picture: Two teams, and the system they built split along the same line.*

## The idea

Organizations that design systems, Mel Conway argued in 1968, end up with designs that copy their own communication structures. The word that matters is communication: the system follows who actually talks to whom, and that isn't always what the org chart says. Ruth Malan puts it in one line in her workshop notes (February 2025, p. 314): "if the architecture of the system and the architecture of the organization are at odds, the architecture of the organization wins."

## Why a PM cares

- **Team boundaries become product boundaries.** Each handoff between teams tends to become an interface, and a place where work waits. Customers feel the join: a traveler books a flight in one flow, then starts over in another to add a bag.
- **Whoever designs the teams designs the architecture.** Malan again: "if we have managers deciding on teams, and deciding which services will be built, by which teams, we implicitly have managers deciding on the system architecture." Doing that on purpose, to get the system you want, is the inverse Conway maneuver.

## How to spot it

- A change touching three teams takes far longer than one touching one.
- The product has seams where the organization does: settings split across screens, APIs that follow department lines.
- A reorganization is announced, and what it does to the system comes up afterward.

## What it does not say

It's a strong tendency, not a law of physics. Reviewing 142 studies, Lyra Colfer and Carliss Baldwin found that organizations usually do mirror what they build, especially inside one company. Open, collaborative projects, mostly software, often broke the pattern, with help from digital coordination tools.

**One question to carry:** Where does a boundary between teams in your area cut through something a customer experiences as one thing?

## Go deeper

**[The Mirroring Hypothesis: Theory, Evidence, and Exceptions](https://dash.harvard.edu/entities/publication/73120379-10f0-6bd4-e053-0100007fdf3b), Lyra Colfer and Carliss Baldwin (2016)**

A research paper in *Industrial and Corporate Change*. Free at dash.harvard.edu.

**Why trust it:** Peer-reviewed, and it weighs many studies, not one case.

**What you'll get:** Where mirroring holds, where it breaks, and why.

*To check: the link is to Harvard's repository record, found by a search, so check it opens the full paper.*
