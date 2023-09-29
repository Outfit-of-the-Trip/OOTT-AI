import argparse
import shutil
import urllib.request
import ssl
import time
import requests
from glob import glob 
import base64
import os
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver

from google.cloud import storage

from utils import load_config
ssl._create_default_https_context = ssl._create_unverified_context


def gcs_setting(cfg):
    global bucket
    secret = load_config(cfg['secret_dir'])
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = secret['trend_crawling']['gcs']['key']
    storage_client = storage.Client()
    bucket = storage_client.bucket("oott_crawling")

def crawling_setting(cfg):
    global driver
    secret = load_config(cfg['secret_dir'])
        
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--single-process")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get("https://instagram.com")

    driver.implicitly_wait(10)
    login_id = driver.find_element(By.CSS_SELECTOR, 'input[name="username"]')
    login_id.send_keys(secret['trend_crawling']['instagram_key']['id'])
    login_pwd = driver.find_element(By.CSS_SELECTOR, 'input[name="password"]')
    login_pwd.send_keys(secret['trend_crawling']['instagram_key']['pw'])
    driver.implicitly_wait(10)
    login_id.send_keys(Keys.ENTER)
    time.sleep(3)
    
    
def main(parser):
    cfg = parser.parse_args()
    cfg = load_config(cfg.config)
    gcs_setting(cfg)
    
    if cfg['debug']:
        핫플레이스 = ['홍대','연남동']
        전통 = ['인사동', '광화문']
        놀이공원 = ['롯데월드']
        바닷가 = ['을왕리', '가평']
        산 = ['인왕산','관악산']
    else:
        핫플레이스 = ['홍대','연남동','명동','익선동','성수동','동대문','한남동','이태원', '강남', '가로수길']
        전통 = ['인사동', '광화문', '불국사', '경주', '경복궁', '창덕궁', '창경궁', '덕수궁', '경희궁']
        놀이공원 = ['롯데월드','에버랜드','서울랜드','경주월드']
        바닷가 = ['을왕리', '가평', '정동진', '해운대', '제주', '광안리', '양양', '협지해수욕장']
        산 = ['인왕산','관악산','성산일출봉','북악산','낙산','북한산','도봉산','아차산','용마산']
        
    location_dict = {
        '핫플레이스': 핫플레이스,
        '전통': 전통,
        '놀이공원': 놀이공원,
        '바닷가': 바닷가,
        '산': 산
    }
    
    crawling_setting(cfg)
    date = datetime.now().strftime("%Y-%m-%d")
    print(f"#################### {date}: Start Crawling ####################")
    
    for location_categori, location_list in location_dict.items():
        save_dir = cfg['save_dir']
        os.makedirs(f'{save_dir}/{date}/{location_categori}', exist_ok=True)
        i = 0
        
        for location in location_list:
            print(f'{date}: {location_categori} - {location}')
            time.sleep(3)
            driver.get(f'https://www.instagram.com/explore/tags/{location}/')
            driver.implicitly_wait(15)
            first_img = driver.find_element(By.CSS_SELECTOR, '._aagw').click() # 첫번째 사진 클릭
            driver.implicitly_wait(15)
            
            for _ in range(cfg['image_num']):
                try:
                    #사진 저장
                    img_element = driver.find_element(By.CSS_SELECTOR, '._aatk .x5yr21d.xu96u03.x10l6tqk.x13vifvy.x87ps6o.xh8yej3')
                    img_src = img_element.get_attribute('src')
                    save_name = f'{date}/{location_categori}/{i}.jpg'
                    urllib.request.urlretrieve(img_src, f'{save_dir}/{save_name}')
                    i += 1
                    
                    # Saving image to gcs
                    if cfg['save_gcs']:
                        blob = bucket.blob(save_name)
                        blob.upload_from_filename(f'{save_dir}/{save_name}')

                    driver.find_element(By.CSS_SELECTOR, '._aaqg ._abl-').click() # Click next button
                except:
                    driver.find_element(By.CSS_SELECTOR, '._aaqg ._abl-').click() # Click next button

        if cfg['serve_info']:
            images = []
            data_path_list = glob(f'{save_dir}/{date}/{location_categori}/*')
            
            for img in data_path_list:
                with open(img, "rb") as f:
                    im_bytes = f.read()  
                im_b64 = base64.b64encode(im_bytes).decode("utf8")
                images.append(im_b64)

            url = f'http://0.0.0.0:5543/predict/batch'
            payload = {
                "base64_images": images,
                "recommend_type": location_categori
            }
            resp= requests.post(url=url, json=payload)
    
    shutil.rmtree(f'{save_dir}/{date}') # Remove loacl image
    print(f"#################### {date}: Finished Crawling ####################")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config", 
        type=str, 
        default='./config/trend_crawling.yaml',
        help="Set the config to train base model."
    )

    main(parser)