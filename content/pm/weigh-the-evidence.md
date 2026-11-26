---
title: Weigh the Evidence
layout: module
module: weigh-the-evidence
question: What do the numbers and the stories each tell you, and how much should either decide?
setting: a grocery delivery app
one_thing: Take one decision in front of you, list the evidence you're leaning on, and write next to each piece who's missing from it.
do_minutes: 30
game: ranking

last_time:
  - q: Why break a rollout's guardrail metrics down for the customers it could hurt most?
    a: A guardrail can hold on average while it fails them, such as people on older phones or using a screen reader.
  - q: Why ask for the 99th percentile when someone quotes you an average?
    a: An average hides the customers who wait. The 99th percentile tells you how long all but the slowest one in a hundred wait.

steps:
  - id: card-small-numbers
    kind: card
    card: cards/law-of-small-numbers
    minutes: 5
    look: Why the worst week usually gets better on its own.
  - id: ranking
    kind: play
    title: Play the ranking game
    minutes: 15
    where: It's on this page, just below this list.
    look: Which stores fill both ends of the ranking, where the one real problem ends up, and how long a fix tried in small stores takes to show.
  - id: munro
    kind: read
    title: 'Eileen Munro, "Decision making under uncertainty in child protection"'
    minutes: 5
    where: A journal article. Free at researchonline.lse.ac.uk. Read the two paragraphs on being "risk-to-self averse," just before the heading "Organisational Cultures about Uncertainty."
    links:
      - text: "Decision making under uncertainty in child protection: creating a just and learning culture"
        url: https://researchonline.lse.ac.uk/id/eprint/88108/1/Munro_Decision%20Making_Accepted.pdf
    look: How a tool that's often more accurate than professionals can still carry their bias, now "out of sight in an apparently neutral scientific instrument."
    trust: "An argument. It's a peer-reviewed paper by the professor of social policy who led England's 2011 review of child protection."
    only: A sharp account of bias hidden in a number that looks neutral. Your product's data, too, carries the judgment of whoever collected it.
  - id: cartwright
    kind: read
    title: 'Nancy Cartwright, Brendan Kelters, Eileen Munro and John Pemberton, "Can I make this policy work here?"'
    minutes: 15
    where: A working paper. Free at dur.ac.uk. Read pages 3 to 7.
    links:
      - text: "Can I make this policy work here? Using evidence for better policy design, prediction and evaluation"
        url: https://dur.ac.uk/media/durham-university/research-/research-centres/humanities-engaging-sci-and-soc-centre-for/CWP_2025_01.pdf
    look: "The question to ask in place of \"did it work there?\": \"How would the policy lead to the intended outcome here?\""
    trust: "An argument. Cartwright is a philosopher of science at Durham who studies how evidence gets used, and Munro co-wrote it. It's the short version of their 2026 book from Cambridge University Press, and not peer-reviewed itself."
    only: A way to read a competitor's case study step by step before you copy it.
  - id: card-riskiest-assumption
    kind: card
    card: cards/riskiest-assumption
    minutes: 5
    look: How to pick the one thing to test first, and what a cheap test can't show.
  - id: do
    kind: do
    title: Weigh the evidence for one decision, and log your call
    where: The Do, on this page, below.
    look: Who's missing from each piece, and what would change your mind.
  - id: check
    kind: check
    title: Check yourself
    where: The Check, on this page, below.
    look: The answers you missed, and why you missed them.

example:
  body: |
    **Decision:** batch two orders a trip in the suburbs?

    - **Number.** Pilot city: late orders flat at 6 percent, shoppers' hourly pay up 8 percent. Missing: shoppers who quit. Collected: logs, six weeks. Carries over if drives are as short.
    - **Story.** A manager's call: batches crowd the pickup shelf. Missing: the other 29 managers. Collected: one call. Carries over where shelves are small.
    - **Number.** Survey: 70 percent fine waiting longer. Missing: 96 percent never replied. Collected: email. Carries over if suburbs are as patient.

    **Would change our mind:** late orders 2 points above unbatched suburbs.

    **Decision log:** two random suburbs batched, three not. Expect late orders within a point of theirs. 60 percent sure: drives are longer. Know by September 30.
  good:
    - Each "Carries over" names one thing to check here, like drive length or shelf size.
    - "\"Missing\" names the people each piece can't hear from, like the shoppers who quit."
    - The call compares batched suburbs with unbatched ones, and its doubt comes from what differs here.

