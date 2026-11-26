---
title: Mind the Seams
layout: module
module: mind-the-seams
question: How does the way we're organized shape what we build, and what falls between the parts?
setting: a marketplace for secondhand goods
one_thing: Sketch who talks to whom in your area, then how the system's parts connect, and mark where the two pictures disagree.
do_minutes: 30

last_time:
  - q: Review is your fitness app's constraint. Before anyone hires more coaches, what do you try?
    a: Getting more from the coaches you have, so they never wait for work, and making every other step serve their pace. Both are cheap.
  - q: A team is judged on reviews completed per day. What does Goodhart's Law warn you about?
    a: Once the number is a target, people find the cheapest way to raise it, so it stops telling you whether the work flows any faster.

steps:
  - id: card-conway
    kind: card
    card: cards/conways-law
    minutes: 5
    look: Which word in Conway's sentence matters, and what the org chart misses.
  - id: conway
    kind: read
    title: Melvin Conway, "How Do Committees Invent?"
    minutes: 20
    where: A magazine article from 1968. Free at melconway.com.
    links:
      - text: "How Do Committees Invent?"
        url: https://www.melconway.com/Home/pdf/committees.pdf
    look: "His advice: since the first design is rarely the best, \"flexibility of organization is important to effective design.\""
    trust: "An argument. It's the original."
    only: The law in its author's words, with the reasoning a one-line summary leaves out.
  - id: kelly
    kind: read
    title: Allan Kelly, "Conway's Law v. Software Architecture"
    minutes: 10
    where: A blog post. Free at allankelly.net.
    links:
      - text: "Conway's Law v. Software Architecture"
        url: https://allankelly.net/archives/638/conway-law-v-software-architecture
    look: "The force running the other way: \"Conway's Law is now working in reverse: the system is imposing structure on the organization.\""
    trust: "An argument. A practitioner's opinion, built on a made-up example."
    only: Why a system that's hard to change can hold a whole company in its shape.
  - id: bottcher
    kind: read
    title: Evan Bottcher, "What I Talk About When I Talk About Platforms"
    minutes: 20
    where: An article. Free at martinfowler.com.
    links:
      - text: "What I Talk About When I Talk About Platforms"
        url: https://www.martinfowler.com/articles/talk-about-platforms.html
    look: "His definition, \"a foundation of self-service APIs, tools, services, knowledge and support,\" run as an internal product. Its customers are the other teams, so it has to be worth choosing, not only required."
    trust: "Experience. One Thoughtworks consultant's view, drawn from his own client work."
    only: A checklist of what makes a platform worth choosing.
  - id: bounded
    kind: read
    title: Martin Fowler, "Bounded Context"
    minutes: 5
    where: A short note. Free at martinfowler.com.
    links:
      - text: "Bounded Context"
        url: https://martinfowler.com/bliki/BoundedContext.html
    look: The word "meter," which meant different things to different parts of an electricity utility.
    trust: "Experience. Fowler, a software developer who's written about design for decades, retells a pattern from Eric Evans's domain-driven design, which builds software around the business's language."
    only: A way to hear a boundary in how people talk.
  - id: do
    kind: do
    title: Draw the two pictures, and log a seam
    where: The Do, on this page, below. A tech lead's corrections can come later.
    look: Where the teams' boundaries and the system's cross.
  - id: check
    kind: check
    title: Check yourself
    where: The Check, on this page, below.
    look: The answers you missed, and why you missed them.

example:
  body: |
    **Who talks:** listings and review, daily. Payments and support, weekly, by ticket. Shipping, to the carrier, never to payments.

    **Parts, from memory:** listings feed review. Checkout writes the order; payouts and shipping's labels read it. Disputes live in support's tool. After checkout, buyers see only the order page.

    **Lines up:** listings and review.

    **Crosses:** a "not as described" dispute. Support opens it, payments freezes the payout, shipping labels the return. The return scan stays with shipping, so refunds wait: 300 open, the oldest 40 days since arrival.

    **Decision log:** this seam first, where the most money waits. Once someone owns the handoff, expect refunds within a week of arrival. 50 percent sure: some returns go unscanned. Check July 1.
  good:
    - The first picture shows who actually talks, and how often, rather than the org chart.
    - "The seam it picks is where the pictures disagree: payouts and returns share the order, but payments and shipping never talk."
    - It counts what waits at the seam from a stated start, so the change it expects for buyers has a baseline.

check:
  - q: Does a system mirror the org chart of the organization that builds it?
    a: Not necessarily. It mirrors who actually talks to whom, and that often isn't what the chart shows.
  - q: Own Your Role asked you to grow the role toward value nobody assigned, like a gap at your edge. Here, a handoff between teams needs someone who owns it. Should that be you?
    against: own-your-role
    a: For a while, so customers don't fall through it while you show the gap is real. Then get it an owner who'll still be there when you move on, since a seam held by one person's goodwill opens again when they leave.
  - q: Every team on the marketplace hits its target, and buyers still see a gap. Where do you look?
    a: Between the teams, at the joins. What one side sends isn't what the other expects, or nobody owns the handoff.
  - q: "**Beyond this module.** Your two pictures show your own company's teams and parts. Who shapes the product from outside both?"
    a: Vendors, partners, regulators and the open-source projects you build on. Their seams are yours too, and you can't reorganize them. Ask your tech lead which outside part you'd least like to lose.

deeper_one:
  title: "Team Topologies"
  why: "When someone asks a team to own one more thing, its words, cognitive load above all, are the ones you'll reach for."
