import yaml

from app.common.config import Paths


def read_config(paths: Paths) -> dict:
    with paths.config_file.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)
