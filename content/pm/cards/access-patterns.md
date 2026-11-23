---
title: Access Patterns
layout: card
module: design-for-change
weight: 20
figure: access-patterns
figure_caption: Every question reaches the same data, each with its own need for freshness, and the freshest answers cost the most to keep.
question: Who will ask this, how fast do they need the answer, and what would break if it were a day old?
deeper:
  title: "The world beyond batch: Streaming 101"
  by: Tyler Akidau (2015)
  url: https://www.oreilly.com/radar/the-world-beyond-batch-streaming-101/
  where: An article. Free at oreilly.com. Read through "Event time vs. processing time," about 15 minutes.
  trust: "Experience. Akidau was working on Google's large-scale streaming systems when he wrote it."
  only: The words engineers use about batch and streaming, and why late data is the hard part.
---

## The idea

An {{< pm/term "access-pattern" >}} is a question the data has to answer, and how it's asked: who asks, how often, how fast and how fresh. [AWS's guide to its DynamoDB database](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-general-nosql-design.html) says not to design the data's layout until you know those questions. Not every database is that strict, but every design makes some questions cheap and others expensive.

## Why a PM cares

- **The questions are product knowledge.** On an insurance claims product, you know what the claimant, the adjuster and finance will ask, and how soon.
- **Freshness has a price.** Fresher copies take more machinery to keep up, so before you ask for "real time," ask what decision the answer feeds.
- **Late data forces a choice.** {{< pm/term "event-time" "Event time" >}} is when something happened, and processing time is when the system saw it. A sensor reading taken on Friday arrives on Monday, and someone has to decide which day it counts for.

## How to spot it

- A request says "real time" but not for whom, or for which decision.
- Two screens show different numbers for the same thing, because they read copies of different ages.
- A question is fast one way and slow the other. Listing one player's matches is quick, and finding every player who used one item may not be.

## What it does not say

It doesn't say you must list every question before you build. Needs change, and some designs adjust more easily than others.
