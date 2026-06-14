import heapq


def prim(graph: list[list[tuple[int, int]]], start: int):
    """
    약간 구현 자체는 bfs 처럼 lazy-guard 형식에 visited를 사용하면서, 다익스트라처럼 heap을 사용한다.
    다만, 프림은 자료구조에 u와 v를 모두 저장한다는 점.
    """

    mst = []
    visited = set[int]()

    # (w, u, v), bfs/dijkstra는 현재 정점 (v)만을 저장하지만 프림은 (u, v) 전부 저장해야하므로 -1이라는 더미 정점을 만들어줌.
    heap = [(0, -1, start)]

    while heap:
        d, u, v = heapq.heappop(heap)
        if v in visited:  # u가 아니라 v임에 주의!!! 상식적으로 u면 -1이 들어갈 수 있어서 안됨
            continue

        visited.add(v)  # 마찬가지로 u가 아니라 v임에 주의!!!
        if u != -1:
            mst.append((d, u, v))

        for w, next_v in graph[v]:  # 마찬가지로 u가 아니라 v임에 주의!!!
            if next_v not in visited:
                heapq.heappush(heap, (w, v, next_v))

    return mst
