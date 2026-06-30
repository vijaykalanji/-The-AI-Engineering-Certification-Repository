<p align="center" draggable="false"><img src="https://github.com/AI-Maker-Space/LLM-Dev-101/assets/37101144/d1343317-fa2f-41e1-8af1-1dbb18399719"
     width="200px"
     height="auto"/>
</p>

<h1 align="center" id="heading">Session 8: Model Context Protocol (MCP)</h1>

### [Quicklinks]()

| Session Sheet | Recording | Slides | Repo | Homework | Feedback |
|:--------------|:----------|:-------|:-----|:---------|:---------|
| [Session 8: MCP](https://github.com/AI-Maker-Space/The-AI-Engineering-Certification-v1.0/tree/main/00_Docs/Modules/08_MCP) |[Recording!](https://us02web.zoom.us/rec/share/rqw5I5hwbOOHy8TrGjnu0IjDJi53ykHb0k897jYfyHqZpgRhUuFP4A18d4NrcEKS.18sNk6Do9XwyaVUy) <br> passcode: `E56&^V+8`| [Session 8 Slides](https://canva.link/k8cixqgkfeghdsn) |You are here! | [Session 8 Assignment](https://forms.gle/TcjjChq38ydMjuqn8) | [Feedback 6/25](https://forms.gle/DvcWDgBXatBWCXqi7) |

## Useful Resources

**MCP (Model Context Protocol)**
- [MCP Official Docs](https://modelcontextprotocol.io/) — Spec, tutorials, and guides
- [MCP-UI](https://mcpui.dev/) — Official standard for interactive UI in MCP
- [MCP Auth Guide (Auth0)](https://auth0.com/blog/mcp-specs-update-all-about-auth/) — Deep dive into MCP auth spec updates

## Main Assignment

In this session, you will build an MCP server with OAuth authentication — a cat
shop application that exposes tools for browsing products, managing a cart, and
checking out.

The main entry point is:

```text
server.py
```

The server implementation lives in:

```text
app/
```

Available MCP tools:

- `list_products`
- `get_product`
- `add_to_cart`
- `view_cart`
- `remove_from_cart`
- `checkout`

## Setup

From this folder:

```bash
uv sync
```

Copy the example env file and fill in your OpenAI API key:

```bash
cp .env.example .env
```

## Running the MCP Server

Run the server locally:

```bash
uv run server.py
```

The server starts on `http://localhost:8000`.

### Expose the server with ngrok

In a separate terminal, start an ngrok tunnel:

```bash
ngrok http 8000
```

Copy the ngrok forwarding URL (e.g. `https://xxxx-xx-xx-xx-xx.ngrok-free.app`) and
restart the server with it:

```bash
ISSUER_URL=https://xxxx-xx-xx-xx-xx.ngrok-free.app uv run server.py
```

> **Note:** The `ISSUER_URL` must match the public URL clients use to reach the
> server, otherwise OAuth authentication will fail.

## Outline

### Breakout Room #1

- Set up the MCP server with OAuth and the product database
- Explore the MCP tools: `list_products`, `get_product`, `add_to_cart`, `view_cart`, `remove_from_cart`, `checkout`

### Breakout Room #2

- Connect an MCP client to the server
- Build an end-to-end interaction flow using the MCP tools

## Ship

The completed MCP server and client integration!

### Deliverables

- A short Loom of either:
  - the MCP server you built and a demo of the client interacting with it; or
  - the notebook you created for the Advanced Build

## Share

Make a social media post about your final application!

### Deliverables

- Make a post on any social media platform about what you built!

Here's a template to get you started:

```
🚀 Exciting News! 🚀

I am thrilled to announce that I have just built and shipped an MCP server with OAuth authentication! 🎉🤖

🔍 Three Key Takeaways:
1️⃣
2️⃣
3️⃣

Let's continue pushing the boundaries of what's possible in the world of AI and tool integration. Here's to many more innovations! 🚀
Shout out to @AIMakerspace !

#MCP #ModelContextProtocol #OAuth #Innovation #AI #TechMilestone

Feel free to reach out if you're curious or would like to collaborate on similar projects! 🤝🔥
```

## Submitting Your Homework 

Follow these steps to prepare and submit your homework assignment:

1. Review the MCP server code in `server.py` and the `app/` directory
2. Run the MCP server locally using `uv run server.py`
3. Connect to the server using an MCP client (e.g., Claude Desktop, or a custom client)
4. Test all available tools: browsing products, adding to cart, viewing cart, removing items, and checkout
5. Record a Loom video reviewing what you have learned from this session

## Questions

### Question #1

Why is OAuth important for MCP servers, and what security considerations should you keep in mind when exposing tools to AI clients?

#### Answer

OAuth is important for MCP servers because MCP tools are executable capabilities, not just static data reads. Without OAuth, any client that can reach the server could trigger sensitive actions (for example modifying carts or checking out) without user identity, consent, or scope boundaries. OAuth gives us authenticated identity, delegated consent, and scoped access so we can enforce least privilege.

When exposing tools to AI clients, key security considerations are:
- strict scope design (`read` vs `write`) and server-side scope checks on every tool call,
- short-lived access tokens plus refresh-token revocation and secure token storage,
- explicit confirmation patterns for destructive actions (for example checkout),
- strong input validation and output constraints to prevent prompt-induced misuse,
- audit logging, rate limiting, and safe public exposure (TLS, issuer URL consistency, and minimal attack surface).

### Question #2

What is Streamable HTTP transport in MCP, and why might you expose a server publicly with OAuth instead of using a local stdio connection?

#### Answer

Streamable HTTP transport is MCP over HTTP where the client and server exchange MCP messages as a continuous, stateful stream rather than one-off local process I/O. It enables remote clients, browser-based auth redirects, and multi-step interactions while preserving MCP semantics.

You might expose a server publicly with OAuth instead of local stdio when you need real authentication, shared access across machines, and production-like integration. Stdio is great for local development and trust boundaries on a single host, but it does not provide internet-reachable endpoints, OAuth redirect flows, or clean multi-user access patterns by itself.

## Activity 1: Extend the MCP Server

Add at least one new tool to the cat shop MCP server (e.g., `search_products`, `update_cart_quantity`, or `get_order_history`). Ensure the new tool integrates properly with the existing database and OAuth authentication. Demo the new tool through an MCP client and include it in your Loom video.

### Activity 1 Completion

Implemented `search_products(query, category=None)` in `app/tools.py`.

- Searches by keyword across product name and description
- Supports optional category filter
- Returns normalized product records sorted by ascending price
- Uses the existing MCP server/database stack and is exposed as a standard MCP tool

## Advanced Activity: Build a Custom MCP Client

Build a custom MCP client that connects to the cat shop server over Streamable HTTP, authenticates via OAuth, and orchestrates a multi-step shopping flow (browse → add to cart → checkout). Compare the developer experience of MCP-based tool integration vs. traditional REST API calls.

Include your findings and a demo in your Loom video.
