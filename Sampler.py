import sys
import operator
import random
import json
import io
import http.client;
import networkx as nx
import numpy as np
import math

class Sampler():
	def __init__(self, node_limit):
		self.node_limit = node_limit		

	def query_public_graph(self, team, node):
		url= "/SNA2014/hw3/query.php?team=" + team
		if str(node) != "":
			url += "&node=" + str(node);
		connection = http.client.HTTPConnection("140.112.31.186", 80);
		connection.request("GET", url);
		response = connection.getresponse();
		data = response.read().decode("utf-8");
		lines = data.split('\n')

		if len(lines) == 1:
			print('you can no longer query nodes')
			return



		if str(node) != "":
			return self.process_response_data(lines)
		else:
			return self.process_subgraph(lines)



	def process_subgraph(self, lines):
		nodes = []
		edges = []
		for i in range(len(lines)):
			if lines[i] == '':
				continue
			if i == 0:
				team_id = lines[i]
			elif i == 1:
				i_th_query = lines[i]
			elif i == 2:
				kv = int(lines[i].split()[0])
				ke = int(lines[i].split()[1])
			elif i == 3 :
				ns = int(lines[i])
			elif i > 3 and i < 4 + ns :
				node_data = self.process_node_data(lines[i], kv)
				if 'id' in node_data:
					nodes.append(node_data)
			else:
				edges.append(lines[i].split())

		return nodes, edges

	def process_node_data(self, line, node_attr_num):
		node_dict = dict()
		entries = line.split()
		for j in range(len(entries)):
			if j == 0:
				node_dict['id'] = int(entries[j])
			elif j == 1:
				node_dict['degree'] = int(entries[j])
			elif j >= 2 and (j-2) < node_attr_num :
				if 'node_attr' not in node_dict:
					node_dict['node_attr'] = [int(entries[j])]
				else:
					node_dict['node_attr'].append(int(entries[j]))
			else:
				node_dict['edge_attr'] = entries[j]
		return node_dict


	def process_response_data(self, lines):
		query_node_neighbor = []
		for i in range(len(lines)):
			if i == 0:
				team_id = lines[i]
			elif i == 1:
				i_th_query = lines[i]
			elif i == 2:
				query_node = self.process_node_data(lines[i], 2147483647)
				node_attr_num = len(query_node['node_attr'])
				if node_attr_num == 0:
					print('the node you queried does not exist')
					return
			else :
				node_data = self.process_node_data(lines[i], node_attr_num)
				if 'id' in node_data:
					query_node_neighbor.append(node_data)

		return query_node, query_node_neighbor

	def maxdegree_sample(self, team):		

		graph = nx.Graph()
		max_degree_node = 1
		for i in range(self.node_limit):
			print(str(i) + ' th query')
			query_node, query_node_neighbor = self.query_public_graph(team, max_degree_node)
			graph.add_node(query_node['id'], node_attr=query_node['node_attr'], degree=query_node['degree'])
			print(query_node)

			max_degree = 0
			max_degree_node = 1
			for node in query_node_neighbor:
				graph.add_node(node['id'], node_attr=node['node_attr'], degree=node['degree'])
				if node['degree'] > max_degree:
					max_degree = node['degree']
					max_degree_node = node['id']
				if 'edge_attr' in node:
					graph.add_edge(query_node['id'], node['id'], edge_attr=node['edge_attr'])
				else:
					graph.add_edge(query_node['id'], node['id'])

		# print(graph.nodes())
	def average_degree(self, graph):
		node_num = 0
		sum_degree = 0
		for n in graph.nodes():
			node_num = node_num + 1
			sum_degree = sum_degree + graph.node[n]['degree']
		return sum_degree/node_num
	def node_attribute_preserving_sample(self, team):
		graph = nx.Graph()
		attr_distribution = [[2 for i in range(2)], [2 for i in range(2)], [2 for i in range(10)], [2 for i in range(7)], [2 for i in range(113)]]

		nodes, edges = self.query_public_graph(team, '')
		for node in nodes:
			graph.add_node(int(node['id']), node_attr=node['node_attr'], degree=node['degree'])
			for i in range(len(node['node_attr'])):
				attr_distribution[i][node['node_attr'][i]] = attr_distribution[i][node['node_attr'][i]] + 1
		for edge in edges:
			graph.add_edge(int(edge[0]), int(edge[1]))

		queried_set = set()
		query_node_neighbor = [{'id' : node} for node in graph.nodes()]

		for i in range(self.node_limit):
			print(str(i) + ' th query')
			highest_importance = 0
			node_attr_dict = nx.get_node_attributes(graph, 'node_attr')
			degree_dict = nx.get_node_attributes(graph, 'degree')


			for node in query_node_neighbor:
				n = node['id']
				graph.node[n]['importance'] = self.cal_degree_multiply_delta_kldivergence(attr_distribution, node_attr_dict[int(n)], degree_dict[int(n)])

				if graph.node[n]['importance'] > highest_importance and n not in queried_set:
					highest_importance = graph.node[n]['importance']
					most_important_node = n

			queried_set.add(most_important_node)
			print(str(highest_importance)+'\t'+str(most_important_node))

			query_node, query_node_neighbor = self.query_public_graph(team, most_important_node)
			graph.add_node(query_node['id'], node_attr=query_node['node_attr'], degree=query_node['degree'])
			for node in query_node_neighbor:
				graph.add_node(node['id'], node_attr=node['node_attr'], degree=node['degree'])

				for j in range(len(node['node_attr'])):
					attr_distribution[j][node['node_attr'][j]] = attr_distribution[j][node['node_attr'][j]] + 1


				if 'edge_attr' in node:
					graph.add_edge(query_node['id'], node['id'], edge_attr=node['edge_attr'])
				else:
					graph.add_edge(query_node['id'], node['id'])
		return self.cal_degree_distribution(graph), self.normalize_attr_distribution(attr_distribution)
			

	def cal_degree_multiply_delta_kldivergence(self, attr_distribution, node_attr, degree):
		kldivergence = 0
		for i in range(len(attr_distribution)):
			# copy_attr_distribution = list(attr_distribution[i])
			# copy_attr_distribution[node_attr[i]] = copy_attr_distribution[node_attr[i]] -1

			# probability_denominator = sum(attr_distribution[i])
			# for j in range(len(attr_distribution[i])):
			# 	kldivergence = kldivergence +  math.log((attr_distribution[i][j]/probability_denominator)/(copy_attr_distribution[j]/(probability_denominator-1)))
			# 	kldivergence = kldivergence +  math.log((copy_attr_distribution[j]/(probability_denominator-1))/(attr_distribution[i][j]/probability_denominator))

			kldivergence = kldivergence + attr_distribution[i][node_attr[i]]*math.log(attr_distribution[i][node_attr[i]]/(attr_distribution[i][node_attr[i]]-1))
			kldivergence = kldivergence + (attr_distribution[i][node_attr[i]]-1)*math.log((attr_distribution[i][node_attr[i]]-1)/attr_distribution[i][node_attr[i]])
		return degree*kldivergence;
	def create_public_graph(self, node_file, edge_file):
		graph = nx.Graph()
		with open(node_file, 'r') as f:
			for line in f:
				entries = line.strip().split(',')
				graph.add_node(int(entries[0]), node_attr=entries[1:], degree=0)
		with open(edge_file, 'r') as f:
			for line in f:
				entries = line.strip().split(',')
				graph.node[int(entries[0])]['degree'] = graph.node[int(entries[0])]['degree'] + 1
				graph.node[int(entries[1])]['degree'] = graph.node[int(entries[1])]['degree'] + 1
		return graph



	def find_attribute_range(self, filename):
		attr_distribution = [[10000,0],[10000,0],[10000,0],[10000,0],[10000,0]]
		with open(filename, 'r') as f:
			for line in f:
				entries = line.strip().split(',')[1:]
				for i in range(len(entries)):
					if int(entries[i]) > attr_distribution[i][1]:
						attr_distribution[i][1] = int(entries[i])
					if int(entries[i]) < attr_distribution[i][0]:
						attr_distribution[i][0] = int(entries[i])
		print(attr_distribution)

	def find_attribute_distribution(self, filename):
		attr_distribution = [[0 for i in range(2)], [0 for i in range(2)], [0 for i in range(10)], [0 for i in range(7)], [0 for i in range(113)]]
		with open(filename, 'r') as f:
			for line in f:
				entries = line.strip().split(',')[1:]
				for i in range(len(entries)):
					attr_distribution[i][int(entries[i])] = attr_distribution[i][int(entries[i])] + 1
		
		return self.normalize_attr_distribution(attr_distribution)		

	def normalize_attr_distribution(self, attr_distribution):
		for distribution in attr_distribution:
			denominator = sum(distribution)
			for i in range(len(distribution)):
				distribution[i] = distribution[i]/denominator

		return attr_distribution

	def kldivergence(self, true_attr_distribution, sample_attr_distribution):
		kldivergence = 0
		for i in range(len(true_attr_distribution)):
			if true_attr_distribution[i] > 0 and sample_attr_distribution[i] > 0:
				kldivergence = kldivergence +  true_attr_distribution[i]*math.log((true_attr_distribution[i])/(sample_attr_distribution[i]))
				kldivergence = kldivergence +  sample_attr_distribution[i]*math.log((sample_attr_distribution[i])/(true_attr_distribution[i]))
		return kldivergence/2
	def cal_degree_distribution(self, graph):
		degree_dict = nx.get_node_attributes(graph, 'degree')
		degree_distribution = [1 for i in range(15)]
		for n in graph.nodes():
			degree = int(degree_dict[n])
			if degree == 1:
				degree_distribution[0] = degree_distribution[0] + 1
			elif degree == 2:
				degree_distribution[1] = degree_distribution[1] + 1
			elif degree == 3:
				degree_distribution[2] = degree_distribution[2] + 1
			elif degree <= 6:
				degree_distribution[3] = degree_distribution[3] + 1
			elif degree <= 10:
				degree_distribution[4] = degree_distribution[4] + 1
			elif degree <= 15:
				degree_distribution[5] = degree_distribution[5] + 1
			elif degree <= 21:
				degree_distribution[6] = degree_distribution[6] + 1
			elif degree <= 28:
				degree_distribution[7] = degree_distribution[7] + 1
			elif degree <= 36:
				degree_distribution[8] = degree_distribution[8] + 1
			elif degree <= 45:
				degree_distribution[9] = degree_distribution[9] + 1
			elif degree <= 55:
				degree_distribution[10] = degree_distribution[10] + 1
			elif degree <= 70:
				degree_distribution[11] = degree_distribution[11] + 1
			elif degree <= 100:
				degree_distribution[12] = degree_distribution[12] + 1
			elif degree <= 200:
				degree_distribution[13] = degree_distribution[13] + 1
			else :
				degree_distribution[14] = degree_distribution[14] + 1
		denominator = sum(degree_distribution)
		for i in range(len(degree_distribution)):
			degree_distribution[i] = degree_distribution[i]/denominator
		return degree_distribution

















		


			
		



			



		




