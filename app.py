from flask import Flask, render_template
import os

app = Flask(__name__)


# app_static_folder = './static'

@app.route('/artist')
def artist():
    return render_template('artist.html')

@app.route('/listener')
def listener():
    return render_template('listener.html')


@app.route("/")
def hello():
    return render_template('index.html')


if __name__ == "__main__":
    # app._static_folder = os.path('./static')
    app.run(debug=True)
