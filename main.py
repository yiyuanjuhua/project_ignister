#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工程结构分析工具 - 主程序入口
"""

import tkinter as tk
from tkinter import messagebox
import os
import sys
import threading

# 添加当前目录到路径，以便导入模块
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# 导入应用模块
from ui.main_view import MainView
from ui.config_view import ConfigView
from ui.project_view import ProjectView
from data.project_model import ProjectModel
from logic.file_processor import FileProcessor


class ProjectAnalyzerApp:
    """工程分析工具应用主类"""
    
    def __init__(self):
        # 创建主窗口
        self.root = tk.Tk()
        
        # 设置应用程序属性
        self.setup_app_properties()
        
        # 初始化数据模型
        self.project_model = ProjectModel()
        self.file_processor = FileProcessor()
        
        # 当前视图
        self.current_view = None
        
        # 创建主界面
        self.show_main_view()
    
    def setup_app_properties(self):
        """设置应用程序属性"""
        # 设置窗口图标（如果有的话）
        try:
            # 这里可以设置应用图标
            # self.root.iconbitmap('icon.ico')
            pass
        except:
            pass
        
        # 设置窗口关闭行为
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # 设置最小窗口大小
        self.root.minsize(400, 300)
        
        # 配置样式
        self.setup_styles()
    
    def setup_styles(self):
        """设置UI样式"""
        try:
            # 尝试设置现代主题
            style = tk.ttk.Style()
            available_themes = style.theme_names()
            
            # 优先选择现代主题
            preferred_themes = ['clam', 'alt', 'default']
            
            for theme in preferred_themes:
                if theme in available_themes:
                    style.theme_use(theme)
                    break
        except Exception as e:
            print(f"设置主题失败: {e}")
    
    def show_main_view(self):
        """显示主界面"""
        self.current_view = MainView(
            self.root, 
            on_project_scan_clicked=self.show_config_view
        )
    
    def show_config_view(self):
        """显示配置界面"""
        self.current_view = ConfigView(
            self.root,
            on_start_scan=self.start_project_scan,
            on_back_to_main=self.show_main_view
        )
    
    def show_project_view(self):
        """显示工程运维界面"""
        self.current_view = ProjectView(
            self.root,
            self.project_model,
            on_back_to_config=self.show_config_view
        )
    
    def start_project_scan(self, project_path, filter_conditions, use_gitignore):
        """开始项目扫描"""
        try:
            # 显示进度对话框
            progress_dialog = ProgressDialog(self.root, "正在扫描项目...")
            
            # 在后台线程中执行扫描
            def scan_task():
                try:
                    # 设置项目模型
                    self.project_model.set_project_path(project_path)
                    self.project_model.filter_conditions = filter_conditions
                    self.project_model.set_use_gitignore(use_gitignore)
                    
                    # 扫描目录
                    root_node = self.file_processor.scan_directory(
                        project_path, 
                        filter_conditions, 
                        use_gitignore
                    )
                    
                    self.project_model.set_root_node(root_node)
                    
                    # 在主线程中更新UI
                    self.root.after(0, lambda: self.on_scan_completed(progress_dialog))
                    
                except Exception as e:
                    # 在主线程中显示错误
                    self.root.after(0, lambda: self.on_scan_error(progress_dialog, str(e)))
            
            # 启动后台线程
            thread = threading.Thread(target=scan_task)
            thread.daemon = True
            thread.start()
            
        except Exception as e:
            messagebox.showerror("错误", f"启动扫描失败: {str(e)}")
    
    def on_scan_completed(self, progress_dialog):
        """扫描完成回调"""
        try:
            progress_dialog.close()
            
            # 显示扫描结果统计
            stats = self.file_processor.get_file_statistics(self.project_model.root_node)
            message = f"扫描完成！\n\n统计信息:\n"
            message += f"- 目录: {stats['total_directories']} 个\n"
            message += f"- 文件: {stats['total_files']} 个\n"
            message += f"- 总大小: {self.format_file_size(stats['total_size'])}\n\n"
            message += "点击确定查看详细结构。"
            
            messagebox.showinfo("扫描完成", message)
            
            # 切换到项目视图
            self.show_project_view()
            
        except Exception as e:
            messagebox.showerror("错误", f"显示扫描结果失败: {str(e)}")
    
    def on_scan_error(self, progress_dialog, error_message):
        """扫描出错回调"""
        progress_dialog.close()
        messagebox.showerror("扫描失败", f"扫描项目时出现错误:\n{error_message}")
    
    def format_file_size(self, size_bytes):
        """格式化文件大小"""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        elif size_bytes < 1024 * 1024 * 1024:
            return f"{size_bytes / (1024 * 1024):.1f} MB"
        else:
            return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"
    
    def on_closing(self):
        """处理窗口关闭事件"""
        if messagebox.askokcancel("退出", "确定要退出工程结构分析工具吗？"):
            self.root.destroy()
    
    def run(self):
        """运行应用程序"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("\n程序被用户中断")
        except Exception as e:
            print(f"程序运行出错: {e}")
            messagebox.showerror("错误", f"程序运行出错: {str(e)}")


class ProgressDialog:
    """进度对话框"""
    
    def __init__(self, parent, message="正在处理..."):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("请稍候")
        self.dialog.geometry("300x100")
        self.dialog.resizable(False, False)
        
        # 设置模态
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # 居中显示
        self.center_dialog(parent)
        
        # 创建界面
        self.setup_ui(message)
        
        # 禁用关闭按钮
        self.dialog.protocol("WM_DELETE_WINDOW", lambda: None)
    
    def center_dialog(self, parent):
        """居中显示对话框"""
        parent.update_idletasks()
        
        # 获取父窗口位置和大小
        parent_x = parent.winfo_x()
        parent_y = parent.winfo_y()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()
        
        # 获取对话框大小
        dialog_width = 300
        dialog_height = 100
        
        # 计算居中位置
        x = parent_x + (parent_width - dialog_width) // 2
        y = parent_y + (parent_height - dialog_height) // 2
        
        self.dialog.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")
    
    def setup_ui(self, message):
        """设置对话框界面"""
        # 主框架
        main_frame = tk.ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 消息标签
        label = tk.ttk.Label(main_frame, text=message, font=("Arial", 10))
        label.pack(pady=(0, 10))
        
        # 进度条
        self.progress = tk.ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=(0, 10))
        self.progress.start(10)
    
    def close(self):
        """关闭对话框"""
        try:
            self.progress.stop()
            self.dialog.grab_release()
            self.dialog.destroy()
        except:
            pass


def main():
    """主函数"""
    try:
        # 检查Python版本
        if sys.version_info < (3, 6):
            print("错误: 需要Python 3.6或更高版本")
            sys.exit(1)
        
        # 创建并运行应用
        app = ProjectAnalyzerApp()
        app.run()
        
    except Exception as e:
        print(f"程序启动失败: {e}")
        # 尝试显示错误对话框
        try:
            root = tk.Tk()
            root.withdraw()  # 隐藏主窗口
            messagebox.showerror("启动失败", f"程序启动失败:\n{str(e)}")
        except:
            pass
        sys.exit(1)


if __name__ == "__main__":
    main()