# 🛡️ Aegis

> A production-grade distributed rate limiting SDK for Python featuring multiple rate limiting algorithms, Redis-backed atomic execution with Lua scripts, and a clean, extensible backend architecture.

---

## Why Aegis?

Modern backend applications rarely run on a single server.

Whether you're building APIs with FastAPI, Flask, Django, or any other framework, your application will eventually be deployed across multiple instances behind a load balancer. At that point, traditional in-memory rate limiting stops working because each server maintains its own counters.

Aegis was built to solve that problem.

It provides multiple production-proven rate limiting algorithms, atomic Redis execution using Lua scripts, and an SDK that makes distributed rate limiting easy to integrate into your applications.

---

## Features

### 🚀 Multiple Rate Limiting Algorithms

- Fixed Window
- Sliding Window Log
- Token Bucket
- Leaky Bucket

### ⚡ Multiple Backends

- In-Memory
- Redis

### 🔒 Distributed & Atomic

- Redis Lua Scripts
- Atomic Operations
- Race Condition Safe
- Redis Server Time
- TTL-based Cleanup

### 🧪 Well Tested

- Unit tests for all algorithms
- Redis integration tests
- Distributed behavior validation

---

## Quick Start

### Installation

> Installation instructions will be available once Aegis is published on PyPI.

```bash
pip install aegis-rl
```

### Example

```python
from app import Aegis, RedisBackend

backend = RedisBackend()

limiter = Aegis(
    backend=backend,
    algorithm="fixed_window",
    limit=100,
    window_size=60,
)

if limiter.allow("user123"):
    print("Request Allowed")
else:
    print("Rate Limited")
```

---

## Supported Algorithms

| Algorithm | In-Memory | Redis | Distributed |
|-----------|:---------:|:------:|:-----------:|
| Fixed Window | ✅ | ✅ | ✅ |
| Sliding Window | ✅ | ✅ | ✅ |
| Token Bucket | ✅ | ✅ | ✅ |
| Leaky Bucket | ✅ | ✅ | ✅ |

---

## Architecture

```
                   Client
                      │
                      ▼
          RateLimitMiddleware
                      │
                      ▼
                  Aegis SDK
                      │
         ┌────────────┴────────────┐
         │                         │
   RedisBackend             MemoryBackend
         │                         │
         ▼                         ▼
 Redis Algorithms         Memory Algorithms
         │                         │
         ▼                         ▼
 Redis + Lua Scripts      InMemory Storage
```

--- 

## Project Structure

```
aegis/
│
├── algorithms/
├── backends/
├── middleware/
├── redis/
├── storage/
├── lua/
├── core/
├── tests/
└── docs/
```

---

## Roadmap

### Version 0.1

- [x] Four rate limiting algorithms
- [x] Redis backend
- [x] Lua-based atomic execution
- [x] SDK Factory
- [x] Backend abstraction
- [x] FastAPI middleware

### Next

- [ ] Benchmarks
- [ ] Prometheus Metrics
- [ ] OpenTelemetry Support
- [ ] GitHub Actions
- [ ] PyPI Release
- [ ] Documentation

### Future

- [ ] Node.js SDK
- [ ] Go SDK
- [ ] Java SDK

---

## Documentation

Detailed documentation is available inside the `docs/` directory.

- Architecture
- Algorithms
- Benchmarking
- SDK Guide

---

## Contributing

Contributions, issues, and feature requests are welcome.

Please read `CONTRIBUTING.md` before opening a Pull Request.

---

## License

This project is licensed under the MIT License.