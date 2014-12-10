import recorder
from operator import itemgetter
import networkx as nx

def which_bin(degree):
	if degree == 1:
		return 0
	elif degree == 2:
		return 1
	elif degree == 3:
		return 2
	elif degree <= 6:
		return 3
	elif degree <= 10:
		return 4
	elif degree <= 15:
		return 5
	elif degree <= 21:
		return 6
	elif degree <= 28:
		return 7
	elif degree <= 36:
		return 8
	elif degree <= 45:
		return 9
	elif degree <= 55:
		return 10
	elif degree <= 70:
		return 11
	elif degree <= 100:
		return 12
	elif degree <= 200:
		return 13
	else :
		return 14

def de_bin(iter):
	if iter == 0:
		return (1, 1)
	elif iter == 1:
		return (2, 2)
	elif iter == 2:
		return (3, 3)
	elif iter == 3:
		return (4, 6)
	elif iter == 4:
		return (7, 10)
	elif iter == 5:
		return (11, 15)
	elif iter == 6:
		return (16, 21)
	elif iter == 7:
		return (22, 28)
	elif iter == 8:
		return (29, 36)
	elif iter == 9:
		return (37, 45)
	elif iter == 10:
		return (46, 55)
	elif iter == 11:
		return (56, 70)
	elif iter == 12:
		return (71, 100)
	elif iter == 13:
		return (101, 200)
	else :
		return (201, 0)

def attr_len(j):
	if j == 0:
		return 1534
	elif j == 1:
		return 2
	elif j == 2:
		return 384
	else:
		return 3

def sampled_edge_output():
	graph, time, queried_set, candidate_list = recorder.read_graph()
	f = open('sample.txt', 'w')
	for edge in graph.edges():
		f.write(str(edge[0]) + ' ' + str(edge[1]) + '\n')
	f.close()

def degree_output():
	graph, time, queried_set, candidate_list = recorder.read_graph()
	all = 0.0
	deg_list = [0.0]*15
	testsum = 0.0
	degree_dict = nx.get_node_attributes(graph, 'degree')
	for node in degree_dict:
		iter = which_bin(degree_dict[node])
		deg_list[iter] = deg_list[iter] + 1
		all = all + 1
	for i in range(len(deg_list)):
		deg_list[i] = deg_list[i] / all
		testsum = testsum + deg_list[i]
	if testsum < 0.9999 or testsum > 1.0001:
		for i in range(len(deg_list)):
			deg_list[i] = deg_list[i] / testsum
	deg_list.reverse()
	f = open('degree.txt', 'w')
	for i in range(len(deg_list)):
		f.write(str(de_bin(i)[0]) + ' ' + str(de_bin(i)[1]) + ' ' + str(deg_list[i]) + '\n')
	f.close()
	
def closeness_output():
	graph, time, queried_set, candidate_list = recorder.read_graph()
	degree_dict = nx.get_node_attributes(graph, 'degree')
	maxkey=sorted(degree_dict,key=degree_dict.get,reverse=True)
	f = open('closeness.txt', 'w')
	for x in range(100):
		f.write(str(int(maxkey[x])) + '\n')
	f.close()

def attr_output():
	graph, time, queried_set, candidate_list = recorder.read_graph()
	attr_distribution = {}
	node_attr_dict = nx.get_node_attributes(graph, 'node_attr')
	for j in range(4):
		attr_distribution[j] = {}
		all = 0.0
		testsum = 0.0
		for n in graph.nodes():
			if node_attr_dict[n][j] not in attr_distribution[j]:
				attr_distribution[j][node_attr_dict[n][j]] = 0.0
			attr_distribution[j][node_attr_dict[n][j]] = attr_distribution[j][node_attr_dict[n][j]] + 1.0
			all = all + 1.0
		for atr in attr_distribution[j]:
			attr_distribution[j][atr] = attr_distribution[j][atr] / all
			testsum = testsum + attr_distribution[j][atr]
		if testsum < 0.9999 or testsum > 1.0001:
			for atr in attr_distribution[j]:
				attr_distribution[j][atr] = attr_distribution[j][atr] / testsum
		for i in range(attr_len(j)):
			if i not in attr_distribution[j]:
				attr_distribution[j][i] = 0.0
		maxkey = sorted(attr_distribution[j].items(), key=itemgetter(0))
		f = open('node_attr_' + str(j + 1) + '.txt', 'w')
		for x in maxkey:
			f.write(str(x[0]) + ' ' + str(x[1]) + '\n')
		f.close()
	