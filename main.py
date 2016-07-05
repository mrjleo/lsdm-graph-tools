#! /usr/bin/python
# -*- coding: utf-8 -*-

from argparse import ArgumentParser
from graph import Graph
from collections import deque
import json
import sys
import time
	

def create_labeled_landmarks(graph, naiive):
	verts = graph.get_verts()
	L = dict.fromkeys(verts)
	P = dict.fromkeys(verts)

	# for progess indicator
	total = len(verts)
	current = 0

	# create empty index
	for v in verts:
		L[v] = {}

		# initialize only once for better performance
		P[v] = float('inf')

	for v in verts:
		# bfs from v
		visited = [v]
		Q = deque()
		Q.appendleft(v)
		P[v] = 0
		Lnew = {}

		while Q:
			u = Q.pop()
			# naiive => never prune
			if naiive or shortest_path_query(v, u, L)[0] > P[u]:
				visited.append(u)
				Lnew[u] = P[u]

				for w in graph.get_neighbors(u):
					if P[w] == float('inf'):
						P[w] = P[u] + 1
						Q.appendleft(w)

		# L_{k} <- L_{k-1}
		for u in Lnew:
			L[u][v] = Lnew[u]

		# reset
		for u in visited:
			P[u] = float('inf')
		
		# show progress
		current += 1
		sys.stdout.write('\r{}%\t[{}/{}]'.format(int(100 * current / total), current, total))
		sys.stdout.flush()

	sys.stdout.write('\n')
	return L


def shortest_path_query(vert1, vert2, L):
	sp = float('inf')
	hop = ''

	for vert in L[vert1]:
		if vert in L[vert2]:
			path = L[vert1][vert] + L[vert2][vert]
			if path < sp:
				sp = path
				hop = vert

	return [sp, hop];


def export_json(file_name, content):
	with open(file_name, 'w') as f:
		json.dump(content, f)


def import_json(file_name):
	with open(file_name, 'r') as f:    
		content = json.load(f)

	return content


def time_diff_s(time_from):
	return (time.time() - time_from) / 1000


def main():
	ap = ArgumentParser()
	ap.add_argument('INPUT_FILE', help='the file that contains the graph')
	ap.add_argument('--pattern', metavar='PATTERN', default='\d+\\t\d+', help='specify a pattern to use when parsing the input file (default: \d+\\t\d+)')
	ap.add_argument('--split', metavar='PATTERN', default='\\t', help='specify a pattern to use when splitting the lines of the input file (default: \\t)')
	ap.add_argument('--fromfile', metavar='FILE', help='import labeled landmarks from JSON file')
	ap.add_argument('--save', metavar='FILE', help='dump the labeled landmarks into a JSON file')
	ap.add_argument('--naiive', action='store_true', help='use naiive landmark labeling (no pruning)')
	ap.add_argument('-sp', nargs=2, metavar=('V1', 'V2'), action='append', help='calculate the shortest path between V1 and V2')
	args = ap.parse_args()

	# create graph
	print('reading file \'{}\'...'.format(args.INPUT_FILE))
	time_start = time.time()
	g = Graph.from_file(args.INPUT_FILE, args.pattern, args.split)
	time_end = time_diff_s(time_start)
	print('created graph with {} vertices [{:.2f}s]'.format(len(g.get_verts()), time_end))

	# create labeled landmarks
	time_start = time.time()
	if args.fromfile:
		print('importing labeled landmarks from \'{}\'...'.format(args.fromfile))
		ll = import_json(args.fromfile)
	else:
		print('creating labeled landmarks...')
		ll = create_labeled_landmarks(g, args.naiive)
	time_end = time_diff_s(time_start)
	print('created labeled landmarks [{:.2f}s]'.format(time_end))

	# execute all tasks
	if args.sp:
		for sp_req in args.sp:
			sp = shortest_path_query(sp_req[0], sp_req[1], ll)
			print('shortest path ({}) --> ({}) --> ({}): length {}'.format(sp_req[0], sp[1], sp_req[1], sp[0]))

	if args.save:
		print('exporting labeled landmarks to \'{}\'...'.format(args.save))
		export_json(args.save, ll)


if __name__ == '__main__':
	main()