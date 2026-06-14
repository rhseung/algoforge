"""union_find 테스트 — naive(find_naive/union_naive)와 최적화 기본(find/union) 양쪽.

기본 ``find``/``union`` 은 경로 압축 + union by rank 가 적용된 버전이고, ``*_naive`` 는
미적용 버전이다. 최적화가 *어떻게* 동작하는지 내부 상태(parent·rank)를 직접 단언하는
화이트박스 테스트로 검증한다 (rank 최적화는 연결성만 봐선 안 잡힘).

``UnionFind(n)`` 은 ``parent = list(range(n))`` 이라 정점 0..n-1 을 다룬다(0-indexed).
"""

from sets.union_find.union_find import UnionFind


class TestInit:
    def test_each_node_is_its_own_parent(self):
        uf = UnionFind(3)

        assert uf.parent == [0, 1, 2]
        assert uf.rank == [0, 0, 0]


class TestFindNaive:
    def test_root_returns_itself(self):
        uf = UnionFind(2)

        assert uf.find_naive(0) == 0

    def test_non_root_follows_chain_to_root(self):
        uf = UnionFind(2)
        uf.union_naive(0, 1)  # parent[0] = 1

        assert uf.find_naive(0) == 1

    def test_naive_find_does_not_compress(self):
        # naive find 는 경로를 그대로 둔다 (압축 없음)
        uf = UnionFind(3)
        uf.union_naive(0, 1)  # 0 → 1
        uf.union_naive(1, 2)  # 1 → 2  (사슬 0 → 1 → 2)

        assert uf.find_naive(0) == 2
        assert uf.parent[0] == 1  # 여전히 1 을 가리킴 (압축 안 됨)


class TestUnionNaive:
    def test_union_merges_and_returns_true(self):
        uf = UnionFind(2)

        assert uf.union_naive(0, 1) is True
        assert uf.find_naive(0) == uf.find_naive(1)

    def test_union_already_connected_returns_false(self):
        uf = UnionFind(3)
        uf.union_naive(0, 1)

        assert uf.union_naive(0, 1) is False

    def test_attaches_rx_under_ry(self):
        uf = UnionFind(2)
        uf.union_naive(0, 1)  # 주석대로 ry(1) 아래에 rx(0)

        assert uf.parent[0] == 1


class TestFindCompression:
    def test_root_returns_itself(self):
        uf = UnionFind(2)

        assert uf.find(0) == 0

    def test_flattens_chain_to_root(self):
        # 0 → 1 → 2 사슬을 만든 뒤 find 로 전부 루트(2)에 직결
        uf = UnionFind(3)
        uf.union_naive(0, 1)
        uf.union_naive(1, 2)

        assert uf.find(0) == 2
        assert uf.parent[0] == 2  # 압축됨
        assert uf.parent[1] == 2  # 중간 노드도 압축됨


class TestUnionByRank:
    def test_equal_rank_increments_root_rank(self):
        uf = UnionFind(2)

        assert uf.union(0, 1) is True
        # rank 동률 → parent[0]=1, rank[1] 증가
        assert uf.parent[0] == 1
        assert uf.rank[1] == 1

    def test_lower_rank_attaches_under_higher_no_swap(self):
        # {0,1}(루트 1, rank1) 에 단일 노드 2(rank0)를 붙임 → rank[rx] < rank[ry], swap 없음
        uf = UnionFind(3)
        uf.union(0, 1)  # rank[1] = 1
        uf.union(2, 1)  # rx=2(rank0), ry=1(rank1)

        assert uf.parent[2] == 1
        assert uf.rank[1] == 1  # 높이 안 늘어남

    def test_higher_rank_root_kept_with_swap(self):
        # rx 가 더 높은 rank 인 경우 → swap 후 낮은 쪽을 높은 쪽 아래에
        uf = UnionFind(4)
        uf.union(0, 1)  # rank[1] = 1, 루트 1
        uf.union(1, 3)  # rx=1(rank1), ry=3(rank0) → swap → parent[3]=1

        assert uf.parent[3] == 1
        assert uf.rank[1] == 1  # 큰 트리 rank 유지

    def test_union_already_connected_returns_false(self):
        uf = UnionFind(3)
        uf.union(0, 1)

        assert uf.union(0, 1) is False

    def test_rank_grows_only_on_equal_rank_merges(self):
        # 동률 트리끼리 합칠 때만 높이 1 증가: {0,1}(rank1) + {2,3}(rank1) → rank2
        uf = UnionFind(4)
        uf.union(0, 1)  # rank 1
        uf.union(2, 3)  # rank 1
        root_before = uf.find(2)
        uf.union(0, 2)  # 두 rank1 트리 병합 → 루트 rank 2

        assert uf.rank[root_before] == 2
        assert uf.connected(0, 3) is True


class TestConnected:
    def test_not_connected_initially(self):
        uf = UnionFind(3)

        assert uf.connected(0, 1) is False

    def test_connected_after_union(self):
        uf = UnionFind(3)
        uf.union(0, 1)

        assert uf.connected(0, 1) is True
        assert uf.connected(0, 2) is False


class TestIntegration:
    def test_component_merging_and_queries(self):
        uf = UnionFind(6)  # 정점 0..5
        uf.union(0, 1)
        uf.union(2, 3)
        uf.union(1, 2)  # {0,1,2,3}

        assert uf.connected(0, 3) is True
        assert uf.connected(0, 4) is False
        assert uf.connected(4, 5) is False

        uf.union(4, 5)  # {4,5}

        assert uf.connected(4, 5) is True
        assert uf.connected(3, 5) is False
