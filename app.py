from flask import Flask, render_template, request
import os
from PIL import Image, ImageFont, ImageDraw, ImageEnhance
from io import BytesIO
import base64
from matplotlib.pyplot import imshow
import numpy as np
app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
@app.route("/")
def index():
	return render_template("index.html")

@app.route('/hello',methods=['POST'])
def hello():
    data_url = request.values['imageBase64']
    data_url= data_url[22:]
    im = Image.open(BytesIO(base64.b64decode(data_url)))
    print(type(im))
    #imshow(np.asarray(im))
    im.save('image.jpeg')
    return ''

if(__name__ == '__main__'):
    app.run(host='0.0.0.0',port=5000, ssl_context = 'adhoc')