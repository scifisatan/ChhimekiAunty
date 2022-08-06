# Fetches tweets into list fetchedTweets
# Fetches top 5 most popular contexts/topics of the username (if available) into set topFive
# Import and call run(username)

import requests
import yaml
import json

class UserNotFound(Exception):
    pass

# the main function
def run(username, FETCHCOUNT=20):

    try:

        bearerToken = parse_yaml()
        userID = getUserID(bearerToken, username)
        #print(f"UserID is: {userID}")

        tweetData = getTweets(bearerToken, userID, FETCHCOUNT)
        jsonObj = json.loads(tweetData.text)

        fetchedTweets, fetchedContexts = getTweetsandContextList(jsonObj)
        topFiveContexts = getTopFiveContexts(fetchedContexts)

        return fetchedTweets, topFiveContexts

    except UserNotFound:
        raise UserNotFound


# parses the yaml and obtains ApiToken
def parse_yaml():
    with open("config.yaml", "r") as fileObj:
        try:
            yamlObj = yaml.safe_load(fileObj)
            # print(yamlObj)
            return yamlObj["apiBearerToken"]
        except yaml.YAMLError as excep:
            print(excep)


# Finds the top five most talked about topics
def getTopFiveContexts(fetchedContexts, topX=5):

    contexts = {}
    for item in set(fetchedContexts):
        contexts[item] = fetchedContexts.count(item)

    contexts = list(sorted(contexts.items(), key=lambda x: x[1], reverse=True))
    # print(contexts)

    return contexts[:topX]


def getTweetsandContextList(jsonObj):
    fetchedTweets = []
    fetchedContexts = []

    try:
        for tweetDict in jsonObj["data"]:
            # tweetDict for individual tweet
            fetchedTweets.append(tweetDict["text"])

        for contexts in tweetDict["context_annotations"]:
            fetchedContexts.append(contexts["entity"]["name"])
    except:
        return fetchedTweets, fetchedContexts

    return fetchedTweets, fetchedContexts


# requests api for userID
def getUserID(bearerToken, username):

    urlForId = f"https://api.twitter.com/2/users/by/username/{username}"
    headers = {"Authorization": "Bearer {}".format(bearerToken)}
    response = requests.request("GET", urlForId, headers=headers)


    try:
        return response.json()["data"]["id"]
    
    except:
        raise UserNotFound('The given user is not available')

# requests api for tweets
def getTweets(bearerToken, userID, FETCHCOUNT):
    urlForTweets = f"https://api.twitter.com/2/users/{userID}/tweets?max_results={FETCHCOUNT}&exclude=replies,retweets&tweet.fields=context_annotations"
    headers = {"Authorization": "Bearer {}".format(bearerToken)}
    response = requests.request("GET", urlForTweets, headers=headers)
    return response


if __name__ == "__main__":
    pass
