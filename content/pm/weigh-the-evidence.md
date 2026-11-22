---
title: Weigh the Evidence
layout: module
module: weigh-the-evidence
question: What do the numbers and the stories each tell you, and how much should either decide?
one_thing: Take one decision in front of you, list the evidence you're leaning on, and write next to each piece who's missing from it.
do_minutes: 35
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
    minutes: 10
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
    trust: It's a peer-reviewed paper by the professor of social policy who led England's 2011 review of child protection.
    only: Bias hidden in a number that looks neutral, put sharply. Your product's data, too, carries the judgment of whoever collected it.
  - id: cartwright
    kind: read
    title: 'Nancy Cartwright, Brendan Kelters, Eileen Munro and John Pemberton, "Can I make this policy work here?"'
    minutes: 15
    where: A working paper. Free at dur.ac.uk. Read pages 3 to 7.
    links:
      - text: "Can I make this policy work here? Using evidence for better policy design, prediction and evaluation"
        url: https://dur.ac.uk/media/durham-university/research-/research-centres/humanities-engaging-sci-and-soc-centre-for/CWP_2025_01.pdf
    look: "The question to ask in place of \"did it work there?\": \"How would the policy lead to the intended outcome here?\""
    trust: Cartwright is a philosopher of science at Durham who studies how evidence gets used, and Munro co-wrote it. It's the short version of their 2026 book from Cambridge University Press, and not peer-reviewed itself.
    only: A way to read a competitor's case study step by step before you copy it.

check:
  - q: Your dashboard ranks twenty cities by on-time delivery, and the bottom three are called in for a review. What do you check first?
    a: How many orders each city had. The smallest fill both ends of a ranking by chance alone, and they'll trade places next week. Compare each rate with the range its size allows, as the funnel did in the ranking game.
  - q: Know Who It's For says interviews beat your vision on what the problem is, and a story speaks only for whoever told it. When do three interviews settle it, and when do you need the numbers?
    against: know-who-its-for
    a: Interviews settle what the problem is for the people you asked. Numbers tell you how many share it. When the two disagree, find out who you didn't interview.
  - q: A competitor's case study says a feature lifted retention by 20 percent. What do you ask before you copy it?
    a: "Cartwright's question: how would it lead to that result here, step by step, and what would support or derail each step for your customers?"
  - q: "**Beyond this module.** You've weighed the evidence you have. What decides how much more to gather?"
    a: What it costs to be wrong, and whether you can undo the call. Decide and Set Direction sorts out the decisions worth slowing down for.

deeper:
  - title: The Tyranny of Metrics
    by: Jerry Z. Muller
    where: A book.
    note: "Read the introduction, the first two chapters, the case chapter nearest your work (medicine, policing, business and finance), and the last, \"When and How to Use Metrics: A Checklist.\""
    trust: Muller is a historian, arguing from cases. It's an argument, so expect one side of it.
    only: Thursday's mistake in field after field, what he calls metric fixation, and a checklist for using numbers alongside judgment, not in place of it.
  - title: The Art of Statistics
    by: David Spiegelhalter
    where: A book.
    note: "Read chapter 3, \"Why Are We Looking at Data Anyway? Populations and Measurement,\" then chapter 5, \"Modelling Relationships Using Regression,\" where regression to the mean starts with Galton's heights of fathers and sons, and chapter 9, \"Putting Probability and Statistics Together,\" whose funnel plot of death rates by district shows why small places swing more than large ones."
    trust: Spiegelhalter is a Cambridge statistician and a past president of the Royal Statistical Society, writing for readers who don't want equations. Its examples lean on British medicine and public health.
    only: "The card's ideas at full length: small samples, chance and regression to the mean. Then how to read a number well. It balances a list that's mostly warnings about numbers."
  - title: Data Feminism
    by: Catherine D'Ignazio and Lauren F. Klein
    url: https://doi.org/10.7551/mitpress/11805.001.0001
    where: A book.
    note: "Free at direct.mit.edu, open access. Read chapter 4, \"What Gets Counted Counts,\" and chapter 6, \"The Numbers Don't Speak for Themselves.\""
    trust: Its authors are professors, of urban science at MIT and of data and decision sciences at Emory, and its draft went through open peer review. It argues from a stated standpoint, intersectional feminism, and says so.
    only: "Who gets counted, and how: colleges' official counts of sexual assault, whose picture ran \"closer to the reverse\" of what anonymous surveys found, and a gender field that took any answer and still sorted people into two."
  - title: Clinical Versus Actuarial Judgment
    by: Robyn Dawes, David Faust and Paul Meehl (Science, 1989)
    url: https://meehl.umn.edu/sites/meehl.umn.edu/files/files/138cstixdawesfaustmeehl.pdf
    where: A journal article.
    note: Free at meehl.umn.edu, Meehl's archive, with an exchange of letters from 1990 at the end. Read the "broken leg" exception closely.
    trust: "*Science* published it, and Meehl's 1954 book set out the question."
    only: The honest counterweight to this module. In study after study, a formula did as well as the expert or better, and the article says why professionals resist hearing it.
  - title: The Big Short
    by: directed by Adam McKay, written by Charles Randolph and McKay from Michael Lewis's book (Paramount, 2015)
    where: A film.
    note: "Michael Burry reads the loans inside the mortgage bonds, which almost nobody does, and bets they'll fail. Mark Baum's team won't take the numbers alone and flies to Florida, where they find empty neighborhoods, brokers proud of loans to people with no income and no job, and a dancer with five houses and a condo. \"They're not confessing... They're bragging!\""
    only: "This module's optional exercise done for real, with billions on it: a number checked against the people behind it, whose stories showed what the ratings hid."
