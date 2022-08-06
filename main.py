
from distutils.log import debug
from flask import Flask, render_template, request
from blob import TweetIsEmpty
import core
from tweetSource import UserNotFound
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = dict(request.form)
        input = data['input']

        #send input data to twitter api, and model
        #the api will be used only for username
        try:
            polarity, subjectivity, contexts, pol_avg, sub_avg, user_name = core.process_data(input)
            
            data_dict = {
                'polarity': polarity,
                'subjectivity': subjectivity,
                'contexts': contexts,
                'pol_avg': pol_avg,
                'sub_avg': sub_avg,
                'user_name': user_name
                }

            return render_template('username.html', data = data_dict)

        except TweetIsEmpty:
            return render_template('notfound.html')

        except UserNotFound:
            return render_template('notfound.html')

    if request.method == 'GET':
        return render_template("index.html")


if __name__ == '__main__':
    os.system("python -m textblob.download_corpora") 
    app.run(host='0.0.0.0',debug=True)
