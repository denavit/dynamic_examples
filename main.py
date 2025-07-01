from flask import Flask, render_template, request
from dictionaries.aisc import names
from math import floor, log10, pi
from pageText.wideFlangeText import wideFlangeText
from pageText.FEDSTD_text import boltFEDText
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

    return render_template('base.html', name = r'/wideFlange', 
                        title = 'Wide Flange Steel Members', headerText = headerText, inputText = inputText, outputText = outputText, footerText = footerText)
    
@app.route('/boltFED', methods = ['POST', 'GET'])
def bolt():
    # Gets User Inputs
    if request.form.get('boltDropdown') == None:
        bolt = '1/2-13'
    else:
        bolt = request.form.get('boltDropdown')
    
    if request.form.get('boltDropdown') == None:
        bolt = '1/2-13'
    else:
        bolt = request.form.get('boltDropdown')

    try:
        UTSs_str = int(request.values.get('UTSs'))
    except:
        UTSs_str = 110000
    
    try:
        UTSn_str = int(request.values.get('UTSn'))
    except:
        UTSn_str = 105000
    
    headerText, inputText, outputText, footerText = boltFEDText(bolt, UTSs_str, UTSn_str)

    return render_template('base.html', name = r'/boltFED', 
        title = 'FED-STD H28/2B Tensile Strength', headerText = headerText, inputText = inputText, outputText = outputText, footerText = footerText)



if __name__ == '__main__':
    app.run(debug = True)
