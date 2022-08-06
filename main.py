
from distutils.log import debug
from flask import Flask, render_template, request
import core

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = dict(request.form)
        input = data['input']

        #send input data to twitter api, and model
        #the api will be used only for username
        

        if input.startswith('https://twitter.com/'):

            return render_template('tweet.html', input=input)
        else:
            polarity, subjectivity, contexts, pol_avg, sub_avg = core.process_data(input)
            return render_template('username.html', input = \
            {'polarity': polarity,
            'subjectivity': subjectivity,
            'contexts': contexts,
            'pol_avg': pol_avg,
            'sub_avg': sub_avg
            })

    if request.method == 'GET':
        return render_template("index.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080,debug=True)
