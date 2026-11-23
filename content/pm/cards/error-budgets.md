---
title: Error Budgets
layout: card
module: change-safely
weight: 10
figure: error-budget
figure_caption: Nearly all of the month is uptime. The thin slice the target leaves is the budget, and each incident eats into it.
question: How much failure would our customers accept for this service, and who agreed to that?
deeper:
  title: Example Error Budget Policy
  by: Google SRE Workbook (Appendix B)
  url: https://sre.google/workbook/error-budget-policy/
  where: An appendix, about 5 minutes. Free at sre.google.
  trust: "Experience. Google's site reliability engineers wrote it as a template: one company's policy, for an example game service, ready for you to adapt."
  only: What a team agrees to do once the budget is spent, and the exceptions, such as security fixes.
---

## The idea

No service is perfectly reliable, and chasing 100 percent costs a lot for a difference customers won't notice. So you agree on a reliability target, a {{< pm/term "slo" "service level objective (SLO)" >}} such as "up 99.9 percent of the time," and treat the gap below perfect as an {{< pm/term "error-budget" "error budget" >}}. While some is left, releases go ahead. Once it's spent, they slow or stop until reliability recovers. A written policy says ahead of time what "stop" means, and who can make an exception.

## Why a PM cares

- **How much failure customers will accept is a product question.** It turns on what they expect, what the service earns and what competitors offer. In Google's account, product management sets the target, with the reliability engineers, and the two teams agree the budget it leaves.
- **It puts a number on caution.** "We can't afford failures" becomes a figure you can spend. A 99.9 percent target over 30 days leaves about 43 minutes of downtime.

## How to spot it

- Arguments about reliability end in "it depends who you ask," not a number.
- Nobody can tell you your service's target, or who agreed to it.
- Releases freeze after every incident, however small, or never freeze at all.

## What it does not say

It doesn't say all failures are equal. As Google's chapter notes, a privacy leak is far worse than a brief display glitch. Some failures, such as a double charge on a card, don't belong in a budget at all: treat them as hard lines.
