---
title: Answer for What You Build
layout: module
module: answer-for-what-you-build
question: Who benefits and who is harmed by what we build, and what's our share of the responsibility?
setting: a video-sharing app
one_thing: Run a consequence scan on one feature you own, and write down one change you'd propose.
do_minutes: 35

last_time:
  - q: Your team still sends a weekly report nobody seems to read. Before you stop it, what do you find out?
    a: Why it started and what leans on it. Someone may still depend on it, which is Chesterton's point about the fence.
  - q: Why can a team that shares your picture of a situation act without asking you first?
    a: It knows the intent behind the task, so it can still act when the task goes stale. Boyd put orientation, that shared picture, at the center of his loop.

steps:
  - id: doteveryone
    kind: read
    title: 'Doteveryone, "Consequence Scanning"'
    minutes: 10
    where: A web page and a manual. Free at adalovelaceinstitute.org. Read the page, then the manual's steps for running a session.
    links:
      - text: "Consequence Scanning"
        url: https://www.adalovelaceinstitute.org/resource/doteveryone-consequence-scanning/
    look: The three questions you'll use in the Do, and how a session runs.
    trust: "Experience. It's from the method's designers at Doteveryone, a responsible technology think tank that ran from 2015 to 2020, and it describes the tool rather than testing it."
    only: A conversation to run with your team in about an hour, early, while the feature can still change.
  - id: reichheld-markey
    kind: read
    title: 'Fred Reichheld and Rob Markey, "Blowing the whistle on bad profits"'
    minutes: 10
    where: An article. Free at bain.com.
    links:
      - text: "Blowing the whistle on bad profits"
        url: https://www.bain.com/insights/blowing-whistle-on-bad-profits
    look: "What they count as bad profits, \"profits earned at the expense of customer relationships.\" Then ask how much of your product's revenue comes from value it created, and how much from making it hard to leave."
    trust: "An argument. Two Bain consultants make the case for their own customer survey."
    only: "A name for that kind of revenue, bad profits, and a question for whoever sets your prices: how much of ours is that?"
  - id: card-many-hands
    kind: card
    card: cards/many-hands
    minutes: 5
    look: The phrases people reach for to feel less responsible.
  - id: card-mission-excuse
    kind: card
    card: cards/mission-excuse
    minutes: 5
    look: The signs that a mission has started to excuse its costs, and the question to carry.
  - id: cheung
    kind: read
    title: 'Erika Cheung, "Theranos, whistleblowing and speaking truth to power"'
    minutes: 20
    where: A talk, with a transcript. Free at ted.com.
    links:
      - text: "Theranos, whistleblowing and speaking truth to power"
        url: https://www.ted.com/talks/erika_cheung_theranos_whistleblowing_and_speaking_truth_to_power/transcript?language=en
    look: "What she's told when she raises her doubts, and the question she asks after: what happens when \"the vision is so compelling and the desire to believe is so strong that it starts to cloud your judgment about what reality is?\""
    trust: "Experience. Cheung joined Theranos's lab as a recent graduate and raised her concerns inside. It's her side of it, told years later."
    only: What the pull feels like from inside, told by someone who met it early in her career.
  - id: schneier
    kind: read
    title: 'Bruce Schneier, "Data Is a Toxic Asset, So Why Not Throw It Out?"'
    minutes: 10
    where: An essay. Free at schneier.com.
    links:
      - text: "Data Is a Toxic Asset, So Why Not Throw It Out?"
        url: https://www.schneier.com/essays/archives/2016/03/data_is_a_toxic_asse.html
    look: "Why he treats stored data as a liability: everyone from thieves to governments wants it, and it stays dangerous as long as you keep it."
    trust: "An argument. Schneier is a security technologist, and CNN first published the essay."
    only: "His fix, in one line: \"there's no better security than deleting the data.\""
  - id: inclusive
    kind: read
    title: GOV.UK Service Manual, "Making your service more inclusive"
    minutes: 10
    where: A guide for the UK government's digital teams. Free at gov.uk.
    links:
      - text: "Making your service more inclusive"
        url: https://www.gov.uk/service-manual/design/making-your-service-more-inclusive
    look: Why "Is this your first child?" is hard for some people to answer, and the fix, "Focus on what your service really needs to know." It's Schneier's point from the service side.
    trust: "Experience. It's the UK government's guidance for its own services, which have to work for everyone, since people usually have no alternative. Parts are for a public service's legal duties."
    only: A test for every field you ask people to fill in, and the common reasons people get shut out, from time and trust to the evidence they're asked for.
  - id: do
    kind: do
    title: Scan one feature, and write your lines
    where: The Do, on this page, below. Showing it to support or trust and safety can come later.
    look: Who's easiest to overlook, and where groups overlap.
  - id: check
    kind: check
    title: Check yourself
    where: The Check, on this page, below.
    look: The answers you missed, and why you missed them.

