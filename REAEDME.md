# OOTT-AI
## Architecture
## Detail

---

## Program
### Pre-requirement
1. Create ./config/secrets.yaml file
```yaml
# secrets.yaml
server:
  db:
    host: [MYSQL SERVER IP]
    port: [MYSQL SERVER PORT]
    user: [MYSQL USER]
    pw: [MYSQL PASSWORD]
    db: [MYSQL NAME]
    multipleStatements: True

trend_crawling:
  instagram_key:
    id: [INSTAGRAM ID]
    pw: [INSTAGRAM PASSWORD]
```

2. Install the module to run the program.
```bash
pip install ./requirements.txt
```

3. Install chrmoe for crawling (The code below is for linux.)
```bash
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install ./google-chrome-stable_current_amd64.deb
```

4. If you want to train target model (Yolo v8), refer to sample.txt, sample.jpg in the `main_data` folder and transfer the data to the format.

5. If you want to create a pseudo label, check sample.txt, sample.jpg in the `sub_images` folder and transfer the data to the format.

### Trend Crawling
Change the hyperparameters of `./config/trend_crawling.yaml` and run them.
<details>
<summary>📔 About hyperparameters config</summary>

```yaml
### ./config/trend_crawling.yaml ###
debug: True # Options for debugging
secret_dir: ./config/secrets.yaml # Path to Secret file 
image_num: 2 # Number of images per category to be collected during crawling
save_dir: ./data/crawling_images # Path to saving crawling images
serve_info: True # Request crawling results to AI servers
```
</details>

```bash
python ./trend_crawling.py --config ./config/trend_crawling.yaml
```

### Train Model (base / target)
Change the hyperparameters of `./config/base_model.yaml`, `./config/target_model.yaml` and run them.
<details>
<summary>📔 About hyperparameters config</summary>

```yaml
### ./config/base_model.yaml ###
model: GroundedSAM # Choose a large model for creating psudo labels. (eg. GroundedSAM, GroundingDino)
input_dir: ./data/sub_images # Path of data to generate psudo labels
output_dir: ./data/sub_data # Path to saving images and generated psudo labels
data_merge: True # Merges existing and psudo datasets
main_data_dir: ./data/main_data # Path to main data
merge_data_dir: ./data/augmented_data # Path of data to be merged
```
```yaml
### ./config/target_model.yaml ###
model: yolov8m # Choose from yolov8n, yolov8s, yolov8m, yolov8l and yolov8x
data_path: ./data/main_data/data.yaml # Paths of data to train the model
epochs: 1000 # Number of times to repeat the training
conver_to_onnx: True # Convert the model to the onnx form
```
</details>

```bash
python3 ./base_model.py --config ./config/base_model.yaml
python3 ./target_model.py --config ./config/target_model.yaml
```

### Run API Server
Change the hyperparameters of `./config/server.yaml` and run them.
<details>
<summary>📔 About hyperparameters config</summary>

```yaml
### ./config/server.yaml ###
secret_dir: ./config/secrets.yaml # Path to Secret file 
model:
  dir: ./runs/detect/train/weights/best.onnx # Path to trained model file
  iou_thres: 0.25 # IoU(Intersection of Union)
  conf_thres: 0.55 # Remove bounding boxes below confidence threshold.
info: # AI API Server config
  host: 0.0.0.0 
  port: 5543
  log_level: info
  workers: 1
```
</details>

```bash
python3 ./server.py --config ./config/server.yaml
```

---

## Author
```yaml
Github: @jeirfe
Website: jerife.github.io
Email: jerife@naver.com

Copyright © 2022 jerife.
This project is Apache-2.0 licensed.
```