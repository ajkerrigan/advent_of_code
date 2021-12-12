import sys

from collections import defaultdict

graph = defaultdict(list)
for line in sys.stdin.readlines():
    a, b = line.strip().split("-")
    graph[a].append(b)
    graph[b].append(a)

paths = set()


def walk(graph, path, source, dest, small_visited_twice):
    small_visits_allowed = 2 if not small_visited_twice else 1
    options = [
        node
        for node in graph[source]
        if not (
            node == "start"
            or (node.islower() and path.count(node) >= small_visits_allowed)
        )
    ]
    for opt in options:
        if opt == dest:
            paths.add(path + (opt,))
        else:
            walk(
                graph,
                path + (opt,),
                opt,
                dest,
                small_visited_twice or (opt.islower() and opt in path),
            )


walk(graph, ("start",), "start", "end", False)
print("\n".join(str(p) for p in paths))
print(len(paths))
