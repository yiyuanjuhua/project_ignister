"""
文件处理核心模块
"""

import os
from data.tree_node import TreeNode
from logic.filter_engine import FilterEngine
from utils.path_utils import PathUtils

class FileProcessor:
    """文件处理核心类"""
    
    def __init__(self):
        self.filter_engine = FilterEngine()
    
    def scan_directory(self, project_path, filter_patterns=None, use_gitignore=False):
        """
        扫描目录并构建文件树
        
        Args:
            project_path: 项目根目录路径
            filter_patterns: 过滤模式列表
            use_gitignore: 是否使用.gitignore
            
        Returns:
            TreeNode: 根节点
        """
        # 标准化路径
        project_path = PathUtils.normalize_path(project_path)
        
        if not PathUtils.is_valid_directory(project_path):
            raise ValueError(f"无效的目录路径: {project_path}")
        
        # 设置过滤条件
        all_patterns = filter_patterns or []
        
        # 如果使用.gitignore，加载其规则
        if use_gitignore:
            gitignore_patterns = self.filter_engine.load_gitignore(project_path)
            all_patterns.extend(gitignore_patterns)
        
        self.filter_engine.set_filter_patterns(all_patterns)
        
        # 创建根节点
        root_name = PathUtils.get_filename(project_path) or project_path
        root_node = TreeNode(root_name, project_path, is_directory=True)
        
        # 递归扫描目录
        self._scan_recursive(project_path, root_node, project_path)
        
        return root_node
    
    def _scan_recursive(self, current_path, parent_node, base_path):
        """递归扫描目录"""
        try:
            # 获取目录下的所有项目
            items = os.listdir(current_path)
            items.sort()  # 排序便于展示
            
            for item in items:
                item_path = PathUtils.join_path(current_path, item)
                
                # 检查是否应该排除
                if self.filter_engine.should_exclude(item_path, base_path):
                    continue
                
                # 判断是文件还是目录
                is_directory = os.path.isdir(item_path)
                
                # 创建节点
                node = TreeNode(item, item_path, is_directory=is_directory)
                parent_node.add_child(node)
                
                # 如果是目录，递归扫描
                if is_directory:
                    self._scan_recursive(item_path, node, base_path)
                    
        except PermissionError:
            # 跳过没有权限的目录
            print(f"跳过无权限访问的目录: {current_path}")
        except Exception as e:
            print(f"扫描目录时出错: {current_path}, 错误: {str(e)}")
    
    def get_file_statistics(self, root_node):
        """获取文件统计信息"""
        stats = {
            'total_files': 0,
            'total_directories': 0,
            'file_types': {},
            'total_size': 0
        }
        
        self._collect_statistics(root_node, stats)
        return stats
    
    def _collect_statistics(self, node, stats):
        """收集统计信息"""
        if node.is_directory:
            stats['total_directories'] += 1
            # 递归处理子节点
            for child in node.children:
                self._collect_statistics(child, stats)
        else:
            stats['total_files'] += 1
            
            # 获取文件扩展名
            ext = PathUtils.get_file_extension(node.path)
            if ext:
                stats['file_types'][ext] = stats['file_types'].get(ext, 0) + 1
            else:
                stats['file_types']['无扩展名'] = stats['file_types'].get('无扩展名', 0) + 1
            
            # 获取文件大小
            try:
                file_size = os.path.getsize(node.path)
                stats['total_size'] += file_size
            except OSError:
                pass
    
    def search_in_tree(self, root_node, keyword):
        """在文件树中搜索"""
        results = []
        self._search_recursive(root_node, keyword.lower(), results)
        return results
    
    def _search_recursive(self, node, keyword, results):
        """递归搜索"""
        if keyword in node.name.lower():
            results.append(node)
        
        for child in node.children:
            self._search_recursive(child, keyword, results)
    
    def get_tree_depth(self, root_node):
        """获取树的最大深度"""
        if not root_node.children:
            return 1
        
        max_depth = 0
        for child in root_node.children:
            child_depth = self.get_tree_depth(child)
            max_depth = max(max_depth, child_depth)
        
        return max_depth + 1
    
    def get_node_count(self, root_node):
        """获取节点总数"""
        count = 1  # 包含根节点
        for child in root_node.children:
            count += self.get_node_count(child)
        return count