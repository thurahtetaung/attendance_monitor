from flask import Flask, render_template, request
import os
from PIL import Image, ImageFont, ImageDraw, ImageEnhance
import PIL.Image
import PIL.ImageOps
from io import BytesIO
import base64
from matplotlib.pyplot import imshow
import numpy as np
import face_recognition
from itertools import compress
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage


cred = credentials.Certificate("smart-attendance-584dc-firebase-adminsdk-mrqx9-f4215345a1.json")
fb_app = firebase_admin.initialize_app(cred,{'storageBucket': 'smart-attendance-584dc.appspot.com',}, name='storage')

bucket = storage.bucket(app=fb_app)

app = Flask(__name__)

# obama_image = face_recognition.load_image_file("faces/obama.jpg")
# obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

# thura_image = face_recognition.load_image_file("faces/thura.jpg")
# thura_face_encoding = face_recognition.face_encodings(thura_image)[0]

# # Load a second sample picture and learn how to recognize it.
# biden_image = face_recognition.load_image_file("faces/biden.jpg")
# biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

# # Load a second sample picture and learn how to recognize it.
# mom_image = face_recognition.load_image_file("faces/mom.jpg")
# mom_face_encoding = face_recognition.face_encodings(mom_image)[0]

# known_face_encodings = [
#     obama_face_encoding,
#     thura_face_encoding,
#     biden_face_encoding,
#     mom_face_encoding
# ]
# known_face_names = [
#     "Barack Obama",
#     "Thura Htet Aung",
#     "Joe Biden",
#     "Daw Thida Oo"
# ]

def exif_transpose(img):
    if not img:
        return img

    exif_orientation_tag = 274

    # Check for EXIF data (only present on some files)
    if hasattr(img, "_getexif") and isinstance(img._getexif(), dict) and exif_orientation_tag in img._getexif():
        exif_data = img._getexif()
        orientation = exif_data[exif_orientation_tag]

        # Handle EXIF Orientation
        if orientation == 1:
            # Normal image - nothing to do!
            pass
        elif orientation == 2:
            # Mirrored left to right
            img = img.transpose(PIL.Image.FLIP_LEFT_RIGHT)
        elif orientation == 3:
            # Rotated 180 degrees
            img = img.rotate(180)
        elif orientation == 4:
            # Mirrored top to bottom
            img = img.rotate(180).transpose(PIL.Image.FLIP_LEFT_RIGHT)
        elif orientation == 5:
            # Mirrored along top-left diagonal
            img = img.rotate(-90, expand=True).transpose(PIL.Image.FLIP_LEFT_RIGHT)
        elif orientation == 6:
            # Rotated 90 degrees
            img = img.rotate(-90, expand=True)
        elif orientation == 7:
            # Mirrored along top-right diagonal
            img = img.rotate(90, expand=True).transpose(PIL.Image.FLIP_LEFT_RIGHT)
        elif orientation == 8:
            # Rotated 270 degrees
            img = img.rotate(90, expand=True)

    return img


def load_image_file(file, mode='RGB'):
    # Load the image with PIL
    img = PIL.Image.open(file)
    img = exif_transpose(img)
    img = img.convert(mode)

    return np.array(img)

@app.route("/")
def index():
	return render_template("layout.html")

@app.route('/upload',methods=['POST'])
def hello():
    print(request)
    data = request.files['image']
    name = request.values['userid']
    # print(data)
    # print(name)

    blob = bucket.blob("user_photos/" + name)
    blob.download_to_filename("faces/user_face.jpg")
    user_image = load_image_file("faces/user_face.jpg")
    user_face_encodings = face_recognition.face_encodings(user_image)
    print(user_face_encodings)
    if not user_face_encodings:
        return {'Present': False}
    user_face_encoding = user_face_encodings[0]
    im = Image.open(data)
    #print(im)
    im.save("images/unknown_face.jpg")
    unknown_image = PIL.Image.open("images/unknown_face.jpg")
    unknown_image = unknown_image.rotate(90, expand=True)
    unknown_image.save("images/unknown_face.jpg")

    unknown_image = load_image_file("images/unknown_face.jpg")
    unknown_face_encoding = face_recognition.face_encodings(unknown_image)
    print(unknown_face_encoding)
    if unknown_face_encoding:
        result = face_recognition.compare_faces([user_face_encoding], unknown_face_encoding[0])
        print(result)
        return {'Present': bool(result[0])}
    return {'Present': False}

if(__name__ == '__main__'):
    app.run(host='0.0.0.0',port=5000, ssl_context = ('cert.pem', 'key.pem'))
