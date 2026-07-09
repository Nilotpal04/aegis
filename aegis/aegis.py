class Aegis:
    def __init__(
        self,
        backend,
        algorithm: str,
        **kwargs,
    ):
        self.limiter = backend.create_limiter(
            algorithm,
            **kwargs
        )
            
    def allow(self, key: str) -> bool:
        return self.limiter.allow(key)