check:
  - q: Your grocery app's dashboard ranks twenty cities by on-time delivery, and the bottom three are called in for a review. What do you check first?
    a: How many orders each city had. The smallest fill both ends of a ranking by chance alone, and they'll trade places next week. Compare each rate with the range its size allows, as the funnel did in the ranking game.
  - q: Know Who It's For says interviews beat your vision on what the problem is. Three customers say late orders made them quit, and you're asked to speed up delivery in every city. Do the interviews settle it?
    against: know-who-its-for
    wins: weigh-the-evidence
    a: "Not this one. They show the problem is real for three people. A change for every city needs how many share it: compare how often customers leave after a late order with how often others do."
  - q: A competitor's case study says a feature lifted retention by 20 percent. What do you ask before you copy it?
    a: "Cartwright's question: how would it lead to that result here, step by step, and what would support or derail each step for your customers?"
  - q: "**Beyond this module.** You've weighed the evidence you have. What decides how much more to gather?"
    a: What it costs to be wrong, and whether you can undo the call. [Decide and Set Direction](/pm/decide-and-set-direction/) sorts out the decisions worth slowing down for.

deeper_one:
  title: "The Art of Statistics"
  why: "It's written for readers who don't want equations, and it teaches the habit every step here leans on: reading a number well."
deeper:
  - title: Superforecasting
    by: Philip E. Tetlock and Dan Gardner
    where: A book.
    note: "Read chapter 1, \"An Optimistic Skeptic,\" and chapter 3, \"Keeping Score,\" then the appendix, \"Ten Commandments for Aspiring Superforecasters.\""
    trust: "A study. It reports the Good Judgment Project, Tetlock's years-long study of tens of thousands of ordinary people forecasting world events."
    only: "Your hunch, given a number and scored against what happened: how people whose forecasts were scored got better at them, and why Tetlock calls forecasting \"a skill that can be cultivated.\""
  - title: The Art of Statistics
    by: David Spiegelhalter
    where: A book.
    note: "Read chapter 3, \"Why Are We Looking at Data Anyway? Populations and Measurement,\" then chapter 5, \"Modelling Relationships Using Regression,\" where regression to the mean starts with Galton's heights of fathers and sons, and chapter 9, \"Putting Probability and Statistics Together,\" whose funnel plot of death rates by district shows why small places swing more than large ones."
    trust: "Experience. Spiegelhalter is a Cambridge statistician and a past president of the Royal Statistical Society, writing for readers who don't want equations. Its examples lean on British medicine and public health."
    only: "The card's ideas at full length: small samples, chance and regression to the mean. Then how to read a number well."
  - title: Data Feminism
    by: Catherine D'Ignazio and Lauren F. Klein
    url: https://doi.org/10.7551/mitpress/11805.001.0001
    where: A book.
    note: "Free at direct.mit.edu, open access. Read chapter 4, \"What Gets Counted Counts,\" and chapter 6, \"The Numbers Don't Speak for Themselves.\""
    trust: "An argument. Its authors are professors, of urban science at MIT and of data and decision sciences at Emory, and its draft went through open peer review. It's written from a stated standpoint, intersectional feminism, and says so."
    only: "Who gets counted, and how: colleges' official counts of sexual assault, whose picture ran \"closer to the reverse\" of what anonymous surveys found, and a gender field that took any answer and still sorted people into two."
  - title: Clinical Versus Actuarial Judgment
    by: Robyn Dawes, David Faust and Paul Meehl (Science, 1989)
    url: https://meehl.umn.edu/sites/meehl.umn.edu/files/files/138cstixdawesfaustmeehl.pdf
    where: A journal article.
    note: Free at meehl.umn.edu, Meehl's archive, with an exchange of letters from 1990 at the end. Read the "broken leg" exception closely.
    trust: "A review of studies. *Science* published it, and Meehl's 1954 book set out the question."
    only: The honest counterweight to this module. In study after study, a formula did as well as the expert or better, and the article says why professionals resist hearing it.
  - title: The Big Short
    by: directed by Adam McKay, written by Charles Randolph and McKay from Michael Lewis's book (Paramount, 2015)
    where: A film.
    note: "Michael Burry reads the loans inside the mortgage bonds, which almost nobody does, and bets they'll fail. Mark Baum's team won't take the numbers alone and flies to Florida, where they find empty neighborhoods, brokers proud of loans to people with no income and no job, and a dancer with five houses and a condo. \"They're not confessing... They're bragging!\""
    only: "This module's optional exercise done for real, with billions on it: a number checked against the people behind it, whose stories showed what the ratings hid."
