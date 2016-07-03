#! /usr/bin/python
# -*- coding: utf-8 -*-

from argparse import ArgumentParser
from graph import Graph


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
	print('created graph with {} nodes'.format(len(g.get_verts())))
	print(g.graph)


if __name__ == '__main__':
	main()