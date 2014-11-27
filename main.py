import sys
import Sampler

if __name__ == "__main__":
	team = sys.argv[1];

	node_limit = 10
	sampler = Sampler.Sampler(node_limit)
	sampler.maxdegree_sample(team)
