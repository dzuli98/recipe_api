# recepe_api
Recepe API project


# docker compose
docker compose up -d


# Redis

### Rate Limiting in This API

To protect the API from abuse and ensure fair usage, this project implements **rate limiting**. Two strategies are discussed below.

---

#### 1️⃣ Fixed Window Rate Limiting

**How it works:**  
- Counts the number of requests per client in **fixed time intervals** (e.g., 5 requests per 60 seconds).  
- Each request increments a Redis counter, which resets at the end of the window.

**Example:**

| Time      | Requests Allowed |
|----------|-----------------|
| 0–60s    | 5               |
| 60–120s  | 5               |

**Pros:**  
- Simple to implement  
- Very low overhead (only a counter per client in Redis)  
- Easy to understand and debug

**Cons:**  
- **Burst problem:** Users can exceed the intended limit if they send requests at the boundary between windows  
- Less fair for rapid traffic or high-frequency requests

**Why it was used initially:**  
- Easy for prototyping and internal testing  
- Suitable for low-traffic scenarios

---

#### 2️⃣ Sliding Window Rate Limiting

**How it works:**  
- Tracks **timestamps of each request** using a Redis sorted set.  
- Counts requests in the **last N seconds dynamically**, rather than in fixed intervals.  
- Blocks the request if the number of requests in the current window exceeds the limit.

**Example:**

| Request Time (s) | Requests in Last 60s |
|-----------------|---------------------|
| 0               | 1                   |
| 10              | 2                   |
| 50              | 3                   |
| 70              | 3 (old requests removed) |

**Pros:**  
- Prevents bursts at window boundaries → **fairer and more accurate**  
- Handles **high-frequency requests** safely  
- Scales well for production use

**Cons:**  
- Slightly more complex implementation  
- Uses more memory (stores timestamps per request)  
- More Redis commands per request (`ZADD`, `ZREM`, `ZCARD`)

**Why it was switched to in production:**  
- Needed a **robust solution** for real-world usage  
- Prevents exceeding the request limit in rapid bursts  
- Provides a **smooth and predictable rate limiting experience**

---

#### ✅ Summary Table

| Feature                  | Fixed Window       | Sliding Window           |
|--------------------------|-----------------|-------------------------|
| Implementation           | Simple counter   | Sorted set (timestamps) |
| Burst at window boundary | Possible         | Prevented               |
| Memory usage             | Very low         | Higher (timestamps stored) |
| Accuracy                 | Approximate      | Exact                   |
| Best for                 | Low-traffic, simple | Production, high-traffic |


## Background Tasks (FastAPI)

FastAPI BackgroundTasks are used to execute **lightweight, non-critical work after the HTTP response has been sent to the client**.

This allows the user to receive a response immediately, while additional work is performed in the background.

### Typical use cases
- Logging
- Audit trails
- Metrics / analytics
- Fire-and-forget notifications (e.g. Slack, webhooks)

### How it works
- A `BackgroundTasks` instance is **created per request**
- Tasks are **registered**, not executed immediately
- The HTTP response is sent to the client
- After the response is sent, the registered tasks are executed

### Important characteristics
- Background tasks run **in the same worker process**
- They run **on the same machine**
- Tasks are executed **sequentially**
- There is **no retry mechanism**
- Tasks are **lost if the process crashes**
- Long-running tasks will **block the worker**

### When to use BackgroundTasks
- The task is short and lightweight
- The task is not business-critical
- It is acceptable to lose the task on failure
- No retries or persistence are required

### When NOT to use BackgroundTasks
- Sending important emails (e.g. password reset)
- Payments or billing
- Long-running or CPU-intensive jobs
- Tasks that must be retried or guaranteed

For critical or long-running work, a task queue such as **Celery** should be used instead.
