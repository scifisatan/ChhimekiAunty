import blob
import tweetSource
import re


def process_data(user_input):
    
    expression = r"(https://)?(www\.)?(twitter.com/)?(?P<username>[-_a-zA-Z0-9]*)(\?.*|/.*)?"

    try:

        #a url of username is provided the first extract the username
        if user_name := re.search(expression, user_input):

            user_name = user_name.group('username')

            tweets, contexts = tweetSource.run(user_name)

            #here we receive a list of tweets to analysis
            #a list of sentiment for each tweets will be provided
            polarity = []
            subjectivity = []

            pol_avg = 0.0
            sub_avg = 0.0

            if len(tweets) == 0:
                raise blob.TweetIsEmpty
                
            for tweet in tweets:
                result = blob.evaluate_tweet(tweet)
                polarity.append(result[0])
                subjectivity.append(result[1])
                pol_avg = sum(polarity) / len(polarity)
                sub_avg = sum(subjectivity) / len(subjectivity)

            return polarity, subjectivity, contexts, pol_avg, sub_avg, user_name
        else:
            raise tweetSource.UserNotFound

    except tweetSource.UserNotFound:
        raise tweetSource.UserNotFound
    
    except blob.TweetIsEmpty:
        raise blob.TweetIsEmpty

    

