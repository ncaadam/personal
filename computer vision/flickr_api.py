import flickr_api
import json
import urllib
import sys

def flickr_downloader(search_term):
	#set api key and secret
	flickr_api.set_keys(api_key = '78aa598201fe0779491cafac6c036e57', api_secret = '1397b96faca96861')

	photos = flickr_api.Photo.search(tags = search_term, media = 'photos')

	i = 1

	for photo in photos: 
	    photo_url = "http://farm"+ str(photo.farm)+".staticflickr.com/" + str(photo.server) + "/" + str(photo.id) + "_" + str(photo.secret) + ".jpg"
	    print photo_url
	    urllib.urlretrieve(photo_url,"./" + search_term + "/photo" + str(i) + ".jpg")
	    i += 1

flickr_downloader(sys.argv)