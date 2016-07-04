#! /usr/bin/python
# -*- coding: utf-8 -*-

from argparse import ArgumentParser
from graph import Graph
from collections import deque


def bfs(graph, vert_root, use_pruning, landmarks):
	verts = graph.get_verts()
	dists = {}
	visited = dict.fromkeys(verts, False)
	q = deque()

	dists[vert_root] = 0
	visited[vert_root] = True
	q.append(vert_root)

	while q:
		vert = q.pop()
		dist = dists[vert] + 1
		for neighbor in graph.get_connected_verts(vert):
			if not visited[neighbor]:
				visited[neighbor] = True
				# pruning happens when there's already a distance and it's shorter
				if not use_pruning or dist < shortest_path(vert_root, neighbor, landmarks)[0]:
					dists[neighbor] = dist
					q.appendleft(neighbor)

	return dists
	

def create_labeled_landmarks(graph, use_pruning):
	verts = graph.get_verts()
	d = dict.fromkeys(verts)

	# create empty index
	for v in verts:
		d[v] = {}

	for vert in verts:
		bfs_dists = bfs(graph, vert, use_pruning, d)
		# L_{i} -> L_{i+1}
		for bfs_vert in bfs_dists:
			d[bfs_vert][vert] = bfs_dists[bfs_vert]

	return d


def shortest_path(vert1, vert2, d):
	sp = float("inf")
	hop = '(none)'

	for vert in d[vert1]:
		if vert in d[vert2]:
			path = d[vert1][vert] + d[vert2][vert]
			if path < sp:
				sp = path
				hop = vert

	return [sp, hop];


def main():
	ap = ArgumentParser()
	ap.add_argument('INPUT_FILE', help='the file that contains the graph')
	ap.add_argument('--pattern', default='\d+\\t\d+', help='specify a pattern to use when parsing the input file (default: \d+\\t\d+)')
	ap.add_argument('--split', default='\\t', help='specify a pattern to use when splitting the lines of the input file (default: \\t)')
	args = ap.parse_args()

	print('reading file \'{}\'...'.format(args.INPUT_FILE))
	g = Graph.from_file(args.INPUT_FILE, args.pattern, args.split)
	print('created graph with {} vertices'.format(len(g.get_verts())))
	print('creating landmark labels...')
	ll = create_labeled_landmarks(g, True)


if __name__ == '__main__':
	main()