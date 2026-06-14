from sets.union_find.union_find import UnionFind


def kruskal(v_cnt: int, edges: list[tuple[int, int, int]]) -> list[tuple[int, int, int]]:
    uf = UnionFind(v_cnt)
    mst = []

    # weight를 기준으로 정렬하는 것이 중요하다. (u, v, weight)면 key=lambda e: e[2]로.
    for w, u, v in sorted(edges, key=lambda e: e[0]):
        if uf.union(u, v):
            mst.append((w, u, v))
            # 아래 코드는 사실 필요 없으나 교과서에서 많이 나와서
            if len(mst) == v_cnt - 1:
                break

    return mst
