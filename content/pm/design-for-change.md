---
title: Design for Change
layout: module
module: design-for-change
question: What will change, how fast, and what should be easy to change?
setting: a school's learning platform
one_thing: Before your next request is estimated, write down the slowest layer you think it touches.
do_minutes: 35

last_time:
  - q: Why can't "approved" mean one thing to every team on a marketplace?
    a: Different groups mean different things by it. Give each bounded context its own consistent model, and make the translation between contexts explicit, with someone who owns it.
  - q: What makes an internal platform worth choosing, and not only required?
    a: It's run as a product, for the teams that use it. In Bottcher's words, it's "a foundation of self-service APIs, tools, services, knowledge and support," and it has to be good enough that those teams would pick it.

steps:
  - id: brand
    kind: read
    title: 'Stewart Brand, "Pace Layering: How Complex Systems Learn and Keep Learning"'
    minutes: 10
    where: An essay. Free at longnow.org.
    links:
      - text: "Pace Layering: How Complex Systems Learn and Keep Learning"
        url: https://longnow.org/ideas/pace-layers/
    look: "Two points: slow layers control fast ones, and a layer forced to another's pace ends badly, whichever way the push goes. One of his examples is the Soviet Union forcing a five-year-plan pace on commerce and art."
    trust: "An argument. {{< pm/voice \"brand-trust\" >}}"
    only: Why each layer needs its own pace, from the person who drew the layers.
  - id: card-coupling
    kind: card
    card: cards/coupling
    minutes: 5
    look: The question to ask whenever someone says two parts are tightly coupled.
  - id: card-access
    kind: card
    card: cards/access-patterns
    minutes: 5
    look: The four things to write down about every question, and why freshness has a price.
  - id: reporting
    kind: read
    title: Martin Fowler, "Reporting Database"
    minutes: 5
    where: A short note from 2004, updated since. Free at martinfowler.com.
    links:
      - text: "Reporting Database"
        url: https://martinfowler.com/bliki/ReportingDatabase.html
    look: Why reports get a copy of their own, made from the live system, and what it costs to keep that copy fresh.
    trust: "Experience. He's a software developer who's written about design for decades, and he's open about his doubts: he's skeptical that near-real-time analytics is worth it."
    only: Operational use against analytical use, and the price of freshness, on one page.

check:
  - q: Letting a student join two classes at once looks small on screen. Why might it take a quarter?
    a: The slowest layer it touches sets the cost. If it reaches into the data model, a core system or a contract, it moves at that layer's pace.
  - q: An engineer says the gradebook and the course calendar are tightly coupled. What do you ask?
    a: For which change? Parts are coupled only with respect to a particular change, so name the one you expect and ask whether it would make both move.
  - q: Know Who It's For put a price on every week of waiting. This module asks you to spend weeks making likely changes cheap. When does each win?
    against: know-who-its-for
    a: Price both. When a change is likely and soon, making it cheap pays for itself in the weeks it saves later. When it's a guess, ship the value now, and count the rework in the price of the decision.
  - q: "**Beyond this module.** Your list stops at what you build and the rules it must meet. What slow layer lives in your customers' heads?"
    a: Their habits, and what they've learned to do on your screens. A redesign that's quick for you can be slow for them. After your next change to a screen people use every day, read your support queue for a week.

deeper:
  - title: Designing Data-Intensive Applications
    by: Martin Kleppmann and Chris Riccomini
    where: A book.
    note: "Read chapter 1, especially \"Operational Versus Analytical Systems,\" with its part on systems of record and derived data, then chapters 11 and 12, on batch and stream processing."
    trust: "Experience. Kleppmann built large-scale data infrastructure at LinkedIn before he became a professor at Cambridge."
    only: The whole picture of where data lives and how it moves, and what each choice trades away.
  - title: Seeing Like a State
    by: James C. Scott
    where: A book.
    note: "Read the introduction, then chapter 1, \"Nature and Space,\" on the scientific forestry of eighteenth-century Prussia and Saxony, and chapter 10, \"Conclusion.\" It's dense in places, so take your time as needed."
    trust: "An argument. {{< pm/voice \"scott-trust\" >}}"
    only: "Why planners sure of one future build what can't change, and four rules for doing better that are applicable to our own work: \"Take small steps.\" \"Favor reversibility.\" \"Plan on surprises.\" \"Plan on human inventiveness.\""
  - title: A Philosophy of Software Design
    by: John Ousterhout
    where: A book.
    note: Read it whole. Chapters 2 and 3, on complexity and on tactical against strategic work, are the heart of it for this module.
    trust: "An argument. Ousterhout taught a software design course at Stanford, and the book grew out of it. It's one designer's view, made from experience."
    only: The three symptoms of complexity in full, and the difference between tactical work, which gets this feature out, and strategic work, which keeps the next one cheap. That difference is the case you can make for engineering time.
  - title: On the Criteria To Be Used in Decomposing Systems into Modules
    by: David Parnas (Communications of the ACM, 1972)
    where: A journal article.
    note: It's short and dense, so read it slowly. The argument is in his comparison of two ways to split the same program, and you can skim the technical detail.
    trust: "An argument. It's the classic case for information hiding, keeping each decision likely to change inside one module, and he makes it from a single worked example."
    only: Why a system's boundaries go around the decisions likely to change. Engineers can draw them only as well as they know what's coming, and often you're the one who knows.
  - title: Yes Minister
    by: written by Antony Jay and Jonathan Lynn (BBC, 1980)
    where: A TV series.
    note: "Watch series 1, episode 4, \"Big Brother.\" A new minister wants safeguards on a national database. His predecessor drafted the same ones. He tells the new minister how the permanent secretary stalled them, one polite stage at a time, until an election took him out of office and the department wiped the slate clean."
    only: Pace layers in a government department. Ministers come and go while the civil service stays, so a change that has to pass through it moves at its speed.
