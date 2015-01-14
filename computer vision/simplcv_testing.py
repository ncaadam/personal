import SimpleCV as s
import numpy as np

img = s.Image('./pepsican.jpeg')
img = img.scale(.2)
binary = img.binarize(215).invert()
binary2 = img.hueDistance(1).invert().threshold(0)
filled = binary.floodFill((0,img.height-1),color = s.Color.BLACK)
better = filled.logicalOR(binary2)
eroded = better.erode()
dialated = better.dilate(1)
final = dialated.watershed()

blobs = final.findBlobs(threshval=175,minsize=50)
blobs.draw(width = -1, color = s.Color.BLUE)

final.show()