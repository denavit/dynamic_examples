from math import floor, log10, sqrt, pi
from dictionaries.ASME_B11 import ASME_B11_UN_2A2B_dict
from dictionaries.threads import *
from static.string_functions import htmlstr, sigfigstr

def boltFEDText(bolt, UTSs_str, UTSn_str):

    def boltText_header():
        text = htmlstr(default_indent=10);
        text.newline('Bolt Tensile Strength Calculation According to FED-STD-H28/2B', tag='h1')
        return text.string


    def boltText_input(UTSs_str,UTSn_str):

        text = htmlstr(default_indent=10);

        text.newline(r'<div class="col-4">')
        text.newline(r'  <div style = "justify-content: center";>')
        text.newline(r'     <label class="boltDropdownLabel" for="boltInput" style="vertical-align: middle" >Nominal Size and Threads per Inch:</label>')
        text.newline(r'     <select id="boltDropdown" name="boltDropdown" class = "boltInput">')
        text.newline(r'      <option id="1/4-20" value="1/4-20">1/4-20</option>')
        text.newline(r'      <option id="1/4-28" value="1/4-28">1/4-28</option>')
        text.newline(r'      <option id="1/2-13" value="1/2-13">1/2-13</option>')
        text.newline(r'      <option id="1/2-20" value="1/2-20">1/2-20</option>')
        text.newline(r'      <option id="3/4-10" value="3/4-10">3/4-10</option>')
        text.newline(r'      <option id="3/4-16" value="3/4-16">3/4-16</option>')
        text.newline(r'      <option id="1-8" value="1-8">1-8</option>')
        text.newline(r'      <option id="1-14" value="1-14">1-14</option>')
        text.newline(r'     </select>')
        text.newline(r'   </div>')
        text.newline(r'  <label class="boltInputLabel" for="UTSs"')
        text.newline(r'    >$UTS_s$ (Strength of Externally Threaded Part):')
        text.newline(r'  </label>')
        text.newline(r'  <input class="boltInput" type="text" id="UTSs" value=' + f'"{UTSs_str}"' + r' name="UTSs"/>')
        text.newline(r'  <label class="unit">psi</label>')
        text.newline(r'')
        text.newline(r'  <label class="boltInputLabel" for="UTSn">$UTS_n$ (Strength of Internally Threaded Part):</label>')
        text.newline(r'  <input class="boltInput" type="text" id="UTSn" value=' + f'"{UTSn_str}"' + r' name="UTSn"/>')
        text.newline(r'  <label class="unit">psi</label>')
        text.newline(r'  <button class = "generalButton" style = "width: 30%" type = "submit">Calculate</button>')
        text.newline(r'</div>')
        text.newline(r'<script>')
        text.newline(r'  document.getElementById("boltDropdown").onchange = function () {')
        text.newline(r'    sessionStorage.setItem("boltSelectItem",document.getElementById("boltDropdown").value);')
        text.newline(r'    this.form.submit();')
        text.newline(r'  };')
        text.newline(r'')
        text.newline(r'  if (sessionStorage.getItem("boltSelectItem")) {')
        text.newline(r'    document.getElementById("boltDropdown").options[sessionStorage.getItem("boltSelectItem")].selected = true;')
        text.newline(r'  }')
        text.newline(r'</script>')

        return text.string
        
    def boltText_output(bolt, UTSs_str,UTSn_str):

        text = htmlstr(default_indent=10);
        
        # Check input and convert to numbers
        bad_input = False
        try:
            UTSs = float(UTSs_str)
        except:
            bad_input = True
            text.newline(r'<p>The ultimate tensile strength of the externally threaded part must be a number</p>')

        try:
            UTSn = float(UTSn_str)
        except:
            bad_input = True
            text.newline(r'<p>The ultimate tensile strength of the internally threaded part must be a number</p>')

        if bad_input:
            return text.string
            
        if UTSs <= 0:
            bad_input = True
            text.newline(r'<p>The ultimate tensile strength of the externally threaded part must be a positive number</p>')

        if UTSn <= 0:
            bad_input = True
            text.newline(r'<p>The ultimate tensile strength of the internally threaded part must be a positive number</p>')
        
        if bad_input:
            return text.string    
        
        # Thread Form Dimensions
        thread_data = ASME_B11_UN_2A2B_dict[bolt]
        boltObj = Assembly(thread_data, UTSs, UTSn)

        text.newline('Thread Form Dimensions', tag='h1')
        text.newline(f'A {bolt} thread has a nominal size of ' + sigfigstr(boltObj.dbsc) + ' in. and ' + str(boltObj.n) + ' threads/in.', tag='p')
        text.newline(r'$d_{bsc} = ' + sigfigstr(boltObj.dbsc) + r'\text{ in.}$',tag='p',cls='eqn')
        text.newline(r'$n = ' + str(boltObj.n) + r'\text{ threads/in.}$',tag='p',cls='eqn')
        
        text.newline(f'Based on the basic profile for UN screw threads shown in ASTM B1.1-2019 Figure 2, basic thread dimensions are:', tag='p')    
        text.newline(r'$p = \dfrac{1}{n} = \dfrac{1}{' + str(boltObj.n) + r'\text{ threads/in.}} = ' + sigfigstr(1/boltObj.n) + r'\text{ in.}$',tag='p',cls='eqn')
        text.newline(r'$H = \dfrac{\sqrt{3}}{2n} = \dfrac{\sqrt{3}}{2(' + str(boltObj.n) + r'\text{ threads/in.})} = ' + sigfigstr(sqrt(3)/2/boltObj.n) + r'\text{ in.}$',tag='p',cls='eqn')
        
        text.newline(r'$D_{1,bsc} = d_{1,bsc} = d_{bsc} - 2(0.625)H = ' + sigfigstr(boltObj.dbsc) + r'\text{ in. }- 2(0.625)\left(' + sigfigstr(boltObj.H) + r'\text{ in.}\right) = ' + sigfigstr(boltObj.D1bsc) + r'$ in.', tag='p',cls='eqn')
        text.newline(r'$D_{2,bsc} = d_{2,bsc} = d_{bsc} - 2(0.375)H = ' + sigfigstr(boltObj.dbsc) + r'\text{ in. }- 2(0.375)\left(' + sigfigstr(boltObj.H) + r'\text{ in.}\right) = ' + sigfigstr(boltObj.D2bsc) + r'$ in.', tag='p',cls='eqn')

        text.newline(f'From ASME B1.1-2019 Table 2A, the minimum dimensions of the external threads are:', tag='p')
        text.newline(r'$d_{min} = ' + sigfigstr(boltObj.dmin) + r'\text{ in.}$',tag='p',cls='eqn')
        text.newline(r'$d_{2,min} = ' + sigfigstr(boltObj.d2min) + r'\text{ in.}$',tag='p',cls='eqn')
        
        text.newline(f'From ASME B1.1-2019 Table 2B, the maximum dimensions of the internal threads are:', tag='p')
        text.newline(r'$D_{1,max} = ' + sigfigstr(boltObj.D1max) + r'\text{ in.}$',tag='p',cls='eqn')
        text.newline(r'$D_{2,max} = ' + sigfigstr(boltObj.D2max) + r'\text{ in.}$',tag='p',cls='eqn')
        
        # Tensile Strength
        text.newline(f'Tensile Strength', tag='h1')
        text.newline(f'The tensile strength of a fastener is equal to the ultimate tensile strength of the material times the tensile stress area.', tag='p')
        text.newline(f'The two formulas for tensile stress area in FED-STD-H28/2B Table II.B.1 are geometrically identical (however, differences may result from rounding). For this example, formula (1a) is used.',tag='p')
        
        line = r'$\begin{aligned}A_{s} &= \pi\left(\dfrac{d_{2,bsc}}{2}-\dfrac{3H}{16}\right)^{2} \\'
        line += r'&= \pi\left(\dfrac{' + sigfigstr(boltObj.d2bsc) + r'\text{ in.}}{2} - \dfrac{3(' + sigfigstr(boltObj.H) + r'\text{ in.})}{16}\right)^{2} \\'
        line += r'&= ' + sigfigstr(boltObj.As_FEDSTD_1a()) + r' \text{ in.}^{2}\end{aligned}$'
        text.newline(line, tag='p',cls='eqn')   

        text.newline(f'Calculate the tensile strength.', tag='p')
        text.newline(r'$F = UTS_s A_s = \left(' + sigfigstr(boltObj.UTSs) + r'\text{ psi}\right)\left(' + sigfigstr(boltObj.As_FEDSTD_1a()) + r'\text{ in.}^{2}\right) = ' + sigfigstr(boltObj.UTSs * boltObj.As_FEDSTD_1a()) + r'\text{ lbs}$', tag='p',cls='eqn')

        # Length of Engagement
        text.newline(f'Length of Engagement', tag='h1')
        text.newline(f'The length of engagement is the distance along the thread axis over which the internal and external mated threads are engaged (i.e., in contact). FED-STD-H28/2B Table II.B.1 provides formulas for the required length of engagement such that tensile failure is more likely to occur than thread stripping failures.', tag='p')
        text.newline(f'The specific formula to use depends on which thread stripping failure controls (shear failure of the external thread, shear failure of the internal thread, or combined shear failure of the external and internal threads) as evaluated using ' + r'$R_{1}/R_{2}$', tag='p')
        text.newline(f'According to formula (8), ' + r'$R_{1}$' + f' is the ratio of ' + r'$AS_{s,max}$' + f' to ' + r'$AS_{n,min}$' + f'. Both ' + r'$AS_{s,max}$' + f' and ' + r'$AS_{n,min}$' + f' depend on LE, which cancels out.')
        text.newline(r'$AS_{s,max}$' + f' may be calculated using formula (6a) or (6b). This example uses formula (6b) because formula (6a) requires values read from a chart.', tag = 'p')
        text.newline(r'$AS_{s,max} = \pi\dfrac{3}{4}D_{1,bsc}LE = \pi\dfrac{3}{4}\left(' + sigfigstr(boltObj.D1bsc) + r'\text{ in.}\right)LE = \left(' + sigfigstr(boltObj.ASs_max_FEDSTD_6b()) + r'\text{ in.}\right)LE$', tag='p',cls='eqn')
        text.newline(r'$AS_{n,min}$' + f' may be calculated using formula (2a) or (2b). This example uses formula (2a) because formula (2b) requires dimensions not already used within this example.', tag='p')

        line = r'$\begin{aligned}AS_{n,min} &= \pi d_{min} n\left(\dfrac{1}{2n} + \dfrac{1}{\sqrt{3}}\left(d_{min} - D_{2,max}\right)\right)LE \\'
        line += r'&= \pi\left(' + str(boltObj.dmin) + r'\text{ in.}\right)\left(' + str(boltObj.n) + r'\text{ threads/in.}\right)\left(\dfrac{1}{2\left(' + str(boltObj.n) + r'\text{ threads/in.}\right)} + \dfrac{1}{\sqrt{3}}\left(' + str(boltObj.dmin) + r'\text{ in.} - ' + str(boltObj.D2max) + r'\text{ in.}\right)\right)LE \\'
        line += r'&= \left(' + sigfigstr(boltObj.ASn_min_FEDSTD_2a()) + r'\text{ in.}\right)LE\end{aligned}$'
        text.newline(line, tag='p',cls='eqn')

        text.newline(f'Calculate ' + r'$R_{1}$', tag='p')
        text.newline(r'$R_{1} = \dfrac{AS_{s,max}}{AS_{n,min}} = \dfrac{\left(' + sigfigstr(boltObj.ASs_max_FEDSTD_6b()) + r'\text{ in.}\right)LE}{\left(' + sigfigstr(boltObj.ASn_min_FEDSTD_2a()) + r'\text{ in.}\right)LE} = ' + sigfigstr(boltObj.ASs_max_FEDSTD_6b()/boltObj.ASn_min_FEDSTD_2a()) + r'$', tag='p',cls='eqn')
        
        text.newline(f'According to formula (9), '+ r'$R_{2}$' + f' is the ratio of ' + r'$UTS_{n}$' + f' to ' + r'$UTS_{s}$' + f'.')
        text.newline(f'Calculate ' + r'$R_{2}$', tag='p')
        text.newline(r'$R_{2} = \dfrac{UTS_{n}}{UTS_{s}} = \dfrac{' + sigfigstr(boltObj.UTSn) + r'\text{ psi}}{' + sigfigstr(boltObj.UTSs) + r'\text{ psi}} = ' + sigfigstr(boltObj.UTSn / boltObj.UTSs) + r'$', tag='p',cls='eqn')
        text.newline(f'Calculate ' + r'$R_{1}/R_{2}$', tag='p')
        text.newline(r'$\dfrac{R_{1}}{R_{2}} = \dfrac{' + sigfigstr(boltObj.ASs_max_FEDSTD_6b()/boltObj.ASn_min_FEDSTD_2a()) + r'}{' + sigfigstr(boltObj.UTSn / boltObj.UTSs) + r'} = ' + sigfigstr((boltObj.ASs_max_FEDSTD_6b()/boltObj.ASn_min_FEDSTD_2a())/(boltObj.UTSn / boltObj.UTSs)) + r'$', tag='p',cls='eqn')

        if (boltObj.ASs_max_FEDSTD_6b() / boltObj.ASn_min_FEDSTD_2a()) / (boltObj.UTSn / boltObj.UTSs) <= 1:
            text.newline(f'Since ' + r'$R_{1}/R_{2}$' + f' is less than or equal to 1, the external threads are weaker than the interal threads and the required length of engagement should be based on the \
                        strength of the external threads. Formula (14) defines the required length of engagement based upon shear of external threads. However, if the strength of the external and internal threads are approximately \
                        equal (i.e., ' + r'$R_{1}/R_{2} \approx 1$' +  f') then a combined shear failure may control. Formula (13) gives the required length of engagement based upon combined shear failure of external and internal \
                        threads. FED-STD-H28/2B does not provide an explicit limit for when formula (13) applies. The required length of engagement from both formulas are calculated in this example.', tag='p')
            text.newline(f'The required length of engagement based upon shear of external threads is defined in formula (14) as two times the tensile stress area divided by the shear area of the external threads per unit length of engagement. ', tag='p')
            text.newline(f'The tensile stress area, ' + r'$A_{s}$' + f', can be computed from either formula (1a) or (1b) and was computed previously.', tag='p')
            text.newline(r'$A_{s}' + f' = ' + sigfigstr(boltObj.As_FEDSTD_1a()) + r'\text{ in.}^{2}$',tag='p',cls='eqn')
            text.newline(f'The shear area, ' + r'$AS_{s}$' + f', can be computed from either formula (4a) or (4b). This example uses formula (4a) because formula (4b) requires dimensions not already used within this text.')
            
            line = r'$\begin{aligned}AS_{s,min} &= \pi D_{1,max} n \left(\dfrac{1}{2n} + \dfrac{1}{\sqrt{3}}\left(d_{2,min} - D_{1,max}\right)\right) LE \\'
            line += r'&= \pi\left(' + sigfigstr(boltObj.D1max) + r'\text{ in.}\right)\left(' + str(boltObj.n) + r'\text{ threads/in.}\right)\left(\dfrac{1}{2\left(' + str(boltObj.n) + r'\text{ threads/in.}\right)} + \dfrac{1}{\sqrt{3}}\left(' + sigfigstr(boltObj.d2min) + r'\text{ in.} - ' + sigfigstr(boltObj.D1max) + r'\text{ in.}\right)\right) LE \\'
            line += r'&= \left(' + sigfigstr(boltObj.ASs_min_FEDSTD_4a()) + r'\text{ in.}\right) LE\end{aligned}$'
            text.newline(line, tag='p',cls='eqn')        
                    
            text.newline(f'The required length of engagement is computed using formula (14) as follows:', tag='p')
            text.newline(r'$LE_{r,14} = \dfrac{2A_{s}}{AS_{s,min}/LE} = \dfrac{2\left(' + sigfigstr(boltObj.As_FEDSTD_1a()) + r'\text{ in.}^{2}\right)}{' + sigfigstr(boltObj.ASs_min_FEDSTD_4a()) + r'\text{ in.}} = ' + sigfigstr(boltObj.LEr_FEDSTD_14()) + r'\text{ in.}$', tag='p',cls='eqn')
            text.newline(f'The required length of engagement based upon combined shear failure of external and internal threads, which is defined as four times the tensile stress area divided by ' + r'$\pi$' + f' times the basic pitch diameter, is computed using formula (13) as follows: ', tag='p')
            text.newline(r'$LE_{r,13} = \dfrac{4A_{s}}{\pi d_{2,bsc}} = \dfrac{4\left(' + sigfigstr(boltObj.As_FEDSTD_1a()) + r'\text{ in.}^{2}\right)}{\pi\left(' + sigfigstr(boltObj.d2bsc) + r'\text{ in.}\right)} = ' + sigfigstr(boltObj.LEr_FEDSTD_13()) + r'\text{ in.}$', tag='p',cls='eqn')
            text.newline(f'Therefore, the required length of engagement is either ' + sigfigstr(boltObj.LEr_FEDSTD_14()) + ' in. if the external threads are stronger than the internal threads by a sufficient amount that combined failure will not occur or ' + sigfigstr(boltObj.LEr_FEDSTD_13()) +' in. if combined failure may occur.', tag='p')
        else:
            text.newline(f'Since ' + r'$R_{1}/R_{2}$' + f' is greater than 1, the internal threads are weaker than the external threads and the required length of engagement should be based on the strength of the \
                        internal threads. Formula (16) defines the required length of engagement based upon shear of internal threads. However, if the strength of the external and internal threads are approximately equal \
                        (i.e., ' + r'$R_{1}/R_{2} \approx 1$' +  f') then a combined shear failure may control. Formula (13) gives the required length of engagement based upon combined shear failure of external and internal \
                        threads. FED-STD-H28/2B does not provide an explicit limit for when formula (13) applies. The required length of engagement from both formulas are calculated in this example.', tag='p')
            text.newline(f'The required length of engagement based upon shear of internal threads is defined in formula (16) as the length of engagement based upon developing full tensile strength of external threads \
                        with threads a basic size, calculated using formula (15), multiplied by ' + r'$R_{1}/R_{2}$' + f'.', tag='p')
            text.newline(f'The length of engagement based upon developing full tensile strength of external threads with threads at basic size is defined in formula (15) as two times the tensile stress area divided by \
                        the shear area per unit length of engagement from formula (6b).', tag='p')
            text.newline(f'The required length of engagement based upon shear of internal threads is computed using formula (16) as follows:', tag='p')
            text.newline(r'$LE_{r,16} = \dfrac{\dfrac{2A_{s}}{AS_{n,min}/LE}}{R_{2}} = \dfrac{\dfrac{2\left(' + sigfigstr(boltObj.As_FEDSTD_1a()) + r'\text{ in.}^{2}\right)}{' + sigfigstr(boltObj.ASn_min_FEDSTD_2a()) + r'\text{ in.}}}{' + sigfigstr(boltObj.UTSn / boltObj.UTSs) + r'} = ' + sigfigstr(boltObj.LEr_FEDSTD_16()) + r'\text{ in.}$', tag='p',cls='eqn')
            text.newline(f'The required length of engagement based upon combined shear failure of external and internal threads, which is defined as four times the tensile stress area divided by ' + r'$\pi$' + f' times the basic pitch diameter, is computed using formula (13) as follows: ', tag='p')
            text.newline(r'$LE_{r,13} = \dfrac{4A_{s}}{\pi d_{2,bsc}} = \dfrac{4\left(' + sigfigstr(boltObj.As_FEDSTD_1a()) + r'\text{ in.}^{2}\right)}{\pi\left(' + sigfigstr(boltObj.d2bsc) + r'\text{ in.}\right)} = ' + sigfigstr(boltObj.LEr_FEDSTD_13()) + r'\text{ in.}$', tag='p',cls='eqn')
            text.newline(f'Therefore, the required length of engagement is either ' + sigfigstr(boltObj.LEr_FEDSTD_16()) + ' in. if the internal threads are stronger than the external threads by a sufficient amount that combined failure will not occur or ' + sigfigstr(boltObj.LEr_FEDSTD_13()) + ' \
                        in. if combined failure may occur.')       
        return text.string

    def boltText_footer():

        text = htmlstr(default_indent=10);
        text.newline('Developed by Jonathan Smith and Mark Denavit at the University of Tennessee, Knoxville.', tag='p')
        text.newline('This work was supported by the Naval Engineering Education Consortium [Award Number N00174-22-1-0017].', tag='p')
        return text.string
    
    return boltText_header(), boltText_input(UTSs_str,UTSn_str), boltText_output(bolt, UTSs_str,UTSn_str), boltText_footer()
