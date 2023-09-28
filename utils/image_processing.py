import numpy as np
from PIL import Image
import extcolors
import numpy as np
import io
import base64
import cv2

outter = ['blazer', 'denim jacket', 'leather jacket', 'coat', 'windbreaker jacket', "cardigan", "puffer"]
top = ["tee shirt", "long sleeve shirt", "tank top", "shirt", "polo shirt", "sweat shirt", "hoodie sweat shirt", "knit sweater", "dress"]
bottom = [ "jeans", "slacks", "sweat pants", "skirt", "shorts pants",]
shoes = ["sneakers", "dress shoes", "sandals"]
        
        
def base64_list_to_image(base64_list):
    image_list = []
    for base64_each in base64_list:
        request = str.encode(base64_each)
        request = base64.b64decode(request)
        request = Image.open(io.BytesIO(request))
        request = np.array(request)
        request = cv2.cvtColor(request, cv2.COLOR_BGR2RGB)
        image_list.append(request)
    return image_list
        
        
def get_image_color(image):
    colors, pixel_count = extcolors.extract_from_image(image)
    best_color = colors[0][0]
    primary_colors = [(255,255,255), (235,211,176), (0,0,255), (128,128,128), (0,0,0)] 
    
    min_dist=10000
    min_color=0
    for i, primary_color in enumerate(primary_colors):
        dist = np.linalg.norm(np.array(best_color)-np.array(primary_color))
        if dist < min_dist:
            min_dist = dist
            min_color = i

    return min_color 


def get_combi(combi):
    best_outter = ['', 0, 0]
    best_top = ['', 0, 0]
    best_bottom = ['', 0, 0]
    best_shoes = ['', 0, 0]
    
    for l, s, c in combi:
        if l in outter:
            if best_outter[1] < s:
                best_outter[0] = l
                best_outter[1] = s
                best_outter[2] = c
        elif l in top:
            if best_top[1] < s:
                best_top[0] = l
                best_top[1] = s
                best_top[2] = c
        elif l in bottom:
            if best_bottom[1] < s:
                best_bottom[0] = l
                best_bottom[1] = s
                best_bottom[2] = c
        elif l in shoes:
            if best_shoes[1] < s:
                best_shoes[0] = l
                best_shoes[1] = s
                best_shoes[2] = c
    
    return [best_outter[0], best_top[0], best_bottom[0], best_shoes[0]], [best_outter[2], best_top[2], best_bottom[2], best_shoes[2]]
          

def from_image_to_bytes(img):
    imgByteArr = io.BytesIO() # Pillow 이미지 객체를 Bytes로 변환
    img.save(imgByteArr, format=img.format)
    imgByteArr = imgByteArr.getvalue() # Base64로 Bytes를 인코딩
    encoded = base64.b64encode(imgByteArr)
    decoded = encoded.decode('ascii') # Base64로 ascii로 디코딩
    return decoded
      
        
def get_batch_info(images, boxes, labels, scores):
    crop_list = []
    label_list = []
    color_list = []
    combi_list = []
    combi_color_list = []
    categori_list = []
    
    for image, box, label, score in zip(images, boxes, labels, scores):
        pil_image=Image.fromarray(image)
        combi = []
        
        for b, l, s in zip(box, label, score):
            cropped_image = pil_image.crop(b)
            crop_list.append(cropped_image)
            label_list.append(l)
            c = get_image_color(cropped_image)
            color_list.append(c)
            combi.append([l, s, c])
            
            if l in outter:
                categori = 'outter'
            elif l in top:
                categori = 'top'
            elif l in bottom:
                categori = 'bottom'
            elif l in shoes:
                categori = 'shoes'
            categori_list.append(categori)
        
        combi_clothes, combi_color = get_combi(combi)
        combi_list.append(combi_clothes)
        combi_color_list.append(combi_color)
        
    return crop_list, label_list, color_list, categori_list, combi_list, combi_color_list


def get_camera_info(images, boxes, labels, scores):
    best_score = 0.0
    
    for image, box, label, score in zip(images, boxes, labels, scores):
        pil_image=Image.fromarray(image)
        for b, l, s in zip(box, label, score):
            if s > best_score:
                best_label = l
                cropped_image = pil_image.crop(b)
                best_color = get_image_color(cropped_image)
                            
    return best_label, best_color