import flickrapi as flickr_api
import json
import urllib
import urllib2
import sys
import os
import time
import requests 
import BeautifulSoup as bs
import urlparse as urlp
import numpy as np

def flickr_downloader(search_term):
	#set api key and secret
	"""flickr_api.set_keys(api_key = '78aa598201fe0779491cafac6c036e57', api_secret = '1397b96faca96861')"""

	print "Searching Flickr....."
	photos = flickr_api.Photo.search(tags = search_term, media = "photos")
	
	newpath = "./flickr_photos/" + str(search_term) + "/"
	if not os.path.exists(newpath): os.makedirs(newpath)

	i = 1
	print "Downloading Images....."
	for photo in photos: 
	    photo_url = "http://farm"+ str(photo.farm)+".staticflickr.com/" + str(photo.server) + "/" + str(photo.id) + "_" + str(photo.secret) + ".jpg"
	    #print photo_url
	    urllib.urlretrieve(photo_url,newpath + "photo" + str(i) + ".jpg")
	    i += 1

	print "Complete....check the path " + newpath

def flickr_downloader_list(file_name):
	
	noun_list = []
	noun_file = open(file_name)
	noun_list = noun_file.readlines()

	i = 1

	for noun in noun_list:
		i = 1
		noun = noun.replace("\r\n","")
		print "Searching Flickr for " + noun + "....."
		noun_photos = flickr_api.Photo.search(tags = noun, media = "photos")
		noun_newpath = "./flickr_photos/" + str(noun) + "/"
		if not os.path.exists(noun_newpath): os.makedirs(noun_newpath)

		print "Downloading " + noun + " Images....."
		for i in range(1,100): 
			photo_url = "http://farm"+ str(noun_photos[i].farm)+".staticflickr.com/" + str(noun_photos[i].server) + "/" + str(noun_photos[i].id) + "_" + str(noun_photos[i].secret) + ".jpg"
			urllib.urlretrieve(photo_url,noun_newpath + "photo" + str(i) + ".jpg")

		print "Complete....check the path " + noun_newpath
	   
def google_images_downloader(search_term):
	
	i = 1
	raw_search_term = search_term
	
	newpath = "./google_photos/" + str(search_term) + "/"
	if not os.path.exists(newpath): os.makedirs(newpath)
	
	search_term = raw_search_term.replace(" ","%20")

	print "Searching Google....."
	while(i <= 100):
	    req_results = requests.get("https://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=" + search_term + "&userip=155.201.35.55&start=" + str(i))
	    json_results = req_results.json()
	    
	    for result in json_results['responseData']['results']:
	        for key, value in result.iteritems():
	            if key == 'unescapedUrl':
	                if value[-3:] == "jpg":
	                    urllib.urlretrieve(value,newpath + "photo" + str(i) + ".jpg")
	                i += 1
	    print str(i-1) + " pictures downloaded...."
	    time.sleep(5)

	print "Complete.....check the path " + newpath

def google_img_scraper(search_term):
	raw_search_term = search_term
	file_search_term = raw_search_term.replace(" ","_")
	search_term = raw_search_term.replace(" ","+")
	
	"""
	This defaults to coca cola can. If you want to customize the search term, use sorce below
	"""
	
	#open saved HTML text
	htmltext = open("./html files/" + file_search_term + "_search_html.html")

	#instantiate variables
	img_urls = []
	formatted_images = []
	i = 1

	#create a path for the pictures if it doesn't already exist
	newpath = "./google_photos/" + str(raw_search_term) + "/"
	if not os.path.exists(newpath): os.makedirs(newpath) 

	#run html text through BS and find all 'a' tags
	b_soup = bs.BeautifulSoup(htmltext)
	bs_results = b_soup.findAll("a")

	#find the hrefs in the html
	for r in bs_results:
	    try:
	        if "imgres?imgur" in r['href']:
	            img_urls.append(r['href'])
	    except:
	        print "This is normal"

	#parse the hrefs to find the source url for the image
	for img in img_urls:
	    orig_url = urlp.urlparse(str(img))
	    source_url = orig_url.query.split("&")[0].replace("imgurl=","")
	    formatted_images.append(source_url)

	#save all the images
	if len(formatted_images) > 0:
	    for img in formatted_images:
	    	try:
		    	print "Photo #" + str(i)
		    	print "Retrieving: " + img
		        urllib.urlretrieve(img,newpath + "photo" + str(i))
		        i += 1
		        #time.sleep(5)
	    	except:
	    		print "Photo #" + str(i) + " failed....."
	    		i += 1
	else:
		print "No images found....."
	
	print "Complete....check the path " + newpath

def main(input_var):
	#flickr
	flickr_downloader(input_var)
	#flickr_downloader_list(input_var)

	#google
	#google_images_downloader(input_var)
	#google_img_scraper(input_var)
	

if __name__ == "__main__":
	main(sys.argv[1])