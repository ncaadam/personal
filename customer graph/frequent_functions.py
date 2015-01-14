import oauth2 as oauth
import urllib2 as urllib
from pymongo import MongoClient 
import ngram

def authenticate_url(access_token_key, access_token_secret,consumer_key,consumer_secret,url):    
    """
    access_token_key -> api access key
    access_token_secret -> api access secret
    consumer_key -> api account's key
    consumer_secret -> api account's secret
    url -> url to authenticate
    
    returns an opener object from url lib
    returns the authenticated url
    """

    _debug = 0
    
    oauth_token    = oauth.Token(key=access_token_key, secret=access_token_secret)
    oauth_consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)
    
    signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()
    
    http_method = "GET"

    http_handler  = urllib.HTTPHandler(debuglevel=_debug)
    https_handler = urllib.HTTPSHandler(debuglevel=_debug)
    
    oauth_token    = oauth.Token(key=access_token_key, secret=access_token_secret)
    oauth_consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)
    
    parameters = []
    req = oauth.Request.from_consumer_and_token(oauth_consumer,
                                                token=oauth_token,
                                                http_method=http_method,
                                                http_url=url,
                                                parameters=parameters)
    
    req.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)

    headers = req.to_header()
    
    if http_method == "POST":
        encoded_post_data = req.to_postdata()
    else:
        encoded_post_data = None
        url = req.to_url()
        
    opener = urllib.OpenerDirector()
    opener.add_handler(http_handler)
    opener.add_handler(https_handler)
    
    return opener,url

def set_twitter_keys():
    #twitter token keys
    access_token_key = "2544560712-jrJOwSbx1itPVchmUYAa5dgx251zNrZJckQPAab"
    access_token_secret = "x3Ur5EFUmLSX08qK1H4EIEveFTLVF4DgX0NdM5M2a5Nu2"

    #twitter consumer keys
    consumer_key = "ys3WwaOhona6vznsgn3OPVSIY"
    consumer_secret = "kKqEz3nptXXuFkOwKnw97UrUfKi3OAmUFgEjCFNxU7rRuC8Eo9"
    
    return access_token_key,access_token_secret,consumer_key,consumer_secret

def set_twitter_keys_2():
    #twitter token keys
    access_token_key = "21776771-BpXsZQi7UzkTcOZIXXy7fVNr9vbpG6jjiAd1NEOdT"
    access_token_secret = "SOmrIPr4Trwo9LofKusD6Q9KT54xhycr77bXH3bgThQBL"

    #twitter consumer keys
    consumer_key = "mpIQDS8wHuEvdrOechSEg"
    consumer_secret = "jAykYTLYuR8WUNc26o28howrad5n5h9lsC7GS2OL8iw"
    
    return access_token_key,access_token_secret,consumer_key,consumer_secret


def get_database_collection(collection_name):
    client = MongoClient()
    db = client.mysite
    python_code = "collection = db." + collection_name
    exec python_code
    return collection

def twitter_handle_remover(string):

    split_string = string.split(" ")
    no_handle_string = ""

    for word in split_string:
        if word[0] != '@':
            if len(new_string) == 0:
                new_string += word
            else:
                new_string += " " + word
        else:
            pass

    return new_string

def find_locations(search_term):
    if type(search_term) == 'string':
        items = []
        with open('usa_cities.data') as data:
            for line in data:
                items.append(line.strip())
    
        city_state_parser = ngram.NGram(items = items)
        results = city_state_parser.search(str(search_term))
        return results
    else:
        return None

def set_glassdoor_keys():
    partner_id = "19507"
    key = "evTGICdJoEq"

    return partner_id,key

def set_linkedin_keys():
    api_key = "75rxa1i3g3y8kr"
    secret_key = "88QX5bJTI8byCFQg"
    user_token = "5bb5a10c-4b5f-4837-a2ed-802968f438d8"
    user_secret = "45105892-4957-447f-a366-4cfd0d958546"

    return api_key,secret_key,user_token,user_secret