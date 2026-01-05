from .base_class import Page
from flask import request
from static.string_functions import htmlstr, sigfigstr

from dictionaries.aisc import wide_flange_database, names
from math import sqrt, pi

class WideFlangeBeamBasic(Page):
    
    def __init__(self,member,Fy_str,E_str,Lb_str,Cb_str):
        self.member = member
        self.Fy_str = Fy_str
        self.E_str = E_str
        self.Lb_str = Lb_str
        self.Cb_str = Cb_str
        self.name = r'/wide_flange_beam_basic'
        self.title = 'Wide Flange Steel Members'
   
    @classmethod
    def from_page(cls):
        member = request.form.get('memberDropdown')
        if member is None:
            member = 'W30X90'
   
        Fy_str = request.values.get('Fy')
        if Fy_str is None:
            Fy_str = '50'
           
        E_str = request.values.get('E')
        if E_str is None:
            E_str = '29000'
            
        Lb_str = request.values.get('Lb')
        if Lb_str is None:
            Lb_str = '240'
            
        Cb_str = request.values.get('Cb')
        if Cb_str is None:
            Cb_str = '1.00'  
        
        return cls(member,Fy_str,E_str,Lb_str,Cb_str)
        
   
    def header(self):
        text = htmlstr(default_indent=10);
        text.newline('Major-axis Flexural and Shear Strength of Wide Flange Steel Beams', tag='h1')
        text.newline('Example calculation of the available strength (ASD and LRFD) of compact wide flange steel beams for the limit state of flexural yielding, lateral-torsional buckling, and shear yielding according to the 2022 AISC <i>Specification</i> and 16th Edition AISC <i>Manual</i>.', tag='p')
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
   
        text.newline(r'  <label class="input_label" for="Lb">$L_b$ (unbraced length):</label>')
        text.newline(r'  <input class="input_box" type="text" id="Lb" value="' + self.Lb_str + r'" name="Lb" />')
        text.newline(r'  <label class="input_units">in.</label>')
   
        text.newline(r'  <label class="input_label" for="Cb">$C_b$ (lateral-torsional buckling modification factor):</label>')
        text.newline(r'  <input class="input_box" type="text" id="Cb" value="' + self.Cb_str + r'" name="Cb" />')
        text.newline(r'  <label class="input_units" for="Cb"></label>')
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
            Lb = float(self.Lb_str)
        except:
            bad_input = True
            text.newline(r'The unbraced length, $L_b$, must be a number', tag='p')
          
        try:
            Cb = float(self.Cb_str)
        except:
            bad_input = True
            text.newline(r'The lateral-torsional buckling modification factor, $C_{b}$, must be a number', tag='p')
   
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
        
        if Lb < 0:
            text.newline(f'Error: the unbraced length must be greater than or equal to zero.', tag='p')
            bad_input = True
   
        if Cb < 0:
            text.newline(f'Error: lateral-torsional buckling modification factor must be greater than or equal to zero.', tag='p')
            bad_input = True
       
        if bad_input:
            return text.string
        
        # Section Properties Data
        d = wide_flange_database[self.member]['d']
        tw = wide_flange_database[self.member]['tw']
        Sx = wide_flange_database[self.member]['Sx']
        Zx = wide_flange_database[self.member]['Zx']
        ry = wide_flange_database[self.member]['ry']
        bf2tf = wide_flange_database[self.member]['bf/2tf']
        htw = wide_flange_database[self.member]['h/tw']
        rts = wide_flange_database[self.member]['rts']
        ho = wide_flange_database[self.member]['ho']
        J = wide_flange_database[self.member]['J']
        Cw = wide_flange_database[self.member]['Cw']

        text.newline(r'Cross-Sectional Properties', tag='h2')
   
        text.newline(f'From AISC <i>Manual</i> Table 1-1, the geometric properties for a {self.member} are as follows.', tag='p')
        text.newline(r'$d = ' + sigfigstr(d) + r'\text{ in.}$', tag='p', cls='eqn')
        text.newline(r'$t_w = ' + sigfigstr(tw) + r'\text{ in.}$', tag='p', cls='eqn')
        text.newline(r'$S_x = ' + sigfigstr(Sx) + r'\text{ in.}^3$', tag='p', cls='eqn')
        text.newline(r'$Z_x = ' + sigfigstr(Zx) + r'\text{ in.}^3$', tag='p', cls='eqn')
        text.newline(r'$r_y = ' + sigfigstr(ry) + r'\text{ in.}$', tag='p', cls='eqn')
        text.newline(r'$\dfrac{b_f}{2t_f} = ' + sigfigstr(bf2tf) + '$', tag='p', cls='eqn')
        text.newline(r'$\dfrac{h}{t_w} = ' + sigfigstr(htw) + '$', tag='p', cls='eqn')
        text.newline(r'$r_{ts} = ' + sigfigstr(rts) + r'\text{ in.}$', tag='p', cls='eqn')
        text.newline(r'$h_o = ' + sigfigstr(ho) + r'\text{ in.}$', tag='p', cls='eqn')
        text.newline(r'$J = ' + sigfigstr(J) + r'\text{ in.}^4$', tag='p', cls='eqn')
        text.newline(r'$C_w = ' + sigfigstr(Cw) + r'\text{ in.}^6$', tag='p', cls='eqn')

   
        text.newline(r'Flexural Strength', tag='h2')
   
        text.newline(r'Slenderness Check', tag='h3')
        
        # Check flange slenderness
        lambda_p_flange = 0.38 * sqrt(E/Fy)
   
        text.newline(f'The width-to-thickness ratio of the flanges of the {self.member} is:', tag='p')
        text.newline(r'$\dfrac{b_f}{2t_f} = ' + sigfigstr(bf2tf) + '$', tag='p', cls='eqn')
        text.newline(r'From AISC <i>Specification</i> Table B4.1b, Case 10, the limiting width-to-thickness ratio, $\lambda_p$, of the flanges is:', tag='p')
        
        if bf2tf > lambda_p_flange:
            compare_result1 = r' < '
            compare_result2 = 'not compact'         
        else:
            compare_result1 = r' \geq '
            compare_result2 = 'compact'          
   
        text.newline(r'$\begin{aligned}\lambda_p &= 0.38\sqrt{\dfrac{E}{F_{y}}} \\ &= 0.38\sqrt{\dfrac{' + sigfigstr(E) + r'\text{ ksi}}{' + \
                sigfigstr(Fy) + r'\text{ ksi}}} \\ &= ' + sigfigstr(lambda_p_flange) + compare_result1 + sigfigstr(bf2tf) + r'\end{aligned}$', tag='p', cls='eqn')
        text.newline(f'therefore the flanges are {compare_result2}.', tag='p')
        
        # Check web slenderness
        lambda_p_web = 3.76 * sqrt(E/Fy)
   
        text.newline(f'The width-to-thickness ratio of the web of the {self.member} is:', tag='p')
        text.newline(r'$\dfrac{h}{t_w} = ' + sigfigstr(htw) + '$', tag='p', cls='eqn')
        text.newline(r'From AISC <i>Specification</i> Table B4.1b, Case 15, the limiting width-to-thickness ratio, $\lambda_p$, of the web is:', tag='p')
            
        if htw > lambda_p_web:
            compare_result1 = r' < '
            compare_result2 = 'slender'         
        else:
            compare_result1 = r' \geq '
            compare_result2 = 'nonslender'
   
        text.newline(r'$\begin{aligned}\lambda_p &= 3.76\sqrt{\dfrac{E}{F_{y}}} \\ &= 3.76\sqrt{\dfrac{' + sigfigstr(E) + r'\text{ ksi}}{' + \
                sigfigstr(Fy) + r'\text{ ksi}}} \\ &= ' + sigfigstr(lambda_p_web) + compare_result1 + sigfigstr(htw) + r'\end{aligned}$', tag='p', cls='eqn')
        text.newline(f'therefore the web is {compare_result2}.', tag='p')
   
        # Check if Section E3 applies
        if bf2tf > lambda_p_flange:
            if htw > lambda_p_web:
                text.newline(r'Because neither the web nor flanges are compact, the flexural strength cannot be computed using AISC <i>Specification</i> Section F2 and the calculation will not be shown here.', tag='p')
                show_flexural_strength = False
            else:
                text.newline(r'Because the flanges are not compact, the flexural strength cannot be computed using AISC <i>Specification</i> Section F2 and the calculation will not be shown here.', tag='p')
                show_flexural_strength = False
        else:
            if htw > lambda_p_web:
                text.newline(r'Because the web is not compact, the flexural strength cannot be computed using AISC <i>Specification</i> Section F2 and the calculation will not be shown here.', tag='p')
                show_flexural_strength = False
            else:
                text.newline(r'Because the web and flanges are compact, the limit state of local buckling does not apply and the strength is computed according to AISC <i>Specification</i> Section F2.', tag='p')
                show_flexural_strength = True
   
        if show_flexural_strength:
            # Flexural Yielding
            text.newline(r'Flexual Yielding', tag='h3')
            
            Mp = Fy*Zx
            
            text.newline('Calculate the nominal flexural strength for the limit state of yielding (also referred to as the plastic moment) according to AISC <i>Specification</i> Section F2.1.', tag='p')
            
            text.newline(r'$\begin{aligned}M_n &= M_p = F_yZ_x \\ &= (' + sigfigstr(Fy) + r'\text{ ksi})(' + \
                    sigfigstr(Zx) + r'\text{ in.}^3) \\ &= ' + sigfigstr(Mp) + r'\text{ kip-in.} \end{aligned}$', tag='p', cls='eqn')
            
            # Lateral-Torsional Buckling
            text.newline(r'Lateral-Torsional Buckling', tag='h3')
            text.newline(r'The unbraced length is:', tag='p')
            text.newline(r'$L_b = ' + sigfigstr(Lb) + r'\text{ in.}$', tag='p', cls='eqn')
            
            Lp = 1.76*ry*sqrt(E/Fy)
            text.newline(r'Calculate the limiting unbraced length, $L_p$, according to AISC <i>Specification</i> Equation F2-5.', tag='p')
            text.newline(r'$L_p = 1.76 r_y \sqrt{\dfrac{E}{F_y}} = 1.76 (' + sigfigstr(ry) + r'\text{ in.}) \sqrt{\dfrac{' + sigfigstr(E) + r' \text{ ksi}}{' + sigfigstr(Fy) + r' \text{ ksi}}} = ' + sigfigstr(Lp) + r'\text{ in.}$', tag='p', cls='eqn')
       
            if Lb <= Lp:
                LTB_applies = False
                text.newline(r'Lateral-torsional buckling does not apply because $L_b \leq L_p$.', tag='p')
            
            else:
                LTB_applies = True
                text.newline(r'Lateral-torsional buckling applies because $L_b > L_p$.', tag='p')
       
                text.newline(r'From AISC <i>Specification</i> Equation F2-8a, $c = 1$.', tag='p')
       
                c = 1
                Lr = 1.95*rts*E/(0.7*Fy)*sqrt((J*c)/(Sx*ho)+sqrt(((J*c)/(Sx*ho))**2+6.76*(0.7*Fy/E)**2))
                text.newline(r'Compute the limiting unbraced length, $L_r$, according to AISC <i>Specification</i> Equation F2-6.', tag='p')         
                text.newline(r'$\begin{aligned}L_r &= 1.95 r_{ts} \dfrac{E}{0.7F_y} \sqrt{\dfrac{Jc}{S_xh_o} + \sqrt{ \left( \dfrac{Jc}{S_xh_o} \right)^2 + 6.76\left( \dfrac{0.7F_y}{E} \right)^2 }} \\' + 
                    r'&= 1.95 (' + sigfigstr(rts) + r'\text{ in.}) \dfrac{(' + sigfigstr(E) + r'\text{ ksi})}{0.7(' + sigfigstr(Fy) + r'\text{ ksi})} \sqrt{\dfrac{(' + sigfigstr(J) + r'\text{ in.}^4)(1)}{(' + sigfigstr(Sx) + r'\text{ in.}^3)(' + sigfigstr(ho) + r'\text{ in.})} + \sqrt{ \left( \dfrac{(' + sigfigstr(J) + r'\text{ in.}^4)(1)}{(' + sigfigstr(Sx) + r'\text{ in.}^3)(' + sigfigstr(ho) + r'\text{ in.})} \right)^2 + 6.76\left( \dfrac{0.7(' + sigfigstr(Fy) + r'\text{ ksi})}{(' + sigfigstr(E) + r'\text{ ksi})} \right)^2 }} \\' + 
                    r'&= ' + sigfigstr(Lr) + r'\text{ in.}\end{aligned}$', tag='p', cls='eqn')
       
                if Lb <= Lr:
                    text.newline(r'Inelastic lateral-torsional buckling applies because $L_p < L_b \leq L_r$.', tag='p')
       
                    MnLTB = min(Cb*(Mp-(Mp-0.7*Fy*Sx)*(Lb-Lp)/(Lr-Lp)),Mp)
                    text.newline(r'Compute the nominal flexural strength according to AISC <i>Specification</i> Equation F2-2.', tag='p')

                    text.newline(r'$\begin{aligned}M_n &= C_b \left[ M_p - \left(M_p - 0.7F_yS_x \right) \left( \frac{L_b-L_p}{L_r-L_p} \right) \right] \leq M_p \\' + 
                        r'&= (' + sigfigstr(Cb) + r') \left[ (' + sigfigstr(Mp) + r'\text{ kip-in.}) - \left[(' + sigfigstr(Mp) + r'\text{ kip-in.}) - 0.7(' + sigfigstr(Fy) + r'\text{ ksi})(' + sigfigstr(Sx) + r'\text{ in.}^3) \right] \left( \frac{' + sigfigstr(Lb) + r'\text{ in.}-' + sigfigstr(Lp) + r'\text{ in.}}{' + sigfigstr(Lr) + r'\text{ in.}-' + sigfigstr(Lp) + r'\text{ in.}} \right) \right] \leq ' + sigfigstr(Mp) + r'\text{ kip-in.} \\' + 
                        r'&= ' + sigfigstr(MnLTB) + r'\text{ kip-in.}\end{aligned}$', tag='p', cls='eqn')
                
                else:
                    
                    text.newline(r'Elastic lateral-torsional buckling applies because $L_b > L_r$.', tag='p')
       
                    Fcr = Cb*pi**2*E/(Lb/rts)**2*sqrt(1+0.078*((J*c)/(Sx*ho))*(Lb/rts)**2)
                    text.newline(r'Compute the critical stress according to AISC <i>Specification</i> Equation F2-4.', tag='p')
                    text.newline(r'$\begin{aligned}F_{cr} &= \dfrac{C_b \pi^2 E}{\left( \dfrac{L_b}{r_{ts}} \right)^2 } \sqrt{1+0.078\frac{Jc}{S_xh_o} \left( \frac{L_b}{r_{ts}} \right)^2} \\' + 
                        r'&= \dfrac{(' + sigfigstr(Cb) + r') \pi^2 (' + sigfigstr(E) + r'\text{ ksi})}{\left( \dfrac{' + sigfigstr(Lb) + r'\text{ in.}}{' + sigfigstr(rts) + r'\text{ in.}} \right)^2 } \sqrt{1+0.078\frac{(' + sigfigstr(J) + r'\text{ in.}^4)(1)}{(' + sigfigstr(Sx) + r'\text{ in.}^3)(' + sigfigstr(ho) + r'\text{ in.})} \left( \frac{' + sigfigstr(Lb) + r'\text{ in.}}{' + sigfigstr(rts) + r'\text{ in.}} \right)^2} \\' + 
                        r'&= ' + sigfigstr(Fcr) + r'\text{ ksi}\end{aligned}$', tag='p', cls='eqn')
                        
       
                    MnLTB = min(Fcr*Sx,Mp)
                    text.newline(r'Compute the nominal flexural strength according to AISC <i>Specification</i> Equation F2-3.', tag='p')
                    text.newline(r'$\begin{aligned}M_n &= F_{cr}S_x \leq M_p \\' + 
                        r'&= (' + sigfigstr(Fcr) + r'\text{ ksi})(' + sigfigstr(Sx) + r'\text{ in.}^3) \leq ' + sigfigstr(Mp) + r'\text{ kip-in.} \\' + 
                        r'&= ' + sigfigstr(MnLTB) + r'\text{ kip-in.}\end{aligned}$', tag='p', cls='eqn')
       
            text.newline(r'Available Flexural Strength', tag='h3')
            
            if LTB_applies == False:
                Mn = Mp
                text.newline('Because lateral-torsional buckling does not apply, the nominal flexural strength is the plastic moment.', tag='p')
                text.newline(r'$M_n = M_p =' + sigfigstr(Mn) + r'\text{ kip-in.}$', tag='p', cls='eqn')     
            else:
                Mn = min(Mp,MnLTB)
                text.newline('The nominal flexural strength, $M_n$, is the lower value obtained according to the limit states of yielding and lateral-torsional buckling.', tag='p')
                text.newline(r'$\begin{aligned}M_n &= \text{min}(M_{n,yielding},M_{n,LTB}) \\ &= \text{min}(' + sigfigstr(Mp) + r'\text{ kip-in.},' + sigfigstr(MnLTB) + r'\text{ kip-in.}) \\ &= ' + sigfigstr(Mn) + r'\text{ kip-in.}\end{aligned}$', tag='p', cls='eqn')       
            
            text.newline('For LRFD:', tag='p')
            text.newline(r'$\phi_b M_n = 0.90 (' + sigfigstr(Mn) + r'\text{ kip-in.}) = ' + sigfigstr(0.9*Mn) + r'\text{ kip-in.}$', tag='p', cls='eqn')     
            text.newline('For ASD:', tag='p')
            text.newline(r'$\dfrac{M_n}{\Omega_b} = \dfrac{(' + sigfigstr(Mn) + r'\text{ kip-in.})}{1.67} = ' + sigfigstr(Mn/1.67) + r'\text{ kip-in.} $', tag='p', cls='eqn')     
   
        
        text.newline(r'Shear Strength', tag='h2')
        text.newline('Calculate the nominal shear strength according to AISC <i>Specification</i> Section G2.1.', tag='p')
   
        text.newline(f'The width-to-thickness ratio of the web of the {self.member} is:', tag='p')
        text.newline(r'$\dfrac{h}{t_w} = ' + sigfigstr(htw) + '$', tag='p', cls='eqn')
        text.newline(r'AISC <i>Specification</i> Section G2.1(a) applies if $h/t_w \leq 2.24\sqrt{E/F_y}$.', tag='p')
            
        if htw <= 2.24 * sqrt(E/Fy):
            compare_result1 = r' \leq '
        else:
            compare_result1 = r' > '
   
        text.newline(r'$\dfrac{h}{t_w} = ' + sigfigstr(htw) + compare_result1 + r'2.24\sqrt{\dfrac{E}{F_{y}}} = 2.24\sqrt{\dfrac{' + sigfigstr(E) + r'\text{ ksi}}{' + \
                sigfigstr(Fy) + r'\text{ ksi}}} = ' + sigfigstr(2.24*sqrt(E/Fy)) + r'$', tag='p', cls='eqn')
        
        if htw > 2.24 * sqrt(E/Fy):        
            text.newline(r'Because $h/t_w > 2.24\sqrt{E/F_{y}}$, the web shear strength coefficient, $C_{v1}$, must be calculated according to AISC <i>Specification</i> Section G2.1(b). Additionally, the resistance factor and safety factor defined in AISC <i>Specification</i> Section G1 apply.', tag='p')
            
            phi_v = 0.90
            Omega_v = 1.67
            
            kv = 5.34
            text.newline(f'Assume the web is without transverse stiffeners and thus $k_v = 5.34$.', tag='p')

            text.newline(r'Compare $h/t_w$ to $1.10\sqrt{k_vE/F_y}$.', tag='p')

            if htw <= 1.10 * sqrt(kv*E/Fy):
                compare_result1 = r' \leq '
            else:
                compare_result1 = r' > '
       
            text.newline(r'$\dfrac{h}{t_w} = ' + sigfigstr(htw) + compare_result1 + r'1.10\sqrt{\dfrac{k_vE}{F_{y}}} = 1.10\sqrt{\dfrac{(' + sigfigstr(kv,3) + r')(' + sigfigstr(E) + r'\text{ ksi})}{(' + \
                    sigfigstr(Fy) + r'\text{ ksi})}} = ' + sigfigstr(1.10*sqrt(kv*E/Fy)) + r'$', tag='p', cls='eqn')
            
            if htw <= 1.10*sqrt(kv*E/Fy):
                Cv1 = 1.0
                text.newline(r'Beacause $h/t_w \leq 1.10\sqrt{k_vE/F_y}$, $C_{v1} = 1.0$ according to AISC <i>Specification</i> Equation G2-3.', tag='p')

            else:
                Cv1 = 1.10*sqrt(kv*E/Fy)/htw
                text.newline(r'Beacause $h/t_w > 1.10\sqrt{k_vE/F_y}$, calculate $C_{v1}$ according to AISC <i>Specification</i> Equation G2-4.', tag='p')
                text.newline(r'$C_{v1} = \dfrac{1.10\sqrt{k_vE/F_y}}{h/t_w} = \dfrac{1.10\sqrt{(' + sigfigstr(kv,3) + r')(' + sigfigstr(E) + r'\text{ ksi})/(' + sigfigstr(Fy) + r'\text{ ksi})}}{(' + sigfigstr(htw) + r')} = ' + sigfigstr(Cv1) + r'$', tag='p', cls='eqn')
            
        else:
            text.newline(r'Because wide flanges are rolled I-shapes and $h/t_w \leq 2.24\sqrt{E/F_{y}}$, the resistance factor is taken as $\phi_v = 1.00$, the safety factor is taken as $\Omega_v = 1.50$, and the web shear strength coefficient is taken as $C_{v1} = 1.0$ according to AISC <i>Specification</i> Section G2.1(a).', tag='p')
   
            phi_v = 1.00
            Omega_v = 1.50
            Cv1 = 1.0
   
   
        Aw = d*tw        
        text.newline(r'Calculate the area of the web as the overall depth times the web thickness.', tag='p')
        text.newline(r'$A_w = dt_w = (' + sigfigstr(d) + r'\text{ in.})(' + sigfigstr(tw) + r'\text{ in.}) = ' + sigfigstr(Aw) + r'\text{ in.}^2$', tag='p', cls='eqn')
        
        Vn = 0.6*Fy*Aw*Cv1
        text.newline(r'Calculate the nominal shear strength according to AISC <i>Specification</i> Equation G2-1.', tag='p')
        text.newline(r'$V_n = 0.6F_yA_wC_{v1} = 0.6(' + sigfigstr(Fy) + r'\text{ ksi})(' + sigfigstr(Aw) + r'\text{ in.}^2)(' + sigfigstr(Cv1) + r') = ' + sigfigstr(Vn) + r'\text{ kips}$', tag='p', cls='eqn')
        
            
        text.newline(r'Available Shear Strength', tag='h3')
        text.newline('For LRFD:', tag='p')
        text.newline(r'$\phi_v V_n = ' + sigfigstr(phi_v,2) + ' (' + sigfigstr(Vn) + r'\text{ kips}) = ' + sigfigstr(phi_v*Vn) + r'\text{ kips}$', tag='p', cls='eqn')     
        text.newline('For ASD:', tag='p')
        text.newline(r'$\dfrac{V_n}{\Omega_v} = \dfrac{(' + sigfigstr(Vn) + r'\text{ kips})}{' + sigfigstr(Omega_v,3) + '} = ' + sigfigstr(Vn/Omega_v) + r'\text{ kips} $', tag='p', cls='eqn')   
        
        return text.string
    
    def footer(self):
        text = htmlstr(default_indent=10);
        text.newline('Developed by Mark Denavit at the University of Tennessee, Knoxville.', tag='p')
        return text.string
