import Sampler
import networkx as nx
import numpy as np

def create_first_graph(password,sampler):
	nodes,others=sampler.query_public_graph(team,"")
	mygraph=nx.Graph()
	for edge in others:
		mygraph.add_edge(int(edge[0]),int(edge[1]))
	for node in nodes:
		mygraph.node[node['id']]['degree']=int(node['degree'])
	return mygraph

def choose_seed(graph):
	nodes_list=graph.nodes()
	max=0
	id=0
	for node in nodes_list:
		if graph.node[node]['degree'] > max:
			max=graph.node[node]['degree']
			id=node
	return id

def forest_fire_sample(graph,list,pf,count,limit,password,sampler):
	while(len(list)>0 and count < limit):
		point=list[0]
		list.remove(point)
		node,neighbors=sampler.query_public_graph(team,str(point))
		count=count +1
		for neighbor in neighbors :
			mygraph.add_edge(point,neighbor['id'])
			mygraph.node[neighbor['id']]['degree']=neighbor['degree']
		w=np.random.geometric(pf)
		tmpw=w
		for neighbor in neighbors :
			if w==0:
				break
			sample_degree_dic=graph.degree([neighbor['id']])
			sample_degree=sample_degree_dic[neighbor['id']]
			true_degree=mygraph.node[neighbor['id']]['degree']
			if sample_degree != true_degree:
				list.append(neighbor['id'])
				w=w-1
		'''check="point "+str(point)+",length "+str(len(list))+", w="+str(tmpw)+","+str(graph.number_of_nodes())+" nodes, Query "+str(count)
		f.write(check)
		print(check)'''
		
def get_graph_degree_destribution(graph):
	degs={}
	seq_list=list()
	for node in graph.nodes():
		seq_list.append(graph.node[node]['degree'])
	seq_list.sort()
	for n in seq_list:
		if n not in degs:
			degs[n] = 0
		degs[n]+=1
	
	return degs

def get_graph_degree_prob_distribution(graph,distribution=None):
		degs={}
		if distribution==None:
			real=get_graph_degree_destribution(graph)
		nodes=float(graph.number_of_nodes())
		for key,value in degree_distribution.items():
			degs[key]=float(value)/nodes
		return degs

if __name__ == "__main__":
	team = "s5PMHD50Tb";
	node_limit = 1000
	query_time = 0
	probability=0.25
	sampler = Sampler.Sampler(node_limit)
	mygraph=create_first_graph(team,sampler)
	#choose the first node to sample
	first_seed=choose_seed(mygraph)
	# add the first seed to a list
	burning_list=list()
	burning_list.append(first_seed)
	forest_fire_sample(mygraph,burning_list,probability,query_time,node_limit,team,sampler)
	degree_distribution= get_graph_degree_destribution(mygraph)
	prob_distribution= get_graph_degree_prob_distribution(mygraph,degree_distribution)
	