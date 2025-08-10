#include <bits/stdc++.h>
using namespace std;

static inline int lsb_index(uint64_t x) { return __builtin_ctzll(x); }
static inline int popcnt(uint64_t x) { return __builtin_popcountll(x); }

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    while (cin >> n >> m) {
        vector<string> g(n);
        for (int i = 0; i < n; ++i) cin >> g[i];

        vector<pair<int,int>> specials;
        for (int i = 0; i < n; ++i)
            for (int j = 0; j < m; ++j)
                if (g[i][j] == '*') specials.push_back({i,j});

        auto inb = [&](int r, int c) { return r >= 0 && r < n && c >= 0 && c < m; };
        auto id = [&](int r, int c) { return r * m + c; };

        // 枚举所有合法摆放（至少一端在特殊格子上），用掩码去重
        unordered_set<uint64_t> seenMask;
        vector<uint64_t> cellMasks;
        const int dr[4] = {-1, 1, 0, 0};
        const int dc[4] = {0, 0, -1, 1};

        for (auto [r, c] : specials) {
            for (int k = 0; k < 4; ++k) {
                int r1 = r + dr[k], c1 = c + dc[k];
                int r2 = r + 2*dr[k], c2 = c + 2*dc[k];
                if (!inb(r1,c1) || !inb(r2,c2)) continue;
                uint64_t mask = 0;
                mask |= (1ULL << id(r,c));
                mask |= (1ULL << id(r1,c1));
                mask |= (1ULL << id(r2,c2));
                if (seenMask.insert(mask).second) cellMasks.push_back(mask);
            }
        }

        int V = (int)cellMasks.size();
        // 若没有任何可摆放，空局面本身就是极大，答案为 1
        if (V == 0) {
            cout << 1 << "\n";
            continue;
        }

        // 构建冲突图邻接（重叠即相邻）
        vector<uint64_t> adj(V, 0);
        for (int i = 0; i < V; ++i) {
            for (int j = i + 1; j < V; ++j) {
                if (cellMasks[i] & cellMasks[j]) {
                    adj[i] |= (1ULL << j);
                    adj[j] |= (1ULL << i);
                }
            }
        }

        // 补图邻接（用于枚举极大团 => 原图的极大独立集）
        uint64_t ALL = (V == 64) ? ~0ULL : ((1ULL << V) - 1);
        vector<uint64_t> nadj(V, 0);
        for (int i = 0; i < V; ++i) {
            nadj[i] = (ALL & ~adj[i]) & ~(1ULL << i);
        }

        // Bron–Kerbosch 算法计数（去重覆盖）
        unordered_set<uint64_t> coverSet;
        coverSet.reserve(1u << min(V, 20)); // 预留一些空间

        function<void(uint64_t,uint64_t,uint64_t,uint64_t)> BK =
        [&](uint64_t R, uint64_t P, uint64_t X, uint64_t cover) {
            if (P == 0 && X == 0) {
                coverSet.insert(cover);
                return;
            }
            // 选支点：使得 |P ∩ N(u)| 最大
            uint64_t UX = P | X;
            int pivot = -1, best = -1;
            if (UX) {
                uint64_t t = UX;
                while (t) {
                    int u = lsb_index(t);
                    t &= t - 1;
                    int cnt = popcnt(P & nadj[u]);
                    if (cnt > best) { best = cnt; pivot = u; }
                }
            }
            uint64_t candidates = (pivot == -1) ? P : (P & ~nadj[pivot]);
            uint64_t c = candidates;
            while (c) {
                int v = lsb_index(c);
                c &= c - 1;
                uint64_t vb = 1ULL << v;
                BK(R | vb, P & nadj[v], X & nadj[v], cover | cellMasks[v]);
                P &= ~vb;
                X |= vb;
            }
        };

        BK(0, ALL, 0, 0);
        cout << (unsigned long long)coverSet.size() << "\n";
    }
    return 0;
}
