from flask import Flask, render_template, request
from dictionaries.aisc import names
from math import floor, log10, pi
from pageText.wideFlangeText import wideFlangeText
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
                        headerText = headerText, inputText = inputText, outputText = outputText, footerText = footerText)
    
@app.route('/bolt', methods = ['POST', 'GET'])
def bolt():
    
    # Gets User Inputs
    bolt = request.form.get('boltDropdown')
    UTSs_str = request.values.get('UTSs')
    UTSn_str = request.values.get('UTSn')
    LE_str   = request.values.get('LE')

    if bolt is None and UTSs_str is None and UTSn_str is None and LE_str is None:
        bolt = '1/2-13'
        UTSs_str = 110000
        UTSn_str = 105000
        LE_str = 1
    
    from pageText.FEDSTD_text import boltText_header, boltText_input, boltText_output, boltText_footer
    headerText = boltText_header()
    inputText  = boltText_input(UTSs_str,UTSn_str,LE_str)
    outputText = boltText_output(bolt, UTSs_str, UTSn_str, LE_str)
    footerText = boltText_footer()

    return render_template('base.html', name = r'/bolt', 
        headerText = headerText, inputText = inputText, outputText = outputText, footerText = footerText)



if __name__ == '__main__':
    app.run(debug = True)
