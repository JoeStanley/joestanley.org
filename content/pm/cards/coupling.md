---
title: Coupling Is About a Change
layout: card
module: design-for-change
weight: 10
figure: coupling
figure_caption: A price change stays inside the plan catalog. A new kind of charge runs through both systems, so for that change they're coupled.
question: For the change you most expect next year, which teams would have to ship together?
deeper:
  title: Uncoupling
  by: Michael Nygard (2018)
  url: https://www.youtube.com/watch?v=EirOknZJvYc
  where: A talk, his SATURN 2018 keynote. Free on YouTube.
  trust: Nygard is a software architect and wrote Release It!, a book on building software that holds up in production. It's one practitioner's talk, not research.
  only: All five kinds of coupling, as he lays them out.
---

## The idea

"Are these two parts coupled?" has no useful answer until you name the change. In [a 2020 talk](https://www.youtube.com/watch?v=3gib0hKYjB0), Kent Beck put it this way: two parts are {{< pm/term "coupling" "coupled" >}} "with respect to a particular change" if changing one means changing the other. A phone company's plan catalog and billing system can be independent when a price changes, and welded together when a new kind of charge arrives.

Michael Nygard names five kinds, and two land on your roadmap: development coupling, where "changes in producer and consumer must be coordinated," so the part that provides something and the part that uses it ship together, and semantic coupling, where parts change together because they share a concept.

## Why a PM cares

- **You often know which changes are coming.** When an engineer says two systems are tightly coupled, ask: for which change? Then name the one you expect, such as new eligibility rules on a benefits service.
- **Development coupling goes on the plan.** Each change two teams must coordinate costs meetings, a joint release and waiting. Name it when you plan, or meet it in week six.

## How to spot it

- A small change needs two teams to release on the same day.
- The same two services change together, release after release.
- Two services that never call each other still change together, because both rely on the same idea of a delivery zone.

## What it does not say

It doesn't say coupling is bad: a checkout that isn't coupled to its prices can't charge anyone. Decoupling costs something too, so pay for it where the likely changes are.
