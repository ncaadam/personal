#import twitter
import json
import requests
import sys
from frequent_functions import authenticate_url,set_twitter_keys

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

def grab_users_from_list(users):
   	access_token_key, access_token_secret, consumer_key, consumer_secret = set_twitter_keys()

	user_bin = 0
	user_number = 0
	user_lookup_url = "https://api.twitter.com/1.1/users/lookup.json?"
	user_accounts_json = []
	while user_bin < len(users):
		current_users = str(users[user_bin:(user_bin + 100)])
		current_users = current_users.replace("'", "")
		current_users = current_users.replace("[", "")
		current_users = current_users.replace("]", "")
		current_users = current_users.replace(" ", "")
		non_auth_url = user_lookup_url + 'user_id=' + current_users
		opener, auth_url = authenticate_url(access_token_key, access_token_secret, consumer_key, consumer_secret,
											non_auth_url)
		user_accounts = opener.open(auth_url)
		user_accounts_json = json.load(user_accounts)
		user_bin += 100
		for user in user_accounts_json:
			user_number += 1
			for key,value in user.iteritems():
				if key in ['screen_name']:
					print value


def main(input_var):
    users = grab_twitter_followers(input_var)
    #grab_users_from_list(users)
    print len(users)

if __name__ == "__main__":
    main(sys.argv[1])