from math import floor, log10

def sigfigstr(n,sigfigs=4):
    n = float(n)
    sigfigsleft = floor(log10(n)) + 1
    if sigfigsleft > sigfigs:
        n = int(round(n,sigfigs-sigfigsleft))
        return f'{n:0,}'
    else:
        format_str = '{:.' + str(sigfigs-sigfigsleft) + 'f}'
        return format_str.format(n)
        
class htmlstr:
    def __init__(self, newstr='', default_indent=0, indent_multiplier=1):
        self.string = newstr
        self.default_indent = default_indent
        self.indent_multiplier = indent_multiplier
        
    def append(self, newstr):
        self.string += newstr
        
    def newline(self, newstr, indent=None, tag=None):
        if self.string is not '':
            self.string += '\n'
       
        if indent is None:
            self.string += ' '*self.default_indent*self.indent_multiplier
        else:
            self.string += ' '*self.indent*self.indent_multiplier

        if tag is not None:
            newstr = f'<{tag}>' + newstr + f'</{tag}>'
            
        self.string += newstr
