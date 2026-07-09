from dataclasses import dataclass


@dataclass
class LeakyBucketState:
    water: float
    last_leak: float
