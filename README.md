# 简易 OJ 测试小工具

这是一个功能完整的本地 OJ 测试系统，支持多个测试用例、多种编程语言、跨平台运行（Windows/WSL/Linux）。

## ✨ 主要特性

- 🔥 **多语言支持**: C++, C, Java, Python
- 🎯 **多测试用例**: 每个问题可包含多个测试用例
- 📝 **友好格式**: 支持多行文本格式，直接复制粘贴，无需转义
- 🌈 **彩色输出**: 清晰的测试结果显示
- ⚡ **快速测试**: 自动编译、运行和结果比较
- 🔄 **跨平台**: 支持 Windows、WSL、Linux
- 📊 **详细报告**: 执行时间、错误信息、输出对比

## 📁 目录结构

```
local_OJ/
├── problems/                 # 问题目录
│   ├── p0001/               # 字符串处理问题
│   │   ├── cpp/main.cpp     # C++ 解法
│   │   ├── python/main.py   # Python 解法
│   │   └── tests.json       # 测试用例
│   └── p0002/               # 数学问题 (GCD)
│       ├── python/main.py   # Python 解法
│       └── tests.json       # 测试用例
├── oj.py                    # 核心测试脚本
├── test.bat                 # Windows 批处理脚本
├── makefile                 # Linux/WSL Makefile
└── build/                   # 编译产物（自动创建）
```

## 🚀 快速开始

### 1. 列出所有可用问题
```bash
python oj.py --list
```

### 2. 创建新问题
```bash
# 创建新问题p0004，自动生成目录结构和模板文件
python oj.py --new p0004
```

### 3. 运行单个问题
```bash
# Python 版本（推荐，兼容性最好）
python oj.py --problem p0001 --lang python
python oj.py --problem p0002 --lang python

# C++ 版本
python oj.py --problem p0001 --lang cpp

# 在 Windows 上使用 WSL
python oj.py --problem p0001 --lang cpp --wsl
```

### 3. 运行所有问题
```bash
python oj.py --all --lang python
```

### 4. Windows 用户的便捷方式
```cmd
# 使用批处理脚本
.\test.bat p0001 python
.\test.bat p0002 python
```

### 5. Linux/WSL 用户使用 Makefile
```bash
make test PROB=p0001 LANG=python
make test-all LANG=python
```

## 📝 添加新问题

### 方法一：自动创建（推荐）

```bash
# 一键创建新问题，自动生成目录和模板文件
python oj.py --new p0004
```

这个命令会自动创建：
- `problems/p0004/cpp/main.cpp` - C++ 解法模板
- `problems/p0004/python/main.py` - Python 解法模板  
- `problems/p0004/tests.txt` - 测试用例模板

创建完成后：
1. 编辑 `tests.txt` 添加测试用例
2. 在模板文件中实现算法
3. 运行测试验证

### 方法二：手动创建

### 1. 创建问题目录
```bash
mkdir -p problems/p0003/python
```

### 2. 编写解法 (`problems/p0003/python/main.py`)
```python
#!/usr/bin/env python3

def main():
    # 读取输入
    n = int(input())
    
    # 处理逻辑
    result = n * 2
    
    # 输出结果
    print(result)

if __name__ == "__main__":
    main()
```

### 3. 创建测试用例 (`problems/p0003/tests.txt`)

**新的文本格式（推荐）**：支持多行输入输出，直接复制粘贴，无需转义
```
=== TEST CASE 1 ===
INPUT:
5
OUTPUT:
10

=== TEST CASE 2 ===
INPUT:
0
OUTPUT:
0

=== TEST CASE 3 ===
INPUT:
100
OUTPUT:
200
```

**传统JSON格式（兼容）**：需要用\n表示换行
```json
[
  {
    "input": "5",
    "output": "10"
  },
  {
    "input": "0",
    "output": "0"
  },
  {
    "input": "100",
    "output": "200"
  }
]
```

### 4. 测试新问题
```bash
python oj.py --problem p0003 --lang python
```

## 🛠️ 命令行选项

