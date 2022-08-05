#simple flask server that returns hello world
from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = dict(request.form)
        input = data['input']
        return input
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
