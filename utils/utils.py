"""
通用工具函数
"""

import os
import json
from datetime import datetime

class Utils:
    """通用工具类"""
    
    @staticmethod
    def read_file_content(file_path, encoding='utf-8'):
        """读取文件内容"""
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                return f.read()
        except Exception as e:
            print(f"读取文件失败: {file_path}, 错误: {str(e)}")
            return ""
    
    @staticmethod
    def write_file_content(file_path, content, encoding='utf-8'):
        """写入文件内容"""
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding=encoding) as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"写入文件失败: {file_path}, 错误: {str(e)}")
            return False
    
    @staticmethod
    def read_json_file(file_path):
        """读取JSON文件"""
        try:
            content = Utils.read_file_content(file_path)
            return json.loads(content) if content else {}
        except json.JSONDecodeError as e:
            print(f"JSON解析失败: {file_path}, 错误: {str(e)}")
            return {}
    
    @staticmethod
    def write_json_file(file_path, data):
        """写入JSON文件"""
        try:
            content = json.dumps(data, ensure_ascii=False, indent=2)
            return Utils.write_file_content(file_path, content)
        except Exception as e:
            print(f"写入JSON文件失败: {file_path}, 错误: {str(e)}")
            return False
    
    @staticmethod
    def get_timestamp():
        """获取当前时间戳字符串"""
        return datetime.now().strftime("%Y%m%d_%H%M%S")
    
    @staticmethod
    def format_datetime(timestamp=None):
        """格式化日期时间"""
        if timestamp is None:
            timestamp = datetime.now()
        return timestamp.strftime("%Y-%m-%d %H:%M:%S")
    
    @staticmethod
    def sanitize_filename(filename):
        """清理文件名中的非法字符"""
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        return filename
    
    @staticmethod
    def format_file_size(size_bytes):
        """格式化文件大小"""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        elif size_bytes < 1024 * 1024 * 1024:
            return f"{size_bytes / (1024 * 1024):.1f} MB"
        else:
            return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"