from .base_class import Page
from flask import request
from static.string_functions import htmlstr, sigfigstr

from dictionaries.aisc import wide_flange_database, names
from math import sqrt, pi

class WideFlangeColumnBasic(Page):
    
  def __init__(self,member,Fy_str,E_str,Lcx_str,Lcy_str):
      self.member = member
      self.Fy_str = Fy_str
      self.E_str = E_str
      self.Lcx_str = Lcx_str
      self.Lcy_str = Lcy_str
      self.name = r'/wide_flange_column_basic'
      self.title = 'Wide Flange Steel Members'

  @classmethod
  def from_page(cls):
      member = request.form.get('memberDropdown')
      if member is None:
          member = 'W14X159'

      Fy_str = request.values.get('Fy')
      if Fy_str is None:
          Fy_str = '50'
         
      E_str = request.values.get('E')
      if E_str is None:
          E_str = '29000'
          
      Lcx_str = request.values.get('Lcx')
      if Lcx_str is None:
          Lcx_str = '240'
          
      Lcy_str = request.values.get('Lcy')
      if Lcy_str is None:
          Lcy_str = '240'  
      
      return cls(member,Fy_str,E_str,Lcx_str,Lcy_str)
      

  def header(self):
      text = htmlstr(default_indent=10);
      text.newline('Axial Compressive Strength of Wide Flange Steel Columns', tag='h1')
      text.newline('Example calculation of the available strength (ASD and LRFD) of wide flange steel columns without slender elements for the limit state of flexural buckling according to the 2022 AISC <i>Specification</i> and 16th Edition AISC <i>Manual</i>.', tag='p')
      return text.string
  
  def input(self):
      
      text = htmlstr(default_indent=10);

      text.newline(r'<div class="input_wrapper">')     
      text.newline(r'  <label class="input_label" for="memberDropdown">Wide Flange Section: </label>')
      text.newline(r'  <select class="input_box" id="memberDropdown" name="memberDropdown">')
      for selectMember in names():
          if selectMember == self.member:
            text.newline(r'    <option id="' + f'{selectMember}"' + r" value=" + f'"{selectMember}' + r'" selected>' + f'{selectMember}' + r'</option>')
          else:
            text.newline(r'    <option id="' + f'{selectMember}"' + r" value=" + f'"{selectMember}' + r'">' + f'{selectMember}' + r'</option>') 
      text.newline(r'  </select>')
      text.newline(r'  <label class="input_units">&nbsp;</label>')


      text.newline(r'  <label class="input_label" for="Fy">$F_y$ (specified minimum yield stress):</label>')
      text.newline(r'  <input class="input_box" type="text" id="Fy" value="' + self.Fy_str + r'" name="Fy" />')
      text.newline(r'  <label class="input_units">ksi</label>')

      text.newline(r'  <label class="input_label" for="E">$E$ (modulus of elasticity):</label>')
      text.newline(r'  <input class="input_box" type="text" id="E" value="' + self.E_str + r'" name="E" />')
      text.newline(r'  <label class="input_units">ksi</label>')

      text.newline(r'  <label class="input_label" for="Lcx">$L_{cx}$ (effective length for major-axis buckling):</label>')
      text.newline(r'  <input class="input_box" type="text" id="Lcx" value="' + self.Lcx_str + r'" name="Lcx" />')
      text.newline(r'  <label class="input_units">in.</label>')

      text.newline(r'  <label class="input_label" for="Lcy">$L_{cy}$ (effective length for minor-axis buckling):</label>')
      text.newline(r'  <input class="input_box" type="text" id="Lcy" value="' + self.Lcy_str + r'" name="Lcy" />')
      text.newline(r'  <label class="input_units" for="Lcy">in.</label>')
      text.newline(r'</div>')


      text.newline(r'<button class = "generalButton" style="display: block; margin-top: 3px;" type = "submit">Calculate</button>')

      text.newline(r'<script>')
      text.newline(r'  document.getElementById("memberDropdown").onchange = function () {')
      text.newline(r'    sessionStorage.setItem("flangeSelectItem",document.getElementById("memberDropdown").value);')
      text.newline(r'    this.form.submit();')
      text.newline(r'  };')
      text.newline(r'  if (sessionStorage.getItem("flangeSelectItem")) {')
      text.newline(r'    document.getElementById("memberDropdown").options[sessionStorage.getItem("flangeSelectItem")].selected = true;')
      text.newline(r'  }')
      text.newline(r'</script>')

      return text.string
  
  def output(self):
      text = htmlstr(default_indent=10);
      
      # Check Input
      bad_input = False
      
      try:
        Fy = float(self.Fy_str)
      except:
        bad_input = True
        text.newline(r'The yield stress, $F_y$, must be a number', tag='p')

      try:
        E = float(self.E_str)
      except:
        bad_input = True
        text.newline(r'The modulus of elasticity, $E$, must be a number', tag='p')
        
      try:
        Lcx = float(self.Lcx_str)
      except:
        bad_input = True
        text.newline(r'The effective length about the x-axis, $L_{cx}$, must be a number', tag='p')
        
      try:
        Lcy = float(self.Lcy_str)
      except:
        bad_input = True
        text.newline(r'The effective length about the y-axis, $L_{cy}$, must be a number', tag='p')

      if bad_input:
        return text.string

            
      if self.member == None:
        text.newline(f'Error: member must be defined.', tag='p')
        bad_input = True

      if Fy <= 0:
        text.newline(f'Error: steel yield stress must be greater than zero.', tag='p')
        bad_input = True

      if E <= 0:
        text.newline(f'Error: modulus of elasticity stress must be greater than zero.', tag='p')
        bad_input = True
      
      if Lcx < 0 or Lcy < 0:
        text.newline(f'Error: effective lengths must be greater than or equal to zero.', tag='p')
        bad_input = True
     
      if bad_input:
        return text.string
      
      # Section Properties Data
      A = wide_flange_database[self.member]['A']
      rx = wide_flange_database[self.member]['rx']
      ry = wide_flange_database[self.member]['ry']
      bf2tf = wide_flange_database[self.member]['bf/2tf']
      htw = wide_flange_database[self.member]['h/tw']

      text.newline(r'Cross-Sectional Properties', tag='h2')

      text.newline(f'From AISC <i>Manual</i> Table 1-1, the geometric properties for a {self.member} are as follows.', tag='p')
      text.newline(r'$A_g = ' + sigfigstr(A) + r'\text{ in.}^2$', tag='p', cls='eqn') 
      text.newline(r'$r_x = ' + sigfigstr(rx) + r'\text{ in.}$', tag='p', cls='eqn')
      text.newline(r'$r_y = ' + sigfigstr(ry) + r'\text{ in.}$', tag='p', cls='eqn')
      text.newline(r'$\dfrac{b_f}{2t_f} = ' + sigfigstr(bf2tf) + '$', tag='p', cls='eqn')
      text.newline(r'$\dfrac{h}{t_w} = ' + sigfigstr(htw) + '$', tag='p', cls='eqn')

      text.newline(r'Slenderness Check', tag='h2')
      
      # Check flange slenderness
      lambdar_flange = 0.56 * sqrt(E/Fy)

      text.newline(f'The width-to-thickness ratio of the flanges of the {self.member} is:', tag='p')
      text.newline(r'$\dfrac{b_f}{2t_f} = ' + sigfigstr(bf2tf) + '$', tag='p', cls='eqn')
      text.newline(r'From AISC <i>Specification</i> Table B4.1a, Case 1, the limiting width-to-thickness ratio of the flanges is:', tag='p')
      
      if bf2tf > lambdar_flange:
          compare_result1 = r' < '
          compare_result2 = 'slender'         
      else:
          compare_result1 = r' \geq '
          compare_result2 = 'nonslender'          

      text.newline(r'$\begin{aligned}\lambda_{r} &= 0.56\sqrt{\dfrac{E}{F_{y}}} \\ &= 0.56\sqrt{\dfrac{' + sigfigstr(E) + r'\text{ ksi}}{' + \
              sigfigstr(Fy) + r'\text{ ksi}}} \\ &= ' + sigfigstr(lambdar_flange) + compare_result1 + sigfigstr(bf2tf) + r'\end{aligned}$', tag='p', cls='eqn')
      text.newline(f'therefore the flanges are {compare_result2}.', tag='p')
      
      # Check web slenderness
      lambdar_web = 1.49 * sqrt(E/Fy)

      text.newline(f'The width-to-thickness ratio of the web of the {self.member} is:', tag='p')
      text.newline(r'$\dfrac{h}{t_w} = ' + sigfigstr(htw) + '$', tag='p', cls='eqn')
      text.newline(r'From AISC <i>Specification</i> Table B4.1a, Case 5, the limiting width-to-thickness ratio of the web is:', tag='p')
          
      if htw > lambdar_web:
          compare_result1 = r' < '
          compare_result2 = 'slender'         
      else:
          compare_result1 = r' \geq '
          compare_result2 = 'nonslender'

      text.newline(r'$\begin{aligned}\lambda_{r} &= 1.49\sqrt{\dfrac{E}{F_{y}}} \\ &= 1.49\sqrt{\dfrac{' + sigfigstr(E) + r'\text{ ksi}}{' + \
              sigfigstr(Fy) + r'\text{ ksi}}} \\ &= ' + sigfigstr(lambdar_web) + compare_result1 + sigfigstr(htw) + r'\end{aligned}$', tag='p', cls='eqn')
      text.newline(f'therefore the web is {compare_result2}.', tag='p')

      # Check if Section E3 applies
      if bf2tf > lambdar_flange:
          if htw > lambdar_web:
              text.newline(r'Because the web and flanges are slender, the strength must be computed using AISC <i>Specification</i> Section E6 and will not be shown here.', tag='p')
              return text.string
          else:
              text.newline(r'Because the flanges are slender, the strength must be computed using AISC <i>Specification</i> Section E6 and will not be shown here.', tag='p')
              return text.string
      else:
          if htw > lambdar_web:
              text.newline(r'Because the web is slender, the strength must be computed using AISC <i>Specification</i> Section E6 and will not be shown here.', tag='p')
              return text.string
          else:
              text.newline(r'Because the web and flanges are nonslender, the limit state of local buckling does not apply and the strength is computed according to AISC <i>Specification</i> Section E3.', tag='p')

      # Gets Critical Stresses Data
      text.newline(r'Slenderness Ratio', tag='h2')

      text.newline(r'$\dfrac{L_{cx}}{r_x} = \dfrac{' + sigfigstr(Lcx) + r'\text{ in.}}{' + \
              sigfigstr(rx) + r'\text{ in.}} = ' + sigfigstr(Lcx/rx) + r'$', tag='p', cls='eqn')


      text.newline(r'$\dfrac{L_{cy}}{r_y} = \dfrac{' + sigfigstr(Lcy) + r'\text{ in.}}{' + \
              sigfigstr(ry) + r'\text{ in.}} = ' + sigfigstr(Lcy/ry) + r'$', tag='p', cls='eqn')

        
      if Lcx/rx > Lcy/ry:
          text.newline(r'Because $\dfrac{L_{cx}}{r_x} > \dfrac{L_{cy}}{r_y}$, major-axis buckling controls and $\dfrac{L_{c}}{r} =  ' + sigfigstr(Lcx/rx) + '$', tag='p')
          Lc_over_r = Lcx/rx
      else:
          text.newline(r'Because $\dfrac{L_{cy}}{r_y} > \dfrac{L_{cx}}{r_x}$, minor-axis buckling controls and $\dfrac{L_{c}}{r} =  ' + sigfigstr(Lcy/ry) + '$', tag='p')
          Lc_over_r = Lcy/ry

      
      text.newline(r'Nominal Compressive Strength', tag='h2')

      text.newline(r'The available critical stresses may be interpolated from AISC <i>Manual</i> Table 4-14 or calculated directly according to AISC <i>Specification</i> Section E3 as follows.', tag='p')
      text.newline(r'Calculate the elastic critical buckling stress, $F_{{e}}$', tag='p')

      Fe = pi**2 * E / Lc_over_r**2
      text.newline(r'$\begin{aligned}F_e &= \dfrac{\pi^2 E}{\left(\dfrac{L_c}{r}\right)^2} \\' + \
              r'&= \dfrac{\pi^2 (' + sigfigstr(E) + r'\text{ ksi})}{(' + sigfigstr(Lc_over_r) + r')^2} \\' + \
              r'&= ' + sigfigstr(Fe) + r'\text{ ksi} \end{aligned}$', tag='p', cls='eqn')

      text.newline('Calculate the nominal stress, $F_{{n}}$', tag='p')

      text.newline(r'$4.71\sqrt{\dfrac{E}{F_y}} = 4.71\sqrt{\dfrac{' + sigfigstr(E) + r'\text{ ksi}}{' + sigfigstr(Fy) + r'\text{ ksi}}} = ' + sigfigstr(4.71*sqrt(E/Fy)) + r'$', tag='p', cls='eqn')
           
      if Lc_over_r <= 4.71*sqrt(E/Fy):
          text.newline(r'Because $\dfrac{L_c}{r} = ' + sigfigstr(Lc_over_r) + r'\leq 4.71\sqrt{\dfrac{E}{F_y}} = ' + sigfigstr(4.71*sqrt(E/Fy)) + r'$, inelastic buckling governs and $F_n$ is determined using AISC <i>Specification</i> Equation E3-2', tag='p')

          Fn = 0.658**(Fy/Fe)*Fy

          text.newline(r'$\begin{aligned}F_n &= \left(0.658^{\dfrac{F_y}{F_e}}\right)F_y \\' + \
                  r'&= \left[0.658^\dfrac{' + sigfigstr(Fy) + r'\text{ ksi}}{' + sigfigstr(Fe) + r'\text{ ksi}}\right](' + sigfigstr(Fy) + r'\text{ ksi}) \\' + \
                  r'&=' + sigfigstr(Fn) + r'\text{ ksi} \end{aligned}$', tag='p', cls='eqn')
                  
      else:
          text.newline(r'Because $\dfrac{L_c}{r} = ' + sigfigstr(Lc_over_r) + r'> 4.71\sqrt{\dfrac{E}{F_y}} = ' + sigfigstr(4.71*sqrt(E/Fy)) + r'$, elastic buckling governs and $F_n$ is determined using AISC <i>Specification</i> Equation E3-3', tag='p')
      
          Fn = 0.877 * Fe

          text.newline(r'$\begin{aligned}F_n &= 0.877 F_e \\' + \
                  r'&= 0.877 (' + sigfigstr(Fe) + r'\text{ ksi}) \\' + \
                  r'&=' + sigfigstr(Fn) + r'\text{ ksi} \end{aligned}$', tag='p', cls='eqn')


      text.newline('Calculate the nominal axial compressive strength, $P_{{n}}$, using  AISC <i>Specification</i> Equation E3-1.', tag='p')

      Pn = Fn * A

      text.newline(r'$P_n = F_n A_g = (' + sigfigstr(Fn) + r'\text{ ksi})(' + sigfigstr(A) + r'\text{ in.}^2) = ' + sigfigstr(Pn) + r'\text{ kips}$', tag='p', cls='eqn') 

      text.newline(r'Available Compressive Strength', tag='h2')
      text.newline('For LRFD:', tag='p')
      text.newline(r'$\phi_c P_n = 0.90 (' + sigfigstr(Pn) + r'\text{ kips}) = ' + sigfigstr(0.9*Pn) + r'\text{ kips}$', tag='p', cls='eqn')     
      text.newline('For ASD:', tag='p')
      text.newline(r'$\dfrac{P_n}{\Omega_c} = \dfrac{(' + sigfigstr(Pn) + r'\text{ kips})}{1.67} = ' + sigfigstr(Pn/1.67) + r'\text{ kips} $', tag='p', cls='eqn')     
      
      return text.string
  
  def footer(self):
      text = htmlstr(default_indent=10);
      text.newline('Developed by Jonathan Smith and Mark Denavit at the University of Tennessee, Knoxville.', tag='p')
      text.newline('This work was supported by the Naval Engineering Education Consortium [Award Number N00174-22-1-0017].', tag='p')
      return text.string
