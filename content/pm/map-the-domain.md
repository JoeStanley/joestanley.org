---
title: Map the Domain
layout: module
module: map-the-domain
question: What must your data answer, and what have you promised the teams that build on it?
setting: a weather data API that farm apps, airlines and delivery firms build on
one_thing: Write the five questions your data must answer, and what each team that uses it is counting on.
do_minutes: 45

last_time:
  - q: Why can't "approved" mean one thing to every team on a marketplace?
    a: Different groups mean different things by it. Give each bounded context its own consistent model, and make the translation between contexts explicit, with someone who owns it.
  - q: What makes an internal platform worth choosing, and not only required?
    a: It's run as a product, for the teams that use it. In Bottcher's words, it's "a foundation of self-service APIs, tools, services, knowledge and support," and it has to be good enough that those teams would pick it.

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
    trust: "Experience. You met Fowler in [Mind the Seams](/pm/mind-the-seams/). He's open about his doubts: he's skeptical that near-real-time analytics is worth it."
    only: Operational use against analytical use, and the price of freshness, on one page.
  - id: dehghani
    kind: read
    title: 'Zhamak Dehghani, "How to Move Beyond a Monolithic Data Lake to a Distributed Data Mesh"'
    minutes: 10
    where: An article from 2019. Read its parts "Domain data as a product" and "Domain data cross-functional teams." Free at martinfowler.com.
    links:
      - text: "How to Move Beyond a Monolithic Data Lake to a Distributed Data Mesh"
        url: https://martinfowler.com/articles/data-monolith-to-mesh.html
    look: "Her case that the teams who read your data are its customers, and her line \"No one will use a product that they can't trust.\""
    trust: "An argument. Dehghani wrote it as a consultant at Thoughtworks, from the data platforms she'd seen clients build, and data mesh as a whole is still debated."
    only: Data as a product at its source, in the two parts a PM needs most.
  - id: card-promise
    kind: card
    card: cards/api-is-a-promise
    minutes: 5
    look: Why callers count on more than you wrote down, and what retiring a version costs on both sides.
  - id: leach
    kind: read
    title: 'Brandur Leach, "APIs as infrastructure: future-proofing Stripe with versioning"'
    minutes: 10
    where: A blog post from 2017. Free at stripe.com. You can skip the code.
    links:
      - text: "APIs as infrastructure: future-proofing Stripe with versioning"
        url: https://stripe.com/blog/api-versioning
    look: "Why Stripe compares itself to a power company that \"shouldn't change its voltage every two years,\" and how it keeps old versions working."
    trust: "Experience. An engineer on Stripe's own API, making the case for his company's choices. Stripe now ships two major releases a year and monthly ones that break nothing, so read it as the scheme it ran in 2017."
    only: One company's account of what keeping its promise costs, concrete enough to follow without the code.
  - id: do
    kind: do
    title: Map the questions and the promises
    where: The Do, on this page, below. A tech lead's answers, and a design doc's author's, can come later.
    look: Which question your design answers worst, and who would notice a wrong copy first.
  - id: check
    kind: check
    title: Check yourself
    where: The Check, on this page, below.
    look: The answers you missed, and why you missed them.

example:
  body: |
    **Operational** (who, how often, how fast, how fresh, what breaks):

    - **Ice ahead?** Delivery firms, constantly, under a second, a minute, a skid.
    - **Storm alert?** Airlines, polled every 5 minutes, seconds, a minute, late diversions. Worst: 5 minutes stale.
    - **Over the limit?** Gateway, every call, instant, seconds, false blocks.

    **Analytical:**

    - **Season's rain?** Farm apps, nightly, minutes, by morning, reordering breaks charts (unwritten).
    - **Hail on June 3?** Insurers, per claim, hours, final, reopened claims.

    **Hourly rain:** record: the raw store. Copies: farm totals, forecast model, insurers' history, airline caches. Totals break most: farmers notice, the ingest team fixes them.

    **Decision log:** a push service, a quarter's work, so airlines divert sooner. 60 percent: two airlines can't take pushes. Check in March.
  good:
    - Every row fills the same fields, down to what a miss costs the caller, even where nothing was written down.
    - It marks the question the design answers worst, and the log prices a fix for it, with a date to check.
    - The trace names the record, the copy most likely to go wrong, who would notice and who would fix it.

