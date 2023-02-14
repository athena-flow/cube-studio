import base64
import io,sys,os

from cubestudio.aihub.model import Model
from cubestudio.aihub.web.server import Server,Field,Field_type
import json
import pysnooper
from darknetpy.detector import Detector
from PIL import ImageGrab, Image
from PIL import Image,ImageFont
from PIL import ImageDraw
import numpy

import os
myfont = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc', 20)

class Yolov3_Model(Model):
    # 模型基础信息定义
    name='yolov3'
    label='目标识别'
    describe="darknet yolov3 目标识别"
    field="机器视觉"
    scenes="目标识别"
    status='online'
    version='v20221001'
    doc='https://github.com/tencentmusic/cube-studio/tree/master/aihub/deep-learning/yolov3'
    pic='example.jpg'

    inference_inputs = [
        Field(type=Field_type.image, name='img_file_path', label='待识别图片', describe='用于目标识别的原始图片')
    ]
    web_examples = [
        {
            "label": "示例1",
            "input": {
                "img_file_path":"test.jpg"
            }
        }
    ]

    # 加载模型
    def load_model(self):
        self.detector = Detector('/yolo/coco.data', '/yolo/yolov3.cfg', '/yolo/yolov3.weights')

    # 推理
    @pysnooper.snoop()
    def inference(self,img_file_path):
        res = self.detector.detect(img_file_path)

        img = Image.open(img_file_path)
        dr = ImageDraw.Draw(img)
        for data in res:
            class_name = data['class']
            x, y, w, h = data['left'], data['top'], data['right'] - data['left'], data['bottom'] - data['top']
            # 画矩形框
            dr.rectangle((x, y, x + w, y + h), outline=(46, 254, 46), width=3)
            dr.text((data['left'], data['top']), class_name, font=myfont, fill='red')

        out_image_path = os.path.join('result',os.path.basename(img_file_path))
        os.makedirs('result', exist_ok=True)
        img.save(out_image_path)
        print(res)
        back=[{
            "image":out_image_path,
            # "text":json.dumps(res,indent=4,ensure_ascii=False)
        }]
        return back

model=Yolov3_Model()
# model.load_model()
# result = model.inference(img_file_path='test.jpg')  # 测试
# print(result)

# # 启动服务
server = Server(model=model)
server.server(port=8080)

