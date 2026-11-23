---
title: Goodhart's Law
layout: card
module: find-the-constraint
weight: 20
figure: goodhart
figure_caption: Before a number is a target, it moves with the thing you care about. Afterwards the number can keep climbing on its own.
question: If people hit this number in the cheapest way open to them, would the customer still be better off?
deeper:
  title: Categorizing Variants of Goodhart's Law
  by: David Manheim and Scott Garrabrant (2018)
  url: https://arxiv.org/abs/1803.04585
  where: A research paper. Free at arxiv.org.
  trust: "An argument. It's a research preprint, so treat it as careful, not settled."
  only: It separates the different ways a measure can fail, so you can tell which one you're looking at.
---

## The idea

Once people are judged by a number, they adapt to it, and it stops telling you what it used to. The economist Charles Goodhart made the point in 1975, about UK monetary policy. The well-known wording, "When a measure becomes a target, it ceases to be a good measure," is the anthropologist Marilyn Strathern's, from 1997.

## Why a PM cares

- **A target changes behavior before it changes results.** Tell a delivery team to raise its on-time rate, and it can start promising later dates. The number improves while parcels arrive no sooner.
- **{{< pm/term "okr" >}} make gaming easy.** A key result often ends in a bare number, and a bare number invites the cheapest way to reach it. When you write one, put the intent beside the number.
- **Local targets hide the constraint.** A target on one step, such as reviews completed per day, can lift that step's number while the whole flow stays slow.

## How to spot it

- A number jumps soon after it becomes a target, while complaints, rework or escalations don't improve.
- People can tell you how to hit the number, but not what it was meant to show.
- Definitions drift. What counts as "resolved" or "on time" quietly narrows or loosens.

## What it does not say

It does not say measures are bad, or that every target fails. The usual remedy is more than one measure. Pair each number with one that would show the cheap way of hitting it: the on-time rate with how far out the promised date was, say.
