import os

kCachePath = "data/"
kMaxTimesVisited = 250

# Caches and retrieves caches of weights when the weights are kept as 
#  a dict of feature to (timesVisited, weight), where weight is the average reward

def kingdomToFilename(kingdom, cacheFilenameKey):
    name = ""
    for cardID in kingdom:
        name += str(cardID) + "-" + str(kingdom[cardID]) + "#"
    return kCachePath + cacheFilenameKey + name

def bpcacheWeights(kingdom, weights, cacheFilenameKey=""):
	filename = kingdomToFilename(kingdom, cacheFilenameKey)
	f = open(filename, "w")
	print "caching"
	for feature, weight in weights.iteritems():
		f.write(feature + "#" + str(weight[0]) + "#" + str(weight[1]) + "\n")

# The reduction factor reduces the value of the number of times we've seen the given 
#   feature. This speeds up the learning rate because the average reward is affected 
#   more on each game when the number of times visited is smaller.
# 
def bpsetWeightsFromCache(kingdom, weights, cacheFilenameKey="", reductionFactor=1):
	filename = kingdomToFilename(kingdom, cacheFilenameKey)
	if os.path.isfile(filename):
		f = open(filename, "r")
		for line in f:
			splitLine = line.split("#")
			feature = splitLine[0]
			numTimesVisited = float(splitLine[1]) / reductionFactor
			numTimesVisited = min(kMaxTimesVisited, float(splitLine[1]))
			weight = (numTimesVisited, float(splitLine[2]))
			weights[feature] = weight
		return True
	else:
	    return False
    
