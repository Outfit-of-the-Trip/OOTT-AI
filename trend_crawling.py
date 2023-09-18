import argparse

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

import urllib.request
import ssl
import time

from utils import load_config
ssl._create_default_https_context = ssl._create_unverified_context


    
def crawling_setting(cfg):
    global driver
    secrect = load_config(cfg['secrect_dir'])
    ['trend_crawling']['instagram_key']
    service = Service(executable_path=ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(service=service, options=options)

    driver.get("https://instagram.com")

    driver.implicitly_wait(10)
    login_id = driver.find_element(By.CSS_SELECTOR, 'input[name="username"]')
    login_id.send_keys(secrect['trend_crawling']['instagram_key']['id'])
    login_pwd = driver.find_element(By.CSS_SELECTOR, 'input[name="password"]')
    login_pwd.send_keys(secrect['trend_crawling']['instagram_key']['pw'])
    driver.implicitly_wait(10)
    login_id.send_keys(Keys.ENTER)
    time.sleep(3)
    
    
def main(parser):
    cfg = parser.parse_args()
    cfg = load_config(cfg.config)
    
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
    location_list = [핫플레이스, 전통, 놀이공원, 바닷가, 산]
    
    crawling_setting(cfg)
    
    for location_list in location_list:
        for location in location_list:
            time.sleep(3)
            driver.get(f'https://www.instagram.com/explore/tags/{location}/')
            driver.implicitly_wait(15)
            first_img = driver.find_element(By.CSS_SELECTOR, '._aagw').click() # 첫번째 사진 클릭
            driver.implicitly_wait(15)
            

            for i in range(cfg['image_num']):
                try:
                    #사진 저장
                    img_element = driver.find_element(By.CSS_SELECTOR, '._aatk .x5yr21d.xu96u03.x10l6tqk.x13vifvy.x87ps6o.xh8yej3')
                    img_src = img_element.get_attribute('src')
                    save_dir = cfg['save_dir']
                    urllib.request.urlretrieve(img_src, f'{save_dir}/{location}/{i}.jpg')

                    # 다음 버튼 클릭
                    driver.find_element(By.CSS_SELECTOR, '._aaqg ._abl-').click()
                except:
                    # 다음 버튼 클릭
                    driver.find_element(By.CSS_SELECTOR, '._aaqg ._abl-').click()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config", 
        type=str, 
        default='./config/base_model.yaml',
        help="Set the config to train base model."
    )

    main(parser)