check:
  - q: A weather station records Friday's rain and loses its connection until Monday. Which day's total does the reading count in, and whose call is it?
    a: By event time it's Friday's, and by processing time Monday's. A farm checking last week's rain wants Friday, so it's a product call as much as an engineering one. Say which you promise, and when a day's total is final.
  - q: Your team changes the order of the hourly readings in a response, which the documentation never promised. A farm app breaks. Whose problem is it?
    a: Yours as much as theirs. With enough callers, every behavior they can see gets depended on, which is Hyrum's Law. Next time, count who calls it and tell them first. Then either promise the order, or vary it on purpose so nobody relies on it.
  - q: In Know Who It's For, your customers paid for waiting. Here your callers pay for your changes. A farm app still calls version 1 of your forecast, and keeping it alive costs your team a week's work every month. When do you switch it off?
    against: know-who-its-for
    a: Price both sides. Each week version 1 stays costs your team, and each week of notice you cut costs the farm app, which didn't choose to move. Set a date far enough out for them to plan, and keep it, since a date that slips teaches callers to wait. If the call isn't yours, list who still calls version 1, check what notice your terms promise, and bring a draft date to whoever owns the API.
  - q: "**Beyond this module.** Your table lists what your callers count on. What does your own API count on that you don't control?"
    a: "The public weather services its data starts from. In 2025 the US National Weather Service [cut weather balloon launches](https://weather.gov/media/notification/pdf_2025/scn25-36_suspension_of_raob_launches.pdf), whose data it says \"support weather modeling and forecasting,\" at some sites for lack of staff, and NOAA [retired its database of billion-dollar disasters](https://www.nesdis.noaa.gov/about/documents-reports/notice-of-changes/2025-notice-of-changes/billion-dollar-weather-and-climate-disasters). Some launches have since come back. The same holds for a cloud region or a vendor's API. Your promise can't be stronger than the ones you were given, so write down which of yours rests on whose. [The Compass](/pm/the-compass/) gathers the questions to carry to any call that touches data."

deeper_one:
  title: "Designing Data-Intensive Applications"
  why: "It's the book many of your engineers will have read, so it gives you their words."
deeper:
  - title: Designing Data-Intensive Applications
    by: Martin Kleppmann and Chris Riccomini
    where: A book.
    note: Read chapter 1, with its parts on operational against analytical systems and on systems of record and derived data, then chapters 11 and 12, on batch and stream processing.
    trust: "Experience. Kleppmann built large-scale data infrastructure at LinkedIn before he became a professor at Cambridge."
    only: The whole picture of where data lives and how it moves, and what each choice trades away.
  - title: Continuous API Management
    by: Mehdi Medjaoui, Erik Wilde, Ronnie Mitra and Mike Amundsen
    where: A book.
    note: "Free at [f5.com](https://www.f5.com/content/dam/f5/corp/global/pdf/ebooks/continuous-api-mgmt-2e.pdf). NGINX, part of F5, sponsored it. Read chapters 3, \"The API as a Product,\" 5, \"Continuous API Improvement,\" and 7, \"The API Product Lifecycle.\""
    trust: "Experience. Four consultants and authors on running APIs. Medjaoui created the apidays conferences, and Wilde wrote the Sunset header, the web's way of telling callers an API will be switched off."
    only: Running an API as a product across its whole life, from a caller's first try to its retirement, with what to measure at each stage.
  - title: Domain-Driven Design
    by: Eric Evans
    where: A book.
    note: "Read chapters 14, \"Maintaining Model Integrity,\" and 15, \"Distillation.\""
    trust: "Experience. It's where bounded contexts and the core domain start. This one's target audience is architects, but I think the work required to navigate it as a PM pays for itself in time, especially as agentic workflows become more common."
    only: Where to draw the lines between models, and where to spend. Keep the core, the part that sets your product apart, small. Think about buying the generic parts everyone needs, such as login.
  - title: Data Mesh
    by: Zhamak Dehghani
    where: A book.
    note: "Read chapter 3, \"Principle of Data as a Product.\""
    trust: "An argument. Dehghani set out data mesh at Thoughtworks, an approach in which each part of a business owns and serves its own analytical data. This is her case for it."
    only: What it takes to run a dataset as a product, with an owner measured on its quality and on how satisfied its users are.
  - title: Brazil
    by: directed by Terry Gilliam, written by Gilliam, Tom Stoppard and Charles McKeown (Universal, 1985)
    where: A classic film.
    note: "A beetle falls into a teleprinter, an arrest warrant for Tuttle comes out as Buttle, and the state pursues and arrests the wrong man. The entire thing is a story of what happens when indifference leads to bureaucratic dystopia, reinforcing societal indifference."
    only: A dark satire of the system of record. Every department downstream builds on a record it never checks.
