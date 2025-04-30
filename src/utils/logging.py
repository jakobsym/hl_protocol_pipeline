import logging.config
import yaml
from pathlib import Path

def config_logging():
    # create log directory
    (Path(__file__).parent.parent / "logs").mkdir(exist_ok=True)

    # load logging.yaml
    config_path = Path(__file__).parent.parent / "config" / "logging.yaml"
    with open(config_path) as f:
        config = yaml.safe_load(f)
        logging.config.dictConfig(config)

