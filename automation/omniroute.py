"""Private compatibility entrypoint for the immutable public Auto runtime.

Shared execution and provider logic are maintained in tim8es/book-translator.
Do not add implementation here: upgrade the reviewed public runtime lock.
"""
from runtime_loader import load_shared_module

load_shared_module(__name__, "omniroute.py")
