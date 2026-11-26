---
title: An API Is a Promise
layout: card
module: map-the-domain
weight: 20
figure: api-promise
figure_caption: Callers count on what an API documents and on what it happens to do, and changing either can break them.
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

An API is a promise to the teams that call it, and so is a dataset other teams read. Hyrum Wright, then an engineer at Google, put it as a law: "With a sufficient number of users of an API, it does not matter what you promise in the contract: all observable behaviors of your system will be depended on by somebody." That's {{< pm/term "hyrums-law" "Hyrum's Law" >}}. A farm app may count on a weather API's hourly readings coming back in order, though nobody promised they would.

## Why a PM cares

- **Its customers are other teams.** They feel how long it keeps working, and how soon a first call works, which [GOV.UK's API guidance](https://www.gov.uk/guidance/defining-an-api-management-strategy) calls "time to 200," after the web's code for success.
- **Retiring a version is a product decision.** Keeping an old version costs your team, and forcing an early move costs callers. A {{< pm/term "deprecation" >}} with no date and nobody to help callers move rarely finishes. As Google's engineers put it, "Hope is not a strategy."
- **Count, then ask.** Your docs won't tell you what callers depend on. Count calls by version, then ask the teams behind them. If the date isn't your call, bring both answers to whoever owns the API.

## How to spot it

- A field renamed in a "small cleanup," or inches changed to millimeters.
- A caller counting on an order or a time zone nobody promised: "today" in UTC isn't today on a farm in Iowa.
- Nobody can retire a version, because nobody knows who still calls it.

## What it does not say

It doesn't say you can't change an API. Add the new field, move callers to it and remove the old one last, or publish a new version, and say which you'll take and when. Careful teams differ: GOV.UK puts a version in the address, and Zalando, an online retailer, avoids versions where it can.
