---
title: Answer for What You Build
layout: module
module: answer-for-what-you-build
question: Who benefits and who is harmed by what we build, and what's our share of the responsibility?
setting: a video-sharing app
one_thing: Run a consequence scan on one feature you own, and write down one change you'd propose.
do_minutes: 40

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
    minutes: 15
    where: A talk, with a transcript. Free at ted.com.
    links:
      - text: "Theranos, whistleblowing and speaking truth to power"
        url: CHEUNG_URL
    look: "When her doubts begin, what she's told when she raises them, and the question she asks after: what happens when \"the vision is so compelling and the desire to believe is so strong that it starts to cloud your judgment about what reality is?\""
    trust: "Experience. Cheung joined Theranos straight out of college, raised her concerns inside, and was told to do what she was paid to do. It's her own account."
    only: What the pull feels like from the inside, for someone early in her career, down to the moment she wonders if she's the crazy one.
  - id: schneier
    kind: read
    title: 'Bruce Schneier, "Data Is a Toxic Asset, So Why Not Throw It Out?"'
    minutes: 10
    where: An essay. Free at schneier.com.
    links:
      - text: "Data Is a Toxic Asset, So Why Not Throw It Out?"
        url: https://www.schneier.com/essays/archives/2016/03/data_is_a_toxic_asse.html
    look: "Why he treats stored data as a liability, and one test to put to every field you collect: which decision will it change?"
    trust: "An argument. Schneier is a security technologist, and CNN first published the essay."
    only: "His fix, in one line: \"there's no better security than deleting the data.\""
  - id: inclusive
    kind: read
    title: GOV.UK Service Manual, "Making your service more inclusive"
    minutes: 5
    where: A guide for the UK government's digital teams. Free at gov.uk.
    links:
      - text: "Making your service more inclusive"
        url: https://www.gov.uk/service-manual/design/making-your-service-more-inclusive
    look: Why "Is this your first child?" is hard for some people to answer, and the fix, "Focus on what your service really needs to know." It's Schneier's test from the service side.
    trust: "Experience. It's the UK government's guidance for its own services, which have to work for everyone, since people usually have no alternative to using them. Parts are written for a public service's legal duties."
    only: A test for every field you ask people to fill in, and the common reasons people get shut out, from time and trust to the evidence they're asked for.

check:
  - q: A change lifts hours watched on your video app by starting the next video without asking. Has it created value?
    a: Ask whether viewers are better off, or only up later than they meant to be. If they'd switch it off given a plain choice, those hours were taken from them, not created for them.
  - q: To meet sales targets, Wells Fargo employees opened accounts customers hadn't asked for. See the System would look at the structure, not the people. Here, each employee still had a share. Who's right?
    against: see-the-system
    a: "See the System, when you ask why it happened and how to stop it: change the targets. This module, when you're the one asked to hit them: a target explains a choice, but it doesn't make it for you."
  - q: A teammate wants a new sign-up field "in case we need it." What do you ask?
    a: Which decision will it change? If none does yet, leave it out. Every field you keep is something to secure, and something to find when a customer asks you to erase it.
  - q: Your CEO calls the new feed the company's future. To make the launch date, your lead asks you to leave one failing test out of the launch review, just this once. Everyone else is excited. What do you do?
    a: "Name the move: a big end making a small harm look fine. Ask who pays if the test is right, and whether you'd still ship if the vision never came true. Say so to your lead, and if the room won't hear it, take it to someone outside it, such as your legal or trust and safety team. Being the only doubter is a reason to slow down, not proof you're wrong."
  - q: "**Beyond this module.** Your own line is yours to draw. Which line isn't?"
    a: The one the law draws. Ask your legal or privacy team which rules your product has to meet. Your own line sits beyond them.

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
  - title: The Good Place
    by: created by Michael Schur (NBC)
    where: A TV series.
    note: "A sitcom about moral philosophy. Watch \"The Book of Dougs,\" in season 3. Nobody has gotten into the Good Place in more than 500 years. Long ago, one Doug gives his grandmother flowers and earns 145 points. A modern Doug does the same and loses four, because his phone, his roses and the companies he paid each hurt someone he'll never see."
    only: "The Many Hands card's problem, with jokes: harm spread so thin across a supply chain that nobody in it feels responsible."
---

## Why this matters

