---
title: Own Your Role
layout: module
module: own-your-role
question: How do you grow your role beyond what you were handed, and make the product's vision your own?
setting: a music streaming app
one_thing: Finish "We're building this in order to ..." for your work, then ask two teammates (ideally from different job families) to finish it without seeing yours.
do_minutes: 30

steps:
  - id: card-champion
    kind: card
    card: cards/concept-champion
    minutes: 5
    look: What the two look-alike jobs leave undone.
  - id: brooks
    kind: read
    title: Fred Brooks, "Aristocracy, Democracy, and System Design"
    minutes: 20
    where: Chapter 4 of The Mythical Man-Month. Free as the publisher's sample chapter.
    links:
      - text: "Aristocracy, Democracy, and System Design"
        url: https://ptgmedia.pearsoncmg.com/images/0201835959/samplechapter/chap4.html
    look: Why he let 150 implementers write the specifications to save the schedule, and what it cost.
    trust: "Experience. Brooks managed IBM's System/360 and its operating system in the 1960s, so it's from the man who made the call."
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
    trust: "Experience. Vogels was Amazon's chief technology officer when he wrote it, in 2006."
    only: The shortest way into working backwards, in four steps you take before you build.
  - id: reilly
    kind: read
    title: Tanya Reilly, "Being Glue"
    minutes: 25
    where: A talk, as text beside its slides. Free at noidea.dog.
    links:
      - text: "Being Glue"
        url: https://noidea.dog/glue
    look: What glue work is, why it rarely gets anyone promoted, and the conversation to have before your review.
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

example:
  body: |
    **Search, in order to:** help listeners who know only a lyric or hum find the song, then something new they'll keep.

    **Tests:**

    - Fewer lyric and hum searches end with nothing played: from 1 in 3 to 1 in 5.
      - Means: Search logs, monthly.
    - More saves of songs suggested after the match, by artists the listener had never played.
      - Means: Save logs.
    - More of those saves still played a month later.
      - Means: Play history.

    **As the musicians:** a small artist gains only if "something new" isn't ranked by plays alone. Test 2 also counts the share from artists outside the top 10,000.

    **Later, two teammates:** design wrote "faster search," engineering "fewer empty results." Both are outputs, and neither wrote anything about discovery. The vision is not settled: take it to the lead on Thursday.
  good:
    - Each test counts what listeners do, plays and saves, never what the team ships.
    - Reading it as the musicians found who could lose, and changed a test to watch for them.
    - Where the teammates' sentences differ, it names the gap and when it goes to the lead.

check:
  - q: It's Thursday. In terms of time, your week on the streaming app has gone to standup, two status reports, and a meeting where you split the next sprint so each squad gets something. Your lead set the destination last quarter. Which versions of the job filled your week, and what's yours to add?
    a: "Both of the imposters. The standup and the status reports are a form of running the project, and splitting the sprint so everyone gets something is running the room. Ask yourself — did it need to be you who did these things? Your role is to refine and champion the vision, which no part of your week clearly went toward: finish its \"in order to,\" check it against your team's and your lead's, and say where they don't fit."
  - q: The date for your streaming app's new playlists is slipping, and someone suggests each squad write its own part of the spec to save time. What could that cost, and does it even save the date?
    a: Its conceptual integrity, one set of design ideas throughout. And it may not save the date. When Brooks let 150 implementers write the specifications to save the schedule, the specifications came out late anyway, and the lost integrity cost his system, by his estimate, a year of debugging time.
  - q: Half your last month went to onboarding two engineers, writing up every meeting and chasing the teams the playlists depend on. Your review is next month. What would Reilly have you do?
    a: Talk with your manager now, not after the review. Ask which of that work counts toward it, keep the glue the team really needs, and push back on doing more than your share of the rest.
  - q: "**Beyond this module.** What can't any course tell you about the job you have?"
    a: What your company means by it. The expectations of product management vary wildly company to company, so ask your manager and the leads you work with what they'd miss if you stopped doing it, what they wish you'd start, or (if you're coming into a new role) what success means to them in a year's time.
deeper_one:
  title: "Working Backwards"
  why: "It shows the press release written before anything is built, a habit you can try this week, as Amazon runs it."
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
    trust: "An argument. Schön watched professionals at work, from engineers to town planners, and builds his case on what he saw."
    only: How good practitioners handle a case their training didn't cover, by thinking while they act. Chapter 8 turns it on managers.
  - title: Working Backwards
    by: Colin Bryar and Bill Carr
    where: A book.
    note: "Read chapter 5, \"Working Backwards: Start with the Desired Customer Experience,\" and chapter 3, \"Organizing: Separable, Single-Threaded Leadership.\" Their free article on the PR/FAQ, at workingbackwards.com, gives the template in brief, with a pitch for their course."
    trust: "Experience. Two former Amazon executives, with close to thirty years there between them, who now teach the method for a living, so expect them to champion it."
    only: How a press release and its FAQ get written, picked apart in a meeting and rewritten before anything is built, and the single-threaded leader, one owner for one initiative, the role at its fullest.
  - title: "Crafting a Job: Revisioning Employees as Active Crafters of Their Work"
    by: Amy Wrzesniewski and Jane Dutton (Academy of Management Review, 2001)
    where: A journal article.
    trust: "An argument. It's peer-reviewed theory, the paper that named job crafting."
    only: "Three levers for reshaping a job yourself: your tasks, your working relationships, and how you see the work's purpose. Notice which one you use least."
  - title: Mozart in the Jungle
    by: developed by Roman Coppola, Jason Schwartzman, Alex Timbers and Paul Weitz (Amazon Prime Video, 2014 to 2018)
    where: A TV series.
    note: "Start with season 1. Rodrigo explains where \"the blood\" comes from at the end of season 3, and in season 4, episode 6, a robot conducts flawlessly but it's the orchestra that makes the music beautiful. It's a comedy, loosely inspired by the oboist Blair Tindall's memoir of playing in New York."
    only: What mastering a craft asks of people who are already good.
---

## Why this matters

In the tabletop role-playing community, there's the concept of Rule Zero: The game runner or other players can modify any rule, narrative element, anything where it would better suit their local experience. The game system is to enable meaningful experiences, and a table sacrificing that to follow the letter of the rules has done so at the cost of the system's broader intent. It's called Rule Zero because it's a meta rule, sitting outside the system's frame entirely.

A job description works the same way. It's a point-in-time set of expectations to enable someone to add value to the organization. But where following its letter would cost the organization (or in a PM's specific case, the product), you should probably reshape the job. That's why this module is numbered zero: it's about the frame you work in, not the work itself.

