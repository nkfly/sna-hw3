import pickle
import networkx as nx

#基本實作概念，把東西都塞到圖裡面當作是 attribute 打算把他都變成 function 以隱藏

#儲存圖需要使用的function需要給他 圖 已經使用的次數 最後可以把每次 query 的點都 記在一個 list 中 我會把它存取在 record.gpickle 內
def store_graph(graph,time,queried_set = None,candidate = None):
	try:
		graph.graph['used_time'] = time
		if candidate != None:
			graph.graph['candidate_list'] = candidate
		if queried_set != None:
			graph.graph['queried_set'] = queried_set
		nx.write_gpickle(graph,"record.gpickle")
		return True
	except:
		return False

def read_graph(path = None, data = True):
	try:
		if path == None:
			path = "record.gpickle"
		graph = nx.read_gpickle(path)
		time = graph.graph['used_time']
		a = graph.graph['queried_set']
		b = graph.graph['candidate_list']
		if data == True:
			return graph, time, a, b
		else:
			return graph
	except:
		a = set()
		b=list()
		return nx.Graph(), 0, a, b

#這個 function 單純就只是把每次紀錄的點記下來也可以自己做一個 list 最後在儲存時把它用出來
'''def add_point(graph,point):
	if 'candidate_list' not in graph.graph:
		graph.graph['candidate_list'] = list()
	graph.graph['candidate_list'].append(point)
	
def remove_point(graph,point):
	if 'candidate_list' not in graph.graph:
		return True
	else :
		graph.graph['candidate_list'].remove(point)'''