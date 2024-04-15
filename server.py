from flask import Flask,request,jsonify
import datetime
from urllib.parse import urlparse

import pymysql
import os
import requests
import json
import logging
logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger('get_scales')
logger.setLevel(logging.INFO)

# 创建文件处理器并设置级别
fh = logging.FileHandler('get_scales.log')
fh.setLevel(logging.INFO)

# 创建formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# 添加formatter到fh
fh.setFormatter(formatter)

# 添加fh到logger
logger.addHandler(fh)

app = Flask(__name__)
nowdate = datetime.datetime.now().date()

@app.route('/photo', methods = ["POST"])
def photo():
    image_urls = request.json['imageUrls']
    print(image_urls)
    if not os.path.exists('images'):
        os.makedirs('images')

    for image_url in image_urls:
        image_content = requests.get(image_url).content
        image_name = os.path.basename(urlparse(image_url).path)
        with open(os.path.join('images', image_name), 'wb') as image_file:
            image_file.write(image_content)

    return jsonify({'message': 'Images downloaded'})
    
    return jsonify({"message": "succeed update rank"})
 
 

if __name__ == '__main__':
    app.run(host = '0.0.0.0',port='2007', debug= True)
    
