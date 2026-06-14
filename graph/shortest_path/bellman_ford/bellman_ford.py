from math import inf


def bellman_ford(v_cnt: int, edges: list[tuple[int, int, int]], start: int):
    dist = [inf] * v_cnt
    dist[start] = 0

    for _ in range(v_cnt - 1):
        for u, v, w in edges:
            dist[v] = min(dist[v], dist[u] + w)

    has_negative_cycle = any(dist[v] > dist[u] + w for u, v, w in edges)

    return dist, has_negative_cycle
