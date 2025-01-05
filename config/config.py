from pathlib import Path
import yaml

CONFIG_PATH = Path(__file__).resolve().parent.parent / 'config' / 'config.yaml'

with open(CONFIG_PATH, 'r') as yaml_file:
    config = yaml.safe_load(yaml_file)