import logging
from .__version__ import __version__
from .PickyDict import PickyDict


logging.getLogger(__name__).addHandler(logging.NullHandler())

__author__ = "Florian Huber"
__all__ = [
    "__version__",
    "PickyDict",
]
