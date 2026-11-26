---
title: Bring People With You
layout: module
module: bring-people-with-you
question: How do you earn the trust of the people around you, and bring them along when they don't agree?
setting: a hospital's clinic scheduling software
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
    where: A podcast transcript. Free at lean.org. Read the section headed "How to Encourage Transparency and Information Sharing."
    links:
      - text: "People First Leadership"
        url: https://www.lean.org/the-lean-post/articles/people-first-leadership-a-conversation-between-jim-morgan-and-alan-mulally/
    look: What it said about Ford that all 300 status charts showed everything on track, at a company about to lose billions, and what Mulally, then its chief executive, did when Mark Fields showed the first one that didn't.
    trust: "Experience. It's Mulally telling his own story, years later, on the Lean Enterprise Institute's podcast: one man's memory of a moment he's proud of, so hold the details loosely."
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
    trust: "Experience. It's a chapter of his book *Staff Engineer*, by an engineering leader writing for staff engineers rather than PMs, so read it with your own role in mind."
    only: The case for updating upward as a habit, for people who lead without formal authority.
  - id: bezos-2016
    kind: read
    title: 'Jeff Bezos, "2016 Letter to Shareholders"'
    minutes: 5
    where: A shareholder letter. Free at aboutamazon.com. Read the section headed "High-Velocity Decision Making."
    links:
      - text: "2016 Letter to Shareholders"
        url: https://www.aboutamazon.com/news/company-news/2016-letter-to-shareholders
    look: "His third point, \"disagree and commit,\" and his fourth: escalate early when teams truly aren't aligned, or \"the default dispute resolution mechanism for this scenario is exhaustion.\""
    trust: "Experience. It's a chief executive on his own habit, a year after the letter you read in [Decide and Set Direction](/pm/decide-and-set-direction/)."
    only: What to do once the call is made and you still disagree, from someone who says the boss should do it too.
  - id: resnick
    kind: read
    title: 'Pete Resnick, "On Consensus and Humming in the IETF"'
    minutes: 10
    where: A guidance document, RFC 7282. Free at rfc-editor.org. Read section 2, "Lack of disagreement is more important than agreement."
    links:
      - text: "On Consensus and Humming in the IETF"
        url: https://www.rfc-editor.org/rfc/rfc7282.html
    look: "Why a chair who asks \"Can anyone not live with choice A?\" learns more than one who asks whether everyone's fine with it, and how to tell agreement from people who've given up."
    trust: "Experience. It's how the Internet Engineering Task Force, which sets many of the internet's technical standards, reaches decisions, written up by one of its members and published after public review."
    only: How peers decide with no boss to break the tie, and why a minority that says "Forget it, do what you want" hasn't agreed.
  - id: gopen-swan
    kind: read
    title: 'George Gopen and Judith Swan, "The Science of Scientific Writing"'
    minutes: 20
    where: An article. Free at human.libretexts.org, where you may need to click to open the article on the page. Read up to the end of the section "The Stress Position."
    links:
      - text: "The Science of Scientific Writing"
        url: https://human.libretexts.org/Bookshelves/Composition/Technical_Composition/Effective_Technical_Writing_in_the_Information_Age_(Schall)/10%3A_Journal_Articles_about_Writing/10.06%3A_The_Science_of_Scientific_Writing
    look: Why readers give the most weight to what comes at the end of a sentence, the stress position.
    trust: "An argument. American Scientist published it, and a Penn State textbook on technical writing reprints it with its permission. It's about scientific papers, but its point about readers holds for any prose."
    only: A reason, not just a rule, for why some sentences are hard to read.
  - id: do
    kind: do
    title: Map your readers, and send the first update
    where: The Do, on this page, below.
    look: One item that isn't on track, its line ending on what you need.
  - id: check
    kind: check
    title: Check yourself
    where: The Check, on this page, below.
    look: The answers you missed, and why you missed them.

