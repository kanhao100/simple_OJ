#include <iostream>
#include <string>

using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string s, t;
    // 读入 s、t（可能包含空格）
    if (!getline(cin, s)) return 0;
    getline(cin, t);

    int m = (int)t.size();
    int half = m / 2;
    // t 的前半部分
    string first = t.substr(0, half);
    // t 的后半部分
    string second = t.substr(half);

    // 输出：s 拼接 后半部分
    cout << s << second << "\n";
    // 输出：t 的前半部分
    cout << first << "\n";

    return 0;
}


