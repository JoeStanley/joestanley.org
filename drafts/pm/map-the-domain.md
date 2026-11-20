About 90 minutes: 60 reading, 30 doing (a 20-minute exercise and a 10-minute optional one).

**If you only do one thing:** Write down five questions your product's data has to answer, and how fresh each answer needs to be.

## Why this matters

Engineers can't design a data system until they know what it will be asked. Each question, together with how it gets asked (who, how often, how fast, how fresh), is called an access pattern. You often know these better than the engineers do, because the questions come from customers, support, operations and finance, and you're the one who hears them. A design built without them can answer the wrong questions quickly and the right ones slowly, or not at all.

Two more choices follow. It's tempting to leave them to engineering, but both are partly yours. How fresh does each answer have to be, since fresher costs more? And where do the lines fall between parts of the business, since a word like "customer" rarely means one thing everywhere? This module gives you the vocabulary to take part in those decisions, and to ask whether a fashionable pattern is earning its cost.

Two terms keep coming up. Domain-driven design (DDD) is a way of building software around the language and parts of the business. A batch job processes data in scheduled chunks, overnight for example, where streaming processes it as it arrives.

## The short path

1. **AWS, "First steps for modeling relational data in DynamoDB"**

   5 minutes. The opening of the page. Free at docs.aws.amazon.com.

   **Look for:** Where you're meant to find the access patterns. For a new application, the page points you to user stories and use cases.

   **Why trust it:** It's Amazon's documentation for its own database product, DynamoDB, so read it for the principle, not the product.

   **What you'll get:** A plain statement that design waits until you know the questions the data has to answer.
2. **Martin Fowler, "Reporting Database" (2004, updated 2014)**

   4 minutes. Free at martinfowler.com.

   **Look for:** Why reports get their own copy of the data, and what he says about freshness. (That copy is made from the operational data. The live system stays the source of the truth, and engineers call it the system of record.)

   **Why trust it:** It's a short, dated note by Fowler, and he's open about where he stands: he's skeptical of the value of near-real-time reporting.

   **What you'll get:** The difference between operational and analytical use, and what freshness costs, in one page.
3. **Tyler Akidau, "The world beyond batch: Streaming 101" (2015)**

   12 minutes. Read the opening sections, through "Event time vs. processing time" (about 3,300 words). Free at oreilly.com/radar.

   **Look for:** Bounded data, which has an end, versus unbounded data, which keeps arriving. Then watch for the gap between when something happened and when the system saw it.

   **Why trust it:** When he wrote it, Akidau had worked on large-scale streaming systems at Google, including its Dataflow product (a Google Cloud service for processing data streams). The examples use Google's tools, so keep that in mind.

   **What you'll get:** The vocabulary engineers use when they argue about batch versus streaming. (Streaming means processing data as it arrives.)
4. **Martin Fowler, "Bounded Context" (2014)**

   5 minutes. Free at martinfowler.com.

   **Look for:** Why one model for a whole business fails, and what draws the lines. (A bounded context is an area inside which each word and model has one agreed meaning.) Notice his example, a single word that meant different things to different departments.

   **Why trust it:** It's a short note by Fowler on a core pattern of domain-driven design, and it comes with a worked example.

   **What you'll get:** A way to hear a boundary in how people talk.
5. **Eric Evans, *Domain-Driven Design Reference* (2015)**

   10 minutes. Read printed pages 2 to 4 (Bounded Context, Ubiquitous Language, the shared language a team uses in talk and code) and printed pages 40 and 41 (Core Domain, Generic Subdomains). A subdomain is one area of the business. Free PDF at domainlanguage.com.

   **Look for:** On page 40, the advice to keep the core (the part that makes your product different) small. On page 41, the advice to give generic parts (the ones everyone needs, such as login) lower priority and to consider off-the-shelf software or published designs.

   **Why trust it:** It's Evans's own summary of the patterns from his book, Domain-Driven Design (2003). Go by the numbers printed on the pages, not the ones your PDF viewer shows.

   **What you'll get:** The source definitions, about a page each.
