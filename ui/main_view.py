"""
主界面
"""

import tkinter as tk
from tkinter import ttk

class MainView:
    """主界面类"""
    
    def __init__(self, root, on_project_scan_clicked):
        self.root = root
        self.on_project_scan_clicked = on_project_scan_clicked
        
        self.setup_ui()
    
    def setup_ui(self):
        """设置用户界面"""
        # 设置窗口标题和大小
        self.root.title("工程结构分析工具")
        self.root.geometry("500x400")
        self.root.resizable(True, True)
        
        # 居中窗口
        self.center_window()
        
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # 标题
        title_label = ttk.Label(
            main_frame, 
            text="工程结构分析工具", 
            font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, pady=(0, 20))
        
        # 描述文本
        description_text = """
这是一个用于分析工程目录结构的工具。

主要功能：
• 读取指定目录下的文件结构
• 支持过滤条件配置（包括.gitignore）
• 以树状结构展示文件目录
• 为每个文件/目录添加功能描述
• 导出为Markdown、JSON或Cursor rules格式

请选择要使用的功能：
        """
        
        description_label = ttk.Label(
            main_frame, 
            text=description_text.strip(),
            justify=tk.LEFT,
            font=("Arial", 10)
        )
        description_label.grid(row=1, column=0, pady=(0, 30), sticky=(tk.W, tk.E))
        
        # 功能按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, pady=(0, 20))
        button_frame.columnconfigure(0, weight=1)
        
        # 工程结构读取按钮
        self.scan_button = ttk.Button(
            button_frame,
            text="工程结构读取",
            command=self.on_scan_button_click,
            width=20
        )
        self.scan_button.grid(row=0, column=0, pady=5)
        
        # 预留其他功能按钮的位置
        placeholder_label = ttk.Label(
            button_frame,
            text="更多功能敬请期待...",
            font=("Arial", 9),
            foreground="gray"
        )
        placeholder_label.grid(row=1, column=0, pady=20)
        
        # 底部信息
        info_frame = ttk.Frame(main_frame)
        info_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(20, 0))
        info_frame.columnconfigure(0, weight=1)
        
        version_label = ttk.Label(
            info_frame,
            text="版本: 1.0.0  |  支持: Windows & Linux",
            font=("Arial", 8),
            foreground="gray"
        )
        version_label.grid(row=0, column=0)
        
        # 快捷键提示
        shortcut_label = ttk.Label(
            info_frame,
            text="快捷键: Ctrl+Q 退出",
            font=("Arial", 8),
            foreground="gray"
        )
        shortcut_label.grid(row=1, column=0)
        
        # 绑定快捷键
        self.root.bind('<Control-q>', lambda e: self.root.quit())
        
        # 设置焦点
        self.scan_button.focus()
    
    def center_window(self):
        """居中显示窗口"""
        self.root.update_idletasks()
        
        # 获取窗口尺寸
        window_width = self.root.winfo_reqwidth()
        window_height = self.root.winfo_reqheight()
        
        # 获取屏幕尺寸
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # 计算居中位置
        pos_x = (screen_width // 2) - (window_width // 2)
        pos_y = (screen_height // 2) - (window_height // 2)
        
        # 设置窗口位置
        self.root.geometry(f"{window_width}x{window_height}+{pos_x}+{pos_y}")
    
    def on_scan_button_click(self):
        """处理扫描按钮点击事件"""
        if self.on_project_scan_clicked:
            self.on_project_scan_clicked()
    
    def show_message(self, title, message, message_type="info"):
        """显示消息对话框"""
        from tkinter import messagebox
        
        if message_type == "info":
            messagebox.showinfo(title, message)
        elif message_type == "warning":
            messagebox.showwarning(title, message)
        elif message_type == "error":
            messagebox.showerror(title, message)