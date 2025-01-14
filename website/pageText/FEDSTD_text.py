from math import floor, log10, sqrt, pi
from dictionaries.ASME_B11 import ASME_B11_UN_2A2B_dict
from dictionaries.boltEquations import *
from .string_functions import htmlstr, sigfigstr


def boltText_header():
    text = htmlstr(default_indent=10);
    text.newline('Bolt Tensile Strength Calculation According to FED-STD-H28/2B', tag='h1')
    return text.string


def boltText_input(UTSs_str,UTSn_str,LE_str):
    text = htmlstr(default_indent=10);
    text.newline(r'<div class="col-3">')
    text.newline(r'  <div style = "text-align: center";>')
    text.newline(r'    <label class="bolt_select_label" for="boltDropdown" style="vertical-align: middle" >Selected Bolt:</label>')
    text.newline(r'    <select class="boltDropdown" id="boltDropdown" name="boltDropdown">')
    text.newline(r'      <option id="1/4-20" value="1/4-20">1/4-20</option>')
    text.newline(r'      <option id="1/4-28" value="1/4-28">1/4-28</option>')
    text.newline(r'      <option id="1/2-13" value="1/2-13">1/2-13</option>')
    text.newline(r'      <option id="1/2-20" value="1/2-20">1/2-20</option>')
    text.newline(r'      <option id="3/4-10" value="3/4-10">3/4-10</option>')
    text.newline(r'      <option id="3/4-16" value="3/4-16">3/4-16</option>')
    text.newline(r'      <option id="1-8" value="1-8">1-8</option>')
    text.newline(r'      <option id="1-14" value="1-14">1-14</option>')
    text.newline(r'    </select>')
    text.newline(r'  </div>')
    text.newline(r'  <button class = "button1" style = "display: flex; flex-wrap: wrap;" type = "submit">Calculate</button>')
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
    text.newline(r'<div class="col-3">')
    text.newline(r'  <label class="boltInputLabel" for="UTSs"')
    text.newline(r'    >UTSs (Strength of Externally Threaded Part) :')
    text.newline(r'  </label>')
    text.newline(r'  <input class="boltInput" type="text" id="UTSs" value=' + f'"{UTSs_str}"' + r' name="UTSs"/>')
    text.newline(r'  <label class="unit">psi</label>')
    text.newline(r'')
    text.newline(r'  <label class="boltInputLabel" for="UTSn">UTSn (Strength of Internally Threaded Part) :</label>')
    text.newline(r'  <input class="boltInput" type="text" id="UTSn" value=' + f'"{UTSn_str}"' + r' name="UTSn"/>')
    text.newline(r'  <label class="unit">psi</label>')
    text.newline(r'')
    text.newline(r'  <label class="boltInputLabel" for="LE">LE (Length of Engagement) :</label>')
    text.newline(r'  <input class="boltInput" type="text" id="LE" value='+ f'"{LE_str}"' + r'name="LE" />')
    text.newline(r'  <label class="unit">in.</label>')
    text.newline(r'</div>')
    return text.string
    
