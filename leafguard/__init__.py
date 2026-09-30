"""LeafGuard AI: leaf and spot detection plus multilingual advice for crop disease screening."""
from .segmentation import analyze_leaf
from .advice import get_advice

__all__ = ["analyze_leaf", "get_advice"]
