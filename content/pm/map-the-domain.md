---
title: Map the Domain
layout: module
module: map-the-domain
question: What must your data answer, and what have you promised the teams that build on it?
setting: a weather data API that farm apps, airlines and delivery firms build on
one_thing: Write the five questions your data must answer, and what each team that calls it is counting on.
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
    trust: "Experience. You met Fowler in [Mind the Seams](/pm/mind-the-seams/). He's written about software design for decades, and he's open about his doubts: he's skeptical that near-real-time analytics is worth it."
    only: Operational use against analytical use, and the price of freshness, on one page.
  - id: dehghani
    kind: read
    title: 'Zhamak Dehghani, "How to Move Beyond a Monolithic Data Lake to a Distributed Data Mesh"'
    minutes: 10
    where: An article from 2019. Read its parts "Domain data as a product" and "Domain data cross-functional teams." Free at martinfowler.com.
    links:
      - text: "How to Move Beyond a Monolithic Data Lake to a Distributed Data Mesh"
        url: https://martinfowler.com/articles/data-monolith-to-mesh.html
    look: "The teams who read your data are its customers, so it needs what a product needs: an owner, a promise about its quality, and a way to find it. \"No one will use a product that they can't trust.\""
    trust: "An argument. Dehghani wrote it as a consultant at Thoughtworks, from the data platforms she'd seen clients build, and data mesh as a whole is still debated."
    only: Data as a product where the idea starts, and in the two parts a PM needs most.
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
    look: "\"Just like a power company shouldn't change its voltage every two years,\" callers should be able to trust an API to stay put. Then how Stripe keeps old versions working for the accounts that still use them, and what that costs."
    trust: "Experience. An engineer on Stripe's own API, making the case for his company's choices. Since 2024 Stripe ships two major releases a year and monthly ones that break nothing, so read it as the scheme it ran in 2017."
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
    **Questions** (who, how often, how fast, how fresh, kind):

    - **Conditions now?** Phone apps, millions hourly, under a second, 10 minutes, operational.
    - **Season's rain?** Farm apps, nightly, minutes, by morning, analytical.
    - **Storm alert?** Airlines, polled every 5 minutes, seconds, a minute, operational. Worst: 5 minutes late.
    - **Hail on June 3?** Insurers, per claim, hours, final, analytical. Revising it reopens claims.
    - **Under the rate limit?** Gateway, every call, instant, exact, operational.

    **One reading:** record in the raw store. Copies: hourly totals, the model, insurers' history, airline caches. Farmers spot bad totals first. Ingest fixes them.

    **Decision log:** push storm alerts, at a push service's cost. Airlines hear within a minute. 60 percent sure: two airlines can't take pushes. Check in March.
  good:
    - Every row fills the same fields, so the costly ones stand out, fresh to the minute or exact and final.
    - It marks the one question the design answers worst, which is the one to raise first.
    - The trace names the record, who would notice a wrong copy first and who would fix it.

check:
  - q: A weather station records Friday's rain and loses its connection until Monday. Which day's total does the reading count in, and whose call is it?
    a: By event time it's Friday's, and by processing time Monday's. A farm looking back at last week's rain wants Friday, so it's a product call as much as an engineering one. Say which you promise, when a day's total is final, and how you'll correct one you've already sent.
  - q: Your team changes the order of the hourly readings in a response, which the documentation never promised. A farm app breaks. Whose problem is it?
    a: Yours as much as theirs. With enough callers, every behavior they can see gets depended on, which is Hyrum's Law, so a change that broke no written promise can still break a caller. Before the next one, count who calls it, tell them, and give them time to move. Then either promise the order in the documentation or stop callers being able to rely on it.
  - q: In Know Who It's For, your customers paid for waiting. Here your callers pay for your changes. A farm app still calls version 1 of your forecast, and keeping it alive costs your team a week's work every month. When do you switch it off?
    against: know-who-its-for
    a: Price both sides. Each week version 1 stays costs your team, and each week of notice you cut costs the farm app, which didn't choose to move. Give a date far enough out for them to plan, say what the new version gives them, and keep the date, since a date that slips teaches callers to wait. If the call isn't yours, list who still calls version 1, check what notice your terms promise paying callers, draft the notice and the date, and bring them to whoever owns the API.
  - q: "**Beyond this module.** Your table lists what your callers count on. What does your own API count on that you don't control?"
    a: "The public weather services whose observations and models it starts from. In 2025 the US National Weather Service [cut weather balloon launches](https://weather.gov/media/notification/pdf_2025/scn25-36_suspension_of_raob_launches.pdf) at some of its sites for lack of staff. It says the balloons' data \"support weather modeling and forecasting.\" NOAA also [retired its database of billion-dollar disasters](https://www.nesdis.noaa.gov/about/documents-reports/notice-of-changes/2025-notice-of-changes/billion-dollar-weather-and-climate-disasters). Some launches have since come back. The same holds for a cloud region, a vendor's API or another team's schema. Your promise to your callers can't be stronger than the one you were given, so write down which of yours rests on whose, and what you'd tell your callers if it changed. [The Compass](/pm/the-compass/) asks the same of any call that touches data: what it creates, who depends on it, and what it would take to change."

