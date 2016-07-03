#! /usr/bin/python
# -*- coding: utf-8 -*-

import re


class Graph(object):
	def __init__(self):
		self.graph = {}


	def add_vert(self, vert):
		if not vert in self.graph:
			self.graph[vert] = []


	def add_undirected_edge(self, edge):
		# add 2 directed edges to simulate undirected edge
		self.add_directed_edge(edge)
		self.add_directed_edge(edge[::-1])


	# edge = [v_from, v_to]
	def add_directed_edge(self, edge):
		v_from = edge[0]
		v_to = edge[1]

		self.add_vert(v_from)
		self.add_vert(v_to)

		if not v_to in self.graph[v_from]:
			self.graph[v_from].append(v_to)
	

	def get_verts(self):
		return self.graph.keys()


	def get_connected_verts(self, vert):
		return self.graph[vert]


	def is_vert(self, vert):
		return vert in self.graph


	def is_edge(self, edge):
		v_from = edge[0]
		v_to = edge[1]

		return is_vert(v_from) and v_to in get_connected_verts(v_from)


	@staticmethod
	def from_file(file_name, pattern='\d+\t\d+', split_by='\t'):
		g = Graph()
		input_file = open(file_name, 'r')
		pattern_edge = re.compile(pattern)

		for line in input_file:
			line = line.strip()
			if pattern_edge.match(line):
				edge = re.split(split_by, line)
				g.add_undirected_edge(edge)

		return g