# Tour Manager AI Agent

A conversational AI assistant that helps a touring tour manager run a show day. Ask it about weather or currency in plain language, and it decides on its own which tools to call, chains them when needed, and answers like a real assistant.

Built to demonstrate the core of agentic AI: an agent that reasons, makes decisions, and takes action, not just a chatbot that talks.

Try it out : more add ins comming soon https://fictional-space-enigma-9jj496jp5h79p6-5000.app.github.dev/
---

## What it does

You talk to it the way you'd talk to a real assistant. It figures out the rest.

A tour manager juggles a hundred moving pieces on the road: show-day weather, crew per diems, catering buyouts in foreign currency, settlement at the end of the night. This agent handles the questions that come up constantly, instantly, in plain English.

The magic is that **you don't tell it which tool to use.** It reads your question, decides what it needs, and acts.

```
You: We're in Osaka for load-in. What's the weather, and how much is
     the 18000 JPY catering buyout in USD?

   [Claude is using get_weather with Osaka]
   [Claude is using convert_currency with 18000 JPY to USD]

Tour Manager: Here's the rundown for Osaka:
  Weather: 21.1 C with very light winds, great conditions for load-in.
  Catering Buyout: 18,000 JPY comes out to 111.42 USD.
```

One sentence. Two different tools. One clean answer. The agent decided all of it.

---

## Features

- **Live weather** for any city, for show-day and travel planning.
- **Currency conversion** at live exchange rates, for per diems, crew buyouts, and settlement.
- **Smart tool selection.** It picks the right tool for each question, or chains several at once.
- **Conversation memory.** Follow-ups like "what about Tokyo?" still make sense.
- **Natural chat.** You ask in plain language, it answers like a person.

---

## How it works

The heart of the project is the **agent loop**, the cycle that turns a chatbot into something that can actually do things.

1. You ask a question.
2. The AI looks at the tools it has and decides whether it needs one.
3. If yes, it requests a tool with the exact details, like a city or an amount.
4. The tool runs and hands back a real result, live weather or a live exchange rate.
5. The AI reads that result, then either reaches for another tool or writes the final answer.

This decide, act, read, decide cycle repeats until it has everything it needs.

```
Your question
      |
      v
  AI decides  ---- needs info ----> Uses a tool ----+
      |                                             |
      | has everything                       (result loops back)
      v                                             |
  Final answer  <-------------------------------- +
```

---

## Tech stack

- **Python** for the agent and tools.
- **Anthropic API** as the reasoning engine, built raw with no framework so the decision-making is fully visible.
- **Open-Meteo** for live weather data.
- **Frankfurter** for live currency exchange rates.

---

## Examples of how it works

```
What's the weather in Playa del Carmen?

How much is 100 USD in MXN?

Convert 500 euros to pesos.

What's the weather in Tokyo and how much is 20000 yen in USD?
```

Each one is answered live. Weather questions pull real forecasts. Money questions pull real rates. Mixed questions trigger both tools in a single turn.

---

## Project structure

```
tour-manager-agent/
  tour_manager.py   the agent loop and conversation interface
  tools.py          the tools: get_weather and convert_currency
  README.md         this file
```

The design is deliberately simple. The agent loop lives in one place, the tools in another. Adding a new capability means adding one new tool, the loop never changes.

---

## What I learned

This project taught me how agentic AI works under the hood, with no framework hiding the mechanics:

- How an agent loop turns a chatbot into something that can take action.
- How tool calling lets an AI choose and use external functions on its own.
- How to write tool descriptions clear enough that the AI picks the right one.
- How to manage conversation state so the assistant remembers context.
- How to keep secrets like API keys secure and out of a public repository.

---

## Roadmap

Planned additions, framed around the real tour manager workflow:

- **Day sheet tool.** Track load-in, soundcheck, doors, and curfew, timezone-aware.
- **Settlement tool.** Nightly box office math, taxes and fees out, net payout.
- **Web interface.** A simple dashboard so it can be used outside the terminal.
- **More integrations.** Flights, hotels, and crew logistics over time.

---

Built as a hands-on project to learn agentic AI from the ground up, and as the first step toward a real tour management product.# CodeCademy-TourManager
