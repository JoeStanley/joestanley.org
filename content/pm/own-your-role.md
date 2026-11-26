---
title: Own Your Role
layout: module
module: own-your-role
question: How do you grow your role beyond what you were handed, and make the product's vision your own?
setting: a music streaming app
one_thing: Finish "We're building this in order to ..." for your work, then ask two teammates to finish it without seeing yours.
do_minutes: 35

steps:
  - id: card-champion
    kind: card
    card: cards/concept-champion
    minutes: 5
    look: What the two look-alike jobs leave undone, and how to work back from a destination.
  - id: brooks
    kind: read
    title: Fred Brooks, "Aristocracy, Democracy, and System Design"
    minutes: 15
    where: Chapter 4 of The Mythical Man-Month. Free as the publisher's sample chapter.
    links:
      - text: "Aristocracy, Democracy, and System Design"
        url: https://ptgmedia.pearsoncmg.com/images/0201835959/samplechapter/chap4.html
    look: Why he let 150 implementers write the specifications to save the schedule, and what it cost.
    trust: "Experience. Brooks managed IBM's System/360 and its operating system in the 1960s, so you're hearing it from the man who made the call."
    only: A first-hand case of trading a product's conceptual integrity for the schedule, and getting neither.
  - id: vogels
    kind: read
    title: Werner Vogels, "Working Backwards"
    minutes: 5
    where: A blog post. Free at allthingsdistributed.com.
    links:
      - text: "Working Backwards"
        url: https://www.allthingsdistributed.com/2006/11/working_backwards.html
    look: Why the press release comes first, before a line of code, and what the FAQ and the user manual add to it.
    trust: "Experience. Vogels was Amazon's chief technology officer when he wrote it, in 2006, describing how its teams start a product."
    only: The shortest way into working backwards, in four steps you take before you build.
  - id: reilly
    kind: read
    title: Tanya Reilly, "Being Glue"
    minutes: 20
    where: A talk, as text beside its slides. Free at noidea.dog.
    links:
      - text: "Being Glue"
        url: https://noidea.dog/glue
    look: What glue work is, why it so rarely gets anyone promoted, and the conversation to have about it before your review.
    trust: "Experience. Reilly is a principal software engineer, telling a story from the kind of career she's watched and had."
    only: The cost of the work that holds a team together, for the person who does it.
  - id: do
    kind: do
    title: Finish the sentence
    where: The Do, on this page, below. Asking two teammates can come later.
    look: Outcomes, changes for people, not features you ship.
  - id: check
    kind: check
    title: Check yourself
    where: The Check, on this page, below.
    look: The answers you missed, and why you missed them.

check:
  - q: It's Thursday, and your week on the streaming app has gone to standup, two status reports and a meeting where you split the next sprint so each squad gets something. Your lead set the destination last quarter. Which versions of the job filled your week, and what's yours to add?
    a: Both look-alikes. The standup and the status reports are running the project, and splitting the sprint so everyone gets something is running the room. Yours to add is the vision's part in your slice. Finish its "in order to" for your own work, check it against your team's and your lead's, and say where they don't fit.
  - q: The date for your streaming app's new playlists is slipping, and someone suggests each squad write its own part of the spec to save time. What does Brooks's story warn it costs?
    a: Its conceptual integrity, one set of design ideas throughout, and maybe not even the date. When Brooks let 150 implementers write the specifications to save the schedule, the specifications came out late anyway, and the lost integrity cost his system, by his estimate, a year of debugging time.
  - q: Half your last month went to onboarding two engineers, writing up every meeting and chasing the teams the playlists depend on. Your review is next month. What would Reilly have you do?
    a: Talk with your manager now, not after the review. Ask which of that work counts toward it, keep the glue the team really needs, and push back on doing more than your share of the rest.
  - q: "**Beyond this module.** What can't any course tell you about the job you have?"
    a: What your company means by it. The same title covers very different work from one company to the next, so ask your manager and the leads you work with what they'd miss if you stopped doing it, and what they wish you'd start.
