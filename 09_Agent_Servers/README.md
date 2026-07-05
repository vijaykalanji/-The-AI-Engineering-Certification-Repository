<p align="center" draggable="false"><img src="https://github.com/AI-Maker-Space/LLM-Dev-101/assets/37101144/d1343317-fa2f-41e1-8af1-1dbb18399719"
     width="200px"
     height="auto"/>
</p>

<h1 align="center" id="heading">Session 9: Agent Servers</h1>

### [Quicklinks]()

| Session Sheet | Recording | Slides | Repo | Homework | Feedback |
|:--------------|:----------|:-------|:-----|:---------|:---------|
| [Session 9: Agent Servers & E2E Agents](https://github.com/AI-Maker-Space/The-AI-Engineering-Certification-v1.0/tree/main/00_Docs/Modules/09_Agent_servers_%26_E2E_Agents) |[Recording!](https://us02web.zoom.us/rec/share/ByhPGNz-CQ4C9k859VnRIoGPfkS4AdBzLPQiCIgEafYiDjYxtNXUjidTI1dM-79R.oCxzwNn0SyVAWj88) <br> passcode: `r14dvS$V`| [Session 9 Slides](https://canva.link/yqymnzjmzhpnyiy) | You are here! | [Session 9 Assignment](https://forms.gle/PMmqBBLZ8d8fGg1L8) | [Feedback 7/1](https://forms.gle/36tnHPpeS562DD3fA) |

## Useful Resources

**LangSmith Deployment & Studio**
- [LangSmith Deployment docs](https://docs.langchain.com/langsmith/deployments) — Deploy, manage, and monitor agent APIs
- [LangGraph Studio](https://docs.langchain.com/langgraph-platform/langgraph-studio) — Visualize, debug, and test agents locally and in production
- [Agent Server API](https://docs.langchain.com/langsmith/agent-server) — Threads, runs, assistants, and streaming
- [You don't know what your agent will do until it's in production](https://blog.langchain.com/you-dont-know-what-your-agent-will-do-until-its-in-production/)

**Frontend Integration**
- [`@langchain/react` — `useStream` hook](https://www.npmjs.com/package/@langchain/react) — Stream agent responses in React/Next.js
- [`langgraph-nextjs-api-passthrough`](https://www.npmjs.com/package/langgraph-nextjs-api-passthrough) — Secure Next.js API routes that proxy to your deployed agent without exposing keys in the browser
- [Next.js on Vercel](https://vercel.com/docs/frameworks/nextjs) — Deploy the frontend

## What You Are Building

In earlier sessions, you built LangGraph agents in notebooks. In this session, you take that agent to production in two parts:

1. **Deploy the agent** as an API backend on LangSmith (via LangGraph Studio and `langgraph deploy`)
2. **Build a website** that talks to that agent, then **deploy the site on Vercel**

```mermaid
flowchart LR
  User[User in browser] --> Vercel[Next.js frontend on Vercel]
  Vercel -->|"/api proxy route"| LangSmith[LangSmith Agent API]
  LangSmith --> Agent[Your LangGraph agent]
  Agent --> Tools[Tools + RAG + memory]
  LangSmith --> Traces[LangSmith tracing & evals]
```

> **Important:** LangSmith deploys your agent as an **API backend only**. It does not serve a frontend. Vercel hosts the UI; LangSmith hosts the agent.

## Main Assignment

You will package a LangGraph agent into a production-ready Python project, test it in **LangGraph Studio**, deploy it to **LangSmith**, then build a **Next.js chat UI** that streams responses from your deployed agent and ship that UI to **Vercel**.

Expected agent project layout:

```text
09_Agent_Servers/
├── langgraph.json          # Manifest — how LangGraph discovers your graphs
├── app/
│   ├── state.py            # Shared state schema
│   ├── models.py           # Model factory
│   ├── tools.py            # Tool belt
│   ├── rag.py              # Optional RAG pipeline
│   └── graphs/
│       └── simple_agent.py
├── data/
│   └── cat-health-guide.pdf
└── frontend/               # Next.js app (you create this)
    └── app/
        ├── page.tsx
        └── api/[...path]/route.ts
```

## Prerequisites

In addition to tools from earlier sessions, you will need:

1. A [LangSmith](https://smith.langchain.com/) account
2. **Docker** installed locally (needed for `langgraph up` and some deploy paths)
3. Your agent code pushed to a **GitHub** repository (needed for LangSmith cloud deploys)
4. A [Vercel](https://vercel.com/) account
5. *(Optional)* **LangSmith Plus** (~$40/month) for one-click cloud deploys via `langgraph deploy`

## Quick Command Reference

Two servers run **locally** (the agent API and the frontend), and two things deploy **online** (the agent to LangSmith, the frontend to Vercel). Run commands from `09_Agent_Servers/` unless noted. The detailed walkthrough for each step is in Parts 1–4 below.

### Run locally

**1. Agent server (LangGraph) — terminal 1**

```bash
uv sync                            # install Python deps (first time only)
cp .env.example .env               # then fill in OPENAI_API_KEY and TAVILY_API_KEY
uv run langgraph dev               # API at http://localhost:2024 + opens LangGraph Studio
```

**2. Frontend (Next.js) — terminal 2**

```bash
cd frontend
npm install                        # install JS deps (first time only)
cp .env.local.example .env.local   # defaults already point at http://localhost:2024
npm run dev                        # chat UI at http://localhost:3000
```

Open `http://localhost:3000` and chat. The browser hits the Next.js `/api` proxy, which forwards to your local agent server.

### Deploy online

**3. Agent → LangSmith** (push your repo to GitHub first; run from `09_Agent_Servers/`)

```bash
uv run langgraph deploy            # LangSmith cloud build + host (requires LangSmith Plus)
# or self-host in Docker on your own VPS instead:
uv run langgraph up
```

Then copy the **Deployment URL** and **LangSmith API key** from the LangSmith Deployments tab.

**4. Frontend → Vercel** (run from `frontend/`)

```bash
npm install -g vercel              # install the Vercel CLI (first time only)
cd frontend
vercel                             # first run links/creates the project (preview deploy)
vercel --prod                      # production deploy
```

Set these in the Vercel project (Settings → Environment Variables, or `vercel env add`), then run `vercel --prod` again:

```text
LANGGRAPH_API_URL=https://your-deployment.us.langgraph.app
LANGSMITH_API_KEY=lsv2_pt_...
NEXT_PUBLIC_API_URL=https://your-app.vercel.app/api
```

## Setup

From this folder, install the agent environment:

```bash
uv sync
```

Copy the example env file and fill in your keys:

```bash
cp .env.example .env
```

Typical variables:

```text
OPENAI_API_KEY=
TAVILY_API_KEY=
LANGSMITH_API_KEY=
LANGSMITH_TRACING=true
```

## Part 1: Run Locally and Use LangGraph Studio

Package your agent so it can be served as an API — not as a notebook cell.

### 1. Define your graphs in `langgraph.json`

Register each compiled graph and the assistants you want to expose:

```json
{
  "dependencies": ["."],
  "env": ".env",
  "graphs": {
    "simple_agent": "app.graphs.simple_agent:graph"
  },
  "assistants": {
    "agent": {
      "graph_id": "simple_agent",
      "name": "Simple Agent",
      "description": "Agent with tools using conditional tool-calling."
    }
  }
}
```

Each graph file should export a compiled graph named `graph`.

### 2. Start the local agent server

```bash
uv run langgraph dev
```

This starts the agent API at `http://localhost:2024` and opens **LangGraph Studio** in your browser (Chromium-based browsers work best).

### 3. Explore and debug in Studio

Use Studio to:

- Visualize graph topology — nodes, edges, and conditional branches
- Step through execution and inspect tool calls and results
- Fork conversations to test alternate paths
- Switch between assistants defined in `langgraph.json`

Studio and the SDK stream the same events. Studio is for debugging; the SDK (and your frontend) is for production integration.

### 4. Smoke-test with the SDK

```python
from langgraph_sdk import get_client

client = get_client(url="http://localhost:2024")

for chunk in client.runs.stream(
    None,
    "agent",
    input={"messages": [{"role": "human", "content": "How often should I deworm my cat?"}]},
    stream_mode="updates",
):
    print(chunk)
```

If this works locally, you are ready to deploy.

## Part 2: Deploy the Agent on LangSmith

Push your agent repo to GitHub, then deploy.

### Option A: LangSmith cloud deploy (recommended for this session)

```bash
uv run langgraph deploy
```

Requires LangSmith Plus. LangSmith builds and hosts the agent API for you. After deploy, copy your **Deployment URL** and **LangSmith API key** from the LangSmith Deployments tab — you will need both for the frontend.

Enable **auto-update on push** so every commit to your main branch triggers a redeploy.

### Option B: Self-hosted with Docker

```bash
uv run langgraph up
```

Runs a production-ready container you can host on any VPS. You manage scaling, uptime, and auth yourself.

### What you get

A hosted API endpoint with standard routes for threads, runs, and assistants. Your agent runs behind that API; LangSmith traces and monitors execution.

## Part 3: Build a Website That Uses Your Agent

Create a Next.js frontend that streams chat responses from your deployed agent.

### Recommended architecture

Never put `LANGSMITH_API_KEY` in client-side code. Use a **Next.js API route** as a secure proxy:

```text
Browser  →  /api/* on Vercel  →  LangSmith Deployment URL
              (injects API key server-side)
```

### 1. Scaffold the frontend

From this folder:

```bash
npx create-next-app@latest frontend
cd frontend
npm install @langchain/react langgraph-nextjs-api-passthrough
```

### 2. Add the API passthrough route

Create `frontend/app/api/[...path]/route.ts`:

```typescript
import { initApiPassthrough } from "langgraph-nextjs-api-passthrough";

export const { GET, POST, PUT, PATCH, DELETE, OPTIONS, runtime } =
  initApiPassthrough({
    apiUrl: process.env.LANGGRAPH_API_URL,
    apiKey: process.env.LANGSMITH_API_KEY,
    runtime: "edge",
  });
```

### 3. Build the chat UI with `useStream`

In a client component (e.g. `frontend/app/page.tsx`), connect to your local proxy or deployed passthrough:

```typescript
"use client";

import { useStream } from "@langchain/react";

export default function ChatPage() {
  const { messages, submit, isLoading } = useStream({
    apiUrl: process.env.NEXT_PUBLIC_API_URL ?? "/api",
    assistantId: "agent",
  });

  // Render messages and a form that calls submit({ messages: [...] })
}
```

Use the `assistantId` that matches your `langgraph.json` assistants block.

### 4. Test locally

In `frontend/.env.local`:

```text
# Point at your local agent server (uv run langgraph dev):
LANGGRAPH_API_URL=http://localhost:2024
LANGSMITH_API_KEY=

# ...or point at your deployed LangSmith agent instead:
# LANGGRAPH_API_URL=https://your-deployment.us.langgraph.app
# LANGSMITH_API_KEY=lsv2_pt_...

NEXT_PUBLIC_API_URL=http://localhost:3000/api
```

Install deps (first time) and run the frontend:

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000`, send a message, and confirm you see streamed responses from your LangSmith deployment.

## Part 4: Deploy the Frontend on Vercel

### 1. Push the frontend to GitHub

Commit the `frontend/` directory (either in the same repo as your agent or a separate repo).

### 2. Import the project in Vercel

1. Go to [vercel.com/new](https://vercel.com/new) and import your repository
2. Set the **Root Directory** to `frontend` if the Next.js app is not at the repo root
3. Add environment variables in the Vercel project settings:

```text
LANGGRAPH_API_URL=https://your-deployment.us.langgraph.app
LANGSMITH_API_KEY=lsv2_pt_...
NEXT_PUBLIC_API_URL=https://your-app.vercel.app/api
```

4. Deploy

### 3. Verify end-to-end

Visit your Vercel URL, send a chat message, and confirm:

- The UI streams agent responses
- Tool calls work against your deployed agent
- Traces appear in LangSmith for each run

## Outline

### Breakout Room #1: Agent Packaging & LangGraph Studio

- Restructure a notebook agent into a Python package (`app/`, `langgraph.json`)
- Run `langgraph dev` and explore the agent in LangGraph Studio
- Test with the LangGraph SDK locally

### Breakout Room #2: Deploy Agent + Build & Ship Frontend

- Deploy the agent to LangSmith with `langgraph deploy`
- Scaffold a Next.js chat UI with `useStream`
- Add a secure API passthrough route
- Deploy the frontend to Vercel and connect it to your LangSmith deployment

## Ship

A deployed agent on LangSmith **and** a live website on Vercel that uses it.

### Deliverables

- A short Loom of either:
  - LangGraph Studio debugging your agent, then your Vercel site chatting with the deployed agent; or
  - your Advanced Activity below

## Share

Make a social media post about shipping your first production agent + frontend!

### Deliverables

- Make a post on any social media platform about what you built!

Here's a template to get you started:

```
🚀 Exciting News! 🚀

I just deployed a LangGraph agent to LangSmith and built a website on Vercel that streams responses from it! 🎉🤖

🔍 Three Key Takeaways:
1️⃣
2️⃣
3️⃣

Let's continue pushing the boundaries of what's possible in agent engineering. Here's to many more innovations! 🚀
Shout out to @AIMakerspace !

#LangGraph #LangSmith #NextJS #Vercel #AgentEngineering #Innovation #AI

Feel free to reach out if you're curious or would like to collaborate on similar projects! 🤝🔥
```

## Submitting Your Homework

Follow these steps to prepare and submit your homework assignment:

1. Package your agent with `langgraph.json` and run it locally with `langgraph dev`
2. Debug and demo the agent in LangGraph Studio
3. Deploy the agent to LangSmith and note your deployment URL
4. Build a Next.js frontend that streams from the deployed agent via a secure API route
5. Deploy the frontend to Vercel
6. Record a Loom video reviewing what you learned from this session

## Questions

### Question #1

Why does LangSmith deploy your agent as an API backend only, and why do you still need a separate frontend deployment like Vercel?

#### Answer

LangSmith deploys your agent as an **API backend only** because its job is to run the LangGraph agent — handle threads, runs, streaming, tool calls, and tracing — not to serve a user-facing website. The deployment exposes standard HTTP endpoints (threads, runs, assistants) that any client can call. It is optimized for agent execution, observability, and scaling the backend logic, not for hosting HTML, CSS, JavaScript, or a chat UI.

You still need a **separate frontend deployment like Vercel** because users interact through a browser app (the Next.js chat UI). That frontend renders the interface, streams responses to the user, and proxies requests to the LangSmith agent API through a secure server-side route so API keys are never exposed in the browser. LangSmith hosts the **brain** (agent API); Vercel hosts the **face** (website). Splitting them keeps concerns separated: the agent backend can scale and be monitored independently, while the frontend can be updated, styled, and deployed on its own without redeploying the agent.

### Question #2

Why should the LangSmith API key live in a Next.js API route (server-side) instead of in the browser?

#### Answer

The LangSmith API key must stay **server-side** because anything sent to the browser is visible to users. If the key were in client-side JavaScript, anyone could open DevTools, view the page source, or inspect network requests and steal it. They could then call your LangSmith deployment directly, run up your usage/costs, or abuse your agent API.

The Next.js `/api` route acts as a **secure proxy**: the browser only talks to your own frontend (`/api/*`), and the server injects the LangSmith API key when forwarding requests to the agent deployment. The key never leaves your server or appears in the client bundle. This follows the standard pattern of keeping secrets in environment variables on the host (Vercel), not in `NEXT_PUBLIC_*` variables that get bundled into the browser.

## Activity 1: Build a Helpfulness Loop in Production

Build an `agent_with_helpfulness` graph that adds a post-response helpfulness check: after the agent answers, a judge model decides whether the response is helpful, and if not, the graph loops back for another attempt (with a safe loop limit). Register it in `langgraph.json`, deploy it, then compare LangSmith traces for queries that pass vs. fail the helpfulness check. Does the retry loop behave differently in Studio vs. production?

#### Answer

**Implementation:** Added `app/graphs/agent_with_helpfulness.py` and registered it in `langgraph.json` as graph `agent_with_helpfulness` with assistant `agent_with_helpfulness`.

Graph flow:

```text
START → agent → (tool calls?) → action → agent
              → (no tool calls) → helpfulness → (Y?) → END
                                              → (N?) → agent  [retry]
                                              → (>10 msgs?) → END  [loop guard]
```

- **`agent`** — cat-health model with tools (RAG, Tavily, Arxiv), same system prompt as `simple_agent`.
- **`action`** — `ToolNode` executes tool calls, then returns to `agent`.
- **`helpfulness`** — judge model reads the initial user query and latest AI response; returns `HELPFULNESS:Y` or `HELPFULNESS:N`.
- **Loop guard** — if message count exceeds 10, emits `HELPFULNESS:END` and exits (prevents runaway cost).

**How to run locally (LangGraph Studio):**

```bash
cd 09_Agent_Servers
uv run langgraph dev
```

In Studio, select assistant **`agent_with_helpfulness`**, then test:

| Query | Expected behavior |
|-------|-------------------|
| *"How often should I deworm my cat?"* | Agent uses RAG → helpfulness judge likely passes on first try (`HELPFULNESS:Y`) |
| *"cat"* (vague) | Weak first answer → judge returns `N` → agent retries with a more complete response |

**Deploy to production:**

```bash
uv run langgraph deploy --name cat-health-agent-vijay
```

Both `simple_agent` and `agent_with_helpfulness` are included in the same deployment.

**Trace comparison (pass vs. fail):**

| Trace type | What you see in LangSmith |
|------------|---------------------------|
| **Pass (helpful on first try)** | `agent` → optional `action` (tools) → `agent` → `helpfulness` → END. Fewer nodes, lower latency, one model answer visible to the user. |
| **Fail (retry loop)** | Extra cycles: `helpfulness` → `agent` → … → `helpfulness` again. Trace shows multiple `agent` + `helpfulness` pairs. Each retry adds LLM cost. The final user-visible answer is the last `agent` message before `HELPFULNESS:Y`. |

**Studio vs. production:**

| | LangGraph Studio (local) | LangSmith production |
|---|--------------------------|----------------------|
| **Graph logic** | Same compiled graph | Same compiled graph |
| **Visibility** | Step-by-step in Studio UI; easy to inspect `HELPFULNESS:Y/N` markers inline | Full traces in LangSmith Deployments → Runs; harder to see live but better for comparing runs over time |
| **Latency** | Lower (local server) | Higher (network + cloud cold start) |
| **Retry behavior** | Identical routing — retries fire when judge returns `N` | Identical routing; retries show as extra span groups in the trace |
| **Loop guard** | Triggers at >10 messages in state | Same guard; important in production where vague queries could otherwise loop |

**Key takeaway:** The helpfulness loop adds a **quality gate** at the cost of extra judge-model calls and possible retries. In production, traces for failed-then-recovered queries are visibly longer than one-shot passes — useful for spotting when the agent needs better prompts, tools, or judge calibration. For the Vercel frontend, switch `ASSISTANT_ID` to `"agent_with_helpfulness"` in `frontend/app/page.tsx` to demo this graph in the live chat UI.

## Advanced Activity: Auth and Custom Routes

Research [LangSmith Deployments custom routes](https://github.com/langchain-samples/lsd-custom-route-react-ui) and describe how you could add authentication so each user only sees their own threads. Optionally implement a simple auth gate on your Vercel frontend.

Include your findings and a demo in your Loom video.
