# Session 1: Dense Vector Retrieval

### [Quicklinks]()


| 📰 Module Sheet                                                                  | ⏺️ Recording                                                                                                                                           | 🖼️ Slides                                             | 👨‍💻 Repo    | 📝 Homework                                                 | 📁 Feedback                                         |
| -------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------ | ------------- | ----------------------------------------------------------- | --------------------------------------------------- |
| [Dense Vector Retrieval](../00_Docs/Modules/01_Dense_Vector_Retrieval/README.md) | [Recording!](https://us02web.zoom.us/rec/share/sHWvo0Nd1aI0SEhKecOLEX9kFGVJJAdYfsKiuTmm8t85W48Z2lnjpnzTy8jAd8R5.PwuqibGwAZhvDd8c) passcode: `C62n^@Q!` | [Session 1 Slides](https://canva.link/htfqf8i39yejyhn) | You are here! | [Session 1 Assignment](https://forms.gle/Z9qskfVaAvPjn6gz8) | [Feedback 6/2](https://forms.gle/21a2uoL9DVZPwgJP6) |


## 🏗️ How AIM Does Assignments

> 📅 **Assignments will always be released to students as live class begins.** We will never release assignments early.

Each assignment will have a few of the following categories of exercises:

- ❓ **Questions** - these will be questions that you will be expected to gather the answer to. These can appear as general questions, or questions meant to spark a discussion in your breakout rooms.
- 🏗️ **Activities** - these will be work or coding activities meant to reinforce specific concepts or theory components.
- 🚧 **Advanced Builds (optional)** - Take on a challenge. These builds require you to create something with minimal guidance outside of the documentation.

## Main Assignment

In this assignment, you will build a vector RAG application using LangChain v1, OpenAI embeddings, and Qdrant.

The main notebook is:

```text
01_Cat_Health_Vector_RAG_LangChain_Qdrant.ipynb
```

The notebook uses the bundled cat health guideline PDF in `data/cat_health_guidelines.pdf`.

### Setup

From this folder, install the environment with uv:

```bash
uv sync
```

Then open the notebook in Cursor or VS Code and select the Python/Jupyter environment created by uv.

You will also need an OpenAI API key available when running the notebook.

---

## 🏗️ Activity #1: Embedding Similarity

Run the embedding similarity primer in the notebook.

You will compare embeddings for terms like:

- `king`
- `queen`
- `banana`
- `cat`
- `veterinarian`
- `cat health guidelines`

#### ❓Question #1

Why is cosine similarity useful for dense vector retrieval?

##### ✅ Answer:

When we search documents, we turn each chunk and the user’s question into lists of numbers called vectors. Cosine similarity tells us how similar two vectors are based on their direction, which reflects how close they are in meaning.

That’s useful because a user’s question is usually short, but document chunks are much longer. Both still become one vector of the same size. Cosine similarity lets us compare them fairly — we’re matching meaning, not text length.

It also avoids favoring longer vectors the way a simple dot product might. We get a score for each chunk, rank them, and pull back the ones that best match the question. That’s the core of dense vector retrieval in RAG.

---

## 🏗️ Activity #2: Build the Vector RAG Pipeline

Run the notebook sections that:

1. Load the PDF into LangChain `Document` objects
2. Split the document into chunks
3. Embed the chunks
4. Store the chunk embeddings in in-memory Qdrant
5. Retrieve relevant chunks with similarity scores
6. Generate an answer grounded in retrieved context

#### ❓Question #2

Why is metadata important for a RAG application?

##### ✅ Answer:

Metadata is important for the following reasons:

1. When a query returns a response, we can use metadata to identify the page and the name of the file for citation.
2. Metadata helps tag and group chunks. For instance, if I am looking for cat health, then `'source': 'cat_health_guidelines.pdf'` in the metadata is useful for grouping all the chunks together.

#### ❓Question #3

What tradeoff do we make when choosing chunk size and chunk overlap?

##### ✅ Answer:

**Chunk size:** Larger chunks contain more text, so each vector represents more information. That can help when a question needs surrounding context, but it can hurt retrieval for narrow questions because one chunk may mix several topics and its embedding becomes less precise. Smaller chunks are more focused and can match specific questions better, but they may not include enough context to fully answer a question, especially if an idea is split across chunks. Smaller chunks also mean more chunks overall, which requires more embeddings to store.

**Chunk overlap:** Some overlap helps avoid losing context at chunk boundaries when a sentence or idea is cut in half. Too little overlap increases that risk. Too much overlap creates duplicate content across chunks, which can lead to redundant results in top-k retrieval instead of diverse, useful context.

#### ❓Question #4

What does a similarity score help you understand, and what does it not prove by itself?

##### ✅ Answer:

The similarity score shows which retrieved text is closest to the input question, but it doesn’t prove the information is correct or that the AI will give a good answer.

---

## 🏗️ Activity #3: Vibe Check Retrieval Quality

Run the notebook's vibe check queries and inspect both:

- The retrieved context
- The generated answer

#### ❓Question #5

For the vibe check queries, did the retrieved context seem relevant before generation? Why or why not?

##### ✅ Answer:

For the vibe check queries, the retrieved context was mostly relevant for the cat-health questions, but not perfect. The taxes question worked the way I expected.

For preventive care, the chunks were mostly helpful. I got good passages about parasite prevention and annual vet visits. One chunk was just a reference list, which wasn’t useful. Still, enough context was there to answer the question.

For symptoms that should make me call a vet, retrieval was okay but not great. The best chunks mentioned things like vomiting, diarrhea, and changes in appetite or habits. Some chunks were only partly related, and one was more about kittens. The similarity scores were lower than the other questions, but the top results were still useful.

For feeding a healthy adult cat, retrieval was the best. All four chunks were about nutrition — things like RER/DER, AAFCO labels, body condition, and how much to feed. This question matched the PDF the most clearly.

For “Can my cat help me file my taxes?”, the retrieved context was not relevant, which makes sense. The chunks were still about cat health, but nothing about taxes. The scores were also the lowest. That’s what I’d want for a question the PDF can’t answer.

Overall, retrieval worked because similar questions pulled similar passages from the guidelines. But some chunks had extra noise (like bibliography sections), so not every source was equally helpful. The similarity scores helped rank results, but they didn’t guarantee every chunk was a perfect match.

---

## 🏗️ Activity #4: Tune Retrieval

Improve retrieval quality by changing one or more of:

- Chunk size
- Chunk overlap
- Retrieval `k`
- Query wording

Document what changed and whether retrieval improved.

##### Settings Changed:

I tried two things for the question *"What symptoms should make me call a veterinarian?"*

First, I made the chunks smaller (`chunk_size` 1000 → 500, `chunk_overlap` 200 → 100).

Then I rephrased the question to: *"What signs of illness or behavior changes in a cat should prompt a veterinary visit?"*

I kept `k = 4` the whole time.

##### Results:

Making the chunks smaller did not help much. The similarity scores were basically the same (0.435 vs 0.436), and the top chunk did not look better to me.

Rephrasing the question worked much better. The top score went up to 0.670, and the chunks I got back were actually about things like behavior changes and signs that a cat should see a vet.

So for this question, changing the wording mattered more than changing the chunk size. When I used words closer to how the PDF talks (like "signs," "behavior changes," and "veterinary visit"), retrieval improved a lot.

---

## Optional Deep Dive: RAG From Scratch

If you want to look underneath the library abstractions, run the optional reference notebook:

```text
02_Cat_Health_Vector_RAG_From_Scratch.ipynb
```

It builds the same retrieval pipeline again with only:

- `pypdf` for extracting text from the PDF
- Python standard-library HTTP requests for calling OpenAI
- Handcrafted document, chunking, embedding, similarity-search, vector-store, and generation primitives

This notebook is a reference walkthrough, not an additional assignment. Its purpose is to make the responsibilities hidden by LangChain, Qdrant, and provider SDKs visible.

---

## Submitting Your Homework

### Main Assignment

Follow these steps to prepare and submit your homework:

1. Pull the latest updates from upstream into the main branch of your AIE9 repo:

```bash
git checkout main
git pull upstream main
git push origin main
```

1. Start Cursor from the `01_Dense_Vector_Retrieval` folder.
2. Complete the notebook.
3. Answer the questions in this `README.md`.
4. Add, commit, and push your modified work to your origin repository.

When submitting your homework, provide the GitHub URL to your AIE9 repo.