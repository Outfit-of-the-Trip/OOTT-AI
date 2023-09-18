import os
import yaml
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
secret_file = os.path.join(BASE_DIR, 'config/secrets.yaml')  # secrets.json 파일 위치를 명시

def load_config(path):
    with open(path) as f:
        info = yaml.load(f, Loader=yaml.FullLoader)
    return info