This module runs longer than the others, on purpose. It ties together threads you've met in earlier modules, and it still has new ground to cover.

What you build reaches people you'll never meet. On a video-sharing app, small rules decide which video plays next, who can send a teenager a message, and what counts as a view.

Some of them live a world away. In 2017, Myanmar's military killed and raped Rohingya by the thousands and drove hundreds of thousands into Bangladesh. [UN investigators](https://www.ohchr.org/sites/default/files/Documents/HRBodies/HRCouncil/FFM-Myanmar/A_HRC_39_64.pdf) called for its generals to be tried for genocide, and found that Facebook had been "a useful instrument for those seeking to spread hate, in a context where, for most users, Facebook is the Internet." An assessment Facebook commissioned said it hadn't done enough, and Facebook agreed it should do more. In 2022, [Global Witness](https://globalwitness.org/en/campaigns/digital-threats/facebook-approves-adverts-containing-hate-speech-inciting-violence-and-genocide-against-the-rohingya/) submitted eight real examples of that hate speech to it as ads, in Burmese, and Facebook approved all eight. And in 2023, Amnesty International found that Meta, as Facebook's owner is now called, had contributed to abuses again, against Tigrayans in Ethiopia's war.

You've met parts of this question already. Know Who It's For asked whose problem you hear, and whose work an order rests on. See the System asked whose costs fall outside a system's edge, Find the Constraint whom a stand-in measure misses, and Mind the Seams who falls between two categories. Design for Change asked who pays for a change, and Change Safely and Weigh the Evidence whom an average hides. Here it's the whole module.

So ask two things of what you build. Who gains, and who pays? A product can earn by helping people or by making them hard to leave. It can cut a cost by designing it away, or by passing it to parts of the system that are less visible or have less say. For a while, each pair looks the same on a dashboard.

The hardest pressure may come from inside, from a mission you believe in. Tech leaders often talk about their products the way prophets talk about salvation. Marc Andreessen calls AI that's held back ["a form of murder,"](ANDREESSEN_URL) and names "tech ethics" and "trust and safety" among his enemies. Bryan Johnson says of his longevity project, ["Don't Die is a religion."](JOHNSON_URL) Mary-Jane Rubenstein, a scholar of religion, hears in the billionaires' race to space ["a barely-disguised doomsday prophecy."](RUBENSTEIN_URL) The historian Jason Resnikoff hears last century's talk of automation, which made its outcomes ["seem natural, even inevitable."](RESNIKOFF_URL) A story that big makes any cost in its way look small, and any doubt look like disloyalty. The Mission Excuse card says how to spot it, and Erika Cheung's talk shows how it feels from inside.

In life, ethical matters rarely come to you as clear cases of good and bad. Instead, it's a thousand small choices of degree, {{< pm/voice "eye-doctor" >}}. {{< pm/voice "own-line" >}} But wherever you land, hold fast.

[//]: # (short-path)

## Do

**Scan one feature you own (25 minutes).** Pick a feature, such as autoplay or the way the feed ranks videos, and run a {{< pm/term "consequence-scanning" "consequence scan" >}} on it. On one page, answer the method's three questions in order:

1. What are the intended and unintended consequences? Name everyone affected, including the easiest to overlook, like the person in the background of someone else's video. Then look where groups overlap. A harm can be invisible in each group alone and plain for the people in both: the overlap Kimberlé Crenshaw called {{< pm/term "intersectional" >}}, as you saw in Mind the Seams.
2. Which positive consequences do you want to focus on?
3. Which do you want to mitigate? Beside each one, write who'd own the fix.

End with one change you'd propose. Outside the 25 minutes, show it to someone in support or in trust and safety, and ask what you missed.

**Write your lines first (5 minutes).** Before anyone asks, write down two things you won't do for any mission, however much you believe in it. Beside them, write who outside your team you'd go to if you were asked. Keep the page somewhere you'll see it again.

**For your decision log.** Write the change you'd propose, and what you expect it to cost or save, and for whom. Then write how sure you are, and when you'll know.

**Optional: list what the feature keeps (10 minutes).** List each data field it collects, next to the decision that uses it, and mark any field with no decision. Ask who the fields can't record as they are, such as someone whose name won't split into first and last, or a child with two mothers. Then pick one field. If a customer used their {{< pm/term "right-to-erasure" "right to erasure" >}}, could you find every copy, in the backups and at the companies you share it with?