---

## Why this matters

You'll meet both mistakes in the same week. On Monday, one vivid story from a customer, or one loud sales call, turns the roadmap. On Thursday, a dashboard settles an argument because it has decimals in it, though nobody can say who's in the data or who isn't. Both feel responsible at the time. Adam Mosseri, then a designer at Facebook, put the aim in the title of [a 2010 talk](https://www.youtube.com/watch?v=bKZiXAFeBeY): be {{< pm/term "data-informed" >}}, not data-driven. Use the numbers and the stories for what each can tell you, and keep the decision yours.

Numbers tell you how much and how often, across many people, but only about what someone chose to measure. Forget that, and what's hard to measure gets left out, then called unimportant, then treated as if it isn't there: the {{< pm/term "mcnamara-fallacy" "McNamara fallacy" >}}, as the market researcher Daniel Yankelovich named it in 1971. It's a sibling of Goodhart's Law from Find the Constraint: there a number is gamed once it's a target, and here it's trusted because it can be counted. Stories tell you why, and what nobody thought to measure, but only about the people who told them, which is why Know Who It's For asked whose problem you hear. When the numbers and the stories disagree, look into why before you pick a side.

When you break a number down, break it down by more than one thing at once. In [Gender Shades](https://proceedings.mlr.press/v81/buolamwini18a.html), a 2018 paper, Joy Buolamwini and Timnit Gebru tested face analysis from three companies on gender and skin type together. It got darker-skinned women's gender wrong up to a third of the time, and lighter-skinned men's almost never. The word for looking where two such lines cross is {{< pm/term "intersectional" >}}, from Kimberlé Crenshaw, whom you met in Mind the Seams. The groups there are small, so they swing, as the card warns: get more data there, not less attention.

Your own hunch is evidence too. Gary Klein, a psychologist who studies how experts decide, calls it "an important data point," and you check it like any other. It deserves more weight when the situation has patterns you can learn, and you've made this kind of call often and found out each time whether you were right (Kahneman and Klein, 2010).

[//]: # (short-path)

## Do

**Weigh the evidence for one decision (25 minutes).** Pick a decision in front of you, such as whether a delivery app should change how it batches orders. List every piece of evidence you're leaning on, one line each, and mark each one a story or a number. Next to each, answer three questions in a few words. Who's missing from it? How was it collected? And what would have to hold here for it to carry over? Then write one sentence on what would change your mind.

**For your decision log.** Write the call you'd make on that decision now, what you expect to happen, how sure you are, and when you'll know.

**Optional: find the stories behind one number (10 minutes).** Pick a number on your dashboard that moved last month, such as the time to settle an insurance claim. Find three cases behind the move and read them. Does what happened to those people match what the number says? If not, write down what it isn't measuring.
