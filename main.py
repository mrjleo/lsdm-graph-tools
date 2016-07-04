#! /usr/bin/python
# -*- coding: utf-8 -*-

from argparse import ArgumentParser
from graph import Graph
from collections import deque
import json
import sys
import time
	

def create_labeled_landmarks(graph, use_pruning):
	verts = graph.get_verts()
	
	# distances: d[v] is a (pruned) table of all distances from/to v
	d = dict.fromkeys(verts)

	# for progess indicator
	total = len(verts)
	current = 0

	# create empty index
	for v in verts:
		d[v] = {}
		d[v][v] = 0

	for v in verts:
		# bfs from v
		visited = dict.fromkeys(verts, False)
		q = deque()

		visited[v] = True
		q.appendleft(v)

		while q:
			next_vert = q.pop()
			dist = d[next_vert][v] + 1
			for neighbor in graph.get_neighbors(next_vert):
				if not visited[neighbor]:
					visited[neighbor] = True
					# pruning happens when there's already a distance and it's shorter
					if not use_pruning or dist < shortest_path(v, neighbor, d)[0]:
						d[neighbor][v] = dist
						q.appendleft(neighbor)
		
		# show progress
		current += 1
		sys.stdout.write('\r{}%\t[{}/{}]'.format(int(100 * current / total), current, total))
		sys.stdout.flush()

	sys.stdout.write('\n')
	return d


def shortest_path(vert1, vert2, d):
	sp = float("inf")
	hop = ''

	for vert in d[vert1]:
		if vert in d[vert2]:
			path = d[vert1][vert] + d[vert2][vert]
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
		ll = create_labeled_landmarks(g, True)
	time_end = time_diff_s(time_start)
	print('created labeled landmarks [{:.2f}s]'.format(time_end))

	# execute all tasks
	if args.sp:
		for sp_req in args.sp:
			sp = shortest_path(sp_req[0], sp_req[1], ll)
			print('shortest path ({}) --> ({}) --> ({}): length {}'.format(sp_req[0], sp[1], sp_req[1], sp[0]))

	if args.save:
		print('exporting labeled landmarks to \'{}\'...'.format(args.save))
		export_json(args.save, ll)


if __name__ == '__main__':
	main()