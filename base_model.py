from autodistill.detection import CaptionOntology
import supervision as sv
import argparse

from distutils.dir_util import copy_tree
import shutil
import os
from glob import glob

from utils import load_config
os.environ['CUDA_LAUNCH_BLOCKING'] = "1"
os.environ["CUDA_VISIBLE_DEVICES"] = "0"


ontology=CaptionOntology({
    "blazer": "blazer",
    "denim jacket": "denim jacket",
    "leather jacket": "leather jacket",
    "coat": "coat",
    "windbreaker jacket": "windbreaker jacket",
    "cardigan": "cardigan",
    "puffer": "puffer",
    "tee shirt": "tee shirt",
    "long sleeve shirt": "long sleeve shirt",
    "tank top": "tank top",
    "shirt": "shirt",
    "polo shirt": "polo shirt",
    "sweat shirt": "sweat shirt",
    "hoodie sweat shirt": "hoodie sweat shirt",
    "knit sweater": "knit sweater",
    "dress": "dress",
    "jeans": "jeans",
    "slacks": "slacks",
    "sweat pants": "sweat pants",
    "skirt": "skirt",
    "short pants": "shorts pants",
    "sneakers": "sneakers",
    "dress shoes": "dress shoes",
    "sandals": "sandals"
})


def main(parser):
    cfg = parser.parse_args()
    cfg = load_config(cfg.config)
    
    if cfg['model'] == "GroundedSAM":
        from autodistill_grounded_sam import GroundedSAM
        
        base_model = GroundedSAM(ontology=ontology)
        dataset = base_model.label(
            input_folder=cfg['input_dir'],
            extension=".jpg",
            output_folder=cfg['output_dir'])
        
    elif cfg['model'] == "GroundingDino":
        from autodistill_grounding_dino import GroundingDino
        
        base_model = GroundingDino(ontology=ontology)
        dataset = base_model.label(
            input_folder=cfg['input_dir'],
            extension=".jpg",
            output_folder=cfg['output_dir'])


    dataset = sv.DetectionDataset.from_yolo(
        images_directory_path=cfg['output_dir']+'/train/images',
        annotations_directory_path=cfg['output_dir']+'/train/labels',
        data_yaml_path=cfg['output_dir']+'/data.yaml')


    if cfg['data_merge']:
        copy_tree(cfg['main_data_dir'], cfg['merge_data_dir'])
        
        data_yaml_path = cfg['merge_data_dir']+'/data.yaml'
        new_data_yaml = ''
        with open(data_yaml_path, 'r') as f:
            lines = f.readlines()
            for i, l in enumerate(lines):
                new_data_yaml += l.replace('main_data', 'augmented_data')
        with open(data_yaml_path,'w') as f:
            f.write(new_data_yaml)
            
        train_data_path = cfg['merge_data_dir']+'/train/images'
        train_label_path =  cfg['merge_data_dir']+'/train/labels'
        
        for file in glob(cfg['output_dir']+'/*/images/*'):
            file_label = file.replace('jpg', 'txt').replace('images', 'labels')
            file_name = file.split('/')[-1].split('.')[0]
            
            shutil.copy(file, train_data_path+f'/{file_name}.jpg')
            shutil.copy(file_label, train_label_path+f'/{file_name}.txt')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config", 
        type=str, 
        default='./config/base_model.yaml',
        help="Set the config to train base model."
    )

    main(parser)