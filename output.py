import recorder

def sampled_edge_output(recorder):
	graph, time, queried_set, candidate_list = recorder.read_graph()
	f = open('sample.txt', 'w')
	for edge in graph.edges():
		f.write(str(edge[0]) + ' ' + str(edge[1]) + '\n')
	f.close()

def degree_output(recorder):
	f = open('degree.txt', 'w')