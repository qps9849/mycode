from flask import Flask, render_template, request
from PIL import Image
import numpy as np
from tensorflow.keras.models import  load_model

app=Flask(__name__)

@app.route('/')
def main():
    return render_template('mnist/index.html')

@app.route('/uploader',methods=['POST'])
def upload_image():
    model = load_model('c:/data/mnist')
    img=Image.open(request.files['file'].stream).convert("L")
    print(type(img))
    img=img.resize((28,28))
    arr=np.array(img)/255
    print(arr.shape)
    arr = arr.reshape(1,28,28,1)
    pred = model.predict(arr)
    pred=np.argmax(pred,axis=1)
    return '숫자 이미지:'+str(pred[0])

if __name__=='__main__':
    app.run(port=8000,threaded=False)