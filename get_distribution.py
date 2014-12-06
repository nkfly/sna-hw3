def get_distribution(filename):
	#open the file
	try:
		fd = open(filename,"r")
	except:
		print("Can't open the file"+filename)
	content=fd.readlines()
	degree_distribution = [1 for i in range(15)]
	for a in content:
		nodes=a.split(' ')
		degree=int(nodes[0])
		total=int(nodes[1])
		if degree == 1:
				degree_distribution[0] = degree_distribution[0] + total
		elif degree == 2:
			degree_distribution[1] = degree_distribution[1] + total
		elif degree == 3:
			degree_distribution[2] = degree_distribution[2] + total
		elif degree <= 6:
			degree_distribution[3] = degree_distribution[3] + total
		elif degree <= 10:
			degree_distribution[4] = degree_distribution[4] + total
		elif degree <= 15:
			degree_distribution[5] = degree_distribution[5] + total
		elif degree <= 21:
			degree_distribution[6] = degree_distribution[6] + total
		elif degree <= 28:
			degree_distribution[7] = degree_distribution[7] + total
		elif degree <= 36:
			degree_distribution[8] = degree_distribution[8] + total
		elif degree <= 45:
			degree_distribution[9] = degree_distribution[9] + total
		elif degree <= 55:
			degree_distribution[10] = degree_distribution[10] + total
		elif degree <= 70:
			degree_distribution[11] = degree_distribution[11] + total
		elif degree <= 100:
			degree_distribution[12] = degree_distribution[12] + total
		elif degree <= 200:
			degree_distribution[13] = degree_distribution[13] + total
		else :
			degree_distribution[14] = degree_distribution[14] + total
	denominator = sum(degree_distribution)
	for i in range(len(degree_distribution)):
		degree_distribution[i] = degree_distribution[i]/denominator
	#	print("The Undirected Graph here has "+str(uGraph.number_of_edges())+" edges and "+str(uGraph.number_of_nodes())+" vertex")
	#close the file
	try:
		fd.close();
	except: 
		pass
	return degree_distribution
	
if __name__ == "__main__":
	degree=get_distribution("output.txt")
	print(degree)