So take the job as described first, and do it well enough that people trust you with more. Then, once you get a handle on things, grow the role toward value nobody assigned, like the gap at your team's edge that nobody owns. Researchers call reshaping a job from the inside {{< pm/term "job-crafting" >}}: changing its tasks, who you work with, or how you see its purpose (Wrzesniewski and Dutton, 2001).

Much of what you'll find in those gaps is {{< pm/term "glue-work" >}}, Tanya Reilly's name for the work that holds a team together, like noticing when someone's blocked and helping them out. The team needs it, and it rarely counts when promotions are decided, so watch how much of your week it takes, and talk with your manager about it if you find more and more of your time going toward it. Her warning is worth remembering: "If you only do glue, you will only get better at glue." Notice, too, who on your team does most of it. Economists have found that women volunteer for work that does little for a promotion more often than men do, are asked more often, and say yes more often ([Babcock and colleagues, 2017](https://doi.org/10.1257/aer.20141734)).

Two versions of the job look real and aren't. In one, you're a project manager: you're tracking dates, status, who's blocked. In the other, you're the facilitator: you're running the room and repeating back what everyone wants.

You'll do plenty of both, but the job is the product's vision: what it's for and where it's going. Cultivate it, share it until the team can say it too, and work back from it.

Early in your career, someone above you usually names that destination. On a music streaming app, your lead might set it as the place people find music they'll love, while you own search. But even in this context, you'll likely have some degree of flexibility in solving your piece of the bigger problem — that's your room to craft a vision. {{< pm/mod decide-and-set-direction >}} comes back to this sentence: it's the intent you hand out with each task.

The vision has to be yours, too, in a second sense: a product can be right in every detail and still say nothing. In the second episode of *Mozart in the Jungle*, the orchestra's president is sure the new oboist plays flawlessly. "No, she doesn't play flawlessly," says the conductor, Rodrigo De Souza. "She plays with blood, and that's what matters." He asks it of everyone: play with the blood. It matters because people respond to the person in the work. I expect you can feel it in the products you use (or don't) in your own life — which have a sense of personality, and which feel lifeless even if useful? It's been my experience people will generally prefer the imperfect product with a point of view over the perfect one without.

Now with all this said, a word of caution: you champion the vision, but you're not a dictator. To extend the musical comparison, you're a bit composer, a bit conductor. The people you'll work with aren't resources or tools, they're human beings with their own agency, views, and experience. Guide them, make hard choices when necessary, but above all, respect and work with them.

[//]: # (short-path)

## Do

**Finish the sentence (30 minutes).** A best practice in engineering is to write the test before the code. Teams building AI features do the same, and call their tests evaluations. So can you. Finish "We're building this in order to ..." for the work you own. Then write your tests: three things that would be true if you got there, each with how you'd check it, and a target where you know today's number. Make each one an outcome, a change for people, not an output, a feature you ship. That's what teams mean by "outcomes over outputs." Read it as someone your work touches but the sentence never names: on a music streaming app, say, the musicians whose songs it plays. Would they want you to get there? If not, change a test to watch for them. Outside the 30 minutes, ask two teammates, one an engineer on the work, to finish the sentence without seeing yours. Where the versions meaningfully differ, the vision isn't settled: take that to your team or whoever sets direction. Then ask the engineer which of your tests they could measure today, and what the rest would take.

{{< pm/example >}}

**Optional: map your scope (15 minutes).** List what you were handed in your job responsibilities (a specific example), one thing you do that nobody asked for, and one gap at your edge that nobody seems to own. Then look back over last week. How much of it went to glue work, and what did that crowd out?
