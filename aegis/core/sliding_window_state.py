from collections import deque
from dataclasses import dataclass


@dataclass
class SlidingWindowState:
    requests: deque[float]