deeper:
  - title: Team Topologies
    by: Matthew Skelton and Manuel Pais
    where: A book.
    note: "Read the chapters \"Conway's Law and Why It Matters\" and \"Team-First Thinking\" first, then the rest."
    trust: "Experience. Two consultants' model, built from their work with software teams and widely used."
    only: "A vocabulary for designing teams: four team types, three ways for teams to work together, and cognitive load, how much a team has to hold in its head, as a limit on what it should own."
  - title: "Architectural Innovation: The Reconfiguration of Existing Product Technologies and the Failure of Established Firms"
    by: Rebecca Henderson and Kim Clark (Administrative Science Quarterly, 1990)
    where: A journal article.
    note: Read it whole. Kim Clark is the researcher behind the heavyweight product manager on [Own Your Role](/pm/own-your-role/)'s full path.
    trust: "A study. A peer-reviewed classic, from one industry: the makers of the alignment equipment used to make chips."
    only: Evidence that a product's architecture gets built into a firm's communication channels, which helps explain why established firms stumbled when that architecture had to change.
  - title: Design and Reality
    by: Rebecca Wirfs-Brock and Mathias Verraes
    where: A book of six essays.
    note: "Read it whole, starting with the title essay. Engineers on an oil rig switched the alarms off during a long failure, and the system took the silence to mean the emergency was over. One word, \"alarm,\" had been covering two things. Then read \"Splitting a Domain Across Multiple Bounded Contexts.\""
    trust: "Experience. Wirfs-Brock invented responsibility-driven design, a method for designing software, and Verraes founded DDD Europe, a conference on domain-driven design. They write up cases from their own work."
    only: How a team finds a concept nobody had named, and where to draw the lines between contexts.
  - title: The Art of Systems Architecting
    by: Mark Maier and Eberhardt Rechtin
    where: A textbook.
    note: "Read the chapter \"Heuristics as Tools,\" then the appendix of heuristics for system-level architecting."
    trust: "Experience. Rechtin led the building of NASA's deep space tracking network, directed ARPA and founded a systems architecting program at the University of Southern California, and the book collects what that work taught."
    only: "Rules of thumb for the joins between parts: architect across an interface, not only up to it, as Robert Spinrad put it; ask what's the worst that could come across it; and draw interfaces so each part can be built on its own, without slicing through parts that must talk all the time."
  - title: Halt and Catch Fire
    by: created by Christopher Cantwell and Christopher C. Rogers (AMC, 2014 to 2017)
    where: A TV series.
    note: "A small company builds a portable PC, with a hardware chief, Gordon, and a software lead, Cameron, who want different machines. Her operating system has a personality and needs memory he won't give it, and the programmers take orders from both. In the ninth episode of season 1, when a rival unveils a faster, cheaper machine at a trade show, Gordon pulls her system out and swaps in MS-DOS: \"We had a problem. Now we have a product.\""
    only: A product shaped by the fight between the teams that built it. Then watch the software team walk out and found a company of its own.
---

## Why this matters

Much of the friction you fight as a PM looks like people being slow: the handoff, the work waiting on another team. Usually it's where the boundaries between teams sit, and how teams work across them. The longest wait you mapped in [Find the Constraint](/pm/find-the-constraint/) may well sit at one of them. Every team can do its part well and the product still fail, because the trouble sits between them. So treat the organization as a system you can read and help design, not as fixed scenery.

Some seams run through words. When two teams use one word for two things, the bug ships between them. On a secondhand marketplace, "approved" can mean to one team that a listing passed review, and to another that the seller can be paid. An area inside which each word has one agreed meaning is a {{< pm/term "bounded-context" >}}, and where one ends, someone has to translate, owned or not.

A category is a boundary of meaning too, and people fall between categories the way work falls between teams. In 1976 five Black women sued General Motors, which had hired no Black women before 1964, and a US court said it would hear their case as race discrimination or as sex discrimination, "but not a combination of both." In 1989 the law scholar Kimberlé Crenshaw used their case to name {{< pm/term "intersectional" "intersectionality" >}}: what happens where two categories meet, and what neither one shows on its own. Look for it in your product as you'd look for any seam: the customer whose problem is half one team's and half another's, so each team looks at its half and finds nothing wrong, or who belongs in two boxes on a form that allows one.

[//]: # (short-path)

## Do

**Draw the two pictures (30 minutes).** Sketch two pictures of your area, the part you and your nearest teams build. Lists will do. The first shows the teams and who actually talks to whom. The second shows the system's main parts and how they connect: services, data stores, and the screens or APIs customers touch. Draw the second from memory, then lay them side by side. Where do the boundaries line up, and where do they cross? Outside the 30 minutes, ask a tech lead to correct your second picture.

**For your decision log.** Pick the seam you'd fix first, where most customers or money wait, and roughly how much waits. Write what you expect to change for customers once someone owns it, how confident you are, and when you'll check.

{{< pm/example >}}

**Optional: walk one seam (15 minutes).** Pick a place where a customer's journey crosses between two teams. Write what each side promises the other at that {{< pm/term "interface" >}}: what it sends, how fast, and what happens when it fails. Check that a word such as "approved" means the same thing on both sides.

## Questions to bring to engineers

- Which parts of our system are hardest to change, and why? Do our team boundaries follow them?
- At this interface between teams, what does each side promise the other, and what happens when that breaks?
- What's the worst thing that could come across this interface, and who would notice first?
- Does "user" or "order" mean the same thing on both sides of this boundary?
