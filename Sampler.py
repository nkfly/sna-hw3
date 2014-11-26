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
		self.g = nx.Graph()

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
			self.process_response_data(lines)
		else:
			self.process_subgraph(lines)



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
				nodes.append(self.process_node_data(lines[i], kv))
			else:
				edges.append(lines[i].split())

		print(nodes)
		print(edges)


	def process_node_data(self, line, node_attr_num):
		node_dict = dict()
		entries = line.split()
		for j in range(len(entries)):
			if j == 0:
				node_dict['id'] = entries[j]
			elif j == 1:
				node_dict['degree'] = entries[j]
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
				query_node_neighbor.append(self.process_node_data(lines[i], node_attr_num))


		print(query_node)
		print(query_node_neighbor)


