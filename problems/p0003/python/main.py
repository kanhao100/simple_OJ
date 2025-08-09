#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
问题: 矩阵转置
输入: 第一行包含两个整数 m, n，表示矩阵的行数和列数
      接下来 m 行，每行包含 n 个整数，表示矩阵的元素
输出: 转置后的矩阵，共 n 行，每行 m 个整数
"""

def main():
    try:
        m, n = map(int, input().split())
        matrix = []
        
        for i in range(m):
            row = list(map(int, input().split()))
            matrix.append(row)
        
        # 转置矩阵
        for j in range(n):
            row = []
            for i in range(m):
                row.append(matrix[i][j])
            print(' '.join(map(str, row)))
            
    except (ValueError, EOFError):
        return

if __name__ == "__main__":
    main()
