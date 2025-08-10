#include <iostream>
#include <vector>
#include <queue>
#include <utility>
#include <functional>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    while (cin >> n) {
        vector<int> adoptionNumber(n), firstColor(n), secondColor(n);
        for (int i = 0; i < n; ++i) cin >> adoptionNumber[i];
        for (int i = 0; i < n; ++i) cin >> firstColor[i];
        for (int i = 0; i < n; ++i) cin >> secondColor[i];

        priority_queue<pair<int,int>, vector<pair<int,int>>, greater<pair<int,int>>> heapByColor[4];
        for (int i = 0; i < n; ++i) {
            int x = adoptionNumber[i];
            int a = firstColor[i], b = secondColor[i];
            heapByColor[a].push({x, i});
            if (b != a) heapByColor[b].push({x, i});
        }

        int m;
        if (!(cin >> m)) break;
        vector<int> preferredColors(m);
        for (int i = 0; i < m; ++i) cin >> preferredColors[i];

        vector<char> isAvailable(n, 1);
        vector<int> answer(m, -1);

        for (int i = 0; i < m; ++i) {
            int c = preferredColors[i];
            auto &pq = heapByColor[c];
            while (!pq.empty() && !isAvailable[pq.top().second]) pq.pop();
            if (!pq.empty()) {
                auto top = pq.top(); pq.pop();
                answer[i] = top.first;
                isAvailable[top.second] = 0;
            } else {
                answer[i] = -1;
            }
        }

        for (int i = 0; i < m; ++i) {
            if (i) cout << ' ';
            cout << answer[i];
        }
        cout << '\n';
    }
    return 0;
}