example:
  body: |
    **Readers:**

    - Director of clinic operations, the sponsor: Mondays.
    - Manager and tech lead: the same note.
    - Twelve clinic managers: when a release changes their morning list.
    - Hospital IT: when the feed or a release date changes.

    **Monday, to the director:** "The waitlist is live at three clinics, as planned. Two more, neither in cardiology, asked to join early. Let's say yes: five clinics by May 15. The cardiology feed still drops overnight cancellations, so those slots stay empty. This week, can you get us an hour with IT's lead?"

    **Decision log:** expect the director to get IT's hour, not hold the two new clinics. 80 percent sure: she runs the clinics losing those slots. Know by Tuesday's reply.
  good:
    - The map gives Mondays to the people steering the work, and a trigger to those who only need its news.
    - It opens with the situation, the change and the call, and ends on the need, asked of the one person who can meet it.
    - The log line gives a reason for its 80 percent, which the director's reply will test.

check:
  - q: Decide and Set Direction says to give your view last when the call is yours, so it doesn't sway the room. SCR puts your recommendation in the opening lines. When does each hold?
    against: decide-and-set-direction
    a: SCR is for when someone else makes the call. They need your view from the first line, so they can weigh it. Speaking last is for when the call is yours, and you need the room's views more than its agreement.
  - q: Your update lists only wins. Which parts of the trust equation does it work against?
    a: Two. Self-orientation goes up, because it reads as being about you, and credibility goes down, because nobody believes nothing's wrong.
  - q: Your update opens with two paragraphs of background and asks for a decision in its last line. What would SCR change?
    a: It puts the ask in the opening, as the resolution, after one line the reader already accepts and one on what changed.
  - q: Your tech lead wanted the new booking screen to wait for a rewrite, and the call went the other way. What do you owe them, so they can disagree and commit?
    a: A real hearing before the call, their concern written into the decision record, and a date when you'll look again. Then committing isn't the same as giving up.
  - q: "**Beyond this module.** Whose trust will you need in a year that you haven't started to earn?"
    a: Someone your work will soon depend on, such as a team you'll need next year or a leader two levels up. Name one, and ask your manager how that person likes to hear news.

deeper:
  - title: The Trusted Advisor
    by: David Maister, Charles Green and Robert Galford
    where: A book.
    note: "Read the chapters \"The Trust Equation\" and \"The Development of Trust.\""
    trust: "Experience. It's where the card's model comes from, written by three advisers to professional firms from their own practice. There's no peer-reviewed test of the equation to point you to."
    only: The trust equation from its authors, and the stages they see trust go through as it grows.
  - title: Influence Without Authority
    by: Allan Cohen and David Bradford
    where: A book.
    note: "Read the chapters on the influence model and its currencies of exchange, then \"Influencing Your Boss.\""
    trust: "Experience. Two business school teachers, at Babson and Stanford, wrote it from their teaching and consulting, and it's reached a third edition."
    only: "Influence as exchange: work out what the other person values, the book's currencies, and offer it."
  - title: An Integrative Model of Organizational Trust
    by: Roger Mayer, James Davis and David Schoorman (Academy of Management Review, 1995)
    url: https://doi.org/10.2307/258792
    where: A journal article.
    trust: "An argument. It's a peer-reviewed paper, a research model of trust to set beside the trust equation."
    only: Trustworthiness split into ability, benevolence and integrity, and trust defined as a willingness to be vulnerable to someone else's actions.
  - title: Ted Lasso
    by: "developed by Jason Sudeikis, Bill Lawrence, Brendan Hunt and Joe Kelly (Apple TV+, 2020), with *Succession*, created by Jesse Armstrong (HBO, 2018)"
    where: A pair of TV series.
    note: "Watch them side by side: *Ted Lasso*'s first season, and *Succession* through season 1, episode 6. In *Ted Lasso*, the owner who hired Ted to fail confesses it in episode 9, and he forgives her. In *Succession*'s episode 6, a son calls a board vote to oust his father, over the phone, and loses it: his father won't leave the room, and the people he counted on don't speak up."
    only: Trust earned and trust spent. Ted is predictable and plainly on everyone's side while his club keeps losing. In the Roy family every update is a maneuver, so nobody believes anyone, and the vote goes to whoever looks stronger in the room.
