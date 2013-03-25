from flask import Flask, render_template

app = Flask(__name__)
app.config.from_object('settings')

@app.route('/')
def home():
    return render_template('home.html')

import simple_page
app.register_blueprint(simple_page.simple_page)


if __name__ == '__main__':
    app.run()