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
from flask_cors import CORS


import requests

app = Flask(__name__)
CORS(app)

import os

def file_is_empty(path):
    if(os.stat(path).st_size==0):
      return 1
    else:
      return 0
myclient = MongoClient("mongodb://localhost:27017/")
mydb = myclient["WebTech"]

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/login')
def login():
  return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/logout',methods = ['GET'])
#@login_required
def logout():
  open("user.txt","w").close()
  return render_template('login.html')

@app.route('/profile')
def profile():
    if(file_is_empty("user.txt")):
      return render_template('login.html')
    else:
      return render_template('profile.html')


@app.route('/upload')
def upload():
    if(file_is_empty("user.txt")):
      return render_template('login.html')
    else:
      return render_template('upload.html')  


@app.route('/explore')
def explore():
    if(file_is_empty("user.txt")):
      return render_template('login.html')
    else:
      return render_template('explore.html')  
             
@app.route('/return_user', methods = ['GET'])
def ret_user():
    fd=open("user.txt","r")
    fd.seek(0)
    l=fd.readlines()
    l=l[0].rstrip("\n")
    fd.close()    
    l=[l]
    response = app.response_class(response=json.dumps(l), status=200, mimetype='application/json')
    return response     

@app.route('/verifyPassword', methods = ['GET'])
def verify_password():

    if request.method!='GET':
      response = app.response_class(response=json.dumps({}), status=405, mimetype='application/json')
      return response
    email=request.args.get('username')
    password=request.args.get('password')
    mycol = mydb["Users"]
    for x in mycol.find({} ,{"_id": 0, "username":1, "email_id": 1, "password": 1}):
        if(x["email_id"]==email):
          if(x["password"]==password):

            fd=open("user.txt","w")
            fd.seek(0)
            fd.write(x["username"])
            fd.close()
            response = app.response_class(response=json.dumps({}), status=200, mimetype='application/json')
            return response

    response = app.response_class(response=json.dumps({}), status=400, mimetype='application/json')
    return response 
    
@app.route('/gentag', methods = ['GET'])
def gentag():
    tag=request.args.get('image') 
    r = requests.get('http://127.0.0.1:5000/'+str(tag))
    
    response = app.response_class(response=json.dumps(r.json()), status=200, mimetype='application/json')
    return response  

@app.route('/signout', methods = ['POST'])
def signout():
    open('user.txt', 'w').close() 
    response = app.response_class(response=json.dumps({}), status=200, mimetype='application/json')
    return response     

@app.route('/addUsers', methods = ['POST'])
def add_Users():
    if request.method!='POST':
      response = app.response_class(response=json.dumps({}), status=405, mimetype='application/json')
      return response     
    fd=open("signup.txt","w")
    fd.seek(0)
    fd.write("a")
    fd.close()    
    mycol = mydb["Users"]
    content = request.get_json()
    mycol.insert_one(content)
    response = app.response_class(response=json.dumps({}), status=200, mimetype='application/json')
    
    return response

    
@app.route('/suggest', methods = ['GET'])
def suggest():
    if request.method!='GET':
      response = app.response_class(response=json.dumps({}), status=405, mimetype='application/json')
      return response    
    username=request.args.get('term')  
    mycol = mydb["Users"]
    myquery = { "username": { "$regex": username } }
    mydoc = mycol.find(myquery)
    l=[]
    for x in mydoc:
        l.append(x["username"])                     
    response = app.response_class(response=json.dumps(l), status=200, mimetype='application/json')
    return response

@app.route('/listPosts', methods = ['GET'])
def listPosts():
    if request.method!='GET':
      response = app.response_class(response=json.dumps({}), status=405, mimetype='application/json')
      return response    
    username=request.args.get('term')  
    mycol = mydb["User_Posts"]
    l=[]
    for x in mycol.find({} ,{"_id": 0, "username": 1, "email_id": 1, "title": 1, "caption": 1,"image":1,
                        "comment":1,"tag":1}): 
        if(x["username"]==username):
          
          l.append(x)
    
    if(len(l)==0):
       response = app.response_class(response=json.dumps({}), status=400, mimetype='application/json')
       return response
    response = app.response_class(response=json.dumps(l), status=200, mimetype='application/json')
    return response

@app.route('/upload_post', methods = ['POST'])
def upload_post():
    if request.method!='POST':
      response = app.response_class(response=json.dumps({}), status=405, mimetype='application/json')
      return response      
    mycol = mydb["User_Posts"]
    content = request.get_json()
    with open(content["image"], "rb") as imageFile:
         b64 = base64.b64encode(imageFile.read())
         content["image"]=str(b64)
    mycol.insert_one(content)
    response = app.response_class(response=json.dumps({}), status=200, mimetype='application/json')
    return response

@app.route('/addComment', methods = ['POST'])
def Comment_Review():
    if request.method!='POST':
      response = app.response_class(response=json.dumps({}), status=405, mimetype='application/json')
      return response    
    content = request.get_json()
    mycol = mydb["User_Posts"]
    for x in mycol.find({} ,{"_id": 0, "username": 1,"comment":1}): 
        if(x["username"]==content["username"]):
          try:
            if(len(x["comment"])>0):
              l=x["comment"] 
              l.append(content["comment"])              
              myquery ={"username": x["username"] }
              newvalues = { "$set": { "comment": l} }
              mycol.update_one(myquery, newvalues)
              response = app.response_class(response=json.dumps({}), status=200, mimetype='application/json')
              return response 
          except:
            myquery ={"comment":  {"$exists":False}}
            l=[content["comment"]]
            newvalues = { "$set": { "comment": l } }
            mycol.update_one(myquery, newvalues)    
            response = app.response_class(response=json.dumps(), status=200, mimetype='application/json')
            return response    
    response = app.response_class(response=json.dumps({}), status=400, mimetype='application/json')
    return response 

   




if __name__ == '__main__':
   app.run(host='localhost',port="3000")

    

    



  

  

