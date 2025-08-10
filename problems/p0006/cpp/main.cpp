#include <iostream>
#include <string>
#include <vector>
#include <algorithm>

using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    if (!(cin >> T)) return 0;
    while (T--) {
        int n;
        long long m;
        cin >> n >> m;
        vector<int> a(n + 1), pos(n + 1);
        for (int i = 1; i <= n; ++i) {
            cin >> a[i];
            pos[a[i]] = i;
        }

        for (int i = 1; i <= n && m > 0; ++i) {
            if (a[i] == i) continue;
            int j = pos[i];           // 位置 j 上是值 i
            int v = a[i];             // 当前位置的值
            swap(a[i], a[j]);         // 把 i 放到 i 位
            pos[i] = i;
            pos[v] = j;
            --m;
        }

        for (int i = 1; i <= n; ++i) {
            if (i > 1) cout << ' ';
            cout << a[i];
        }
        cout << '\n';
    }
    return 0;
}
