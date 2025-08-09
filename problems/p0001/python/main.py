#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def main():
    # 读取输入
    try:
        s = input().strip()
        t = input().strip()
    except EOFError:
        return
    
    # 计算t的长度和中点
    m = len(t)
    half = m // 2
    
    # 获取t的前半部分和后半部分
    first = t[:half]
    second = t[half:]
    
    # 输出结果
    print(s + second)
    print(first)

if __name__ == "__main__":
    main()
