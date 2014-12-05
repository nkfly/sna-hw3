import sys
import Sampler

if __name__ == "__main__":
	team = sys.argv[1];



	node_limit = 100
	sampler = Sampler.Sampler(node_limit)

	# sampler.find_attribute_range('public_nodes.txt')
	# sampler.find_attribute_distribution('public_nodes.txt')
	true_attr_distribution = sampler.find_attribute_distribution('public_nodes.txt')
	sample_attr_distribution = sampler.node_attribute_preserving_sample(team)

	print(sampler.kldivergence(true_attr_distribution, sample_attr_distribution))


