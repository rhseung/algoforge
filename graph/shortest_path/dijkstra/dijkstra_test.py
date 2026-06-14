"""dijkstra 테스트 — 방문 순서를 yield 하고, 소진 후 최단거리 배열을 return.

``return dist`` 는 제너레이터 반환값이라 ``list(gen)`` 으로는 못 받는다.
``StopIteration.value`` 로 꺼내야 하므로 _run 헬퍼가 (방문순서, dist) 를 함께 capture 한다.

간선 표기는 구현의 ``for utov, v in graph[u]`` 순서를 따라 ``(weight, neighbor)`` 다.
"""

import types
from math import inf

from graph.shortest_path.dijkstra.dijkstra import dijkstra


def _run(graph: list[list[tuple[int, int]]], start: int) -> tuple[list[int], list[float]]:
    """제너레이터를 소진해 (방문 순서, 최단거리 배열) 을 반환."""
    gen = dijkstra(graph, start)
    order: list[int] = []
    try:
        while True:
            order.append(next(gen))
    except StopIteration as stop:
        return order, stop.value


# (weight, neighbor) — 0→1 직통(4)보다 0→2→1 우회(3)가 더 짧다.
#
#         (4)
#    0 ─────────▶ 1 ──(1)──▶ 3
#    │            ▲          ▲
#   (1)          (2)        (5)
#    ▼            │          │
#    2 ───────────┴──────────┘
#  4: 도달 불가
WEIGHTED = [
    [(4, 1), (1, 2)],
    [(1, 3)],
    [(2, 1), (5, 3)],
    [],
    [],
]


class TestBasic:
    def test_single_node(self):
        order, dist = _run([[]], 0)

        assert order == [0]
        assert dist == [0]

    def test_start_is_first(self):
        order, _ = _run(WEIGHTED, 0)

        assert order[0] == 0

    def test_visits_all_reachable_nodes(self):
        order, _ = _run(WEIGHTED, 0)

        assert set(order) == {0, 1, 2, 3}

    def test_each_node_visited_exactly_once(self):
        order, _ = _run(WEIGHTED, 0)

        assert len(order) == len(set(order))

    def test_unreachable_node_not_visited(self):
        order, dist = _run(WEIGHTED, 0)

        assert 4 not in order
        assert dist[4] == inf

    def test_start_from_nonzero(self):
        # 1 에서 시작하면 1, 3 만 도달
        order, dist = _run(WEIGHTED, 1)

        assert order == [1, 3]
        assert dist[1] == 0
        assert dist[3] == 1
        assert dist[0] == inf


class TestShortestDistance:
    def test_computes_shortest_distances(self):
        _, dist = _run(WEIGHTED, 0)

        assert dist == [0, 3, 1, 4, inf]

    def test_prefers_cheaper_detour_over_direct_edge(self):
        # 0→1 직통 10, 0→2→1 우회 3 → dist[1] 은 우회로 확정
        graph = [[(10, 1), (1, 2)], [], [(2, 1)]]
        order, dist = _run(graph, 0)

        assert dist[1] == 3
        assert order == [0, 2, 1]

    def test_yields_in_nondecreasing_distance_order(self):
        # 다익스트라는 거리 오름차순으로 정점을 확정한다
        order, dist = _run(WEIGHTED, 0)

        assert [dist[v] for v in order] == sorted(dist[v] for v in order)


class TestStaleHeapGuard:
    """힙에 남은 낡은(거리가 큰) 엔트리는 pop 시 건너뛴다 (``if d > dist[u]``)."""

    def test_no_revisit_when_better_path_found_later(self):
        # 1 은 (4,1) 로 먼저, (3,1) 로 나중에 push → 낡은 (4,1) 은 스킵돼 재방문 없음
        order, _ = _run(WEIGHTED, 0)

        assert order.count(1) == 1
        assert order == [0, 2, 1, 3]


class TestSelfLoopAndCycle:
    def test_self_loop_ignored(self):
        # 0→0 (5): 거리를 개선하지 못해 완화 분기가 false
        order, dist = _run([[(5, 0)]], 0)

        assert order == [0]
        assert dist == [0]

    def test_cycle_terminates(self):
        # 0→1→2→0 — 무한 루프 없이 각 정점 1회
        order, dist = _run([[(1, 1)], [(1, 2)], [(1, 0)]], 0)

        assert order == [0, 1, 2]
        assert dist == [0, 1, 2]


class TestZeroWeight:
    def test_zero_weight_edges(self):
        order, dist = _run([[(0, 1)], [(0, 2)], []], 0)

        assert order == [0, 1, 2]
        assert dist == [0, 0, 0]


class TestLazy:
    def test_returns_lazy_generator(self):
        gen = dijkstra(WEIGHTED, 0)

        assert isinstance(gen, types.GeneratorType)
        assert next(gen) == 0
