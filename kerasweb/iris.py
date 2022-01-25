from flask import Flask,render_template,request
import numpy as np

app = Flask(__name__)

@app.route('/iris',methods=['GET'])
def main():
    return render_template('iris/input.html')

#import tensorflow as tf
from keras.models import load_model

@app.route('/iris_result',methods=['POST'])
def iris_result():
    flowers = ['sesota', 'versicolor', 'virginica']
    # with tf.device('/CPU:0'):
    #     model=load_model('c:/data/iris/iris.keras')
    #     model.load_weights('c:/data/iris/iris.weights')
    a = float(request.form['a'])
    b = float(request.form['b'])
    c = float(request.form['c'])
    d = float(request.form['d'])
    test_set=np.array([[a,b,c,d]])
    #n=model.predict_classes(test_set)
    #result=flowers[n[0]]
    result=''
    return render_template('iris/result.html', result=result,a=a,b=b,c=c,d=d)

if __name__=='__main__':
    app.run(port=8000, threaded=False)