from dictionaries.aisc import wide_flange_database, names
from math import floor, log10, sqrt, pi
from static.string_functions import htmlstr, sigfigstr

def wideFlangeText(member,Fy,Eksi,Lcx,Lcy):

  def header():
      
      text = htmlstr(default_indent=10);

      text.newline(r'<div class="section">')
      text.newline(r' <div class="headerText col-4">')
      text.newline(r'   <h1>Wide Flange Steel Members Calculator</h1>')
      text.newline(r' </div>')
      text.newline(r'</div>')

      return text.string
  
  def input(Fy, Eksi, Lcx, Lcy):
      
      text = htmlstr(default_indent=10);

      text.newline(r'<div class="section">')
      text.newline(r' <div class="col-3 alignment">')
      text.newline(r' <div style = "text-align: center;>')
      text.newline(r'  <label class="member_select_label" for="memberDropdown" style="vertical-align: middle" id="test" >Selected Member: </label>')
      text.newline(r'  <select class="memberDropdown" id="memberDropdown" name="memberDropdown">')

      for selectMember in names():
          if selectMember == 'W14X159':
            text.newline(r'<option id="' + f'{selectMember}' + r" value=" + f'{selectMember}' + r'" selected>' + f'{selectMember}' + r'</option>') 
          else:
            text.newline(r'<option id="' + f'{selectMember}' + r" value=" + f'{selectMember}' + r'">' + f'{selectMember}' + r'</option>') 

      text.newline(r'  </select>')
      text.newline(r' </div>')
      text.newline(r' <button class = "generalButton" style = "width: 50%; margin: 10px auto;" type = "submit">Calculate</button>')
      text.newline(r' </div>')
      text.newline(r' <script>')
      text.newline(r'  document.getElementById("memberDropdown").onchange = function () {')
      text.newline(r'   sessionStorage.setItem(')
      text.newline(r'    "flangeSelectItem",')
      text.newline(r'    document.getElementById("memberDropdown").value);')
      text.newline(r'   this.form.submit();};')
      text.newline(r'  if (sessionStorage.getItem("flangeSelectItem")) {')
      text.newline(r'   document.getElementById("memberDropdown").options[')
      text.newline(r'    sessionStorage.getItem("flangeSelectItem")')
      text.newline(r'   ].selected = true;}')
      text.newline(r' </script>')

      text.newline(r' <div class="col-3">')
      text.newline(r'  <label class="member member_space">' + f'{member}' + r'</label> <br />')
      text.newline(r'  <label class = "wideFlangeInputLabel" for="Fy">F<sub>y</sub> : </label>')
      text.newline(r'  <input class="user_input" type="text" id="Fy" value=' + f'{'%g'%(Fy)}' + r' name="Fy" />')
      text.newline(r'  <label class="unit"> ksi</label> <br />')

      text.newline(r'  <label class="wideFlangeInputLabel" for="E">E : </label>')
      text.newline(r'  <input class="user_input" type="text" id="E" value=' + f'{'%g'%(Eksi)}' + r' name="E" />')
      text.newline(r'  <label class="unit"> ksi</label> <br />')

      text.newline(r'  <label class="wideFlangeInputLabel" for="Lcx">L<sub>cx</sub> : </label>')
      text.newline(r'  <input class="user_input" type="text" id="Lcx" value=' + f'{'%g'%(Lcx)}' + r' name="Lcx" />')
      text.newline(r'  <label class="unit"> in</label> <br />')

      text.newline(r'  <label class="wideFlangeInputLabel" for="Lcy">L<sub>cy</sub> : </label>')
      text.newline(r'  <input class="user_input" type="text" id="Lcy" value=' + f'{'%g'%(Lcy)}' + r' name="Lcy" />')
      text.newline(r'  <label class="unit"> in</label>')
      text.newline(r' </div>')
      text.newline(r'</div>')

      return text.string
  
  def output(member, A, rx, ry, bf2tf, htw, Fy, Eksi, Lcx, Lcy):
      outputText =  f'''
        <p>From AISC <i>Manual</i> Table 1-1, the geometric properties for a {member} are as follows:</p>
        <p>$A_{{g}} = {{{'%.2f'%A}}}\\text{{ in.}}^{{2}}$</p> 
        <p>$r_{{x}} = {{{'%.2f'%rx}}}\\text{{ in.}}$</p>
        <p>$r_{{y}} = {{{'%.2f'%ry}}}\\text{{ in.}}$</p>
        <p>$\\dfrac{{b_{{f}}}}{{2t_{{f}}}} = {{{'%.2f'%bf2tf}}}$</p>
        <p>$\\dfrac{{h}}{{t_{{w}}}} = {{{'%.2f'%htw}}}$</p>'''

      outputText += f'''
        <h1>Slenderness Check</h1>
        <p>The width-to-thickness ratio of the flanges of the {member} is:</p>
        <p>$\\dfrac{{b_{{f}}}}{{2t_{{f}}}} = {{{'%.2f'%bf2tf}}}$</p>
        <p>From AISC <i>Specification</i> Table B4.1a, Case 1, the limiting width-to-thickness ratio of the flanges is:</p>
        <p>'''
      
      lambdar_flange = 0.56 * sqrt(Eksi / Fy)
      lambdar_web = 1.49 * sqrt(Eksi / Fy)

      outputText += r'$\begin{aligned}\lambda_{r} &= 0.56\sqrt{\dfrac{E}{F_{y}}} \\ &= 0.56\sqrt{\dfrac{' + sigfigstr(Eksi) + r'\text{ ksi}}{' + \
              sigfigstr(Fy) + r'\text{ ksi}}} \\ &= ' + sigfigstr(lambdar_flange)

      if bf2tf > lambdar_flange:
          outputText += r' < ' + sigfigstr(bf2tf) + r'\end{aligned}$</p>'
          outputText += '\n      <p>therefore the flanges are slender</p>'
      else:
          outputText += r' \geq ' + sigfigstr(bf2tf) + r'\end{aligned}$</p>' 
          outputText += '\n      <p>therefore the flanges are nonslender</p>'
  
      outputText += f'''
        <p>The width-to-thickness ratio of the web of the {member} is:</p>
        <p>$\\dfrac{{h}}{{t_{{w}}}} = {{{'%.2f'%htw}}}$</p>
        <p>From AISC <i>Specification</i> Table B4.1a, Case 5, the limiting width-to-thickness ratio of the web is:</p>
        <p>'''
          
      outputText += r'$\begin{aligned}\lambda_{r} &= 1.49\sqrt{\dfrac{E}{F_{y}}} \\ &= 1.49\sqrt{\dfrac{' + sigfigstr(Eksi) + r'\text{ ksi}}{' + \
              sigfigstr(Fy) + r'\text{ ksi}}} \\ &= ' + sigfigstr(lambdar_web)
          
      if htw > lambdar_web:
          outputText += r' < ' + sigfigstr(htw) + r'\end{aligned}$</p>'
          # + r'$; therefore the web is slender'      ----------- This line throws an error. Is it meant to be here?
          outputText += '\n      <p>therefore the web is slender</p>\n'
          
      else:
          outputText += r' \geq ' + sigfigstr(htw) + r'\end{aligned}$</p>'
          outputText += '\n      <p>therefore the web is nonslender</p>\n'

        
      if bf2tf > lambdar_flange:
          if htw > lambdar_web:
              outputText += r'      <p>Because the web and flanges are slender, the strength must be computed using AISC <i>Specification</i> Section E6 and will not be shown here.</p>'
              return outputText
          else:
              outputText += r'      <p>Because the flanges are slender, the strength must be computed using AISC <i>Specification</i> Section E6 and will not be shown here.</p>'
              return outputText
      else:
          if htw > lambdar_web:
              outputText += r'      <p>Because the web is slender, the strength must be computed using AISC <i>Specification</i> Section E6 and will not be shown here.</p>'
              return outputText
          else:
              outputText += r'      <p>Because the web and flanges are nonslender, the limit state of local buckling does not apply and the strength is computed according to AISC <i>Specification</i> Section E3.</p>'

      # Gets Critical Stresses Data
      outputText += f'''
        <h1>Slenderness Ratio</h1>
        <p>'''

      outputText += r'$\dfrac{L_{cx}}{r_x} = \dfrac{' + sigfigstr(Lcx) + r'\text{ in.}}{' + \
              sigfigstr(rx) + r'\text{ in.}} = ' + sigfigstr(Lcx/rx) + r'$'

      outputText += f'''</p>
        <p>'''

      outputText += r'$\dfrac{L_{cy}}{r_y} = \dfrac{' + sigfigstr(Lcy) + r'\text{ in.}}{' + \
              sigfigstr(ry) + r'\text{ in.}} = ' + sigfigstr(Lcy/ry) + r'$'

      outputText += f'''</p>
        <p>'''
        
      if Lcx/rx > Lcy/ry:
          outputText += r'Because $\dfrac{L_{cx}}{r_x} > \dfrac{L_{cy}}{r_y}$, major-axis buckling controls and $\dfrac{L_{c}}{r} =  ' + sigfigstr(Lcx/rx) + '$'
          Lc_over_r = Lcx/rx
      else:
          outputText += r'Because $\dfrac{L_{cy}}{r_y} > \dfrac{L_{cx}}{r_x}$, minor-axis buckling controls and $\dfrac{L_{c}}{r} =  ' + sigfigstr(Lcy/ry) + '$'
          Lc_over_r = Lcy/ry

      
      outputText += f'''
        <h1>Nominal Compressive Strength</h1>

        <p>The available critical stresses may be interpolated from AISC <i>Manual</i> Table 4-14 or calculated directly according to AISC <i>Specification</i> Section E3 as follows.</p>
        <p>Calculate the elastic critical buckling stress, $F_{{e}}$</p>
        <p>'''

      Fe = pi**2 * Eksi / Lc_over_r**2
      outputText += r'$\begin{aligned}F_e &= \dfrac{\pi^2 E}{\left(\dfrac{L_c}{r}\right)^2} \\' + \
              r'&= \dfrac{\pi^2 (' + sigfigstr(Eksi) + r'\text{ ksi})}{(' + sigfigstr(Lc_over_r) + r')^2} \\' + \
              r'&= ' + sigfigstr(Fe) + r'\text{ ksi} \end{aligned}$</p>' 

      outputText += f'''
        <p>Calculate the nominal stress, $F_{{n}}$</p>
        <p>'''

      outputText += r'$4.71\sqrt{\dfrac{E}{F_y}} = 4.71\sqrt{\dfrac{' + sigfigstr(Eksi) + r'\text{ ksi}}{' + sigfigstr(Fy) + r'\text{ ksi}}} = ' + sigfigstr(4.71*sqrt(Eksi/Fy)) + r'$'
      
      outputText += f'''</p>
        <p>'''
      
      if Lc_over_r <= 4.71*sqrt(Eksi/Fy):
          outputText += r'Because $\dfrac{L_c}{r} = ' + sigfigstr(Lc_over_r) + r'\leq 4.71\sqrt{\dfrac{E}{F_y}} = ' + sigfigstr(4.71*sqrt(Eksi/Fy)) + r'$, inelastic buckling governs and $F_n$ is determined using AISC <i>Specification</i> Equation E3-2'

          outputText += f'''</p>
        <p>'''


          Fn = 0.658**(Fy/Fe)*Fy

          outputText += r'$\begin{aligned}F_n &= \left(0.658^{\dfrac{F_y}{F_e}}\right)F_y \\' + \
                  r'&= \left[0.658^\dfrac{' + sigfigstr(Fy) + r'\text{ ksi}}{' + sigfigstr(Fe) + r'\text{ ksi}}\right](' + sigfigstr(Fy) + r'\text{ ksi}) \\' + \
                  r'&=' + sigfigstr(Fn) + r'\text{ ksi} \end{aligned}$</p>'
                  
      else:
          outputText += r'Because $\dfrac{L_c}{r} = ' + sigfigstr(Lc_over_r) + r'> 4.71\sqrt{\dfrac{E}{F_y}} = ' + sigfigstr(4.71*sqrt(Eksi/Fy)) + r'$, elastic buckling governs and $F_n$ is determined using AISC <i>Specification</i> Equation E3-3'
      
          outputText += f'''</p>
        <p>'''

          Fn = 0.877 * Fe

          outputText += r'$\begin{aligned}F_n &= 0.877 F_e \\' + \
                  r'&= 0.877 (' + sigfigstr(Fe) + r'\text{ ksi}) \\' + \
                  r'&=' + sigfigstr(Fn) + r'\text{ ksi} \end{aligned}$</p>'


      outputText += f'''
        <p>Calculate the nominal axial compressive strength, $P_{{n}}$, using  AISC <i>Specification</i> Equation E3-1.</p>
        <p>'''
      Pn = Fn * A

      outputText += r'$P_n = F_n A_g = (' + sigfigstr(Fn) + r'\text{ ksi})(' + sigfigstr(A) + r'\text{ in.}^2) = ' + sigfigstr(Pn) + r'\text{ kips} $</p>'

      phiPn = 0.9 * Pn
      omegaPn = Pn / 1.67 
      
      outputText += f'''
        <p>For LRFD:</p>
        <p>'''

      outputText += r'$\phi_c P_n = 0.90 (' + sigfigstr(Pn) + r'\text{ kips}) = ' + sigfigstr(0.9*Pn) + r'\text{ kips} $</p>'

      outputText += f'''
        <p>For ASD:</p>
        <p>'''

      outputText += r'$\dfrac{P_n}{\Omega_c} = \dfrac{(' + sigfigstr(Pn) + r'\text{ kips})}{1.67} = ' + sigfigstr(Pn/1.67) + r'\text{ kips} $</p>'
      
      return outputText
  
  def footer():
      text = htmlstr(default_indent=10);
      text.newline('Developed by Jonathan Smith and Mark Denavit at the University of Tennessee, Knoxville.', tag='p')
      text.newline('This work was supported by the Naval Engineering Education Consortium [Award Number N00174-22-1-0017].', tag='p')
      return text.string

  # Check output
  if member == None:
      return header(), input(Fy, Eksi, Lcx, Lcy), '', footer()
  elif Fy <= 0:
      return header(), input(Fy, Eksi, Lcx, Lcy), 'Steel yield stress must be greater than zero', footer()       
  elif Eksi <= 0:
      return header(), input(Fy, Eksi, Lcx, Lcy), 'Modulus of elasticity must be greater than zero', footer()
  elif Lcx < 0 or Lcy < 0:
      return header(), input(Fy, Eksi, Lcx, Lcy), 'The effective lengths must be greater than or equal to zero', footer()
  else:
    # Section Properties Data
    A = wide_flange_database[member]['A']
    rx = wide_flange_database[member]['rx']
    ry = wide_flange_database[member]['ry']
    bf2tf = wide_flange_database[member]['bf/2tf']
    htw = wide_flange_database[member]['h/tw']

    return header(), input(Fy, Eksi, Lcx, Lcy), output(member, A, rx, ry, bf2tf, htw, Fy, Eksi, Lcx, Lcy), footer()
