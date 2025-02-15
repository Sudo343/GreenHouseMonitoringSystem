import os
from keras.models import model_from_json
import cv2
from keras.preprocessing.image import img_to_array
import numpy as np
import json
import base64
import re

maps = ['Pepper__bell___Bacterial_spot','Pepper__bell___healthy','Potato___Early_blight', 'Potato___Late_blight',
        'Potato___healthy', 'Tomato_Bacterial_spot', 'Tomato_Early_blight', 'Tomato_Late_blight','Tomato_Leaf_Mold', 
        'Tomato_Septoria_leaf_spot','Tomato_Spider_mites_Two_spotted_spider_mite','Tomato__Target_Spot',
         'Tomato__Tomato_YellowLeaf__Curl_Virus', 'Tomato__Tomato_mosaic_virus','Tomato_healthy']


class prediction():
    def __init__(self):
        
        json_file = open('crop_model.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()

        self.model = model_from_json(loaded_model_json)
        self.model.load_weights("model.h5")
        
        
    def convert_image_to_array(self,image_dir):
        image = cv2.imread(image_dir)
        if image is not None:
            image = cv2.resize(image, (256,256))   
            return img_to_array(image)
        else:
            return np.array([])

    def parseImage(self,imgData):
        imgstr = re.search(b'base64,(.*)', imgData).group(1)
        with open('output.png','wb') as output:
            output.write(base64.decodebytes(imgstr))
        
    def predict(self, imgData):
        imgData = self.parseImage(imgData)
        image = self.convert_image_to_array("output.png")/255.0
        image = np.expand_dims(image, axis=0)
        
        result = self.model.predict(image)
        result = np.argmax(result, axis=1)
        
        return json.dumps(maps[result[0]])




#imageData = "#############"

#obj = prediction()
#print(obj.predict(imageData))


