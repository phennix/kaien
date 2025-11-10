# Loads and parses config.yaml

# kaien_core/config.py
import yaml
from typing import Dict, Any

def load_config(path: str = "config/config.yaml") -> Dict[str, Any]:
    """Loads the YAML configuration file."""
    try:
        with open(path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        raise Exception(f"Configuration file not found at: {path}")
    except Exception as e:
        raise Exception(f"Error loading configuration: {e}")