# OJ测试工具安装指南

本文档提供详细的安装和配置指南，帮助用户快速开始使用OJ测试工具。

## 📋 目录

- [快速安装](#快速安装)
- [详细安装步骤](#详细安装步骤)
- [环境配置](#环境配置)
- [故障排除](#故障排除)
- [便携式版本](#便携式版本)

## 🚀 快速安装

### 方法一：便携式版本（推荐）

1. **下载便携式包**
   - 从发布页面下载 `oj_tester_portable_windows.zip` (Windows)
   - 或下载 `oj_tester_portable_linux.tar.gz` (Linux/macOS)

2. **解压文件**
   - 解压到任意目录（如 `C:\OJ_Tester` 或 `~/oj_tester`）

3. **运行测试**
   ```bash
   # Windows
   start_oj.bat --env

   # Linux/macOS
   ./start_oj.sh --env
   ```

### 方法二：自动配置

```bash
# 运行环境配置脚本
python setup_environment.py
```

**自动配置流程：**
1. 检测Python版本
2. 检查编译器状态
3. 提供多种配置选项：
   - 自动安装MinGW-w64（推荐）
   - 手动下载安装MinGW-w64
   - 使用Visual Studio Build Tools
   - 跳过编译器配置
4. 可选配置WSL环境
5. 创建桌面快捷方式（Windows）

### 方法三：手动安装

按照[详细安装步骤](#详细安装步骤)进行安装。

## 📦 详细安装步骤

### 1. Python环境

**检查Python版本：**
```bash
python --version
# 应该显示 3.6 或更高版本
```

**如果没有Python：**
- **Windows**: 从 [python.org](https://python.org) 下载安装包
- **Ubuntu/Debian**: `sudo apt install python3 python3-pip`
- **CentOS/RHEL**: `sudo yum install python3 python3-pip`
- **macOS**: 使用Homebrew: `brew install python`

### 2. 编译器安装

#### Windows用户

**推荐：MinGW-w64**
1. 下载: https://www.mingw-w64.org/downloads/
2. 选择: `x86_64-win32-seh` 版本
3. 安装时选择"添加到PATH"
4. 验证: `g++ --version`

**替代方案：Visual Studio Build Tools**
1. 下载Visual Studio Community
2. 安装时选择"Desktop development with C++"
3. 重启计算机

#### Linux用户

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install g++ gcc default-jdk

# CentOS/RHEL
sudo yum install gcc-c++ java-devel

# Arch Linux
sudo pacman -S gcc jdk-openjdk
```

#### macOS用户

```bash
# 安装Xcode命令行工具
xcode-select --install

# 或者使用Homebrew
brew install gcc
```

### 3. Java环境（可选）

**下载OpenJDK：**
- [Adoptium](https://adoptium.net/) (推荐)
- [Oracle JDK](https://oracle.com/java/)

**验证安装：**
```bash
javac -version
java -version
```

## ⚙️ 环境配置

### 1. 环境检查

```bash
python oj.py --env
```

这将显示：
```
============================================================
                            环境信息
============================================================
Python版本: 3.10.11
操作系统: Windows 10

编译器状态:
  CPP : ✓ 找到 (g++ 13.1.0)
  C   : ✓ 找到 (gcc 13.1.0)
  JAVA: ✓ 找到 (javac)
  PY  : ✓ 可用
```

### 2. 自动配置

```bash
python setup_environment.py
```

这个脚本会：
- 检测Python版本
- 检查编译器状态
- 自动下载安装MinGW-w64（Windows）
- 创建桌面快捷方式
- 提供配置建议

## 🔧 使用方法

### 基本使用

```bash
# 查看帮助
python oj.py --help

# 查看环境信息
python oj.py --env

# 列出所有问题
python oj.py --list

# 创建新问题
python oj.py --new p0005

# 运行测试（Python）
python oj.py --problem p0001 --lang python

# 运行测试（C++）
python oj.py --problem p0001 --lang cpp

# 运行所有问题
python oj.py --all --lang python
```

### Windows便捷方式

```cmd
REM 使用批处理脚本
.\test.bat p0001 python
.\test.bat p0002 cpp
```

### Linux/macOS使用Makefile

```bash
make test PROB=p0001 LANG=python
make test-all LANG=python
```

## 🛠️ 故障排除

### 编译器相关问题

**问题：`g++: command not found`**
- **Windows**: 重新安装MinGW-w64，确保添加到PATH
- **Linux**: `sudo apt install g++`
- **macOS**: `xcode-select --install`

**问题：编译失败**
```bash
# 检查编译器版本
g++ --version

# 清理构建文件
python oj.py --clean

# 重新编译
python oj.py --problem p0001 --lang cpp
```

### Python相关问题

**问题：`ModuleNotFoundError`**
```bash
# 升级pip
python -m pip install --upgrade pip

# 安装依赖
pip install requests py7zr
```

**问题：编码错误**
- 确保测试文件使用UTF-8编码
- Windows用户可以在命令行前添加 `chcp 65001`

### 权限问题

**Linux/macOS权限问题：**
```bash
# 给脚本执行权限
chmod +x oj.py
chmod +x start_oj.sh

# 如果需要sudo权限运行编译器
sudo apt install g++
```

## 📦 便携式版本

### 创建便携式包

如果您想为其他用户创建便携式版本：

```bash
# 运行打包脚本
python package_oj.py
```

**便携式版本特性：**
- 使用MSYS2作为MinGW-w64环境
- 提供完整的Linux工具链
- 包含以下内容：
  - OJ测试工具核心程序
  - MSYS2编译器环境
  - 所有测试问题和示例
  - 启动脚本
  - 自动配置脚本

### 便携式版本优势

1. **零配置**: 解压即用，无需安装
2. **完整环境**: 包含所有必需的编译器
3. **跨平台**: 支持Windows、Linux、macOS
4. **便于分发**: 单文件分发，适合教学环境
5. **版本一致**: 确保所有用户使用相同环境

### 便携式版本使用

```bash
# 解压后直接使用
cd oj_tester_portable/

# 运行环境检查
python oj.py --env

# 运行测试
python oj.py --problem p0001 --lang python
```

## 📞 获取帮助

如果遇到问题：

1. **查看环境信息**: `python oj.py --env`
2. **检查README.md**: 包含详细的使用说明
3. **运行自动配置**: `python setup_environment.py`
4. **查看帮助**: `python oj.py --help`

## 📝 版本说明

- **v1.0**: 基础OJ测试功能
- **v2.0**: 添加环境检测和自动配置
- **v3.0**: 支持便携式打包和多平台部署

---

**提示**: 建议优先使用Python语言进行测试，因为它兼容性最好且无需额外编译器。
