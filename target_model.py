from ultralytics import YOLO

import argparse
import os

from utils import load_config
os.environ['CUDA_LAUNCH_BLOCKING'] = "1"
os.environ["CUDA_VISIBLE_DEVICES"] = "0"


def main(parser):
    cfg = parser.parse_args()
    cfg = load_config(cfg.config)
    
    target_model = YOLO(cfg['model'])
    target_model.train(
        data=cfg['data_path'], 
        epochs=cfg['epochs']
    )
    
    if cfg['conver_to_onnx']:
        target_model.export(format='onnx')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config", 
        type=str, 
        default='./config/target_model.yaml',
        help="Set the config to train target model (Yolov8)."
    )

    main(parser)