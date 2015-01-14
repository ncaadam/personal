import oauth2 as oauth
import urllib2 as urllib

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