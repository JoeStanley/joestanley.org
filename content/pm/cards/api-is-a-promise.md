---
title: An API Is a Promise
layout: card
module: map-the-domain
weight: 20
figure: api-promise
figure_caption: Callers build on what an API documents and on what it happens to do. A change to the second can break them as surely as a change to the first.
question: Who calls this, and what are they counting on that we never wrote down?
deeper:
  title: Deprecation
  by: Hyrum Wright, in Software Engineering at Google (2020)
  url: https://abseil.io/resources/swe-book/html/ch15.html
  where: A chapter of a book. Free at abseil.io. Read "Why Is Deprecation So Hard?" and "Types of Deprecation," about 10 minutes.
  trust: "Experience. Wright, the engineer the law above is named for, on what retiring old systems taught Google."
  only: Why switching something off is harder than building it, and why a deprecation with no deadline and no team behind it stalls.
---

## The idea

An API is a promise to the teams that call it, and so is a dataset other teams read. They build on what it does, not only on what you wrote down. Hyrum Wright, then an engineer at Google, put it as a law: "With a sufficient number of users of an API, it does not matter what you promise in the contract: all observable behaviors of your system will be depended on by somebody." That's {{< pm/term "hyrums-law" "Hyrum's Law" >}}. A farm app may count on a weather API's hourly readings coming back in order, though nobody promised they would.

## Why a PM cares

- **Its customers are other teams.** Their experience is how fast they make a first call that works, and how long they can trust it not to break. [GOV.UK's API guidance](https://www.gov.uk/guidance/defining-an-api-management-strategy) calls the first "time to 200," after the code for a call that worked, a measure of how easy an API is to start with.
- **Retiring a version is a product decision.** Each month an old version stays costs your team, and each month you make callers move before they planned costs them. A {{< pm/term "deprecation" >}} with no date and nobody assigned to help callers move rarely finishes. As Google's engineers put it, "Hope is not a strategy."
- **Ask before you set a date.** Your docs won't tell you what callers depend on. Count calls by version first, then ask the teams behind them. If the date isn't your call, bring the count and what they told you to whoever owns the API.

## How to spot it

- A field renamed in a "small cleanup," or a unit changed from inches to millimeters.
- A caller counting on an order, a default or a time zone nobody promised: "today" in UTC isn't today on a farm in Iowa.
- A version nobody can retire, because nobody knows who still calls it.

## What it does not say

It doesn't say you can never change it. Add the new field first, move callers to it and remove the old one last, or publish a new version. Every path costs callers something, so say which you'll take and when. Careful teams differ: GOV.UK puts a version in the address, Stripe, in 2017, pinned each account to the version it started on, and Zalando, an online retailer, avoids versions where it can.
