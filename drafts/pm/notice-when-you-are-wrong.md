## Why this matters

Every plan rests on assumptions, and some of yours are probably wrong today. You don't know which yet. This module is about finding them early, in your thinking and your team's.

## Short path (about an hour and a half of reading, plus half an hour for the exercises)

The deck is a 514-page set of workshop slide notes written for software architects, not a book, and you don't need most of it here. Read only the pages named, and only the parts named. Any term you don't know is defined under "Terms you will meet", below. If you split the path across two sittings, stop after step 3.

1. Deck p. 389 (5 minutes). Read the notes headed "Cognitive Biases" beneath the slide. Skip the slide and the references above the heading.
2. Deck pp. 395 and 396 (10 minutes), then Ed Batista, ["Racing Up the Ladder of Inference"](https://www.edbatista.com/2014/02/racing-up-the-ladder-of-inference.html) (2014), about 10 minutes. Free at edbatista.com. On p. 395, look at the ladder on the slide and read the notes headed "Moving Up (and Down) the Ladder of Inference". On p. 396, read the two notes headed "Left Column, Right Column" and "Espoused Theory vs Theory in Use". Skip the rest.
3. Deck pp. 400 to 403 (20 minutes). On p. 400, read the notes headed "We Need to Loop Back to That". On p. 401, read the slide. On p. 402, read the slide and the notes beneath it that begin "Put simply". On p. 403, read the definition on the slide and the notes headed "Safety Doesn't Mean 'Just Being Nice'". Skip the large side quotes on all four pages.
4. Deck p. 398 (5 minutes). Read the notes headed "Repairing Blindspots" beneath the slide. Skip the rest.
5. Deck pp. 455, 456 and 487 (12 minutes). On p. 455, read the three steps on the slide and the right-hand column of notes on quantifying and prioritizing risks. On p. 456, read the notes headed "Premortem". On p. 487, read the short note headed "Design Crit". Skip the rest.
6. Deck pp. 491, 493 and 496 (15 minutes), then Michael Nygard, ["Consequences are not Pros or Cons"](https://www.michaelnygard.com/blog/2020/06/consequences-are-not-pros-or-cons/) (2020), about 3 minutes. Free at michaelnygard.com. On p. 491, read the slide and the notes headed "Architecture Decisions". On p. 493, read the notes headed "RFC Template". On p. 496, read the notes headed "Writing Things Down". Skip the rest.

## Full path

- Kathryn Schulz, ["On being wrong"](https://www.ted.com/talks/kathryn_schulz_on_being_wrong) (TED2011), about 18 minutes. Free at ted.com.
- Gary Klein, "Performing a Project Premortem" (*Harvard Business Review*, September 2007), about 15 minutes. It's the source of the premortem on deck p. 456.
- Deck pp. 387, 390 to 394, 397, 404 to 411, 488, 489, 494, 495 and 497, on bias, error, design briefs and risk radars. About 90 minutes in all.

## Terms you will meet

- **Cognitive bias:** a predictable error in thinking that everyone makes, not a sign of carelessness.
- **Hindsight bias:** after something goes wrong, the feeling that you knew it all along.
- **Outcome bias:** judging a decision by how bad the result was, not by what was known when it was made.
- **Ladder of inference:** Chris Argyris's model of how we climb from what we observe, through the data we pick out, the meaning we add and the beliefs we form, to action, usually without noticing the steps.
- **Left-hand column:** an exercise from Argyris and Donald Schön. Beside what was said in a conversation, you write what you thought and felt but didn't say.
- **Espoused theory and theory-in-use:** what we say guides our behavior, and what actually does, as others can see from our actions.
- **Single-loop learning:** changing your actions to reach the same goal, like a thermostat switching the heat on and off.
- **Double-loop learning:** questioning the assumptions and goals behind the actions, not just the actions.
- **Psychological safety:** Amy Edmondson's term for a shared belief that it's safe to take interpersonal risks at work, such as raising a concern or admitting a mistake.
- **Risk storming:** Simon Brown's workshop technique. People mark risks on a diagram of the system alone and in silence, then compare and prioritize them together.
- **Premortem:** Gary Klein's technique of assuming a project has already failed and asking the team why.
- **Design crit:** short for design critique, a review that raises questions and concerns about work in progress without attacking the people doing it.
- **Architecture decision record (ADR):** a short note recording one decision and why you made it; see the decision record in Module 8, Decide and Set Direction.
- **Request for comment (RFC):** a document that describes a problem and a few possible solutions, shared for comment before anyone decides.

## What to look for

- **Your judgments feel like facts.** On p. 395, notice Argyris's point: we reach them so fast we treat them as concrete. Batista's post gives you a question for each rung, so you can climb back down to the data.
- **Bad outcomes rewrite history.** In Allspaw's list on p. 389, hindsight bias and outcome bias are the two to watch in any review. Listen for "they should have", and for blame that grows with the size of the damage.
- **Fixing the action is not fixing the goal.** Pages 401 and 402 contrast tuning the method with questioning the assumptions behind the goal. Retuning a streaming service's recommendations to lift watch time is the first; asking whether watch time keeps subscribers is the second.
- **Silence can become an organization's habit.** Argyris's 1977 example on p. 400 is a norm against challenging policies top management likes, and a second norm that nobody mentions the first. Edmondson's definition on p. 403 describes the opposite: people say what they see, and the bar stays high. For when to voice or hold back your own view, see the Curious and Opinionated card in Module 0, Own Your Role.
- **Assume it has already failed.** Klein's premortem on p. 456 asks what did go wrong, not what might, and that makes it safer for doubters to speak. Risk storming on p. 455 adds a second protection: everyone writes risks alone, in silence, before anyone discusses them.
- **Consequences before verdicts.** Nygard (p. 491 and his post) asks you to list how the future will differ before calling anything a pro or a con. Then ask what follows from each consequence.

## Apply it to your own work

1. Write a left-hand column, in about 15 minutes. Pick a recent meeting where you held back a concern, or where a decision went a way you doubted. Everyone has one. Follow the steps on deck p. 396: what was said goes in the right column, what you thought in the left. Then take one left-column thought down the ladder of inference: what did you actually see or hear, and what did you add? Rewrite it as one sentence you could have said, starting from the data.
2. Run a premortem on your own work, in about 15 minutes. Imagine it's a year from now and your main initiative has failed. Alone and in silence, as risk storming asks, write at least five plausible reasons why. Rate each one low, medium or high for how likely it is and how much damage it would do (p. 455). For the top one, name an early signal you could watch for in the next month. A first pass from what you already know is fine. To test it, ask a colleague who knows the work, or whoever would see it break first, such as an on-call engineer: "If this failed, what would you bet the reason was?"

## Check your own thinking

The shift this module is after is from "how do I show I am right?" to "how would I find out I am wrong?" Test yourself against it: of your next three plans or proposals, count how many name one way you could be wrong and an early signal you'd watch for. You're aiming for three out of three. If you'd like a sounding board, take your premortem list to your manager or a mentor.

Finding out is half the job. Saying what you found, so the people who decide can act on it, is the next module, Bring People With You.

> Deck page references are to Ruth Malan's System Design and Software Architecture workshop notes, February to March 2025 edition. This guide is an independent companion; it has not been reviewed or endorsed by Ruth Malan.

# Double-Loop Learning

## The idea

Chris Argyris called organizational learning "a process of detecting and correcting error." Single-loop learning corrects the error and keeps the goal, like a thermostat switching the heat on when the room gets cold. Double-loop learning questions the goal itself, and the norms and assumptions behind it. A double-loop thermostat would ask, "Why am I set at 68 degrees?"

His 1977 *Harvard Business Review* article tells of Product X, which lost more than $100 million. At least five people knew it was in trouble six years before it was dropped, but their memos were softened and cut on the way up. Argyris called the cause "norms embedded within norms": don't confront policies top management is excited about, and don't openly confront the rule that tells you so.

## Why a PM cares

- **Most of your feedback loops are single loop.** Retros, experiments and incident reviews tune the method and leave the goal alone. A claims team that keeps cutting days off insurance payouts may never ask whether speed is what claimants wanted. You're often the one placed to ask.
- **Bad news waits for a fix.** The people closest to Product X knew "bad news would not be well received at the upper levels if it was not accompanied by suggestions for positive action." If engineers and support tell you first, that's where the softening starts.
- **Successful people learn worst from failure.** Argyris found that when professionals' "single-loop learning strategies go wrong, they become defensive, screen out criticism, and put the 'blame' on anyone and everyone but themselves." Most of us do it. When a launch misses, check whether every reason you list sits outside your team.
- **Use his other tools.** The left-hand column and the ladder of inference, earlier in this module, help you find the assumption under a goal.

## How to spot it

- Every retro ends with a tweak to the process. None has asked "should we be doing this at all?"
- On a telecom network rollout, every slip brings a plan to speed up the crews, and nobody asks whether the coverage target still fits.
- The real reason a project is struggling gets said in the corridor after the meeting.

## What it does not say

It does not say single-loop learning is bad: Argyris argued that the capacity for double loop "does not inhibit single loop learning; indeed, it usually helps it." It doesn't mean reopening the goal every week. And an off-site where everyone levels with each other won't fix it for long. Of such workshops he wrote, "After a month or so back at home, the spirit seems to wane."

**One question to carry:** Which assumption behind your team's goal hasn't been questioned since it was set, and who would tell you if it were wrong?

## Go deeper

**[Teaching Smart People How to Learn](https://hbr.org/1991/05/teaching-smart-people-how-to-learn), Chris Argyris (1991)**

A *Harvard Business Review* article, about 30 minutes. Paywalled at hbr.org.

**Why trust it:** Argyris coined the terms. The article draws on his 15 years of studying management consultants: field cases from one profession, not controlled experiments.

**What you'll get:** A team meeting that goes wrong line by line, then rewritten so you can hear what questioning your own reasoning sounds like.

*To check: both articles are paywalled (the 1977 one is at hbr.org/1977/09/double-loop-learning-in-organizations). Their full text was readable in the page source on 20 November 2026, and the quotations were copied from it. Confirm them against the printed articles, and decide whether a card should point behind a paywall.*
