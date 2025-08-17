#include <iostream>
#include <vector>
#include <queue>
#include <algorithm>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int v) : val(v), left(nullptr), right(nullptr) {}
};

int dfs(TreeNode* node, int& diameter) {
    if (!node) return -1;
    int left = dfs(node->left, diameter);
    int right = dfs(node->right, diameter);
    diameter = max(diameter, left + right + 2);
    return 1 + max(left, right);
}

int main() {
    int N;
    while (cin >> N) { // 注意 while 处理多个 case
        vector<int> seq(N);
        for (int i = 0; i < N; ++i) {
            cin >> seq[i];
        }
        if (N == 0 || seq[0] == 0) {
            cout << 0 << endl;
            continue;
        }
        TreeNode* root = new TreeNode(seq[0]);
        queue<TreeNode*> q;
        q.push(root);
        int idx = 1;
        while (!q.empty() && idx < N) {
            TreeNode* cur = q.front();
            q.pop();
            if (idx < N) {
                if (seq[idx] != 0) {
                    cur->left = new TreeNode(seq[idx]);
                    q.push(cur->left);
                }
                ++idx;
            }
            if (idx < N) {
                if (seq[idx] != 0) {
                    cur->right = new TreeNode(seq[idx]);
                    q.push(cur->right);
                }
                ++idx;
            }
        }
        int diameter = 0;
        dfs(root, diameter);
        cout << diameter << endl;
        // 清理内存（可选，ACM中可省）
    }
    return 0;
}
