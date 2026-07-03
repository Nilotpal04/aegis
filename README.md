# Aegis

A production-grade distributed rate limiting library built from scratch using Python, Redis, and Lua.

Aegis explores how modern backend systems implement atomic, scalable rate limiting across multiple application servers.

## Features

- Fixed Window
- Sliding Window
- Token Bucket
- Leaky Bucket

### Storage Backends

- In-Memory
- Redis

### Distributed Features

- Redis Lua Scripts
- Atomic Operations
- Race Condition Safe
- Redis Server Time
- TTL-based Cleanup

### Tested

- Unit tests for every algorithm
- Redis integration tests

## Roadmap

- SDK
- Middleware
- Benchmarks
- Documentation
- Multi-language support