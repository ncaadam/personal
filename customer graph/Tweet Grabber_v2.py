import sys
import json
import time
from frequent_functions import authenticate_url,set_twitter_keys
from pymongo import MongoClient

def grab_tweets_from_username(username,num_tweets = 200):
    access_token_key,access_token_secret,consumer_key,consumer_secret = set_twitter_keys()
    url = "https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=" + username + "&count=" + str(num_tweets) + "&trim_user=1"
    opener,url = authenticate_url(access_token_key,access_token_secret,consumer_key,consumer_secret,url)
    responses = opener.open(url)
    responses_json = json.load(responses)
    return responses_json

    """
    i = 0
    for response in responses_json:
        i += 1
        print "\nNEW TWEET #" + str(i) + "\n"
        for key,value in response.iteritems():
            #if key == 'text' or key ==  'created_at':
            if key == 'user':
                print "---", key
                for user_entry in value.iteritems():
                    user_key = user_entry[0]
                    user_value = user_entry[1]
                    if user_key in ['id','name','screen_name','created_at']:
                        print "---", user_key, "->", user_value
            elif key in ['text','id_str','created_at']:
                print "+++", key, "->", value
    """


def upload_tweets(username):
    db = MongoClient().mysite
    cust_coll = db.testing_customer
    tweet_coll = db.testing_tweet
    cust = cust_coll.find({"handle":username})
    if(cust.count() > 0):
        for record in cust:
            cust_id = record['_id']

            dict = grab_tweets_from_username(username)
            try:
                if dict['error']:
                    print "There was an error within the API"
                    print "API Error:",dict['error']
                    return dict['error']
                else:
                    try:
                        error = dict['errors'][0]['code']
                        print 'HELLO', error
                        return dict['errors'][0]['code']
                    except Exception,e:
                        print "Yup"
                    
            except Exception,e:
                print "Saving", str(len(dict)), "of", username + "'s tweets."
                #tweet_coll.save({"testing_customer_id": cust_id, "tweets" : dict})
                return ""

                
    elif(cust.count() > 1):
        print "No tweets saved. \nThere are multiple customers with that handle."

    elif(cust.count() == 0):
        print "No tweets saved. \nNo customers have that handle."


def grab_handles_from_db():
    db = MongoClient().mysite
    cust_coll = db.testing_customer

    cust_handles = cust_coll.find({},{"handle":1})
    return cust_handles

def main():
    handles = grab_handles_from_db()
    user_counter = 0
    for cust in handles:
        user_counter += 1
        print "User#",user_counter
        status = upload_tweets(cust['handle'])
        print status
            #sys.exit()
        #time.sleep(10)
    """tweets = grab_tweets_from_username("Starbucks")
    try:
        print tweets
        error_code = tweets['errors']
        print error_code
    except Exception,e:
        print e"""


if __name__ == "__main__":
    main()