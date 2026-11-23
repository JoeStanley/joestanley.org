---
title: Own Your Role
layout: module
module: own-your-role
question: How do you grow your role beyond what you were handed, and make the product's vision your own?
setting: a music streaming app
one_thing: Finish "We're building this in order to ..." for your product, then ask two teammates to finish it without seeing yours.
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
    only: A first-hand case of the schedule beating a product's conceptual integrity.
  - id: meadows
    kind: read
    title: Donella Meadows, "Envisioning a Sustainable World"
    minutes: 20
    where: A paper. Free at donellameadows.org.
    links:
      - text: "Envisioning a Sustainable World"
        url: https://donellameadows.org/archives/envisioning-a-sustainable-world/
    look: She judges a vision by how clear its values are, not how clear the path to it is.
    trust: "Experience. Meadows, the systems scientist you'll meet in See the System, writing from her own practice. Her subject is a sustainable world, not a product."
    only: The one reading here on forming a vision and keeping it open to correction.

check:
  - q: Which two versions of the job look real and aren't, and what do both leave undone?
    a: Running the project and running the room. Neither cultivates the vision nor shares it.
  - q: The date for your streaming app's new playlists is slipping, and someone suggests each squad write its own part of the spec to save time. What does Brooks's story warn it costs?
    a: Its conceptual integrity, one set of design ideas throughout. When Brooks let 150 implementers write the specifications to save the schedule, it cost his system that, and by his estimate a year of debugging time.
  - q: What does Meadows judge a vision by, and what does she do with hers?
    a: How clear its values are, not how clear the path is. And she shows it to other people, who correct and refine it.
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
  - title: Understanding by Design
    by: Grant Wiggins and Jay McTighe
    where: A book.
    note: "Read chapter 1, \"Backward Design.\""
    trust: "Experience. Two educators explaining their own method to teachers, so expect them to champion it."
    only: "Backward design, test-first's cousin in teaching: name the result, decide what evidence would show you got there, then plan. It's the Do's first exercise, worked out at length."
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

In the same way, Module Zero lays out what it means to be an actual product manager.

You'll start every PM role by taking it as described. Once you see the system around you, grow the role toward value nobody assigned.

Two versions of the job look real and aren't. In one, you run the project: dates, status, who's blocked. In the other, you run the room and average what everyone wants. You'll do plenty of both, but the job is the product's vision: what it's for and where it's going. Cultivate it, share it until the team can say it too, and work back from it. If you don't name that destination, usually nobody does.

The vision has to be yours, too, because a product can be right in every detail and still say nothing. In the second episode of *Mozart in the Jungle*, the orchestra's president, Gloria Windsor (played by the incomparable Bernadette Peters), is sure the new oboist plays flawlessly. "No, she doesn't play flawlessly," says the conductor, Rodrigo De Souza. "She plays with blood, and that's what matters." He asks it of everyone: play with the blood. It matters because people respond to the person in the work. Every product is creative work in some way, and creative work is how one mind reaches another. {{< pm/voice "human-existence" >}}

Now with all this said, a word of caution: you champion the vision, but you're not a dictator. To extend the musical comparison, you're a bit composer, a bit conductor. The people you'll work with aren't resources or tools, they're human beings with their own agency, views, and experience. {{< pm/voice "symphony" >}}

[//]: # (short-path)

## Do

**Finish the sentence (25 minutes).** Engineers often write the test before the code, and you can borrow the move. Finish "We're building this in order to ..." for your current work. Then write your tests: three things that would be true if you got there, each with how you'd check it. Make each one an outcome, a change for people, not an output, a feature you ship. That's what teams mean by "outcomes over outputs." Now read it as someone your work touches but the sentence never names: on a music streaming app, say, the musicians whose songs it plays. Would they want you to get there? Outside the 25 minutes, ask two teammates to finish the sentence without seeing yours. Where the versions differ, the vision isn't settled, and settling it is your job.

**Optional: map your scope (10 minutes).** List what you were handed, one thing you do that nobody asked for, and one gap at your edge that nobody seems to own. Reshaping a job from the inside is what researchers call {{< pm/term "job-crafting" >}}: changing its tasks, who you work with, or how you see its purpose (Wrzesniewski and Dutton, 2001). Then ask yourself how much of your week went to {{< pm/term "glue-work" >}}, as Tanya Reilly calls the work that holds a team together, and what it crowded out. Notice, too, who on your team does most of it. Economists have found that women volunteer for work that does little for a promotion more often than men do, are asked more often, and say yes more often (Babcock and colleagues, 2017).
