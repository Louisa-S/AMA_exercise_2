import sys
import string as pstring

string = sys.argv[1]
string = string.lower()
string += "$"


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
		

lmsstring = []

#computing lms substrings
for i in range(len(lms)-1):
	s = string[lms[i]:lms[i+1]+1]
	lmsstring.append(s)
	i += 1

lmsstring.append(string[lms[-1]])


#sorting the substrings	
lmssort = []
for i in range(len(lms)):
	lmssort.append((lms[i], lmsstring[i]))
	

def getkey(item):
	return item[1]

sort = sorted(lmssort, key = getkey)


#suffix array of the lms positions
suffixarray = []

for i in sort:
	suffixarray.append(i[0])

print "Suffix array of the LMS positions:"
print suffixarray

#replace each lms substring by a symbol
alpha = list(pstring.ascii_uppercase)

sym = dict()
i = 0
for s in sort:
	if s[1] not in sym:
		if s[1] == "$":
			sym[s[1]] = "$"
		else:
			sym[s[1]] = alpha[i]
			i += 1

seq = []

#sequencq s' contain symbols fot the lms substrings
for s in lmsstring:
	seq.append(sym[s])
		


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

#start positions of the buckets
sa = p0+1
sc = pa+1
sg = pc+1
st = pg+1

#original end positions
ea = pa
ec = pc
eg = pg
et = pt


#positions of lms positions in respective buckets
#if two strings are the same, the sorting could be different
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


 
#sorting the L-positions
for r in rank:
	if pos[r] == -1:
		continue
	else:
		if pos[r]-1 in lpos:
			if string[pos[r]-1] == "a":
				pos[sa] = pos[r]-1
				sa += 1
			else:
				if string[pos[r]-1] == "c":
					pos[sc] = pos[r]-1
					sc += 1
				else:
					if string[pos[r]-1] == "g":
						pos[sg] = pos[r]-1
						sg += 1
					else:
						if string[pos[r]-1] == "t":
							pos[st] = pos[r]-1
							st += 1
		else:
			continue


#only the l positions
for r in rank:
	if pos[r] == -1:
		continue
	if pos[r] not in lpos:
		if r == 0:
			p0 = 0
		else:
			if r <= ea:
				pa += 1
			else:
				if r <= ec:
					pc += 1
				else:
					if r <= eg:
						pg += 1
					else:
						pt += 1
		pos[r] = -1

print "pos after sorting of L-positions:"
print pos

#sorting the S-positions 
for r in rank[::-1]:
	if r == 0:
		pos[0] = len(string)-1
	if pos[r] == -1:
		continue
	else:
		if pos[r]-1 in spos:
			if string[pos[r]-1] == "a":
				pos[pa] = pos[r]-1
				pa -= 1
			else:
				if string[pos[r]-1] == "c":
					pos[pc] = pos[r]-1
					pc -= 1
				else:
					if string[pos[r]-1] == "g":
						pos[pg] = pos[r]-1
						pg -= 1
					else:
						if string[pos[r]-1] == "t":
							pos[pt] = pos[r]-1
							pt -= 1
		else:
			continue

print "final pos:"
print pos
