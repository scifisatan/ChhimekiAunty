from model import blob
from tweetSource import tweetSource

class CannotProcessUrl(Exception):
    pass

def process_data(user_input):
    
    if user_input.startswith('https://twitter.com'):
        raise CannotProcessUrl("Only username can be used in the field")
    
    #send the username to tweetSource to receive tweets, and context
    tweets, contexts = tweetSource.run(username=user_input)

    #here we receive a list of tweets to analysis
    #a list of sentiment for each tweets will be provided
    polarity = []
    subjectivity = []

    for tweet in tweets:
        result = blob.evaluate_tweet(tweet)
        polarity.append(result[0])
        subjectivity.append(result[1])

    pol_avg = sum(polarity) / len(polarity)
    sub_avg = sum(subjectivity) / len(subjectivity)

    return polarity, subjectivity, contexts, pol_avg, sub_avg
