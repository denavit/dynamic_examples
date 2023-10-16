from flask import Flask, render_template, request, flash
from aisc import wide_flange_database, names
from math import sqrt, pi

app = Flask(__name__)

app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
@app.route('/', methods = ['POST', 'GET'])

def calculations():
    # Initializing Variables for Global Access
    member = request.form.get('member_dropdown')
    
    Fy = 0
    E = 0
    Lcx = 0
    Lcy = 0
    
    A = 0
    rx = 0
    ry = 0
    bf2tf = 0
    htw = 0
    lambdar_flange = 0
    flange_slenderness = ''
    lambdar_web = 0
    web_slenderness = ''
    Lcxrx = 0
    Lcyry = 0
    Lcr = 0
    controlling_axis = ''
    Fe = 0
    Fcr1 = 0
    Fcr2 = 0
    buckling_method = ''
    Fcr3 = 0
    Pn = 0
    phiPn = 0

    # Gets User Inputs
    if request.form.get('Fy') != None and request.form.get('Fy') != 0:
        Fy = float(request.values.get('Fy'))
    if request.form.get('E') != None and request.form.get('E') != 0:
        E = float(request.values.get('E'))
    if request.form.get('Lcx') != None and request.form.get('Lcx') != 0:
        Lcx = float(request.values.get('Lcx'))
    if request.form.get('Lcy') != None and request.form.get('Lcy') != 0:
        Lcy = float(request.values.get('Lcy'))

    if member != None and request.method == 'POST':
        # Gets Section Properties Data
        A = wide_flange_database[member]['A']
        rx = wide_flange_database[member]['rx']
        ry = wide_flange_database[member]['ry']
        bf2tf = wide_flange_database[member]['bf/2tf']
        htw = wide_flange_database[member]['h/tw']

        # Gets Flange and Web Slenderness Data
        if float(request.form.get('Fy')) > 0:
            lambdar_flange = 0.56 * sqrt(E / Fy)
        if bf2tf < lambdar_flange:
            flange_slenderness = 'nonslender'
        else:
            flange_slenderness = 'slender'
        if float(request.form.get('Fy')) > 0:
            lambdar_web = 1.49 * sqrt(E / Fy)
        if htw < lambdar_web:
            web_slenderness = 'nonslender'
        else:
            web_slenderness = 'slender'

        # Gets Axial Strength (Flexural Buckling) Data
        Lcxrx = Lcx / rx
        Lcyry = Lcy / ry
        Lcr = max(Lcxrx, Lcyry)
        if Lcxrx < Lcyry:
            controlling_axis = 'Minor Axis Controls'
        else:
            controlling_axis = 'Major Axis Controls'
        if float(request.form.get('Lcx')) > 0 and float(request.form.get('Lcy')) > 0: 
            Fe = pi**2 * E / Lcr**2
        if float(request.form.get('Lcx')) > 0 and float(request.form.get('Lcy')) > 0:
            Fcr1 = 0.658**(Fy/Fe)*Fy
        Fcr2 = 0.877 * Fe
        if float(request.form.get('Fy')) > 0:
            if Lcr <= 4.71 * sqrt(E / Fy):
                buckling_method = 'Inelastic Buckling'
                Fcr3 = Fcr1
            else:
                buckling_method = 'Elastic Buckling'
                Fcr3 = Fcr2
        Pn = Fcr3 * A
        phiPn = 0.9 * Pn


    return render_template('responsive_base.html', member_list = names(), member = member, Fy = Fy, E = E, Lcx = Lcx, Lcy = Lcy, 
                           A = A, rx = rx, ry = ry, bf2tf = bf2tf, htw = htw, 
                           lambdar_flange = lambdar_flange, flange_slenderness = flange_slenderness, lambdar_web = lambdar_web, web_slenderness = web_slenderness, 
                           Lcxrx = Lcxrx, Lcyry = Lcyry, Lcr = Lcr, controlling_axis = controlling_axis, Fe = Fe, Fcr1 = Fcr1, Fcr2 = Fcr2, buckling_method = buckling_method, Fcr3 = Fcr3, Pn = Pn, phiPn = phiPn)

if __name__ == '__main__':
    app.run(debug = True)

    # app.run(debug = True)
    # app.run(host="0.0.0.0", port=80, debug = True)