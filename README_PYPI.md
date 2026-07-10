# 🛡️ Aegis

Production-grade distributed rate limiting for Python powered by Redis and Lua.

## Installation

```bash
pip install aegis-rl
```

## Quick Start

```python
from aegis import Aegis
from aegis.backends import RedisBackend

backend = RedisBackend()

limiter = Aegis(
    backend=backend,
    algorithm="fixed_window",
    limit=100,
    window_size=60,
)

limiter.allow("user123")
```

## Supported Algorithms

- Fixed Window
- Sliding Window Log
- Token Bucket
- Leaky Bucket

## Features

- Redis Lua Scripts
- Atomic Operations
- Race-condition safe
- In-memory backend
- Redis backend
- Python SDK

## Documentation

See the GitHub repository for full documentation.