# 19. GPU Programming in Python — CUDA & Triton Deep Dive

> The underlying reality of modern AI is that Python is merely a control plane mapping instruction graphs to NVIDIA hardware. When you encounter memory bottlenecks or unsupported tensor operations in PyTorch, you must step beneath the framework abstraction and program the GPU directly.

---

## 🔍 The GPU Hardware Model

To understand Python GPU bindings, you must understand the hardware you are programming.
1.  **Host:** The CPU and System RAM. Managed by the Python runtime.
2.  **Device:** The GPU and VRAM.
3.  **Streaming Multiprocessors (SMs):** The independent computing clusters on the GPU.
4.  **Cores/Threads:** Thousands of tiny ALUs. GPUs don't execute varied code; they use SIMT (Single Instruction, Multiple Threads)—a single math operation applied to arrays of data simultaneously.

*Data transfer between Host (PCIe) and Device is the slowest operation in AI. Minimizing PCIe traffic is the primary goal of GPU programming.*

---

## 🏭 CuPy: NumPy for the GPU

If you need fast array math but don't want the overhead of PyTorch's autograd graphs, `cupy` is the C++ binding to NVIDIA CUDA libraries. Its API mirrors NumPy exactly.

```python
import cupy as cp
import numpy as np
import time

# Host memory (RAM)
np_array = np.random.randn(10000, 10000)

# Move to Device memory (PCIe Transfer - SLOW)
cp_array = cp.asarray(np_array) 

print("Executing NumPy (CPU)...")
start = time.perf_counter()
np_result = np.linalg.svd(np_array) # Singular Value Decomposition
print(f"NumPy took: {time.perf_counter() - start:.2f}s")

print("Executing CuPy (GPU)...")
start = time.perf_counter()
# Executes identical math on thousands of CUDA cores
cp_result = cp.linalg.svd(cp_array) 
cp.cuda.Stream.null.synchronize() # MUST force Python to wait for GPU to finish!
print(f"CuPy took: {time.perf_counter() - start:.2f}s")

# Move back to Host (PCIe Transfer - SLOW)
final_result = cp.asnumpy(cp_result[0])
```

### The Synchronization Trap
Notice `cp.cuda.Stream.null.synchronize()`. GPU operations in Python are **asynchronous**. When you run `c = a + b` in CuPy or PyTorch, Python instantly moves onto the next line of code before the GPU has even started computing. If you attempt to benchmark time without synchronizing, you will measure the time it takes Python to *queue* the operation, not execute it!

---

## 🚀 OpenAI Triton: Modern Custom Kernels

Historically, writing custom GPU operations meant writing complex PyTorch C++ extensions bound to raw CUDA C code. OpenAI released **Triton** (not to be confused with NVIDIA Triton Server): an open-source language that looks like Python but compiles down directly to PTX (NVIDIA assembly code).

Triton allows you to specify memory layouts dynamically in Python, bypassing the framework limitations of PyTorch.

```python
import triton
import triton.language as tl
import torch

@triton.jit
def add_kernel(
    x_ptr,  # Pointer to input array 1
    y_ptr,  # Pointer to input array 2
    output_ptr,  # Pointer to output array
    n_elements,  # Total size of the arrays
    BLOCK_SIZE: tl.constexpr,  # How many elements each GPU block calculates
):
    """
    This function executes independently on hundreds of GPU threads simultaneously.
    It simulates a fast vector addition bypassing PyTorch overhead.
    """
    # 1. Identify which block this specific thread belongs to
    pid = tl.program_id(axis=0)
    
    # 2. Calculate the memory offsets this block is responsible for
    block_start = pid * BLOCK_SIZE
    offsets = block_start + tl.arange(0, BLOCK_SIZE)
    
    # Mask out operations if the array length isn't perfectly divisible by BLOCK_SIZE
    mask = offsets < n_elements
    
    # 3. Load data from the GPU's Global VRAM into the fast SRAM (Registers)
    x = tl.load(x_ptr + offsets, mask=mask)
    y = tl.load(y_ptr + offsets, mask=mask)
    
    # 4. Math processing
    output = x + y
    
    # 5. Store back into VRAM
    tl.store(output_ptr + offsets, output, mask=mask)

def execute_custom_addition(x: torch.Tensor, y: torch.Tensor):
    output = torch.empty_like(x)
    assert x.is_cuda and y.is_cuda and output.is_cuda
    
    n_elements = output.numel()
    
    # Launch configuration: how many blocks of 1024 to map over the GPU
    grid = lambda meta: (triton.cdiv(n_elements, meta['BLOCK_SIZE']),)
    
    # Invoke the hardware-compiled kernel
    add_kernel[grid](x, y, output, n_elements, BLOCK_SIZE=1024)
    return output
```

---

## 🎯 Senior Engineer Interview Questions

**Q1: Explain what "CUDA Pinned Memory" (Page-locked memory) is and why PyTorch uses it via `pin_memory=True` in DataLoaders.**
> **Answer:** During standard PCIe transfers, the OS must copy data from the application's pageable memory into a temporary "pinned" buffer in the OS kernel before the GPU can use Direct Memory Access (DMA) to fetch it. Setting `pin_memory=True` tells the Host OS to directly page-lock the RAM associated with those Python tensors. This allows the GPU to directly stream the data off the RAM and onto the VRAM via DMA, bypassing the CPU entirely and massively speeding up Host-to-Device transfers.

**Q2: In PyTorch distributed training, communication between GPUs on different nodes is a massive bottleneck. Can we use Python's multiprocessing queues to pass gradients between them?**
> **Answer:** Absolutely not. Python's multiprocessing uses serialization (Pickle) across CPU memory spaces, which is horrifyingly slow. We use NVIDIA's NCCL (Nvidia Collective Communication Library) backend wrapper in PyTorch. NCCL coordinates cross-GPU operations natively. If GPUs are on the same local board, it shuttles data across the NVLink bridges directly. If GPUs are on different physical cluster nodes, NCCL uses GPUDirect RDMA (Remote Direct Memory Access) over InfiniBand networks to stream the VRAM of Node A directly into the VRAM of Node B, bypassing the system CPUs and Python runtimes on both machines.

**Q3: What causes "CUDA error: device-side assert triggered" and why is it notoriously difficult to debug in Python?**
> **Answer:** This error is triggered by illegal memory access on the GPU (most commonly an index-out-of-bounds error during an Embedding lookup or CrossEntropy calculation). It is profoundly difficult to debug because GPU operations run asynchronously. By the time the GPU actually crashes and sends the interrupt back up the PCIe bus to the OS, Python has already moved on and executed 10 further lines of logic. The Python traceback points to the wrong line of code. To debug it, you must export the environment variable `CUDA_LAUNCH_BLOCKING=1`, forcing the kernel to wait and surface the error on the exact triggering line of code.

**Q4: Compare using PyTorch's native `.compile()` against writing a custom Triton kernel.**
> **Answer:** `torch.compile()` uses inductor under the hood, traversing the execution DAG and automatically generating optimized Triton kernels for you. For 95% of use cases, it perfectly maps memory usage, fuses operations (running RelU and MatMul in the same memory read cycle), and requires absolutely zero manual C++/Triton code. Writing a manual Triton kernel is necessitated only when you are researching completely novel mathematical algorithms that PyTorch doesn't natively composite well, or when extreme low-level control over exactly how SRAM blocks are partitioned is required for leading-edge optimization (e.g., implementing FlashAttention natively).

---

[← Previous: LLMOps](18-llmops.md) | [Back to Index](../README.md) | [Next: Testing →](20-testing.md)
