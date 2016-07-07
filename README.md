# Overview
Features:
- parse graph from file
- create/export/import (pruned) landmark labels
- calculate shortest paths between vertices
- calculate clustering coefficients of vertices

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
- calculate the shortest path between two vertices `(1) <--> (2)`, creating landmark labels on-the-fly:  
```
./main.py mygraph.txt -sp 1 2
```
- create landmark labels and dump them into a file:
```
./main.py mygraph.txt --saveindex mylabels.json
```
- import the landmark labels from a file and calculate the shortest paths between vertices `(1) <--> (2)` and `(3) <--> (4)`:
```
./main.py mygraph.txt --indexfile mylabels.json -sp 1 2 -sp 3 4
```
- calculate the clustering coefficients of vertices `(1)` and `(2)`, counting triangles on-the-fly:
```
./main.py mygraph.txt -cc 1 -cc 2
```
- count triangles and dump the counts into a file:
```
./main.py mygraph.txt --savetrias mytriangles.json
```
- import the triangle counts from a file and calculate the clustering coefficient of vertex `(1)`:
```
./main.py mygraph.txt --triafile mytriangles.json -cc 1
```