---

## Why this matters

People who decide about your work, or rely on it, can't see inside your team. Going quiet between milestones feels harmless, but that's when the guesses fill the space. If a hospital has planned its clinics around your scheduling release, the guesses tend to be worried ones.

Once you've found something, say it. You build trust by being clear when there's news and predictable when there isn't. {{< pm/voice "own-way" >}}

Some news has a moment of its own: when a new feature goes into testing, when it goes live, when the full release is ready, and when a date someone planned around moves. People outside your company, like customers or key partners, care most about these, though they may come irregularly, with long gaps in between.

The rest goes out on a regular cadence. {{< pm/voice "cadence" >}}

Credibility isn't handed out evenly, though. In a [2014 report on women in science](https://worklifelaw.org/publication/double-jeopardy-gender-bias-against-women-of-color-in-science/), about two thirds said they'd had to prove their competence again and again, and Black women said so most often. It's a survey of one association's members, not a peer-reviewed study, but it's one of the few that breaks the pattern down by race. If you're the one asked to prove it again, the fault isn't in your work, and fixing it isn't yours alone. Meanwhile, this module's habits work harder for you: updates on the promised day, and a decision log anyone can check against what happened. Ask a sponsor, someone senior who backs your work, to say what they've seen you do in rooms you aren't in, and if you don't have one yet, ask your manager who could be. And when the update is someone else's, notice whose you take on trust and whose you check: it's [Weigh the Evidence](/pm/weigh-the-evidence/)'s question, asked of the people who bring the evidence.

Bringing people along is harder when they don't agree, and the people you most need are often peers with no reason to follow you: a tech lead, a designer, another team's PM. Disagreeing about the work isn't the danger. Pooling more than a hundred studies, Frank de Wit, Lindred Greer and Karen Jehn found that conflict about the task didn't clearly hurt how teams did, while conflict about each other, or about who does what, did ([2012](https://doi.org/10.1037/a0024844)). When a view makes no sense to you, get curious about why someone holds it, as Gary Klein advises. [Decide and Set Direction](/pm/decide-and-set-direction/)'s named decider settles who makes the call, not whether people come with it. Among peers, ask whether anyone can't live with a choice. That isn't a veto: every objection gets an answer, and the decider still decides. When the call goes against you, say so once, plainly, then commit. Jeff Bezos calls it "disagree and commit," and expects a boss to do it too. The one exception to committing is a line you drew in [Answer for What You Build](/pm/answer-for-what-you-build/): hold it, and take it outside the room if you have to.

[//]: # (short-path)

## Do

**Map your readers and send the first update (25 minutes).** List everyone who decides about your work or depends on it, and next to each name write a fixed day or a trigger, depending on whether they need your rhythm or only your news (10 minutes). Then write your first fixed-day update and send it to your most senior reader (15 minutes). Open it with {{< pm/term "scr" "SCR" >}}: the situation your reader already accepts, the complication that changed it, and the resolution you recommend. It's the variant I use of Barbara Minto's opening, which ends instead on the question the complication raises. For a late feed, it might read: "Every clinic's morning list comes from the scheduling feed. It's been late twice this week. Once the retry is fixed, let's start the pilot on Thursday." Keep the update to a few lines, include one item that isn't on track, and end that item's line on what you need, the {{< pm/term "stress-position" "stress position" >}} Gopen and Swan describe.

**For your decision log.** Write how you expect your senior reader to take the item that isn't on track, and how sure you are. You'll know by their reply.

{{< pm/example >}}

**Optional: argue the other side (15 minutes).** Pick a call where you and a peer, such as a tech lead or a designer, disagree. Write their case well enough that they'd sign it. Then write yours as an SCR paragraph of under 100 words. Last, write what would let you commit if the call goes their way, and the date you'd look again.
