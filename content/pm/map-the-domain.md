---
title: Map the Domain
layout: module
module: map-the-domain
question: What questions must the system answer, how fast and how fresh, and where should its boundaries fall?
one_thing: Write down five questions your product's data has to answer, and how fresh each answer needs to be.
do_minutes: 30

last_time:
  - q: Kelly says Conway's Law can work in reverse. What does he mean?
    a: A system that's hard to change holds the organization around it in its shape, so teams drift back to fit the system.
  - q: What makes an internal platform worth choosing, and not only required?
    a: It's run as a product, for the teams that use it. In Bottcher's words, it's "a foundation of self-service APIs, tools, services, knowledge and support", and it has to be good enough that those teams would pick it.

steps:
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
    trust: "He's a software developer who's written about design for decades, and he's open about his doubts: he's skeptical that near-real-time analytics is worth it."
    only: Operational use against analytical use, and the price of freshness, on one page.
  - id: bounded
    kind: read
    title: Martin Fowler, "Bounded Context"
    minutes: 5
    where: A short note. Free at martinfowler.com.
    links:
      - text: "Bounded Context"
        url: https://martinfowler.com/bliki/BoundedContext.html
    look: The word "meter", which meant different things to different parts of an electricity utility. A bounded context is an area where each word has one agreed meaning.
    trust: Fowler's retelling of a pattern from Eric Evans's domain-driven design, a way of building software around the language of the business.
    only: A way to hear a boundary in how people talk.

check:
  - q: A dashboard shows yesterday's totals. Is that a defect?
    a: Not by itself. Fowler notes that many reports work well with yesterday's data, and that keeping data fresher takes more machinery.
  - q: Why can't "customer" mean one thing across the whole company?
    a: Different groups mean different things by it. Fowler's advice is to give each bounded context its own consistent model, and to make the relationships between contexts explicit.
  - q: A sensor reading taken on Friday reaches the system on Monday. Which day does it count for, and whose call is it?
    a: By event time it's Friday's, and by processing time Monday's. A report on how the machines ran last week wants Friday, so it's a product call as much as an engineering one.

deeper:
  - title: Designing Data-Intensive Applications
    by: Martin Kleppmann and Chris Riccomini
    where: A book.
    note: "Read chapter 1, especially \"Operational Versus Analytical Systems\" and \"Systems of Record and Derived Data\", then chapters 11 and 12, on batch and stream processing."
    trust: Kleppmann built large-scale data infrastructure at LinkedIn before he became a professor at Cambridge.
    only: The whole picture of where data lives and how it moves, and what each choice trades away.
  - title: Design and Reality
    by: Rebecca Wirfs-Brock and Mathias Verraes
    where: A book of six essays.
    note: "Read it whole, starting with the title essay. Engineers on an oil rig switched the alarms off during a long failure, and the system took the silence to mean the emergency was over. One word, \"alarm\", had been covering two things. Then read \"Splitting a Domain Across Multiple Bounded Contexts\"."
    trust: Wirfs-Brock invented responsibility-driven design, a widely taught way of designing software, and Verraes founded DDD Europe, a conference on domain-driven design. It's two practitioners writing up cases from their own work.
    only: How a team finds a concept nobody had named, and where to draw the lines between contexts.
  - title: Domain-Driven Design
    by: Eric Evans
    where: A book.
    note: "Read the chapters \"Maintaining Model Integrity\" and \"Distillation\"."
    trust: It's where bounded contexts and the core domain start. Fowler calls it not the easiest read, but one that amply repays the effort.
    only: Where to draw the lines between models, and where to spend. Keep the core, the part that sets your product apart, small. Think about buying the generic parts everyone needs, such as login.
  - title: Data Mesh
    by: Zhamak Dehghani
    where: A book.
    note: "Read the chapter \"Principle of Data as a Product\"."
    trust: Dehghani set out data mesh at Thoughtworks, an approach in which each part of a business owns and serves its own analytical data, and the book is her full case for it. It's written for analytical data, and it argues for her approach, so read it as a case being made.
    only: What it takes to run a dataset as a product, with an owner measured on its quality and on how satisfied its users are.
  - title: Brazil
    by: directed by Terry Gilliam, written by Gilliam, Tom Stoppard and Charles McKeown (1985)
    where: A classic film.
    note: "A fly falls into a teleprinter, an arrest warrant for Tuttle comes out as Buttle, and the state arrests the wrong man, who dies under interrogation. Then each system records him its own way: the census has him \"dormanted\", Security \"excised\", Administration \"completed\". The clerks who find the mistake are relieved it's another department's: \"Information Retrieval.\""
    only: A dark satire of the system of record. One copy goes wrong, everything downstream trusts it, and correcting it is nobody's job.
---

## Why this matters

A data system is shaped by the questions people will ask it. Each question, with who asks it, how often, how fast and how fresh, is an {{< pm/term "access-pattern" >}}. You often know these better than the engineers, because the questions come from customers, consumers, support, operations and finance, and you hear them first.

Two choices in particular are partly yours. How fresh does each answer have to be, since fresher costs more? And where do the lines fall, since a word like "customer" rarely means one thing everywhere? The area inside each line is a {{< pm/term "bounded-context" >}}. Then there are the copies that reports, caches and other teams make from the {{< pm/term "system-of-record" "system of record" >}}. When two reports disagree, there's usually a copy behind it. Zhamak Dehghani argues that data other teams analyze should be run like a product, with those teams treated as customers and someone answerable for its quality.

[//]: # (short-path)

## Do

**Write the access patterns for one feature (20 minutes).** Pick a feature, such as a rate limit that caps how many requests one API key can make in a minute. Make a table with a row for each of five questions its data has to answer. Give it columns for the question, who asks, how often, how fast, how fresh, and whether it's {{< pm/term "operational-analytical" "operational or analytical" >}}. Outside the 20 minutes, take it to your tech lead and ask: "Which of these does our design answer well, and which would be expensive?"

**Optional: find where one piece of data lives (10 minutes).** Pick one item your product holds, such as a student's final grade on a learning platform. List its system of record, then every copy you know of, in reports, other teams' systems or a vendor's, and who depends on each. Ask of each copy: if this dataset were wrong tomorrow, who would be told first, and who would fix it?

## Questions to bring to engineers

- How long after a change does each copy catch up?
- When data arrives late, does it count in the period it happened or the period we saw it?
- Does "user" or "order" mean the same thing on both sides of this boundary?
