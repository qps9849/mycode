from flask import Flask, render_template,request
from PIL import Image
import numpy as np
from tensorflow.keras.models import load_model

app=Flask(__name__)
@app.route('/')
def main():
    return render_template('cifar/index.html')

@app.route('/uploader',methods=['POST'])
def upload_image():
    model=load_model('c:/data/cifar')
    img  = Image.open(request.files['file'].stream)
    print(type(img))
    img=img.resize((32,32))
    arr=np.array(img)/255
    print(arr.shape)
    arr = arr.reshape(1, 32, 32, 3)
    pred = model.predict(arr)
    pred=np.argmax(pred,axis=1)
    a = str(pred[0])
    if a == '0':
        name='비행기'
    elif a=='1':
        name='자동차'
    elif a=='2':
        name='새'
    elif a=='3':
        name='고양이'
    elif a=='4':
        name='사슴'
    elif a=='5':
        name='개'
    elif a=='6':
        name='개구리'
    elif a=='7':
        name='말'
    elif a=='8':
        name='배'
    elif a=='9':
        name = '트럭'
    return '이미지:'+name

if __name__=='__main__':
    app.run(port=8000, threaded=False)