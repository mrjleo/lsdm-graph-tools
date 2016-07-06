# Overview
Currently supported:
- parse graph from file
- create/export/import (pruned) landmark labels
- calculate shortest paths between nodes

# Usage
```
usage: main.py [-h] [--pattern PATTERN] [--split PATTERN] [--indexfile FILE]
               [--saveindex FILE] [--noprune] [-sp V1 V2] [--triafile FILE]
               [--savetrias FILE] [-cc V]
               INPUT_FILE

positional arguments:
  INPUT_FILE         the file that contains the graph

optional arguments:
  -h, --help         show this help message and exit
  --pattern PATTERN  specify a pattern to use when parsing the input file
                     (default: \d+\t\d+)
  --split PATTERN    specify a pattern to use when splitting the lines of the
                     input file (default: \t)
  --indexfile FILE   import labeled landmarks from JSON file
  --saveindex FILE   dump the labeled landmarks into a JSON file
  --noprune          use naiive landmark labeling (no pruning)
  -sp V1 V2          calculate the shortest path between vertices V1 and V2
  --triafile FILE    import triangle counts from JSON file
  --savetrias FILE   dump the triangle counts into a JSON file
  -cc V              calculate the clustering coefficient of vertex V
```

# Examples
- calculate the shortest path between two nodes `1 --> 2`, creating landmark labels on-the-fly:  
```
./main.py mygraph.txt -sp 1 2
```
- create landmark labels and dump them into a file:
```
./main.py mygraph.txt --save mylabels.json
```
- import the landmark labels from a file and calculate the shortest paths between nodes `1 --> 2` and `3 --> 4`:
```
./main.py mygraph.txt --fromfile mylabels.json -sp 1 2 -sp 3 4
```
