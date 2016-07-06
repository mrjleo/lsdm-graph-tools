#! /usr/bin/python
# -*- coding: utf-8 -*-

import re


class Graph(object):
	def __init__(self):
		self.graph = {}
		self.u_edge_count = 0


	def add_vert(self, vert):
		if not self.is_vert(vert):
			self.graph[vert] = set()


	def add_undirected_edge(self, edge):
		# add 2 directed edges to simulate undirected edge
		if self.add_directed_edge(edge) and self.add_directed_edge(edge[::-1]):
			self.u_edge_count += 1


	# edge = [v_from, v_to]
	def add_directed_edge(self, edge):
		v_from = edge[0]
		v_to = edge[1]

		self.add_vert(v_from)
		self.add_vert(v_to)

		if not v_to in self.graph[v_from]:
			self.graph[v_from].add(v_to)
			return True
		return False


	def get_verts(self):
		return self.graph.keys()


	def get_neighbors(self, vert):
		return self.graph[vert]


	def is_vert(self, vert):
		return vert in self.graph


	def is_directed_edge(self, edge):
		v_from = edge[0]
		v_to = edge[1]

		return self.is_vert(v_from) and v_to in self.get_neighbors(v_from)


	def is_undirected_edge(self, edge):
		return self.is_directed_edge(edge) and self.is_directed_edge(edge[::-1])

	
	def degree(self, vert):
		return len(self.get_neighbors(vert))


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