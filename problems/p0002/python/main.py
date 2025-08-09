#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
问题: 计算两个数的最大公约数 (GCD)
输入: 两个正整数 a, b
输出: a 和 b 的最大公约数
"""

def gcd(a, b):
    """计算最大公约数"""
    while b:
        a, b = b, a % b
    return a

def main():
    try:
        a, b = map(int, input().split())
        result = gcd(a, b)
        print(result)
    except (ValueError, EOFError):
        return

if __name__ == "__main__":
    main()
