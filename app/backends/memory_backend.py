from app.storage.memory import InMemoryStorage

class MemoryBackend:
    def __init__(self):
        self.storage = InMemoryStorage()
        