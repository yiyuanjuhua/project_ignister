"""
配置界面
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os

class ConfigView:
    """配置界面类"""
    
    def __init__(self, root, on_start_scan, on_back_to_main):
        self.root = root
        self.on_start_scan = on_start_scan
        self.on_back_to_main = on_back_to_main
        
        # 配置变量
        self.project_path = tk.StringVar()
        self.use_gitignore = tk.BooleanVar(value=False)
        self.filter_conditions = []
        
        self.setup_ui()
    
    def setup_ui(self):
        """设置用户界面"""
        # 清空窗口
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # 设置窗口标题
        self.root.title("工程结构读取 - 配置")
        self.root.geometry("700x600")
        
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        row = 0
        
        # 标题
        title_label = ttk.Label(
            main_frame, 
            text="工程结构读取配置", 
            font=("Arial", 14, "bold")
        )
        title_label.grid(row=row, column=0, columnspan=3, pady=(0, 20))
        row += 1
        
        # 工程目录选择
        ttk.Label(main_frame, text="工程目录:").grid(row=row, column=0, sticky=tk.W, pady=5)
        
        path_frame = ttk.Frame(main_frame)
        path_frame.grid(row=row, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        path_frame.columnconfigure(0, weight=1)
        
        self.path_entry = ttk.Entry(path_frame, textvariable=self.project_path, width=50)
        self.path_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        browse_button = ttk.Button(path_frame, text="浏览...", command=self.browse_directory)
        browse_button.grid(row=0, column=1)
        
        row += 1
        
        # .gitignore 选项
        gitignore_frame = ttk.Frame(main_frame)
        gitignore_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        self.gitignore_checkbox = ttk.Checkbutton(
            gitignore_frame,
            text="关注 .gitignore 文件",
            variable=self.use_gitignore,
            command=self.on_gitignore_changed
        )
        self.gitignore_checkbox.grid(row=0, column=0, sticky=tk.W)
        
        row += 1
        
        # 过滤条件
        ttk.Label(main_frame, text="过滤条件:").grid(row=row, column=0, sticky=(tk.W, tk.N), pady=5)
        
        # 过滤条件框架
        filter_frame = ttk.Frame(main_frame)
        filter_frame.grid(row=row, column=1, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        filter_frame.columnconfigure(0, weight=1)
        filter_frame.rowconfigure(0, weight=1)
        
        # 创建滚动文本框
        self.create_filter_widget(filter_frame)
        
        # 配置主框架的行权重
        main_frame.rowconfigure(row, weight=1)
        row += 1
        
        # 按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=row, column=0, columnspan=3, pady=20, sticky=(tk.W, tk.E))
        button_frame.columnconfigure(1, weight=1)
        
        # 返回按钮
        back_button = ttk.Button(button_frame, text="返回", command=self.on_back_click)
        back_button.grid(row=0, column=0, padx=(0, 10))
        
        # 开始按钮
        self.start_button = ttk.Button(
            button_frame, 
            text="开始扫描", 
            command=self.on_start_click,
            style="Accent.TButton"
        )
        self.start_button.grid(row=0, column=2)
        
        # 设置默认值
        self.load_default_filters()
    
    def create_filter_widget(self, parent):
        """创建过滤条件输入控件"""
        # 创建带滚动条的文本框
        text_frame = ttk.Frame(parent)
        text_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        
        # 文本框
        self.filter_text = tk.Text(
            text_frame, 
            height=15, 
            width=50,
            wrap=tk.NONE,
            font=("Consolas", 9)
        )
        self.filter_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 垂直滚动条
        v_scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.filter_text.yview)
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.filter_text.configure(yscrollcommand=v_scrollbar.set)
        
        # 水平滚动条
        h_scrollbar = ttk.Scrollbar(text_frame, orient=tk.HORIZONTAL, command=self.filter_text.xview)
        h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        self.filter_text.configure(xscrollcommand=h_scrollbar.set)
        
        # 说明标签
        help_text = "每行一个过滤条件，支持通配符(*、?)。例如:\n*.pyc\n__pycache__/\n*.log"
        help_label = ttk.Label(parent, text=help_text, font=("Arial", 8), foreground="gray")
        help_label.grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
    
    def browse_directory(self):
        """浏览目录"""
        directory = filedialog.askdirectory(
            title="选择工程目录",
            initialdir=self.project_path.get() or os.getcwd()
        )
        
        if directory:
            self.project_path.set(directory)
            # 如果选择了目录且勾选了gitignore，自动加载gitignore
            if self.use_gitignore.get():
                self.load_gitignore_filters()
    
    def on_gitignore_changed(self):
        """处理gitignore选项变化"""
        if self.use_gitignore.get() and self.project_path.get():
            self.load_gitignore_filters()
        elif not self.use_gitignore.get():
            # 如果取消勾选，移除gitignore相关的过滤条件
            self.load_default_filters()
    
    def load_gitignore_filters(self):
        """加载.gitignore过滤条件"""
        project_path = self.project_path.get()
        if not project_path:
            return
        
        gitignore_path = os.path.join(project_path, '.gitignore')
        
        if os.path.exists(gitignore_path):
            try:
                with open(gitignore_path, 'r', encoding='utf-8') as f:
                    gitignore_content = f.read()
                
                # 解析gitignore内容
                gitignore_patterns = []
                for line in gitignore_content.splitlines():
                    line = line.strip()
                    if line and not line.startswith('#'):
                        gitignore_patterns.append(line)
                
                # 合并默认过滤条件和gitignore条件
                default_filters = self.get_default_filters()
                all_filters = default_filters + ["# .gitignore 规则:"] + gitignore_patterns
                
                # 更新文本框
                self.filter_text.delete(1.0, tk.END)
                self.filter_text.insert(1.0, "\n".join(all_filters))
                
                messagebox.showinfo("成功", f"已加载 .gitignore 文件，共 {len(gitignore_patterns)} 条规则")
                
            except Exception as e:
                messagebox.showerror("错误", f"读取 .gitignore 文件失败: {str(e)}")
        else:
            messagebox.showwarning("提示", "在指定目录中未找到 .gitignore 文件")
    
    def load_default_filters(self):
        """加载默认过滤条件"""
        default_filters = self.get_default_filters()
        self.filter_text.delete(1.0, tk.END)
        self.filter_text.insert(1.0, "\n".join(default_filters))
    
    def get_default_filters(self):
        """获取默认过滤条件"""
        return [
            "# Python 相关",
            "*.pyc",
            "__pycache__/",
            "*.pyo",
            "*.pyd",
            ".Python",
            "build/",
            "dist/",
            "*.egg-info/",
            "",
            "# 版本控制",
            ".git/",
            ".svn/",
            ".hg/",
            "",
            "# IDE",
            ".idea/",
            ".vscode/",
            "",
            "# 日志和临时文件",
            "*.log",
            "*.tmp",
            "*.temp",
            "",
            "# Node.js",
            "node_modules/",
            "*.min.js",
            "*.min.css"
        ]
    
    def get_filter_conditions(self):
        """获取过滤条件列表"""
        content = self.filter_text.get(1.0, tk.END)
        conditions = []
        
        for line in content.splitlines():
            line = line.strip()
            # 忽略注释和空行
            if line and not line.startswith('#'):
                conditions.append(line)
        
        return conditions
    
    def on_start_click(self):
        """处理开始按钮点击"""
        project_path = self.project_path.get().strip()
        
        if not project_path:
            messagebox.showerror("错误", "请选择工程目录")
            return
        
        if not os.path.exists(project_path):
            messagebox.showerror("错误", "指定的工程目录不存在")
            return
        
        if not os.path.isdir(project_path):
            messagebox.showerror("错误", "指定的路径不是目录")
            return
        
        # 获取配置
        filter_conditions = self.get_filter_conditions()
        use_gitignore = self.use_gitignore.get()
        
        # 调用回调函数
        if self.on_start_scan:
            self.on_start_scan(project_path, filter_conditions, use_gitignore)
    
    def on_back_click(self):
        """处理返回按钮点击"""
        if self.on_back_to_main:
            self.on_back_to_main()