---

## Why this matters

Ask how your product will change over time: which parts, how often, and at what cost. The slowest layer a request touches sets its {{< pm/term "cost-of-change" "cost of change" >}}, so the pain comes from fast parts tied to slow ones. Once you can see which is which, you'll estimate more honestly, and you'll have a case for the work that makes likely changes cheap. Mind the Seams asked where the boundaries fall. For a system, David Parnas's answer is to draw them around the decisions likely to change, so each change stays inside one part.

Slow isn't the enemy, though. A school's record of grades moves slowly on purpose, because every transcript depends on it. Each layer has its own right pace, which Stewart Brand calls {{< pm/term "pace-layers" "pace layering" >}}: "Fast learns, slow remembers." Some slow layers aren't yours. Students' phones change at their own pace, so retiring an old app version saves your team the upkeep and hands the bill to students who can't update, often those on the oldest or cheapest phones.

Data is often the slowest layer of all, because so much reads it, and the data a feature creates outlives the feature. Its shape follows the questions people will ask of it: each one, with who asks it, how often, how fast and how fresh, is an {{< pm/term "access-pattern" >}}. You often know these better than the engineers, because they come from customers, consumers, support, operations and finance, and you hear them first. Fresher answers cost more, so ask what decision each one feeds. And when two reports disagree, there's usually a copy behind it. Reports, caches and other teams each read their own copy of the {{< pm/term "system-of-record" "system of record" >}}, for {{< pm/term "operational-analytical" "operational or analytical" >}} use, and a change has to reach every copy.

There's a precise word for what makes a change costly: {{< pm/term "complexity" >}}. John Ousterhout uses it for anything in a system's structure that makes it hard to understand and change, and names three symptoms. Change amplification is a simple change that needs edits in many places. {{< pm/term "cognitive-load" "Cognitive load" >}} is how much you must know to make a change safely. And with unknown unknowns, nobody can tell in advance what a change will touch. With those words, you can say why a small request took a month without blaming anyone.

[//]: # (short-path)

## Do

**List your product's layers (25 minutes).** Take one product or journey you own and list its parts from fastest-changing to slowest: wording, screens, business rules, APIs, the data model, core systems of record, the contracts and laws it must meet. Note how often each changed in the last year. Then take the last request that ran long. Which layers did it touch, and which symptom of complexity showed?

**Trace one piece of data (10 minutes).** Pick one thing your product shows, such as a student's final grade. Find where it's first written, its system of record, then list every copy you know of, in reports, caches, other teams' systems or a vendor's, and who depends on each. For each copy, ask: if it were wrong tomorrow, who would notice first, and who would fix it?

**For your decision log.** Write how long you expect the next request that touches your slowest layer to take, and how sure you are. You'll know when it ships.

**Optional: walk a likely change (10 minutes).** This walk comes from Ruth Malan's workshop notes (February 2025, p. 329): architects run an anticipated change across a design while it's still cheap to change. Pick a change you expect next year, such as letting students take a course pass or fail, and trace the parts it would touch. Outside the 10 minutes, ask a tech lead: "If we did this, which parts would have to change?" If most would, what boundary would have contained it?

## Questions to bring to engineers

- Which of these layers is hardest to change, and why?
- Where in our system is change amplification worst?
- Is the pattern you're proposing earning its complexity, or would a plainer design do?
- How long after a change does each copy of this data catch up?
- When data arrives late, does it count in the period it happened or the period we saw it?