example:
  body: |
    **Feature:** autoplay.

    **Intended:** fewer taps; more watch time.

    **Unintended:** teens up late; prepaid data spent.

    **Easiest to overlook:** viewers with photosensitive epilepsy.

    **Overlap:** prepaid teens. Adults use data saver to stop autoplay; teens' data saver is locked in parental controls.

    **Focus on:** fewer taps, not watch time.

    **Mitigate:**

    - Flashing videos don't autoplay. Trust and safety.
    - Off after 11 p.m. for teens. Teen team.

    **To propose:** let teens turn on data saver, with a one-time prompt on mobile data. Settings team.

    **Decision log:** teen data saver. Expect a fifth less mobile data per teen on a prepaid carrier, costing the app 2 percent of teens' watch time. 55 percent sure: many may tap no. Know by March 31.
  good:
    - It focuses on what viewers gain, fewer taps, not the watch time the app gains.
    - "The overlap shows where an existing fix fails: data saver protects prepaid adults, but not prepaid teens, who can't turn it on."
    - "Its log names who gains and who pays: less data for prepaid teens, 2 percent of teens' watch time for the app."

check:
  - q: A change lifts hours watched on your video app by starting the next video without asking. Has it created value?
    a: Ask whether viewers are better off, or only up later than they meant to be. If they'd switch it off given a plain choice, those hours were taken from them, not created for them.
  - q: To meet sales targets, Wells Fargo employees opened accounts customers hadn't asked for. {{< pm/mod see-the-system words >}} would look at the structure, not the people. Here, each employee still had a share. Who's right?
    against: see-the-system
    a: "{{< pm/mod see-the-system >}}, when you ask why it happened and how to stop it: change the targets. This module, when you're the one asked to hit them: a target explains a choice, but it doesn't make it for you. Sidney Dekker, from {{< pm/mod see-the-system words >}}'s full path, [joins the two](https://sidneydekker.com/just-culture/): after harm, ask who was hurt, what they need and whose job it is to meet it. In his sense, an account is a story, not a debt: \"something you get people to tell, and others to listen to.\""
  - q: A teammate wants a new sign-up field "in case we need it." What do you ask?
    a: Which decision will it change? If none does yet, leave it out. Every field you keep is something to secure, and something to find when a customer asks you to erase it.
  - q: Your CEO calls the new feed the company's future. To make the launch date, your lead asks you to leave one failing test out of the launch review, just this once. It's the test that checks adults can't message teenagers they don't know. Everyone else is excited. What do you do?
    a: "Keep the test in the review, marked as failing, so whoever decides to ship anyway puts their name on it, as the [Many Hands](/pm/cards/many-hands/) card asks. Tell your lead what you see: a big goal making a real risk look small. If the room won't hear it, take it to someone outside it, such as your trust and safety or legal team. Being the only one with doubts doesn't make you wrong."
  - q: "**Beyond this module.** Your own line is yours to draw. Which line isn't?"
    a: The one the law draws. Ask your legal or privacy team which rules your product has to meet. Your own line sits beyond them.

deeper_one:
  title: "Automating Inequality"
  why: "Family by family, it shows who pays when an automated system gets someone wrong."
