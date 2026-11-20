## Why this matters

Most PM questions are about what to build next. Ask about time as well: which parts of your product will change, how often, and what each change will cost. A lot of the pain of change comes from fast-changing parts tied to slow-changing ones. Once you can see which is which, you'll estimate more honestly, sequence work better, and have a case for the engineering work that makes likely changes cheap.

Engineers have a precise word for what makes a change costly: complexity, meaning anything in a system's structure that makes it hard to understand and change. Learn what they mean by it, and you can name why a small request took a month without blaming anyone.

## Short path (about two and a half hours of reading and viewing, plus an hour for the exercises)

The deck is a 514-page set of workshop slide notes written for software architects, not a book. You don't need most of it: read only the pages named here, and only the parts named. Terms you don't know are defined under "Terms you will meet", below. If you split the path across two sittings, stop after step 4.

1. The **Pace Layers** concept card (10 minutes).
2. *How Buildings Learn* (Brand), chapter 2, "Shearing Layers" (about 40 minutes). It's a short chapter with plenty of pictures. If you can't get the book this week, watch episode 6 of the BBC series of the same name instead (30 minutes, free on [Stewart Brand's YouTube channel](https://www.youtube.com/channel/UCjBdRnkOB5P85yki3rAvGUw)).
3. Brand, ["Pace Layering: How Complex Systems Learn and Keep Learning"](https://jods.mitpress.mit.edu/pub/issue3-brand) (2018), about 15 minutes. Free at jods.mitpress.mit.edu.
4. Deck p. 169 (5 minutes). Look at the two layer diagrams on the slide, then read the quoted summary under the heading "Stewart Brand's Pace Layers", beneath the slide. Skip the rest.
5. Deck p. 28 (5 minutes). Read the paragraph headed "Cost of Change" beneath the slide, and the short note near the bottom that begins "In this sense, we're seeking to reduce the cost of change". Skip the rest.
6. Deck p. 329 (10 minutes). Read the quote on the slide from software pioneer David Parnas, and the "Resilient Abstractions" notes beneath it. Skip the two quotes on the right.
7. *A Philosophy of Software Design* (Ousterhout, second edition, 2021), chapter 2, "The Nature of Complexity" (about 20 minutes), and chapter 3, "Working Code Isn't Enough" (about 15 minutes), on tactical and strategic programming. If you can't get the book this week, watch Ousterhout's [talk at Google](https://www.youtube.com/watch?v=bmSAYlu0NcY) (2018, free on YouTube) instead (62 minutes instead of 35).
8. *How Buildings Learn*, chapter 11, "The Scenario-buffered Building", the whole chapter (about 30 minutes). It's about designing for several possible futures instead of betting on one forecast.

## Full path

- The rest of *How Buildings Learn*, especially chapter 3, "'Nobody Cares What You Do In There': The Low Road" (cheap, plain buildings that people change freely), chapter 8, "The Romance of Maintenance", and chapter 12, "Built for Change".
- The full BBC series: six 30-minute episodes, free on Brand's YouTube channel.
- Deck pp. 27, 29 and 30 (architecture as the decisions that are costly to change; modularity as a container for change; software researcher Meir Lehman's law that a system in use must keep changing) and pp. 65 to 67 (evolutionary design: complex systems that work grow from simpler ones that worked, and problem and solution are worked out together).
- For the engineering view: Foote and Yoder, ["Big Ball of Mud"](https://www.laputan.org/mud/) (1997), the "Shearing Layers" section. It's the same idea in software, with layers running from data (fastest) to programming languages (slowest). Free at laputan.org.
- For the engineering view: Parnas, "On the Criteria To Be Used in Decomposing Systems into Modules" (*Communications of the ACM*, 1972). Six pages. The argument is in his comparison of two ways to split the same program, so you can skim the technical detail.
- For the engineering view: *A Philosophy of Software Design*, chapter 11, "Design it Twice" (about 15 minutes), on sketching more than one design before you choose, and chapter 21, "Decide What Matters" (about 15 minutes).
- For the engineering view: deck pp. 313 to 335, on modularity, coupling, cohesion and abstraction. Start with pp. 317, 318, 330 and 331, and skim the rest.
- Optional, for organizations: Beane and Leonardi, "Pace Layering as a Metaphor for Organizing in the Age of Intelligent Technologies" (*Journal of Management Studies*, 2025). It applies the idea to how organizations adapt to fast-changing technology.

## Terms you will meet

- **Shearing layers:** the parts of a building that change at different rates, and so shear against each other. Brand's six, from slowest to fastest: site, structure, skin (the outside walls and roof), services (wiring, plumbing, heating), space plan (the interior layout) and stuff (furniture and belongings).
- **Pace layers:** Brand's later version for whole societies and other complex systems, from fastest to slowest: fashion, commerce, infrastructure, governance, culture and nature.
- **Slippage:** room for a fast layer to change without disturbing a slower one. In a building, that's wiring you can replace without opening the walls. In a game, it's an item's price kept in a setting you can change without shipping a new build.
- **Cost of change:** what it would take to undo or redo a decision later. The deck calls a decision architecturally significant when its cost of change is high, or when it lowers the cost of other changes (p. 28).
- **Coupling:** how much one part depends on others; the deck also calls it entanglement. With tight coupling, a change in one part ripples into the rest.
- **Cohesion:** how closely the things inside one part belong together. High cohesion means a part has one clear job.
- **Modularity:** dividing a system into parts that can be understood, built and changed separately.
- **Interface:** the agreed way one part talks to another. A stable interface lets the part behind it change without disturbing anyone else.
- **Information hiding:** Parnas's rule that each part keeps one likely-to-change decision to itself, behind an interface that doesn't reveal it.
- **Abstraction:** an idea reduced to what matters for the job, with the detail hidden behind it.
- **System of record:** the system that holds the official copy of some data, such as the orders in a marketplace.
- **Complexity (Ousterhout's sense):** anything in a system's structure that makes it hard to understand and change.
- **The three symptoms of complexity:** Ousterhout's names for how complexity shows up.
  - **Change amplification:** a simple change needs edits in many places.
  - **Cognitive load:** how much a developer must know to make a change safely.
  - **Unknown unknowns:** it isn't clear what must change until something breaks.
- **Tactical and strategic programming:** tactical work gets the current feature working fast; strategic work also invests in a design that makes later changes easier.
- **Evolutionary design:** growing a system in steps as you learn, rather than fixing the whole design up front.
- **Scenario planning:** imagining several plausible futures and choosing a design that holds up in all of them (Brand, chapter 11).

## What to look for

- **Slow layers are in charge.** In chapter 2, notice Brand's point that the slower layers govern the faster ones. It's the slowest layer a request touches that sets its real cost.
- **Slippage beats a tight fit.** Binding fast layers into slow ones looks efficient when a building is new, and it blocks change later (chapter 2). Watch for the software version: a business rule buried inside a core system, like a cancellation policy written into an airline's booking engine.
- **Wrong pace, either way.** Brand's essay gives historical cases of a layer forced to another layer's speed. Sometimes a fast layer pushes a slow one, and sometimes a slow schedule is imposed on a fast one. He argues that both end badly.
- **Keep together what changes together.** The deck turns Brand's observation into a design rule and pairs it with Parnas: draw boundaries around the decisions likely to change (p. 329). Engineers can apply it only as well as they know what's likely to change, and often you're the one who knows.
- **A decision is significant if it's costly to undo.** A decision matters architecturally if it would be costly to reverse, or if it makes other changes cheaper (p. 28). That's your test for which decisions deserve slow, careful attention and which you can make quickly.
- **Name the symptom, not the culprit.** Ousterhout's three symptoms let you say why a change was slow without pointing at anyone. Change amplification is coupling seen from the change's side, which is the Coupling Is About a Change card's subject.
- **Strategic work is the case you can make.** Chapter 3 contrasts getting the current feature working fast with investing a little in a design that makes later changes easier. You're often the one who can say which later changes are likely, so you can say where that investment pays.
- **Every forecast is partly wrong.** Brand's own line is "All buildings are predictions. All predictions are wrong." Chapter 11 gives up on a better forecast and plans with scenarios, loose fit and options.

## Apply it to your own work

1. List your product's layers in about 30 minutes. Take one product or user journey you own and list its parts from fastest-changing to slowest. For example: wording and content; screens and flows; business rules and settings; APIs and integrations; the data model; core systems of record; the contracts, standards and laws it has to meet. Next to each, note how often it actually changed in the last year. A first pass from your own knowledge is fine. Then ask a tech lead to check it against release history (the release notes or change log for each system). You might open with "Which of these is hardest to change, and why?" Don't skip that conversation, because it's part of the exercise. Where is a part moving at the wrong pace for its layer?
2. In about 20 minutes, pick a recent request that took far longer than its size suggested. Memory will do if there are no records. Which layers did it touch, and could anyone see the slowest of them when the work was estimated? Which of the three symptoms of complexity showed up?
3. In about 15 minutes, walk a likely change across your system, as the deck suggests on p. 329. Name one change you expect in the next year, such as a second currency at checkout, a new sensor model in the field or a partner asking to build on your API. Start from what you know, then ask a tech lead, and open with "If we did this, which parts would have to change?" If the answer is most of them, what boundary would have contained it?

## Questions to bring to engineers

- Which of these layers is hardest to change, and why?
- If we made this change, which parts would have to change with it?
- Where in our system is change amplification worst?
- What would a small strategic investment there cost, and what would it save?
- For the change we most expect next year, which teams would have to ship together?

## Check your own thinking

The shift this module is after is from "how long will this feature take?" to "which layers does this change touch, and is the slowest of them meant to move this fast?" Here's a way to test yourself. Before your next request is estimated, write down the slowest layer you think it touches and how many weeks you expect it to add, then compare that with what actually happens. If you'd like a sounding board, take your layer list and your prediction to your manager or a mentor.

> Deck page references are to Ruth Malan's System Design and Software Architecture workshop notes, February to March 2025 edition. This guide is an independent companion; it has not been reviewed or endorsed by Ruth Malan.

# Pace Layers

## The idea

A building isn't one thing. It's a stack of layers that change at different speeds: the structure may last centuries while the furniture moves weekly. The architect Frank Duffy made the point in the 1970s, and Stewart Brand built it out in *How Buildings Learn* (1994) as six shearing layers: site, structure, skin, services, space plan and stuff. Buildings that adapt well let each layer change without tearing up the slower one beneath it. In *The Clock of the Long Now* (1999), Brand widened the idea to whole societies, from fashion down to nature, and called it pace layering. His summary: "Fast learns, slow remembers."

## Why a PM should care

- **The slowest layer sets the price of a change.** Letting a student join two classes looks small on screen. It can take a quarter if it reaches down into the data model, a core system or a contract.
- **Keep together what changes together.** Software designers group parts that change at similar rates (Foote and Yoder, 1997) and hide each decision likely to change behind a stable interface (Parnas, 1972). You often know best what's likely to change, so tell your engineers.
- **Each layer has its own right speed.** Trouble starts when a layer is forced to the wrong pace: a core data change rushed at sprint speed, or a wording fix stuck waiting for a quarterly release.
- **Slow is not the enemy.** In a hospital, patient records (a system of record, where the official data lives) and the checks around them move slowly on purpose, to protect continuity and trust. Put fast experiments where a mistake is cheap to undo.
- **Organizations have layers too.** A system that's costly to change holds the teams around it in place (the Conway's Law card in Module 3, Mind the Seams).

## How to spot it at work

- A request that looks small turns into a long project once someone checks what it rests on.
- Everything built on one core system ships on that system's release calendar.
- People get around a slow layer with a rule hard-coded into a screen, a shadow spreadsheet or a manual step.
- A wording change needs a full release, while an API that other teams rely on keeps changing under them.

## What it does not say

It does not say fast is good and slow is bad. Each layer does a different job, and the slow ones carry continuity. The layers and timescales are rules of thumb from building practice and Brand's reading of ecology and history, not measured laws, so redraw them for your own product. And if you hear "pace layering" about applications at work, it probably means Gartner's borrowing of the name, which sorts systems into record, differentiation and innovation. That's a related idea, but it isn't Brand's model.

## One question to carry into your work

Which layer does this change really live in, and what slower layer does it rest on?

## Go deeper

- Brand, *How Buildings Learn* (1994), chapter 2, "Shearing Layers".
- Brand, ["Pace Layering: How Complex Systems Learn and Keep Learning"](https://jods.mitpress.mit.edu/pub/issue3-brand) (2018). Free at jods.mitpress.mit.edu.
- *How Buildings Learn*, BBC series (1997), episode 6, "Shearing Layers". 30 minutes, free on [Stewart Brand's YouTube channel](https://www.youtube.com/channel/UCjBdRnkOB5P85yki3rAvGUw).
- Foote and Yoder, ["Big Ball of Mud"](https://www.laputan.org/mud/) (1997), the "Shearing Layers" section. Free at laputan.org.
- Deck p. 169 (Brand's layer diagrams) and p. 329 (Parnas, and the rule "keep things that change together, together").

> Deck page references are to Ruth Malan's System Design and Software Architecture workshop notes, February to March 2025 edition, a 514-page set of slide notes; read only the pages cited. This card is an independent companion; it has not been reviewed or endorsed by Ruth Malan.

# Coupling Is About a Change

## The idea

"Are these two parts coupled?" has no useful answer until you name the change. Kent Beck's definition, from his talk "The Beauty of Maintenance" (2020): two parts are coupled "with respect to a particular change" if changing one means changing the other. A phone company's plan catalog and billing system can be independent when a price changes, and welded together when a new kind of charge arrives, like data shared across a family.

Michael Nygard sorts coupling into five kinds. Operational: one can't run without the other. Development: "changes in producer and consumer must be co-ordinated". Semantic: they change together because they share a concept. Functional: they share a responsibility. Incidental: they "change together for no good reason".

## Why a PM cares

- **Development coupling is the kind on your roadmap.** Each change two teams must coordinate costs meetings, a joint release and waiting. Name it when you plan and you can schedule it. Leave it unnamed and you'll meet it in week six.
- **You often know which changes are coming.** When an engineer says two systems are tightly coupled, ask for which change, and name the one you expect, such as next year's eligibility rules on a public benefits service. It's Parnas's information hiding, from this module's terms, seen from your side: engineers can only hide the decisions they know will move.
- **You can map it on one page.** Barry O'Reilly lists likely stressors against components and marks each component a stressor hits. For an electric car charging network, his stressors include a new car model and an expired card. Where one stressor marks several components, they're coupled for that change. You bring the business stressors.

## How to spot it

- A small change needs two teams to release on the same day, plus a call to agree on the order.
- The release history shows the same two services changing together, again and again. Engineers call it change coupling.
- Two services talk only through a tidy API, yet both break when a streaming service redefines an active subscriber. That's semantic coupling, and the API doesn't remove it.

## What it does not say

It doesn't say coupling is bad. Parts that work together are coupled for something: a routing service that isn't coupled to its map data won't route anyone. Decoupling has a price in parts and interfaces to run, so pay it where the likely changes are. And Nygard's kinds are a practitioner's vocabulary, not a tested classification. One pair of parts can show several.

**One question to carry:** For the change you most expect next year, which teams would have to ship together?

## Go deeper

**[Uncoupling](https://www.youtube.com/watch?v=EirOknZJvYc), Michael Nygard (2018)**

His keynote at the SATURN 2018 conference, about an hour. Free on YouTube. He gave talks of the same name at other conferences, too.

**Why trust it:** Nygard is a software architect and the author of the book *Release It!*. It's one practitioner's talk, not research.

**What you'll get:** The five kinds from the person who drew them up, so you can judge which ones your teams are paying for.

*To check: nobody has watched a source for this card. YouTube's search listing, read on 20 November 2026, gives the talks' titles, years and lengths: Beck's "The Beauty of Maintenance" is at youtube.com/watch?v=3gib0hKYjB0 (DDD Europe 2020, 56 minutes), and Nygard's "Uncoupling" was the SATURN 2018 keynote (57 minutes), also given at DevOpsDays DFW and JDD 2019. YouTube answers automated requests for a video with a bot check, so neither could be watched. Beck's definition (deck p. 366) and Nygard's kinds (p. 364) are quoted from the deck's copies of their slides: check them against the talks, and check that the SATURN version has Nygard's five kinds. O'Reilly's table (pp. 406, 457) is from his talk "An Introduction to Residuality Theory" (NDC Oslo 2023, youtube.com/watch?v=0wcUG2EV-7E), also unwatched. Beck's book Tidy First? (2023) may suit the full path.*
