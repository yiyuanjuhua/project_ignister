#!/bin/bash

# 工程结构分析工具启动脚本

echo "正在启动工程结构分析工具..."

# 检查Python版本
python3 --version

# 检查tkinter是否安装
if python3 -c "import tkinter" 2>/dev/null; then
    echo "✓ tkinter已安装"
else
    echo "✗ tkinter未安装，尝试安装..."
    sudo apt-get update
    sudo apt-get install -y python3-tk
fi

# 启动程序
echo "启动程序..."
python3 main.py