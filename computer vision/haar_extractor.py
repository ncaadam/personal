hhfe = HueHistogramFeatureExtractor(10) #look for hue
ehfe = EdgeHistogramFeatureExtractor(10) # look at edge orientation
# look at the basic shape
haarfe = HaarLikeFeatureExtractor(fname="../../../SimpleCV/SimpleCV/Features/haar.txt")
extractors = [hhfe,ehfe,haarfe] # put these all together
svm = SVMClassifier(extractors) # try an svm, default is an RBF kernel function
tree = TreeClassifier(extractors) # also try a decision tree
trainPaths = [’./data/wine/train/’,’./data/beer/train/’,’./data/whiskey/train’]
testPaths = [’./data/wine/test/’,’./data/beer/test/’,’./data/whiskey/test/’]
# define the names of our classes
classes = [’wine’,’beer’,’whiskey’]
# train the data
print svm.train(trainPaths,classes,verbose=False)
print tree.train(trainPaths,classes,verbose=False)
print "----------------------------------------"
# now run it against our test data.
print svm.test(testPaths,classes,verbose=False)
print tree.test(testPaths,classes,verbose=False)