deeper:
  - title: Product Development Performance
    by: Kim Clark and Takahiro Fujimoto
    where: A book.
    note: "Read chapter 9, \"Leadership and Organization: The Heavyweight Product Manager.\" Internet Archive's lending library has it."
    trust: "A study. The full one behind the card, by two of the researchers who ran it."
    only: The heavyweight product manager at full length, the "concept infuser" who carries one idea of the car into every team's work.
  - title: The Reflective Practitioner
    by: Donald Schön
    where: A book.
    note: "Read chapter 2, \"From Technical Rationality to Reflection-in-Action,\" and chapter 8, \"The Art of Managing: Reflection-in-Action Within an Organizational Learning System.\""
    trust: "An argument. Schön watched professionals at work, case by case, from engineers and architects to managers and town planners, and he builds his case on what he saw."
    only: How good practitioners handle a case their training didn't cover, by thinking while they act. Chapter 8 turns it on managers.
  - title: Working Backwards
    by: Colin Bryar and Bill Carr
    where: A book.
    note: "Read chapter 5, \"Working Backwards: Start with the Desired Customer Experience,\" and chapter 3, \"Organizing: Separable, Single-Threaded Leadership.\" The authors' free article on the PR/FAQ, at workingbackwards.com, gives the template in brief, with a pitch for their course."
    trust: "Experience. Two former Amazon executives, with close to thirty years there between them, who now teach the method for a living, so expect them to champion it."
    only: How a press release and its FAQ get written, read and picked apart in a meeting, and rewritten before anything is built, and the single-threaded leader, one owner for one initiative, the role at its fullest.
  - title: "Crafting a Job: Revisioning Employees as Active Crafters of Their Work"
    by: Amy Wrzesniewski and Jane Dutton (Academy of Management Review, 2001)
    where: A journal article.
    trust: "An argument. It's peer-reviewed theory, the paper that named job crafting."
    only: "Three levers for reshaping a job yourself: your tasks, your working relationships, and how you see the work's purpose. Notice which one you use least."
  - title: Mozart in the Jungle
    by: developed by Roman Coppola, Jason Schwartzman, Alex Timbers and Paul Weitz (Amazon Prime Video, 2014 to 2018)
    where: A TV series.
    note: "Start with season 1. Rodrigo explains where \"the blood\" comes from at the end of season 3, and in season 4, episode 6, a robot conducts flawlessly and it's the orchestra that makes the music beautiful. It's a comedy, inspired by the oboist Blair Tindall's memoir of playing in New York."
    only: "What mastering a craft asks of people who are already good: an oboist with feeling and not yet control, and a conductor who wants both, from everyone."
---

## Why this matters

In the tabletop role-playing community, there's the concept of Rule Zero: The game runner or other players can modify any rule, narrative element, anything where it would better suit their local experience. The game construct is to enable meaningful experiences, and a table sacrificing that to follow the letter of the rules has done so at the cost of their broader intent. It's called Rule Zero because it's a meta rule, sitting outside the framework entirely.

{{< pm/voice "rule-zero" "paragraph" >}}

So take the job as described first, and do it well enough that people trust you with more. Then, once you see the system around you, grow the role toward value nobody assigned, like the gap at your team's edge that nobody owns. Researchers call reshaping a job from the inside {{< pm/term "job-crafting" >}}: changing its tasks, who you work with, or how you see its purpose (Wrzesniewski and Dutton, 2001).

Much of what you'll find in those gaps is {{< pm/term "glue-work" >}}, Tanya Reilly's name for the work that holds a team together, like noticing when someone's blocked and helping them out. The team needs it, and it rarely counts when promotions are decided, so watch how much of your week it takes, and talk with your manager about how it counts before your review, not after. Her warning is the one to carry: "If you only do glue, you will only get better at glue." Notice, too, who on your team does most of it. Economists have found that women volunteer for work that does little for a promotion more often than men do, are asked more often, and say yes more often (Babcock and colleagues, 2017).

Two versions of the job look real and aren't. In one, you run the project: dates, status, who's blocked. In the other, you run the room and average what everyone wants. You'll do plenty of both, but the job is the product's vision: what it's for and where it's going. Cultivate it, share it until the team can say it too, and work back from it.

Early on, someone above you usually names that destination. On a music streaming app, your lead might set it as the place people find music they'll love, while you own search. Making the vision your own then means knowing it well enough to finish the sentence "We're building this in order to ..." for your slice of the work, checking your sentence against your team's, and saying where they don't fit. Where nobody has named a destination, draft one and bring it to whoever sets the product's direction. Decide and Set Direction comes back to this sentence: it's the intent you hand out with each task.

The vision has to be yours, too, in a second sense: a product can be right in every detail and still say nothing. In the second episode of *Mozart in the Jungle*, the orchestra's president, Gloria Windsor (played by the incomparable Bernadette Peters), is sure the new oboist plays flawlessly. "No, she doesn't play flawlessly," says the conductor, Rodrigo De Souza. "She plays with blood, and that's what matters." He asks it of everyone: play with the blood. It matters because people respond to the person in the work. Every product is creative work in some way, and creative work is how one mind reaches another. {{< pm/voice "human-existence" >}}

Now with all this said, a word of caution: you champion the vision, but you're not a dictator. To extend the musical comparison, you're a bit composer, a bit conductor. The people you'll work with aren't resources or tools, they're human beings with their own agency, views, and experience. {{< pm/voice "symphony" >}} Decide and Set Direction gives you one habit for it: when the call is yours, give your view last.

[//]: # (short-path)

## Do

**Finish the sentence (25 minutes).** Engineers often write the test before the code, and you can borrow the move. Teams building AI features do the same, and call their tests evaluations. Finish "We're building this in order to ..." for your slice of the work. Then write your tests: three things that would be true if you got there, each with how you'd check it. Make each one an outcome, a change for people, not an output, a feature you ship. That's what teams mean by "outcomes over outputs." Now read it as someone your work touches but the sentence never names: on a music streaming app, say, the musicians whose songs it plays. Would they want you to get there? Outside the 25 minutes, ask two teammates to finish the sentence without seeing yours. Where the versions differ, the vision isn't settled, and bringing that to your team, or to whoever sets direction, is your job.

**Optional: map your scope (10 minutes).** List what you were handed, one thing you do that nobody asked for, and one gap at your edge that nobody seems to own. Then look back over last week. How much of it went to glue work, and what did that crowd out?
