import pymysql
from datetime import datetime

def transfer_data_to_db(crop_list, label_list, color_list, categori_list, combi_list, combi_color_list, recommend_type, secret):
    conn = pymysql.connect(
        host=secret['server']['db']['host'],
        user=secret['server']['db']['user'], 
        password=secret['server']['db']['pw'], 
        db=secret['server']['db']['db'], 
        port=secret['server']['db']['port'], 
        charset='utf8'
    )
    cur = conn.cursor()
    date = datetime.now().strftime("%Y-%m-%d")
    
    for label, color, categori in zip(label_list, color_list, categori_list):
        cur.execute(f"INSERT INTO CRAWL_DATA(crawlCategory, crawlClothesCategory, crawlClothes, crawlColor, crawlCount, crawlDate) VALUES ('{recommend_type}','{categori}','{label}','{color}',{1},'{date}')")
    for combi, combi_color in zip(combi_list, combi_color_list):
        combi = ','.join(combi)
        combi_color = ','.join(combi_color)
        cur.execute(f"INSERT INTO CRAWL_COORDI(coordiCategory, coordiClothes, coordiColor, coordiCount, coordiDate) VALUES ('{recommend_type}','{combi}','{combi_color}',{1},'{date}')") #  나중에 중복처리시 참고: ON DUPLICATE KEY UPDATE coordiCount = coordiCount + 1
    
    conn.commit()
    conn.close()