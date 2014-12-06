import sys
import Sampler

if __name__ == "__main__":
	team = sys.argv[1];



	node_limit = 100
	sampler = Sampler.Sampler(node_limit)

	public_graph = sampler.create_public_graph('public_nodes.txt', 'public_edges.txt')

	# print(sampler.find_attribute_range('public_nodes.txt'))
	# sampler.find_attribute_distribution('public_nodes.txt')
	true_attr_distribution = sampler.find_attribute_distribution('public_nodes.txt')
	sample_degree_distribution, sample_attr_distribution = sampler.node_attribute_preserving_sample(team)
	public_degree_distribution = sampler.cal_degree_distribution(public_graph)

	# print(public_degree_distribution)
	print(sample_degree_distribution)
	print(sampler.kldivergence(public_degree_distribution, sample_degree_distribution))

	for i in range(len(true_attr_distribution)):
		print(sampler.kldivergence(true_attr_distribution[i], sample_attr_distribution[i]))


