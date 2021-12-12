import sys
from collections import defaultdict

graph = defaultdict(list)
for line in sys.stdin.readlines():
    a, b = line.strip().split("-")
    graph[a].append(b)
    graph[b].append(a)


def walk(graph, path, source, dest, small_visits_allowed):
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
            graph["paths"].add(path + (opt,))
        else:
            walk(
                graph,
                path + (opt,),
                opt,
                dest,
                1 if opt.islower() and opt in path else small_visits_allowed,
            )


if __name__ == "__main__":
    graph["paths"] = set()
    walk(graph, ("start",), "start", "end", 1)
    print(f"Part 1: {len(graph['paths'])}")

    graph["paths"] = set()
    walk(graph, ("start",), "start", "end", 2)
    print(f"Part 2: {len(graph['paths'])}")
