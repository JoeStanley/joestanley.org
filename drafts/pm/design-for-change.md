About 1 hour.

**If you only do one thing:** Before your next request is estimated, write down the slowest layer you think it touches.

## Why this matters

Ask how your product will change over time: which parts, how often, and at what cost. The slowest layer a request touches sets its cost of change, so the pain comes from fast parts tied to slow ones. Once you can see which is which, you'll estimate more honestly, and you'll have a case for the work that makes likely changes cheap.

Engineers have a precise word for what makes a change costly: complexity, anything in a system's structure that makes it hard to understand and change. John Ousterhout names three symptoms. Change amplification is a simple change that needs edits in many places. Cognitive load is how much you must know to make a change safely. And with unknown unknowns, nobody knows what a change will touch until something breaks. With those words, you can say why a small request took a month without blaming anyone.

## The short path

1. **Pace Layers**

   Concept card. 5 minutes.

   **Look for:** Why the slowest layer a change touches sets its price.
2. **Stewart Brand, "Pace Layering: How Complex Systems Learn and Keep Learning" (2018)**

   15 minutes. Free at jods.mitpress.mit.edu.

   **Look for:** Two points: the slow layers govern the fast ones, and a layer forced to another's pace ends badly, whichever way the push goes.

   **Why trust it:** It's Brand's own, written nearly twenty years after he set out pace layering in *The Clock of the Long Now* (1999). He argues from history and ecology, not from measurement.

   **What you'll get:** Why each layer needs its own pace, in a free essay by the person who drew the layers.
3. **Coupling Is About a Change**

   Concept card. 5 minutes.

   **Look for:** The question to ask whenever someone says two parts are tightly coupled.

## Do

**List your product's layers (25 minutes).** Take one product or journey you own and list its parts from fastest-changing to slowest: wording, screens, business rules, APIs, the data model, core systems of record, the contracts and laws it must meet. Note how often each changed in the last year. Then place the last request that ran long. Which layers did it touch, and which symptom of complexity showed?

**Optional: walk a likely change (10 minutes).** This walk comes from Ruth Malan's workshop notes (February 2025, p. 329): architects run an anticipated change across a design while it's still cheap to change. Pick a change you expect next year, such as a second currency at checkout, and trace the parts it would touch. Then ask a tech lead: "If we did this, which parts would have to change?" If most would, what boundary would have contained it?

## Questions to bring to engineers

- Which of these layers is hardest to change, and why?
- Where in our system is change amplification worst?
- Is this pattern earning its complexity here, or would a plainer design do?

## Check yourself

Answer in your head, then check.

Letting a student join two classes at once looks small on screen. Why might it take a quarter?

**Answer:** The slowest layer it touches sets the cost. If it reaches into the data model, a core system or a contract, it moves at that layer's pace.

An engineer says search and the inventory system are tightly coupled. What do you ask?

**Answer:** For which change? Parts are coupled only with respect to a particular change, so name the one you expect and ask whether it would make both move.

A small change needed edits in a dozen places, then broke something nobody expected. How do you describe it without naming a culprit?

**Answer:** Name the symptoms: change amplification, then an unknown unknown. Both describe the design, not the people, and both show where it could be cheaper to change.

## Go deeper: the full path

Optional, and not counted in the time above.

- **How Buildings Learn, Stewart Brand (1994)** A book. Start with chapter 2, "Shearing Layers", and chapter 11, "The Scenario-buffered Building". **Why trust it:** Brand built the layers out from the architect Frank Duffy's work and tested them on real buildings, photographed as they changed. It's a writer's case from observation, not a study. **What you'll get:** The layers in their first form, and chapter 11's case for designing for several possible futures instead of one forecast. In his words, "All buildings are predictions. All predictions are wrong."
- **"On the Criteria To Be Used in Decomposing Systems into Modules," David Parnas (*Communications of the ACM*, 1972)** A paper of six pages. The argument is in his comparison of two ways to split the same program, so you can skim the technical detail. **Why trust it:** It's where Parnas set out information hiding, in a peer-reviewed journal. **What you'll get:** Why a system's boundaries go around the decisions likely to change. Engineers can draw them only as well as they know what's coming, and often you're the one who knows.
- **A Philosophy of Software Design, second edition, John Ousterhout (2021)** A book. Read chapters 2 and 3, about 30 minutes, or watch his talk at Google (2018), free on YouTube, about an hour. **Why trust it:** Ousterhout teaches computer science at Stanford, and the book grew out of his course in software design there. It's one designer's view, argued from experience. **What you'll get:** The three symptoms in full, and the difference between tactical work, which gets this feature out, and strategic work, which keeps the next one cheap. That difference is the case you can make for engineering time.
- **"Big Ball of Mud," Brian Foote and Joseph Yoder (1997)** Free at laputan.org. Read the section "Shearing Layers". **Why trust it:** Two software researchers wrote it for a patterns conference, from what they'd seen in real systems. **What you'll get:** Brand's shearing layers carried into software, by engineers, for engineers.
- **"CQRS," Martin Fowler (2011)** Free at martinfowler.com, 5 minutes. CQRS uses separate models for writing data and for reading it, and you can skim how. **Why trust it:** Fowler, a software developer who's written about design for years, has seen the pattern on real projects, and he says most of the cases he met went poorly. **What you'll get:** A worked case of asking whether a pattern earns its complexity, with his question: is the benefit worth the jump?
- ***Yes Minister*, "Big Brother", written by Antony Jay and Jonathan Lynn (BBC, 1980)** A TV series. One half-hour episode will do, series 1, episode 4. A new minister wants safeguards on a national database. His predecessor drafted the same ones, and tells him how the permanent secretary stalled them, one polite stage at a time, until an election took the minister away and the department wiped the slate clean. **What you'll get:** Pace layers in a government department. Ministers come and go while the civil service stays, so a change that has to pass through it moves at its speed.

