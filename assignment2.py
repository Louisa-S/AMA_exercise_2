import sys
import string as pstring

string = sys.argv[1]

string += "$"
string.lower()

sortedstring = sorted(string)

stringrev = string[::-1]

types = []
lpos = []
spos = []

#computing the type of the string, L or S
for i in range(len(string)):	
	if stringrev[i] == "$":
		types.append("S")
	else:
		if stringrev[i] < stringrev[i-1]:
			types.append("S")			
		else:
			if stringrev[i] == stringrev[i-1]:
				types.append(types[i-1])				
			else:
				types.append("L")
								
	i += 1

types = types[::-1]

for i in range(len(types)):
	if types[i] == "S":
		spos.append(i)
	else:
		lpos.append(i)
		
lms = []

#computing lms positions
for i in range (len(types)):
	if types[i] == "L" and types[i+1] == "S":
		lms.append(i+1)
	i += 1
		
print lms

lmsstring = []

#computing lms substrings
for i in range(len(lms)-1):
	s = string[lms[i]:lms[i+1]+1]
	lmsstring.append(s)
	i += 1

lmsstring.append(string[lms[-1]])

print lmsstring

#sorting the substrings	
lmssort = []
for i in range(len(lms)):
	lmssort.append((lms[i], lmsstring[i]))
	
print lmssort

def getkey(item):
	return item[1]

sort = sorted(lmssort, key = getkey)

print sort

#suffix array of the lms positions
suffixarray = []

for i in sort:
	suffixarray.append(i[0])

print suffixarray

#replace each lms substring by a symbol
alpha = list(pstring.ascii_uppercase)
print alpha

sym = dict()
i = 0
for s in sort:
	if s[1] not in sym:
		if s[1] == "$":
			sym[s[1]] = "$"
		else:
			sym[s[1]] = alpha[i]
			i += 1

print sym

seq = []

#sequencq s' contain symbols fot the lms substrings
for s in lmsstring:
	seq.append(sym[s])
print seq		


#preparing the suffix array
pos = []
rank = range(len(string))

for i in rank:
	pos.append(-1)
	
#pointer for each bucket, point to the end of the bucket
p0, pa, pc, pg, pt = 0,0,0,0,0

for i in range(len(sortedstring)):
	if sortedstring[i] == "a":
		pa = i
	else:
		if sortedstring[i] == "c":
			pc = i
		else:
			if sortedstring[i] == "g":
				pg = i
			else:
				pt = i
print p0, pa, pc, pg, pt

#posittions of lms positions in respective buckets
for sub in sort[::-1]:
	if sub[1][0] == "a":
		pos[pa] = sub[0]
		pa -= 1
	else:
		if sub[1][0] == "c":
			pos[pc] = sub[0]
			pc -= 1
		else:
			if sub[1][0] == "g":
				pos[pg] = sub[0]
				pg -= 1
			else:
				if sub[1][0] == "t":
					pos[pt] = sub[0]
					pt -= 1
				else:
					pos[p0] = sub[0]

print pos
 
	
