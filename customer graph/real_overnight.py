import frequent_functions as ff
import twitter_functions as tf
import time, datetime
from pymongo import MongoClient
import json


def grab_users_from_list(users):
	access_token_key, access_token_secret, consumer_key, consumer_secret = ff.set_twitter_keys()

	user_lookup_url = "https://api.twitter.com/1.1/users/lookup.json?"
	current_users = str(users)
	current_users = current_users.replace("'", "")
	current_users = current_users.replace("[", "")
	current_users = current_users.replace("]", "")
	current_users = current_users.replace(" ", "")
	non_auth_url = user_lookup_url + 'user_id=' + current_users
	opener, auth_url = ff.authenticate_url(access_token_key, access_token_secret, consumer_key, consumer_secret, non_auth_url)
	user_accounts = opener.open(auth_url)
	user_accounts_json = json.load(user_accounts)

	return user_accounts_json

def grab_tweets_from_user_id(user_id, num_tweets=200,cursor = -1):
	access_token_key, access_token_secret, consumer_key, consumer_secret = ff.set_twitter_keys()

	url = "https://api.twitter.com/1.1/statuses/user_timeline.json?user_id=" + str(user_id) + "&count=" + str(
		num_tweets) + "&trim_user=1" + "&cursor=" + str(cursor)
	opener, url = ff.authenticate_url(access_token_key, access_token_secret, consumer_key, consumer_secret, url)
	responses = opener.open(url)
	try:
		responses_json = json.load(responses)
	except:
		return ""

	return responses_json


def get_profiles(users):
	user_bin = 0
	while user_bin < len(users):
		profile_list = []
		tweet_list = []
		for i in range(0,12,1):
			current_users = users[user_bin:(user_bin+100)]
			current_users_json = grab_users_from_list(current_users)
			
			for user in current_users_json:
				if user['protected'] == False:
					profile_list.append(user)
					if user['statuses_count'] > 200:
						tweet_list.append(user)
			user_bin += 100

		upload_profiles(profile_list)
		print "Bin #:", str((user_bin/100)/12), "is complete"
		#break
		time.sleep(61)

	return tweet_list


def get_tweets(user):
	#call_count = 0
	#initial_call_time = datetime.datetime.now()

	#for good_user in tweet_list:
	    
	    #tweets_gathered = 0
	    #tweets_list = []
	    #while tweets_gathered < good_user['statuses_count'] or tweets_gathered >= 600:
        #if call_count == 180:
        #	current_time = datetime.datetime.now()
        #	time_difference = current_time - initial_call_time
        #   time.sleep(
		#	call_count = 0

	tweets_list = []
	try:
		tweet_response = grab_tweets_from_user_id(str(user))
	except:
		tweet_response = ""
    #call_count += 1
    #tweets_gathered += 200
	for tweet in tweet_response:
		tweets_list.append(tweet)
    
	try:
		upload_tweets(tweets_list)
		print "User_ID:", str(user) + "'s tweets grabbed"
	except Exception,e:
		print "User_ID:", str(user), "had an issue."
		print e

def upload_profiles(user_list):
	db = MongoClient().mysite
	twitter_profile_coll = db.testing_twitter_profile
	for user in user_list:
		twitter_profile_coll.save({"testing_customer_id":None,"profile":user})


def upload_tweets(tweets):
    db = MongoClient().mysite
    tweet_coll = db.testing_tweet
    tweet_coll.save({"testing_customer_id": None, "tweets" : tweets})

def grab_twitter_ids_from_db():
    db = MongoClient().mysite
    prof_coll = db.testing_twitter_profile

    #twitter_ids = prof_coll.find({"profile.statuses_count":{"$gt":200}},{"profile.id":1})
    twitter_ids = prof_coll.find({"$and":[ {"profile.name" : {"$ne":""}} , {"profile.location" : {"$ne":""}} , {"profile.statuses_count":{"$gt" : 200}}]} , {"profile.id":1})
    return twitter_ids


def main():
	#with open("twitter_ids.txt") as f:
	#	output = f.read()
	#	users = output.replace("\n",",")
	#	users = users.split(",")

	#full_tweet_list = get_profiles(users)
	#print "Completed the profile grab at", str(datetime.datetime.now())
	#print "There are", str(len(full_tweet_list)), "robust users."

	user_list = grab_twitter_ids_from_db()

	
	final_list = []
	for user in user_list:

		final_list.append(user['profile']['id'])

	for good_user in final_list:
		#print good_user
		try:
			get_tweets(good_user)
		except:
			continue
		time.sleep(5)
	print "Completed the tweet grab at", str(datetime.datetime.now())
	

if __name__ == "__main__":
	main()