deeper:
  - title: Automating Inequality
    by: Virginia Eubanks
    where: A book.
    note: "Read chapter 4, \"The Allegheny Algorithm,\" then chapter 2, \"Automating Eligibility in the Heartland.\""
    trust: "An argument. Eubanks is a political scientist at the University at Albany, and she reports with a point of view: she chose cases that let the families affected speak. The county answered her, its tool changed after the book, and evaluations since disagree on how fair it is."
    only: Who carries a system's mistakes, and who isn't in its data at all. Allegheny County's screening tool draws on public-service records, so a family that pays privately for treatment leaves no trace in them.
  - title: Design Justice
    by: Sasha Costanza-Chock
    url: https://doi.org/10.7551/mitpress/12255.001.0001
    where: A book.
    note: "Free at direct.mit.edu, open access. Read the opening of the introduction, through the airport scanner and the network's principles, then chapter 2, \"Design Practices: 'Nothing about Us without Us.'\""
    trust: "An argument. Costanza-Chock was a research scientist at MIT and helps lead the Design Justice Network, whose principles the book sets out: an insider's view, drawn from cases, and openly normative."
    only: "An airport scanner that flags a body for not matching the button the operator pressed, and who it fails most. Chapter 2 asks who a team imagines as its user, a choice the book calls political."
  - title: Your Face Belongs to Us
    by: Kashmir Hill
    where: A book.
    note: Read it whole.
    trust: "Experience. It's reporting by the *New York Times* technology reporter whose exposé brought Clearview to light in early 2020."
    only: A startup that built what Google and Facebook had held back, face search across billions of scraped photos, and sold it to police, and a Black father in Michigan, arrested on a false match and held for nearly thirty hours.
  - title: "Pinto Fires and Personal Ethics: A Script Analysis of Missed Opportunities"
    by: Dennis Gioia (Journal of Business Ethics, 1992)
    url: https://doi.org/10.1007/BF00870550
    where: A journal article.
    trust: "Experience. Gioia was Ford's recall coordinator in the early 1970s, and he writes about his own part in the Pinto case."
    only: A first-person account of how an ethical question never came up, because it wasn't part of how he understood the job.
  - title: More Everything Forever
    by: Adam Becker
    where: A book.
    note: Read the introduction, then the chapter on effective altruism and longtermism.
    trust: "An argument. Becker is a science journalist with a doctorate in astrophysics, and he tests Silicon Valley's grand visions against the science they lean on. He writes as a critic, so read it as the case against."
    only: "AI, Mars, living forever and effective altruism in one book, and his summary of where longtermism leads: \"For a strong longtermist, investing in a Silicon Valley AI company is a more worthwhile humanitarian endeavor than saving lives in the tropics.\""
  - title: The Good Place
    by: created by Michael Schur (NBC, 2016 to 2020)
    where: A TV series.
    note: "A sitcom about moral philosophy. Watch \"The Book of Dougs,\" in season 3. Nobody has gotten into the Good Place in more than 500 years. Long ago, one Doug gives his grandmother flowers and earns 145 points. A modern Doug does the same and loses four, because his phone, his roses and the companies he paid each hurt someone he'll never see."
    only: "The [Many Hands](/pm/cards/many-hands/) card's problem, with jokes: harm spread so thin across a supply chain that nobody in it feels responsible."
---

## Why this matters

This module runs longer than the others, on purpose: it ties together earlier threads, and covers new ground too.

What you build reaches people you'll never meet. On a video-sharing app, small rules decide which video plays next, who can send a teenager a message, and what counts as a view.

