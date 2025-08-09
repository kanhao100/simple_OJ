#include <iostream>
#include <string>
#include <vector>
#include <algorithm>

using namespace std;


int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    cin >> T;
    while (T--) {
        int n;
        string s;
        cin >> n >> s;

        // 长度不是 3 的倍数，必然不行
        if (n % 3 != 0) {
            cout << "No\n";
            continue;
        }

        // 转小写，方便比较
        for (char &c : s) {
            c = tolower(c);
        }

        bool ok = true;
        // 每 3 个字符一段，判断是不是 "yes" 或 "sey"
        for (int i = 0; i < n; i += 3) {
            // 直接用下标比较比 substr 效率更高一点
            if (!((s[i] == 'y' && s[i+1] == 'e' && s[i+2] == 's') ||
                  (s[i] == 's' && s[i+1] == 'e' && s[i+2] == 'y'))) {
                ok = false;
                break;
            }
        }

        cout << (ok ? "Yes\n" : "No\n");
    }
    return 0;
}

