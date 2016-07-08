#! /usr/bin/python
# -*- coding: utf-8 -*-

import re


class Graph(object):
	def __init__(self):
		self.graph = {}
		self.u_edge_count = 0

		# dicts to convert between index and label
		self.label_to_index = {}
		self.index_to_label = {}

		self.vert_count = 0


	def add_vert(self, label):
		if not self.is_vert_label(label):
			self.label_to_index[label] = self.vert_count
			self.index_to_label[self.vert_count] = label
			self.graph[self.vert_count] = set()
			self.vert_count += 1


	def add_undirected_edge(self, edge_label):
		# add 2 directed edges to simulate undirected edge
		if self.add_directed_edge(edge_label) and self.add_directed_edge(edge_label[::-1]):
			self.u_edge_count += 1


	# edge = [v_from, v_to]
	def add_directed_edge(self, edge_label):
		self.add_vert(edge_label[0])
		self.add_vert(edge_label[1])

		v_from = self.label_to_index[edge_label[0]]
		v_to = self.label_to_index[edge_label[1]]

		if not v_to in self.graph[v_from]:
			self.graph[v_from].add(v_to)
			return True
		return False


	def get_verts(self):
		return self.graph.keys()


	def get_neighbors(self, index):
		return self.graph[index]


	def is_vert_label(self, label):
		return label in self.label_to_index


	def is_vert_index(self, index):
		return index in self.index_to_label


	def is_directed_edge(self, edge_index):
		v_from = edge_index[0]
		v_to = edge_index[1]

		return self.is_vert_index(v_from) and v_to in self.get_neighbors(v_from)


	def is_undirected_edge(self, edge_index):
		return self.is_directed_edge(index_edge) and self.is_directed_edge(edge_index[::-1])


	def degree(self, index):
		return len(self.get_neighbors(index))


	def get_index(self, label):
		return self.label_to_index[label]

	
	def get_label(self, index):
		return self.index_to_label[index]


	@staticmethod
	def from_file(file_name, pattern, split_by):
		g = Graph()
		with open(file_name, 'r') as input_file:
			pattern_edge = re.compile(pattern)

			for line in input_file:
				line = line.strip()
				if pattern_edge.match(line):
					edge = re.split(split_by, line)
					g.add_undirected_edge(edge)

		return g