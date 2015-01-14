import sys
import json
from frequent_functions import authenticate_url,set_twitter_keys

def grab_tweets_from_username(username,num_tweets = 200):
    #username = 'Starbucks'
    #tweet_count = 200
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

def main(username,num_tweets = 200):
    if(int(num_tweets) > 200):
        print "Only 200 tweets per user per request"
    else:
        tweets = grab_tweets_from_username(username,num_tweets)
        print tweets

if __name__ == "__main__":
    main(sys.argv[1])