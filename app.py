from flask import Flask, render_template, request
import os
from PIL import Image, ImageFont, ImageDraw, ImageEnhance
from io import BytesIO
import base64
from matplotlib.pyplot import imshow
import numpy as np
import face_recognition
from itertools import compress

app = Flask(__name__)

obama_image = face_recognition.load_image_file("faces/obama.jpg")
obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

thura_image = face_recognition.load_image_file("faces/thura.jpg")
thura_face_encoding = face_recognition.face_encodings(thura_image)[0]

# Load a second sample picture and learn how to recognize it.
biden_image = face_recognition.load_image_file("faces/biden.jpg")
biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

# Load a second sample picture and learn how to recognize it.
mom_image = face_recognition.load_image_file("faces/mom.jpg")
mom_face_encoding = face_recognition.face_encodings(mom_image)[0]

known_face_encodings = [
    obama_face_encoding,
    thura_face_encoding,
    biden_face_encoding,
    mom_face_encoding
]
known_face_names = [
    "Barack Obama",
    "Thura Htet Aung",
    "Joe Biden",
    "Daw Thida Oo"
]

@app.route("/")
def index():
	return render_template("layout.html")

@app.route('/upload',methods=['POST'])
def hello():
    data_url = request.values['imageBase64']
    data_url= data_url[22:]
    name = request.values['username']
    im = Image.open(BytesIO(base64.b64decode(data_url)))
    im.save("images/" + name + '.jpg')
    fr = face_recognition.load_image_file("images/" + name + '.jpg')
    unknown_face_encoding = face_recognition.face_encodings(fr)
    result = face_recognition.compare_faces(known_face_encodings, unknown_face_encoding[0])
    face_name = list(compress(known_face_names, result))
    print(face_name[0])
    return ''

if(__name__ == '__main__'):
    app.run(host='0.0.0.0',port=5000, ssl_context = ('cert.pem', 'key.pem'))
