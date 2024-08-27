from flask import Flask, render_template, request
from dictionaries.aisc import names
from math import floor, log10, sqrt, pi
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
    member = request.form.get('memberDropdown')

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
    print('HELLO WORLD')

    flangeOutputText = wideFlangeText(member,Fy,Eksi,Lcx,Lcy)
    
    return render_template('flangeBase.html', 
                        Fy = Fy, E = Eksi, Lcx = Lcx, Lcy = Lcy,
                        flangeOutputText = flangeOutputText,
                        member_list = names())

    
@app.route('/bolt', methods = ['POST', 'GET'])
def bolt():
    # Gets User Inputs
    bolt = request.form.get('boltDropdown')

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
        LE = 1
    print('HELLO WORLD')
    if bolt == None:
        n = 0
        dmin = 0
        dbsc = 0
        d2min = 0
        D1bsc = 0
        D1max = 0
        D2max = 0

        return render_template('boltBase.html',
                               n = n, dmin = dmin, dbsc = dbsc, d2min = d2min, D1bsc = D1bsc, D1max = D1max, D2max = D2max,
                               UTSs = UTSs, UTSn = UTSn, LE = LE)
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

        boltOutputText = boltText(bolt, n, dmin, dbsc, d2min, D1bsc, D1max, D2max, UTSs, UTSn, LE)

        return render_template('boltBase.html',
                               n = n, dmin = dmin, dbsc = dbsc, d2min = d2min, D1bsc = D1bsc, D1max = D1max, D2max = D2max,
                               UTSs = UTSs, UTSn = UTSn, LE = LE,
                               boltOutputText = boltOutputText)


# Text for header moved to flangeBase.html

if __name__ == '__main__':
    app.run(debug = True)

    # app.run(debug = True)
    # app.run(host="0.0.0.0", port=80, debug = True)