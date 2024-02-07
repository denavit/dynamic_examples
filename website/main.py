from flask import Flask, render_template, request
from aisc import wide_flange_database, names
from math import sqrt, pi

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Here is a free cookie!'

@app.route('/', methods = ['POST', 'GET'])
def calculations():

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
    output_text = generate_output_text(member,Fy,Eksi,Lcx,Lcy)
    
    
    
    return render_template('responsive_base.html', 
                        Fy = Fy, E = Eksi, Lcx = Lcx, Lcy = Lcy,
                        main_text = output_text,
                        member_list = names())

def generate_output_text(member,Fy,Eksi,Lcx,Lcy):

    text = ''

    # Check output
    if Fy <= 0:
        return 'Steel yield stress must be greater than zero.'        
    if Eksi <= 0:
        return 'Modulus of elasticity must be greater than zero.'
    if Lcx < 0 or Lcy < 0:
        return 'The effective lengths must be greater than or equal to zero.'


    # Section Properties Data
    A = wide_flange_database[member]['A']
    rx = wide_flange_database[member]['rx']
    ry = wide_flange_database[member]['ry']
    bf2tf = wide_flange_database[member]['bf/2tf']
    htw = wide_flange_database[member]['h/tw']

    text += f'''
    <div class="col-5">
        <p>From AISC <i>Manual</i> Table 1-1, the geometric properties for a {member} are as follows:</p>
        <ul>
          <li>$A_{{g}} = {{{'%.2f'%A}}}\\text{{ in.}}^{{2}}$</li> 
          <li>$r_{{x}} = {{{'%.2f'%rx}}}\\text{{ in.}}$</li>
          <li>$r_{{y}} = {{{'%.2f'%ry}}}\\text{{ in.}}$</li>
          <li>$\\frac{{b_{{f}}}}{{2t_{{f}}}} = {{{'%.2f'%bf2tf}}}$</li>
          <li>$\\frac{{h}}{{t_{{w}}}} = {{{'%.2f'%htw}}}$</li>
        </ul>
    </div>'''

    # Slenderness Check
    lambdar_flange = 0.56 * sqrt(Eksi / Fy)
    lambdar_web = 1.49 * sqrt(Eksi / Fy)

    text += f'''
    <div class="col-5">  
      <h1>Slenderness Check</h1>
      <p>The width-to-thickness ratio of the flanges of the {member} is:</p>
      <ul>
        <li>$\\frac{{b_{{f}}}}{{2t_{{f}}}} = {{{'%.2f'%bf2tf}}}$</li>
      </ul>
      <p>From AISC <i>Specification</i> Table B4.1a, Case 1, the limiting width-to-thickness ratio of the flanges is:</p>
      <ul>
        <li>'''
        
    text += r'$\begin{aligned}\lambda_{r} &= 0.56\sqrt{\frac{E}{F_{y}}} \\ &= 0.56\sqrt{\frac{' + f'{Eksi:.2f}' + r'\text{ ksi}}{' + \
            f'{Fy:.2f}' + r'\text{ ksi}}} \\ &= ' + f'{lambdar_flange:.2f}' + r'\end{aligned}$'
    
    text += '''</li>
        <li>'''    
    
    if bf2tf > lambdar_flange:
        text += r'$\frac{b_f}{2t_f} = ' + f'{bf2tf:.2f}' + r' > \lambda_f =' + f'{lambdar_flange:.2f}' r'$; therefore the flanges are slender'       
    else:
        text += r'$\frac{b_f}{2t_f} = ' + f'{bf2tf:.2f}' + r' \leq \lambda_f =' + f'{lambdar_flange:.2f}' r'$; therefore the flanges are nonslender'       
    
    text += f'''</li>
      </ul>
      <p>The width-to-thickness ratio of the web of the {member} is:</p>
      <ul>
        <li>$\\frac{{h}}{{t_{{w}}}} = {{{'%.2f'%htw}}}$</li>
      </ul>
      <p>From AISC <i>Specification</i> Table B4.1a, Case 5, the limiting width-to-thickness ratio of the web is:</p>
      <ul>
        <li>'''
        
    text += r'$\begin{aligned}\lambda_{r} &= 1.49\sqrt{\frac{E}{F_{y}}} \\ &= 1.49\sqrt{\frac{' + f'{Eksi:.2f}' + r'\text{ ksi}}{' + \
            f'{Fy:.2f}' + r'\text{ ksi}}} \\ &= ' + f'{lambdar_web:.2f}' + r'\end{aligned}$'
    
    text += '''</li>
        <li>'''    
    
    if htw > lambdar_web:
        text += r'$\frac{h}{t_w} = ' + f'{htw:.2f}' + r' > \lambda_f =' + f'{lambdar_web:.2f}' r'$; therefore the web is slender'       
    else:
        text += r'$\frac{h}{t_w} = ' + f'{htw:.2f}' + r' \leq \lambda_f =' + f'{lambdar_web:.2f}' r'$; therefore the web is nonslender'       
    
    text += f'''</li>
      </ul>'''
      
    if bf2tf > lambdar_flange:
        if htw > lambdar_web:
            text += r'Because the web and flanges are slender, the strength must be computed using AISC <i>Specification</i> Section E6 and will not be shown here.'
            text += '''  
    </div>'''            
            return text
        else:
            text += r'Because the flanges are slender, the strength must be computed using AISC <i>Specification</i> Section E6 and will not be shown here.'
            text += '''  
    </div>'''            
            return text
    else:
        if htw > lambdar_web:
            text += r'Because the web is slender, the strength must be computed using AISC <i>Specification</i> Section E6 and will not be shown here.'
            text += '''  
    </div>'''            
            return text
        else:
            text += r'Because the web and flanges are nonslender, the limit state of local buckling does not apply and the strength is computed according to AISC <i>Specification</i> Section E3.'
            
    text += '''  
    </div>'''


    # Gets Critical Stresses Data
    Lcxrx = Lcx / rx
    Lcyry = Lcy / ry
    Lcr = max(Lcxrx, Lcyry)
    if Lcxrx < Lcyry:
        control_sign = '<'
        controlling_axis = 'minor axis controls'
    else:
        control_sign = '>'
        controlling_axis = 'major axis controls'    

    text += f'''
    <div class="col-5">  
      <h1>Governing Slenderness Ratio</h1>
      <ul>
        <li>
          $\\frac{{L_{{cx}}}}{{r_{{x}}}} = \\frac{{{'%.2f'%Lcx}\\text{{ in.}}}}
          {{{'%.2f'%rx}\\text{{ in.}}}} = {{{'%.2f'%Lcxrx}}}\\text{{ governs}}$
        </li>
        <br/>
        <li>
          $\\frac{{L_{{cy}}}}{{r_{{y}}}} = \\frac{{{'%.2f'%Lcy}\\text{{ in.}}}}{{
          {{{'%.2f'%ry}\\text{{ in.}}}}}}= {{{'%.2f'%Lcyry}}}$
        </li>
        <br/>
        <li>
          ${{{'%.2f'%Lcxrx}}} {control_sign} {{{'%.2f'%Lcyry}}}$; therefore, the
          {controlling_axis}
        </li>
        <br/>
        <li>
          $\\frac{{L_{{c}}}}{{r}} = \\text{{max}}(\\frac{{L_{{cx}}}}{{r_{{x}}}},
          \\frac{{L_{{cy}}}}{{r_{{y}}}}) = \\text{{max}}({{{'%.2f'%Lcxrx}}},
          {{{'%.2f'%Lcyry}}}) = {{{'%.2f'%Lcr}}}$
        </li>
      </ul>      
      
    </div>'''
    
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

    # Gets Nominal Compressive Strength Data
    Pn = Fcr3 * A
    phiPn = 0.9 * Pn
    omegaPn = Pn / 1.67    
    
    text += f'''
    <div class="col-5">
      <h1>Critical Stress</h1>
      <p>The available critical stresses may be interpolated from AISC <i>Manual</i> Table 4-14 or calculated directly as follows.</p>
      <p>Calculate the elastic critical buckling stress, $F_{{e}}$, according to AISC <i>Specification</i> Section E3. As noted in AISC
         <i>Specification</i> Commentary Section E4, torsional buckling of symmetric shapes is a failure mode usually not considered in 
         the design of hot-rolled columns. This failure mode generally does not govern unless the section is manufactured from relatively 
         thin plates or a torsional unbraced length significantly larger than the <i>y-y</i> axis flexural unbraced length is present.</p>
      <ul>
        <li>
          $F_{{e}} = \\frac{{\pi ^{{2}}E}}{{(\\frac{{L_{{c}}}}{{r}})^{{2}}}} = \\frac{{\pi
          ^{{2}}( {{{'%.2f'%Eksi}}} )}}{{{'%.2f'%Lcr}}} ^{{2}} =
          {{{'%.2f'%Fe}}} \\text{{ ksi}}$
        </li>
      </ul>
      <p>Calculate the flexural buckling stress, $F_{{cr}}$.</p>
      <ul>
        <li>
          $4.71\sqrt{{\\frac{{E}}{{F_{{y}}}}}} = 4.71\sqrt\\frac{{{'%.2f'%Eksi}}}
          {{{'%.2f'%Fy}}} = {{{'%.2f'%Fcr}}}$
        </li>
      </ul>
      <p>Because $\\frac{{L_{{c}}}}{{r}} = {{{'%.2f'%Lcr}}} {buckling_sign}
        {{{'%.2f'%Fcr}}}$</p>
      <ul>
        {buckling_method_equ}
      </ul>
    </div>'''


    text += f'''
    <div class="col-5">
      <h1>Nominal Compressive Strength</h1>
      <ul>
        <li>
          $P_{{n}}=F_{{cr}}A_{{g}} = ({'%.2f'%Fcr1}\\text{{
          ksi}})({'%.2f'%A}\\text{{ in.}}^{{2}}) = {'%.2f'%Pn}\\text{{
          kips}}$
        </li>
      </ul>
    </div>'''
          
       
    text += f'''
    <div class="col-5">  
      <h1>Available Compressive Strength</h1>
      <p>From AISC <i>Specification</i> Section E1, the available compressive strength is:</p>
      <p><b>LRFD:</b></p>
      <ul>
        <li>$\\phi_{{c}} = 0.90$</li>
        <li>$\\phi_{{c}}P_{{n}} = 0.90({'%.2f'%Pn}\\text{{ kips}}) = {'%.2f'%phiPn}\\text{{ kips}}$</li>
      </ul>
      <br />
      <p><b>ASD:</b></p>
      <ul>
        <li>$\\Omega_{{c}} = 1.67$</li>
        <li>$\\frac{{P_{{n}}}}{{\\Omega_{{c}}}} = \\frac{{{'%.2f'%Pn}\\text{{ kips}}}}{{1.67}} = {'%.2f'%omegaPn}\\text{{ kips}}$</li>
      </ul>
    </div>'''

    return text


if __name__ == '__main__':
    app.run(debug = True)

    # app.run(debug = True)
    # app.run(host="0.0.0.0", port=80, debug = True)