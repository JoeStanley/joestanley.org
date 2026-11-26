---
title: Know Who It's For
layout: module
module: know-who-its-for
question: Whose problem is this, what's it worth to them, and how do you know?
setting: a grocery delivery app
one_thing: Ask about the last time it happened, not whether they'd want it.
do_minutes: 30
game: waiting

last_time:
  - q: Who does your "in order to" leave out?
    a: Someone your work touches but the sentence never names, like the musicians whose songs a streaming app plays. Read the sentence as them, and ask whether they'd want you to get there.
  - q: What does Rule Zero say about the job you were handed?
    a: That a rule can bend where following it would cost the table what it came for. So take the job as described first, and once you see the system around you, grow it toward value nobody assigned.

steps:
  - id: torres
    kind: read
    title: Teresa Torres, "Why You Are Asking the Wrong Customer Interview Questions"
    minutes: 10
    where: A blog post. Free at producttalk.org.
    links:
      - text: "Why You Are Asking the Wrong Customer Interview Questions"
        url: https://www.producttalk.org/customer-interview-questions/
    look: The two answers about jeans, and which one to build on.
    trust: "Experience. Torres coaches product teams on discovery for a living, and the post is built on one interview. It promotes her paid course, though it stands alone."
    only: How someone thinks they buy against how they bought, in one conversation you can copy.
  - id: milkshake
    kind: read
    title: Carmen Nobel, "Clay Christensen's Milkshake Marketing"
    minutes: 10
    where: An article. Free at library.hbs.edu.
    links:
      - text: "Clay Christensen's Milkshake Marketing"
        url: https://www.library.hbs.edu/working-knowledge/clay-christensens-milkshake-marketing
    look: "What watching the restaurant found that asking never did: 40 percent of the milkshakes went first thing in the morning, to commuters."
    trust: "Experience. It's Harvard Business School's own short account for managers, retelling a case from Christensen's research."
    only: What Christensen called the job a product is hired to do, in one memorable case.
  - id: card-last-time
    kind: card
    card: cards/the-last-time
    minutes: 5
    look: The two questions, what each brings back, and why the second shows you the price ceiling.
  - id: waiting
    kind: play
    title: Play the waiting game
    minutes: 10
    where: It's on this page, just below this list.
    look: Which estimate is worth testing while the team builds, and when each pick falls due.
example:
  body: |
    **The problem:** unwanted swaps.

    - **Tuesday evening.** Oat milk swapped for dairy. She poured it out and bought her own: $5, and 20 minutes by her account.
    - **Thursday.** Gluten-free bread swapped for regular. He can't eat gluten, so he took a refund and drove to the store: 45 minutes, a guess.
    - **Saturday.** A cheaper brand of diapers. She kept them, and now watches each swap as it's picked: a guessed 10 minutes an order.

    **A week of waiting:** support tags about 400 a week, at a guessed $5 each, time included. Roughly $2,000, before anyone who quietly leaves.

    **Decision log:** this quarter, ask before every swap. Expect unwanted-swap tickets to halve. 60 percent sure. Know a month after launch.
  good:
    - "Each line is one real time, with its day: what the person did, and what it cost them."
    - "Costs are in dollars or minutes, guesses say so, and the week's price is rough on purpose: close enough to set beside another problem's."
    - The call could turn out wrong, and the entry says how sure you are and when you'll know.

check:
  - q: A user says they'd pay $10 a month for a feature. What do you ask next, and why?
    a: "What they pay now, in money or time, for the workaround. As Teresa Torres puts it, \"What did you pay for that service?\" tells you more than any price for a service that doesn't exist yet."
  - q: A change drops the substitution questions from checkout, so it's faster, and has shoppers photograph each swap in the aisle for the customer to confirm. Who pays for the speed, and how would you find out?
    a: The shoppers, in time, and unpaid unless the pay model counts it. You'd find out from the shoppers themselves, not from the customers, who only see the faster checkout.
  - q: Own Your Role asked you to make the vision your own. Yours says customers want one thing, and three interviews in a row describe doing another. When does the vision win, and when do the interviews?
    against: own-your-role
    a: The interviews win on what the problem is, since they're evidence of what people did. The vision wins on where you're going, as long as its "in order to" still names a problem those people have. When it doesn't, rewrite the sentence.
  - q: "**Beyond this module.** This module shows you how to learn about a problem. What does judging it well take that no course can give you?"
    a: "Product sense: a working knowledge of your own product's domain, what it does and who uses it. You build it in your product, with its people and its data."