6. **DDD Crew, "Core Domain Charts"**

   4 minutes. Free on GitHub, at github.com/ddd-crew/core-domain-charts.

   **Look for:** Who judges which axis. Engineers judge complexity, and product or business people judge differentiation. That second group includes you.

   **Why trust it:** It's a community tool, not research.

   **What you'll get:** One chart where the product view and the engineering view meet.
7. **Martin Fowler, "CQRS" (2011)**

   5 minutes. Free at martinfowler.com.

   **Look for:** His warning that for most systems the pattern adds risk. CQRS (Command Query Responsibility Segregation) means using separate models for writing data and for reading it. Notice the question he asks: is the benefit worth the jump?

   **Why trust it:** He's seen the pattern used on real projects, and he says most of the cases he met went poorly.

   **What you'll get:** A worked example of how to ask whether a pattern earns its complexity.
8. **Access Patterns**

   Concept card. 5 minutes.

   **Look for:** What to write down about every question: who asks, how often, how fast, how fresh, and whether it's operational (serves the live service) or analytical (looks across many records).
9. **Core, Supporting, Generic**

   Concept card. 5 minutes.

   **Look for:** The three-way choice: build with your best people, keep it simple, or buy.
10. **Data as a Product**

    Concept card. 5 minutes.

    **Look for:** A summary of what makes a dataset a product: someone answerable for it, a description of what's in it, quality standards and consumers whose trust matters.

## Do

**Write the access patterns for one feature (20 minutes).** Pick a feature on your product, such as a rate limit that caps how many requests one API key can make in a minute. Make a table with five rows, one for each question its data has to answer. Use these columns: the question, who asks (a customer, support, operations, finance, a report), how often, how fast the answer has to come, how fresh it has to be, and operational or analytical. Short phrases are enough. Then, outside the 20 minutes, take the table to your tech lead and ask: "Which of these does our design answer well, and which would be expensive?"

**Optional: find where one piece of data lives (10 minutes).** Pick one item your product holds, such as a traveler's saved passport number. List the system of record first, then every copy you know of (reports, the warehouse, other teams, vendors), each with who depends on it. Mark the places where you're not sure. Then note which copies you'd miss if that person asked you to erase the item.

## Questions to bring to engineers

- Which of these questions need an answer in under a second, and which can wait for tomorrow's overnight batch run?
- When data shows up late, does it count in the period it happened or the period we saw it?
- Is this part core, supporting or generic, and does the way we're building it match?
- Does "user" or "order" mean the same thing on both sides of this boundary?
- If these access patterns change next year, what would it cost to change the design?
- Is this pattern (CQRS, event sourcing, microservices) earning its complexity here?

## Check yourself

Answer in your head, then check.

A dashboard shows yesterday's totals. Is that a defect?

**Answer:** Not by itself. It depends on which decision the dashboard feeds. Fowler notes that many reports work well with yesterday's data, and that keeping data fresher takes more machinery.

Why can't "customer" mean one thing across the whole company?

**Answer:** Different groups mean different things by it. Each bounded context needs its own consistent model, and Fowler says the relationships between contexts should be made explicit.

Your team wants to build its own identity and login system. What question does domain-driven design prompt you to ask?

**Answer:** Is it core to what makes your product different? If it's a generic part, Evans advises giving it lower priority and considering off-the-shelf software or published designs.

## Go deeper: the full path

Optional, and not counted in the time above.

