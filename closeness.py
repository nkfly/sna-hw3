import networkx as nx
import math
import operator
import sys
import Sampler

def SSSP_init(graph):
	dict = nx.all_pairs_shortest_path_length(graph)
	cc = {}
	for node1 in dict:
		if node1 not in cc:
			cc[node1] = 0
		for node2 in dict[node1]:
			if node1 == node2:
				continue
			cc[node1] = cc[node1] + 1.0 / dict[node1][node2]
	return cc, dict

def edge_update(graph, edge, cc, dd):
	u = edge[0]
	v = edge[1]
	change = 0
	if u not in dict:
		dict[u] = {}
		dict[u][v] = 1
		dict[u][u] = 0
	if v not in dict:
		dict[v] = {}
		dict[v][u] = 1
		dict[v][v] = 0
	for s in graph.nodes():
		if u not in dict[s]:
			try:
				dict[s][u] = nx.shortest_path_length(graph, s ,u)
				dict[u][s] = dict[s][u]
		if v not in dict[s]:
			try:
				dict[s][v] = nx.shortest_path_length(graph, s ,v)
				dict[v][s] = dict[s][v]
		if u in dict[s] and v in dict[s]:
			if math.fabs(dict[s][u] - dict[s][v]) > 1:
				dict[s] = {}
				dict[s] = nx.shortest_path_length(graph, s)
				change = change - cc[s]
				cc[s] = 0
				for n in dict[s]:
					cc[s] = cc[s] + 1.0 / dict[s][n]
				change = change + cc[s]
	return cc, dict

def top_k(cc, k)
	top = sorted(cc.items(), key=operator.itemgetter(1), reverse = 1)[:k]
	t = []
	for i in top:
		t.append(i[0])
	return t

def avg_true_rank(pre, true):
	k = len(pre)
	R = 0.0
	for n in pre:
		if n in true:
			R = R + 1.0 / (true.index(n) + 1)
	R = R / k
	return R

if __name__ == "__main__":
	team = sys.argv[1]
	G = nx.Graph()
	node_limit = 10
	sampler = Sampler.Sampler(node_limit)
	nodes, edges = sampler.query_public_graph(team)
	for node in nodes:
		G.add_node(node['id'], node_attr = node['node_attr'], degree = node['degree'])
	for i in range(0, len(edges), 2):
		G.add_edge((edges[i], edges[i+1]))
	cc, dd = SSSP_init(G)
	
	t = top_k(cc, k)
	if public == 1:
		f = open('public_closeness.txt', 'r')
		for i in range(100):
			
	
	f = open('closeness.txt', 'w')
	for i in t:
		f.write(str(i) + '\n')
	f.close()