import sys


alphabet = ['$', 'A', 'C', 'G', 'T']

# reads an input file into a single string and cuts away all new-lines
def readInputFile(filename):
	f = open(filename, 'r')
	sequence = ''
	for line in f:
		line = line.replace('\n', '')
		sequence += line
		
	return sequence

# compute the type array for a given string S ( array consists of elements of {0,1}, 1 for S and 0 for L)
def computeTypeArray(S):
	typearray = []
	for i in range(len(S)):
		typearray.append(0)
		
	length = len(S)
	typearray[length - 1] = 1
	i = length - 2
	while(i >= 0):
		if(S[i] < S[i+1]):
			typearray[i] = 1
		else:
			if(S[i] == S[i+1]):
				typearray[i] = typearray[i+1]
			
		i -= 1
		
	return typearray

# compute all LMS positions for a given typeArray
def computeLMSPositions(typeArray):
	lmspos = []
	for i in range(len(typeArray)-1):
		if(typeArray[i] == 0 and typeArray[i+1] == 1):
			lmspos.append(i+1)
			
	return lmspos

# returns an array containing |alphabet| * 2 many pointers, for each character one start and end pointer as bucket in the sequence S
def initializeBucketPointers(S):
	pointers = []
	sorteds = sorted(S)
	sorteds = ''.join(sorteds)
	for c in alphabet:
		start = sorteds.find(c)
		end = sorteds.rfind(c)
		pointers.append(start)
		pointers.append(end)
	
	return pointers

# extract all substrings of S defined by lmspos intervals ( cutting the sequence string from one value as index to the next given by the array )
def extractLMSStrings(S, lmspos):
	strings = []
	for i in range(len(lmspos)-1):
		currpos = lmspos[i]
		nextpos = lmspos[i+1]
		substr = S[currpos:nextpos + 1]
		strings.append(substr)
	
	strings.append('$') # add dollar character because the dollar's position is always a S-Position and therefore the last LMS string
	return strings

# map each LMS position to its substring in the sequence by a pair (pos, substr) and add it to a list, which is returned
def mapLMSPositionsToStrings(lmspos, lmsstrings):
	lmsmap = []
	print lmspos
	print len(lmspos)
	print lmsstrings
	print len(lmsstrings)
	for i in range(len(lmspos)):
		lmsmap.append((lmspos[i], lmsstrings[i]))
	
	return lmsmap

# Step 0, fill all positions into the pos array, using the bucketpointers
def fillPositionsInBuckets(lmsmap, buckets, pos):
	length = len(lmsmap)
	i = length -1
	while (i >= 0):
		pair = lmsmap[i]
		index = alphabet.index(pair[1][0]) * 2 + 1
		pos[buckets[index]] = pair[0]
		buckets[index] -= 1
		i -= 1

# Sorts and inserts all L-positions into the position array
def sortLPositions(S, typearray, buckets, pos):
	for index in pos:
		if index != -1:
			altpos = index -1
			if(typearray[altpos] == 0):
				c = S[altpos]
				charindex = alphabet.index(c) * 2
				bucketstart = buckets[charindex]
				pos[bucketstart] = altpos
				buckets[charindex] += 1

# Sorts and inserts all S-positions into the position array
def sortSPositions(S, typearray, buckets, pos):
	length = len(pos)
	i = length -1
	while(i >= 0):
		index = pos[i]
		if (index != -1) :
			altpos = index - 1
			if(typearray[altpos] == 1):
				c = S[altpos]
				charindex = alphabet.index(c) * 2 + 1
				bucketend = buckets[charindex]
				pos[bucketend] = altpos
				buckets[charindex] -= 1		
		i -= 1	

# Removes all S-Positions to prepare pos array for S-Position sorting. Also updates the bucketpointers.			
def removeSPositions(S, typearray, buckets, pos):
	for index, position in enumerate(pos):
		if (position != -1 and typearray[position] == 1):
			pos[index] = -1
			c = S[position]
			charindex = alphabet.index(c) * 2 + 1
			buckets[charindex] += 1	
			
	
# sorting function which is used to sort pairs (tuples)
def sort(pair):
	return pair[1]
	
# Runs the Sorting Algorihm Induced Sorting
def SA_IS(S, pos):
	typearray = computeTypeArray(S)
	print typearray
	lmspos = computeLMSPositions(typearray)
	lmsstrings = extractLMSStrings(S, lmspos)
	lmsmap = mapLMSPositionsToStrings(lmspos, lmsstrings)
	lmsmap = sorted(lmsmap, key=lambda x: x[1])
	buckets = initializeBucketPointers(S)
	print lmsmap
	print buckets
	fillPositionsInBuckets(lmsmap, buckets, pos)
	print pos
	print 'Sorting L-positions'
	sortLPositions(S, typearray, buckets, pos)
	print pos
	pos_copy = list(pos)
	print 'Removing S-positions'
	removeSPositions(S, typearray, buckets, pos_copy)
	print pos_copy
	print 'Sorting S-Positions'
	sortSPositions(S, typearray, buckets, pos_copy)
	print pos_copy

####
#	Assignment 2, Task 3
#	Induced Sorting Algorithm, a linear time construction of suffix arrays
#
####

# Read arguments
args = sys.argv
print args

S = readInputFile(args[1])
S = S + '$'
print S

# Prepare pos array, initialized with -1 for each position in the string S
pos = []
for i in range(len(S)):
	pos.append(-1)

# Run algorithm
SA_IS(S, pos)
