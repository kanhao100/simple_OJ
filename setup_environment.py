#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OJ测试工具环境自动配置脚本
自动检测和安装所需环境
"""

import os
import sys
import subprocess
import platform
from pathlib import Path
import urllib.request
import zipfile

class EnvironmentSetup:
    def __init__(self):
        self.is_windows = platform.system() == "Windows"
        self.is_linux = platform.system() == "Linux"
        self.is_macos = platform.system() == "Darwin"

    def print_info(self, text: str):
        """打印信息"""
        print(f"[INFO] {text}")

    def print_error(self, text: str):
        """打印错误"""
        print(f"[ERROR] {text}")

    def print_success(self, text: str):
        """打印成功"""
        print(f"[SUCCESS] {text}")

    def print_warning(self, text: str):
        """打印警告"""
        print(f"[WARNING] {text}")

    def run_command(self, cmd, check_returncode=True):
        """运行命令"""
        try:
            self.print_info(f"执行: {' '.join(cmd) if isinstance(cmd, list) else cmd}")
            result = subprocess.run(cmd, shell=isinstance(cmd, str),
                                  capture_output=True, text=True, check=check_returncode)
            return result.returncode == 0, result.stdout, result.stderr
        except subprocess.CalledProcessError as e:
            return False, e.stdout, e.stderr
        except FileNotFoundError:
            return False, "", "命令未找到"

    def check_python(self):
        """检查Python环境"""
        self.print_info("检查Python环境...")

        version = sys.version_info
        print(f"Python版本: {version.major}.{version.minor}.{version.micro}")

        if version < (3, 6):
            self.print_error("Python版本太低，建议升级到3.6+")
            return False

        self.print_success("Python环境正常")
        return True

    def check_compilers(self):
        """检查编译器"""
        self.print_info("检查编译器...")

        compilers = {
            'C++': ['g++', '--version'],
            'C': ['gcc', '--version'],
            'Java': ['javac', '-version'],
            'Python': [sys.executable, '--version']
        }

        results = {}

        for name, cmd in compilers.items():
            success, stdout, stderr = self.run_command(cmd, check_returncode=False)
            if success:
                version = stdout.split('\n')[0] if stdout else "未知版本"
                self.print_success(f"{name}编译器: {version}")
                results[name] = True
            else:
                self.print_error(f"{name}编译器: 未找到")
                results[name] = False

        return results

    def install_mingw_windows(self):
        """在Windows上安装MinGW-w64"""
        if not self.is_windows:
            return False

        self.print_info("准备安装MinGW-w64...")

        # 检查是否已安装
        if self.run_command(['g++', '--version'], check_returncode=False)[0]:
            self.print_success("MinGW-w64已安装")
            return True

        # 安装选项
        print("\n选择安装方式:")
        print("1. 自动下载安装MinGW-w64 (推荐)")
        print("2. 手动下载安装包")
        print("3. 跳过，稍后手动安装")

        choice = input("请选择 (1/2/3): ").strip()

        if choice == '1':
            return self.auto_install_mingw()
        elif choice == '2':
            self.print_info("请访问: https://www.mingw-w64.org/downloads/")
            self.print_info("下载x86_64-win32-seh版本，安装时添加到PATH")
            return False
        else:
            return False

    def auto_install_mingw(self):
        """自动安装MinGW-w64"""
        try:
            import requests
        except ImportError:
            self.print_error("需要安装requests库: pip install requests")
            return False

        # MinGW-w64下载地址（使用MSYS2的便携版本）
        mingw_url = "https://github.com/msys2/msys2-installer/releases/download/2023-07-18/msys2-x86_64-20230718.exe"
        installer_path = Path.home() / "mingw_installer.exe"

        try:
            # 下载安装包
            self.print_info("下载MinGW-w64安装包...")
            response = requests.get(mingw_url, stream=True)
            response.raise_for_status()

            with open(installer_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            self.print_success(f"下载完成: {installer_path}")

            # 运行安装包
            self.print_info("请运行安装包完成安装，安装时选择添加到PATH")
            print(f"安装包位置: {installer_path}")
            input("安装完成后按回车键继续...")

            # 验证安装
            if self.run_command(['g++', '--version'], check_returncode=False)[0]:
                self.print_success("MinGW-w64安装成功")
                return True
            else:
                self.print_error("安装验证失败")
                return False

        except Exception as e:
            self.print_error(f"自动安装失败: {e}")
            return False

    def setup_wsl(self):
        """设置WSL环境"""
        if not self.is_windows:
            return False

        self.print_info("检查WSL环境...")

        # 检查WSL是否已安装
        success, _, _ = self.run_command(['wsl', '--list', '--verbose'], check_returncode=False)

        if success:
            self.print_success("WSL已安装")
            return True

        self.print_info("WSL未安装，准备安装...")
        print("\n安装WSL步骤:")
        print("1. 以管理员身份打开PowerShell")
        print("2. 运行: wsl --install")
        print("3. 重启计算机")
        print("4. 安装完成后，运行: wsl --install -d Ubuntu")

        choice = input("是否现在以管理员身份运行安装命令? (y/N): ").strip().lower()

        if choice == 'y':
            try:
                # 尝试运行安装命令
                result = subprocess.run(['powershell', 'Start-Process', 'powershell',
                                       '-Verb', 'runAs', '-ArgumentList',
                                       'wsl --install'],
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    self.print_success("安装命令已执行，请按提示完成安装")
                else:
                    self.print_error("安装命令执行失败")
            except Exception as e:
                self.print_error(f"执行失败: {e}")

        return False

    def create_shortcuts(self):
        """创建快捷方式"""
        if not self.is_windows:
            return

        try:
            import winshell
            from win32com.client import Dispatch
        except ImportError:
            self.print_info("安装winshell和pywin32以创建桌面快捷方式")
            return

        desktop = winshell.desktop()
        oj_path = Path(__file__).parent / "oj.py"

        # 创建快捷方式
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(str(desktop / "OJ测试工具.lnk"))
        shortcut.Targetpath = str(oj_path)
        shortcut.WorkingDirectory = str(oj_path.parent)
        shortcut.IconLocation = str(oj_path)
        shortcut.save()

        self.print_success("桌面快捷方式创建完成")

    def main_setup(self):
        """主设置流程"""
        print("=" * 60)
        print("    OJ测试工具环境配置")
        print("=" * 60)
        print()

        # 检查Python
        if not self.check_python():
            return False

        # 检查编译器
        compiler_results = self.check_compilers()

        missing_compilers = [name for name, available in compiler_results.items()
                           if not available and name != 'Python']

        if missing_compilers:
            print(f"\n缺少编译器: {', '.join(missing_compilers)}")

            if self.is_windows:
                print("\n发现缺少编译器，建议配置选项:")
                print("1. 自动安装MinGW-w64 (推荐)")
                print("2. 手动下载安装MinGW-w64")
                print("3. 使用Visual Studio Build Tools")
                print("4. 跳过编译器配置")

                choice = input("请选择 (1/2/3/4): ").strip()
                if choice == '1':
                    self.install_mingw_windows()
                elif choice == '2':
                    self.print_info("请访问: https://www.mingw-w64.org/downloads/")
                    self.print_info("下载x86_64-win32-seh版本，安装时选择添加到PATH")
                elif choice == '3':
                    self.print_info("请下载Visual Studio Community: https://visualstudio.microsoft.com/")
                    self.print_info("安装时选择'Desktop development with C++'")

                if 'Java' in missing_compilers:
                    self.print_info("请安装Java JDK: https://adoptium.net/")
            else:
                print("\n在Linux/macOS上安装编译器:")
                print("Ubuntu/Debian: sudo apt install g++ default-jdk")
                print("CentOS/RHEL: sudo yum install gcc-c++ java-devel")
                print("macOS: xcode-select --install")
        else:
            self.print_success("所有编译器都已可用")

        # 提供WSL选项（仅Windows）
        if self.is_windows:
            print("\n可选环境配置:")
            print("1. WSL (Windows Subsystem for Linux) - Linux开发环境")
            print("2. 跳过")
            choice = input("是否配置WSL环境? (1/2): ").strip()
            if choice == '1':
                self.setup_wsl()

        # 创建快捷方式
        if self.is_windows:
            try:
                self.create_shortcuts()
            except:
                pass

        print("\n" + "=" * 60)
        print("环境配置完成!")
        print("=" * 60)
        print("\n测试工具使用:")
        print("  python oj.py --help              # 查看帮助")
        print("  python oj.py --env               # 查看环境信息")
        print("  python oj.py --new p0005         # 创建新问题")
        print("  python oj.py --problem p0001 --lang python  # 运行测试")
        print()
        print("如有问题，请查看README.md或运行: python oj.py --help")

        return True

def main():
    setup = EnvironmentSetup()
    try:
        setup.main_setup()
    except KeyboardInterrupt:
        print("\n操作已取消")
    except Exception as e:
        setup.print_error(f"设置过程出错: {e}")

if __name__ == "__main__":
    main()
