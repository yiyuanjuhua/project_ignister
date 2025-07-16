"""
过滤逻辑引擎
"""

import os
import fnmatch
import re
from utils.path_utils import PathUtils
from utils.utils import Utils

class FilterEngine:
    """文件过滤引擎"""
    
    def __init__(self):
        self.filter_patterns = []
    
    def load_gitignore(self, project_path):
        """加载.gitignore文件的过滤规则"""
        gitignore_path = PathUtils.join_path(project_path, '.gitignore')
        patterns = []
        
        if os.path.exists(gitignore_path):
            content = Utils.read_file_content(gitignore_path)
            for line in content.splitlines():
                line = line.strip()
                # 忽略注释和空行
                if line and not line.startswith('#'):
                    patterns.append(line)
        
        return patterns
    
    def set_filter_patterns(self, patterns):
        """设置过滤模式"""
        self.filter_patterns = patterns or []
    
    def should_exclude(self, file_path, base_path):
        """判断文件是否应该被排除"""
        # 获取相对路径
        rel_path = PathUtils.get_relative_path(base_path, file_path)
        filename = PathUtils.get_filename(file_path)
        
        # 检查每个过滤模式
        for pattern in self.filter_patterns:
            if self._match_pattern(pattern, rel_path, filename):
                return True
        
        return False
    
    def _match_pattern(self, pattern, rel_path, filename):
        """匹配单个模式"""
        # 清理模式
        pattern = pattern.strip()
        if not pattern:
            return False
        
        # 处理否定模式（以!开头）
        negate = False
        if pattern.startswith('!'):
            negate = True
            pattern = pattern[1:]
        
        # 处理目录模式（以/结尾）
        is_dir_pattern = pattern.endswith('/')
        if is_dir_pattern:
            pattern = pattern[:-1]
        
        # 匹配逻辑
        matched = False
        
        # 绝对路径模式（以/开头）
        if pattern.startswith('/'):
            pattern = pattern[1:]
            matched = fnmatch.fnmatch(rel_path, pattern)
        else:
            # 相对路径模式
            # 检查文件名匹配
            if fnmatch.fnmatch(filename, pattern):
                matched = True
            # 检查路径匹配
            elif fnmatch.fnmatch(rel_path, pattern):
                matched = True
            # 检查路径中任意部分匹配
            elif fnmatch.fnmatch(rel_path, f"*/{pattern}") or fnmatch.fnmatch(rel_path, f"*/{pattern}/*"):
                matched = True
        
        # 应用否定逻辑
        return not matched if negate else matched
    
    def filter_file_list(self, file_list, base_path):
        """过滤文件列表"""
        filtered_list = []
        
        for file_path in file_list:
            if not self.should_exclude(file_path, base_path):
                filtered_list.append(file_path)
        
        return filtered_list
    
    def get_common_ignore_patterns(self):
        """获取常见的忽略模式"""
        return [
            "*.pyc",
            "__pycache__/",
            "*.pyo",
            "*.pyd",
            ".Python",
            "build/",
            "develop-eggs/",
            "dist/",
            "downloads/",
            "eggs/",
            ".eggs/",
            "lib/",
            "lib64/",
            "parts/",
            "sdist/",
            "var/",
            "wheels/",
            "*.egg-info/",
            ".installed.cfg",
            "*.egg",
            ".git/",
            ".svn/",
            ".hg/",
            ".idea/",
            ".vscode/",
            "*.log",
            "*.tmp",
            "*.temp",
            "node_modules/",
            "*.min.js",
            "*.min.css"
        ]