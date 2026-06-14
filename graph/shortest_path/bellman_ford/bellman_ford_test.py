"""bellman_ford 테스트 — 엣지 리스트 기반, ``(dist, 음수사이클여부)`` 반환.

음수 가중치를 허용하고, **start 에서 도달 가능한** 음수 사이클을 검출한다
(도달 불가 사이클은 검출 대상이 아니다). 간선은 ``(u, v, w)`` = (출발, 도착, 가중치).
"""

from math import inf

from graph.shortest_path.bellman_ford.bellman_ford import bellman_ford


# 0→1 직통(4)보다 0→2→1 우회(3)가 짧다. 4 번은 도달 불가. (dijkstra 테스트와 같은 그래프)
#   edges = (u, v, w)
WEIGHTED = [(0, 1, 4), (0, 2, 1), (1, 3, 1), (2, 1, 2), (2, 3, 5)]


class TestBasic:
    def test_single_node(self):
        dist, neg = bellman_ford(1, [], 0)

        assert dist == [0]
        assert neg is False

    def test_shortest_distances(self):
        dist, neg = bellman_ford(5, WEIGHTED, 0)

        assert dist == [0, 3, 1, 4, inf]
        assert neg is False

    def test_unreachable_node_stays_inf(self):
        dist, _ = bellman_ford(3, [(0, 1, 2)], 0)

        assert dist == [0, 2, inf]

    def test_isolated_graph_no_edges(self):
        dist, neg = bellman_ford(3, [], 0)

        assert dist == [0, inf, inf]
        assert neg is False

    def test_start_from_nonzero(self):
        dist, neg = bellman_ford(5, WEIGHTED, 2)

        assert dist == [inf, 2, 0, 3, inf]
        assert neg is False


class TestMultiPassPropagation:
    def test_relaxes_across_passes_with_adversarial_edge_order(self):
        # 체인 0→1→2→3 이지만 간선이 역순으로 나열됨 → 한 패스로는 부족, n-1 패스 필요
        dist, neg = bellman_ford(4, [(2, 3, 1), (1, 2, 1), (0, 1, 1)], 0)

        assert dist == [0, 1, 2, 3]
        assert neg is False


class TestNegativeWeights:
    def test_negative_edge_without_cycle(self):
        # 0→1(4), 0→2(5), 1→2(-3) → 0→1→2 = 1 이 0→2 = 5 보다 짧다
        dist, neg = bellman_ford(3, [(0, 1, 4), (0, 2, 5), (1, 2, -3)], 0)

        assert dist == [0, 4, 1]
        assert neg is False


class TestNegativeCycle:
    def test_two_node_negative_cycle(self):
        # 0→1(1), 1→0(-2) → 사이클 가중치 -1
        _, neg = bellman_ford(2, [(0, 1, 1), (1, 0, -2)], 0)

        assert neg is True

    def test_negative_self_loop_is_a_cycle(self):
        # 0→0(-1) 자기 간선은 음수 사이클
        _, neg = bellman_ford(1, [(0, 0, -1)], 0)

        assert neg is True

    def test_positive_self_loop_is_not_a_cycle(self):
        _, neg = bellman_ford(1, [(0, 0, 5)], 0)

        assert neg is False

    def test_unreachable_negative_cycle_not_detected(self):
        # 2↔3 음수 사이클은 start(0) 에서 도달 불가 → 검출되지 않는다 (의도된 동작)
        dist, neg = bellman_ford(4, [(0, 1, 1), (2, 3, -1), (3, 2, -1)], 0)

        assert dist[0] == 0
        assert dist[1] == 1
        assert dist[2] == inf
        assert dist[3] == inf
        assert neg is False
