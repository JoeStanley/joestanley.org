About 112 minutes: 67 reading, 45 doing.

**If you only do one thing:** Run a consequence scan (a short team conversation about what a feature will cause) on one feature you own, and write down one change you'd propose.

## Why this matters

Your choices land on people who were never in the meeting. On a delivery platform, small rules decide how many stops fit in a shift, which order waits when a van runs late, and what counts as delivered. Across millions of orders, a small rule becomes a large effect. Route planning is a good example: the software picks the route that scores best on some number, and it's worth asking what that number leaves out, such as a driver with no time to stop or a customer who needs a minute to reach the door.

This module covers four things: who gains and who pays, your share of the responsibility when you feel like one cog, the difference between creating value and merely capturing it, and how much data you collect. Three other parts of the syllabus connect to it. The Goodhart's Law card says a measure that becomes a target stops being a good measure, and that's how a metric comes to reward harm. Change Safely covers how to run experiments safely, and experiments are run on people: in 2014 a journal published a Facebook study that changed what users saw in their feeds to test their moods. The journal later added an expression of concern about consent. Map the Domain shows you how to map the data a system holds and where it lives.

## The short path

1. **Consequence Scanning: how to build responsibility into product development**

   10 minutes. Free at safetytechnetwork.org.uk.
   - [Consequence Scanning explainer](https://www.safetytechnetwork.org.uk/consequence-scanning-how-to-build-responsibility-into-product-development/)

   **Look for:** The three questions: what are the intended and unintended consequences, which positive ones do we want to focus on, and which do we want to mitigate (reduce or prevent). You'll use them in the exercise.

   **Why trust it:** The page names Sam Brown, who created the method while working at Doteveryone, a responsible technology think tank, and it lays out the three questions.

   **What you'll get:** A way to run the conversation with your team before launch, on a feature that's defined but not yet built.
2. **Value Created, Value Captured**

   Concept card. 5 minutes.

   **Look for:** The difference between the benefit customers get and the share you keep, and which tactics raise one without the other (making it hard to leave is one).
3. **Fred Reichheld and Rob Markey, "Blowing the whistle on bad profits" (2006)**

   10 minutes. Free at bain.com.
   - [Blowing the whistle on bad profits](https://bain.com/insights/blowing-whistle-on-bad-profits)

   **Look for:** Where they draw the line between profit customers would endorse and profit customers resent.

   **Why trust it:** Bain & Company published it in August 2006. It's a consultancy arguing for its own measure, the Net Promoter Score (NPS, a customer survey score of how likely people are to recommend you), so read it as a case for a method.

   **What you'll get:** An argument you can make in business terms, not only ethical ones, against profit that costs you the customer relationship.
4. **Cory Doctorow, "Tiktok's enshittification" (2023)**

   20 minutes. Free at pluralistic.net.
   - [Pluralistic: Tiktok's enshittification](https://pluralistic.net/2023/01/21/potemkin-ai/)

   **Look for:** The three stages of what he calls enshittification (his crude word for a platform getting worse): good to users first, then shifting value to business customers, then taking it for itself. Also how lock-in, which makes leaving costly, lets a company shift value away from users.

   **Why trust it:** It's an opinion essay posted on 21 January 2023, in which Doctorow describes the pattern he calls enshittification. It's an argument, not research.

   **What you'll get:** A vivid account of how a product slides from serving users to extracting from them.
5. **Many Hands**

   Concept card. 5 minutes.

   **Look for:** The problem of many hands (harm that comes from many small contributions, so no one feels responsible) and the phrases people reach for to feel less responsible. You'll hear them in your own meetings.
6. **Consumer Financial Protection Bureau (CFPB), Wells Fargo enforcement action (2016)**

   5 minutes. Free at consumerfinance.gov.
   - [Wells Fargo Bank, N.A. (2016)](https://www.consumerfinance.gov/enforcement/actions/wells-fargo-bank-2016/)

   **Look for:** How sales targets and pay incentives led employees to open accounts customers hadn't asked for.

   **Why trust it:** The CFPB is the US consumer finance regulator, and this is its own page on its September 2016 action, so you're reading what the regulator found and ordered.

   **What you'll get:** A real case where a target number, many people each doing a small part, and customer harm all show up together.
7. **Collect Less**

   Concept card. 5 minutes.

   **Look for:** The test to put to every field you collect: which decision will it change? The card also names data minimization, the principle of collecting no more than a purpose needs.
8. **Bruce Schneier, "Data Is a Toxic Asset, So Why Not Throw It Out?" (2016)**

   7 minutes. Free at schneier.com.
   - [Data Is a Toxic Asset](https://www.schneier.com/essays/archives/2016/03/data_is_a_toxic_asse.html)

   **Look for:** Why he treats stored data as a liability, and what he says organizations should delete.

   **Why trust it:** It's an opinion essay, first published by CNN on 1 March 2016, by a security writer arguing a position. Read it as an argument, not a study.

   **What you'll get:** A reason to collect less that rests on risk to your organization, not only on principle.

## Do

**Consequence scan of one feature you own (35 minutes, plus a conversation).** Pick one feature you own, such as a retry rule for failed card payments, a marketplace search ranking or a rule for filling cancelled hospital appointments. Write one page (25 minutes) that answers the three Consequence Scanning questions in order:

1. What are the intended and unintended consequences? Name each person or group affected, including the people easiest to overlook, such as the seller a ranking pushes down or the patient who can't come in at short notice.
2. Which positive consequences do you want to focus on?
3. Which consequences do you want to mitigate?

Then add two short steps (10 minutes). List each data field the feature collects or keeps, next to the decision that uses it, and mark any field with no decision. Finish with one change you'd propose, in one sentence. The data list may run past the one page, and that's fine.

Afterwards, share the page with an engineer or someone in support and ask what you missed. Book that separately, because it isn't in the 35 minutes. If your company needs approval before you discuss a feature outside the team, ask first.

**Optional: what the number rewards (10 minutes).** Take the main number your feature is judged on, such as bookings per search on a travel site. Write one sentence on the cheapest way to raise it and one on who would pay for that. If the cheapest way harms a customer, name a second measure to watch beside it, such as refund requests or next-day cancellations. The Change Safely module calls this a guardrail measure.

## Check yourself

Answer in your head, then check.

Consequence Scanning has three questions. What are they?

**Answer:** What are the intended and unintended consequences? What are the positive consequences we want to focus on? What are the consequences we want to mitigate?

Sales targets and pay incentives led Wells Fargo employees to open accounts customers didn't ask for. Which two cards explain it?

**Answer:** Goodhart's Law (a measure used as a target stops being a good measure), because the target changed how people behaved. And Many Hands, because each person could say they were only following the targets and the system.

A change lifts hours watched on your streaming service by starting the next episode without asking. Has it created value?

**Answer:** You can't tell from hours watched alone. Ask whether viewers are better off or only up later than they meant to be.

## Go deeper: the full path

Optional, and not counted in the time above.

- **[Harms Modeling](https://learn.microsoft.com/azure/architecture/guide/responsible-innovation/harms-modeling), Microsoft Azure Architecture Center**

  A guidance page. Free at learn.microsoft.com.

  **Why trust it:** It's Microsoft's own guidance, written for architects who design algorithm-driven systems. It lists categories of harm and gives steps for ranking them.

  **What you'll get:** A checklist of harm types, such as denial of consequential services and loss of privacy, and a way to rank harms by severity, scale, probability and frequency.
- **[Designing Responsibility: The Problem of Many Hands in Complex Organizations](https://dash.harvard.edu/server/api/core/bitstreams/7312037e-b8fa-6bd4-e053-0100007fdf3b/content), Dennis Thompson (2017)**

  A book chapter. Free preprint at dash.harvard.edu.

  **Why trust it:** It's a chapter in the book *Designing in Ethics* (Cambridge University Press, 2017), edited by Jeroen van den Hoven, Seumas Miller and Thomas Pogge.

  **What you'll get:** A clear argument that you stay responsible as an individual inside a large organization, and a case for naming who's responsible for the structure.
- **[Right to erasure](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/individual-rights/individual-rights/right-to-erasure/), UK Information Commissioner's Office**

  Guidance, about 15 minutes. Free at ico.org.uk. Read "At a glance" and the checklists, then the answers to "Do we have to tell other organisations about the erasure of personal data?" and "Do we have to erase personal data from backup systems?"

  **Why trust it:** It's the UK data protection regulator's own guidance on the UK GDPR, so it's written for organizations under UK law. Ask your lawyers which rules apply to you.

  **What you'll get:** What a request to erase someone's data asks of a product in practice: a one-month clock, the organizations you shared the data with, and the backups. Every copy is a place the request has to reach.
- **Moral Disengagement in the Perpetration of Inhumanities, Albert Bandura (1999)**

  A journal article. Free at core.ac.uk/download/76471013.pdf.

  **Why trust it:** It appeared in *Personality and Social Psychology Review* in 1999, written by a Stanford psychologist.

  **What you'll get:** The full list of ways people switch off self-criticism. Once you've read it, the phrases in your meetings get easier to recognize.
- **Pinto Fires and Personal Ethics: A Script Analysis of Missed Opportunities, Dennis Gioia (1992)**

  A journal article, in the *Journal of Business Ethics*, volume 11, issues 5 and 6, pages 379 to 389.

  **Why trust it:** Gioia was a recall coordinator at Ford in the early 1970s, and he's writing about his own part in the Pinto case.

  **What you'll get:** A first-person account of how an ethical question never came up, because it wasn't part of how he understood the job.
- **The Tyranny of Metrics, Jerry Muller (2018)**

  A book, published by Princeton University Press.

  **Why trust it:** It's a book-length argument against leaning too hard on measurement, published by Princeton University Press in 2018.

  **What you'll get:** Examples from police, medicine, schools and business of what happens when rewards follow numbers.
- **[Privacy as Contextual Integrity](https://nissenbaum.tech.cornell.edu/papers/H.%20Nissenbaum,%20_Privacy%20as%20Contextual%20Integrity.pdf), Helen Nissenbaum (2004)**

  A law review article. Free at nissenbaum.tech.cornell.edu.

  **Why trust it:** It appeared in the *Washington Law Review*, volume 79, issue 1, and it's where the idea of contextual integrity comes from.

  **What you'll get:** A way to ask whether a use of data fits the setting people shared it in. A consent checkbox doesn't answer that.
- **[Bringing Dark Patterns to Light](https://ftc.gov/reports/bringing-dark-patterns-light), staff of the Federal Trade Commission (FTC) (2022)**

  A staff report. Dark patterns are interface designs that trick or trap people. Free at ftc.gov.

  **Why trust it:** It's a September 2022 report from the US FTC's Bureau of Consumer Protection, and it describes practices the agency has challenged in enforcement cases.

  **What you'll get:** Named cases of interface design that hides terms, blocks cancellation or steers people into sharing data.

# Value Created, Value Captured

## The idea

Value created is the benefit people get from what you build, compared with what they had without it. Value captured is the share your business keeps. The strategy writers Adam Brandenburger and Barry Nalebuff put it this way: creating value is cooperative (you and your customers gain together), and capturing it is competitive (you and your customers split a fixed pot).

A healthy product captures part of what it creates. The trouble starts when capture grows and creation doesn't: you lock customers in, close the exits, or charge for friction you added yourself. A 2008 blog post by Aaron Wall, quoting Tim O'Reilly, reports his rule of thumb: create more value than you capture.

## Why a PM cares

- **Lock-in is capture, not creation.** Lock-in means leaving costs too much. Cory Doctorow describes people who stayed on Facebook because enough of their friends were there, and readers tied to Amazon by locked ebooks. They stayed because leaving cost too much, not because the product got better.
- **Fees for friction take value the customer never got.** The FTC's 2022 staff report on dark patterns (interface designs that trick or trap people) describes cancellation that took six to nine screens in one alleged case. If your revenue depends on a hard exit, you're charging for a problem you built.
- **It tends to cost the business later.** Fred Reichheld and Rob Markey of the consultancy Bain call "profits earned at the expense of customer relationships" bad profits, and argue against them in business terms. Doctorow's version: serve users, then squeeze them, then squeeze the businesses that depend on you.
- **In a game, the cheap capture is the streak.** A reward streak that resets when a player misses a day will lift your daily active count. A player who logs in only to keep it alive gives you their attention and gets nothing they came for. Whether your own mechanics do this is something you can test, for example by looking at how short those sessions are.

## How to spot it

- Customers would leave if leaving were easy, and the cost of leaving is on your feature list.
- A revenue or usage number rises while complaints, cancellations or support tickets don't fall.
- A charge exists only because a step, such as cancelling or changing a booking, was made hard.
- The reason for a feature is "keeps them from leaving", not "helps them do something".

## What it does not say

It does not say a business shouldn't earn. Capturing a fair share of the value you created is the point of having a business. And not every switching cost (what it costs a customer to move to a rival) is a trap: some come from real integration the customer wants. O'Reilly's line, as reported, is a rule of thumb and not a proven law, so use it as a question.

**One question to carry:** If this customer could leave at no cost, would they still choose what we built?

## Go deeper

**[Blowing the whistle on bad profits](https://bain.com/insights/blowing-whistle-on-bad-profits), Fred Reichheld and Rob Markey (2006)**

An article. Free at bain.com.

**Why trust it:** Bain & Company published it in August 2006. It argues for the firm's own measure, the Net Promoter Score (a customer survey score of how likely people are to recommend you), so read it as a case for a method.

**What you'll get:** The split between profit customers would endorse and profit they resent, argued in business terms.

# Many Hands

## The idea

In a large organization, harm often comes from many small contributions, and no one person decides it. Dennis Thompson first analyzed this in 1980 and called it the problem of many hands: so many people contribute that it's hard to say who is responsible. (The chapter under Go deeper is his 2017 return to the idea.) From the inside, it's also easy to feel like a cog.

The psychologist Albert Bandura described how people quiet their own conscience while they do harm. They blame orders (displacement), spread the blame across a group (diffusion), soften the words (euphemistic labeling), or ignore the consequences. The labels under How to spot it follow his list.

## Why a PM cares

- **You're a hand, not a bystander.** Thompson argues that individual responsibility can't be avoided. He tests two things: whether your act was a cause, and whether you could have acted otherwise. "I had no choice" is often a poor excuse, and so is not having noticed.
- **Targets can turn people into cogs.** The US Consumer Financial Protection Bureau (CFPB) found that sales targets and pay incentives led Wells Fargo employees to open accounts without customers' consent. The bank's own analysis found more than two million accounts that may not have been authorized.
- **It happens to decent people.** Dennis Gioia was a recall coordinator at Ford in the early 1970s. He later analyzed his own part in the Pinto case and concluded that his mental scripts had no ethical dimension. In his words, quoted by Penn State: "If it could happen to me, it could happen to anybody."
- **Responsibility can be designed in.** Thompson proposes naming who's responsible for the structure before anything fails. For you, that means naming an owner for each harm you can foresee, writing the risk into the record of the decision (a ticket, memo or meeting notes), and saying it out loud in the meeting. The step from Thompson to those actions is this syllabus's suggestion, not his.

## How to spot it

- Displacement: "The business asked for it." You're treating yourself as an instrument.
- Diffusion: "It passed launch review, and everyone agreed." Each person assumes someone else is carrying the concern.
- Soft labels (euphemism): "engagement" or "retention" for what users experience as pressure.
- Distance: the harm lands in a support queue, a refund claim or a late shift you never see, so it feels like no one's problem.

## What it does not say

It does not say you're as guilty as the person who made the decision, or that you have to refuse every request you dislike. Thompson's point is that responsibility is shared, and a share isn't nothing. Yours is usually to see the consequence, say it clearly, and make sure someone owns it.

**One question to carry:** If this harms a customer, whose name would be on the decision, and is it anyone's yet?

## Go deeper

**[Designing Responsibility: The Problem of Many Hands in Complex Organizations](https://dash.harvard.edu/server/api/core/bitstreams/7312037e-b8fa-6bd4-e053-0100007fdf3b/content), Dennis Thompson (2017)**

A book chapter. Free preprint at dash.harvard.edu.

**Why trust it:** It's a chapter in the book *Designing in Ethics* (Cambridge University Press, 2017), edited by Jeroen van den Hoven, Seumas Miller and Thomas Pogge.

**What you'll get:** A worked argument for why you stay responsible inside an organization, and which structures help.

# Collect Less

## The idea

Every field you collect has a cost. The person it describes is exposed if it leaks or gets misused, and your organization has to keep it secure. So collect only what a decision needs, and keep it only as long as that decision needs it.

Bruce Schneier calls stored personal data a toxic asset: easy to keep, hard to protect, damaging when breached. Helen Nissenbaum adds that privacy depends on context, an idea she calls contextual integrity. What you tell a doctor fits that setting, and the same details passed to your employer may not. Where the EU General Data Protection Regulation (GDPR) applies, data minimization is a legal principle: personal data should be limited to what's necessary for its purpose.

## Why a PM cares

- **Wanting more data is the default.** It feels safe to have, because it might answer a question later. Schneier names hype around big data and underestimating breach risk as reasons organizations keep too much. Jerry Muller calls the wider habit of trusting numbers over judgment metric fixation.
- **Hitting a number can mean steering people.** On a developer tool, a target for installs that send usage telemetry can tempt a team toward a setup prompt where yes is one keystroke and no is a config file. The 2022 staff report of the US Federal Trade Commission (FTC) describes defaults that maximize data collection and privacy choices designed to steer people to share.
- **These patterns are common.** Dark patterns are interface designs that trick or trap people. A 2019 study of about 11,000 shopping websites found 1,818 instances (each a dark pattern found on a site), and some were sold by third parties as ready-made products. Your product probably isn't a shopping site, so read this as a sign of how widespread the tricks are, not a measure of your own company.
- **Reuse can break the original promise.** The quiz answers a student gave you to get feedback weren't given to help you pick which parents to sell tutoring to. Nissenbaum's test is whether the use fits the setting the data came from.

## How to spot it

- A field is collected "in case we need it", with no named decision.
- Event tracking gets added to every click, and a dashboard no one acts on stays alive.
- A cookie banner where accept is one tap and decline takes several steps.
- Data stays long after its purpose has ended, because nobody owns deleting it.
- Someone asks to have their data erased, and nobody can list every place it was copied.

## What it does not say

It does not say never to measure. Measuring is how you learn whether you're helping, and some records you have to keep by law. The rule is to name the decision before you collect: if no decision uses a field, stop collecting it or delete it. The specific legal rules belong to your company's lawyers. Your job is to ask the question early.

**One question to carry:** What decision will this data change, and who is exposed while we hold it?

## Go deeper

**[Data Is a Toxic Asset, So Why Not Throw It Out?](https://www.schneier.com/essays/archives/2016/03/data_is_a_toxic_asse.html), Bruce Schneier (2016)**

An opinion essay. Free at schneier.com.

**Why trust it:** CNN first published it on 1 March 2016. It argues a position, and it backs that with examples of breaches in 2015.

**What you'll get:** A short case for deleting data, with the reasons organizations keep it and what he proposes instead.

# Consequence Scanning

## The idea

Consequence Scanning is a short team conversation, before a feature is built, about everything it could cause. Doteveryone, a responsible technology think tank, built it around three questions, and its manual (2019) is credited to Sam Brown, who ran the program: "What are the intended and unintended consequences of this product or feature?" "What are the positive consequences we want to focus on?" "What are the consequences we want to mitigate?"

Run it when a product starts, in roadmap planning and as you shape a feature, in 45 minutes to an hour. Everyone writes consequences alone first, so the most senior voice doesn't set the list. Post them, group them, and take a second quiet round. Then sort them into what the team can act on, what it can only influence and what it can only monitor, and spend most of the time there. Mark which are positive and which to mitigate. Don't close until each one you can act on has an owner and a place in the backlog.

## Why a PM cares

- **The unintended consequences land on people who aren't in the room.** Picture a city council moving parking permit renewals online only. Shorter queues are intended. Locking out residents who don't have a smartphone isn't. You can make the room look for them.
- **Ask the misuse question out loud.** Nat Pryce asks: "could people misuse this feature to harass/attack/abuse/defraud our users?" A mobile carrier's family location sharing helps a parent see that a teenager got home. It also lets a controlling partner track someone who doesn't know it's on, and no test will catch that.
- **Scale changes the answer.** One of the method's prompts asks, "What could this mean if everyone in the world were doing it?" A rule that's harmless for a hundred people acts like a policy for a million.
- **It turns worry into owners.** Naming who owns each harm is the Many Hands card's advice, built into a meeting you'd hold anyway.

## How to spot it

- Launch reviews ask whether it works and whether it's on time, never who it could hurt.
- Every risk in the plan is a risk to the team: a late date, a missed target.
- An insurance claims model flags claims as suspicious, and nobody has asked what happens to an honest claimant it flags.
- You first hear about a harm from support, a journalist or a regulator.

## What it does not say

It won't show you every consequence. Some appear only after launch, so scan again once it's live. It isn't a sign-off: a scan that ends with "no concerns" every time has stopped looking. It doesn't rank harms by how bad they are; Microsoft's Harms Modeling, on this module's full path, does that. And it doesn't decide for you. Whoever owns the product still makes the call.

**One question to carry:** Who will this feature affect who'll never be in our planning meeting, and what would they ask us to change?

## Go deeper

**[Consequence Scanning](https://www.adalovelaceinstitute.org/resource/doteveryone-consequence-scanning/), Doteveryone (2019)**

The method's own page, with its manual and prompt cards, about 20 minutes. Free at adalovelaceinstitute.org, which keeps Doteveryone's work since the think tank closed in 2020.

**Why trust it:** It's from the method's designers, so it describes a tool rather than testing one: practitioners' guidance, not evidence that it works.

**What you'll get:** The method as its authors meant it to run, with prompts that push a team past the obvious.

*To check: the method's page and its manual (Version 1, April 2019) were opened on 20 November 2026, and the three questions, the steps, the timing, the "everyone in the world" prompt and Sam Brown's credit were checked against them. Still open: Pryce's question comes from deck p. 295, which names no work for him, and a search found no original.*