deeper_one:
  title: "Designing Data-Intensive Applications"
  why: "Where your data lives, how it moves and what each choice trades away, in the book many of your engineers will have read."
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
    trust: "Experience. Four consultants and authors who work on how companies run their APIs. Medjaoui created the apidays conferences, and Wilde wrote the Sunset header, the web's way of telling callers when an API will be switched off."
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

Some of what you build is for other teams: an API their products call, or a dataset their reports read. In [Mind the Seams](/pm/mind-the-seams/) you heard a boundary in how people talk. Here the boundary is written down, in an API's fields and a dataset's columns, and other teams build on it. Picture a weather data API. Farm apps call it for rain, airlines for storms, delivery firms for ice on the roads, and each of them has made promises of its own on top of yours.

The API's shape follows the questions people will ask of it. Each one, with who asks it, how often, how fast and how fresh, is an {{< pm/term "access-pattern" >}}. You often know these better than the engineers, because the questions come from customers, consumers, support, operations and finance, and you hear them first. Fresher answers cost more, so ask what decision each one feeds: a phone app wants this minute's temperature, and an insurer is happy with last month's. Reports, caches and other teams work from copies of the {{< pm/term "system-of-record" "system of record" >}}, for {{< pm/term "operational-analytical" "operational or analytical" >}} use, and each copy is one more place a wrong number can travel. That's why two reports can disagree. Some of what matters about people won't fit in a record's fields, and [Answer for What You Build](/pm/answer-for-what-you-build/) takes that up.

Data other teams read can be run as a product. Zhamak Dehghani's case is that those teams are its customers, so it needs an owner and a promise about its quality, such as how fresh it is. An API is the same kind of promise, and a stricter one. Callers build on what it does, not only on what you wrote down, so a change costs every team that built on it, and retiring an old version is a product decision with a price on both sides.

[//]: # (short-path)

## Do

**Write the access patterns (20 minutes).** Pick the API or dataset you work nearest, or one feature's data, such as the rate limit that caps how many calls one API key can make in a minute. Make a table of five questions its data has to answer, one row each, with columns for the question, who asks, how often, how fast (how long they'll wait for an answer), how fresh (how old the answer may be), and whether it's operational, keeping the service running, or analytical, looking back across many records. Where it matters, add what that caller is counting on, written down or not, and what breaks for them if the answer is late or wrong. Mark the row you think the design answers worst. Outside the 20 minutes, take it to your tech lead and ask: "Which of these does our design answer well, and which would be expensive?"

**Trace one piece of data (10 minutes).** Pick one thing your data holds, such as one station's hourly rainfall. Find its system of record, the copy everyone treats as the truth. Then list every copy you know of, in reports, caches, other teams' systems or a partner's, and who depends on each. For each copy, ask: if it were wrong tomorrow, who would notice first, and who would fix it?

**Read one design doc (15 minutes).** Find the design doc or decision record for the API or dataset you traced: the page where its engineers wrote down what they chose and why. Read it for what it promises callers and what it trades away, and write down one question it leaves open for you. Outside the 15 minutes, take the question to its author.

**For your decision log.** Pick one question from your table that a caller wants fresher than it gets today. Write what you'd trade to make it fresher, what you expect it to change for them, how sure you are, and when you'll know.

{{< pm/example >}}

## Questions to bring to engineers

- How long after a change does each copy of this data catch up?
- When data arrives late, does it count in the period it happened or the period we saw it?
- Who calls this API, by version, and how would we know if one of them stopped?
- What do our callers rely on that we never wrote down?
- What's our freshness target for this data, how do we measure it, and who hears when we miss it?
