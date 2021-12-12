import sys

from collections import defaultdict

graph = defaultdict(list)
for line in sys.stdin.readlines():
    a, b = line.strip().split("-")
    graph[a].append(b)
    graph[b].append(a)

paths = set()


def walk(graph, path, source, dest):
    options = [
        node
        for node in graph[source]
        if not (node == "start" or (node.islower() and node in path))
    ]
    for opt in options:
        if opt == dest:
            paths.add(path + (opt,))
        else:
            walk(graph, path + (opt,), opt, dest)


walk(graph, ("start",), "start", "end")
print("\n".join(str(p) for p in paths))
print(len(paths))
