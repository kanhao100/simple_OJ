#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简易OJ测试小工具
支持多个测试用例、多种语言、跨平台运行
"""

import os
import sys
import json
import subprocess
import time
import argparse
import platform
from pathlib import Path
from typing import List, Dict, Tuple, Optional

class Colors:
    """ANSI颜色代码"""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

    @staticmethod
    def disable():
        """禁用颜色（在Windows Command Prompt中可能需要）"""
        Colors.RED = Colors.GREEN = Colors.YELLOW = Colors.BLUE = ''
        Colors.PURPLE = Colors.CYAN = Colors.WHITE = Colors.BOLD = ''
        Colors.UNDERLINE = Colors.END = ''

class OJTester:
    def __init__(self, use_wsl: bool = False, timeout: int = 5):
        self.use_wsl = use_wsl
        self.timeout = timeout
        self.problems_dir = Path("problems")
        self.build_dir = Path("build")
        self.results = []
        
        # 在Windows下检测颜色支持
        if platform.system() == "Windows" and os.environ.get('TERM') != 'xterm':
            try:
                # 尝试启用Windows 10的ANSI支持
                import ctypes
                kernel32 = ctypes.windll.kernel32
                kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
            except:
                Colors.disable()
    
    def print_header(self, text: str):
        """打印标题"""
        print(f"\n{Colors.CYAN}{Colors.BOLD}{'='*60}{Colors.END}")
        print(f"{Colors.CYAN}{Colors.BOLD}{text:^60}{Colors.END}")
        print(f"{Colors.CYAN}{Colors.BOLD}{'='*60}{Colors.END}")
    
    def print_success(self, text: str):
        """打印成功信息"""
        print(f"{Colors.GREEN}✓ {text}{Colors.END}")
    
    def print_error(self, text: str):
        """打印错误信息"""
        print(f"{Colors.RED}✗ {text}{Colors.END}")
    
    def print_warning(self, text: str):
        """打印警告信息"""
        print(f"{Colors.YELLOW}⚠ {text}{Colors.END}")
    
    def print_info(self, text: str):
        """打印信息"""
        print(f"{Colors.BLUE}ℹ {text}{Colors.END}")

    def load_test_cases(self, problem_dir: Path) -> List[Dict]:
        """加载测试用例"""
        # 优先尝试新的文本格式
        tests_txt_file = problem_dir / "tests.txt"
        tests_json_file = problem_dir / "tests.json"
        
        if tests_txt_file.exists():
            return self.load_test_cases_from_txt(tests_txt_file)
        elif tests_json_file.exists():
            return self.load_test_cases_from_json(tests_json_file)
        else:
            raise FileNotFoundError(f"测试文件不存在: {tests_txt_file} 或 {tests_json_file}")
    
    def load_test_cases_from_txt(self, tests_file: Path) -> List[Dict]:
        """从文本格式加载测试用例"""
        try:
            with open(tests_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            test_cases = []
            # 按测试用例分割
            case_sections = content.split('=== TEST CASE')
            
            for i, section in enumerate(case_sections):
                if i == 0 and not section.strip():
                    continue  # 跳过第一个空段
                
                section = section.strip()
                if not section:
                    continue
                
                # 移除开头的数字和 ===
                if section.startswith(str(i)) or any(section.startswith(str(j)) for j in range(1, 100)):
                    lines = section.split('\n')
                    section = '\n'.join(lines[1:])  # 移除第一行的 "1 ==="
                
                # 查找 INPUT: 和 OUTPUT: 标记
                if 'INPUT:' not in section or 'OUTPUT:' not in section:
                    continue
                
                input_start = section.find('INPUT:') + len('INPUT:')
                output_start = section.find('OUTPUT:')
                
                if output_start == -1:
                    continue
                
                input_text = section[input_start:output_start].strip()
                output_text = section[output_start + len('OUTPUT:'):].strip()
                
                test_cases.append({
                    'input': input_text,
                    'output': output_text
                })
            
            if not test_cases:
                raise ValueError("没有找到有效的测试用例")
            
            return test_cases
            
        except Exception as e:
            raise ValueError(f"解析文本格式测试用例失败: {e}")
    
    def load_test_cases_from_json(self, tests_file: Path) -> List[Dict]:
        """从JSON格式加载测试用例（保持向后兼容）"""
        try:
            with open(tests_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                # 修复可能的JSON格式问题
                if content.endswith(','):
                    content = content[:-1]
                if content.startswith('[') and not content.endswith(']'):
                    content += ']'
                
                tests = json.loads(content)
                if isinstance(tests, dict):
                    tests = [tests]  # 单个测试用例转换为列表
                return tests
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON格式错误: {e}")

    def get_compiler_command(self, lang: str, source_file: Path, output_file: Path) -> List[str]:
        """获取编译命令"""
        if lang == "cpp":
            base_cmd = ["g++", "-std=c++17", "-O2", "-o", str(output_file), str(source_file)]
            if self.use_wsl:
                return ["wsl"] + base_cmd
            return base_cmd
        elif lang == "c":
            base_cmd = ["gcc", "-std=c99", "-O2", "-o", str(output_file), str(source_file)]
            if self.use_wsl:
                return ["wsl"] + base_cmd
            return base_cmd
        elif lang == "java":
            # Java需要特殊处理
            return ["javac", str(source_file)]
        elif lang == "python":
            # Python不需要编译，直接返回空命令
            return []
        else:
            raise ValueError(f"不支持的语言: {lang}")

    def get_run_command(self, lang: str, executable: Path) -> List[str]:
        """获取运行命令"""
        if lang in ["cpp", "c"]:
            if self.use_wsl:
                return ["wsl", str(executable).replace('\\', '/')]
            return [str(executable)]
        elif lang == "java":
            class_name = executable.stem
            return ["java", "-cp", str(executable.parent), class_name]
        elif lang == "python":
            return ["python", str(executable)]
        else:
            raise ValueError(f"不支持的语言: {lang}")

    def compile_solution(self, problem: str, lang: str) -> Optional[Path]:
        """编译解决方案"""
        problem_dir = self.problems_dir / problem
        source_dir = problem_dir / lang
        
        if not source_dir.exists():
            self.print_error(f"源代码目录不存在: {source_dir}")
            return None
        
        # 查找源文件
        if lang == "cpp":
            source_files = list(source_dir.glob("*.cpp"))
        elif lang == "c":
            source_files = list(source_dir.glob("*.c"))
        elif lang == "java":
            source_files = list(source_dir.glob("*.java"))
        elif lang == "python":
            source_files = list(source_dir.glob("*.py"))
        else:
            self.print_error(f"不支持的语言: {lang}")
            return None
        
        if not source_files:
            self.print_error(f"在 {source_dir} 中找不到源文件")
            return None
        
        source_file = source_files[0]  # 使用第一个找到的源文件
        
        # 创建构建目录
        build_problem_dir = self.build_dir / problem
        build_problem_dir.mkdir(parents=True, exist_ok=True)
        
        # 设置输出文件
        if lang == "java":
            output_file = build_problem_dir / f"{source_file.stem}.class"
        elif lang == "python":
            # Python不需要编译，直接返回源文件
            self.print_success(f"Python脚本: {source_file}")
            return source_file
        else:
            executable_name = f"{problem}_{lang}"
            if platform.system() == "Windows" and not self.use_wsl:
                executable_name += ".exe"
            output_file = build_problem_dir / executable_name
        
        # 编译
        compile_cmd = self.get_compiler_command(lang, source_file, output_file)
        if not compile_cmd:  # Python等解释型语言
            return source_file
            
        self.print_info(f"编译命令: {' '.join(compile_cmd)}")
        
        try:
            result = subprocess.run(
                compile_cmd, 
                capture_output=True, 
                text=True, 
                timeout=30,
                cwd=str(build_problem_dir) if lang == "java" else None,
                encoding='utf-8',
                errors='replace'
            )
            
            if result.returncode != 0:
                self.print_error("编译失败:")
                if result.stderr:
                    print(f"{Colors.RED}{result.stderr}{Colors.END}")
                return None
            
            self.print_success(f"编译成功: {output_file}")
            return output_file
            
        except subprocess.TimeoutExpired:
            self.print_error("编译超时")
            return None
        except FileNotFoundError:
            self.print_error(f"编译器未找到。请确保已安装 {lang} 编译器")
            if not self.use_wsl and platform.system() == "Windows":
                self.print_info("提示: 在Windows上可以尝试使用 --wsl 选项")
                self.print_info("或者安装 MinGW-w64 或 Visual Studio Build Tools")
            return None

    def run_single_test(self, executable: Path, lang: str, test_input: str) -> Tuple[bool, str, str, float]:
        """运行单个测试用例"""
        run_cmd = self.get_run_command(lang, executable)
        
        start_time = time.time()
        try:
            process = subprocess.run(
                run_cmd,
                input=test_input,
                capture_output=True,
                text=True,
                timeout=self.timeout,
                encoding='utf-8',
                errors='replace'
            )
            end_time = time.time()
            
            if process.returncode != 0:
                return False, "", f"运行时错误 (退出码: {process.returncode})\n{process.stderr}", end_time - start_time
            
            return True, process.stdout, process.stderr, end_time - start_time
            
        except subprocess.TimeoutExpired:
            end_time = time.time()
            return False, "", f"超时 (>{self.timeout}秒)", end_time - start_time

    def compare_output(self, expected: str, actual: str) -> bool:
        """比较输出结果"""
        # 去除首尾空白并比较
        expected_lines = [line.rstrip() for line in expected.strip().split('\n')]
        actual_lines = [line.rstrip() for line in actual.strip().split('\n')]
        return expected_lines == actual_lines

    def run_tests(self, problem: str, lang: str) -> bool:
        """运行所有测试用例"""
        self.print_header(f"测试问题: {problem} ({lang})")
        
        try:
            # 加载测试用例
            problem_dir = self.problems_dir / problem
            test_cases = self.load_test_cases(problem_dir)
            self.print_info(f"加载了 {len(test_cases)} 个测试用例")
            
            # 编译
            executable = self.compile_solution(problem, lang)
            if not executable:
                return False
            
            # 运行测试
            passed = 0
            total = len(test_cases)
            
            for i, test_case in enumerate(test_cases, 1):
                print(f"\n{Colors.YELLOW}测试用例 {i}/{total}:{Colors.END}")
                
                test_input = test_case.get("input", "")
                expected_output = test_case.get("output", "")
                
                # 显示输入（如果不太长）
                if len(test_input) <= 100:
                    print(f"输入: {repr(test_input)}")
                else:
                    print(f"输入: (长度 {len(test_input)} 字符)")
                
                success, actual_output, error_msg, exec_time = self.run_single_test(
                    executable, lang, test_input
                )
                
                if not success:
                    self.print_error(f"运行失败: {error_msg}")
                    continue
                
                if self.compare_output(expected_output, actual_output):
                    self.print_success(f"通过 (耗时: {exec_time:.3f}秒)")
                    passed += 1
                else:
                    self.print_error("输出不匹配")
                    print(f"{Colors.PURPLE}期望输出:{Colors.END}")
                    print(repr(expected_output))
                    print(f"{Colors.PURPLE}实际输出:{Colors.END}")
                    print(repr(actual_output))
            
            # 总结
            print(f"\n{Colors.BOLD}测试结果: {passed}/{total} 通过{Colors.END}")
            
            if passed == total:
                self.print_success("所有测试用例通过! 🎉")
                return True
            else:
                self.print_warning(f"{total - passed} 个测试用例失败")
                return False
                
        except Exception as e:
            self.print_error(f"测试过程中出错: {e}")
            return False

    def clean_build(self, problem: str):
        """清理构建产物"""
        build_problem_dir = self.build_dir / problem
        if build_problem_dir.exists():
            import shutil
            shutil.rmtree(build_problem_dir)
            self.print_success(f"已清理构建目录: {build_problem_dir}")
        else:
            self.print_info(f"构建目录不存在: {build_problem_dir}")

    def list_problems(self) -> List[str]:
        """列出所有问题"""
        if not self.problems_dir.exists():
            return []
        
        problems = []
        for item in self.problems_dir.iterdir():
            if item.is_dir() and ((item / "tests.json").exists() or (item / "tests.txt").exists()):
                problems.append(item.name)
        
        return sorted(problems)

    def run_all_problems(self, lang: str):
        """运行所有问题"""
        problems = self.list_problems()
        if not problems:
            self.print_warning("没有找到任何问题")
            return
        
        self.print_header(f"运行所有问题 ({len(problems)} 个)")
        
        success_count = 0
        for problem in problems:
            if self.run_tests(problem, lang):
                success_count += 1
        
        print(f"\n{Colors.BOLD}总体结果: {success_count}/{len(problems)} 个问题全部通过{Colors.END}")
        
        if success_count == len(problems):
            self.print_success("恭喜! 所有问题都通过了! 🎉🎉🎉")
        else:
            self.print_warning(f"还有 {len(problems) - success_count} 个问题需要解决")

    def create_new_problem(self, problem_name: str):
        """创建新问题"""
        self.print_header(f"创建新问题: {problem_name}")
        
        problem_dir = self.problems_dir / problem_name
        if problem_dir.exists():
            self.print_warning(f"问题 {problem_name} 已存在")
            return
        
        try:
            # 创建目录结构
            cpp_dir = problem_dir / "cpp"
            python_dir = problem_dir / "python"
            cpp_dir.mkdir(parents=True, exist_ok=True)
            python_dir.mkdir(parents=True, exist_ok=True)
            
            # 创建C++模板文件
            cpp_template = """#include <iostream>
