from flask import render_template

class Page:
  def render_template(self):
      return render_template('base.html', 
                name = self.name, title = self.title, 
                headerText = self.header(), inputText = self.input(), 
                outputText = self.output(), footerText = self.footer())
