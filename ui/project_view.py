"""
工程运维界面 - v1.0.1
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from logic.exporter import Exporter
from utils.logger import logger


class ProjectView:
    """工程运维界面类"""
    
    def __init__(self, root, project_model, on_back_to_config):
        self.root = root
        self.project_model = project_model
        self.on_back_to_config = on_back_to_config
        self.exporter = Exporter()
        
        # 用于存储所有节点的Entry引用
        self.node_entries = {}
        
        # 标签管理
        self.available_tags = ["功能复合", "单一职责", "服务层"]  # 默认标签
        self.node_tags = {}  # 存储每个节点的标签
        
        logger.info("Initializing project view")
        self.setup_ui()
    
    def setup_ui(self):
        """设置用户界面"""
        # 清空窗口
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # 设置窗口标题和大小
        self.root.title("工程运维 - 结构展示 v1.0.1")
        self.root.geometry("1200x800")
        
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # 顶部信息框架
        self.create_info_panel(main_frame)
        
        # 标签管理框架
        self.create_tag_panel(main_frame)
        
        # 主要内容框架
        content_frame = ttk.Frame(main_frame)
        content_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        content_frame.columnconfigure(0, weight=1)
        content_frame.rowconfigure(0, weight=1)
        
        # 创建树形视图
        self.create_tree_view(content_frame)
        
        # 底部按钮框架
        self.create_button_panel(main_frame)
        
        logger.info("UI setup completed")
    
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
    
    def create_tag_panel(self, parent):
        """创建标签管理面板"""
        tag_frame = ttk.LabelFrame(parent, text="目录/文件标签", padding="10")
        tag_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        tag_frame.columnconfigure(1, weight=1)
        
        # 标签显示区域
        ttk.Label(tag_frame, text="可用标签:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        
        # 标签容器框架
        self.tag_container = ttk.Frame(tag_frame)
        self.tag_container.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        
        # 新标签输入框
        self.new_tag_entry = ttk.Entry(tag_frame, width=15)
        self.new_tag_entry.grid(row=0, column=2, padx=(5, 0))
        self.new_tag_entry.bind('<Return>', self.add_new_tag)
        
        # 添加标签按钮
        add_tag_button = ttk.Button(tag_frame, text="+", width=3, command=self.add_new_tag)
        add_tag_button.grid(row=0, column=3, padx=(5, 0))
        
        # 更新标签显示
        self.update_tag_display()
    
    def update_tag_display(self):
        """更新标签显示"""
        # 清空现有标签显示
        for widget in self.tag_container.winfo_children():
            widget.destroy()
        
        # 添加标签按钮
        for i, tag in enumerate(self.available_tags):
            tag_frame = ttk.Frame(self.tag_container)
            tag_frame.grid(row=0, column=i, padx=(0, 5))
            
            tag_label = ttk.Label(tag_frame, text=tag, background="lightblue", 
                                 relief="solid", borderwidth=1, padding="2")
            tag_label.grid(row=0, column=0)
            
            # 删除按钮
            if tag not in ["功能复合", "单一职责", "服务层"]:  # 默认标签不可删除
                remove_btn = ttk.Button(tag_frame, text="×", width=3,
                                       command=lambda t=tag: self.remove_tag(t))
                remove_btn.grid(row=0, column=1, padx=(2, 0))
    
    def add_new_tag(self, event=None):
        """添加新标签"""
        new_tag = self.new_tag_entry.get().strip()
        if new_tag and len(new_tag) <= 5 and new_tag not in self.available_tags:
            self.available_tags.append(new_tag)
            self.new_tag_entry.delete(0, tk.END)
            self.update_tag_display()
            logger.info(f"Added new tag: {new_tag}")
    
    def remove_tag(self, tag):
        """删除标签"""
        if tag in self.available_tags and tag not in ["功能复合", "单一职责", "服务层"]:
            self.available_tags.remove(tag)
            # 同时从所有节点中删除此标签
            for node_id in list(self.node_tags.keys()):
                if tag in self.node_tags[node_id]:
                    self.node_tags[node_id].remove(tag)
            self.update_tag_display()
            self.refresh_tree()
            logger.info(f"Removed tag: {tag}")
    
    def create_tree_view(self, parent):
        """创建树形视图"""
        # 创建框架用于放置树形视图和滚动条
        tree_frame = ttk.Frame(parent)
        tree_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)
        
        # 创建Treeview，增加标签列
        self.tree = ttk.Treeview(tree_frame, columns=('tags', 'description'), show='tree headings')
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置列
        self.tree.heading('#0', text='文件/目录结构', anchor=tk.W)
        self.tree.heading('tags', text='标签', anchor=tk.W)
        self.tree.heading('description', text='功能描述', anchor=tk.W)
        
        self.tree.column('#0', width=350, minwidth=250)
        self.tree.column('tags', width=150, minwidth=100)
        self.tree.column('description', width=400, minwidth=200)
        
        # 配置树形视图样式，添加行分隔线
        style = ttk.Style()
        style.configure("Treeview", rowheight=25)
        
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
        
        # 绑定事件
        self.tree.bind('<Double-1>', self.on_item_double_click)
        self.tree.bind('<Button-3>', self.show_context_menu)
        self.tree.bind('<Button-1>', self.on_item_click)
    
    def create_button_panel(self, parent):
        """创建按钮面板"""
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=10)
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
        
        # 获取节点标签
        node_key = f"{node.path}_{node.name}"
        tags = self.node_tags.get(node_key, [])
        tags_text = ", ".join(tags) if tags else ""
        
        # 插入节点
        display_text = f"{icon} {node.name}"
        item_id = self.tree.insert(parent_id, 'end', text=display_text, 
                                  values=(tags_text, node.description))
        
        # 存储节点引用映射
        self.item_to_node_map[item_id] = node
        
        # 设置行的背景色（创建分隔线效果）
        if len(self.tree.get_children(parent_id)) % 2 == 0:
            self.tree.set(item_id, 'tags', tags_text)
        
        # 递归插入子节点
        for child in node.children:
            self.insert_node(child, item_id)
        
        # 展开目录节点
        if node.is_directory and parent_id == '':
            self.tree.item(item_id, open=True)
    
    def on_item_click(self, event):
        """处理单击事件 - 用于标签编辑"""
        item_id = self.tree.identify_row(event.y)
        column = self.tree.identify_column(event.x)
        
        if item_id and column == '#2':  # 标签列
            self.edit_tags(item_id)
    
    def on_item_double_click(self, event):
        """处理双击事件"""
        item_id = self.tree.identify_row(event.y)
        column = self.tree.identify_column(event.x)
        
        if item_id:
            if column == '#3':  # 描述列
                self.edit_description_inline(item_id)
            else:
                self.edit_description(item_id)
    
    def edit_tags(self, item_id):
        """编辑标签"""
        node = self.get_node_from_item(item_id)
        if not node:
            return
        
        node_key = f"{node.path}_{node.name}"
        current_tags = self.node_tags.get(node_key, [])
        
        # 创建标签选择对话框
        dialog = TagSelectionDialog(self.root, self.available_tags, current_tags)
        new_tags = dialog.result
        
        if new_tags is not None:
            self.node_tags[node_key] = new_tags
            # 更新树形视图显示
            tags_text = ", ".join(new_tags) if new_tags else ""
            self.tree.set(item_id, 'tags', tags_text)
            logger.info(f"Updated tags for {node.name}: {new_tags}")
    
    def edit_description_inline(self, item_id):
        """内联编辑描述"""
        node = self.get_node_from_item(item_id)
        if not node:
            return
        
        # 获取项目位置
        bbox = self.tree.bbox(item_id, 'description')
        if not bbox:
            return
        
        # 创建编辑框
        edit_frame = tk.Frame(self.tree)
        edit_entry = tk.Entry(edit_frame, font=("Arial", 9))
        edit_entry.insert(0, node.description)
        edit_entry.select_range(0, tk.END)
        
        # 定义保存函数
        def save_description(event=None):
            new_description = edit_entry.get()
            node.description = new_description
            self.tree.set(item_id, 'description', new_description)
            edit_frame.destroy()
            logger.info(f"Updated description for {node.name}")
        
        def cancel_edit(event=None):
            edit_frame.destroy()
        
        # 绑定事件
        edit_entry.bind('<Return>', save_description)
        edit_entry.bind('<Escape>', cancel_edit)
        edit_entry.bind('<FocusOut>', save_description)
        
        edit_entry.pack(fill=tk.BOTH, expand=True)
        edit_frame.place(x=bbox[0], y=bbox[1], width=bbox[2], height=bbox[3])
        edit_entry.focus()
    
    def edit_description(self, item_id):
        """编辑描述（使用对话框）"""
        # 获取节点
        node = self.get_node_from_item(item_id)
        if not node:
            return
        
        try:
            # 创建编辑对话框
            dialog = DescriptionDialog(self.root, node.name, node.description)
            new_description = dialog.result
            
            if new_description is not None:
                # 更新节点描述
                node.description = new_description
                
                # 更新树形视图显示
                self.tree.set(item_id, 'description', new_description)
                logger.info(f"Updated description for {node.name}")
        except Exception as e:
            logger.error(f"Error editing description: {str(e)}")
            messagebox.showerror("错误", f"编辑描述时出现错误: {str(e)}")
    
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
            context_menu.add_command(label="编辑标签", command=lambda: self.edit_tags(item_id))
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
                    logger.info(f"Exported to markdown: {output_path}")
                else:
                    messagebox.showerror("错误", message)
                    logger.error(f"Export to markdown failed: {message}")
        except Exception as e:
            error_msg = f"导出失败: {str(e)}"
            messagebox.showerror("错误", error_msg)
            logger.error(error_msg)
    
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
                    logger.info(f"Exported to JSON: {output_path}")
                else:
                    messagebox.showerror("错误", message)
                    logger.error(f"Export to JSON failed: {message}")
        except Exception as e:
            error_msg = f"导出失败: {str(e)}"
            messagebox.showerror("错误", error_msg)
            logger.error(error_msg)
    
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
                    logger.info(f"Exported to cursor rules: {output_path}")
                else:
                    messagebox.showerror("错误", message)
                    logger.error(f"Export to cursor rules failed: {message}")
        except Exception as e:
            error_msg = f"导出失败: {str(e)}"
            messagebox.showerror("错误", error_msg)
            logger.error(error_msg)
    
    def on_back_click(self):
        """处理返回按钮点击"""
        if self.on_back_to_config:
            logger.info("Returning to config view")
            self.on_back_to_config()


class DescriptionDialog:
    """描述编辑对话框"""
    
    def __init__(self, parent, node_name, current_description=""):
        self.result = None
        self.parent = parent
        
        # 创建对话框窗口
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(f"编辑描述 - {node_name}")
        self.dialog.geometry("500x200")
        self.dialog.resizable(True, True)
        
        # 居中显示
        self.center_dialog(parent)
        
        # 创建界面
        self.setup_ui(current_description)
        
        # 延迟设置模态，避免grab错误
        self.dialog.after(100, self.setup_modal)
        
        # 等待对话框关闭
        self.dialog.wait_window()
    
    def setup_modal(self):
        """延迟设置模态"""
        try:
            self.dialog.transient(self.parent)
            self.dialog.grab_set()
            self.dialog.focus()
        except tk.TclError as e:
            logger.warning(f"Modal setup warning: {str(e)}")
    
    def center_dialog(self, parent):
        """居中显示对话框"""
        self.dialog.update_idletasks()
        
        # 获取父窗口位置和大小
        parent.update_idletasks()
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


class TagSelectionDialog:
    """标签选择对话框"""
    
    def __init__(self, parent, available_tags, current_tags):
        self.result = None
        self.available_tags = available_tags
        self.current_tags = current_tags.copy()
        
        # 创建对话框窗口
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("选择标签")
        self.dialog.geometry("400x300")
        self.dialog.resizable(False, False)
        
        # 居中显示
        self.center_dialog(parent)
        
        # 创建界面
        self.setup_ui()
        
        # 延迟设置模态
        self.dialog.after(100, self.setup_modal)
        
        # 等待对话框关闭
        self.dialog.wait_window()
    
    def setup_modal(self):
        """延迟设置模态"""
        try:
            self.dialog.transient(self.dialog.master)
            self.dialog.grab_set()
            self.dialog.focus()
        except tk.TclError as e:
            logger.warning(f"Tag dialog modal setup warning: {str(e)}")
    
    def center_dialog(self, parent):
        """居中显示对话框"""
        self.dialog.update_idletasks()
        parent.update_idletasks()
        
        parent_x = parent.winfo_x()
        parent_y = parent.winfo_y()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()
        
        dialog_width = 400
        dialog_height = 300
        
        x = parent_x + (parent_width - dialog_width) // 2
        y = parent_y + (parent_height - dialog_height) // 2
        
        self.dialog.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")
    
    def setup_ui(self):
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
        ttk.Label(main_frame, text="请选择标签:").grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        
        # 标签选择区域
        self.tag_vars = {}
        tag_frame = ttk.Frame(main_frame)
        tag_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        for i, tag in enumerate(self.available_tags):
            var = tk.BooleanVar()
            var.set(tag in self.current_tags)
            self.tag_vars[tag] = var
            
            cb = ttk.Checkbutton(tag_frame, text=tag, variable=var)
            cb.grid(row=i//2, column=i%2, sticky=tk.W, padx=(0, 20), pady=2)
        
        # 按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, sticky=(tk.W, tk.E))
        button_frame.columnconfigure(0, weight=1)
        
        # 按钮
        ttk.Button(button_frame, text="确定", command=self.on_ok).grid(row=0, column=1, padx=(5, 0))
        ttk.Button(button_frame, text="取消", command=self.on_cancel).grid(row=0, column=2, padx=(5, 0))
    
    def on_ok(self):
        """确定按钮"""
        self.result = [tag for tag, var in self.tag_vars.items() if var.get()]
        self.dialog.destroy()
    
    def on_cancel(self):
        """取消按钮"""
        self.result = None
        self.dialog.destroy()