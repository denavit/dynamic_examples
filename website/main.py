from flask import Flask, render_template, request
from dictionaries.aisc import names
from math import floor, log10, pi
from pageText.wideFlangeText import wideFlangeText
from pageText.boltText import boltText
from dictionaries.ASME_B11 import ASME_B11_UN_2A2B_dict

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Here is a free cookie!' # Not sure if the secret key is needed. It caused an error for me previously by removing it but now it is not creating any errors

@app.route('/', methods = ['POST', 'GET'])
def home():
    return render_template('home.html')

@app.route('/wideFlange', methods = ['POST', 'GET'])
def wideFlange():
    # Gets User Inputs
    if request.form.get('memberDropdown') == None:
        member = 'W14X159'
    else:
        member = request.form.get('memberDropdown')


    try:
        Fy = float(request.values.get('Fy'))
    except:
        Fy = 25
        
    try:
        Eksi = float(request.values.get('E'))
    except:
        Eksi = 29000

    try:
        Lcx = float(request.values.get('Lcx'))
    except:
        Lcx = 240

    try:
        Lcy = float(request.values.get('Lcy'))
    except:
        Lcy = 240    
    
    headerText, inputText, outputText, footerText = wideFlangeText(member,Fy,Eksi,Lcx,Lcy)

    return render_template('base.html', 
                        Fy = Fy, E = Eksi, Lcx = Lcx, Lcy = Lcy, 
                        headerText = headerText, inputText = inputText, outputText = outputText, footerText = footerText
                        )
    
@app.route('/bolt', methods = ['POST', 'GET'])
def bolt():
    # Gets User Inputs
    bolt = request.form.get('boltDropdown')

    try:
        UTSs = float(request.values.get('UTSs'))
    except:
        UTSs = 110000

    try:
        UTSn = float(request.values.get('UTSn'))
    except:
        UTSn = 105000

    try:
        LE = float(request.values.get('LE'))
    except:
        LE = 1

    if bolt == None:
        bolt = '1/2-13'
        n = ASME_B11_UN_2A2B_dict[bolt]['n']
        dmin = ASME_B11_UN_2A2B_dict[bolt]['dmin']
        dbsc = ASME_B11_UN_2A2B_dict[bolt]['dbsc']
        d2min = ASME_B11_UN_2A2B_dict[bolt]['d2min']
        D1bsc = ASME_B11_UN_2A2B_dict[bolt]['D1bsc']
        D1max = ASME_B11_UN_2A2B_dict[bolt]['D1max']
        D2max = ASME_B11_UN_2A2B_dict[bolt]['D2max']

        headerText, inputText, outputText, footerText = boltText(bolt, n, dmin, dbsc, d2min, D1bsc, D1max, D2max, UTSs, UTSn, LE)


        return render_template('base.html',
            n = n, dmin = dmin, dbsc = dbsc, d2min = d2min, D1bsc = D1bsc, D1max = D1max, D2max = D2max,
            UTSs = UTSs, UTSn = UTSn, LE = LE, 
            headerText = headerText, inputText = inputText, outputText = outputText, footerText = footerText)
            

    else:
        n = ASME_B11_UN_2A2B_dict[bolt]['n']
        dmin = ASME_B11_UN_2A2B_dict[bolt]['dmin']
        dbsc = ASME_B11_UN_2A2B_dict[bolt]['dbsc']
        # d1bsc = ASME_B11_UN_2A2B_dict[bolt]['d1bsc']
        d2min = ASME_B11_UN_2A2B_dict[bolt]['d2min']
        # d2bsc = ASME_B11_UN_2A2B_dict[bolt]['d2bsc']
        D1bsc = ASME_B11_UN_2A2B_dict[bolt]['D1bsc']
        D1max = ASME_B11_UN_2A2B_dict[bolt]['D1max']
        D2max = ASME_B11_UN_2A2B_dict[bolt]['D2max']

        headerText, inputText, outputText, footerText = boltText(bolt, n, dmin, dbsc, d2min, D1bsc, D1max, D2max, UTSs, UTSn, LE)

        return render_template('base.html',
            n = n, dmin = dmin, dbsc = dbsc, d2min = d2min, D1bsc = D1bsc, D1max = D1max, D2max = D2max,
            UTSs = UTSs, UTSn = UTSn, LE = LE,
            headerText = headerText, inputText = inputText, outputText = outputText, footerText = footerText)


# Text for header moved to flangeBase.html

if __name__ == '__main__':
    app.run(debug = True)

    # app.run(debug = True)
    # app.run(host="0.0.0.0", port=80, debug = True)