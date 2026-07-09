class AegisError(Exception):
    """Base exception for Aegis"""
    
class UnsupportedBackendError(AegisError):
    pass

class UnsupportedAlgorithmError(AegisError):
    pass
