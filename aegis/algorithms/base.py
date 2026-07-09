from abc import ABC, abstractmethod


class RateLimiterAlgorithm(ABC):
    @abstractmethod
    def allow(self, key: str) -> bool:
        pass
