from flask import Flask, render_template, request
from aisc import wide_flange_database, names
from math import floor, log10, sqrt, pi
from pageText.wideFlange import wideFlangeText

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Here is a free cookie!' # Not sure if the secret key is needed. It caused an error for me previously by removing it but now it is not creating any errors

@app.route('/', methods = ['POST', 'GET'])
def home():
    return render_template('home.html')

@app.route('/wideFlange', methods = ['POST', 'GET'])
def wideFlange():
    # Gets User Inputs
    member = request.form.get('member_dropdown')
    
    try:
        Fy = float(request.values.get('Fy'))
    except:
        Fy = 0
        
    try:
        Eksi = float(request.values.get('E'))
    except:
        Eksi = 0

    try:
        Lcx = float(request.values.get('Lcx'))
    except:
        Lcx = 0

    try:
        Lcy = float(request.values.get('Lcy'))
    except:
        Lcy = 0        

    # Creates main text to be sent to website
    output_text = wideFlangeText(member,Fy,Eksi,Lcx,Lcy)
    
    return render_template('flangeBase.html', 
                        Fy = Fy, E = Eksi, Lcx = Lcx, Lcy = Lcy,
                        output_text = output_text,
                        member_list = names())

# Text for header moved to flangeBase.html

if __name__ == '__main__':
    app.run(debug = True)

    # app.run(debug = True)
    # app.run(host="0.0.0.0", port=80, debug = True)