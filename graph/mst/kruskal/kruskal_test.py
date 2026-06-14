"""kruskal 테스트 — 가중치 오름차순으로 간선을 보며 Union-Find 로 사이클을 피해 MST 구성.

간선은 weight-first ``(w, u, v)``. 정점은 ``UnionFind(v_cnt)`` 가 0-indexed 라 0..v_cnt-1.
비연결 그래프면 최소 신장 *숲* 을 반환한다.
"""

from graph.mst.kruskal.kruskal import kruskal


def _weight(mst: list[tuple[int, int, int]]) -> int:
    return sum(w for w, _, _ in mst)


# 0,1,2,3 그래프. MST 는 (1,0,1)+(2,1,3)+(3,1,2)=6, (4,0,2)·(5,2,3) 은 사이클로 제외.
WEIGHTED = [(1, 0, 1), (4, 0, 2), (3, 1, 2), (2, 1, 3), (5, 2, 3)]


class TestBasic:
    def test_builds_minimum_spanning_tree(self):
        mst = kruskal(4, WEIGHTED)

        assert mst == [(1, 0, 1), (2, 1, 3), (3, 1, 2)]

    def test_total_weight_is_minimal(self):
        assert _weight(kruskal(4, WEIGHTED)) == 6

    def test_has_v_minus_one_edges_when_connected(self):
        assert len(kruskal(4, WEIGHTED)) == 3

    def test_edges_emitted_in_weight_order(self):
        mst = kruskal(4, WEIGHTED)
        weights = [w for w, _, _ in mst]

        assert weights == sorted(weights)


class TestSorting:
    def test_result_independent_of_input_order(self):
        # 간선을 거꾸로 넣어도 동일한 MST (내부에서 가중치 정렬하므로)
        assert kruskal(4, list(reversed(WEIGHTED))) == [(1, 0, 1), (2, 1, 3), (3, 1, 2)]


class TestCycleSkip:
    def test_skips_edge_that_would_form_cycle(self):
        # (2,0,1) 은 0,1 이 이미 연결된 뒤라 사이클 → 제외.
        # MST 완성(조기 break) *전에* 평가되도록 배치해 skip 분기를 탄다.
        mst = kruskal(4, [(1, 0, 1), (2, 0, 1), (3, 1, 2), (4, 2, 3)])

        assert mst == [(1, 0, 1), (3, 1, 2), (4, 2, 3)]

    def test_parallel_edges_keeps_cheaper(self):
        # 0-1 사이 평행 간선 두 개 → 싼 것만 채택
        mst = kruskal(2, [(5, 0, 1), (1, 0, 1)])

        assert mst == [(1, 0, 1)]


class TestDisconnected:
    def test_returns_spanning_forest(self):
        # {0,1} 과 {2,3} 가 분리 → 간선 2개짜리 숲 (v_cnt-1=3 보다 적음)
        mst = kruskal(4, [(1, 0, 1), (2, 2, 3)])

        assert mst == [(1, 0, 1), (2, 2, 3)]
        assert len(mst) == 2


class TestEdgeCases:
    def test_single_vertex_no_edges(self):
        assert kruskal(1, []) == []

    def test_no_edges_returns_empty(self):
        assert kruskal(3, []) == []
