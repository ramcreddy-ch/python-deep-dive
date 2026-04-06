# 23. LLM Engineering (LLMOps) — Transformers, RAG & LangChain

> "Large Language Models aren't just a new type of software; they are a new type of compute. Expert LLM Engineers use Python to bridge the 'Deterministic' world of code with the 'Probabilistic' world of AI via Prompt Engineering, Vector Databases, and high-speed token serving."

---

## 🌱 The Basics: Transformers & Tokenization
The entry-level way to use LLMs in Python is via the **HuggingFace Transformers** library.

- **Tokens**: LLMs don't read words; they read "Tokens" (numeric IDs representing word parts).
- **Inference**: The process of giving a model an input (Prompt) and getting an output (Completion).

```python
from transformers import pipeline

# 1. Simple setup
# This downloads a small pre-trained model and sets up the inference pipeline
# generator = pipeline('text-generation', model='gpt2')

# 2. Basic Inference
# result = generator("The future of AI in DevOps is", max_length=30)
# print(result)
```

---

## 🌿 Intermediate: LangChain & Prompt Workflows
`LangChain` and `LlamaIndex` are the standard frameworks for building complex AI applications. They provide a "Chain" of events.

**Real Use (Internal Tooling)**:
A chatbot that first searches your internal documentation and then answers a question.

```python
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

# 1. Define the Prompt Template
template = "You are an expert SRE. Answer the following question: {question}"
prompt = PromptTemplate(input_variables=["question"], template=template)

# 2. Combine with an LLM
# llm = ChatOpenAI(model_name="gpt-4", temperature=0)
# chain = prompt | llm
```

---

## 🌳 Advanced: RAG (Retrieval-Augmented Generation)
Senior engineers use **RAG** to give an LLM "Memory" of your private data without retraining the large model.

- **Embedding**: Converting text into an array of numbers (Vector).
- **Vector DB**: Storing those numbers in a database (like **Pinecone** or **Milvus**) that can find "Similar" text instantly.

```python
# Expert Pattern: RAG Workflow. 
# 1. User asks question.
# 2. Python converts question to Vector.
# 3. Vector DB finds relevant 3-4 paragraphs from your docs.
# 4. Python adds those paragraphs to the Prompt.
# 5. LLM answers using your private data.
```

---

## 🔥 Expert: vLLM & Inference Performance
Principal engineers use **vLLM** or **NVIDIA Triton** to serve models to thousands of users. This involves **Quantization** (making models smaller/faster) and **Paged Attention** (managing GPU memory efficiently).

---

## 🎯 Top 20 Principal Interview Questions (LLMOps)

1. **Q: What is 'Hallucination' in LLMs and how do you reduce it?**
   - **Answer**: This is when an LLM confidently says something that is factually incorrect. We reduce this using **RAG** (providing grounded evidence in the prompt) and setting the **Temperature** to 0 (making the output more deterministic and less 'creative').
2. **Q: What is the difference between 'Fine-Tuning' and 'RAG'?**
   - **Answer**: **Fine-Tuning** is like an expert taking a new degree (changing the model's weights permanently). **RAG** is like an expert looking up a book in a library (providing the information in the temporary context window). RAG is faster, cheaper, and safer for private data.
3. **Q: What is 'Tokenization'?**
   - **Answer**: The process of breaking down a string of text into smaller units (tokens) that the LLM can understand. Most common schemes are **BPE** (Byte Pair Encoding) or **WordPiece**.
4. **Q: What is a 'Prompt Template'?**
   - **Answer**: A reusable formatting string (using f-strings or Jinja2) that holds the constant part of a conversation (e.g., "Answer as a helpful assistant") and leaves placeholders for user input.
5. **Q: Explain 'Few-Shot' vs 'Zero-Shot' prompting.**
   - **Answer**: **Zero-Shot**: You give the LLM a task without any examples. **Few-Shot**: You give the LLM 3-5 examples of the input and desired output inside the prompt to "teach" it the pattern.
6. **Q: What is a 'Vector Embedding'?**
   - **Answer**: A multi-dimensional array of numbers that represents the **semantic meaning** of a piece of text. "King" and "Queen" will have similar vectors, whereas "King" and "Apple" will be far apart.
7. **Q: What is a 'Vector Database' (e.g., Pinecone, Milvus, Chroma)?**
   - **Answer**: An optimized database that stores and searches through millions of vector embeddings to find the most "Similar" information in milliseconds.
8. **Q: Explain the 'Attention Mechanism' in a Transformer.**
   - **Answer**: It allows the model to "focus" on different words in a sentence simultaneously, deciding which words are most relevant to understanding the current word (e.g., in "The bank was closed," the word 'closed' helps define if 'bank' is a riverbank or a financial bank).
9. **Q: What is 'Temperature' in LLM generation?**
   - **Answer**: A setting (usually from 0.0 to 1.0) that controls the **Randomness**. 0.0 makes the model deterministic (always picking the highest probability token); 1.0 makes it "creative" and more random.
10. **Q: What is 'Context Window' and why is it limited?**
    - **Answer**: The maximum number of tokens an LLM can "Keep in mind" at once. It is limited by the **GPU memory**, as the cost of processing tokens grows quadratically (O(n^2)) with the window size.
11. **Q: Explain 'LangChain' and 'LlamaIndex'.**
    - **Answer**: **LangChain** is a framework for building LLM applications via "Chains" of prompts and tools. **LlamaIndex** is more focused on **Data Ingestion** and **Search** over private data.
12. **Q: What is 'RLHF' (Reinforcement Learning from Human Feedback)?**
    - **Answer**: A training technique where humans rank different model outputs to "Tune" the model to be more helpful, safe, and aligned with human values.
13. **Q: What is 'Quantization' in LLMs?**
    - **Answer**: Reducing the precision of weights (e.g., from 16-bit to 4-bit) to make the model run on **cheaper GPUs** (or even local CPUs) with minimal accuracy loss.
14. **Q: What is an 'Agent' in an AI application?**
    - **Answer**: An LLM that has been given **Tools** (like a Python interpreter or a Search engine) and the power to "Select" which tool to use and how to use it based on the user's question.
15. **Q: Explain 'vLLM' and why it is 10x faster for serving.**
    - **Answer**: It uses a technique called **PagedAttention** to manage GPU memory more efficiently, allowing the model to handle much larger batches of requests and reducing wasted RAM.
16. **Q: What is 'Self-Attention'?**
    - **Answer**: The ability of a model to look at other words in the **same sentence** to understand the context of a given word. It's the core innovation of the Transformer architecture.
17. **Q: What is 'Model Hallucination'?**
    - **Answer**: When an LLM confidently produces factually incorrect output. This is a side-effect of its "Probabilistic" nature (it's essentially a very advanced auto-complete).
18. **Q: How do you perform 'Sentiment Analysis' with an LLM?**
    - **Answer**: By giving it a prompt: "Classify the sentiment of the following text as POSITIVE, NEGATIVE, or NEUTRAL: [Text]".
19. **Q: What is 'Semantic Search'?**
    - **Answer**: Searching for information based on **Meaning** rather than just matching Keywords. If you search for "fast vehicle," semantic search can find documents mentioning "quick cars."
20. **Q: How do you securely handle Personable Identifiable Information (PII) with LLMs?**
    - **Answer**: By using a Python script to **Redact** sensitive information (like names, SSNs, or credit cards) before sending the text to a public API like OpenAI or Anthropic.

---

[← Previous: MLOps](22-mlops.md) | [Next: Level 4 Recap →](../Level-4/24-performance-profiling.md)
