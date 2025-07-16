"""
导出模块
"""

import json
from datetime import datetime
from utils.utils import Utils
from utils.path_utils import PathUtils

class Exporter:
    """导出功能类"""
    
    def __init__(self):
        pass
    
    def export_to_json(self, project_model, output_path=None):
        """导出为JSON格式"""
        try:
            # 构建导出数据
            export_data = {
                'export_time': Utils.format_datetime(),
                'project_info': {
                    'project_path': project_model.project_path,
                    'filter_conditions': project_model.filter_conditions,
                    'use_gitignore': project_model.use_gitignore
                },
                'structure': project_model.root_node.to_dict() if project_model.root_node else None
            }
            
            # 如果没有指定输出路径，使用默认路径
            if not output_path:
                project_name = PathUtils.get_filename(project_model.project_path) or "project"
                filename = f"{project_name}_structure_{Utils.get_timestamp()}.json"
                output_path = PathUtils.join_path("exports", filename)
            
            # 写入文件
            success = Utils.write_json_file(output_path, export_data)
            
            if success:
                return output_path, "JSON导出成功"
            else:
                return None, "JSON导出失败"
                
        except Exception as e:
            return None, f"JSON导出失败: {str(e)}"
    
    def export_to_markdown(self, project_model, output_path=None):
        """导出为Markdown格式"""
        try:
            # 构建Markdown内容
            markdown_content = self._build_markdown_content(project_model)
            
            # 如果没有指定输出路径，使用默认路径
            if not output_path:
                project_name = PathUtils.get_filename(project_model.project_path) or "project"
                filename = f"{project_name}_structure_{Utils.get_timestamp()}.md"
                output_path = PathUtils.join_path("exports", filename)
            
            # 写入文件
            success = Utils.write_file_content(output_path, markdown_content)
            
            if success:
                return output_path, "Markdown导出成功"
            else:
                return None, "Markdown导出失败"
                
        except Exception as e:
            return None, f"Markdown导出失败: {str(e)}"
    
    def _build_markdown_content(self, project_model):
        """构建Markdown内容"""
        lines = []
        
        # 标题
        project_name = PathUtils.get_filename(project_model.project_path) or "项目"
        lines.append(f"# {project_name} 工程结构文档")
        lines.append("")
        
        # 基本信息
        lines.append("## 基本信息")
        lines.append("")
        lines.append(f"- **项目路径**: `{project_model.project_path}`")
        lines.append(f"- **导出时间**: {Utils.format_datetime()}")
        lines.append(f"- **使用.gitignore**: {'是' if project_model.use_gitignore else '否'}")
        lines.append("")
        
        # 过滤条件
        if project_model.filter_conditions:
            lines.append("## 过滤条件")
            lines.append("")
            for condition in project_model.filter_conditions:
                lines.append(f"- `{condition}`")
            lines.append("")
        
        # 目录结构
        lines.append("## 目录结构")
        lines.append("")
        
        if project_model.root_node:
            self._build_tree_markdown(project_model.root_node, lines, 0)
        else:
            lines.append("无数据")
        
        return "\n".join(lines)
    
    def _build_tree_markdown(self, node, lines, depth):
        """构建树状结构的Markdown"""
        # 缩进
        indent = "  " * depth
        
        # 图标
        icon = "📁" if node.is_directory else "📄"
        
        # 节点名称
        name = node.name
        
        # 描述
        description = f" - {node.description}" if node.description else ""
        
        # 添加行
        lines.append(f"{indent}- {icon} **{name}**{description}")
        
        # 递归处理子节点
        for child in node.children:
            self._build_tree_markdown(child, lines, depth + 1)
    
    def export_to_cursor_rules(self, project_model, output_path=None):
        """导出为Cursor rules格式"""
        try:
            # 构建rules内容
            rules_content = self._build_cursor_rules_content(project_model)
            
            # 如果没有指定输出路径，使用默认路径
            if not output_path:
                filename = f".cursorrules"
                output_path = PathUtils.join_path("exports", filename)
            
            # 写入文件
            success = Utils.write_file_content(output_path, rules_content)
            
            if success:
                return output_path, "Cursor rules导出成功"
            else:
                return None, "Cursor rules导出失败"
                
        except Exception as e:
            return None, f"Cursor rules导出失败: {str(e)}"
    
    def _build_cursor_rules_content(self, project_model):
        """构建Cursor rules内容"""
        lines = []
        
        project_name = PathUtils.get_filename(project_model.project_path) or "项目"
        
        # 项目概述
        lines.append(f"# {project_name} 项目规则")
        lines.append("")
        lines.append("## 项目结构说明")
        lines.append("")
        
        if project_model.root_node:
            self._build_cursor_rules_structure(project_model.root_node, lines, 0)
        
        lines.append("")
        lines.append("## 开发规范")
        lines.append("")
        lines.append("- 遵循项目现有的代码结构和命名规范")
        lines.append("- 新增文件时请放在合适的目录下")
        lines.append("- 修改文件时请保持原有的功能职责清晰")
        lines.append("")
        
        return "\n".join(lines)
    
    def _build_cursor_rules_structure(self, node, lines, depth):
        """构建Cursor rules的结构说明"""
        indent = "  " * depth
        
        if node.is_directory:
            lines.append(f"{indent}- `{node.name}/`: {node.description or '目录'}")
        else:
            lines.append(f"{indent}- `{node.name}`: {node.description or '文件'}")
        
        for child in node.children:
            self._build_cursor_rules_structure(child, lines, depth + 1)