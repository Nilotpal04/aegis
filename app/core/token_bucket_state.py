from dataclasses import dataclass
from uvicorn.protocols.http import flow_control

@dataclass
class TokenBucketState:
    token: float
    last_refill: float
    