---
title: Conway's Law
layout: card
module: mind-the-seams
weight: 10
figure_quote:
  text: "The basic thesis of this article is that organizations which design systems (in the broad sense used here) are constrained to produce designs which are copies of the communication structures of these organizations."
  by: Melvin Conway
  work: How Do Committees Invent?
  url: https://www.melconway.com/Home/Committees_Paper.html
  year: 1968
question: Where does a boundary between teams in your area cut through something a customer experiences as one thing?
deeper:
  title: "The Mirroring Hypothesis: Theory, Evidence, and Exceptions"
  by: Lyra Colfer and Carliss Baldwin (2016)
  url: https://dash.harvard.edu/bitstream/handle/1/33785675/colfer%2cbaldwin_mirroring-hypothesis.pdf
  where: A paper in Industrial and Corporate Change. Free at dash.harvard.edu.
  trust: "A review of studies. It's peer-reviewed, and it analyzes more than a hundred."
  only: Where mirroring holds, where it breaks, and why.
---

## The idea

The word in Conway's sentence that matters is communication: the system follows who actually talks to whom, and that isn't always what the org chart says. The software architect Ruth Malan puts it in one line: "if the architecture of the system and the architecture of the organization are at odds, the architecture of the organization wins" (unpublished workshop notes, February 2025).

## Why a PM cares

- **Team boundaries become product boundaries.** Each handoff between teams tends to become an {{< pm/term "interface" >}}, and a place where work waits. Customers feel the join: a traveler books a flight in one flow, then starts over in another to add a bag.
- **Whoever designs the teams designs the architecture.** Malan again: "if we have managers deciding on teams, and deciding which services will be built, by which teams, we implicitly have managers deciding on the system architecture." Doing that on purpose, to get the system you want, is the {{< pm/term "inverse-conway" "inverse Conway maneuver" >}}. If you don't draw the teams, sketch the system you want and show it to whoever does.

## How to spot it

- A change that touches three teams takes far longer than one that stays inside a team.
- The product has seams where the organization does: settings split across screens, APIs that follow department lines.

## What it does not say

It's a strong tendency, not a law of physics. Over more than a hundred studies, Lyra Colfer and Carliss Baldwin found mirroring common, across industries and inside firms, but not universal. Open, collaborative projects, mostly software, often broke it, helped by digital coordination tools.