- **Designing Data-Intensive Applications, second edition, Martin Kleppmann and Chris Riccomini (2026)** A book from O'Reilly. Borrow it or buy it. Read chapter 1, "Trade-Offs in Data Systems Architecture," especially "Operational Versus Analytical Systems" and "Systems of Record and Derived Data." Then chapter 11, "Batch Processing," and chapter 12, "Stream Processing." **Why trust it:** It's published by O'Reilly, and the 2026 second edition adds Chris Riccomini as co-author. **What you'll get:** The whole picture of where data lives and how it moves, from the people who build such systems.
- **Learning Domain-Driven Design, Vlad Khononov (2021)** A book from O'Reilly. Part I covers strategic design, starting with chapter 1, "Analyzing Business Domains." **Why trust it:** It's published by O'Reilly, and chapter 1 covers core, supporting and generic subdomains. **What you'll get:** A fuller account of how to tell core, supporting and generic subdomains apart.
- **"Introducing EventStorming," Alberto Brandolini (2013)** Free on his blog. **Why trust it:** It's Brandolini's own blog post describing the workshop. **What you'll get:** A way to map a business process with domain experts and engineers together, using sticky notes on a wall. The post is from 2013, and the format has changed a good deal since.
- **"The world beyond batch: Streaming 102," Tyler Akidau (2016)** Free at oreilly.com/radar. **Why trust it:** It's the second part of the same two-part series, with examples from Google's Dataflow. **What you'll get:** How systems cope with data that arrives late and out of order, which is the hard part of event time.
- **Domain-Driven Design, Eric Evans (2003)** The original book. **Why trust it:** It's the 2003 book that the Evans Reference above summarizes. **What you'll get:** The reasoning behind the pattern summaries.

# Access Patterns

*Picture: Five questions arrive at one body of data. One needs an answer in a blink, one can wait for tomorrow, and each costs something different to serve.*

## The idea

An access pattern is a question the data has to answer, together with how it gets asked. Who asks, how often, how fast does the answer have to come, and how fresh does it have to be? AWS's guidance for its DynamoDB database product says not to start designing a schema (the layout of the data) until you know the questions it needs to answer. It points to user stories and use cases as the place to find them.

