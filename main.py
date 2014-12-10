import sys
import Sampler
import recorder
import output

if __name__ == "__main__":
	team = sys.argv[1];
	node_limit = sys.argv[2];
	#node_limit = 300
	sampler = Sampler.Sampler(node_limit*3/100)

	# public_graph = sampler.create_public_graph('public_nodes.txt', 'public_edges.txt')

	# print(sampler.find_attribute_range('public_nodes.txt'))
	# sampler.find_attribute_distribution('public_nodes.txt')
	# true_attr_distribution = sampler.find_attribute_distribution('public_nodes.txt')
	
	graph, time, queried_set, candidate_list = recorder.read_graph(None)
	graph,time, queried_set, candidate_list, sample_degree_distribution, sample_attr_distribution = sampler.node_attribute_preserving_sample(team, graph, time, queried_set, candidate_list, 1)
	recorder.store_graph(graph, time, queried_set,  candidate_list)

	sampler = Sampler.Sampler(node_limit/2 - node_limit*3/100)
	graph, time, queried_set, candidate_list = recorder.read_graph(None)
	graph,time, queried_set, candidate_list, sample_degree_distribution, sample_attr_distribution = sampler.node_attribute_preserving_sample(team, graph, time, queried_set, candidate_list, 2)
	recorder.store_graph(graph, time, queried_set,  candidate_list)
	
	sampler = Sampler.Sampler(node_limit/2)
	graph, time, queried_set, candidate_list = recorder.read_graph(None)
	graph,time, queried_set, candidate_list, sample_degree_distribution, sample_attr_distribution = sampler.node_attribute_preserving_sample(team, graph, time, queried_set, candidate_list, 3)
	recorder.store_graph(graph, time, queried_set,  candidate_list)
	

	# public_degree_distribution = sampler.cal_degree_distribution(public_graph, True)
	#closeness_node=sampler.get_100_highest_closeness(graph)
	#sampler.atr(closeness_node)
	# # print(public_degree_distribution)
	#sample_degree_distribution.reverse()
	#print(sample_degree_distribution)
	# print(sampler.kldivergence(public_degree_distribution, sample_degree_distribution))

	#for i in range(len(sample_attr_distribution)):
		# print(sampler.kldivergence(true_attr_distribution[i], sample_attr_distribution[i]))
		#print(sample_attr_distribution[i])
	output.sampled_edge_output()
	output.degree_output()
	output.closeness_output()
	output.attr_output()

