"""
工程数据模型
"""

from data.tree_node import TreeNode

class ProjectModel:
    """工程数据模型类"""
    
    def __init__(self):
        self.project_path = ""  # 工程根目录路径
        self.root_node = None  # 根节点
        self.filter_conditions = []  # 过滤条件列表
        self.use_gitignore = False  # 是否使用.gitignore
        
    def set_project_path(self, path):
        """设置工程路径"""
        self.project_path = path
        
    def set_root_node(self, root_node):
        """设置根节点"""
        self.root_node = root_node
        
    def add_filter_condition(self, condition):
        """添加过滤条件"""
        if condition and condition not in self.filter_conditions:
            self.filter_conditions.append(condition)
            
    def remove_filter_condition(self, condition):
        """移除过滤条件"""
        if condition in self.filter_conditions:
            self.filter_conditions.remove(condition)
            
    def clear_filter_conditions(self):
        """清空过滤条件"""
        self.filter_conditions.clear()
        
    def set_use_gitignore(self, use_gitignore):
        """设置是否使用.gitignore"""
        self.use_gitignore = use_gitignore
        
    def to_dict(self):
        """转换为字典格式"""
        return {
            'project_path': self.project_path,
            'filter_conditions': self.filter_conditions,
            'use_gitignore': self.use_gitignore,
            'structure': self.root_node.to_dict() if self.root_node else None
        }