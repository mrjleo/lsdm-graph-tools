#! /usr/bin/python
# -*- coding: utf-8 -*-

from argparse import ArgumentParser
from graph import Graph
from collections import deque


def bfs(graph, vert_root):
	verts = graph.get_verts()
	dists = dict.fromkeys(verts, 0)
	visited = dict.fromkeys(verts, False)
	q = deque()

	dists[vert_root] = 0
	visited[vert_root] = True
	q.append(vert_root)
	
	while q:
		vert = q.pop()
		for neighbor in graph.get_connected_verts(vert):
			if not visited[neighbor]:
				dists[neighbor] = dists[vert] + 1
				q.append(neighbor)
				visited[neighbor] = True

	return dists
	

def create_ll_naiive(graph):
	verts = graph.get_verts()
	d = dict.fromkeys(verts)

	# create empty index
	for v in verts:
		d[v] = {}

	for vert in verts:
		bfs_dists = bfs(graph, vert)
		# L_{i} -> L_{i+1}
		for bfs_vert in bfs_dists:
			d[bfs_vert][vert] = bfs_dists[bfs_vert]

	return d


def main():
	ap = ArgumentParser()
	ap.add_argument('INPUT_FILE', help='the file that contains the graph')
	ap.add_argument('-p', '--pattern', help='specify a pattern to use when parsing the input file (default: \d+\\t\d+)')
	ap.add_argument('-s', '--split', help='specify a pattern to use when splitting the lines of the input file (default: \\t)')
	args = ap.parse_args()

	print('reading file \'{}\'...'.format(args.INPUT_FILE))
	if args.pattern:
		if args.split:
			g = Graph.from_file(args.INPUT_FILE, pattern=args.pattern, split_by=args.split)
		else:
			g = Graph.from_file(args.INPUT_FILE, pattern=args.pattern)
	elif args.split:
		g = Graph.from_file(args.INPUT_FILE, split_by=args.split)
	else:
		g = Graph.from_file(args.INPUT_FILE)
	print('created graph with {} vertices'.format(len(g.get_verts())))

	print(create_ll_naiive(g))


if __name__ == '__main__':
	main()