deeper:
  - title: The Mom Test
    by: Rob Fitzpatrick
    where: A book.
    note: "Read it whole: it's short. Chapter 1, \"The Mom Test,\" is the core, with questions such as \"Talk me through the last time that happened.\""
    trust: "Experience. It's a founder's handbook for other founders, and its site says it's taught at Harvard, UCL and Seedcamp."
    only: Questions even your mother couldn't lie to you about, and how to tell a compliment from a commitment.
  - title: Continuous Discovery Habits
    by: Teresa Torres
    where: A book.
    note: Read chapters 5 to 7, on interviewing every week, mapping what you hear and choosing which opportunity to work on.
    trust: "Experience. It's the method Torres teaches the product teams she coaches, set out step by step."
    only: A weekly habit of talking to customers, and her opportunity solution tree, which ties what you hear to the outcome you're after.
  - title: Monetizing Innovation
    by: Madhavan Ramanujam and Georg Tacke
    where: A book.
    note: "Read chapter 4, \"Have the 'Willingness-to-Pay' Talk Early: You Can't Prioritize without It,\" and chapter 5 if you want more."
    trust: "Experience. Both work at Simon-Kucher, a pricing consultancy, and the cases are named products, from Porsche to LinkedIn. Expect them to champion their firm's way of working."
    only: How to ask what a product is worth to its customers before anything is built.
  - title: Black Swan Farming using Cost of Delay
    by: Joshua Arnold and Özlem Yüce (2013)
    url: https://blackswanfarming.com/black-swan-farming-using-cost-of-delay/
    where: A paper.
    note: Free at blackswanfarming.com. Read it whole.
    trust: "Experience. It's the whole case, with its numbers, written by the two who ran the change."
    only: How Maersk Line put a price on waiting, one feature at a time, and what that changed about what it built first.
  - title: Silicon Valley
    by: created by Mike Judge, John Altschuler and Dave Krinsky (HBO, 2014 to 2019)
    where: A TV series.
    note: "Watch season 3, episode 9, \"Daily Active Users.\" Pied Piper celebrates half a million downloads while hardly anyone uses it each day. Its beta went to engineers and people like them. When ordinary users try it, they're lost, and Richard's answer is to explain more rather than listen. Then Jared quietly buys fake users from a click farm to cover the gap."
    only: Downloads mistaken for use, and the sample you listen to deciding what you hear.
---

## Why this matters

Own Your Role had you finish "We're building this in order to ...," a sentence that names someone the work is for. Does that person really have the problem, and what's it worth to them? Finding out is what teams call {{< pm/term "discovery" >}}. When enough people like them keep using and paying for what you build, you'll hear that called product-market fit.

Start with what people do, not what they say they'd want. People are poor forecasters of their own behavior and good witnesses to their last week. Ask a woman what matters most when she buys jeans and she'll say the fit, but her last pair came from Amazon, on sale, from a brand she knew. Ask an AI model to play your customer and you get a forecast too, with no last week behind it. Your data shows what people did, but not why. So ask about the last time it happened, what they did about it, and what it cost them. That cost caps what a fix is worth to them. And the people you hear from aren't a fair sample: your keenest users speak up, while the ones who left, or never came, are the ones you most need to hear.

Then ask whose problem it is. Say an adult child orders groceries for an aging parent: one person pays, another eats, and the app hears mostly from the one who pays. A gap like that pulls a team toward the buyer. On a platform team the gap is built in: your customer is another team, and the person with the problem is at the far end of its app.

An order has a third person in it, too: the shopper who picks it and brings it to the door. The price and the delivery window rest on their work, yet they're not the customer, so their side of the flow is easy to design without ever hearing from them. For restaurant delivery, New York City studied the apps' own records and [found](https://www.nyc.gov/assets/dca/downloads/pdf/workers/Delivery-Worker-Study-November-2022.pdf) that workers spent about two fifths of their working time waiting for the next offer, mostly unpaid. A large pool of waiting workers, the study said, helps an app promise short windows and keep pay per trip low. Grocery shoppers sent their own pay screenshots to [an MIT audit](https://dspace.mit.edu/handle/1721.1/147669) of one app, and more than a quarter of them had worked at least one shift below their state's minimum wage. Veena Dubal, a legal scholar who spent years with ride-hail drivers, [argues](https://columbialawreview.org/wp-content/uploads/2023/11/Dubal-On_Algorithmic_Wage_discrimination.pdf) that on-demand companies design their pay systems to keep that pool large and its pay low.

{{< pm/voice "shopper-incentive" "paragraph" >}}

AI makes some kinds of building cheap, which puts more of the job in knowing what's worth building. Google's [People + AI Guidebook](https://pair.withgoogle.com/chapter/user-needs/) asks first whether AI is the right tool at all: "Often a rule or heuristic-based solution will work just as well, if not better, than an AI version." Deciding where a model's judgment helps, and where a plain rule should stay in charge, is a product decision.

Value alone doesn't order the work, because waiting costs money too. What a fix is worth to each person, times how many hit the problem in a week, is roughly what a week without it costs: its {{< pm/term "cost-of-delay" "cost of delay" >}}. Once you price it, the urgent and the merely valuable stop looking alike.

[//]: # (short-path)

## Do

**Find the last time (30 minutes).** Pick one problem on your team's list. Read the last three support tickets, sales notes or session recordings where it shows up. For each, write when it happened, what the person did about it, and what it cost them in time or money. Tickets seldom say what it cost, so write your best guess and mark it as one. Then put a rough price on a week of waiting: how often the problem comes up in a week, times what it costs each time. On a platform team, trace one request to the experience it shows up in, and name the person at the end. Where your product depends on people you don't employ, such as a grocery app's shoppers, read their side too, in a support queue or a forum of their own.

Outside the 30 minutes, talk to two people who had the problem recently. Start with "Tell me about the last time ..." and keep them on that one time.

**Start a decision log.** Write down the call you'd make on this problem now, what you expect to happen, how sure you are as a percentage, and when you'll know. Keep the page: each module from here adds a line.

{{< pm/example >}}

## Questions to bring to designers and researchers

- What did people do about this the last time it happened, before our product did anything for them?
- Who didn't we hear from, and why?
- Whose work does this flow depend on, and have we watched them do it?
- What would we have to see to stop believing this problem matters?