Some of them live a world away. In 2017, Myanmar's military killed and raped Rohingya by the thousands and drove hundreds of thousands into Bangladesh. [UN investigators](https://www.ohchr.org/sites/default/files/Documents/HRBodies/HRCouncil/FFM-Myanmar/A_HRC_39_64.pdf) called for its generals to be tried for genocide, and found that Facebook had been "a useful instrument for those seeking to spread hate, in a context where, for most users, Facebook is the Internet." An assessment Facebook commissioned said it hadn't done enough, and Facebook agreed it should do more. In 2022, [Global Witness](https://globalwitness.org/en/campaigns/digital-threats/facebook-approves-adverts-containing-hate-speech-inciting-violence-and-genocide-against-the-rohingya/) submitted eight real examples of that hate speech to it as ads, in Burmese, and Facebook approved all eight. And in 2023, [Amnesty International found](https://www.amnesty.org/en/documents/afr25/7292/2023/en/) that Meta, as Facebook's owner is now called, had contributed to abuses again, against Tigrayans in Ethiopia's war.

You've met parts of this question already. {{< pm/mod know-who-its-for >}} asked whose problem you hear, and whose work an order rests on. {{< pm/mod see-the-system >}} asked whose costs fall outside a system's edge, {{< pm/mod find-the-constraint >}} whom a stand-in measure misses, and {{< pm/mod mind-the-seams >}} who falls between two categories. {{< pm/mod design-for-change >}} asked who pays for a change, and {{< pm/mod change-safely >}} and {{< pm/mod weigh-the-evidence >}} whom an average hides. Here it's the whole module.

So ask two things of what you build. Who gains, and who pays? A product can earn by helping people or by making it hard for them to leave. It can cut a cost by designing it away, or by passing it to parts of the system that are less visible or have less say. For a while, each pair looks the same on a dashboard.

In life, ethical matters rarely come to you as clear cases of good and bad. Instead, it's a thousand small choices of degree, {{< pm/voice "eye-doctor" >}}. {{< pm/voice "own-line" >}} But wherever you land, hold fast.

The hardest place to hold fast may be inside, in a mission you believe in. Some tech leaders talk about their products the way prophets talk about salvation. Marc Andreessen writes that deaths an AI held back could have prevented are ["a form of murder,"](https://a16z.com/the-techno-optimist-manifesto/) and lists "trust and safety" and "tech ethics" under the heading "The Enemy." Bryan Johnson says of his longevity project, ["Don't Die is a religion."](https://www.npr.org/transcripts/1263527103) Scholars hear older stories in this. Mary-Jane Rubenstein, who studies religion, finds in the billionaires' race to space ["a barely-disguised doomsday prophecy."](https://nextbigideaclub.com/magazine/astrotopia-dangerous-religion-corporate-space-race-bookbite/37624/) The historian Jason Resnikoff hears in today's AI talk an echo of last century's talk of automation, which made its outcomes ["seem natural, even inevitable."](https://www.equaltimes.org/jason-resnikoff-us-labour) On a video app it's quieter: the new feed is the company's future, so the launch can't slip. The pull works because the mission is often real, and that's what makes its costs look small. [The Mission Excuse](/pm/cards/mission-excuse/) card says how to spot it, and Erika Cheung's talk shows how it feels from inside.

[//]: # (short-path)

## Do

**Scan one feature you own (30 minutes).** Pick a feature, such as how the feed ranks videos or who can comment, and run a {{< pm/term "consequence-scanning" "consequence scan" >}} on it. In short notes, answer the method's three questions in order:

1. What are the intended and unintended consequences? Name everyone affected, including the easiest to overlook, like the person in the background of someone else's video. Then look where groups overlap. A harm can be invisible in each group alone and plain for the people in both: the overlap Kimberlé Crenshaw called {{< pm/term "intersectional" >}}, as you saw in {{< pm/mod mind-the-seams >}}.
2. Which positive consequences do you want to focus on?
3. Which do you want to mitigate? Beside each one, write who'd own the fix.

End with one change you'd propose. Outside the 30 minutes, show it to someone in support or in trust and safety, and ask what you missed.

**Write your lines (5 minutes).** Before anyone asks, write down two things you won't do for any mission, however much you believe in it, such as launching past a failing child-safety test, or keeping data you told users you'd delete. Beside them, write who outside your team you'd go to if you were asked to cross one. If you don't know who that is, ask your manager this week. The example leaves them out: your lines are yours to draw.

**For your decision log.** Write the change you'd propose, and what you expect it to cost or save, and for whom. Then write how sure you are, and when you'll know.

{{< pm/example >}}

**Optional: list what the feature keeps (15 minutes).** List each data field it collects, next to the decision that uses it, and mark any field with no decision. Ask who the fields can't record as they are, such as someone whose name won't split into first and last, or a child with two mothers. Then pick one field. If a customer used their {{< pm/term "right-to-erasure" "right to erasure" >}}, could you find every copy, in the backups and at the companies you share it with?
