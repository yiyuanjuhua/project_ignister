# σ₃: Technical Context
*v1.0 | Created: 2025-01-17 | Updated: 2025-01-17*
*Π: DEVELOPMENT | Ω: PLAN*

## 🛠️ Technology Stack

### 🖥️ Frontend/UI
- **Tkinter**: Python 内置 GUI 框架
  - 版本: 随 Python 3.6+ 提供
  - 特点: 跨平台、零依赖、轻量级
  - 组件: Frame, Label, Button, Entry, Text, Treeview, Menu

### 🔧 Backend/Logic
- **Python**: 核心开发语言
  - 版本要求: Python 3.6+
  - 特性使用: 类型提示、上下文管理器、生成器
  - 标准库: os, sys, threading, json, fnmatch

### 📚 Core Libraries
```python
# 内置标准库
import os           # 文件系统操作
import sys          # 系统相关功能
import json         # JSON 数据处理
import threading    # 多线程支持
import fnmatch      # 通配符匹配
import tkinter      # GUI 框架
```

## 🗂️ Project Structure Detail

```
project_ignister/
├── ui/                      # 🎨 用户界面层
│   ├── __init__.py         # 模块初始化
│   ├── main_view.py        # 主界面 (185 lines)
│   ├── config_view.py      # 配置界面 (350+ lines)
│   └── project_view.py     # 工程运维界面 (400+ lines)
├── logic/                   # 🧠 业务逻辑层
│   ├── __init__.py         
│   ├── file_processor.py   # 文件处理核心 (200+ lines)
│   ├── filter_engine.py    # 过滤引擎 (150+ lines)
│   └── exporter.py         # 导出模块 (300+ lines)
├── data/                    # 📊 数据层
│   ├── __init__.py         
│   ├── project_model.py    # 项目数据模型 (100+ lines)
│   └── tree_node.py        # 树节点结构 (80+ lines)
├── utils/                   # 🔧 工具层
│   ├── __init__.py         
│   ├── utils.py            # 通用工具 (120+ lines)
│   └── path_utils.py       # 路径工具 (80+ lines)
├── docs/                    # 📖 文档目录
├── exports/                 # 📤 导出文件目录
├── main.py                 # 🚀 程序入口 (287 lines)
├── run.sh                  # 🔄 启动脚本
└── README.md               # 📋 项目说明
```

## 🔧 Development Environment

### 系统要求
- **操作系统**: Windows 10+ / Linux (Ubuntu 18.04+)
- **Python版本**: 3.6.0 或更高版本
- **内存**: 最少 256MB RAM
- **磁盘**: 约 50MB 存储空间

### 开发工具
- **编辑器**: Cursor AI Editor
- **版本控制**: Git
- **测试**: 手动功能测试
- **文档**: Markdown 格式

## 📦 Dependencies

### 核心依赖
```
# 无外部依赖！
# 仅使用 Python 标准库
Python 3.6+ (内置):
  - tkinter (GUI)
  - os (文件系统)
  - sys (系统功能)
  - json (数据序列化)
  - threading (多线程)
  - fnmatch (模式匹配)
```

### 可选依赖
```
# 用于增强功能 (未使用)
# - pathlib (现代路径处理)
# - typing (类型注解支持)
# - dataclasses (数据类)
```

## 🚀 Deployment & Runtime

### 启动方式
```bash
# 直接启动
python main.py

# 或使用脚本
chmod +x run.sh
./run.sh
```

### 运行时特征
- **启动时间**: < 2 秒
- **内存占用**: 约 20-50MB
- **CPU 使用**: 扫描时中等，其他时候低
- **磁盘 I/O**: 扫描和导出时较高

## 🔍 Key Technical Features

### 文件系统处理
- **递归遍历**: 使用 `os.walk()` 高效遍历
- **权限处理**: 异常捕获处理访问受限目录
- **路径标准化**: 跨平台路径处理

### 过滤算法
- **通配符支持**: 基于 `fnmatch` 的模式匹配
- **gitignore 解析**: 完整支持 gitignore 语法
- **否定模式**: 支持 `!pattern` 排除语法

### UI 响应性
- **多线程**: 文件扫描在后台线程执行
- **进度反馈**: 实时进度条和状态更新
- **异步操作**: 避免 UI 冻结

### 数据格式
```python
# TreeNode 数据结构
{
    "name": "文件名",
    "type": "file|directory", 
    "path": "完整路径",
    "size": 文件大小,
    "description": "用户描述",
    "children": [子节点列表]
}
```

## 🔒 Security Considerations

- **路径遍历防护**: 验证用户输入的路径
- **权限检查**: 访问文件前检查读取权限
- **异常处理**: 全面的错误捕获和处理
- **资源限制**: 避免过深的递归和大文件处理

## 📈 Performance Characteristics

- **时间复杂度**: O(n) where n = 文件总数
- **空间复杂度**: O(h) where h = 目录深度
- **扩展性**: 适合中小型项目 (< 10k 文件)
- **响应时间**: 大多数操作 < 1 秒 