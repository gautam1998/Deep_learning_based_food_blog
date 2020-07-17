from flask import Flask,Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import login_user,logout_user,login_required
import hashlib
import base64
import binascii
import json
import datetime
from pathlib import Path
from pymongo import MongoClient
import requests
import numpy as np
import tensorflow as tf
graph= tf.get_default_graph()
from keras.applications.resnet50 import ResNet50, preprocess_input, decode_predictions
from keras.preprocessing.image import load_img, img_to_array
from flask_cors import CORS


import requests

app = Flask(__name__)
CORS(app)
model = ResNet50(include_top=True, weights='imagenet')
def compute(tag):
    
    
    tag=request.args.get('image') 

    myimages = []
    myimages.append(tag)
    images = []
    
    for ii in myimages:
        images.append(load_img(ii, target_size=(224,224)))
    
    for y in range(len(images)):
        images[y] = img_to_array(images[y])
        x = np.expand_dims(images[y], axis=0)
        x = preprocess_input(x)
        with graph.as_default():
            
             yhat = model.predict(x)
        return yhat

    
@app.route('/<tag>', methods = ['GET'])
def gentag(tag):
    l=compute(tag)
    label_t = decode_predictions(l)
    label = label_t[0][0]
    a=label[1]
    l=[]
    l.append(a)
    response = app.response_class(response=json.dumps(l), status=200, mimetype='application/json')
    return response 

if __name__ == '__main__':
   app.run(host='localhost',port="5000")
    