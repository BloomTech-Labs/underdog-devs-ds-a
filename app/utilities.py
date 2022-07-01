from typing import Dict


def dict_to_str(data: Dict) -> str:
    """Convert dictionaries into easy to read strings."""
    return "\n" + "\n".join(f"{k}: {v}" for k, v in data.items())
