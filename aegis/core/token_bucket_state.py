from dataclasses import dataclass

@dataclass
class TokenBucketState:
    tokens: float
    last_refill: float
