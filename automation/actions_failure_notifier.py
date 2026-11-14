"""Minimal state-repo launcher. Logic is maintained in public book-translator."""
from runtime_loader import load_shared_module

load_shared_module(__name__, "actions_failure_notifier.py")
