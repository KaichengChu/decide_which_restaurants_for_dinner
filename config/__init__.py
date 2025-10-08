import os

import yaml

abs_path = os.path.dirname(os.path.abspath(__file__))
def load_config(yaml_path: str = os.path.join(abs_path, "config.yaml")) -> dict:
    with open(yaml_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


CONFIG = load_config()