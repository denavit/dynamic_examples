from flask import Flask, render_template, request
from dictionaries.aisc import names
from math import floor, log10, sqrt, pi
from pageText.wideFlangeText import wideFlangeText
from pageText.boltText import boltText

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Here is a free cookie!' # Not sure if the secret key is needed. It caused an error for me previously by removing it but now it is not creating any errors

@app.route('/', methods = ['POST', 'GET'])
def home():
    return render_template('home.html')

@app.route('/wideFlange', methods = ['POST', 'GET'])
def wideFlange():
    # Gets User Inputs
    member = request.form.get('wideFlangeDropdown')
    
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

    
@app.route('/bolt', methods = ['POST', 'GET'])
def bolt():
    # Gets User Inputs
    bolt = request.form.get('boltDropdown')

    try:
        n = float(request.values.get('n'))
    except:
        n = 0

    try:
        dmin = float(request.values.get('dmin'))
    except:
        dmin = 0

    try:
        dbsc = float(request.values.get('dbsc'))
    except:
        dbsc = 0

    try:
        d1bsc = float(request.values.get('d1bsc'))
    except:
        d1bsc = 0

    try:
        d2min = float(request.values.get('d2min'))
    except:
        d2min = 0

    try:
        d2bsc = float(request.values.get('d2bsc'))
    except:
        d2bsc = 0

    try:
        D1bsc = float(request.values.get('D1bsc'))
    except:
        D1bsc = 0

    try:
        D1max = float(request.values.get('D1max'))
    except:
        D1max = 0

    try:
        D2max = float(request.values.get('D2max'))
    except:
        D2max = 0

    try:
        UTSs = float(request.values.get('UTSs'))
    except:
        UTSs = 0

    try:
        UTSn = float(request.values.get('UTSn'))
    except:
        UTSn = 0

    try:
        LE = float(request.values.get('LE'))
    except:
        LE = 0

    bolt_output_text = boltText(bolt, n, dmin, dbsc, d1bsc, d2min, d2bsc, D1bsc, D1max, D2max, UTSs, UTSn, LE)


    return render_template('boltBase.html',
                           n = n, dmin = dmin, dbsc = dbsc, d1bsc = d1bsc, d2min = d2min, d2bsc = d2bsc, D1bsc = D1bsc, D1max = D1max, D2max = D2max, UTSs = UTSs, UTSn = UTSn, LE = LE,
                           bolt_output_text = bolt_output_text)


# Text for header moved to flangeBase.html

if __name__ == '__main__':
    app.run(debug = True)

    # app.run(debug = True)
    # app.run(host="0.0.0.0", port=80, debug = True)