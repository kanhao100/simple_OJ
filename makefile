# 多题目 OJ Makefile

# 可传入变量：
#   PROB=p0001 LANG=cpp ARGS="--wsl"

PROB ?= p0001
LANG ?= cpp
ARGS ?=

.DEFAULT_GOAL := test

build:
	python oj.py --problem $(PROB) --lang $(LANG) $(ARGS)

# 运行测试（build 即编译+运行）
test: build

# 运行所有题目
test-all:
	python oj.py --all --lang $(LANG) $(ARGS)

# 清理当前题目
clean:
	python oj.py --clean --problem $(PROB)

.PHONY: build test test-all clean