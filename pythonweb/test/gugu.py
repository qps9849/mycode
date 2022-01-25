from flask import Flask, Markup, render_template, request
app = Flask(__name__)

@app.route('/',methods=['GET'])
def main():
    return render_template('gugu.html')

@app.route('/gugu_result', methods=['POST'])
def gugu_result():
    dan= int(request.form['dan'])
    result=''
    for i in range(1,10):
        result += '{}x{}={}<br>'.format(dan,i,dan*1)
    result=Markup(result)
    return render_template('gugu_result.html',result=result)

if __name__ == '__main__':
    app.run(port=8000, threaded=False)