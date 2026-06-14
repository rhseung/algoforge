import heapq
from math import inf


def dijkstra(graph: list[list[tuple[int, int]]], start: int):
    n = len(graph)
    dist = [inf] * n
    heap = [(0.0, start)]  # (dist, vertex)
    dist[start] = 0

    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        yield u

        for utov, v in graph[u]:
            if dist[v] > dist[u] + utov:
                dist[v] = dist[u] + utov
                heapq.heappush(heap, (dist[v], v))

    return dist
