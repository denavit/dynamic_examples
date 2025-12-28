from flask import Flask, render_template
from pageText.wide_flange_column_basic import WideFlangeColumnBasic
from pageText.bolt_tensile_FEDSTD import BoltTensileFEDSTD

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Here is a free cookie!' # Not sure if the secret key is needed. It caused an error for me previously by removing it but now it is not creating any errors

@app.route('/', methods = ['POST', 'GET'])
def home():
    return render_template('home.html')

@app.route('/wide_flange_column_basic', methods = ['POST', 'GET'])
def wide_flange_column_basic():
    page_obj = WideFlangeColumnBasic.from_page()
    return page_obj.render_template()
    
@app.route('/bolt_tensile_FEDSTD', methods = ['POST', 'GET'])
def bolt_tensile_FEDSTD():
    page_obj = BoltTensileFEDSTD.from_page()
    return page_obj.render_template()

if __name__ == '__main__':
    app.run(debug = True)
