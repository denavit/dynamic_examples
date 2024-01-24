from flask import Flask, render_template, request
from aisc import wide_flange_database, names
from math import sqrt, pi

app = Flask(__name__)

app.config['SECRET_KEY'] = 'Here is a free cookie!'
@app.route('/', methods = ['POST', 'GET'])

def calculations():
    # Initializing Variables for Global Access
    member = request.form.get('member_dropdown')
    
    Fy = 0
    Eksi = 0
    Lcx = 0
    Lcy = 0
    
    section_properties_text = ''
    slenderness_check_text = ''
    column_strength_text = ''
    critical_stresses_text = ''
    nominal_strength_text = ''
    line = ''
    
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
    Fcr = 0
    Fcr1 = 0
    Fcr2 = 0
    buckling_method = ''
    Fcr3 = 0
    Pn = 0
    phiPn = 0
    omegaPn = 0

    # Gets User Inputs
    if request.form.get('Fy') != None and request.form.get('Fy') != 0 and request.form.get('Fy') != '':
        Fy = float(request.values.get('Fy'))
    if request.form.get('E') != None and request.form.get('E') != 0 and request.form.get('E') != '':
        Eksi = float(request.values.get('E'))
    if request.form.get('Lcx') != None and request.form.get('Lcx') != 0 and request.form.get('Lcx') != '':
        Lcx = float(request.values.get('Lcx'))
    if request.form.get('Lcy') != None and request.form.get('Lcy') != 0 and request.form.get('Lcy') != '':
        Lcy = float(request.values.get('Lcy'))

    if Fy == 0 or Fy == None or Eksi == 0 or Eksi == None or Lcx == 0 or Lcx == None or Lcy == 0 or Lcy == None:
        section_properties_text = f'<h2 style = "text-align: center;">Input Values Can Not Equal 0<h2>'
    else:
        # Gets Section Properties Data
        A = wide_flange_database[member]['A']
        rx = wide_flange_database[member]['rx']
        ry = wide_flange_database[member]['ry']
        bf2tf = wide_flange_database[member]['bf/2tf']
        htw = wide_flange_database[member]['h/tw']

        line = '<hr />'

        section_properties_text = f'''<ul>
              <li>
                From AISC
                <i>Manual</i>
                Table 2-4, the material properties are as follows:
                <ul>
                  <li>{member}</li>
                  <li>$A_{{g}} = {{{'%.2f'%A}}}\\text{{ in.}}^{{2}}$</li> 
                  <li>$r_{{x}} = {{{'%.2f'%rx}}}\\text{{ in.}}$</li>
                  <li>$r_{{y}} = {{{'%.2f'%ry}}}\\text{{ in.}}$</li>
                  <li>$\\frac{{b_{{f}}}}{{2t_{{f}}}} = {{{'%.2f'%bf2tf}}}$</li>
                  <li>$\\frac{{h}}{{t_{{w}}}} = {{{'%.2f'%htw}}}$</li>
                </ul>
              </li>
            </ul>'''

        # Gets Slenderness Check Data
        Lcxrx = Lcx / rx
        Lcyry = Lcy / ry
        Lcr = max(Lcxrx, Lcyry)
        if Lcxrx < Lcyry:
            control_sign = '<'
            controlling_axis = 'minor axis controls'
        else:
            control_sign = '>'
            controlling_axis = 'major axis controls'

        slenderness_check_text = f'''
        <ul>
        <li><i>Slenderness Check</i></li>
            <ul>
                <li>
                  $\\frac{{L_{{cx}}}}{{r_{{x}}}} = \\frac{{{'%.2f'%Lcx}\\text{{ in.}}}}
                  {{{'%.2f'%rx}\\text{{ in.}}}} = {{{'%.2f'%Lcxrx}}}\\text{{ governs}}$
                </li>
                <br />
                <li>
                  $\\frac{{L_{{cy}}}}{{r_{{y}}}} = \\frac{{{'%.2f'%Lcy}\\text{{ in.}}}}{{
                  {{{'%.2f'%ry}\\text{{ in.}}}}}}= {{{'%.2f'%Lcyry}}}$
                </li>
                <br />
                <li>
                  ${{{'%.2f'%Lcxrx}}} {control_sign} {{{'%.2f'%Lcyry}}}$; therefore, the
                  {controlling_axis}
                </li>
                <br />
                <li>
                  $\\frac{{L_{{c}}}}{{r}} = \\text{{max}}(\\frac{{L_{{cx}}}}{{r_{{x}}}},
                  \\frac{{L_{{cy}}}}{{r_{{y}}}}) = \\text{{max}}({{{'%.2f'%Lcxrx}}},
                  {{{'%.2f'%Lcyry}}}) = {{{'%.2f'%Lcr}}}$
                </li>
            </ul>
            </ul>'''


        # Gets Column Compressive Strength Data
        lambdar_flange = 0.56 * sqrt(Eksi / Fy)
        lambdar_web = 1.49 * sqrt(Eksi / Fy)

        if bf2tf < lambdar_flange:
            flange_sign = '<'
            flange_slenderness = 'nonslender'
        else:
            flange_sign = '>'
            flange_slenderness = 'slender'

        if htw < lambdar_web:
            web_sign = '<'
            web_slenderness = 'nonslender'
        else:
            web_sign = '>'
            web_slenderness = 'slender'

        column_strength_text = f'''
            <ul>
              <li>
                <i
                  >Column Compressive Strength -- ASTM A992<br /><br />Width-to-Thickness
                  Ratio
                </i>
              </li>
              <br />
              <li>
                The width-to-thickness ratio of the flanges of the {member}
                is:
                <ul>
                  <li>$\\frac{{b_{{f}}}}{{2t_{{f}}}} = {{{'%.2f'%bf2tf}}}$</li>
                </ul>
              </li>
              <br />
              <li>
                From AISC <i>Specification</i> Table B4.1a, Case 1, the limiting
                width-to-thickness ratio of the flanges is:
                <ul>
                  <li>
                    $&#955;_{{f}} = 0.56\sqrt{{\\frac{{E}}{{F_{{y}}}}}} = 0.56\sqrt\\frac{{{'%.2f'%Eksi}}}{{{'%.2f'%Fy}}} = {{{
                    '%.2f'%lambdar_flange}}}$
                    <ul>
                      <li>
                        ${{{'%.2f'%bf2tf}}} {flange_sign} {{{'%.2f'%lambdar_flange}}}$;
                        therefore, the flanges are {flange_slenderness}
                      </li>
                    </ul>
                  </li>
                </ul>
              </li>
              <br />
              <li>
                The width-to-thickness ratio of the web of the {member} is:
                <ul>
                  <li>$\\frac{{h}}{{t_{{w}}}} = {{{'%.2f'%htw}}}$</li>
                </ul>
              </li>
              <br />
              <li>
                From AISC <i>Specification</i> Table B4.1a, Case 5, the limiting
                width-to-thickness ratio of the web is:
                <ul>
                  <li>
                    $&#955;_{{w}} = 1.49\sqrt{{\\frac{{E}}{{F_{{y}}}}}} = 1.49\sqrt\\frac{{{
                    '%.2f'%Eksi}}}{{{'%.2f'%Fy}}} = {
                    '%.2f'%lambdar_web}$
                    <ul>
                      <li>
                        ${htw} {web_sign} {'%.2f'%lambdar_web}$; therefore, the
                        web is {web_slenderness}
                      </li>
                    </ul>
                  </li>
                </ul>
              </li>
              <br />
              <li>
                Because the web and flanges are nonslender, the limit state of
                local buckling does not apply. -- TO FIX LATER, NEED INFO ON
                OTHER CASES: Both slender, one slender/one nonslender, one
                nonslender/one slender
              </li>
            </ul>'''

        # Gets Critical Stresses Data
        Fe = pi**2 * Eksi / Lcr**2
        Fcr = 4.71 * sqrt(Eksi / Fy)
        Fcr1 = 0.658**(Fy/Fe)*Fy
        Fcr2 = 0.877 * Fe

        if Lcr < Fcr:
            buckling_sign = '<'
            buckling_method_equ = f'''$F_{{cr}} = (0.658^{{\\frac{{F_{{y}}}}{{F_{{e}}}}}})F_{{y}} = (0.658^\\frac{{
                  {'%.2f'%Fy}\\text{{ ksi}}}}{{{'%.2f'%Fe}\\text{{ ksi}}}})({{{'%.2f'%Fy}\\text{{ ksi}}}}) = {{{'%.2f'%Fcr1}\\text{{ ksi}}}}$'''
            Fcr3 = Fcr1
        elif Lcr == Fcr:
            buckling_sign = '='
            buckling_method_equ = f'''$F_{{cr}} = (0.658^{{\\frac{{F_{{y}}}}{{F_{{e}}}}}})F_{{y}} = (0.658^\\frac{{
                  {'%.2f'%Fy}\\text{{ ksi}}}}{{{'%.2f'%Fe}\\text{{ ksi}}}})({{{'%.2f'%Fy}\\text{{ ksi}}}}) = {{{'%.2f'%Fcr1}\\text{{ ksi}}}}$'''
            Fcr3 = Fcr1
        else:
            buckling_sign = '>'
            buckling_method_equ = f'''$F_{{cr}} = 0.877Fe = 0.877({'%.2f'%Fe}) = {'%.2f'%Fcr2}\\text{{ ksi}}$'''
            Fcr3 = Fcr2

        critical_stresses_text = f'''
            <ul>
              <li>
                <i>Critical Stresses</i><br /><br />The available critical
                stresses may be interpolated from AISC <i>Manual</i> Table 4-14
                or calculated directly as follows.<br /><br />Calculate the
                elastic critical buckling stress, $F_{{e}}$, according to AISC
                <i>Specification</i> Section E3. As noted in AISC
                <i>Specification</i>
                Commentary Section E4, torsional buckling of symmetric shapes is
                a failure mode usually not considered in the design of
                hot-rolled columns. This failure mode generally does not govern
                unless the section is manufactured from relatively thin plates
                or a torsional unbraced length significantly larger than the
                <i>y-y</i> axis flexural unbraced length is present.
              </li>
              <ul>
                <li>
                  $F_{{e}} = \\frac{{\pi ^{{2}}E}}{{(\\frac{{L_{{c}}}}{{r}})^{{2}}}} = \\frac{{\pi
                  ^{{2}}( {{{'%.2f'%Eksi}}} )}}{{{'%.2f'%Lcr}}} ^{{2}} =
                  {{{'%.2f'%Fe}}} \\text{{ ksi}}$
                </li>
              </ul>
              <br />
              <li>Calculate the flexural buckling stress, $F_{{cr}}$.</li>
              <ul>
                <li>
                  $4.71\sqrt{{\\frac{{E}}{{F_{{y}}}}}} = 4.71\sqrt\\frac{{{'%.2f'%Eksi}}}
                  {{{'%.2f'%Fy}}} = {{{'%.2f'%Fcr}}}$
                </li>
              </ul>
              <br />
              <li>
                Because $\\frac{{L_{{c}}}}{{r}} = {{{'%.2f'%Lcr}}} {buckling_sign}
                {{{'%.2f'%Fcr}}}$
              </li>
              <ul>
                {buckling_method_equ}
              </ul>
            </ul>'''

        # Gets Nominal Compressive Strength Data
        Pn = Fcr3 * A
        phiPn = 0.9 * Pn
        omegaPn = Pn / 1.67

        if phiPn > 840:
            phiPn_sign = '>'
        else:
            phiPn_sign = '<'

        if omegaPn > 560:
            omegaPn_sign = '>'
        else:
            omegaPn_sign = '<'

        nominal_strength_text = f'''
            <ul>
              <li>
                <i>Nominal Compressive Strength</i>
              </li>
              <ul>
                <li>
                  $P_{{n}}=F_{{cr}}A_{{g}} = ({'%.2f'%Fcr1}\\text{{
                  ksi}})({'%.2f'%A}\\text{{ in.}}^{{2}}) = {'%.2f'%Pn}\\text{{
                  kips}}$
                </li>
              </ul>
              <br />
              <li>
                From AISC <i>Specification</i> Section E1, the available
                compressive strength is:
              </li>
              <ul>
                <li><b>LRFD:</b></li>
                <ul>
                  <li>$&#934;_{{c}}$ = 0.90</li>
                  <li>
                    $&#934;_{{c}}P_{{n}} = 0.90({'%.2f'%Pn}\\text{{ kips}}) =
                    {'%.2f'%phiPn}\\text{{ kips}} {phiPn_sign} 840.00\\text{{ kips}}$
                    <b>o.k.</b> -- TO FIX LATER, ADD CONDITIONS FOR WHEN NOT OK -- WHAT IS THE 840
                  </li>
                </ul>
                <br />
                <li><b>ASD:</b></li>
                <ul>
                  <li>$&#937;_{{c}}$ = 1.67</li>
                  <li>
                    $\\frac{{P_{{n}}}}{{&#937;_{{c}}}} = \\frac{{{'%.2f'%Pn}\\text{{
                    kips}}}}{{1.67}} = {'%.2f'%omegaPn} {omegaPn_sign} 560.00\\text{{ kips}}$
                    <b>o.k.</b> -- TO FIX LATER, ADD CONDITIONS FOR WHEN NOT OK -- WHAT IS THE 560
                  </li>
                </ul>
              </ul>
            </ul>'''

    return render_template('responsive_base.html', 
                        Fy = Fy, E = Eksi, Lcx = Lcx, Lcy = Lcy,
                        line = line, 
                        section_properties_text = section_properties_text, 
                        slenderness_check_text = slenderness_check_text, 
                        column_strength_text = column_strength_text, 
                        critical_stresses_text = critical_stresses_text,
                        nominal_strength_text = nominal_strength_text,
                        member_list = names())

if __name__ == '__main__':
    app.run(debug = True)

    # app.run(debug = True)
    # app.run(host="0.0.0.0", port=80, debug = True)