## Why this matters

Engineers mean something precise by complexity, quality and consistency (see "Terms you will meet"), and a request that sounds small can strain all three. Once you know what they mean, you can write a quality need someone can test, and you'll see early where data makes a change slow or risky.

## Short path (about two hours of reading, plus an hour for the exercises)

The deck isn't a book. It's a 514-page set of workshop slide notes written for software architects, so read only the pages named here, and only the parts named. Terms you don't know are defined under "Terms you will meet", below. If you split the path across two sittings, stop after step 4.

1. *A Philosophy of Software Design* (Ousterhout, second edition, 2021), chapter 2, "The Nature of Complexity" (about 20 minutes).
2. The same book, chapter 3, "Working Code Isn't Enough" (about 15 minutes), on tactical and strategic programming. If you can't get the book this week, watch Ousterhout's [talk at Google](https://www.youtube.com/watch?v=bmSAYlu0NcY) (2018, free on YouTube) in place of steps 1 and 2 (62 minutes instead of 35).
3. Deck pp. 418, 422 and 424 (about 10 minutes). On p. 418, read the TWA story on the slide and the first column beneath it, under "Who Defines and Refines Quality Attributes?" On p. 422, you only need the airline examples on the slide. On p. 424, look at the diagram on the slide, then read the short paragraph and the three-line example beneath it. Skip the rest.
4. *Designing Data-Intensive Applications* (Kleppmann and Riccomini, second edition, 2026), chapter 2, "Defining Nonfunctional Requirements" (about 35 minutes). Skim the opening case study on social network timelines, then read "Describing Performance", "Reliability and Fault Tolerance" and "Maintainability". You can skip "Scalability". With the first edition (2017), read its chapter 1, "Reliable, Scalable, and Maintainable Applications", instead (about 35 minutes), and skip "Scalability" there too.
5. The same book, chapter 1, "Trade-Offs in Data Systems Architecture" (about 25 minutes). Skim "Operational Versus Analytical Systems", then read "Systems of Record and Derived Data" and "Data Systems, Law, and Society". Skip the rest. With the first edition, read the introduction to Part III, "Derived Data" (about 5 minutes), and for the law add the UK regulator's free ["Right to erasure"](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/individual-rights/individual-rights/right-to-erasure/) (about 15 minutes).
6. Deck pp. 256 and 257 (about 10 minutes). On p. 256, read the right-hand column of the slide and the paragraph headed "Eventual Consistency" at the bottom. On p. 257, read the Michael Feathers quote on the right of the slide and the large Vladik Khononov quote beneath it, then the sentence at bottom left that begins "The bottom line". Skip the rest.
7. Deck p. 346 (about 5 minutes). Read only the first two paragraphs beneath the slide, starting with the one that begins "A System Context diagram". Skip the rest.
8. Deck p. 481 (about 5 minutes). Look at the template on the slide, then read the paragraphs beneath it that begin "Service Level" and "Notes". Skip the rest.

## Full path

- *A Philosophy of Software Design*, chapter 11, "Design it Twice" (about 15 minutes), on sketching more than one design before you choose, and chapter 21, "Decide What Matters" (about 15 minutes).
- The rest of chapters 1 and 2 of *Designing Data-Intensive Applications* (about 50 minutes), then chapter 14, "Doing the Right Thing" (about an hour), on bias, privacy and legislation.
- Keeling, *Design It!* (2017), the free excerpt ["Activities to Understand the Problem"](https://media.pragprog.com/titles/mkdsa/activities.pdf) (about 20 minutes). Free at pragprog.com.
- Deck pp. 412 to 452, on quality attributes (about 45 minutes): start with pp. 415, 420, 423 and 431, then pp. 445 to 452, on robustness and resilience.
- Deck pp. 243 to 270, on architecture styles (about 45 minutes), and pp. 336 to 383, on sketching and modeling (about 30 minutes): start with pp. 341, 343 to 345, 376, 378 and 381. Deck pp. 464 to 485, on interfaces (about 15 minutes): start with pp. 466, 468 and 485.

## Terms you will meet

- **Complexity (Ousterhout's sense):** anything in a system's structure that makes it hard to understand and change.
- **The three symptoms of complexity:** Ousterhout's names for how complexity shows up.
  - **Change amplification:** a simple change needs edits in many places.
  - **Cognitive load:** how much a developer must know to make a change safely.
  - **Unknown unknowns:** it isn't clear what must change until something breaks.
- **Tactical and strategic programming:** tactical work gets the current feature working fast; strategic work also invests in a design that makes later changes easier.
- **Quality attribute:** how well a system does its job, such as speed, availability or ease of change; also called a nonfunctional requirement.
- **Quality attribute scenario:** a quality written as a test. It names what triggers an event, under which conditions, which part of the system responds, and how the response is measured (deck p. 424). Example: "When 500 students submit their exams in the same minute at the deadline, the submission service confirms 99 in 100 within 3 seconds."
- **Percentile:** the time within which a given share of requests finish: p99 of 2 seconds means 99 in 100 finish within 2 seconds; the median (p50) is the middle one.
- **Reliability and fault tolerance:** continuing to work correctly when parts fail; fault tolerance keeps a failure from reaching customers.
- **System of record:** the system holding the authoritative copy of some data.
- **Derived data:** data built from a system of record, such as a cache (a fast local copy) or a report; it can be rebuilt, but can be out of date.
- **Monolith and microservices:** a monolith is deployed as one unit; microservices are many small services talking over a network (deck p. 254).
- **Transaction and eventual consistency:** a transaction is a group of changes that succeed or fail together; with eventual consistency, copies may disagree for a while and catch up later.
- **Service level:** the quality an interface (the agreed way one part of a system talks to another) promises, such as a response time (deck p. 481).
- **Context diagram:** your system as one box, surrounded by its users and the other systems it exchanges data with (deck p. 346).
- **Data minimization:** collecting only the personal data you need; privacy rules such as the EU's GDPR also let people ask for deletion.

## What to look for

- **Ask for the need behind the specification.** TWA asked for three engines when what it really needed was to fly safely with one engine out (p. 418). The qualities developers need, such as ease of change, often get missed.
- **A quality is not a requirement until it can be tested.** Nobody can build "fast", or check it; pp. 422 and 424 show qualities written as scenarios with a response you can measure.
- **An average hides the customers who wait.** Notice why Kleppmann and Riccomini prefer the median and high percentiles. The next time someone quotes you an average, ask for the 99th percentile.
- **Every copy of data is a promise to keep it in step.** When a screen is stale, two reports disagree or a deletion gets missed, there's often a copy behind it.
- **Splitting a system often moves complexity rather than removing it.** Remote calls are slow, and they can fail (pp. 256 and 257). Khononov's point is that the cost of change runs away because a design is tangled, not because it's a monolith.

## Apply it to your own work

Each time below covers your own first pass. The conversation with a colleague comes on top.

1. State one quality as a testable scenario, in about 20 minutes. Pick a quality your users would notice if it slipped, such as how quickly a video starts playing on a Friday evening. Write it in the parts shown on p. 424. Question to bring to your tech lead: "Do we measure this today, and what would it take to meet it?"
2. Find where one piece of data lives, in about 30 minutes. Pick one data item your product creates or uses, such as a patient's phone number or a driver's home address. Sketch a context diagram as on p. 346: your system as one box, surrounded by the people and systems that send or receive this item. Mark the system of record, then every copy you know of: reports, the data warehouse, other teams' systems, vendors. Next to each copy, note who depends on it, as the "Notes" on p. 481 suggest. Now ask yourself two things. If the person it belongs to asked you to erase it, which copies would you miss? And does each copy need it at all (data minimization)? Question to bring to a tech lead or data engineer: "How long after a change does each copy catch up?"
3. Name the complexity you're paying for, in about 15 minutes. Think of a recent change that took far longer than its size suggested. Which of the three symptoms of complexity showed up? Questions to bring to your tech lead: "Where in our system is this symptom worst?" and "What would a small strategic investment there cost, and what would it save?"

## Check your own thinking

This module is after one shift: from "make it fast and reliable" to "99 in 100 within 3 seconds, and I know where the data lives". Here's how to test yourself. Before your next feature goes to refinement, write one quality scenario with a number in it. List every system that holds the data it touches, then count how many your tech lead adds. Expect a few, because copies are easy to miss. If you'd like a sounding board, take your scenario and your data sketch to your manager or a mentor.

> Deck page references are to Ruth Malan's System Design and Software Architecture workshop notes, February to March 2025 edition. This guide is an independent companion; it has not been reviewed or endorsed by Ruth Malan.

# Models That Are Sometimes Wrong

*Picture: A model chooses, the customer responds, and the response becomes the data the model learns from next. The loop closes without anyone deciding it should.*

## The idea

A model or rule that picks which listings a marketplace shows a shopper first will sometimes pick badly. That's built in: it predicts from past patterns, and the future differs. It's tempting to demand a model that's never wrong, but there isn't one. Your job is to know how often it's wrong, who's affected, and how you'll find out.

Four practices make that knowable:

1. **Evaluate before launch** on data the model never saw, either held back on purpose or from an earlier period. Score a model on its own training data (the past examples it learned from) and its errors stay hidden.
2. **Test in production** with champion and challenger. In a typical setup, the current approach (the champion) keeps most of the traffic and a new one (the challenger) gets a small share, so a bad result stays contained.
3. **Watch for feedback loops.** A feedback loop is when a model's outputs change the data it later learns from. The listing shown first gets the clicks, and the clicks keep it first.
4. **Budget for upkeep.** Sculley and nine co-authors argue that machine learning's quick early gains come with large, ongoing maintenance costs.

## Why a PM cares

- **A good launch score is not a guarantee.** Evaluation on past data tells you how the model would have done. Only live monitoring tells you how it's doing now.
- **Loops bend your data.** If the model only learns from the listings it chose to show, it never finds out how the rest would have done. Sculley et al. name randomization as one remedy: sometimes picking the first listing at random, so the data also shows how the other options would have done.
- **Changes ripple.** Sculley et al. call this "changing anything changes everything". The parts of a model are entangled, so when you tweak one, the others shift.
- **Hidden users of a score.** Other systems may be reading a model's scores without anyone having declared it, so a change can break something you didn't know was there.
- **Regulators have a name for this.** In US banking, SR 11-7 defines model risk as the potential for adverse consequences from decisions based on incorrect or misused model outputs. It expects independent validation, comparison with actual outcomes, and ongoing monitoring.

## How to spot it

- A launch review shows one accuracy number and no test on separate data.
- A challenger test has no stop rule, or it takes a large share of customers at once.
- Nobody can say which systems read the model's scores.
- Results drift slowly, though nobody has touched the model.

## What it does not say

SR 11-7 is US banking guidance, from the Federal Reserve and the Office of the Comptroller of the Currency (OCC, a US bank regulator) in 2011. It applies to the banking organizations those agencies supervise, in proportion to their size and complexity and how much they use models. It may not apply to your industry, so ask whoever handles legal and risk questions where you work which model rules cover you. One more caution: champion and challenger testing isn't free of harm. A challenger is still a live decision about real customers.

**One question to carry:** If this model were quietly wrong next month, what would tell us, and who would see it first?

## Go deeper

**[Hidden Technical Debt in Machine Learning Systems](https://proceedings.neurips.cc/paper_files/paper/2015/file/86df7dcfd896fcaf2674f757a2463eba-Paper.pdf), D. Sculley and nine co-authors (2015)**

A conference paper from NeurIPS. Free at proceedings.neurips.cc.

**Why trust it:** It's a conference paper, presented at NeurIPS (a machine learning conference) in 2015, and all ten authors were at Google when it was published. The tools it mentions are dated, so skim past them.

**What you'll get:** Names for risks you can ask your engineers about: feedback loops, entanglement (changes spreading through linked parts), undeclared consumers (unlisted systems that use a model's output) and changes in the outside world.

**[SR 11-7: Guidance on Model Risk Management](https://www.federalreserve.gov/supervisionreg/srletters/sr1107.htm), Federal Reserve and Office of the Comptroller of the Currency (2011)**

A regulatory letter. Free at federalreserve.gov.

**Why trust it:** It's the primary text, issued by US banking regulators. Bear in mind that it's written for banks.

**What you'll get:** The regulator's own wording on validation, outcomes analysis and monitoring.
