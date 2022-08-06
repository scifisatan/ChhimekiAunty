
from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = dict(request.form)
        input = data['input']
        if input.startswith('https://twitter.com/'):
            return render_template('tweet.html', input=input)
        else:
            return render_template('username.html', input=input)

    if request.method == 'GET':
        return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
