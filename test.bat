@echo off
REM 简易OJ测试系统 - Windows批处理版本

if "%1"=="" (
    echo 用法: test.bat ^<问题名^> [语言] [额外参数]
    echo 示例: test.bat p0001 python
    echo       test.bat p0002 cpp --wsl
    python oj.py --list
    exit /b 0
)

set PROB=%1
set LANG=%2
if "%LANG%"=="" set LANG=python

shift
shift
set EXTRA_ARGS=
:loop
if "%1"=="" goto endloop
set EXTRA_ARGS=%EXTRA_ARGS% %1
shift
goto loop
:endloop

echo 运行问题: %PROB% (语言: %LANG%)
python oj.py --problem %PROB% --lang %LANG% %EXTRA_ARGS%
