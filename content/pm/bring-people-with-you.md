---
title: Bring People With You
layout: module
module: bring-people-with-you
question: How do you earn the trust of the people who decide and depend on you, and keep it when there is nothing to report?
one_thing: Send your most senior reader a short update on a day you've named, with one item in it that isn't on track.
do_minutes: 40

last_time:
  - q: Every retro ends with a process tweak. What question is missing?
    a: Whether the goal is right. A tweak changes the method to hit the same goal, which is single-loop learning. The double loop asks why the goal is what it is.
  - q: Complaints to support fell by half this quarter. Is that good news?
    a: Not on its own. Low numbers can mean people stopped telling you. Ask the support lead what changed, and who'd be the last to write in.

steps:
  - id: mulally
    kind: read
    title: 'Alan Mulally and Jim Morgan, "People First Leadership"'
    minutes: 5
    where: A podcast transcript. Free at lean.org. Read the section headed "How to Encourage Transparency and Information Sharing".
    links:
      - text: "People First Leadership"
        url: https://www.lean.org/the-lean-post/articles/people-first-leadership-a-conversation-between-jim-morgan-and-alan-mulally/
    look: What it said about Ford that all 300 status charts showed everything on track, at a company about to lose billions, and what Mulally, then its chief executive, did when Mark Fields showed the first one that didn't.
    trust: It's Mulally telling his own story, years later, on the Lean Enterprise Institute's podcast. One man's memory of a moment he's proud of, so hold the details loosely.
    only: "The moment a habit of reporting only good news broke, and the same rule that buried Product X's bad news: at Ford, \"you only brought an issue to your supervisor or your manager when you had a solution.\""
  - id: card-trust-equation
    kind: card
    card: cards/trust-equation
    minutes: 5
    look: Why self-orientation sits under the other three.
  - id: larson
    kind: read
    title: 'Will Larson, "Staying aligned with authority"'
    minutes: 5
    where: A guide. Free at staffeng.com.
    links:
      - text: "Staying aligned with authority"
        url: https://staffeng.com/guides/staying-aligned-with-authority/
    look: "His first two tactics: never surprise your manager, and don't let your sponsor, the senior person backing your work, surprise you. For the second he suggests a weekly email, or a Slack thread with your focus for the week."
    trust: It's a chapter of his book *Staff Engineer*, by an engineering leader writing for staff engineers rather than PMs, so read it with your own role in mind.
    only: The case for updating upward as a habit, for people who lead without formal authority.
  - id: gopen-swan
    kind: read
    title: 'George Gopen and Judith Swan, "The Science of Scientific Writing"'
    minutes: 20
    where: An article. Free at human.libretexts.org, where you may need to click to open the article on the page. Read up to the end of the section "The Stress Position".
    links:
      - text: "The Science of Scientific Writing"
        url: https://human.libretexts.org/Bookshelves/Composition/Technical_Composition/Effective_Technical_Writing_in_the_Information_Age_(Schall)/10%3A_Journal_Articles_about_Writing/10.06%3A_The_Science_of_Scientific_Writing
    look: Why readers give the most weight to what comes at the end of a sentence, the stress position.
    trust: A journal article from American Scientist, reprinted with its permission in a Penn State textbook on technical writing. It's about scientific papers, but its point about readers holds for any prose.
    only: A reason, not just a rule, for why some sentences are hard to read.

check:
  - q: An update arrives on the day you promised it. Which part of the trust equation does that build?
    a: Reliability. It's a small promise kept, and a steady rhythm of them is what builds it.
  - q: Your update lists only wins. Which parts of the trust equation does it work against?
    a: Two. Self-orientation goes up, because it reads as being about you, and credibility goes down, because nobody believes nothing's wrong.
  - q: Your update opens with two paragraphs of background and asks for a decision in its last line. What would SCR change?
    a: It puts the ask in the opening, as the resolution, after one line the reader already accepts and one on what changed.

