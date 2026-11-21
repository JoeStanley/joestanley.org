About 41 minutes: 11 reading, 30 doing (a 20-minute exercise and a 10-minute optional one).

**If you only do one thing:** Write down five questions your product's data has to answer, and how fresh each answer needs to be.

## Why this matters

A data system is shaped by the questions people will ask it. Each question, with who asks it, how often, how fast and how fresh, is an access pattern. You often know these better than the engineers, because the questions come from customers, support, operations and finance, and you hear them first.

Two more choices are partly yours. How fresh does each answer have to be, since fresher costs more? And where do the lines fall, since a word like "customer" rarely means one thing everywhere? Then there are the copies that reports, caches and other teams make from the system of record. When two reports disagree, there's usually a copy behind it. Zhamak Dehghani argues that data other teams use should be run like a product, with those teams treated as customers and someone answerable for its quality.

## The short path

1. **Access Patterns**

   Concept card. 2 minutes.

   **Look for:** The four things to write down about every question, and why freshness has a price.
2. **Martin Fowler, "Reporting Database" (2004, updated 2014)**

   4 minutes. Free at martinfowler.com.

   **Look for:** Why reports get a copy of their own, made from the live system, and what it costs to keep that copy fresh.

   **Why trust it:** A short, dated note from a software developer who's written about design for years. He's open that he doubts near-real-time reporting is worth much.

   **What you'll get:** Operational use against analytical use, and the price of freshness, on one page.
3. **Martin Fowler, "Bounded Context" (2014)**

   5 minutes. Free at martinfowler.com.

   **Look for:** His example of a word that meant different things to different departments. A bounded context is an area where each word has one agreed meaning.

   **Why trust it:** Fowler is retelling a pattern from Eric Evans's domain-driven design, a way of building software around the language of the business.

   **What you'll get:** A way to hear a boundary in how people talk.

## Do

**Write the access patterns for one feature (20 minutes).** Pick a feature, such as a rate limit that caps how many requests one API key can make in a minute. Make a table with a row for each of five questions its data has to answer. Give it columns for the question, who asks, how often, how fast, how fresh, and whether it's operational or analytical. Outside the 20 minutes, take it to your tech lead and ask: "Which of these does our design answer well, and which would be expensive?"

**Optional: find where one piece of data lives (10 minutes).** Pick one item your product holds, such as a student's final grade on a learning platform. List its system of record, then every copy you know of, in reports, other teams' systems or a vendor's, and who depends on each. Ask of each copy: if this dataset were wrong tomorrow, who would be told first, and who would fix it?

## Questions to bring to engineers

- How long after a change does each copy catch up?
- When data arrives late, does it count in the period it happened or the period we saw it?
- Does "user" or "order" mean the same thing on both sides of this boundary?

## Check yourself

Answer in your head, then check.

A dashboard shows yesterday's totals. Is that a defect?

**Answer:** Not by itself. Fowler notes that many reports work well with yesterday's data, and that keeping data fresher takes more machinery.

Why can't "customer" mean one thing across the whole company?

**Answer:** Different groups mean different things by it. Fowler's advice is to give each bounded context its own consistent model, and to make the relationships between contexts explicit.

A sensor reading taken on Friday reaches the system on Monday. Which day does it count for, and whose call is it?

**Answer:** By event time it's Friday's, and by processing time Monday's. A report on how the machines ran last week wants Friday, so it's a product call as much as an engineering one.

## Go deeper: the full path

Optional, and not counted in the time above.

