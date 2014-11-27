import sys
import operator
import random
import json
import io
import http.client;
import networkx as nx
import numpy as np

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
					node_dict['node_attr'] = [entries[j]]
				else:
					node_dict['node_attr'].append(entries[j])
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
		