*To check: name one of the cases in Brand's essay where a layer was forced to the wrong pace, and check that the essay makes both points its "Look for" names. Find a free copy of Parnas's paper. The reasons to trust How Buildings Learn, Parnas's paper, Ousterhout's book and "Big Ball of Mud" were written for this draft without opening them: check each against the work.*

## For the glossary

- **Pace layers:** Parts of a building, a society or a product that change at different speeds, with the slow ones setting the terms for the fast. Brand's shearing layers are a building's version.
- **Cost of change:** What it would take to undo or redo a decision later.
- **Coupling:** How far a change to one part forces a change to another, judged for a particular change.
- **Complexity:** In John Ousterhout's sense, anything in a system's structure that makes it hard to understand and change. Its symptoms are change amplification, cognitive load and unknown unknowns.
- **Cognitive load:** How much someone has to know to make a change safely.

# Coupling Is About a Change

*Picture: A plan catalog and a billing system. A price change touches one, and a new kind of charge pulls a line through both.*

## The idea

"Are these two parts coupled?" has no useful answer until you name the change. In a 2020 talk, Kent Beck put it this way: two parts are coupled "with respect to a particular change" if changing one means changing the other. A phone company's plan catalog and billing system can be independent when a price changes, and welded together when a new kind of charge arrives.

Michael Nygard names five kinds, and two land on your roadmap: development coupling, where "changes in producer and consumer must be co-ordinated", and semantic coupling, where parts change together because they share a concept.

## Why a PM cares

- **You often know which changes are coming.** When an engineer says two systems are tightly coupled, ask: for which change? Then name the one you expect, such as new eligibility rules on a benefits service.
- **Development coupling goes on the plan.** Each change two teams must coordinate costs meetings, a joint release and waiting. Name it when you plan, or meet it in week six.

## How to spot it

- A small change needs two teams to release on the same day.
- The same two services change together, release after release.
- Two services that never call each other still change together, because both rely on the same idea of a delivery zone.

## What it does not say

It does not say coupling is bad: a checkout that isn't coupled to its prices can't charge anyone. Decoupling costs something too, so pay for it where the likely changes are.

**One question to carry:** For the change you most expect next year, which teams would have to ship together?

## Go deeper

**[Uncoupling](https://www.youtube.com/watch?v=EirOknZJvYc), Michael Nygard (2018)**

His SATURN 2018 keynote, about an hour. Free on YouTube.

**Why trust it:** Nygard is a software architect and wrote *Release It!*. It's one practitioner's talk, not research.

**What you'll get:** All five kinds, from the person who drew them up.

*To check: nobody has watched a source for this card. YouTube's search listing, read on 20 November 2026, gives the talks' titles, years and lengths: Beck's "The Beauty of Maintenance" is at youtube.com/watch?v=3gib0hKYjB0 (DDD Europe 2020, 56 minutes), and Nygard's "Uncoupling" was the SATURN 2018 keynote (57 minutes), also given at DevOpsDays DFW and JDD 2019. YouTube answers automated requests for a video with a bot check, so neither could be watched. Beck's definition (deck p. 366) and Nygard's kinds (p. 364) are quoted from the deck's copies of their slides: check them against the talks, and check that the SATURN version has Nygard's five kinds. Beck's talk is the source of the quoted definition. His book Tidy First? (2023) may suit the full path.*

# Pace Layers

*Picture: A building cut open to show its layers, site to furniture, each marked with how often it changes, beside the same stack for a software product.*

## The idea

A building is a stack of layers that change at different speeds: the structure may last centuries, while the furniture moves weekly. The architect Frank Duffy made the point, and Stewart Brand built it into six shearing layers in *How Buildings Learn* (1994). Buildings that adapt well let each layer change without tearing up the slower one beneath it. Brand later widened the idea to whole societies as pace layering: "Fast learns, slow remembers."

## Why a PM cares

- **The slowest layer sets the price.** Letting a student join two classes looks small on screen. If it reaches down into the data model or a contract, you're looking at a quarter.
- **Each layer has its own right speed.** Trouble starts when one is forced to the wrong pace: a data model change rushed at sprint speed, or a wording fix held for a quarterly release.
- **Slow isn't the enemy.** A payments ledger moves slowly on purpose, because every balance depends on it.

## How to spot it

- A small request turns into a long project once someone checks what it rests on.
- Everything built on one core system ships on that system's calendar.
- People get around a slow layer with a hard-coded rule, a shadow spreadsheet or a manual step.

## What it does not say

It does not say the layers are laws. They're rules of thumb from buildings and Brand's reading of history, so redraw them for your own product.

**One question to carry:** Which layer does this change really live in, and what slower layer does it rest on?

## Go deeper

**[How Buildings Learn, episode 6, "Shearing Layers"](https://www.youtube.com/channel/UCjBdRnkOB5P85yki3rAvGUw), BBC (1997)**

Half an hour. Free on Stewart Brand's YouTube channel.

**Why trust it:** The BBC made Brand's book into this series, and it's on his own channel. It shows more than it argues.

**What you'll get:** The layers on real buildings, and what gives when one changes.

*To check: the draft doesn't record anyone watching episode 6. Check its title, its length and that it shows the shearing layers.*
