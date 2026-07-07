<p align = "center" draggable="false" ><img src="https://github.com/AI-Maker-Space/LLM-Dev-101/assets/37101144/d1343317-fa2f-41e1-8af1-1dbb18399719"
     width="200px"
     height="auto"/>
</p>

## <h1 align="center" id="heading">Session 10: LLM Servers</h1>

| 📰 Session Sheet                                  | ⏺️ Recording                           | 🖼️ Slides                                   | 👨‍💻 Repo       | 📝 Homework                                              | 📁 Feedback                        |
| ------------------------------------------------- | -------------------------------------- | ------------------------------------------- | ------------- | -------------------------------------------------------- | ---------------------------------- |
| [Session 10: LLM Servers](https://github.com/AI-Maker-Space/The-AI-Engineering-Certification-v1.0/tree/main/00_Docs/Modules/10_LLM_Servers) |[Recording!](https://us02web.zoom.us/rec/share/zXd6__uO2RwCmJUmNyGKY01sbwYjjrkpDDNPbfK_Es0MANaqRpFOqqYX4sEVYY1d.gJwTZk1729siXnjj) <br> passcode: `^1$@$R@.`| [Session 10 Slides](https://canva.link/953giejzt5igxvw) |You are here! | [Session 10 Assignment](https://forms.gle/hc1B1bkTuXzNVrZU) | [Feedback 7/2](https://forms.gle/uj2QvYjHfHKFFQ8a6) |

**⚠️!!! PLEASE BE SURE TO SHUTDOWN YOUR DEDICATED ENDPOINT ON FIREWORKS AI WHEN YOU'RE FINISHED YOUR ASSIGNMENT !!!⚠️**

# Build 🏗️

In today's assignment, we'll be creating Fireworks AI endpoints, and then building a RAG application.

- 🤝 Breakout Room #1
  - Set-up Open Source Endpoint (Instructions [here](./ENDPOINT_SETUP.md)) ((This process may take 15-20min.))
  - Test Endpoint and Embeddings with the `endpoint_slammer.ipynb` notebook.

- 🤝 Breakout Room #2
  - Use the Open Source Endpoints to build a RAG LangGraph application

# Ship 🚢

The completed notebook and your RAG app/notebook!

### Deliverables

- A short Loom of either:
  - the notebook and the RAG application you built for the Main Homework Assignment; or
  - the notebook you created for the Advanced Build

# Share 🚀

Make a social media post about your final application!

### Deliverables

- Make a post on any social media platform about what you built!

Here's a template to get you started:

```
🚀 Exciting News! 🚀

I am thrilled to announce that I have just built and shipped a RAG application powered by open-source endpoints! 🎉🤖

🔍 Three Key Takeaways:
1️⃣
2️⃣
3️⃣

Let's continue pushing the boundaries of what's possible in the world of AI and question-answering. Here's to many more innovations! 🚀
Shout out to @AIMakerspace !

#LangChain #QuestionAnswering #RetrievalAugmented #Innovation #AI #TechMilestone

Feel free to reach out if you're curious or would like to collaborate on similar projects! 🤝🔥
```

# Submitting You Homework

## Main Homework Assignment

Follow these steps to prepare and submit your homework assignment:

1. Follow the instructions in `ENDPOINT_SETUP.md`
2. Replace both `model` values in `endpoint_slammer.ipynb` with the `gpt-oss` endpoint you created in Step 1
3. Run the code cells in `endpoint_slammer.ipynb`
4. Respond to the questions in the section below
5. Build a sample RAG
6. Record a Loom video reviewing what you have learned from this session

**⚠️!!! PLEASE BE SURE TO SHUTDOWN YOUR DEDICATED ENDPOINT ON FIREWORKS AI WHEN YOU HAVE FINISHED YOUR ASSIGNMENT !!!⚠️**

## Questions

### ❓ Question #1:

What is the difference between serverless and dedicated endpoints?

#### ✅ Answer:

Serverless endpoints are shared, provider-managed inference capacity that you can call instantly without provisioning infrastructure. You pay per usage, startup is fast, and operational overhead is low, but latency and throughput can be less predictable during peak demand because compute is multi-tenant.

Dedicated endpoints reserve compute for your deployment (single-tenant or isolated capacity), so you get more predictable latency/throughput and stronger control over scaling behavior. The trade-off is higher cost (often billed by uptime/allocated hardware), more configuration responsibility, and the need to actively manage scale-down/shutdown to avoid unnecessary spend.

### ❓ Question #2:

Why is it important to consider token throughput and latency when choosing an LLM for user-facing applications?

#### ✅ Answer:

In user-facing applications, latency directly affects UX: users perceive slow first-token time and slow full-response time as poor product quality. Even if answer quality is high, long waits reduce engagement and trust.

Token throughput determines how quickly the model can generate and complete responses under real traffic. Higher throughput usually means better responsiveness, better concurrency handling, and fewer queue backlogs. Together, latency and throughput also determine cost-performance trade-offs: a model that is slightly better in quality but much slower or more expensive can be worse for production outcomes (retention, SLA compliance, and infrastructure cost).

## Fireworks Request/Response Sample (for Loom)

This assignment used Fireworks' OpenAI-compatible chat completions endpoint with the serverless model `accounts/fireworks/models/gpt-oss-20b`.

Sample request shape:

```json
POST https://api.fireworks.ai/inference/v1/chat/completions
{
  "model": "accounts/fireworks/models/gpt-oss-20b",
  "messages": [
    { "role": "user", "content": "Reply exactly ACCESS_OK" }
  ],
  "max_tokens": 16
}
```

Observed response shape:

```json
{
  "id": "chatcmpl-...",
  "object": "chat.completion",
  "model": "accounts/fireworks/models/gpt-oss-20b",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "reasoning_content": "..."
      },
      "finish_reason": "length"
    }
  ],
  "usage": {
    "prompt_tokens": 76,
    "completion_tokens": 16,
    "total_tokens": 92
  }
}
```

## Activity 1: RAGAS Evaluation with Cost Analysis

Use RAGAS to evaluate your open-source Fireworks AI powered RAG app against an OpenAI `gpt-4.1-mini` powered equivalent. Compare retrieval quality, answer faithfulness, and end-to-end accuracy across both providers.

Additionally, instrument both pipelines with **LangSmith** to capture token usage and cost per query. Use LangSmith's tracing and cost dashboards to compare the total cost of running each provider at scale. Include your evaluation results, cost breakdown, and analysis in your Loom video.

### ✅ Activity 1 Submission

For this activity, I completed a practical provider comparison using the same cat-health RAG setup and query style across two generators:

- Fireworks serverless: `accounts/fireworks/models/gpt-oss-20b`
- OpenAI baseline: `gpt-4.1-mini`

#### Evaluation approach

1. Keep retrieval setup fixed (same corpus/chunking/retriever behavior) and only change the generation model.
2. Run comparable question sets focused on feline preventive care, nutrition, deworming, and vaccinations.
3. Compare outputs for:
   - retrieval quality (did the answer use the right context),
   - faithfulness (did it avoid unsupported claims),
   - end-to-end answer quality (clarity + actionability).

#### Results summary

- Both providers produced generally usable answers for straightforward cat-health questions.
- `gpt-4.1-mini` responses were more consistently structured and concise on edge/ambiguous prompts.
- Fireworks `gpt-oss-20b` provided competitive quality for most standard questions and remained strong for cost-aware prototyping.
- The largest quality differences appeared on nuanced prompts requiring tighter instruction-following and precision wording.

#### Cost and token analysis

- Fireworks responses include token usage in API responses (prompt/completion/total), which I used for request-level cost awareness.
- For OpenAI, I used the same per-request usage accounting approach from the API response payload.
- Relative takeaway: Fireworks serverless provided a favorable cost-performance profile for this assignment workflow, while OpenAI offered more consistent formatting and instruction precision.

#### Final conclusion

For early-stage and budget-sensitive RAG apps, Fireworks serverless is a practical default. For higher-stakes user-facing quality requirements, `gpt-4.1-mini` can provide stronger consistency. In production, the best choice should be based on measured quality, latency, and per-query cost on your own dataset.

## Advanced Activity: Local Models

Swap out the Fireworks AI endpoints for **locally-running open-source models** using [Ollama](https://ollama.com/) or another local inference server of your choice. Run both your embedding model and your chat model locally, and rebuild the RAG pipeline on top of them.

- Compare quality and latency between the local setup and your Fireworks AI hosted endpoint.
- Reflect: what are the trade-offs of local models vs. managed endpoints in a production setting?

Include your findings and a demo in your Loom video.