```bash
python oj.py [选项]

选项:
  --problem, -p    指定要测试的问题名称
  --lang, -l       编程语言 (cpp/c/java/python, 默认: cpp)
  --all, -a        运行所有问题
  --list           列出所有可用问题
  --new, -n        创建新问题（指定问题名称，如: p0004）
  --clean, -c      清理构建产物
  --wsl            在 Windows 上强制使用 WSL
  --timeout, -t    执行超时时间(秒) (默认: 5)
```

## 🎯 示例问题

### p0001: 字符串处理
- **描述**: 给定两个字符串 s 和 t，将 s 与 t 的后半部分拼接，然后输出 t 的前半部分
- **输入**: 两行字符串
- **输出**: 拼接结果和前半部分

### p0002: 最大公约数
- **描述**: 计算两个正整数的最大公约数
- **输入**: 两个空格分隔的正整数
- **输出**: 最大公约数

## 🔧 环境要求

- **Python 3.6+** (必需)
- **C++ 编译器** (可选，用于 C++ 解法)
  - Linux: `g++`
  - Windows: MinGW-w64 或 Visual Studio Build Tools
  - WSL: Ubuntu 的 `g++`
- **Java JDK** (可选，用于 Java 解法)

## 💡 使用提示

1. **Python 最兼容**: 建议优先使用 Python 语言，兼容性最好
2. **Windows 用户**: 如果没有 C++ 编译器，使用 `--wsl` 选项或安装 MinGW-w64
3. **测试用例格式**: 
   - **推荐**: 使用 `tests.txt` 文本格式，支持多行，易于编辑
   - **兼容**: 仍支持 `tests.json` JSON格式
4. **输出比较**: 自动去除首尾空白进行比较
5. **执行时间**: 每个测试用例会显示执行时间
6. **多行输入**: 文本格式下可以直接粘贴多行内容，无需转义

## 🎨 输出示例

```
============================================================
                    测试问题: p0002 (python)
============================================================
ℹ 加载了 5 个测试用例
✓ Python脚本: problems\p0002\python\main.py

测试用例 1/5:
输入: '12 8'
✓ 通过 (耗时: 0.203秒)

测试用例 2/5:
输入: '15 25'
✓ 通过 (耗时: 0.202秒)

...

测试结果: 5/5 通过
✓ 所有测试用例通过! 🎉
```

## 🤖 AI 生成测试用例 Prompt

如果你想使用AI模型来帮助生成测试用例，可以使用以下Prompt模板：

### 基础Prompt

```
你是一个专业的算法题测试用例生成助手。请为给定的算法题生成全面的测试用例。

**任务要求：**
1. 仔细分析题目描述，理解输入输出格式
2. 从最简单的边界情况开始思考
3. 逐步增加复杂度，覆盖各种情况
4. 按照指定的文本格式输出测试用例

**生成策略：**
- **边界情况**: 最小值、最大值、空输入、单元素等
- **正常情况**: 典型的中等规模测试用例
- **极端情况**: 接近题目限制的大规模测试用例
- **特殊情况**: 可能的特殊输入模式或陷阱

**输出格式：**
=== TEST CASE 1 ===
INPUT:
[输入内容]
OUTPUT:
[预期输出]

=== TEST CASE 2 ===
INPUT:
[输入内容]
OUTPUT:
[预期输出]


**题目描述：**
[在这里粘贴你的算法题描述]

请生成5-8个测试用例，确保覆盖上述各种情况。对于每个测试用例，请简要说明测试的目的。
```

### 高级Prompt（针对复杂题目）

```
你是一个资深的竞赛编程测试用例设计专家。请为以下算法题设计一套完整的测试用例。

**分析步骤：**
1. **题目理解**: 解释题目要求和关键约束
2. **算法分析**: 简述可能的解法思路
3. **复杂度考虑**: 分析时间和空间复杂度要求
4. **测试策略**: 列出需要测试的关键场景

**测试用例分类：**
- **功能测试**: 验证基本功能正确性
- **边界测试**: 测试边界条件和极值
- **性能测试**: 验证在限制条件下的表现
- **错误测试**: 测试异常输入的处理
- **随机测试**: 生成随机数据验证健壮性

**输出要求：**
1. 每个测试用例包含简短的说明
2. 确保测试用例的正确性
3. 按难度递增排列
4. 使用指定的文本格式

**题目描述：**
[复杂算法题描述]

请生成8-12个高质量测试用例。
```


