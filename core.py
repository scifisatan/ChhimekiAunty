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
    sentiments = []

    for tweet in tweets:
        sentiments.append(blob.evaluate_tweet(tweet))

    return sentiments, contexts
