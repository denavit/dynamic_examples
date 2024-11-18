from math import floor, log10, sqrt, pi
from dictionaries.ASME_B11 import ASME_B11_UN_2A2B_dict
from dictionaries.boltEquations import *

def sigfigstr(n,sigfigs=4):
    n = float(n)
    sigfigsleft = floor(log10(n)) + 1
    if sigfigsleft > sigfigs:
        n = int(round(n,sigfigs-sigfigsleft))
        return f'{n:0,}'
    else:
        format_str = '{:.' + str(sigfigs-sigfigsleft) + 'f}'
        return format_str.format(n)

def boltText(bolt, n, dmin, dbsc, d2min, D1bsc, D1max, D2max, UTSs, UTSn, LE):
    def header():
        headerText = f'''
        <form action="/bolt" method="POST">
            <div class="section">
                <div class="header col-4">
                <h1>Bolt Calculator</h1>
                </div>
            </div>'''
        return headerText
    
    def input(UTSs, UTSn, LE):
        inputText = f'''
        <div class="section">
            <div class="col-3">
                <div style = "text-align: center;>
                    <label
                        class="bolt_select_label"
                        for="boltDropdown"
                        style="vertical-align: middle"
                        >Selected Bolt:
                    </label>
                    <select class="boltDropdown" id="boltDropdown" name="boltDropdown">
                        <option id="1/4-20" value="1/4-20">1/4-20</option>
                        <option id="1/4-28" value="1/4-28">1/4-28</option>
                        <option id="1/2-13" value="1/2-13" selected>1/2-13</option>
                        <option id="1/2-20" value="1/2-20">1/2-20</option>
                        <option id="3/4-10" value="3/4-10">3/4-10</option>
                        <option id="3/4-16" value="3/4-16">3/4-16</option>
                        <option id="1-8" value="1-8">1-8</option>
                        <option id="1-14" value="1-14">1-14</option>
                    </select>
                </div>
                <button class = "button1" style = "display: flex; flex-wrap: wrap;" type = "submit">Calculate</button>
            </div>
            <script>
            document.getElementById("boltDropdown").onchange = function () {{
                sessionStorage.setItem(
                "boltSelectItem",
                document.getElementById("boltDropdown").value
                );
                this.form.submit();
            }};

            if (sessionStorage.getItem("boltSelectItem")) {{
                document.getElementById("boltDropdown").options[
                sessionStorage.getItem("boltSelectItem")
                ].selected = true;
            }}
            </script>
            <div class="col-3">
                <label class="boltInputLabel" for="UTSs"
                    >UTSs (Strength of Externally Threaded Part) :
                </label>
                <input
                    class="boltInput"
                    type="text"
                    id="UTSs"
                    value="{'%g'%(UTSs)}"
                    name="UTSs"
                />
                <label class="unit">psi</label>

                <label class="boltInputLabel" for="UTSn"
                    >UTSn (Strength of Internally Threaded Part) :
                </label>
                <input
                    class="boltInput"
                    type="text"
                    id="UTSn"
                    value="{'%g'%(UTSn)}"
                    name="UTSn"
                />
                <label class="unit">psi</label>

                <label class="boltInputLabel" for="LE"
                    >LE (Length of Engagement) :
                </label>
                <input
                    class="boltInput"
                    type="text"
                    id="LE"
                    value="{'%g'%(LE)}"
                    name="LE"
                />
                <label class="unit">in.</label>
            </div>
        </div>
        <hr />'''
    
        return inputText
    
    def output(bolt, n, pVar, HVar, dmin, dbsc, d2min, D1bsc, D1max, d2bscVar, D2max, As1a, ASn2a, ASs6b, LEr = 1):
        # Based off of Alexander 1977 Text, ASME B1.1-2019, and Wide Flange Page Text
        outputText = f'''
        <h1>Thread Form Dimensions</h1>
        <h4>From ASME B1.1-2019, the dimensions of a {bolt} fastener are: </h4>
        <p>$n = {n}$ threads/in.</p>
        '''
        
        outputText += r'<p>$P = \frac{1}{n} = \frac{1}{' + str(n) + r'} = ' + str(pVar) + r'\text{ in./thread}$</p>'
               
        outputText += f'''
        <p>$H = \\frac{{\\sqrt{3}}}{{2n}} = \\frac{{\\sqrt{3}}}{{2({n})}} = {HVar} $ in.</p>
        <p>$d_{{min}} = {dmin}$ in.</p>
        <p>$d_{{bsc}} = {dbsc}$ in.</p>
        <p>$d_{{2,min}} = {d2min}$ in.</p>
        <p>$D_{{1,bsc}} = d_{{1,bsc}} = {D1bsc}$ in.</p>
        <p>$D_{{1,max}} = {D1max}$ in.</p>
        <p>$D_{{2,bsc}} = d_{{2,bsc}} = {d2bscVar}$ in.</p>
        <p>$D_{{2,max}} = {D2max}$ in.</p>
        '''


        # How to say "they can be simplified to be exactly the same" in a short, concise manner? Currently I have "geometrically identical"
        # Also I'm currently doing += to the text to separate it into sections. Is there another way to do that that can keep it as once block while still having visual markers of sections?
        outputText += f'''
        <h1>Tensile Strength</h1>
        <h4>The ultimate tensile strength of a threaded fastener is directly proportional to the cross sectional area through the threaded region.</h4>
        <h4>FED-STD-H28/2B provides two equations to calculate the tensile stress area, both of which are geometrically identical: </h4>
        <p>$A_{{s, 1a}} = \\pi\\left(\\frac{{d_{{2,bsc}}}}{{2}}-\\frac{{3H}}{{16}}\\right)^{{2}} = \\pi\\left(\\left(\\frac{{1}}{{2}}\\right)\\left({{d_{{2,bsc}}}} - \\frac{{3H}}{{8}}\\right)\\right)^{{2}} = \\frac{{\\pi}}{{4}}\\left({{d_{{2,bsc}}}} - \\frac{{3H}}{{8}}\\right)^{{2}}$</p>
        <p>$A_{{s, 1b}} = \\frac{{\\pi}}{{4}}\\left(d_{{bsc}} - \\frac{{0.9743}}{{n}}\\right)^{{2}} = \\frac{{\\pi}}{{4}}\\left(d_{{bsc}} - \\frac{{9P\\sqrt{{3}}}}{{16}}\\right)^{{2}} = \\frac{{\\pi}}{{4}}\\left(d_{{bsc}} - \\frac{{9\\sqrt{{3}}\\left(\\frac{{2H}}{{\\sqrt{{3}}}}\\right)}}{{16}}\\right)^{{2}} = \\frac{{\\pi}}{{4}}\\left(d_{{bsc}} - \\frac{{9H}}{{8}}\\right)^{{2}}$</p>
        <p>Figure 2 in ASME B1.1-2019 provides thread geometry to further prove the equality:</p>
        <p>$d_{{2,bsc}} = d_{{bsc}} - 2\\left(\\frac{{3H}}{{8}}\\right) = d_{{bsc}} - \\frac{{6H}}{{8}}$</p>
        <p>$A_{{s, 1a}} = \\frac{{\\pi}}{{4}}\\left(d_{{bsc}} - \\frac{{6H}}{{8}} - \\frac{{3H}}{{8}}\\right)^{{2}} = \\frac{{\\pi}}{{4}}\\left(d_{{bsc}} - \\frac{{9H}}{{8}}\\right)^{{2}} = A_{{s, 1b}}$</p>
        <p>For this example, equation $A_{{s, 1a}}$ will be used</p>
        <p>$A_{{s, 1a}} = \\pi\\left(\\frac{{d_{{2,bsc}}}}{{2}}-\\frac{{3H}}{{16}}\\right)^{{2}}$</p>
        <p>$= \\pi\\left(\\frac{{{d2bscVar}}}{{2}}-\\frac{{3({HVar})}}{{16}}\\right)^{{2}}$</p>
        <p>$= {As1a} \\text{{ in.}}^{{2}}$</p>
        '''

        outputText += f'''
        <p>The tensile strength of a threaded fastener is equal to:</p>
        <p>$P = \\frac{{F}}{{A}} \\therefore F = PA$</p>
        <p>$F = {{UTSs}}\\left(A_{{s, 1a}}\\right) = {UTSs}\\left({round(As_FEDSTD_1a(float(d2bscVar), H(float(n))), 3)}\\right) = {round(UTSs * As_FEDSTD_1a(float(d2bscVar), H(float(n))))} \\text{{ lbs}}$</p>
        <hr />
        '''

        outputText += f'''
        <h1>Length of Engagement</h1>
        <p>The length of engagement is the measured length of interaction between a fastener and its mating material</p>
        <p>The method of failure for a fastener is dependent on the length of engagement</p>
        <p>FED-STD-H28/2B provides equations to calculate the length of engagement to ensure a specific mode of failure</p>
        <p>$R_{{1}} = \\frac{{AS_{{s,max}}}}{{AS_{{n,min}}}} 
        = \\frac{{\\pi\\frac{{3}}{{4}}D_{{1,bsc}}LE}}{{\\pi d_{{min}}\\left(\\frac{{1}}{{2n}} + \\frac{{1}}{{\\sqrt{{3}}}}\\left(d_{{min}} - D_{{2,max}}\\right)\\right)LE}} 
        = \\frac{{\\pi\\frac{{3}}{{4}}{D1bsc}({LEr})}}{{\\pi ({dmin})\\left(\\frac{{1}}{{2({n})}} + \\frac{{1}}{{\\sqrt{{3}}}}\\left({dmin} - {D2max}\\right)\\right)({LEr})}}
        = {sigfigstr(float(ASn2a)/float(ASs6b))}$</p>
        <p>$R_{{2}} = \\frac{{UTSn}}{{UTSs}} = {sigfigstr(float(UTSn)/float(UTSs))}$</p>
        <p>$\\frac{{R_{1}}}{{R_{2}}} = {sigfigstr((float(ASn2a)/float(ASs6b))/(float(UTSn)/float(UTSs)))}$</p>'''
        
        if (float(ASn2a)/float(ASs6b))/(float(UTSn)/float(UTSs)) < 1:
            outputText += f'''
            <p>Because $\\frac{{R_{1}}}{{R_{2}}}$ < 1, external thread failure controls and FED-STD-H28/2B Formula (15) is used</p>
            <p>$A_{{s}} = \\pi\\left(\\frac{{d_{{2,bsc}}}}{{2}}-\\frac{{3H}}{{16}}\\right)^{{2}} = '''
            
            outputText += r'\pi\left(\frac{' + str(d2bscVar) + r'}{2}-\frac{3(' + sigfigstr(HVar) + r')}{16}\right)^{2} =' + sigfigstr(As1a) + r'\text{ in.}^{2}$</p>'

            outputText += f'''
            <p>$AS_{{s,min}} = \\pi d_{{min}}\\left(\\frac{{1}}{{2n}} + \\frac{{1}}{{\\sqrt{{3}}}}\\left(d_{{min}} - D_{{2,max}}\\right)\\right)LE = \\pi ({dmin})\\left(\\frac{{1}}{{2({n})}} + \\frac{{1}}{{\\sqrt{{3}}}}\\left({dmin} - {D2max}\\right)\\right)({LEr}) = {sigfigstr(float(ASn2a))} \\text{{ in.}}^{{2}}$</p>
            <p>$LE = \\frac{{2A_{{s}}}}{{AS_{{s,min}}}} = \\frac{{2({As1a})}}{{{ASn2a}}} = {sigfigstr(2 * float(As1a) / float(ASn2a))} \\text{{ in.}}$</p>
            <hr />
            '''
        else:
            outputText += f'''            
            <p>Because $\\frac{{R_{1}}}{{R_{2}}}$ > 1, either internal thread failure or combined failure controls and FED-STD-H28/2B Formula (13) or (16) is used</p>
            <p>$A_{{s}} = \\pi\\left(\\frac{{d_{{2,bsc}}}}{{2}}-\\frac{{3H}}{{16}}\\right)^{{2}} = '''

            outputText += r'\pi\left(\frac{' + str(d2bscVar) + r'}{2}-\frac{3(' + sigfigstr(HVar) + r')}{16}\right)^{2} =' + sigfigstr(As1a) + r'\text{ in.}^{2}$</p>'

            outputText += f'''<p>$AS_{{s,min}} = \\pi d_{{min}}\\left(\\frac{{1}}{{2n}} + \\frac{{1}}{{\\sqrt{{3}}}}\\left(d_{{min}} - D_{{2,max}}\\right)\\right)LE = \\pi ({dmin})\\left(\\frac{{1}}{{2({n})}} + \\frac{{1}}{{\\sqrt{{3}}}}\\left({dmin} - {D2max}\\right)\\right)({LEr}) = {sigfigstr(float(ASn2a))} \\text{{ in.}}^{{2}}$</p>
'''

            outputText += f'''<p>$LE_{{r,13}} = \\frac{{4A_{{s}}}}{{\\pi{{d_{{2,bsc}}}}}} = \\frac{{4{{({As1a})}}}}{{\\pi{{({d2bscVar})}}}} = {sigfigstr(4 * float(As1a) / (pi * float(d2bscVar)))} \\text{{ in.}}$</p>
            <p>$LE_{{r,16}} = \\frac{{\\frac{{2A_{{s}}}}{{AS_{{n}}}}}}{{R_{{2}}}} = \\frac{{\\frac{{2({As1a}))}}{{{ASn2a}}}}}{{{sigfigstr(float(UTSn)/float(UTSs))}}} = {sigfigstr((2*float(As1a)/float(ASn2a))/(float(UTSn)/float(UTSs)))} \\text{{ in.}}$</p>
            <p>The controlling length of engagement is the maximum of $LE_{{r,13}}$ and $LE_{{r,16}}$</p>
            '''
            
            if 4 * float(As1a) / (pi * float(d2bscVar)) > (2*float(As1a)/float(ASn2a))/(float(UTSn)/float(UTSs)):
                outputText += f'''<p>Thus, LE = $LE_{{r,13}} = {sigfigstr(4 * float(As1a) / (pi * float(d2bscVar)))}$</p>
                '''
            else:
                outputText += f'''<p>Thus, LE = $LE_{{r,16}} = {sigfigstr((2*float(As1a)/float(ASn2a))/(float(UTSn)/float(UTSs)))}</p>
                '''
            
        return outputText

    def footer():
        footerText = f'''
        <h4>Developed by Dr. Mark Denavit and Jonathan Smith of the University of Tennessee, Knoxville</h4>
        <p>Supported by _______</p>'''

        return footerText
    

    # Returns page text
    if bolt == None:
        return header(), input(UTSs, UTSn, LE), '', footer()
    elif UTSs <= 0:
        return header(), input(UTSs, UTSn, LE), 'UTSs must be greater than zero <hr />', footer()
    elif UTSn <= 0:
        return header(), input(UTSs, UTSn, LE), 'UTSn must be greater than zero <hr />', footer()
    elif LE <= 0:
        return header(), input(UTSs, UTSn, LE), 'LE must be greater than zero <hr />', footer()
    else:
        pVar = sigfigstr(p(n))
        HVar = sigfigstr(H(n))
        d2bscVar = sigfigstr(d2bsc(dbsc, H(n)))
        As1a = sigfigstr(As_FEDSTD_1a(d2bsc(dbsc, H(n)), H(n)))
        ASn2a = sigfigstr(ASn_min_FEDSTD_2a(n, dmin, D2max))
        ASs6b = sigfigstr(ASs_max_FEDSTD_6b(D1bsc))
        LEr = sigfigstr(LEr_FEDSTD(n, D1bsc, dmin, D2max, UTSn, UTSs, float(d2bscVar), float(HVar), dbsc, D1max, d2min))

        return header(), input(UTSs, UTSn, LE), output(bolt, n, pVar, HVar, dmin, dbsc, d2min, D1bsc, D1max, d2bscVar, D2max, As1a, ASn2a, ASs6b, LEr), footer()