Two splits help. Operational questions keep the live service running, and analytical ones look across many records, the way reports do. Data can also be bounded (finite, like yesterday's file) or unbounded (it keeps arriving).

## Why a PM cares

- **The questions are product knowledge.** On a clinic booking product, you know what patients, the front desk and the clinic manager will ask, and how soon.
- **Freshness is a decision with a price.** Martin Fowler notes that many reports work well with yesterday's data, and he's skeptical of the value of near-real-time analytics. Before you ask for "real time," ask what decision the answer feeds.
- **Late data forces a choice.** Event time is when something happened, and processing time is when the system saw it. Say a sensor reading taken on Friday arrives on Monday. Someone has to decide which day it counts for.

## How to spot it

- A request says "real time" or "up to date" but doesn't say for whom, or for which decision.
- Two screens or reports show different numbers for the same thing, because they're reading copies of different ages.
- A question is quick to answer from one direction and slow from the other. Finding everything one viewer watched may be fast, while finding every viewer who watched one particular episode may be slow.

## What it does not say

It does not say you have to list every question before you build anything. Needs change, and some designs adjust more easily than others. Fowler isn't saying fresh data is wrong, either. His point is that keeping data fresh is the downside of a separate reporting copy.

**One question to carry:** Who will ask this, how fast do they need the answer, and what would break if it were a day old?

## Go deeper

**[The world beyond batch: Streaming 102](https://www.oreilly.com/radar/the-world-beyond-batch-streaming-102/), Tyler Akidau (2016)**

Free at oreilly.com/radar.

**Why trust it:** It's the second part of the series that starts with Streaming 101, and its examples use Google's Dataflow, a Google Cloud service for processing data streams.

**What you'll get:** How streaming systems handle data that arrives late and out of order.

# Core, Supporting, Generic

*Picture: A business drawn as a map of areas. A few are where you win, some only keep things running, and others you could buy off the shelf.*

## The idea

Domain-driven design (a way of building software around the parts and language of the business) splits a business into subdomains, meaning areas such as pricing, route planning or login. Then it asks how much effort each one deserves. The core is where your product differs from the rest, so it gets your best people, and Eric Evans advises keeping it small. A generic subdomain is something nearly everyone needs, but it isn't why the product exists. Evans says to give it lower priority and to consider off-the-shelf software or published designs.

Later writers add a third kind, the supporting subdomain. You need it, it's simple, and it won't give you an edge. Teams typically build it themselves.

## Why a PM cares

- **It's a decision about where to spend.** Spread effort evenly and you starve the core. The Strategy as Forsaking card makes the same point: choosing what you won't do is part of strategy.
- **It stops quiet overbuilding.** A team can enjoy building its own version of something common, such as identity and login, and it's an easy thing to say yes to. Ask whether it's generic, and whether buying it would free people for the core.
- **The judgment is shared.** The DDD Crew's core domain chart (a community tool that plots each area by how different it makes you and how complex it is) has engineers judge complexity, and product or business people judge differentiation. Your half is the one engineers can't supply.
- **Boundaries follow the teams.** The parts you draw end up owned by teams. The Conway's Law card covers the idea behind that: a system's structure tends to copy the communication lines of the teams that build it.

## How to spot it

- A team is proud of its custom build of something every company in the industry also needs.
- The area where your product clearly beats the alternatives gets no extra attention, or the fewest people.
- Engineers and product people disagree about where an area sits on the DDD Crew chart. Don't smooth that over, because it's the useful part.

## What it does not say

It does not say generic means unimportant. A generic part can be essential, and a payment service you buy still needs someone to check it and own it. The sorting isn't permanent either: what's core now can become generic as the market catches up.

**One question to carry:** If a competitor copied this part tomorrow, would our customers notice, and should our best people be here?

## Go deeper

**[High Level System Analysis and Design with Domain-Driven Design](https://www.endpointdev.com/blog/2026/04/high-level-system-analysis-and-design-ddd-part-1/) (part 1 of 4), Kevin Campusano (2026)**

A blog post. Free at endpointdev.com.

**Why trust it:** It's a developer's post on the blog of End Point Dev, a software services company, so read it as a practitioner's retelling.

**What you'll get:** All three kinds of subdomain defined side by side, in a few paragraphs.

# Data as a Product

*Picture: A shelf of datasets, each with a label that names its owner, says what is inside, and promises how good it is. People take them down because they trust the label.*

## The idea

Data as a product means treating a dataset like something you ship to customers. Zhamak Dehghani sets out the idea as the second of four principles of the data mesh, an approach that has each business domain own and publish its data for others to use. She says the consumers of the data should be treated as customers. A useful summary (this syllabus's wording, not her list) is: someone answerable for it, a description of what's in it, quality standards, and consumers whose trust matters.

## Why a PM cares

- **Someone is answerable for it.** Dehghani calls for a domain data product owner (the person in a business domain accountable for its data). That owner is measured on data quality, on shorter time to start using the data, and on user satisfaction.
- **Quality moves upstream.** Her article puts responsibility for quality close to where the data is produced, not with whoever cleans it up later.
- **Trust takes work.** She names the cost of finding, understanding and trusting data as a major obstacle.
- **Consumers shape it.** Conversations between users and the owner shape the data's interfaces (the way others get at the data, such as its fields and formats). You can speak up for what analysts and support need.

## How to spot it

- Nobody can say who owns a dataset, or the answer changes depending on who you ask.
- Consumers find out about a change when their reports or alerts break.
- Quality only gets checked downstream, by the people who were handed the bad numbers.
- Nobody has written down what a field means or how fresh it is.

## What it does not say

Her article is about analytical data (data used for reports and analysis, as opposed to data serving the live service), and a full data mesh is a large undertaking. The article presents its four principles as a set, so borrowing this one alone, for a single dataset other teams depend on, is this syllabus's framing, not hers. Applying the idea to operational data, such as the stream of match results a game's matchmaking service reads, also goes beyond her text. It's a reasonable extension, but the article doesn't argue it.

**One question to carry:** If this dataset were wrong tomorrow, who would be told first, and who would fix it?

## Go deeper

**[Data Mesh Principles and Logical Architecture](https://martinfowler.com/articles/data-mesh-principles.html), Zhamak Dehghani (2020)**

A long article. Free at martinfowler.com. Read the section "Data as a product."

**Why trust it:** Dehghani wrote it and Martin Fowler's site published it. It argues for the approach, so read it as a case being made.

**What you'll get:** The owner's role, and how quality is measured, in her own words.

# Concepts

## The idea

A concept is one of the ideas you have to understand to use a piece of software: a paragraph in a word processor, or one user following another on a social network. Daniel Jackson, a computer scientist at MIT, defines it as "a structure that is invented to give a coherent account of the immediate consequences of actions in a complex system." Take styles in a word processor: you could format a document without them, but a style explains why one change reformats many paragraphs.

Concepts are hard to change once they're built in. In *Software Abstractions* (2006), Jackson warns: "No amount of refactoring, bar starting again from scratch, can rescue a system built on flawed concepts." (Refactoring means restructuring code without changing what it does.)

## Why a PM cares

- **Choosing the concepts users see is product work.** Each one is something your users have to learn, and the code gets built around it. Settle which ones they see, and how each behaves, with your engineers before the build starts.
- **A missing concept shows up as odd behavior.** Mathias Verraes and Rebecca Wirfs-Brock describe engineers on an oil rig who turned the alarms off during a long failure so they could concentrate, and the system took a silent alarm to mean the emergency was over. The team added a concept nobody had named, the alert condition. The alarm can still be turned off, and the condition stays.
- **Workarounds point to the gap.** Say an assignment on a learning platform has one due date. A teacher who gives one student two extra days has to move it for the whole class. The missing concept is the extension.

## How to spot it

- Support keeps explaining behavior that's working exactly as designed.
- One word covers two things that behave differently, the way "alarm" covered both the noise and the condition behind it.
- Users coin a word for something the product has no name for.
- A simple request has an ugly side effect. If the only way to stop service to a lost phone is to cancel the line, the customer loses the number too.

## What it does not say

A concept isn't a bounded context: that's about where a word's meaning holds, and a concept is a piece of behavior users have to learn. Nor are more concepts better: each is one more thing to learn, so add one when it explains behavior people already trip over. And Jackson's refactoring warning covers the abstractions in the code as much as the ones on screen.

**One question to carry:** What do users have to understand to use this, and what do they keep needing that has no name yet?

## Go deeper

**[Design and Reality](https://verraes.net/2021/09/design-and-reality/), Mathias Verraes and Rebecca Wirfs-Brock (2021)**

An essay. Free at verraes.net.

**Why trust it:** Verraes founded a software design consultancy and the DDD Europe conference. Wirfs-Brock is a software engineer and consultant known for responsibility-driven design, an approach to object design. It's two practitioners writing up one case, not research.

**What you'll get:** The whole alarm story, and how a team found a concept nobody had named.

**[The Essence of Software](https://essenceofsoftware.com/), Daniel Jackson (2021)**

A book from Princeton University Press. Borrow it or buy it.

**Why trust it:** Jackson is a professor of computer science at MIT. The book argues for his own theory; it isn't an independent test of it.

**What you'll get:** His full account of concepts, which this card only samples.

*To check: the essay (13 September 2021), its author page and the book's site, with Jackson's author page, were opened on 20 November 2026, and the alarm story, Verraes's background, Jackson's post and the book's publisher and year were checked against them. Still open: both Jackson quotes come from the deck (pp. 303 and 325). Check the definition against his paper "Towards a Theory of Conceptual Design for Software" (Onward! 2015, free at dspace.mit.edu, a host this environment doesn't allow yet) and the refactoring line against Software Abstractions (2006). Wirfs-Brock's background comes from Wikipedia only.*
