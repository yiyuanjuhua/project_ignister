"""
工程运维界面
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from logic.exporter import Exporter

class ProjectView:
    """工程运维界面类"""
    
    def __init__(self, root, project_model, on_back_to_config):
        self.root = root
        self.project_model = project_model
        self.on_back_to_config = on_back_to_config
        self.exporter = Exporter()
        
        # 用于存储所有节点的Entry引用
        self.node_entries = {}
        
        self.setup_ui()
    
    def setup_ui(self):
        """设置用户界面"""
        # 清空窗口
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # 设置窗口标题和大小
        self.root.title("工程运维 - 结构展示")
        self.root.geometry("1000x700")
        
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # 顶部信息框架
        self.create_info_panel(main_frame)
        
        # 主要内容框架
        content_frame = ttk.Frame(main_frame)
        content_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        content_frame.columnconfigure(0, weight=1)
        content_frame.rowconfigure(0, weight=1)
        
        # 创建树形视图
        self.create_tree_view(content_frame)
        
        # 底部按钮框架
        self.create_button_panel(main_frame)
    
    def create_info_panel(self, parent):
        """创建信息面板"""
        info_frame = ttk.LabelFrame(parent, text="项目信息", padding="10")
        info_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        info_frame.columnconfigure(1, weight=1)
        
        # 项目路径
        ttk.Label(info_frame, text="项目路径:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        path_label = ttk.Label(info_frame, text=self.project_model.project_path, 
                              foreground="blue", font=("Arial", 9))
        path_label.grid(row=0, column=1, sticky=tk.W)
        
        # 过滤条件数量
        filter_count = len(self.project_model.filter_conditions)
        ttk.Label(info_frame, text="过滤条件:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5))
        ttk.Label(info_frame, text=f"{filter_count} 条").grid(row=1, column=1, sticky=tk.W)
        
        # 使用gitignore
        ttk.Label(info_frame, text="使用.gitignore:").grid(row=2, column=0, sticky=tk.W, padx=(0, 5))
        gitignore_text = "是" if self.project_model.use_gitignore else "否"
        ttk.Label(info_frame, text=gitignore_text).grid(row=2, column=1, sticky=tk.W)
        
        # 统计信息
        if self.project_model.root_node:
            stats = self.get_statistics()
            ttk.Label(info_frame, text="统计:").grid(row=3, column=0, sticky=tk.W, padx=(0, 5))
            stats_text = f"目录 {stats['directories']} 个，文件 {stats['files']} 个"
            ttk.Label(info_frame, text=stats_text).grid(row=3, column=1, sticky=tk.W)
    
    def create_tree_view(self, parent):
        """创建树形视图"""
        # 创建框架用于放置树形视图和滚动条
        tree_frame = ttk.Frame(parent)
        tree_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)
        
        # 创建Treeview
        self.tree = ttk.Treeview(tree_frame, columns=('description',), show='tree headings')
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置列
        self.tree.heading('#0', text='文件/目录结构', anchor=tk.W)
        self.tree.heading('description', text='功能描述', anchor=tk.W)
        
        self.tree.column('#0', width=400, minwidth=300)
        self.tree.column('description', width=500, minwidth=200)
        
        # 垂直滚动条
        v_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.tree.configure(yscrollcommand=v_scrollbar.set)
        
        # 水平滚动条
        h_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        self.tree.configure(xscrollcommand=h_scrollbar.set)
        
        # 填充树形数据
        self.populate_tree()
        
        # 绑定双击事件
        self.tree.bind('<Double-1>', self.on_item_double_click)
        
        # 绑定右键菜单
        self.tree.bind('<Button-3>', self.show_context_menu)
    
    def create_button_panel(self, parent):
        """创建按钮面板"""
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=10)
        button_frame.columnconfigure(2, weight=1)
        
        # 返回按钮
        back_button = ttk.Button(button_frame, text="返回配置", command=self.on_back_click)
        back_button.grid(row=0, column=0, padx=(0, 10))
        
        # 刷新按钮
        refresh_button = ttk.Button(button_frame, text="刷新", command=self.refresh_tree)
        refresh_button.grid(row=0, column=1, padx=(0, 10))
        
        # 导出按钮
        export_frame = ttk.Frame(button_frame)
        export_frame.grid(row=0, column=3)
        
        export_md_button = ttk.Button(export_frame, text="导出 Markdown", 
                                     command=self.export_markdown)
        export_md_button.grid(row=0, column=0, padx=(0, 5))
        
        export_json_button = ttk.Button(export_frame, text="导出 JSON", 
                                       command=self.export_json)
        export_json_button.grid(row=0, column=1, padx=(0, 5))
        
        export_rules_button = ttk.Button(export_frame, text="导出 Cursor Rules", 
                                        command=self.export_cursor_rules)
        export_rules_button.grid(row=0, column=2)
    
    def populate_tree(self):
        """填充树形数据"""
        # 清空现有数据
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        self.node_entries.clear()
        # 创建item_id到节点的映射
        self.item_to_node_map = {}
        
        # 如果有根节点，开始填充
        if self.project_model.root_node:
            self.insert_node(self.project_model.root_node, '')
    
    def insert_node(self, node, parent_id):
        """插入节点到树形视图"""
        # 确定图标
        if node.is_directory:
            icon = "📁"
        else:
            icon = "📄"
        
        # 插入节点
        display_text = f"{icon} {node.name}"
        item_id = self.tree.insert(parent_id, 'end', text=display_text, 
                                  values=(node.description,))
        
        # 存储节点引用映射
        self.item_to_node_map[item_id] = node
        
        # 递归插入子节点
        for child in node.children:
            self.insert_node(child, item_id)
        
        # 展开目录节点
        if node.is_directory and parent_id == '':
            self.tree.item(item_id, open=True)
    
    def on_item_double_click(self, event):
        """处理双击事件"""
        item_id = self.tree.selection()[0] if self.tree.selection() else None
        if item_id:
            self.edit_description(item_id)
    
    def edit_description(self, item_id):
        """编辑描述"""
        # 获取节点
        node = self.get_node_from_item(item_id)
        if not node:
            return
        
        # 创建编辑对话框
        dialog = DescriptionDialog(self.root, node.name, node.description)
        new_description = dialog.result
        
        if new_description is not None:
            # 更新节点描述
            node.description = new_description
            
            # 更新树形视图显示
            self.tree.set(item_id, 'description', new_description)
    
    def get_node_from_item(self, item_id):
        """从树形项目获取节点"""
        # 简化实现：使用item_id到节点的映射
        if hasattr(self, 'item_to_node_map'):
            return self.item_to_node_map.get(item_id)
        return None
    
    def show_context_menu(self, event):
        """显示右键菜单"""
        item_id = self.tree.identify_row(event.y)
        if item_id:
            self.tree.selection_set(item_id)
            
            # 创建右键菜单
            context_menu = tk.Menu(self.root, tearoff=0)
            context_menu.add_command(label="编辑描述", command=lambda: self.edit_description(item_id))
            context_menu.add_separator()
            context_menu.add_command(label="展开所有", command=self.expand_all)
            context_menu.add_command(label="折叠所有", command=self.collapse_all)
            
            # 显示菜单
            try:
                context_menu.tk_popup(event.x_root, event.y_root)
            finally:
                context_menu.grab_release()
    
    def expand_all(self):
        """展开所有节点"""
        def expand_item(item_id):
            self.tree.item(item_id, open=True)
            for child_id in self.tree.get_children(item_id):
                expand_item(child_id)
        
        for item_id in self.tree.get_children():
            expand_item(item_id)
    
    def collapse_all(self):
        """折叠所有节点"""
        def collapse_item(item_id):
            self.tree.item(item_id, open=False)
            for child_id in self.tree.get_children(item_id):
                collapse_item(child_id)
        
        for item_id in self.tree.get_children():
            collapse_item(item_id)
    
    def refresh_tree(self):
        """刷新树形视图"""
        self.populate_tree()
    
    def get_statistics(self):
        """获取统计信息"""
        stats = {'directories': 0, 'files': 0}
        
        def count_nodes(node):
            if node.is_directory:
                stats['directories'] += 1
            else:
                stats['files'] += 1
            
            for child in node.children:
                count_nodes(child)
        
        if self.project_model.root_node:
            count_nodes(self.project_model.root_node)
        
        return stats
    
    def export_markdown(self):
        """导出为Markdown"""
        try:
            file_path = filedialog.asksaveasfilename(
                title="保存 Markdown 文件",
                defaultextension=".md",
                filetypes=[("Markdown files", "*.md"), ("All files", "*.*")]
            )
            
            if file_path:
                output_path, message = self.exporter.export_to_markdown(self.project_model, file_path)
                if output_path:
                    messagebox.showinfo("成功", f"导出成功！\n文件保存至: {output_path}")
                else:
                    messagebox.showerror("错误", message)
        except Exception as e:
            messagebox.showerror("错误", f"导出失败: {str(e)}")
    
    def export_json(self):
        """导出为JSON"""
        try:
            file_path = filedialog.asksaveasfilename(
                title="保存 JSON 文件",
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            if file_path:
                output_path, message = self.exporter.export_to_json(self.project_model, file_path)
                if output_path:
                    messagebox.showinfo("成功", f"导出成功！\n文件保存至: {output_path}")
                else:
                    messagebox.showerror("错误", message)
        except Exception as e:
            messagebox.showerror("错误", f"导出失败: {str(e)}")
    
    def export_cursor_rules(self):
        """导出为Cursor Rules"""
        try:
            file_path = filedialog.asksaveasfilename(
                title="保存 Cursor Rules 文件",
                defaultextension=".cursorrules",
                filetypes=[("Cursor rules files", "*.cursorrules"), ("Text files", "*.txt"), ("All files", "*.*")]
            )
            
            if file_path:
                output_path, message = self.exporter.export_to_cursor_rules(self.project_model, file_path)
                if output_path:
                    messagebox.showinfo("成功", f"导出成功！\n文件保存至: {output_path}")
                else:
                    messagebox.showerror("错误", message)
        except Exception as e:
            messagebox.showerror("错误", f"导出失败: {str(e)}")
    
    def on_back_click(self):
        """处理返回按钮点击"""
        if self.on_back_to_config:
            self.on_back_to_config()


class DescriptionDialog:
    """描述编辑对话框"""
    
    def __init__(self, parent, node_name, current_description=""):
        self.result = None
        
        # 创建对话框窗口
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(f"编辑描述 - {node_name}")
        self.dialog.geometry("500x200")
        self.dialog.resizable(True, True)
        
        # 设置模态
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # 居中显示
        self.center_dialog(parent)
        
        # 创建界面
        self.setup_ui(current_description)
        
        # 等待对话框关闭
        self.dialog.wait_window()
    
    def center_dialog(self, parent):
        """居中显示对话框"""
        parent.update_idletasks()
        
        # 获取父窗口位置和大小
        parent_x = parent.winfo_x()
        parent_y = parent.winfo_y()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()
        
        # 获取对话框大小
        dialog_width = 500
        dialog_height = 200
        
        # 计算居中位置
        x = parent_x + (parent_width - dialog_width) // 2
        y = parent_y + (parent_height - dialog_height) // 2
        
        self.dialog.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")
    
    def setup_ui(self, current_description):
        """设置对话框界面"""
        # 主框架
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.dialog.columnconfigure(0, weight=1)
        self.dialog.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # 标签
        ttk.Label(main_frame, text="请输入功能描述:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        # 文本框
        self.text_entry = tk.Text(main_frame, height=6, wrap=tk.WORD)
        self.text_entry.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        self.text_entry.insert(1.0, current_description)
        
        # 滚动条
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.text_entry.yview)
        scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S), pady=(0, 10))
        self.text_entry.configure(yscrollcommand=scrollbar.set)
        
        # 按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E))
        button_frame.columnconfigure(0, weight=1)
        
        # 按钮
        ttk.Button(button_frame, text="确定", command=self.on_ok).grid(row=0, column=1, padx=(5, 0))
        ttk.Button(button_frame, text="取消", command=self.on_cancel).grid(row=0, column=2, padx=(5, 0))
        
        # 设置焦点
        self.text_entry.focus()
    
    def on_ok(self):
        """确定按钮"""
        self.result = self.text_entry.get(1.0, tk.END).strip()
        self.dialog.destroy()
    
    def on_cancel(self):
        """取消按钮"""
        self.result = None
        self.dialog.destroy()