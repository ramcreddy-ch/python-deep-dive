# 18. LLMOps — Transformers, RAG & vLLM Deep Dive

> LLMOps (Large Language Model Operations) emerged as a distinct discipline because hosting a 70B parameter neural network breaks traditional MLOps architectures. The models barely fit in RAM, inference speed involves entirely new token-generation metrics, and prompt security/evaluation is largely non-deterministic.

---

## 🔍 Core Python Frameworks

### LangChain / LlamaIndex (The Orchestrators)
These libraries act as the glue between LLMs and external data/tools. They chain together prompts, model execution, and output parsers.

```python
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain

# 1. Strict Prompt Versioning (Never hardcode prompts in app logic)
template = """You are a senior Kubernetes operator. 
Explain the following error context to a junior engineer:
{error_log}
Keep it under 3 sentences."""
prompt = PromptTemplate(input_variables=["error_log"], template=template)

# 2. Model Invocation mapping
llm = ChatOpenAI(temperature=0.0, model="gpt-4-turbo")

# 3. Chain execution
chain = LLMChain(llm=llm, prompt=prompt)
response = chain.run(error_log="OOMKilled exit code 137")
```

---

## 🏭 RAG Architecture (Retrieval-Augmented Generation)

LLMs hallucinate. You cannot train an LLM on your company's private Confluence wiki every night. You must use RAG: storing semantic data in a Vector Database and injecting relevance into the prompt at inference time.

```python
import weaviate # Advanced Vector DB
from sentence_transformers import SentenceTransformer

# 1. Initialization
client = weaviate.Client("http://vector-db.internal:8080")
embedder = SentenceTransformer('BAAI/bge-large-en-v1.5')

def query_vector_db(user_query: str):
    """Retrieves context tightly matched to the query"""
    # Convert query text into a semantic array of floats
    query_vector = embedder.encode(user_query).tolist()
    
    # Cosine Similarity search against our database
    result = (
        client.query
        .get("EngineeringDocs", ["content", "url"])
        .with_near_vector({
            "vector": query_vector,
            "certainty": 0.85 # Filter out weak semantic matches
        })
        .with_limit(3)
        .do()
    )
    return result['data']['Get']['EngineeringDocs']

# The result is injected as {retrieved_context} into the LangChain prompt template
```

---

## 🚀 High-Performance Open Source LLMs (vLLM)

Using HuggingFace `transformers` `.generate()` loop in an API endpoint processing 100 users will OOM and timeout instantly. Python must yield to optimized C++/CUDA inference engines. **vLLM** is the modern standard for deploying Llama-3/Mistral internally.

### PagedAttention
vLLM utilizes "PagedAttention". In LLMs, the "KV Cache" (memory tracking previous tokens) grows dynamically and unpredictably, causing severe memory fragmentation in VRAM. PagedAttention divides the KV Cache into OS-like memory blocks, allowing non-contiguous allocation and boosting throughput by 3x-4x.

```python
# The Async vLLM Inference Engine
from vllm import AsyncLLMEngine, AsyncEngineArgs
from fastapi import FastAPI

app = FastAPI()

# Loads model with tensor parallelism (splitting 70B model across two 80GB A100 GPUs)
engine_args = AsyncEngineArgs(
    model="meta-llama/Llama-3-70b-instruct",
    tensor_parallel_size=2, 
    gpu_memory_utilization=0.90 # Claim 90% of VRAM aggressively
)
engine = AsyncLLMEngine.from_engine_args(engine_args)

@app.post("/generate")
async def generate(prompt: str):
    import uuid
    # Async stream generation. The engine natively batches multiple 
    # concurrent FastAPI requests in the background utilizing PagedAttention.
    request_id = str(uuid.uuid4())
    stream = await engine.add_request(request_id, prompt)
    
    # We yield SSE blocks back to the client
    async for request_output in stream:
        yield request_output.outputs[0].text
```

---

## 🎯 Senior Engineer Interview Questions

**Q1: Explain Time To First Token (TTFT) and Time Per Output Token (TPOT). Why do we measure them independently?**
> **Answer:** TTFT measures the latency from the API request to the delivery of the very first word. This captures the compute cost of the "prefill" phase (ingesting the potentially massive prompt and processing the first forward pass). TPOT measures the latency of the "decode" phase, generating each subsequent word sequentially. In LLMOps, we measure them independently because users tolerate a long total completion time if TTFT is fast (they start reading immediately), so TTFT drives perceived application speed, while TPOT defines our underlying compute cluster saturation.

**Q2: We are fine-tuning a 7 Billion parameter model. The weights require 14GB of RAM (float16). By adding the Adam Optimizer, our server crashes with an Out of Memory error on a 24GB GPU. Why?**
> **Answer:** The math of fine-tuning is extremely memory intensive. The model weights require 14GB. The gradients require another 14GB. The Adam optimizer maintains two momentum states per parameter (running average and variance), requiring 28GB. The forward-pass activations require more memory depending on sequence length. The total training memory is realistically >65GB. We must utilize PEFT protocols like LoRA (Low-Rank Adaptation) which freezes the base 14GB model and only tracks gradients/optimizers for a tiny fraction (~1%) of injected parameters.

**Q3: Describe standard techniques for securing an LLM endpoint against Prompt Injection attacks at the platform level.**
> **Answer:** Security requires defense-in-depth since LLMs lack deterministic boundaries between "instructions" and "data." First, use strict templating that separates system prompts from user input arrays. Second, utilize a fast "Guardrail Model" (like Llama-Guard or an adversarial RoBERTa classifier) as middleware to scan inbound user content for injection patterns *before* passing it to the slow/expensive generative LLM. Third, scan the output response for PII/toxicity before returning it to the user.

**Q4: Your semantic search (RAG) system is repeatedly returning irrelevant documents from the Vector Database. How do you re-architect it?**
> **Answer:** Pure embedding Vector search (Cosine Similarity via BERT/OpenAI embedders) suffers on highly domain-specific keywords or exact part numbers. I would implement a Hybrid Search. It queries the database using both Dense Vectors (Semantic meaning) and Sparse Vectors (BM25 / Keyword search). Then, I would deploy a cross-encoder "Re-ranker" step. The hybrid engine pulls 50 potential docs extremely fast, and the slow Re-ranker neural net explicitly scores the pairing of `(User Query, Document)` to pick the final top 3 contextual chunks to feed the LLM.

---

[← Previous: MLOps](17-mlops.md) | [Back to Index](../README.md) | [Next: GPU Programming →](19-gpu-programming.md)
