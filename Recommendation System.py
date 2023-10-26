def recomm_func(usr_Id, date_lst, season, gender,reason,category):
  fin_return_mew=[]
  fin_return=[]
  outer = ["windbreaker jacket","blazer","denim jacket","leather jacket","cardigan","coat","puffer"]
  top = ["tank top","tee shirt", "long sleeve shirt","shirt", "polo shirt", "sweat shirt", "hoodie sweat shirt", "knit sweater", "dress"]
  bottom =["jeans","slacks","short pants","sweat pants","skirt"]
  shoes = ["sandals","sneakers", "dress shoes"]
  datelist_outer_lst=[[0,1,2],[1,2,0],[2,0,1]]
  datelist_top_lst=[[0,1,0],[0,0,1],[1,0,0]]
  datecollist_lst=[[0,1,2],[1,2,0],[2,0,1]]
  import mysql.connector
  db_config = {
      'host': '****',
      'user': '****',
      'password': '****',
      'database': '****'
  }
  conn = mysql.connector.connect(**db_config)
  cursor = conn.cursor()

  if season=='봄': season=0
  if season=='여름': season=1
  if season=='가을': season=2
  if season=='겨울': season=3
  if gender=='M': gender=0
  if gender=='F': gender=1
  if reason=='배낭여행' or reason=='레저여행'or reason=='탐방' or reason=='캠핑' or reason=='엠티': reason=0
  if reason=='호캉스' or reason=='핫플레이스' or reason=='인생샷':reason=1
  if reason=='출장' or reason=='워크숍' or reason=='학회':reason=2
  fin_return=""
  date_origin=[]
  date_lst = date_lst.split(',')
  for k in range(len(date_lst)):
    date_lst[k] = date_lst[k].replace("[","")
    date_lst[k] = date_lst[k].replace("]","")
    date_lst[k] = date_lst[k].replace("'","")
    date_origin.append(date_lst[k])
  date_lst_origin=date_lst
  if len(date_lst)>3:
    date_lst = date_lst[:3]
  for d in range(len(date_lst)):
    date = date_lst[d]
    date = date.replace("[","")
    date = date.replace("]","")
    date = date.replace("'","")
    for i in range(3):
      if d==i:
        datelist_outer=datelist_outer_lst[i]
        datelist_top=datelist_top_lst[i]
        datecollist=datecollist_lst[i]
    trend_outer_before=[]
    trend_top=[]
    trend_outer_col=[]
    trend_top_col=[]

    qtrend_outer=f"SELECT crawlClothes FROM CRAWL_DATA where crawlClothesCategory='outer' and crawlCategory='{category}' GROUP BY crawlCategory,crawlClothesCategory,crawlClothes ORDER BY SUM(crawlCount) DESC LIMIT 2;"
    qtrend_top=f"SELECT crawlClothes FROM CRAWL_DATA where crawlClothesCategory='top' and crawlCategory='{category}' GROUP BY crawlCategory,crawlClothesCategory,crawlClothes ORDER BY SUM(crawlCount) DESC LIMIT 2;"
    qtrend_outer_col=f"SELECT crawlColor FROM CRAWL_DATA where crawlClothesCategory='outer' and crawlCategory='{category}' GROUP BY crawlCategory,crawlClothesCategory,crawlColor ORDER BY SUM(crawlCount) DESC LIMIT 3;"
    qtrend_top_col=f"SELECT crawlColor FROM CRAWL_DATA where crawlClothesCategory='top' and crawlCategory='{category}' GROUP BY crawlCategory,crawlClothesCategory,crawlColor ORDER BY SUM(crawlCount) DESC LIMIT 3;"
    if conn.is_connected():
      cursor.execute(qtrend_outer)
      trend_outer = cursor.fetchall()
      cursor.execute(qtrend_outer_col)
      trend_outer_col = cursor.fetchall()
      cursor.execute(qtrend_top)
      trend_top = cursor.fetchall()
      cursor.execute(qtrend_top_col)
      trend_top_col = cursor.fetchall()
    rem=["(",")",",","'"]
    for r in rem:
      for i in range(2):
        trend_outer[i] = str(trend_outer[i]).replace(r,"")
    for r in rem:
      for i in range(3):
        trend_outer_col[i] = str(trend_outer_col[i]).replace(r,"")
    for r in rem:
      for i in range(2):
        trend_top[i] = str(trend_top[i]).replace(r,"")
    for r in rem:
      for i in range(3):
        trend_top_col[i] = str(trend_top_col[i]).replace(r,"")
    outer_col=[]
    top_col=[]
    """
    for i in range(3):
      outer_col.append(trend_outer_col[i])
      top_col.append(trend_top_col[i])
  """


    user_input_filter=[season,gender] #계절,성별,who(x, 시밀러룩,커플룩(0,1,2)), 상대방 outter,top("beige_coat, white_long_tee")
    user_input_score=[reason,category,trend_outer,trend_top]
    tmp_fin_outer=[]
    tmp_fin_top=[]
    tmp_fin_bottom=[]
    outer_today = outer
    top_today = top
    bottom_today = bottom
    shoes_today = shoes
    outer_todayscore = [0]*7
    top_todayscore = [0]*9
    bottom_todayscore = [0]*5
    shoes_todayscore = [0]*3

    #socre
    if user_input_score[0]==0: #편안한 관광:10
      outer_todayscore[0]+=10 #바람막이
      outer_todayscore[4]+=5#가디건
      outer_todayscore[6]+=10#패딩
      top_todayscore[0]+=10#민소매0
      top_todayscore[1]+=10#반팔티1
      top_todayscore[2]+=10#긴팔티2
      top_todayscore[5]+=10#맨투맨5
      top_todayscore[6]+=10#후드6
      top_todayscore[-1]-=10#원피스
      top_todayscore[3]-=10#셔츠
      bottom_todayscore[-1]-=10#치마
      bottom_todayscore[0]+=5#청바지0
      bottom_todayscore[2]+=10#반바지2
      bottom_todayscore[3]+=15#트레이닝바지3
      shoes_todayscore[0]+=5#샌달0
      shoes_todayscore[1]+=10#운동화1
    if user_input_score[0]==1: #인생샷 남기고 싶은 관광
      outer_todayscore[1]+=10 #블레이져1
      outer_todayscore[2]+=10 #청자켓2
      outer_todayscore[3]+=10 #가죽자켓3
      outer_todayscore[4]+=5 #가디건4
      outer_todayscore[5]+=10 #코트5
      top_todayscore[3]+=5 #셔츠3
      top_todayscore[7]+=10 #니트7
      top_todayscore[8]+=15 #원피스8
      bottom_todayscore[0]+=10 #청바지0
      bottom_todayscore[1]+=5 #슬랙스1
      bottom_todayscore[2]+=5 #반바지2
      bottom_todayscore[4]+=12 #치마4
      shoes_todayscore[2]+=15#구두2
    if user_input_score[0]==2: #일
      outer_todayscore[1]+=10 #블레이저1
      outer_todayscore[4]+=5 #가디건4
      outer_todayscore[5]+=10 #코트5
      top_todayscore[0]-=10 #반팔티1
      top_todayscore[1]+=5 #반팔티1
      top_todayscore[2]+=5 #긴팔티2
      top_todayscore[3]+=10 #셔츠3
      top_todayscore[4]+=10 #카라티4
      top_todayscore[7]+=5 #니트7
      bottom_todayscore[0]+=5 #청바지
      bottom_todayscore[1]+=10#슬랙스1
      bottom_todayscore[2]-=10#반바지2
      bottom_todayscore[3]-=10#트레이닝바지3
      shoes_todayscore[1]+=10 #운동화1
      shoes_todayscore[2]+=10 #구두2
      shoes_todayscore[0]-=10 #샌달


    #필터링 -> 뒤에서 그냥 -100점처리하는 게 나을듯
    if user_input_filter[0]==0: #봄
      outer_todayscore[6]-=1000
      top_todayscore[1]-=1000
      top_todayscore[0]-=1000
      bottom_todayscore[2]-=1000
      shoes_todayscore[0]-=1000
    if user_input_filter[0]==1: #여름
      top_todayscore[2]-=10
      top_todayscore[3]-=10
      top_todayscore[4]-=1000
      top_todayscore[5]-=1000
      top_todayscore[6]-=1000
      top_todayscore[7]-=1000
    if user_input_filter[0]==2: #가을
      outer_todayscore[6]-=1000
      top_todayscore[1]-=1000
      top_todayscore[0]-=1000
      bottom_todayscore[2]-=1000
      shoes_todayscore[0]-=1000
    if user_input_filter[0]==3: #겨울
      outer_todayscore[0]-=1000 #바람막이0 ~ 4
      outer_todayscore[1]-=1000
      outer_todayscore[2]-=1000
      outer_todayscore[3]-=1000
      outer_todayscore[4]-=1000
      top_todayscore[0]-=1000
      top_todayscore[1]-=1000
      bottom_todayscore[2]-=1000
      shoes_todayscore[0]-=1000

    if user_input_filter[1]==0: #남자
      top_todayscore[8]-=3000
      top_todayscore[0]-=100
      bottom_todayscore[4]-=3000
      shoes_todayscore[1]+=5


    fin_outer=[]
    fin_top=[]
    fin_bottom = []
    fin_shoes=[]

    outer_sorted = sorted(set(outer_todayscore), reverse=True)
    outer_sorted = outer_sorted[:3]
    for i  in range(3):
      for j in range(7):
        if outer_sorted[i] == outer_todayscore[j]:
          tmp_fin_outer.append(outer[j])
    tmp_fin_outer = tmp_fin_outer[:3]

    tfin_outer=[]
    tfin_top=[]
    tfin_bottom=[]
    #for k in range(len(date_lst)-1): 
    for ls in datelist_outer:
      tfin_outer.append(tmp_fin_outer[ls])
    for ls in datecollist:
      outer_col.append(trend_outer_col[ls])   

    #마지막socre상하의매치 : 우선순위 : (outer ->) top -> bottom , shoes: 운동화 default
    if user_input_filter[0]!=1: #outer있으면
      shoes_todayscore[0]-=100
      shoes_todayscore[1]+=10
      for i in range(3):
        if tfin_outer[i] == "windbreak jacket":
          top_todayscore[1]+=10
          top_todayscore[2]+=10
          bottom_todayscore[4]-=10
        if tfin_outer[i] == "blazer":
          top_todayscore[1]+=10
          top_todayscore[2]+=10
          top_todayscore[3]+=10
          bottom_todayscore[2]-=30
          bottom_todayscore[3]-=30
        if tfin_outer[i] == "denim jacket":
          top_todayscore[1]+=10
          top_todayscore[2]+=10
          top_todayscore[5]+=10
          top_todayscore[6]+=10
          top_todayscore[8]+=10
        if tfin_outer[i] == "leather jacket":
          top_todayscore[1]+=10
          top_todayscore[2]+=10
          top_todayscore[4]+=10
          top_todayscore[5]+=10
          top_todayscore[6]+=10
          bottom_todayscore[2]-=30
          bottom_todayscore[3]-=30
        if tfin_outer[i] == "coat":
          top_todayscore[3]+=10
          top_todayscore[4]+=10
          top_todayscore[5]+=10
          top_todayscore[6]+=15
          top_todayscore[7]+=15
        if tfin_outer[i] == "puffer":
          top_todayscore[5]+=15
          top_todayscore[6]+=10
          top_todayscore[7]+=10
        #수정



    top_sorted = sorted(set(top_todayscore), reverse=True)
    top_sorted = top_sorted[:3]
    for i  in range(3):
      for j in range(9):
        if top_sorted[i] == top_todayscore[j]:
          tmp_fin_top.append(top[j])
    tmp_fin_top = tmp_fin_top[:3]

    for ls in datelist_top:
      tfin_top.append(tmp_fin_top[ls])
    for ls in datecollist:
      top_col.append(trend_top_col[ls])



    for i in range(3):
      top_todayscore=top_todayscore
      bottom_todayscore=bottom_todayscore
      shoes_todayscore=shoes_todayscore
      if tfin_top[i] == "shirt":
        bottom_todayscore[3]-=100
        shoes_todayscore[0]-=100
      if tfin_top[i] == "knit sweater":
        bottom_todayscore[3]-=100
      if tfin_top[i] == "dress":
        tmp_fin_bottom.append("")
        fin_shoes.append(shoes_today[shoes_todayscore.index(max(shoes_todayscore))])
        continue

      #fin_bottom.append(bottom_today[bottom_todayscore.index(max(bottom_todayscore))])
      fin_shoes.append(shoes_today[shoes_todayscore.index(max(shoes_todayscore))])
    tmp_fin_bottom=[]
    tmp_fin_shoes=[]
    bottom_sorted = sorted(set(bottom_todayscore), reverse=True)
    bottom_sorted = bottom_sorted[:3]
    for i  in range(3):
      for j in range(5):
        if bottom_sorted[i] == bottom_todayscore[j]:
          tmp_fin_bottom.append(bottom[j])
    tmp_fin_bottom = tmp_fin_bottom[:2]
    tmp_fin_bottom.append(tmp_fin_bottom[0])

    #color
    for i  in range(3):
      for j in range(7):
        if outer_sorted[i] == outer_todayscore[j]:
          tmp_fin_outer.append(outer[j])
    tmp_fin_outer = tmp_fin_outer[:3]
    top_sorted = sorted(set(top_todayscore), reverse=True)
    top_sorted = top_sorted[:3]
    for i  in range(3):
      for j in range(9):
        if top_sorted[i] == top_todayscore[j]:
          tmp_fin_top.append(top[j])
    tmp_fin_top = tmp_fin_top[:3]

    p=0
    datelist_outer=[[0,1,2],[1,2,0],[2,0,1]]
    datelist_top=[[0,1,0],[0,0,1],[1,0,0]]
    datecollist=[[0,1,2],[1,2,0],[2,0,1]]
    for k in range(len(date_lst)): 
      for ls in datelist_outer[k]:
        fin_outer.append(tfin_outer[ls])
      for ls in datecollist[k]:
        outer_col.append(trend_outer_col[ls])
      for ls in datelist_top[k]:
        fin_top.append(tfin_top[ls])
      for ls in datecollist[k]:
        top_col.append(trend_top_col[ls])
      for i in range(3):
        fin_bottom.append(tmp_fin_bottom[i])
      for i in range(3):
        fin_shoes.append(fin_shoes[i])
        
    #color_bottom
    bottom_col=[]
    for i in range((len(date_lst))*3):
      if fin_bottom[i] == 'jeans':
        bottom_col.append('blue')
      if fin_bottom[i] == 'slacks':
        if outer_col[i] =='blue':
          bottom_col.append('gray')
        else:
          bottom_col.append('black')
      if fin_bottom[i] == 'sweat pants':
        if top_col[i] =='black':
          bottom_col.append('blue')
        if top_col[i]=='white' and outer_col[i]=='white':
          bottom_col.append('white')
        else:
          bottom_col.append('gray')
      if fin_bottom[i] == 'short pants':
        if top_col[i]=='white' and outer_col[i]=='white':
          bottom_col.append('white')
        else:
          bottom_col.append('blue')
      if fin_bottom[i] == 'skirt':
        if top_col[i]=='white' and outer_col[i]=='white':
          bottom_col.append('white')
        else:
          bottom_col.append('black')
      if fin_top[i] == "dress":
        bottom_col.insert(i," ")

    #color_shoes
    shoes_col=[]
    for da in range(len(date_lst)):
      for i in range(3):
        if fin_shoes[i]=='sandals':
          shoes_col.append('black')
        if fin_shoes[i] =='dress shoes':
          shoes_col.append('black')
        if fin_shoes[i] =='sneakers':
          if fin_bottom[i]=='slacks':
            shoes_col.append('black')
          else:
            shoes_col.append('white')



    import requests
    from bs4 import BeautifulSoup
    outer_adver_img=[]
    outer_adver_url=[]

    for i in range(3):
      if season ==1:
        outer_adver_img=['None','None','None','None','None','None','None','None','None']
        outer_adver_url=['None','None','None','None','None','None','None','None','None']
      else:
        search_query = f"{outer_col[i]} {fin_outer[i]}"
        search_url = f"https://www.musinsa.com/search/musinsa/integration?q={search_query}"
          # 웹 페이지 요청

        response = requests.get(search_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # 이미지 가져오기
            images = soup.find_all('img', class_='lazyload lazy')
            for i, image in enumerate(images[:3]):  # 첫 번째부터 세 번째 이미지 가져오기
                image_url = image['data-original']
                b=image_url[51:].find('/')
                url_n=image_url[45:51+b]
                url = f"https://www.musinsa.com/app/goods/{url_n}"
                outer_adver_img.append(f"https:{image_url}")
                outer_adver_url.append(f"{url}")

    top_adver_img=[]
    top_adver_url=[]

    for i in range(3):
      search_query = f"{top_col[i]} {fin_top[i]}"
      search_url = f"https://www.musinsa.com/search/musinsa/integration?q={search_query}"
      response = requests.get(search_url)
      if response.status_code == 200:
          soup = BeautifulSoup(response.text, 'html.parser')
          # 이미지 가져오기
          images = soup.find_all('img', class_='lazyload lazy')
          for i, image in enumerate(images[:3]):  # 첫 번째부터 세 번째 이미지 가져오기
              image_url = image['data-original']
              b=image_url[51:].find('/')
              url_n=image_url[45:51+b]
              url = f"https://www.musinsa.com/app/goods/{url_n}"
              top_adver_img.append(f"https:{image_url}")
              top_adver_url.append(f"{url}")
    bottom_adver_img=[]
    bottom_adver_url=[]

    for i in range(3*len(date_lst)):
      if fin_top[i]=='dress':
        bottom_adver_img.append('None')
        bottom_adver_img.append('None')
        bottom_adver_img.append('None')
        bottom_adver_url.append('None')
        bottom_adver_url.append('None')
        bottom_adver_url.append('None')
        bottom_col.append('')
      else:
        search_query = f"{bottom_col[i]} {fin_bottom[i]}"
        search_url = f"https://www.musinsa.com/search/musinsa/integration?q={search_query}"
        response = requests.get(search_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # 이미지 가져오기
            images = soup.find_all('img', class_='lazyload lazy')
            for i, image in enumerate(images[:3]):  # 첫 번째부터 세 번째 이미지 가져오기
                image_url = image['data-original']
                b=image_url[51:].find('/')
                url_n=image_url[45:51+b]
                url = f"https://www.musinsa.com/app/goods/{url_n}"
                bottom_adver_img.append(f"https:{image_url}")
                bottom_adver_url.append(f"{url}")

    shoes_adver_img=[]
    shoes_adver_url=[]
    for i in range(3*len(date_lst)):
      if fin_shoes[i]=='dress shoes': search_query = "검정 로퍼"
      else: search_query = f"{shoes_col[i]} {fin_shoes[i]}"
      search_url = f"https://www.musinsa.com/search/musinsa/integration?q={search_query}"
        # 웹 페이지 요청
      response = requests.get(search_url)
      if response.status_code == 200:
          soup = BeautifulSoup(response.text, 'html.parser')
          # 이미지 가져오기
          images = soup.find_all('img', class_='lazyload lazy')
          for i, image in enumerate(images[:3]):  # 첫 번째부터 세 번째 이미지 가져오기
              image_url = image['data-original']
              b=image_url[51:].find('/')
              url_n=image_url[45:51+b]
              url = f"https://www.musinsa.com/app/goods/{url_n}"
              shoes_adver_img.append(f"https:{image_url}")
              shoes_adver_url.append(f"{url}")

    exampleImg_outer=[]
    exampleImg_top=[]
    exampleImg_bottom=[]
    exampleImg_shoes=[]

    if season ==1:
        exampleImg_outer=["00'None'000","00'None'000","00'None'000"]
    else:
      for i in range(3*len(date_lst)):
        exampleClothes=fin_outer[i]
        exampleColor=outer_col[i]
        query=f"select exampleImage from EXAMPLE where exampleClothes='{exampleClothes}' and exampleColor='{exampleColor}' LIMIT 3;"
        cursor.execute(query)
        exampleimg = cursor.fetchall()
        exampleImg_outer.append(exampleimg)

    for i in range(3*len(date_lst)):
      exampleClothes=fin_top[i]
      exampleColor=top_col[i]
      query=f"select exampleImage from EXAMPLE where exampleClothes='{exampleClothes}' and exampleColor='{exampleColor}' LIMIT 3;"
      cursor.execute(query)
      exampleimg = cursor.fetchall()
      exampleImg_top.append(exampleimg)

    for i in range(3*len(date_lst)):
      if fin_top[i]=='dress':
        exampleImg_bottom.append("00'None'000")
      else:
        exampleClothes=fin_bottom[i]
        exampleColor=bottom_col[i]
        query=f"select exampleImage from EXAMPLE where exampleClothes='{exampleClothes}' and exampleColor='{exampleColor}' LIMIT 3;"
        cursor.execute(query)
        exampleimg = cursor.fetchall()
        exampleImg_bottom.append(exampleimg)
 

      exampleClothes=fin_shoes[i]
      exampleColor=shoes_col[i]
      query=f"select exampleImage from EXAMPLE where exampleClothes='{exampleClothes}' and exampleColor='{exampleColor}' LIMIT 3;"
      cursor.execute(query)
      exampleimg = cursor.fetchall()
      exampleImg_shoes.append(exampleimg)



    #closet

    outer_closet=[]
    top_closet=[]
    bottom_closet=[]
    shoes_closet=[]
    test="'https://postfiles.pstatic.net/MjAyMzEwMDFfNjIg/MDAxNjk2MTYzMzcxMjc2.oVup_aS64ZNVcQnNnkmev1v1hFJSFyXTAv243hyRa1kg.QM5VNyfuGV_gZCTzZUp8SrP2XzMbjnruGZjW9zkU3Eog.PNG.pineapple7358/%EC%8A%A4%ED%81%AC%EB%A6%B0%EC%83%B7_2023-10-01_%EC%98%A4%ED%9B%84_9.29.27.png?type=w966'"

    for i in range(3):
      if season ==1:
        outer_closet=["'None'","'None'","'None'","'None'","'None'","'None'","'None'","'None'","'None'"]
      else:
        outercloset=fin_outer[i]
        outercolcloset=outer_col[i]
        query=f"select clothesImg from CLOSET where clothesTag='{outercloset}' and clothesColor='{outercolcloset}' and usrId='{usr_Id}' limit 3;"
        cursor.execute(query)
        exampleimg = cursor.fetchall()

        if len(exampleimg)==0:
          outer_closet.append(test)
          outer_closet.append(test)
          outer_closet.append(test)
        elif len(exampleimg)==1:
          outer_closet.append(str(exampleimg[0])[1:-2])
          outer_closet.append(test)
          outer_closet.append(test)
        elif len(exampleimg)==2:
          outer_closet.append(str(exampleimg[0])[1:-2])
          outer_closet.append(str(exampleimg[1])[1:-2])
          outer_closet.append(test)
        elif len(exampleimg)==3:
          outer_closet.append(str(exampleimg[0])[1:-2])
          outer_closet.append(str(exampleimg[1])[1:-2])
          outer_closet.append(str(exampleimg[2])[1:-2])

    for i in range(3):
      topcloset=fin_top[i]
      topcolcloset=top_col[i]
      query=f"select clothesImg from CLOSET where clothesTag='{topcloset}' and clothesColor='{topcolcloset}' and usrId='{usr_Id}' limit 3;"
      cursor.execute(query)
      exampleimg = cursor.fetchall()

      if len(exampleimg)==0:
        top_closet.append(test)
        top_closet.append(test)
        top_closet.append(test)
      elif len(exampleimg)==1:
        top_closet.append(str(exampleimg[0])[1:-2])
        top_closet.append(test)
        top_closet.append(test)
      elif len(exampleimg)==2:
        top_closet.append(str(exampleimg[0])[1:-2])
        top_closet.append(str(exampleimg[1])[1:-2])
        top_closet.append(test)
      elif len(exampleimg)==3:
        top_closet.append(str(exampleimg[0])[1:-2])
        top_closet.append(str(exampleimg[1])[1:-2])
        top_closet.append(str(exampleimg[2])[1:-2])


      for i in range(3):
        if fin_top[i]=='dress':
          bottom_closet.append("'None'")
          bottom_closet.append("'None'")
          bottom_closet.append("'None'")
        else:
          bottomcloset=fin_bottom[i]
          bottomcolcloset=bottom_col[i]
          query=f"select clothesImg from CLOSET where clothesTag='{bottomcloset}' and clothesColor='{bottomcolcloset}' and usrId='{usr_Id}' limit 3;"
          cursor.execute(query)
          exampleimg = cursor.fetchall()
          if len(exampleimg)==0:
            bottom_closet.append(test)
            bottom_closet.append(test)
            bottom_closet.append(test)
          elif len(exampleimg)==1:
            bottom_closet.append(str(exampleimg[0])[1:-2])
            bottom_closet.append(test)
            bottom_closet.append(test)
          elif len(exampleimg)==2:
            bottom_closet.append(str(exampleimg[0])[1:-2])
            bottom_closet.append(str(exampleimg[1])[1:-2])
            bottom_closet.append(test)
          elif len(exampleimg)==3:
            bottom_closet.append(str(exampleimg[0])[1:-2])
            bottom_closet.append(str(exampleimg[1])[1:-2])
            bottom_closet.append(str(exampleimg[2])[1:-2])

      for i in range(3):
        shoescloset=fin_shoes[i]
        shoescolcloset=shoes_col[i]
        query=f"select clothesImg from CLOSET where clothesTag='{shoescloset}' and clothesColor='{shoescolcloset}' and usrId='{usr_Id}' limit 3;"
        cursor.execute(query)
        exampleimg = cursor.fetchall()
        if len(exampleimg)==0:
          shoes_closet.append(test)
          shoes_closet.append(test)
          shoes_closet.append(test)
        elif len(exampleimg)==1:
          shoes_closet.append(str(exampleimg[0])[1:-2])
          shoes_closet.append(test)
          shoes_closet.append(test)
        elif len(exampleimg)==2:
          shoes_closet.append(str(exampleimg[0])[1:-2])
          shoes_closet.append(str(exampleimg[1])[1:-2])
          shoes_closet.append(test)
        elif len(exampleimg)==3:
          shoes_closet.append(str(exampleimg[0])[1:-2])
          shoes_closet.append(str(exampleimg[1])[1:-2])
          shoes_closet.append(str(exampleimg[2])[1:-2])

    if d==0:
      fin_return_new=[]
    else:
      fin_return+=","
    
    fin_return_new=f"""
      ^
          'date': '{date}',
          'clothes': [
              ^
                  'outter': ^
                      'img': {str(exampleImg_outer[0])[2:-3]},
                      'detail':^
                          'commercial':[
                              ^
                                  'img': '{outer_adver_img[0]}',
                                  'link': '{outer_adver_url[0]}'
                              #,
                              ^
                                  'img': '{outer_adver_img[1]}',
                                  'link': '{outer_adver_url[1]}'
                              #,
                              ^
                                  'img': '{outer_adver_img[2]}',
                                  'link': '{outer_adver_url[2]}'
                              #
                          ],
                          'closet':[
                              ^
                                  'img': {outer_closet[0]}
                              #,
                              ^
                                  'img': {outer_closet[1]}
                              #,
                              ^
                                  'img': {outer_closet[2]}
                              #
                          ]
                      #

                  #,
                  'top': ^
                      'img': {str(exampleImg_top[0])[2:-3]},
                      'detail':^
                          'commercial':[
                              ^
                                  'img': '{top_adver_img[0]}',
                                  'link': '{top_adver_url[0]}'
                              #,
                              ^
                                  'img': '{top_adver_img[1]}',
                                  'link': '{top_adver_url[1]}'
                              #,
                              ^
                                  'img': '{top_adver_img[2]}',
                                  'link': '{top_adver_url[2]}'
                              #
                          ],
                          'closet':[
                              ^
                                  'img': {top_closet[0]}
                              #,
                              ^
                                  'img': {top_closet[1]}
                              #,
                              ^
                                  'img': {top_closet[2]}
                              #
                          ]
                      #
                  #,
                  'bottom': ^
                      'img': {str(exampleImg_bottom[0])[2:-3]},
                      'detail':^
                          'commercial':[
                              ^
                                  'img': '{bottom_adver_img[0]}',
                                  'link': '{bottom_adver_url[0]}'
                              #,
                              ^
                                  'img': '{bottom_adver_img[1]}',
                                  'link': '{bottom_adver_url[1]}'
                              #,
                              ^
                                  'img': '{bottom_adver_img[2]}',
                                  'link': '{bottom_adver_url[2]}'
                              #
                          ],
                          'closet':[
                              ^
                                  'img': {bottom_closet[0]}
                              #,
                              ^
                                  'img': {bottom_closet[1]}
                              #,
                              ^
                                  'img': {bottom_closet[2]}
                              #
                          ]
                      #
                  #,
                  'shoes': ^
                      'img': {str(exampleImg_shoes[0])[2:-3]},
                      'detail':^
                          'commercial':[
                              ^
                                  'img': '{shoes_adver_img[0]}',
                                  'link': '{shoes_adver_url[0]}'
                              #,
                              ^
                                  'img': '{shoes_adver_img[1]}',
                                  'link': '{shoes_adver_url[1]}'
                              #,
                              ^
                                  'img': '{shoes_adver_img[2]}',
                                  'link': '{shoes_adver_url[2]}'
                              #
                          ],
                          'closet':[
                              ^
                                  'img': {shoes_closet[0]}
                              #,
                              ^
                                  'img': {shoes_closet[1]}
                              #,
                              ^
                                  'img': {shoes_closet[2]}
                              #
                          ]
                      #
                  #
              #,
                ^
                  'outter': ^
                      'img': {str(exampleImg_outer[1])[2:-3]},
                      'detail':^
                          'commercial':[
                              ^
                                  'img': '{outer_adver_img[3]}',
                                  'link': '{outer_adver_url[3]}'
                              #,
                              ^
                                  'img': '{outer_adver_img[4]}',
                                  'link': '{outer_adver_url[4]}'
                              #,
                              ^
                                  'img': '{outer_adver_img[5]}',
                                  'link': '{outer_adver_url[5]}'
                              #
                          ],
                          'closet':[
                              ^
                                  'img': {outer_closet[3]}
                              #,
                              ^
                                  'img': {outer_closet[4]}
                              #,
                              ^
                                  'img': {outer_closet[5]}
                              #
                          ]
                      #

                  #,
                  'top': ^
                      'img': {str(exampleImg_top[1])[2:-3]},
                      'detail':^
                          'commercial':[
                              ^
                                  'img': '{top_adver_img[3]}',
                                  'link': '{top_adver_url[4]}'
                              #,
                              ^
                                  'img': '{top_adver_img[4]}',
                                  'link': '{top_adver_url[4]}'
                              #,
                              ^
                                  'img': '{top_adver_img[5]}',
                                  'link': '{top_adver_url[5]}'
                              #
                          ],
                          'closet':[
                              ^
                                  'img': {top_closet[3]}
                              #,
                              ^
                                  'img': {top_closet[4]}
                              #,
                              ^
                                  'img': {top_closet[5]}
                              #
                          ]
                      #
                  #,
                  'bottom': ^
                      'img': {str(exampleImg_bottom[1])[2:-3]},
                      'detail':^
                          'commercial':[
                              ^
                                  'img': '{bottom_adver_img[3]}',
                                  'link': '{bottom_adver_url[3]}'
                              #,
                              ^
                                  'img': '{bottom_adver_img[4]}',
                                  'link': '{bottom_adver_url[4]}'
                              #,
                              ^
                                  'img': '{bottom_adver_img[5]}',
                                  'link': '{bottom_adver_url[5]}'
                              #
                          ],
                          'closet':[
                              ^
                                  'img': {bottom_closet[3]}
                              #,
                              ^
                                  'img': {bottom_closet[4]}
                              #,
                              ^
                                  'img': {bottom_closet[5]}
                              #
                          ]
                      #
                  #,
                  'shoes': ^
                      'img': {str(exampleImg_shoes[1])[2:-3]},
                      'detail':^
                          'commercial':[
                              ^
                                  'img': '{shoes_adver_img[3]}',
                                  'link': '{shoes_adver_url[3]}'
                              #,
                              ^
                                  'img': '{shoes_adver_img[4]}',
                                  'link': '{shoes_adver_url[4]}'
                              #,
                              ^
                                  'img': '{shoes_adver_img[5]}',
                                  'link': '{shoes_adver_url[5]}'
                              #
                          ],
                          'closet':[
                              ^
                                  'img': {shoes_closet[3]}
                              #,
                              ^
                                  'img': {shoes_closet[4]}
                              #,
                              ^
                                  'img': {shoes_closet[5]}
                              #
                          ]
                      #
                  #
              #,
                ^
                  'outter': ^
                      'img': {str(exampleImg_outer[2])[2:-3]},
                      'detail':^
                          'commercial':[
                              ^
                                  'img': '{outer_adver_img[6]}',
                                  'link': '{outer_adver_url[6]}'
                              #,
                              ^
                                  'img': '{outer_adver_img[7]}',
                                  'link': '{outer_adver_url[7]}'
                              #,
                              ^
                                  'img': '{outer_adver_img[8]}',
                                  'link': '{outer_adver_url[8]}'
                              #
                          ],
                          'closet':[
                              ^
                                  'img': {outer_closet[6]}
                              #,
                              ^
                                  'img': {outer_closet[7]}
                              #,
                              ^
                                  'img': {outer_closet[8]}
                              #
                          ]
                      #

                  #,
                  'top': ^
                      'img': {str(exampleImg_top[2])[2:-3]},
                      'detail':^
                          'commercial':[
                              ^
                                  'img': '{top_adver_img[6]}',
                                  'link': '{top_adver_url[6]}'
                              #,
                              ^
                                  'img': '{top_adver_img[7]}',
                                  'link': '{top_adver_url[7]}'
                              #,
                              ^
                                  'img': '{top_adver_img[8]}',
                                  'link': '{top_adver_url[8]}'
                              #
                          ],
                          'closet':[
                              ^
                                  'img': {top_closet[6]}
                              #,
                              ^
                                  'img': {top_closet[7]}
                              #,
                              ^
                                  'img': {top_closet[8]}
                              #
                          ]
                      #
                  #,
                  'bottom': ^
                      'img': {str(exampleImg_bottom[2])[2:-3]},
                      'detail':^
                          'commercial':[
                              ^
                                  'img': '{bottom_adver_img[6]}',
                                  'link': '{bottom_adver_url[6]}'
                              #,
                              ^
                                  'img': '{bottom_adver_img[7]}',
                                  'link': '{bottom_adver_url[7]}'
                              #,
                              ^
                                  'img': '{bottom_adver_img[8]}',
                                  'link': '{bottom_adver_url[8]}'
                              #
                          ],
                          'closet':[
                              ^
                                  'img': {bottom_closet[6]}
                              #,
                              ^
                                  'img': {bottom_closet[7]}
                              #,
                              ^
                                  'img': {bottom_closet[8]}
                              #
                          ]
                      #
                  #,
                  'shoes': ^
                      'img': {str(exampleImg_shoes[2])[2:-3]},
                      'detail':^
                          'commercial':[
                              ^
                                  'img': '{shoes_adver_img[6]}',
                                  'link': '{shoes_adver_url[6]}'
                              #,
                              ^
                                  'img': '{shoes_adver_img[7]}',
                                  'link': '{shoes_adver_url[7]}'
                              #,
                              ^
                                  'img': '{shoes_adver_img[8]}',
                                  'link': '{shoes_adver_url[8]}'
                              #
                          ],
                          'closet':[
                              ^
                                  'img': {shoes_closet[6]}
                              #,
                              ^
                                  'img': {shoes_closet[7]}
                              #,
                              ^
                                  'img': {shoes_closet[8]}
                              #
                          ]
                      #
                  #
              #
          ]
    #
    """
    fin_return_new = fin_return_new.replace("^","{")
    fin_return_new = fin_return_new.replace("#","}")
    fin_return_new = fin_return_new.replace("'",'"')
    fin_return_mew.append(fin_return_new)
    fin_return = fin_return+fin_return_new
  #return [fin_outer,fin_top, fin_bottom, fin_shoes,outer_col,top_col,bottom_col,shoes_col,outer_adver_img,outer_adver_url,top_adver_img, top_adver_url,bottom_adver_img,bottom_adver_url,shoes_adver_img,shoes_adver_url,exampleImg_outer,exampleImg_top, exampleImg_bottom, exampleImg_shoes,closet_outer,closet_top,closet_bottom,closet_shoes]
  #3일 이상일때

  if len(date_lst_origin)>3:
    for i in range(3,len(date_lst_origin)):
      tmp=f'\n          "date": "{date_origin[i]}"'
      fin_return=fin_return+","+"{"+tmp+fin_return_mew[i-3][39:]
      #print(fin_return_mew[i-3][39:])
  fin_return = "["+fin_return+"\n]"

  return fin_return

import sys
import base64
import json
if __name__ == '__main__':
  #python3 recommend.py admin [ '2023-10-10', '2023-10-11'] 가을 M 배낭여행 핫플레이스
  func=recomm_func(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])


  #print(func)
  # JSON 형식으로 파싱
  parsed_data = json.loads(func)
  # 다시 JSON 형식으로 인코딩
  json_data = json.dumps(parsed_data, indent=4)

  bytes_data = func.encode('utf-8')

  encoded_data = base64.b64encode(bytes_data)

  encoded_string = encoded_data.decode('utf-8')

  print(encoded_string)
