#include <bits/stdc++.h>
using namespace std;

int minOperationsToStrictlyIncrease(vector<int> arr1, vector<int> arr2) {
    sort(arr2.begin(), arr2.end());
    arr2.erase(unique(arr2.begin(), arr2.end()), arr2.end());

    unordered_map<int, int> dp;
    dp[-1] = 0; // 哨兵：所有值均 >= 0，-1 一定小于任何元素

    for (int value : arr1) {
        unordered_map<int, int> nextDp;

        auto relax = [&](int lastValue, int ops) {
            auto it = nextDp.find(lastValue);
            if (it == nextDp.end() || ops < it->second) nextDp[lastValue] = ops;
        };

        for (const auto &kv : dp) {
            int last = kv.first;
            int ops = kv.second;

            // 1) 不替换
            if (value > last) {
                relax(value, ops);
            }

            // 2) 用 arr2 中第一个 > last 的值替换
            auto it = upper_bound(arr2.begin(), arr2.end(), last);
            if (it != arr2.end()) {
                relax(*it, ops + 1);
            }
        }

        if (nextDp.empty()) return -1; // 无法继续形成严格递增
        dp.swap(nextDp);
    }

    int ans = INT_MAX;
    for (const auto &kv : dp) ans = min(ans, kv.second);
    return ans == INT_MAX ? -1 : ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    while (cin >> n) {
        vector<int> arr1(n);
        for (int i = 0; i < n; ++i) cin >> arr1[i];

        int m;
        if (!(cin >> m)) break;
        vector<int> arr2(m);
        for (int i = 0; i < m; ++i) cin >> arr2[i];

        cout << minOperationsToStrictlyIncrease(arr1, arr2) << '\n';
    }
    return 0;
}