import pymysql
from datetime import datetime

def transfer_data_to_db(crop_list, label_list, color_list, combi_list, categori_list, recommend_type, secret):
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
    
    for crop, label, color, combi, categori in zip(crop_list, label_list, color_list, combi_list, categori_list):
        cur.execute(f"INSERT INTO CRAWL_DATA(crawlCategory, crawlClothesCategory, crawlClothes, crawlColor, crawlCount, crawlDate) VALUES ('{recommend_type}','{categori}','{label}','{color}',{1},'{date}')")
    
    conn.commit()
    conn.close()
    return True
