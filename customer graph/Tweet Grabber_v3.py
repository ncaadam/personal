import tweepy
from frequent_functions import set_twitter_keys
import json
from pymongo import MongoClient

def auth():
	sj = tweepy.utils.import_simplejson()
	atk,ats,ck,cs=set_twitter_keys()
	auth = tweepy.OAuthHandler(ck,cs)
	auth.set_access_token(atk,ats)
	api = tweepy.API(auth)
	return api

def upload_tweets(username,api):
    db = MongoClient().mysite
    cust_coll = db.testing_customer
    tweet_coll = db.testing_tweet
    twitter_profile_coll = db.testing_twitter_profile
    cust = cust_coll.find({"handle":username})
    if(cust.count() > 0):
        for record in cust:
            cust_id = record['_id']
            tweets = []
            try:
            	dict = api.user_timeline(username, count = 200)
            	for tweet in dict:
            		tweets.append(tweet._json)

            	if len(tweets) > 0:
            		user_profile = tweets[0]['user']
            		print "Saving", username + "'s profile."
            		twitter_profile_coll.save({"testing_customer_id":cust_id,"profile":user_profile})
            		print "Saving", str(len(tweets)), "of", username + "'s tweets."
                	tweet_coll.save({"testing_customer_id": cust_id, "tweets" : tweets})

            except Exception,e:
            	print type(e)

    elif(cust.count() > 1):
        print "No tweets saved. \nThere are multiple customers with that handle."

    elif(cust.count() == 0):
        print "No tweets saved. \nNo customers have that handle."


def grab_handles_from_db():
    db = MongoClient().mysite
    cust_coll = db.testing_customer

    cust_handles = cust_coll.find({},{"handle":1})
    return cust_handles


def grab_twitter_followers(screen_name):
    access_token_key,access_token_secret,consumer_key,consumer_secret = set_twitter_keys()

    url = "https://api.twitter.com/1.1/followers/ids.json?screen_name=" + screen_name + "&stringify_ids=true"
    opener,url = authenticate_url(access_token_key,access_token_secret,consumer_key,consumer_secret,url)
    responses = opener.open(url)
    responses_json = json.load(responses)

    users = []
    for key,value in responses_json.iteritems():
        if key == 'ids':
            for user in value:
                users.append(str(user))
    print "There were",len(users),"users returned in this request"

    return users

def main():
    handles = grab_handles_from_db()
    api = auth()
    user_counter = 0
    for cust in handles:
        user_counter += 1
        print "User#",user_counter
        upload_tweets(cust['handle'],api)
        if user_counter > 25:
        	break


if __name__ == "__main__":
    main()