#include <string>
#include <vector>
#include <algorithm>

using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    // TODO: 实现你的算法
    
    return 0;
}
"""
            cpp_file = cpp_dir / "main.cpp"
            with open(cpp_file, 'w', encoding='utf-8') as f:
                f.write(cpp_template)
            
            # 创建Python模板文件
            python_template = """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"
问题描述: [在这里描述问题]
输入: [描述输入格式]
输出: [描述输出格式]
\"\"\"

def main():
    try:
        # TODO: 读取输入
        # TODO: 实现你的算法
        # TODO: 输出结果
        pass
    except (ValueError, EOFError):
        return

if __name__ == "__main__":
    main()
"""
            python_file = python_dir / "main.py"
            with open(python_file, 'w', encoding='utf-8') as f:
                f.write(python_template)
            
            # 创建测试用例模板文件
            tests_template = """=== TEST CASE 1 ===
INPUT:
[输入示例]
OUTPUT:
[预期输出]

=== TEST CASE 2 ===
INPUT:
[输入示例]
OUTPUT:
[预期输出]
"""
            tests_file = problem_dir / "tests.txt"
            with open(tests_file, 'w', encoding='utf-8') as f:
                f.write(tests_template)
            
            self.print_success(f"成功创建问题目录: {problem_dir}")
            self.print_success(f"C++ 文件: {cpp_file}")
            self.print_success(f"Python 文件: {python_file}")
            self.print_success(f"测试用例文件: {tests_file}")
            
            print(f"\n{Colors.CYAN}下一步:{Colors.END}")
            print(f"1. 编辑 {tests_file} 添加测试用例")
            print(f"2. 实现算法在 {cpp_file} 或 {python_file}")
            print(f"3. 运行测试: {Colors.YELLOW}python oj.py --problem {problem_name} --lang python{Colors.END}")
            
        except Exception as e:
            self.print_error(f"创建问题失败: {e}")

def main():
    parser = argparse.ArgumentParser(description="简易OJ测试小工具")
    parser.add_argument("--problem", "-p", help="要测试的问题名称")
    parser.add_argument("--lang", "-l", default="cpp", help="编程语言 (默认: cpp)")
    parser.add_argument("--all", "-a", action="store_true", help="运行所有问题")
    parser.add_argument("--clean", "-c", action="store_true", help="清理构建产物")
    parser.add_argument("--wsl", action="store_true", help="在Windows上使用WSL运行")
    parser.add_argument("--timeout", "-t", type=int, default=5, help="执行超时时间(秒) (默认: 5)")
    parser.add_argument("--list", action="store_true", help="列出所有可用的问题")
    parser.add_argument("--new", "-n", help="创建新问题（指定问题名称，如: p0004）")
    
    args = parser.parse_args()
    
    tester = OJTester(use_wsl=args.wsl, timeout=args.timeout)
    
    if args.list:
        problems = tester.list_problems()
        if problems:
            tester.print_header("可用的问题")
            for problem in problems:
                print(f"  • {problem}")
            print(f"\n使用示例: python oj.py --problem {problems[0]} --lang python")
        else:
            tester.print_warning("没有找到任何问题")
        return
    
    if args.new:
        tester.create_new_problem(args.new)
        return
    
    if args.clean:
        if args.problem:
            tester.clean_build(args.problem)
        else:
            # 清理所有构建产物
            import shutil
            if tester.build_dir.exists():
                shutil.rmtree(tester.build_dir)
                tester.print_success("已清理所有构建产物")
            else:
                tester.print_info("构建目录不存在")
        return
    
    if args.all:
        tester.run_all_problems(args.lang)
    elif args.problem:
        success = tester.run_tests(args.problem, args.lang)
        sys.exit(0 if success else 1)
    else:
        parser.print_help()
        # 如果没有参数，列出可用问题
        problems = tester.list_problems()
        if problems:
            tester.print_header("可用的问题")
            for problem in problems:
                print(f"  • {problem}")
            print(f"\n{Colors.CYAN}常用命令:{Colors.END}")
            print(f"  创建新问题: {Colors.YELLOW}python oj.py --new p0005{Colors.END}")
            print(f"  运行测试:   {Colors.YELLOW}python oj.py --problem {problems[0]} --lang python{Colors.END}")
            print(f"  列出问题:   {Colors.YELLOW}python oj.py --list{Colors.END}")
        else:
            print(f"\n{Colors.CYAN}开始使用:{Colors.END}")
            print(f"  创建第一个问题: {Colors.YELLOW}python oj.py --new p0001{Colors.END}")

if __name__ == "__main__":
    main()