def boltText_output(bolt, UTSs_str,UTSn_str,LE_str):
    text = htmlstr(default_indent=10);
    
    text.newline('<h1>Input Echo</h1>')
    text.newline('<p>' + f'Bolt: {bolt}' + r'</p>')
    text.newline('<p>' + f'UTSs: {UTSs_str} psi' + r'</p>')
    text.newline('<p>' + f'UTSn: {UTSn_str} psi' + r'</p>')
    text.newline('<p>' + f'LE: {LE_str} in.' + r'</p>')    
    
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

    try:
        LE = float(LE_str)
    except:
        bad_input = True
        text.newline(r'<p>The length of engagement must be a number</p>')        
    
    if bad_input:
        return text.string
        
    if UTSs <= 0:
        bad_input = True
        text.newline(r'<p>The ultimate tensile strength of the externally threaded part must be a positive number</p>')

    if UTSn <= 0:
        bad_input = True
        text.newline(r'<p>The ultimate tensile strength of the internally threaded part must be a positive number</p>')
        
    if LE <= 0:
        bad_input = True
        text.newline(r'<p>The length of engagement must be a positive number</p>')
    
    if bad_input:
        return text.string    
    
    # Thread Form Dimensions
    thread_data = ASME_B11_UN_2A2B_dict[bolt]

    text.newline('Thread Form Dimensions', tag='h1')
    text.newline(f'A {bolt} thread has a nominal size of ' + sigfigstr(thread_data['dbsc']) + ' in. and ' + str(thread_data['n']) + ' theads/in.', tag='p')
    text.newline(r'$d = ' + sigfigstr(thread_data['dbsc']) + r'\text{ in.}$',tag='p')
    text.newline(r'$n = ' + str(thread_data['n']) + r'\text{ threads/in.}$',tag='p')
    
    text.newline(f'Based on the basic profile for UN screw threads shown in ASTM B1.1-2019 Figure 2, basic thread dimensions are:', tag='p')    
    text.newline(r'$p = \dfrac{1}{n} = \dfrac{1}{' + str(thread_data['n']) + r'\text{ threads/in.}} = ' + sigfigstr(1/thread_data['n']) + r'\text{ in.}$',tag='p')
    text.newline(r'$H = \dfrac{\sqrt{3}}{2n} = \dfrac{\sqrt{3}}{2(' + str(thread_data['n']) + r'\text{ threads/in.})} = ' + sigfigstr(sqrt(3)/2/thread_data['n']) + r'\text{ in.}$',tag='p')
    
    
    #    <p>$D_{{1,bsc}} = d_{{1,bsc}} = {D1bsc}$ in.</p>
    #    <p>$D_{{2,bsc}} = d_{{2,bsc}} = {d2bscVar}$ in.</p>

    text.newline(f'From ASME B1.1-2019 Table 2A, the minimum dimensions of the external threads are:', tag='p')
    text.newline(r'$d_{min} = ' + sigfigstr(thread_data['dmin']) + r'\text{ in.}$',tag='p')
    text.newline(r'$d_{2,min} = ' + sigfigstr(thread_data['d2min']) + r'\text{ in.}$',tag='p')
    
    text.newline(f'From ASME B1.1-2019 Table 2B, the maximum dimensions of the internal threads are:', tag='p')
    text.newline(r'$D_{1,max} = ' + sigfigstr(thread_data['D1max']) + r'\text{ in.}$',tag='p')
    text.newline(r'$D_{2,max} = ' + sigfigstr(thread_data['D2max']) + r'\text{ in.}$',tag='p')
    
    
    text.newline(f'Tensile Strength', tag='h1')
    text.newline(f'The ultimate tensile strength of a threaded fastener is directly proportional to the cross sectional area through the threaded region.', tag='p')
    text.newline(f'FED-STD-H28/2B provides two equations to calculate the tensile stress area, both of which are geometrically identical: ',tag='p')
    text.newline(r'$A_{s,1a} = \pi\left(\frac{d_{2,bsc}}{2} - \frac{3H}{16}\right)^{2} = \pi\left(\left(\frac{1}{2}\right)\left(d_{2,bsc} - \frac{3H}{8}\right)\right)^{2} = \frac{\pi}{4}\left(d_{2,bsc} - \frac{3H}{8}\right)^{2}$', tag='p')
    text.newline(r'$A_{s,1b} = \frac{\pi}{4}\left(d_{bsc} - \frac{0.9743}{n}\right)^{2} = \frac{\\pi}{4}\left(d_{bsc} - \frac{9P\sqrt{3}}{16}\right)^{2} = \frac{\pi}{4}\left(d_{bsc} - \frac{9\sqrt{3}\left(\frac{2H}{\sqrt{3}}\right)}{16}\right)^{2} = \frac{\pi}{4}\left(d_{bsc} - \frac{9H}{8}\right)^{2}$', tag='p')
    text.newline(f'Figure 2 in ASME B1.1-2019 provides thread geometry to further prove the equality:', tag='p')
    text.newline(r'$d_{2,bsc} = d_{bsc} - 2\left(\frac{3H}{8}\right) = d_{bsc} - \frac{6H}{8}', tag='p')    
    text.newline(r'$A_{s, 1a} = \frac{\pi}{4}\left(d_{bsc} - \frac{6H}{8} - \frac{3H}{8}\right)^{2} = \frac{\pi}{4}\left(d_{bsc} - \frac{9H}{8}\right)^{2} = A_{s, 1b}$', tag='p')  
    text.newline(r'For this example, equation $A_{s, 1a}$ will be used', tag='p')
    text.newline(r'$A_{s, 1a} = \pi\left(\frac{d_{2,bsc}}{2}-\frac{3H}{16}\right)^{2}$', tag='p')    #    <p>$A_{{s, 1a}} = \\pi\\left(\\frac{{d_{{2,bsc}}}}{{2}}-\\frac{{3H}}{{16}}\\right)^{{2}}$</p>
    text.newline(r'$$', tag='p')    #    <p>$= \\pi\\left(\\frac{{{d2bscVar}}}{{2}}-\\frac{{3({HVar})}}{{16}}\\right)^{{2}}$</p>
    text.newline(r'$$', tag='p')    #    <p>$= {As1a} \\text{{ in.}}^{{2}}$</p>
    text.newline(f'The tensile strength of a threaded fastener is equal to:', tag='p')
    text.newline(r'$$', tag='p')    #    <p>$P = \\frac{{F}}{{A}} \\therefore F = PA$</p>
    text.newline(r'$$', tag='p')    #    <p>$F = {{UTSs}}\\left(A_{{s, 1a}}\\right) = {UTSs}\\left({round(As_FEDSTD_1a(float(d2bscVar), H(float(n))), 3)}\\right) = {round(UTSs * As_FEDSTD_1a(float(d2bscVar), H(float(n))))} \\text{{ lbs}}$</p>
    text.newline(f'Length of Engagement', tag='h1')
    text.newline(f'The length of engagement is the measured length of interaction between a fastener and its mating material', tag='p')
    text.newline(f'The method of failure for a fastener is dependent on the length of engagement', tag='p')
    text.newline(f'FED-STD-H28/2B provides equations to calculate the length of engagement to ensure a specific mode of failure', tag='p')
    text.newline(r'$', tag='p')    #    <p>$R_{{1}} = \\frac{{AS_{{s,max}}}}{{AS_{{n,min}}}} 
    text.newline(r'', tag='p')    #    = \\frac{{\\pi\\frac{{3}}{{4}}D_{{1,bsc}}LE}}{{\\pi d_{{min}}\\left(\\frac{{1}}{{2n}} + \\frac{{1}}{{\\sqrt{{3}}}}\\left(d_{{min}} - D_{{2,max}}\\right)\\right)LE}} 
    text.newline(r'', tag='p')    #    = \\frac{{\\pi\\frac{{3}}{{4}}{D1bsc}({LEr})}}{{\\pi ({dmin})\\left(\\frac{{1}}{{2({n})}} + \\frac{{1}}{{\\sqrt{{3}}}}\\left({dmin} - {D2max}\\right)\\right)({LEr})}}
    text.newline(r'', tag='p')    #    = {sigfigstr(float(ASn2a)/float(ASs6b))}$</p>
    text.newline(r'', tag='p')    #    <p>$R_{{2}} = \\frac{{UTSn}}{{UTSs}} = {sigfigstr(float(UTSn)/float(UTSs))}$</p>
    text.newline(r'', tag='p')    #    <p>$\\frac{{R_{1}}}{{R_{2}}} = {sigfigstr((float(ASn2a)/float(ASs6b))/(float(UTSn)/float(UTSs)))}$</p>'''
    text.newline(r'', tag='p')    #    if (float(ASn2a)/float(ASs6b))/(float(UTSn)/float(UTSs)) < 1:
    text.newline(r'', tag='p')    #        <p>Because $\\frac{{R_{1}}}{{R_{2}}}$ < 1, external thread failure controls and FED-STD-H28/2B Formula (15) is used</p>
    text.newline(r'', tag='p')    #        <p>$A_{{s}} = \\pi\\left(\\frac{{d_{{2,bsc}}}}{{2}}-\\frac{{3H}}{{16}}\\right)^{{2}} = '''
    text.newline(r'', tag='p')    #        '\pi\left(\frac{' + str(d2bscVar) + r'}{2}-\frac{3(' + sigfigstr(HVar) + r')}{16}\right)^{2} =' + sigfigstr(As1a) + r'\text{ in.}^{2}$'
    
    #        outputText += f'''
    #        <p>$AS_{{s,min}} = \\pi d_{{min}}\\left(\\frac{{1}}{{2n}} + \\frac{{1}}{{\\sqrt{{3}}}}\\left(d_{{min}} - D_{{2,max}}\\right)\\right)LE = \\pi ({dmin})\\left(\\frac{{1}}{{2({n})}} + \\frac{{1}}{{\\sqrt{{3}}}}\\left({dmin} - {D2max}\\right)\\right)({LEr}) = {sigfigstr(float(ASn2a))} \\text{{ in.}}^{{2}}$</p>
    #        <p>$LE = \\frac{{2A_{{s}}}}{{AS_{{s,min}}}} = \\frac{{2({As1a})}}{{{ASn2a}}} = {sigfigstr(2 * float(As1a) / float(ASn2a))} \\text{{ in.}}$</p>
    #        <hr />
    #        '''
    #    else:
    #        outputText += f'''            
    #        <p>Because $\\frac{{R_{1}}}{{R_{2}}}$ > 1, either internal thread failure or combined failure controls and FED-STD-H28/2B Formula (13) or (16) is used</p>
    #        <p>$A_{{s}} = \\pi\\left(\\frac{{d_{{2,bsc}}}}{{2}}-\\frac{{3H}}{{16}}\\right)^{{2}} = '''
    #
    #        outputText += r'\pi\left(\frac{' + str(d2bscVar) + r'}{2}-\frac{3(' + sigfigstr(HVar) + r')}{16}\right)^{2} =' + sigfigstr(As1a) + r'\text{ in.}^{2}$</p>'
    #
    #        outputText += f'''<p>$AS_{{s,min}} = \\pi d_{{min}}\\left(\\frac{{1}}{{2n}} + \\frac{{1}}{{\\sqrt{{3}}}}\\left(d_{{min}} - D_{{2,max}}\\right)\\right)LE = \\pi ({dmin})\\left(\\frac{{1}}{{2({n})}} + \\frac{{1}}{{\\sqrt{{3}}}}\\left({dmin} - {D2max}\\right)\\right)({LEr}) = {sigfigstr(float(ASn2a))} \\text{{ in.}}^{{2}}$</p>
    #'''
    #
    #        outputText += f'''<p>$LE_{{r,13}} = \\frac{{4A_{{s}}}}{{\\pi{{d_{{2,bsc}}}}}} = \\frac{{4{{({As1a})}}}}{{\\pi{{({d2bscVar})}}}} = {sigfigstr(4 * float(As1a) / (pi * float(d2bscVar)))} \\text{{ in.}}$</p>
    #        <p>$LE_{{r,16}} = \\frac{{\\frac{{2A_{{s}}}}{{AS_{{n}}}}}}{{R_{{2}}}} = \\frac{{\\frac{{2({As1a}))}}{{{ASn2a}}}}}{{{sigfigstr(float(UTSn)/float(UTSs))}}} = {sigfigstr((2*float(As1a)/float(ASn2a))/(float(UTSn)/float(UTSs)))} \\text{{ in.}}$</p>
    #        <p>The controlling length of engagement is the maximum of $LE_{{r,13}}$ and $LE_{{r,16}}$</p>
    #        '''
    #        
    #        if 4 * float(As1a) / (pi * float(d2bscVar)) > (2*float(As1a)/float(ASn2a))/(float(UTSn)/float(UTSs)):
    #            outputText += f'''<p>Thus, LE = $LE_{{r,13}} = {sigfigstr(4 * float(As1a) / (pi * float(d2bscVar)))}$</p>
    #            '''
    #        else:
    #            outputText += f'''<p>Thus, LE = $LE_{{r,16}} = {sigfigstr((2*float(As1a)/float(ASn2a))/(float(UTSn)/float(UTSs)))}</p>
    #            '''
    #        
    #    return outputText
    return text.string

def boltText_footer():
    text = htmlstr(default_indent=10);
    text.newline('Developed by Jonathan Smith and Mark Denavit at the University of Tennessee, Knoxville.', tag='p')
    text.newline('This work was supported by the Naval Engineering Education Consortium [Award Number N00174-22-1-0017].', tag='p')
    return text.string
