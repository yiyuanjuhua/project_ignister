"""
树节点数据结构定义
"""

class TreeNode:
    """树节点类，用于表示文件系统中的文件或目录"""
    
    def __init__(self, name, path, is_directory=False, parent=None):
        self.name = name  # 文件/目录名
        self.path = path  # 完整路径
        self.is_directory = is_directory  # 是否为目录
        self.parent = parent  # 父节点
        self.children = []  # 子节点列表
        self.description = ""  # 用户填写的功能描述
        
    def add_child(self, child):
        """添加子节点"""
        child.parent = self
        self.children.append(child)
        
    def get_full_path(self):
        """获取完整路径"""
        return self.path
        
    def to_dict(self):
        """转换为字典格式，用于导出"""
        return {
            'name': self.name,
            'path': self.path,
            'is_directory': self.is_directory,
            'description': self.description,
            'children': [child.to_dict() for child in self.children]
        }