deeper:
  - title: The Trusted Advisor
    by: David Maister, Charles Green and Robert Galford
    where: A book.
    note: "Read the chapters \"The Trust Equation\" and \"The Development of Trust\"."
    trust: It's where the card's model comes from, written by three advisers to professional firms from their own practice. We found no peer-reviewed test of the equation.
    only: The trust equation from its authors, and the stages they see trust go through as it grows.
  - title: Influence Without Authority
    by: Allan Cohen and David Bradford
    where: A book.
    note: "Read the chapters on the influence model and its currencies of exchange, then \"Influencing Your Boss\"."
    trust: Two business school teachers, at Babson and Stanford, wrote it from their teaching and consulting, and it's reached a third edition. Expect cases and advice more than research.
    only: "Influence as exchange: work out what the other person values, the book's currencies, and offer it."
  - title: An Integrative Model of Organizational Trust
    by: Roger Mayer, James Davis and David Schoorman (Academy of Management Review, 1995)
    url: https://doi.org/10.2307/258792
    where: A journal article.
    trust: It's a peer-reviewed paper, and a research model to set beside the trust equation.
    only: Trustworthiness split into ability, benevolence and integrity, and trust defined as a willingness to be vulnerable to someone else's actions.
  - title: Ted Lasso
    by: "developed by Jason Sudeikis, Bill Lawrence, Brendan Hunt and Joe Kelly (Apple TV+, 2020), with *Succession*, created by Jesse Armstrong (HBO, 2018)"
    where: A pair of TV series.
    note: "Watch them side by side: *Ted Lasso*'s first season, and *Succession* through season 1, episode 6. In *Ted Lasso*, the owner who hired Ted to fail confesses it in episode 9, and he forgives her. In *Succession*'s episode 6, a son calls a board vote to oust his father, over the phone, and loses it: his father won't leave the room, and the people he counted on don't speak up."
    only: Trust earned and trust spent. Ted is predictable and plainly on everyone's side while his club keeps losing. In the Roy family every update is a maneuver, so nobody believes anyone, and the vote goes to whoever looks stronger in the room.
---

## Why this matters

People who decide about your work, or rely on it, can't see inside your team. Going quiet between milestones feels harmless, but that's when the guesses fill the space. If a hospital has planned its clinics around your scheduling release, the guesses tend to be worried ones.

Once you've found something, say it. You build trust by being clear when there's news and predictable when there isn't. Practitioners say the same about both, and what follows is my own way of thinking about it, though you'll see much the same advice in many places.

First, think about the milestones and outcomes you'd want to tell people about: when a new feature goes into testing, when it goes live, when the full release is ready, and when a date someone planned around moves. People outside your company, like customers or key partners, are likely the most interested in these, though they may come irregularly, with long gaps in between.

So second, think about a regular cadence of updates. Many businesses operate off of a business work week or month, though I try to anchor my communications to the sprint schedule of my teams. Whatever rhythm you pick, say what has happened and what will happen next. People inside it, like your peers and your management chain especially, want to be brought along, both to learn and to avoid surprises.

Credibility isn't handed out evenly, though. In a [2014 report on women in science](https://worklifelaw.org/publication/double-jeopardy-gender-bias-against-women-of-color-in-science/), about two thirds said they'd had to prove their competence again and again, and Black women said so most often. It's a survey of one association's members, not a peer-reviewed study, but it's one of the few that breaks the pattern down by race. So notice whose updates you take on trust, and whose you check.

[//]: # (short-path)

## Do

**Map your readers and send the first update (25 minutes).** List everyone who decides about your work or depends on it, and next to each name write a fixed day or a trigger, depending on whether they need your rhythm or only your news (10 minutes). Then write your first fixed-day update and send it to your most senior reader (15 minutes). Open it with {{< pm/term "scr" "SCR" >}}: the situation your reader already accepts, the complication that changed it, and the resolution you recommend. It's the variant I use of Barbara Minto's opening, which ends instead on the question the complication raises. For a late feed, it might read: "Every site's morning dashboard runs on the sensor feed. It's been late twice this week. Let's start the pilot on Thursday, once the retry is fixed." Keep the update to a few lines, include one item that isn't on track, and end its line on what you need, the {{< pm/term "stress-position" "stress position" >}} Gopen and Swan describe.

**Optional: one story at three sizes (15 minutes).** Turn that item into an ask of your manager. Write it as one sentence, then as an SCR paragraph of under 100 words, then as the outline of a one-page memo: the problem, two or three approaches, your recommendation and the open questions. Write each size fresh, with the ask in it. SCR puts the ask at the top of the message. Inside each sentence, end on what you most want noticed.