---

## Why this matters

You'll meet both mistakes in the same week. On Monday, one vivid story from a customer turns your grocery app's roadmap. On Thursday, a dashboard settles an argument because it has decimals in it, though nobody can say who's in the data. Both feel responsible at the time. Adam Mosseri, then at Facebook, put the aim in the title of [a 2010 talk](https://www.youtube.com/watch?v=bKZiXAFeBeY): be {{< pm/term "data-informed" >}}, not data-driven. Use the numbers and the stories for what each can tell you, and keep the decision yours.

Numbers tell you how much and how often, across many people, but only about what someone chose to measure. Forget that, and what's hard to measure gets left out, then called unimportant, then treated as if it isn't there: the {{< pm/term "mcnamara-fallacy" "McNamara fallacy" >}}, as Daniel Yankelovich named it in 1971. Set it beside [Goodhart's Law](/pm/cards/goodharts-law/) from [Find the Constraint](/pm/find-the-constraint/): there a number is gamed once it's a target, and here it's trusted because it can be counted. Stories tell you why, and what nobody thought to measure, but only about the people who told them, which is why [Know Who It's For](/pm/know-who-its-for/) asked whose problem you hear. An AI summary of your interviews chooses what to keep, too, so check it against your notes before you lean on it. When the numbers and the stories disagree, look into why before you pick a side.

When you break a number down, break it down by more than one thing at once. In [Gender Shades](https://proceedings.mlr.press/v81/buolamwini18a.html), a 2018 paper, Joy Buolamwini and Timnit Gebru tested face analysis from three companies on gender and skin type together. It got darker-skinned women's gender wrong up to a third of the time, and lighter-skinned men's almost never. The word for looking where two such lines cross is {{< pm/term "intersectional" >}}, from Kimberlé Crenshaw, whom you met in [Mind the Seams](/pm/mind-the-seams/). The groups there are small, so they swing, as the card warns: get more data there, not less attention.

Your own hunch is evidence too. Gary Klein, a psychologist who studies how experts decide, calls it "an important data point" in [a 2010 interview alongside Daniel Kahneman](https://www.mckinsey.com/capabilities/strategy-and-corporate-finance/our-insights/strategic-decisions-when-can-you-trust-your-gut), and you check it like any other. It deserves more weight when the situation has patterns you can learn, and you've made this kind of call often and found out each time whether you were right ([Kahneman and Klein, 2009](https://doi.org/10.1037/a0016755)).

[//]: # (short-path)

## Do

**Weigh the evidence for one decision (30 minutes).** Pick a decision in front of you, such as whether a grocery app should change how it batches orders. List three to five pieces of evidence you lean on, one line each, and mark each a story, a number or a hunch. Next to each, answer three questions. Who's missing from it? How was it collected? And what would have to hold here for it to carry over? Then write one sentence on what would change your mind.

**For your decision log.** Write the call you'd make on that decision now (a small test with a comparison counts), what you expect to happen, how sure you are, and when you'll know.

{{< pm/example >}}

**Optional: find the stories behind one number (15 minutes).** Pick a number on your dashboard that moved last month, such as the share of orders missing an item. Find three cases behind the move and read them. Does what happened to those people match what the number says? If not, write down what it isn't measuring.
