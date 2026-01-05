# recepe_api
Recepe API project


# docker compose
docker compose up -d


# Redis

## Rate Limiting in This API

To protect the API from abuse and ensure fair usage, this project implements **rate limiting**. Two strategies are discussed below.

---

### 1️⃣ Fixed Window Rate Limiting

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

### 2️⃣ Sliding Window Rate Limiting

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

### ✅ Summary Table

| Feature                  | Fixed Window       | Sliding Window           |
|--------------------------|-----------------|-------------------------|
| Implementation           | Simple counter   | Sorted set (timestamps) |
| Burst at window boundary | Possible         | Prevented               |
| Memory usage             | Very low         | Higher (timestamps stored) |
| Accuracy                 | Approximate      | Exact                   |
| Best for                 | Low-traffic, simple | Production, high-traffic |
