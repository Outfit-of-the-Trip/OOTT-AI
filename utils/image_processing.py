import numpy as np
from PIL import Image
import extcolors
import numpy as np
import io
import base64

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
    outter = ['blazer', 'denim jacket', 'leather jacket', 'coat', 'windbreaker jacket', "cardigan", "puffer"]
    top = ["tee shirt", "long sleeve shirt", "tank top", "shirt", "polo shirt", "sweat shirt", "hoodie sweat shirt", "knit sweater", "dress"]
    bottom = [ "jeans", "slacks", "sweat pants", "skirt", "shorts pants",]
    shoes = ["sneakers", "dress shoes", "sandals"]
    best_outter = ['', 0]
    best_top = ['', 0]
    best_bottom = ['', 0]
    best_shoes = ['', 0]
    
    for l, s in combi:
        if l in outter:
            if best_outter[1] < s:
                best_outter[0] = l
                best_outter[1] = s
        elif l in top:
            if best_top[1] < s:
                best_top[0] = l
                best_top[1] = s
        elif l in bottom:
            if best_bottom[1] < s:
                best_bottom[0] = l
                best_bottom[1] = s
        elif l in shoes:
            if best_shoes[1] < s:
                best_shoes[0] = l
                best_shoes[1] = s
    
    return [best_outter[0], best_top[0], best_bottom[0], best_shoes[0]]
                
        
def get_image_info(images, boxes, labels, scores):
    crop_list = []
    label_list = []
    color_list = []
    combi_list = []
    
    for image, box, label, score in zip(images, boxes, labels, scores):
        pil_image=Image.fromarray(image)
        combi = []
        for b, l, s in zip(box, label, score):
            cropped_image = pil_image.crop(b)
            crop_list.append(cropped_image)
            label_list.append(l)
            color_list.append(get_image_color(cropped_image))
            combi.append([l, s])
        combi_list.append(get_combi(combi))
        
    return crop_list, label_list, color_list, combi_list


def from_image_to_bytes(img):
    imgByteArr = io.BytesIO() # Pillow 이미지 객체를 Bytes로 변환
    img.save(imgByteArr, format=img.format)
    imgByteArr = imgByteArr.getvalue() # Base64로 Bytes를 인코딩
    encoded = base64.b64encode(imgByteArr)
    decoded = encoded.decode('ascii') # Base64로 ascii로 디코딩
    return decoded