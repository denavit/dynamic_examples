from math import # Relevant Math Functions
from dictionaries import # Relevant Dictionaries
from main import sigfigstr

def overallTextFunction( #All Relevant Variables
        ):
    def header():
        headerText = f'''
        <h1>Some form of header text</h1>'''
        return headerText
    
    def input(inputs):
        inputText = f'''
        <div class="section">
            <div class="col-3">
                <label
                    class="xxxxxxx"
                    for="dropdown">
                    Some sort of select label (if applicable)
                </label>
                <select class="dropdown" id="dropdown" name="dropdown">
                    <option id="xxxxxxx" value="xxxxxxx">Select options (if applicable)</option>
                </select>
            </div>
            <script>
            document.getElementById("dropdown").onchange = function () {{
                sessionStorage.setItem(
                "_____SelectItem",
                document.getElementById("dropdown").value
                );
                this.form.submit();
            }};

            if (sessionStorage.getItem("____SelectItem")) {{
                document.getElementById("dropdown").options[
                sessionStorage.getItem("____SelectItem")
                ].selected = true;
            }}
            </script>
            <div class="col-3">
                <label class="xxxxxxx" for="input"
                    >Relevant label for input (if applicable) :
                </label>
                <input
                    class="input"
                    type="text"
                    id="Variable"
                    value="{'%g'%(Variable)}"
                    name="Variable"
                />
                <label class="unit">UNITS</label>
            </div>
        </div>
        <hr />'''
    
        return inputText
    
    def output(inputs):
        outputText = f'''
        <h1>Section title</h1>
        <h4>Section subheader (if applicable)</h4>
        <p>Section Text</p>
        '''

        return outputText

    def footer():
        footerText = f'''
        <h4>Footer</h4>
        <p>What to put here</p>'''

        return footerText
    

    # Returns page text
    if object == None:
        return header() + input(inputs) + footer()
    elif var1 <= 0:
        return header() + input(inputs) + '(((UTSs))) must be greater than zero <hr />' + footer()
    elif var2 <= 0:
        return header() + input(inputs) + '(((UTSn))) must be greater than zero <hr />' + footer()
    elif var3 <= 0:
        return header() + input(inputs) + '(((LE))) must be greater than zero <hr />' + footer()
    else:
        # Obtain dictionary items/calculate repeated variables
        x = 2*y
        var4 = dictionary[object]['variable required']

        return header() + input(inputs) + output(inputs) + footer()
