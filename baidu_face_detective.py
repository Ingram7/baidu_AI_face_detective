
import base64
import requests
import os
import time

def get_token(api_key,secret_key):
    # 获取token
    URL = "https://aip.baidubce.com/oauth/2.0/token"
    params = {
        "grant_type": "client_credentials",
        "client_id": api_key,
        "client_secret": secret_key
    }
    s = requests.post(URL, data=params)
    token = s.json().get('access_token')
    return token



def face_detective(image_path, token):
    # 人脸检测
    URL = "https://aip.baidubce.com/rest/2.0/face/v3/detect"

    with open(image_path, 'rb') as fp:
        image_base64 = base64.b64encode(fp.read())

    params = {
        "face_field": "age,gender,beauty,qualities",
        "image_type": "BASE64",
        "image": image_base64,
    }

    url = URL + "?access_token=" + token
    response = requests.post(url, data=params)

    r = response.json().get('result')
    print(r)
    return r


def process_face_data(r):
    # 筛选美女
    if r is None or r["face_num"] != 1:
        return []

    else:
        face = r["face_list"][0]
        if face["face_probability"] > 0.7 and face["beauty"] > 70 and face["gender"]["type"] == "female":
            score = face["beauty"]
            return score


if __name__ == '__main__':
    # 百度AI 申请信息   API Key, Secret Key
    API_KEY = "xKyCOwVbU9Un7***************"
    SECRET_KEY = "NgImdvGV7ldd7****************"


    file_path = 'image'

    for image_name_one in os.listdir(file_path):
        # 人脸检测API  有QPS限制  不能请求太快了
        time.sleep(1)
        image_path = os.path.join(file_path, image_name_one)
        try:
            token = get_token(API_KEY, SECRET_KEY)
            data = face_detective(image_path, token)
            result = process_face_data(data)
            result = int(result)

            if result:
                os.rename(image_path, os.path.join(file_path, str(result) + 'II' + image_name_one))
            else:
                os.remove(image_path)

        except Exception as e:
            print('Error:', e)
