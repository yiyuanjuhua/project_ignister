# σ₁: Project Brief
*v1.0 | Created: 2025-01-17 | Updated: 2025-01-17*
*Π: DEVELOPMENT | Ω: PLAN*

## 🏆 Overview
工程结构分析工具 - 一个基于 Python + Tkinter 的项目结构分析和文档生成工具，用于帮助开发者快速了解项目结构并生成相应的文档。

## 📋 Requirements
- [R₁] **目录结构扫描**: 递归扫描指定目录，构建完整的文件树结构
- [R₂] **智能过滤系统**: 支持自定义过滤条件，可以排除不需要的文件和目录
- [R₃] **.gitignore 支持**: 自动读取并应用 .gitignore 文件中的规则
- [R₄] **交互式编辑**: 通过图形界面为每个文件和目录添加功能描述
- [R₅] **多格式导出**: 支持导出为 Markdown、JSON 或 Cursor Rules 格式
- [R₆] **跨平台支持**: 支持 Windows 和 Linux 操作系统
- [R₇] **用户友好界面**: 基于 Tkinter 的图形用户界面

## 🎯 Project Goals
1. 提供简单易用的项目结构分析工具
2. 帮助开发者快速理解和文档化项目结构
3. 支持多种导出格式以满足不同需求
4. 实现跨平台兼容性

## 🔍 Current Status
✅ **已完成**: 核心功能全部实现，包括扫描、过滤、UI界面和多格式导出
✅ **测试状态**: 功能测试完成，程序运行稳定
✅ **部署状态**: 可通过 `python main.py` 直接启动使用

## 📊 Success Criteria
- [C₁] 能够成功扫描和分析项目目录结构
- [C₂] 过滤功能正常工作，支持 .gitignore 规则
- [C₃] UI界面响应流畅，用户体验良好
- [C₄] 导出功能生成正确格式的文件
- [C₅] 在 Windows 和 Linux 平台上正常运行

## 🛠️ Technical Requirements
- Python 3.6+ 
- Tkinter GUI 框架
- 支持的导出格式: Markdown, JSON, Cursor Rules
- 架构模式: 分层架构（UI层、业务逻辑层、数据层、工具层） 