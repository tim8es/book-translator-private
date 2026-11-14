"""Minimal state-repo launcher. Logic is maintained in public book-translator."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'automation'))
from runtime_loader import load_shared_module

load_shared_module(__name__, "verify_changed_books.py")
