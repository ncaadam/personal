import json
import sys
from frequent_functions import authenticate_url, set_twitter_keys, set_twitter_keys_2


def grab_tweets_from_username(screen_name, num_tweets=200):
	access_token_key, access_token_secret, consumer_key, consumer_secret = set_twitter_keys()

	url = "https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=" + screen_name + "&count=" + str(
		num_tweets) + "&trim_user=1"
	opener, url = authenticate_url(access_token_key, access_token_secret, consumer_key, consumer_secret, url)
	responses = opener.open(url)
	responses_json = json.load(responses)

	return responses_json


def grab_twitter_followers(screen_name, cursor):
	access_token_key, access_token_secret, consumer_key, consumer_secret = set_twitter_keys()

	url = "https://api.twitter.com/1.1/followers/ids.json?screen_name=" + screen_name + "&stringify_ids=true" + "&cursor=" + str(cursor)
	opener, url = authenticate_url(access_token_key, access_token_secret, consumer_key, consumer_secret, url)
	responses = opener.open(url)
	responses_json = json.load(responses)

	users = []
	for key, value in responses_json.iteritems():
		if key == 'ids':
			for user in value:
				users.append(str(user))
		if key == 'next_cursor':
			next_cursor = value
	print "There were", len(users), "users returned this cursor", str(cursor)

	return users, next_cursor


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
		user_accounts_json += json.load(user_accounts)
		user_bin += 100

	return user_accounts_json


def grab_users_via_search(search_term, count=20, page=1, include_entities=False):
	access_token_key, access_token_secret, consumer_key, consumer_secret = set_twitter_keys()

	url_search_term = search_term.replace(' ', '%20')
	base_url = "https://api.twitter.com/1.1/users/search.json?"
	query_url = "q=" + url_search_term
	page_url = "page=" + str(page)
	count_url = "count=" + str(count)
	include_entities_url = "include_entities=" + str(include_entities).lower()

	url = base_url + query_url + "&" + page_url + "&" + count_url + "&" + include_entities_url

	opener, url = authenticate_url(access_token_key, access_token_secret, consumer_key, consumer_secret, url)

	responses = opener.open(url)
	responses_json = json.load(responses)

	return responses_json