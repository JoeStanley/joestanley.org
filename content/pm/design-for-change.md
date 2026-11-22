---
title: Design for Change
layout: module
module: design-for-change
question: What will change, how fast, and what should be easy to change?
one_thing: Before your next request is estimated, write down the slowest layer you think it touches.
do_minutes: 35

last_time:
  - q: Besides the question itself, which four things make an access pattern?
    a: Who asks it, how often, how fast and how fresh.
  - q: Why do reports usually read a copy of the data, not the live system?
    a: Reports ask different questions than running the service does, so they get a copy of their own. The fresher that copy has to be, the more machinery it takes to keep it so.

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
    trust: It's Brand's own, a chapter from his book whose message has resonated for decades at this point, refined through constructive feedback along the way.
    only: Why each layer needs its own pace, from the person who drew the layers.
  - id: card-coupling
    kind: card
    card: cards/coupling
    minutes: 5
    look: The question to ask whenever someone says two parts are tightly coupled.

check:
  - q: Letting a student join two classes at once looks small on screen. Why might it take a quarter?
    a: The slowest layer it touches sets the cost. If it reaches into the data model, a core system or a contract, it moves at that layer's pace.
  - q: An engineer says search and the inventory system are tightly coupled. What do you ask?
    a: For which change? Parts are coupled only with respect to a particular change, so name the one you expect and ask whether it would make both move.
  - q: A small change needed edits in a dozen places, then broke something nobody expected. How do you describe it without naming a culprit?
    a: "Name the symptoms: change amplification, then an unknown unknown. Both describe the design, not the people, and both show where it could be cheaper to change."

deeper:
  - title: How Buildings Learn
    by: Stewart Brand
    where: A book.
    note: "Start with the chapters \"Shearing Layers\" and \"The Scenario-Buffered Building.\""
    trust: Brand grew the architect Frank Duffy's four layers into six. He makes his case as a writer, from real buildings and how they changed.
    only: "The building version that pace layering grew from, and the case for designing for several futures instead of one forecast. In his words, \"All buildings are predictions. All predictions are wrong.\""
  - title: Seeing Like a State
    by: James C. Scott
    where: A book.
    note: "Read the introduction, then chapter 1, \"Nature and Space,\" on the scientific forestry of eighteenth-century Prussia and Saxony, and chapter 10, \"Conclusion.\" It's dense in places, so take your time as needed."
    trust: This is an industry classic for a reason. Scott was a political scientist and anthropologist at Yale. He builds his case from real schemes, from a planned capital city to collectivized farms, showing how in complex dynamics even the smartest and wisest continue to assume an overly predictable world.
    only: "Why planners sure of one future build what can't change, and four rules for doing better that are applicable to our own work: \"Take small steps.\" \"Favor reversibility.\" \"Plan on surprises.\" \"Plan on human inventiveness.\""
  - title: A Philosophy of Software Design
    by: John Ousterhout
    where: A book.
    note: Read it whole. Chapters 2 and 3, on complexity and on tactical against strategic work, are the heart of it for this module.
    trust: Ousterhout taught a software design course at Stanford, and the book grew out of it. It's one designer's view, argued from experience, and another industry classic.
    only: The three symptoms of complexity in full, and the difference between tactical work, which gets this feature out, and strategic work, which keeps the next one cheap. That difference is the case you can make for engineering time.
  - title: On the Criteria To Be Used in Decomposing Systems into Modules
    by: David Parnas (Communications of the ACM, 1972)
    where: A journal article.
    note: It's short and dense, so read it slowly. The argument is in his comparison of two ways to split the same program, and you can skim the technical detail.
    trust: It's the classic case for information hiding, keeping each decision likely to change inside one module. He argues it from a single worked example.
    only: Why a system's boundaries go around the decisions likely to change. Engineers can draw them only as well as they know what's coming, and often you're the one who knows.
  - title: Yes Minister
    by: written by Antony Jay and Jonathan Lynn (BBC, 1980)
    where: A TV series.
    note: "Watch series 1, episode 4, \"Big Brother.\" A new minister wants safeguards on a national database. His predecessor drafted the same ones. He tells the new minister how the permanent secretary stalled them, one polite stage at a time, until an election took him out of office and the department wiped the slate clean."
    only: Pace layers in a government department. Ministers come and go while the civil service stays, so a change that has to pass through it moves at its speed.
---

## Why this matters

Ask how your product will change over time: which parts, how often, and at what cost. The slowest layer a request touches sets its {{< pm/term "cost-of-change" "cost of change" >}}, so the pain comes from fast parts tied to slow ones. Once you can see which is which, you'll estimate more honestly, and you'll have a case for the work that makes likely changes cheap.

Slow isn't the enemy, though. A payments ledger moves slowly on purpose, because every balance depends on it. Each layer has its own right pace, which Stewart Brand calls {{< pm/term "pace-layers" "pace layering" >}}: "Fast learns, slow remembers." Some slow layers aren't yours. Your customers' phones change at their own pace, so retiring an old app version saves your team the upkeep and hands the bill to people who can't update, often those on the oldest or cheapest phones.

There's a precise word for what makes a change costly: {{< pm/term "complexity" >}}. John Ousterhout uses it for anything in a system's structure that makes it hard to understand and change, and names three symptoms. Change amplification is a simple change that needs edits in many places. {{< pm/term "cognitive-load" "Cognitive load" >}} is how much you must know to make a change safely. And with unknown unknowns, nobody can tell in advance what a change will touch. With those words, you can say why a small request took a month without blaming anyone.

[//]: # (short-path)

## Do

**List your product's layers (25 minutes).** Take one product or journey you own and list its parts from fastest-changing to slowest: wording, screens, business rules, APIs, the data model, core systems of record, the contracts and laws it must meet. Note how often each changed in the last year. Then take the last request that ran long. Which layers did it touch, and which symptom of complexity showed?

**Optional: walk a likely change (10 minutes).** This walk comes from Ruth Malan's workshop notes (February 2025, p. 329): architects run an anticipated change across a design while it's still cheap to change. Pick a change you expect next year, such as a second currency at checkout, and trace the parts it would touch. Then ask a tech lead: "If we did this, which parts would have to change?" If most would, what boundary would have contained it?

## Questions to bring to engineers

- Which of these layers is hardest to change, and why?
- Where in our system is change amplification worst?
- Is the pattern you're proposing earning its complexity, or would a plainer design do?
