#we will be using textblob for the sentiment analysis of tweets

#imports
from textblob import TextBlob

def __clean_data(tweet):
    #the cleaning has to be implemented
    return tweet

def evaluate_tweet(tweet: str):

    #clean the tweet
    tweet = __clean_data(tweet)

    #there could be multiple sentences in a tweet
    blob = TextBlob(tweet)

    #we will evaluate polarity and subjectivity in a tweet
    pol = []
    sub = []

    for sentence in blob.sentences:
        pol.append(sentence.sentiment.polarity)
        sub.append(sentence.sentiment.subjectivity)
    
    #return the avg``
    return sum(pol) / len(pol), sum(sub) / len(sub)


if __name__ == "__main__":
    pass

