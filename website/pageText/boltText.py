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
    
    def output(bolt, n, pVar, HVar, dmin, dbsc, d2min, D1bsc, D1max, d2bscVar, D2max, As1a, As1b):
        # Based off of Alexander 1977 Text, ASME B1.1-2019, and Wide Flange Page Text
        outputText = f'''
        <h1>Thread Form Dimensions</h1>
        <h4>From ASME B1.1-2019, the dimensions of a {bolt} fastener are: </h4>
        <p>$n = {n}$ (Threads/Inch)</p>
        '''
        
        outputText += r'<p>$P = \frac{1}{n} = \frac{1}{' + str(n) + r'\text{ threads/in.}} = ' + str(pVar) + r'\text{ in./thread}$</p>'
               
        outputText += f'''
        <p>$H = \\frac{{\\sqrt{3}}}{{2n}} = \\frac{{\\sqrt{3}}}{{2({n})}} = {HVar} $ (in.)</p>
        <p>$d_{{min}} = {dmin}$ (in.)</p>
        <p>$d_{{bsc}} = {dbsc}$ (in.)</p>
        <p>$d_{{2,min}} = {d2min}$ (in.)</p>
        <p>$D_{{1,bsc}} = d_{{1,bsc}} = {D1bsc}$ (in.)</p>
        <p>$D_{{1,max}} = {D1max}$ (in.)</p>
        <p>$D_{{2,bsc}} = d_{{2,bsc}} = {d2bscVar}$ (in.)</p>
        <p>$D_{{2,max}} = {D2max}$ (in.)</p>
        '''


        # How to say "they can be simplified to be exactly the same" in a short, concise manner? Currently I have "geometrically identical"
        # Also I'm currently doing += to the text to separate it into sections. Is there another way to do that that can keep it as once block while still having visual markers of sections?
        outputText += f'''
        <h1>Tensile Strength</h1>
        <h4>The ultimate tensile strength of a threaded fastener is directly proportional to the actual cross sectional area.</h4>
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

        return outputText

    def footer():
        footerText = f'''
        <h4>Footer</h4>
        <p>What to put here</p>'''

        return footerText
    

    # Returns page text
    if bolt == None:
        return header(), input(UTSs, UTSn, LE), '', footer()
    elif UTSs <= 0:
        return header(), input(UTSs, UTSn, LE), '(((UTSs))) must be greater than zero <hr />', footer()
    elif UTSn <= 0:
        return header(), input(UTSs, UTSn, LE), '(((UTSn))) must be greater than zero <hr />', footer()
    elif LE <= 0:
        return header(), input(UTSs, UTSn, LE), '(((LE))) must be greater than zero <hr />', footer()
    else:
        pVar = sigfigstr(p(n))
        HVar = sigfigstr(H(n))
        d1bscVar = sigfigstr(D1bsc)
        d2bscVar = sigfigstr(d2bsc(dbsc, H(n)))
        AbscVar = sigfigstr(Absc(dbsc))
        As1a = sigfigstr(As_FEDSTD_1a(d2bsc(dbsc, H(n)), H(n)))
        As1b = sigfigstr(As_FEDSTD_1b(dbsc, n))

        return header(), input(UTSs, UTSn, LE), output(bolt, n, pVar, HVar, dmin, dbsc, d2min, D1bsc, D1max, d2bscVar, D2max, As1a, As1b), footer()
