filename='public_closeness.txt'
def atr(inlist): #average true rank evaluation metrice,need the file closeness.txt to work
	try:
		fd = open(filename,"r")
	except:
		print("Can't open the file "+filename)
	rank=0.0
	index=1.0
	answer={}
	content=fd.readlines()
	for a in content:
		nodes=a.split('	')
		node=int(nodes[0])
		answer[node]=index
		index+=1.0
	for node in inlist:
		try:
			tmpr=answer[node]
			rank=rank+tmpr
		except:
			pass
	rank=rank/len(inlist)
	try:
		fd.close()
	except: 
		pass
	print(rank)
	return rank

if __name__ == "__main__":
	rank=atr([77069,59973])