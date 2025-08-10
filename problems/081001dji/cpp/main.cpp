#include <bits/stdc++.h>
using namespace std;

static bool isPrime(long long x) {
    if (x <= 1) return false;
    if (x % 2 == 0) return x == 2;
    for (long long i = 3; i <= x / i; i += 2) {
        if (x % i == 0) return false;
    }
    return true;
}

static long double fixNegZero(long double x) {
    return fabsl(x) < 0.0005L ? 0.0L : x;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cout.setf(ios::fixed);
    cout << setprecision(2);

    while (cin >> n) {
        vector<long long> v(n);
        for (int i = 0; i < n; ++i) cin >> v[i];

        if (n < 3) { cout << "Singular matrix\n"; continue; }

        vector<long long> t = v;
        sort(t.begin(), t.end(), greater<long long>());

        long long a = t[0], b = t[1], c = t[2];

        long long d = LLONG_MIN;
        for (long long x : v) if (isPrime(x)) d = max(d, x);
        if (d == LLONG_MIN) { cout << "Singular matrix\n"; continue; }

        __int128 det128 = (__int128)a * d - (__int128)b * c;
        if (det128 == 0) { cout << "Singular matrix\n"; continue; }

        long double det = (long double)det128;
        long double m00 = (long double)d / det;
        long double m01 = -(long double)b / det;
        long double m10 = -(long double)c / det;
        long double m11 = (long double)a / det;

        cout << fixNegZero(m00) << " " << fixNegZero(m01) << "\n";
        cout << fixNegZero(m10) << " " << fixNegZero(m11) << "\n";
    }
    return 0;
}