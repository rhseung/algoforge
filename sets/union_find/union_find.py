class UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find_naive(self, x: int):
        if self.parent[x] != x:
            return self.find_naive(self.parent[x])
        return self.parent[x]

    def union_naive(self, x: int, y: int):
        rx = self.find_naive(x)
        ry = self.find_naive(y)

        if rx == ry:
            return False

        # ry 아래에 rx를 넣음
        self.parent[rx] = ry
        return True

    def find(self, x: int):
        """path compression"""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int):
        """union by rank"""
        rx = self.find(x)
        ry = self.find(y)

        if rx == ry:
            return False

        # 트리의 높이가 동일하면 아무 곳으로 붙이고 높이 늘리기
        if self.rank[rx] == self.rank[ry]:
            # ry 아래에 rx를 넣음
            self.parent[rx] = ry
            self.rank[ry] += 1
            return True

        # rx가 항상 더 높이가 낮은 트리가 되도록
        if self.rank[rx] > self.rank[ry]:
            rx, ry = ry, rx

        # 높은 트리(ry) 아래에 높이가 낮은 트리(rx)를 다는 것이 더 높이가 균형적임
        self.parent[rx] = ry
        return True

    def connected(self, x: int, y: int):
        rx = self.find(x)
        ry = self.find(y)

        return rx == ry
