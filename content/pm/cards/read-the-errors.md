---
title: Read the Errors First
layout: card
module: change-safely
weight: 20
figure: read-the-errors
figure_caption: A sample of what a bot score held back and what it let through. Its mistakes fall into a few kinds, and the biggest or the costliest is what to test for first.
question: What does it get wrong, and which of those mistakes do we test for first?
deeper:
  title: A Field Guide to Rapidly Improving AI Products
  by: Hamel Husain (2025)
  url: https://hamel.dev/blog/posts/field-guide/
  where: An article. Free at hamel.dev. Read the introduction and section 1, on error analysis, about 5 minutes.
  trust: "Experience. Husain worked on machine learning at Airbnb and GitHub and has since helped more than 30 companies build AI products. He sells a course on this."
  only: The whole loop on one real case, with the numbers before and after.
---

## The idea

One accuracy figure tells you how often a model is wrong, not how. So before you trust one, read its mistakes. Sample the orders your bot score held back and those it let through, and mark its mistakes: whoever reviews held orders knows which were fans, and resold tickets show which bots got past. Sort the mistakes into kinds and count them. That's {{< pm/term "error-analysis" "error analysis" >}}, and it comes before you choose a test: "grading outputs helps users define criteria" ([Shankar and colleagues, 2024](https://arxiv.org/abs/2404.12272)).

Then test for the biggest or the costliest kind: keep the orders it got wrong, with the right answers, and check that every change still gets them right. Teams call these tests evals. Last, change one thing, such as the cutoff at which it holds an order, and test the same examples again.

## Why a PM cares

- **Which mistake costs more is a product call.** A fan held back during a big on-sale and a bot let through cost different people different things. Weigh them equally, and you've made that call without noticing.
- **One number hides who it fails.** As with a guardrail, a model can look fine overall and still hold back every fan who buys for a group.

## How to spot it

- "It's 95 percent accurate," and nobody has read the other 5 percent.
- A new version shipped because it looked better on a few tries.

## What it does not say

It doesn't say a passing test makes a model safe: tests cover only the mistakes you've seen. A sepsis score used at hundreds of US hospitals missed two in three cases at one health system, far worse than its maker reported ([Wong and colleagues, 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8218233/)).
