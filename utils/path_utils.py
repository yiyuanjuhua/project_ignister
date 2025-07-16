"""
路径处理工具
"""

import os
import platform

class PathUtils:
    """路径处理工具类"""
    
    @staticmethod
    def normalize_path(path):
        """标准化路径"""
        return os.path.normpath(os.path.abspath(path))
    
    @staticmethod
    def get_relative_path(base_path, target_path):
        """获取相对路径"""
        try:
            return os.path.relpath(target_path, base_path)
        except ValueError:
            return target_path
    
    @staticmethod
    def is_valid_directory(path):
        """检查是否为有效目录"""
        return os.path.exists(path) and os.path.isdir(path)
    
    @staticmethod
    def get_file_extension(path):
        """获取文件扩展名"""
        return os.path.splitext(path)[1].lower()
    
    @staticmethod
    def get_filename(path):
        """获取文件名"""
        return os.path.basename(path)
    
    @staticmethod
    def get_parent_directory(path):
        """获取父目录"""
        return os.path.dirname(path)
    
    @staticmethod
    def join_path(*args):
        """连接路径"""
        return os.path.join(*args)
    
    @staticmethod
    def get_system_separator():
        """获取系统路径分隔符"""
        return os.sep
    
    @staticmethod
    def is_windows():
        """检查是否为Windows系统"""
        return platform.system().lower() == 'windows'
    
    @staticmethod
    def is_linux():
        """检查是否为Linux系统"""
        return platform.system().lower() == 'linux'