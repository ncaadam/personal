import os
from PIL import Image

photo_attrib = []

Image.open("photo1.jpg")

for filename in os.listdir("./positive_images"):
	im = Image.open(filename)
	wh = im.size()
	output = "positive_images/" + filename + " 1 0 0 " + wh[0] + " " + wh[1]
	print output
