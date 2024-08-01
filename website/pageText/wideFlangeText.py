from dictionaries.aisc import wide_flange_database, names
from math import floor, log10, sqrt, pi

def sigfigstr(n,sigfigs=4):
    n = float(n)
    sigfigsleft = floor(log10(n)) + 1
    if sigfigsleft > sigfigs:
        n = int(round(n,sigfigs-sigfigsleft))
        return f'{n:0,}'
    else:
        format_str = '{:.' + str(sigfigs-sigfigsleft) + 'f}'
        return format_str.format(n)

def wideFlangeText(member,Fy,Eksi,Lcx,Lcy):

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
      <p>From AISC <i>Manual</i> Table 1-1, the geometric properties for a {member} are as follows:</p>
      <p>$A_{{g}} = {{{'%.2f'%A}}}\\text{{ in.}}^{{2}}$</p> 
      <p>$r_{{x}} = {{{'%.2f'%rx}}}\\text{{ in.}}$</p>
      <p>$r_{{y}} = {{{'%.2f'%ry}}}\\text{{ in.}}$</p>
      <p>$\\dfrac{{b_{{f}}}}{{2t_{{f}}}} = {{{'%.2f'%bf2tf}}}$</p>
      <p>$\\dfrac{{h}}{{t_{{w}}}} = {{{'%.2f'%htw}}}$</p>
    '''

    # Slenderness Check
    lambdar_flange = 0.56 * sqrt(Eksi / Fy)
    lambdar_web = 1.49 * sqrt(Eksi / Fy)

    text += f'''
      <h1>Slenderness Check</h1>
      <p>The width-to-thickness ratio of the flanges of the {member} is:</p>
      <p>$\\dfrac{{b_{{f}}}}{{2t_{{f}}}} = {{{'%.2f'%bf2tf}}}$</p>
      <p>From AISC <i>Specification</i> Table B4.1a, Case 1, the limiting width-to-thickness ratio of the flanges is:</p>
      <p>'''
        
    text += r'$\begin{aligned}\lambda_{r} &= 0.56\sqrt{\dfrac{E}{F_{y}}} \\ &= 0.56\sqrt{\dfrac{' + sigfigstr(Eksi) + r'\text{ ksi}}{' + \
            sigfigstr(Fy) + r'\text{ ksi}}} \\ &= ' + sigfigstr(lambdar_flange)

    if bf2tf > lambdar_flange:
        text += r' < ' + sigfigstr(bf2tf) + r'\end{aligned}$</p>'
        text += '\n      <p>therefore the flanges are slender</p>'
    else:
        text += r' \geq ' + sigfigstr(bf2tf) + r'\end{aligned}$</p>' 
        text += '\n      <p>therefore the flanges are nonslender</p>'
    
    text += f'''
      <p>The width-to-thickness ratio of the web of the {member} is:</p>
      <p>$\\dfrac{{h}}{{t_{{w}}}} = {{{'%.2f'%htw}}}$</p>
      <p>From AISC <i>Specification</i> Table B4.1a, Case 5, the limiting width-to-thickness ratio of the web is:</p>
      <p>'''
        
    text += r'$\begin{aligned}\lambda_{r} &= 1.49\sqrt{\dfrac{E}{F_{y}}} \\ &= 1.49\sqrt{\dfrac{' + sigfigstr(Eksi) + r'\text{ ksi}}{' + \
            sigfigstr(Fy) + r'\text{ ksi}}} \\ &= ' + sigfigstr(lambdar_web)
        
    if htw > lambdar_web:
        text += r' < ' + sigfigstr(htw) + r'\end{aligned}$</p>'
        # + r'$; therefore the web is slender'      ----------- This line throws an error. Is it meant to be here?
        text += '\n      <p>therefore the web is slender</p>\n'
        
    else:
        text += r' \geq ' + sigfigstr(htw) + r'\end{aligned}$</p>'
        text += '\n      <p>therefore the web is nonslender</p>\n'

      
    if bf2tf > lambdar_flange:
        if htw > lambdar_web:
            text += r'      <p>Because the web and flanges are slender, the strength must be computed using AISC <i>Specification</i> Section E6 and will not be shown here.</p>'
            return text
        else:
            text += r'      <p>Because the flanges are slender, the strength must be computed using AISC <i>Specification</i> Section E6 and will not be shown here.</p>'
            return text
    else:
        if htw > lambdar_web:
            text += r'      <p>Because the web is slender, the strength must be computed using AISC <i>Specification</i> Section E6 and will not be shown here.</p>'
            return text
        else:
            text += r'      <p>Because the web and flanges are nonslender, the limit state of local buckling does not apply and the strength is computed according to AISC <i>Specification</i> Section E3.</p>'


    # Gets Critical Stresses Data
    text += f'''
      <h1>Slenderness Ratio</h1>
      <p>'''

    text += r'$\dfrac{L_{cx}}{r_x} = \dfrac{' + sigfigstr(Lcx) + r'\text{ in.}}{' + \
            sigfigstr(rx) + r'\text{ in.}} = ' + sigfigstr(Lcx/rx) + r'$'

    text += f'''</p>
      <p>'''

    text += r'$\dfrac{L_{cy}}{r_y} = \dfrac{' + sigfigstr(Lcy) + r'\text{ in.}}{' + \
            sigfigstr(ry) + r'\text{ in.}} = ' + sigfigstr(Lcy/ry) + r'$'

    text += f'''</p>
      <p>'''
      
    if Lcx/rx > Lcy/ry:
        text += r'Because $\dfrac{L_{cx}}{r_x} > \dfrac{L_{cy}}{r_y}$, major-axis buckling controls and $\dfrac{L_{c}}{r} =  ' + sigfigstr(Lcx/rx) + '$'
        Lc_over_r = Lcx/rx
    else:
        text += r'Because $\dfrac{L_{cy}}{r_y} > \dfrac{L_{cx}}{r_x}$, minor-axis buckling controls and $\dfrac{L_{c}}{r} =  ' + sigfigstr(Lcy/ry) + '$'
        Lc_over_r = Lcy/ry

    
    text += f'''
      <h1>Nominal Compressive Strength</h1>

      <p>The available critical stresses may be interpolated from AISC <i>Manual</i> Table 4-14 or calculated directly according to AISC <i>Specification</i> Section E3 as follows.</p>
      <p>Calculate the elastic critical buckling stress, $F_{{e}}$</p>
      <p>'''

    Fe = pi**2 * Eksi / Lc_over_r**2
    text += r'$\begin{aligned}F_e &= \dfrac{\pi^2 E}{\left(\dfrac{L_c}{r}\right)^2} \\' + \
            r'&= \dfrac{\pi^2 (' + sigfigstr(Eksi) + r'\text{ ksi})}{(' + sigfigstr(Lc_over_r) + r')^2} \\' + \
            r'&= ' + sigfigstr(Fe) + r'\text{ ksi} \end{aligned}$</p>' 

    text += f'''
      <p>Calculate the nominal stress, $F_{{n}}$</p>
      <p>'''

    text += r'$4.71\sqrt{\dfrac{E}{F_y}} = 4.71\sqrt{\dfrac{' + sigfigstr(Eksi) + r'\text{ ksi}}{' + sigfigstr(Fy) + r'\text{ ksi}}} = ' + sigfigstr(4.71*sqrt(Eksi/Fy)) + r'$'
    
    text += f'''</p>
      <p>'''
    
    if Lc_over_r <= 4.71*sqrt(Eksi/Fy):
        text += r'Because $\dfrac{L_c}{r} = ' + sigfigstr(Lc_over_r) + r'\leq 4.71\sqrt{\dfrac{E}{F_y}} = ' + sigfigstr(4.71*sqrt(Eksi/Fy)) + r'$, inelastic buckling governs and $F_n$ is determined using AISC <i>Specification</i> Equation E3-2'

        text += f'''</p>
      <p>'''


        Fn = 0.658**(Fy/Fe)*Fy

        text += r'$\begin{aligned}F_n &= \left(0.658^{\dfrac{F_y}{F_e}}\right)F_y \\' + \
                r'&= \left[0.658^\dfrac{' + sigfigstr(Fy) + r'\text{ ksi}}{' + sigfigstr(Fe) + r'\text{ ksi}}\right](' + sigfigstr(Fy) + r'\text{ ksi}) \\' + \
                r'&=' + sigfigstr(Fn) + r'\text{ ksi} \end{aligned}$</p>'
                
    else:
        text += r'Because $\dfrac{L_c}{r} = ' + sigfigstr(Lc_over_r) + r'> 4.71\sqrt{\dfrac{E}{F_y}} = ' + sigfigstr(4.71*sqrt(Eksi/Fy)) + r'$, elastic buckling governs and $F_n$ is determined using AISC <i>Specification</i> Equation E3-3'
    
        text += f'''</p>
      <p>'''

        Fn = 0.877 * Fe

        text += r'$\begin{aligned}F_n &= 0.877 F_e \\' + \
                r'&= 0.877 (' + sigfigstr(Fe) + r'\text{ ksi}) \\' + \
                r'&=' + sigfigstr(Fn) + r'\text{ ksi} \end{aligned}$</p>'


    text += f'''
      <p>Calculate the nominal axial compressive strength, $P_{{n}}$, using  AISC <i>Specification</i> Equation E3-1.</p>
      <p>'''
    Pn = Fn * A

    text += r'$P_n = F_n A_g = (' + sigfigstr(Fn) + r'\text{ ksi})(' + sigfigstr(A) + r'\text{ in.}^2) = ' + sigfigstr(Pn) + r'\text{ kips} $</p>'

    phiPn = 0.9 * Pn
    omegaPn = Pn / 1.67 
    
    text += f'''
      <p>For LRFD:</p>
      <p>'''

    text += r'$\phi_c P_n = 0.90 (' + sigfigstr(Pn) + r'\text{ kips}) = ' + sigfigstr(0.9*Pn) + r'\text{ kips} $</p>'

    text += f'''
      <p>For ASD:</p>
      <p>'''

    text += r'$\dfrac{P_n}{\Omega_c} = \dfrac{(' + sigfigstr(Pn) + r'\text{ kips})}{1.67} = ' + sigfigstr(Pn/1.67) + r'\text{ kips} $</p>'

    return text
