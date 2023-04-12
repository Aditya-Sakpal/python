from flask import Flask, render_template, request
# from keras.preprocessing import image
import keras.utils as image
from keras.applications.xception import Xception
from keras.applications.xception import preprocess_input, decode_predictions
from numpy import *

model = Xception(weights='imagenet')

app = Flask(__name__)


@app.route('/', methods=['GET'])
def init():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def predict():
    img = request.files['imgfile']
    img_path = "./images/"+img.filename
    img.save(img_path)
    
    img = image.load_img(img_path, target_size=(299, 299))
    x = image.img_to_array(img)
    x = expand_dims(x, axis=0)
    x = preprocess_input(x)
    pred = model.predict(x)
    ans='%s %.2f%%'%(decode_predictions(pred,top=5)[0][0][1],decode_predictions(pred,top=5)[0][0][2]*100)

    

    return render_template('index.html',prediction=ans)

app.run()