---

## Why this matters

Some of what you build is for other teams: an API their products call, or a dataset their reports read. In [Mind the Seams](/pm/mind-the-seams/) you heard a boundary in how people talk. Here the boundary is written down, in an API's fields and a dataset's columns, and other teams build on it. Picture a weather data API: farm apps call it for rain, airlines for storms, delivery firms for ice on the roads, and each has made promises of its own on top of yours. To map the domain is to map what its data must answer, and what you've promised the teams who ask.

The API's shape follows the questions people will ask of it. Each one, with who asks it, how often, how fast and how fresh, is an {{< pm/term "access-pattern" >}}. You often know these better than the engineers, because the questions come from customers, consumers, support, operations and finance, and you hear them first. Fresher answers cost more, so ask what decision each one feeds: a delivery firm wants this minute's road temperature, and an insurer is happy with last month's. Data that arrives late raises a choice too: count it when it happened, its {{< pm/term "event-time" "event time" >}}, or when it arrived, its processing time. Each question is {{< pm/term "operational-analytical" "operational or analytical" >}}: it answers requests as they happen, or it looks back across many records. Reports, caches and other teams work from copies of the {{< pm/term "system-of-record" "system of record" >}}. Each copy can fall behind or go wrong on its own, which is why two reports can disagree.

Data other teams read can be run as a product. Zhamak Dehghani's case is that those teams are its customers, so it needs an owner and a promise about its quality, such as how fresh it is. An API is the same kind of promise, and a stricter one. Callers build on what it does, beyond what you documented, so retiring an old version is a product decision with a price on both sides.

[//]: # (short-path)

## Do

**Write the access patterns (20 minutes).** Pick the API or dataset you work nearest, or one feature's data, such as the counts behind a rate limit. List five questions its data must answer, each with who asks, how often, how fast (how long they'll wait), how fresh (how old the answer may be), and whether it's operational or analytical. Then add what each caller counts on: what breaks for them if the answer is late or wrong, written down or not. Mark the row the design answers worst. Outside the 20 minutes, ask your tech lead: "Which of these does our design answer well, and which would be expensive?"

**Trace one piece of data (10 minutes).** Pick one thing your data holds, such as a station's hourly rain. Find its system of record, where it's first written and where corrections land. List every copy you know of, in reports, caches or other teams' systems, and who depends on each. For the copy most likely to go wrong, ask who would notice first, and who would fix it.

**Read one design doc (15 minutes).** Find the design doc or decision record behind that data, where its engineers wrote down what they chose and why. Read it for what it promises callers and what it trades away, and write down one question it leaves open. Outside the 15 minutes, take it to its author. If there's no doc, ask your tech lead why.

**For your decision log.** Pick a question a caller wants fresher than it gets today, or the one you marked worst. Write what you'd trade to make it fresher, what you expect it to change for them, how sure you are, and when you'll know.

{{< pm/example >}}

## Questions to bring to engineers

- How long after a change does each copy of this data catch up?
- Who calls this API, by version, and how would we know if one of them stopped?
- What do our callers rely on that we never wrote down?
- What's our freshness target for this data, how do we measure it, and who hears when we miss it?