- **Designing Data-Intensive Applications, second edition, Martin Kleppmann and Chris Riccomini (O'Reilly, 2026)** A book. Borrow it or buy it. Read chapter 1, especially "Operational Versus Analytical Systems" and "Systems of Record and Derived Data", then chapters 11 and 12, on batch and stream processing. **Why trust it:** O'Reilly publishes it, and the second edition adds Riccomini as co-author. **What you'll get:** The whole picture of where data lives and how it moves, from people who build such systems.
- **"Data Mesh Principles and Logical Architecture," Zhamak Dehghani (2020)** A long article. Free at martinfowler.com. Read the section "Data as a product". **Why trust it:** Dehghani wrote it, and Fowler's site published it. It argues for the approach, and it's written for analytical data, so read it as a case being made. **What you'll get:** What it takes to run a dataset as a product, with an owner measured on its quality and on how satisfied its users are.
- **Domain-Driven Design Reference, Eric Evans (2015)** A free PDF at domainlanguage.com. Read the entries "Bounded Context", "Ubiquitous Language", "Core Domain" and "Generic Subdomains", about a page each. **Why trust it:** It's Evans's own summary of the patterns in his book *Domain-Driven Design* (2003), where they start. **What you'll get:** The definitions at their source, and his advice on where to spend: keep the core, the part that sets your product apart, small, and think about buying the generic parts everyone needs, such as login.
- **Core Domain Charts, DDD Crew** Free at github.com/ddd-crew/core-domain-charts, about 4 minutes. **Why trust it:** It's a community tool, not research. **What you'll get:** One chart where the product view and the engineering view meet. Engineers judge how complex each area is, and product or business people judge how much it sets you apart. That second half is yours.
- **"Design and Reality," Mathias Verraes and Rebecca Wirfs-Brock (2021)** An essay. Free at verraes.net. **Why trust it:** Verraes founded a software design consultancy and the DDD Europe conference, and Wirfs-Brock is a software engineer known for responsibility-driven design. It's two practitioners writing up one case. **What you'll get:** How a team found a concept nobody had named, after engineers on an oil rig switched the alarms off during a long failure and the system took the silence to mean the emergency was over. One word, "alarm", had been covering two things.
- **The Essence of Software, Daniel Jackson (Princeton University Press, 2021)** A book. Borrow it or buy it. **Why trust it:** Jackson is a professor of computer science at MIT. The book argues for his own theory, so it isn't an independent test of it. **What you'll get:** His full account of concepts, the ideas users have to learn to use software, such as styles in a word processor.
- ***Brazil*, directed by Terry Gilliam, written by Gilliam, Tom Stoppard and Charles McKeown (1985)** A film, 142 minutes in Gilliam's own cut and 132 in the American release. A fly falls into a teleprinter, an arrest warrant for Tuttle comes out as Buttle, and the state arrests the wrong man, who dies under interrogation. Then each system records him its own way: the census has him "dormanted", Security "excised", Administration "completed". The clerks who find the mistake are relieved it's another department's: "Information Retrieval." **What you'll get:** A dark satire of the system of record. One copy goes wrong, everything downstream trusts it, and correcting it is nobody's job.

*To check: these are open from the draft. Does Fowler's "Reporting Database" doubt near-real-time "reporting" or "analytics"? Check the card's line on AWS against its DynamoDB guide, which may say relational designs are more forgiving. Check the second edition of Designing Data-Intensive Applications for its section titles, and find a reason to trust it beyond its publisher. Wirfs-Brock's background comes from Wikipedia only.*

## For the glossary

- **Access pattern:** A question a system's data has to answer, with who asks it, how often, how fast and how fresh.
- **Operational and analytical:** Operational use keeps the live service running, and analytical use looks across many records, the way reports do.
- **System of record and system of reference:** A system of record holds the authoritative copy of some data, from which every other copy is made. A system of reference makes that data easy to use, by gathering or preparing copies for people to read and decide with, and isn't where it changes.
- **Bounded context:** An area of a business or a system inside which each word and model has one agreed meaning.
- **Event time and processing time:** When something happened, and when the system saw it.

# Access Patterns

*Picture: Five questions arrive at one body of data. One needs an answer in a blink, one can wait until tomorrow, and each costs something different.*

## The idea

An access pattern is a question the data has to answer, and how it's asked: who asks, how often, how fast and how fresh. AWS's guide to its DynamoDB database says not to design the data's layout until you know those questions. Not every database is that strict, but every design makes some questions cheap and others expensive.

## Why a PM cares

- **The questions are product knowledge.** On an insurance claims product, you know what the claimant, the adjuster and finance will ask, and how soon.
- **Freshness has a price.** Before you ask for "real time", ask what decision the answer feeds.
- **Late data forces a choice.** Event time is when something happened, and processing time is when the system saw it. A sensor reading taken on Friday arrives on Monday, and someone has to decide which day it counts for.

## How to spot it

- A request says "real time" but not for whom, or for which decision.
- Two screens show different numbers for the same thing, because they read copies of different ages.
- A question is fast one way and slow the other. Listing one player's matches is quick, and finding every player who used one item may not be.

## What it does not say

It does not say you must list every question before you build. Needs change, and some designs adjust more easily than others.

**One question to carry:** Who will ask this, how fast do they need the answer, and what would break if it were a day old?

## Go deeper

**[The world beyond batch: Streaming 101](https://www.oreilly.com/radar/the-world-beyond-batch-streaming-101/), Tyler Akidau (2015)**

Free at oreilly.com/radar. Read through "Event time vs. processing time", about 12 minutes.

**Why trust it:** Akidau worked on Google's large-scale streaming systems when he wrote it, and its examples use Google's tools.

**What you'll get:** The words engineers use about batch and streaming, and why late data is the hard part.
