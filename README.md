# WEB-Tech-2

Food blog website using Vanilla Javascript, HTML, CSS front end and Flask-MongoDB Backend. Users can sign up to the website and upload posts of food which involves uploading photos, writing descriptions and captions. Users can be searched for and their posts and can be commented on. Using Resnet50 object detection the food can be recognized and their names returned with hashtags to provide some captioning automation.

1) Setup flask on your machine
2) Setup MongoDB and create the collections 
2) Run api.py, image.py as 2 separate flask servers on different ports
3) The website is hosted on the api.py flask server.
4) The image.py server is used as the ML component(Food recognition) in the project.
