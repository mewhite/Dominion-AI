import os

#The path to the folder containing the caches
kCachePath = "data/"

#Takes a kingdom and a cacheFilenameKey and turns them  into a path to the cache
def kingdomToFilename(kingdom, cacheFilenameKey):
    name = ""
    for cardID in kingdom:
        name += str(cardID) + "-" + str(kingdom[cardID]) + "#"
    return kCachePath + cacheFilenameKey + name

#Saves the given weights to the disk
def cacheWeights(kingdom, weights, cacheFilenameKey=""):
	filename = kingdomToFilename(kingdom, cacheFilenameKey)
	f = open(filename, "w")
	for feature, weight in weights.iteritems():
		f.write(feature + "#" + str(weight) + "\n")

#Pulls the weights for some kingdom cacheFilenameKey combination
def setWeightsFromCache(kingdom, weights, cacheFilenameKey=""):
	filename = kingdomToFilename(kingdom, cacheFilenameKey)
	if os.path.isfile(filename):
		f = open(filename, "r")
		for line in f:
			splitLine = line.split("#")
			feature = splitLine[0]
			weight = splitLine[1]
			weights[feature] = float(weight)
		return True
	else:
	    return False
    
