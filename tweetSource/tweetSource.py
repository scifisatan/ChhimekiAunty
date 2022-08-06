#Fetches tweets into list fetchedTweets
#Fetches top 5 most popular contexts/topics of the username (if available) into set topFive 
#Import and call run(username)

import requests
import yaml
import json

 
FETCHCOUNT = 50
fetchedTweets = []
fetchedContexts = []

topFive = set()


#the main function
def run(username):
    bearerToken = parse_yaml()

    userID = getUserID(bearerToken, username)
    print(f"UserID is: {userID}")

    tweetData = getTweets(bearerToken, userID)
    jsonObj = json.loads(tweetData.text)
    print(json.dumps(jsonObj, indent =4))
    try:
        loadGlobals(jsonObj)
        topFiveTopics(fetchedContexts)
    except:
        if len(fetchedTweets) > 0:
            print("Only Tweets Loaded, There were no contexts.")

    print("Top Five Contexts: ")
    print(topFive)


#parses the yaml and obtains ApiToken
def parse_yaml():
    with open("config.yaml", "r") as fileObj:
        try:
            yamlObj = yaml.safe_load(fileObj)
            # print(yamlObj)
            return yamlObj["apiBearerToken"]
        except yaml.YAMLError as excep:
            print(excep)


#Finds the top five most talked about topics
def topFiveTopics(fetchedContexts):
    if len(topFive) != 5:
        highest = max(set(fetchedContexts), key=fetchedContexts.count)
        # print(highest)
        topFive.add(highest)
        topFiveTopics(list(filter(lambda a: a != highest, fetchedContexts)))
    else:
        pass


#loads tweets from api payload to fetchedTweets and fetchedContexts
def loadGlobals(jsonObj):
    for tweetDict in jsonObj["data"]:
        # tweetDict for individual tweet
        fetchedTweets.append(tweetDict["text"])
        
        for contexts in tweetDict["context_annotations"]:
            fetchedContexts.append(contexts["entity"]["name"])
        
    print("Fetched Tweets: ")
    print(fetchedTweets)
    # print("FetchedContexts: ")
    # print(fetchedContexts)


#requests api for userID
def getUserID(bearerToken, username):

    urlForId = f"https://api.twitter.com/2/users/by/username/{username}"
    headers = {"Authorization": "Bearer {}".format(bearerToken)}
    response = requests.request("GET", urlForId, headers=headers)

    if response.status_code != 200:
        raise Exception("Error {}: {}".format(response.status_code, response.text))

    return response.json()["data"]["id"]


#requests api for tweets
def getTweets(bearerToken, userID):
    urlForTweets = f"https://api.twitter.com/2/users/{userID}/tweets?max_results={FETCHCOUNT}&exclude=replies,retweets&tweet.fields=context_annotations"
    headers = {"Authorization": "Bearer {}".format(bearerToken)}
    response = requests.request("GET", urlForTweets, headers=headers)
    return response


if __name__ == "__main__":
    run("safal2002")