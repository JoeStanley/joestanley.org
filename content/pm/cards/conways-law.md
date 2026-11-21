---
title: Conway's Law
layout: card
module: mind-the-seams
weight: 10
figure: conways-law
figure_caption: The line between the teams runs through the system, and the join is where work waits.
question: Where does a boundary between teams in your area cut through something a customer experiences as one thing?
deeper:
  title: "The Mirroring Hypothesis: Theory, Evidence, and Exceptions"
  by: Lyra Colfer and Carliss Baldwin (2016)
  url: https://dash.harvard.edu/bitstream/handle/1/33785675/colfer%2cbaldwin_mirroring-hypothesis.pdf
  where: A paper in Industrial and Corporate Change. Free at dash.harvard.edu.
  trust: It's peer-reviewed, and it weighs 142 studies, not one case.
  only: Where mirroring holds, where it breaks, and why.
---

## The idea

Organizations that design systems, Mel Conway argued in 1968, end up with designs that copy their own communication structures. The word that matters is communication: the system follows who actually talks to whom, and that isn't always what the org chart says. Ruth Malan's workshop notes put it in one line (February 2025, p. 314): "if the architecture of the system and the architecture of the organization are at odds, the architecture of the organization wins."

## Why a PM cares

- **Team boundaries become product boundaries.** Each handoff between teams tends to become an {{< pm/term "interface" >}}, and a place where work waits. Customers feel the join: a traveler books a flight in one flow, then starts over in another to add a bag.
- **Whoever designs the teams designs the architecture.** Malan again: "if we have managers deciding on teams, and deciding which services will be built, by which teams, we implicitly have managers deciding on the system architecture." Doing that on purpose, to get the system you want, is the {{< pm/term "inverse-conway" "inverse Conway maneuver" >}}.

## How to spot it

- A change touching three teams takes far longer than one touching one.
- The product has seams where the organization does: settings split across screens, APIs that follow department lines.

## What it does not say

It's a strong tendency, not a law of physics. Across 142 studies, Lyra Colfer and Carliss Baldwin found mirroring common, inside firms too, but not universal. Open, collaborative projects, mostly software, often broke it, helped by digital coordination tools.
