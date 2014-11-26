import sys
import Sampler

if __name__ == "__main__":
	team = sys.argv[1];

	node_limit = 1000
	sampler = Sampler.Sampler(node_limit)
	sampler.query_public_graph(team, '')
