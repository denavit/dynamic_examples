from flask import request
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
    # Gets bolt data
    text = ''

    # Did functions this way as I couldn't figure out how to call the function in the text. No combination of braces would allow it to work
    pVar = p(n)
    HVar = H(n)
    d2bscVar = d2bsc(dbsc, HVar)
    AbscVar = Absc(dbsc)
    As = As_FEDSTD_1a(d2bscVar, HVar)

    # Based off of Alexander 1977 Text

    text += f'''
    <h1>Geometric/Dimensional Properties</h1>
    <p>$P = \\frac{{1}}{{n}} = \\frac{{1}}{{{n}}} = {sigfigstr(pVar)}$ UNITS</p>
    <p>$H = \\frac{{\sqrt{3}}}{{2n}} = \\frac{{\sqrt{3}}}{{2({n})}} = {sigfigstr(HVar)}$ UNITS</p>
    <p>Maybe d1bsc and d2bsc?</p>
    '''

    text += f'''
    <h1>Areas??</h1>
    <p>The ultimate tensile strength of a threaded fastener is directly proportional to the actual cross sectional area: </p>
    <p>$A_{{s}} = \\pi\\left(\\frac{{d_{{2,bsc}}}}{{2}}-\\frac{{3H}}{{16}}\\right)^{{2}}$</p>
    '''

    text += r'$= \pi\left(\frac{' + sigfigstr(d2bscVar) + r'}{2}-\frac{3(' + sigfigstr(HVar) + r')}{16}\right)^{2}$'

    return text
