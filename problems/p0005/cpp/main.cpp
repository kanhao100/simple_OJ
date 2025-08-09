#include <iostream>
#include <string>
#include <vector>
#include <algorithm>

using namespace std;

bool isLucky(int x) {
    bool seen[10] = {false};
    // 0 本身也算 “各位数字互不相同”
    if (x == 0) return true;
    while (x > 0) {
        int d = x % 10;
        if (seen[d]) return false;
        seen[d] = true;
        x /= 10;
    }
    return true;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    cin >> T;
    while (T--) {
        int n;
        cin >> n;
        int y = n + 1;
        while (!isLucky(y)) {
            ++y;
        }
        cout << y << "\n";
    }
    return 0;
}
