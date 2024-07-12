import sys
import json
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, scrolledtext

# 用户定义的函数（示例）
def user_defined_function(data):
    # 假设函数进行某种处理，这里简单返回字典的长度
    return f"字典内容: {json.dumps(data, indent=4)}"

# 新的用户定义的函数，接受目标参数和字典
def quote_function(target_param, data):
    # 示例函数，返回目标参数和字典的一个组合字符串
    return f"目标参数: {target_param}, 字典内容: {json.dumps(data, indent=4)}"

class JSONEditorApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("JSON 文件编辑器")
        self.geometry("700x600")

        self.original_data = {}
        self.edited_data = {}

        self.create_widgets()

    def create_widgets(self):
        self.load_button = tk.Button(self, text="选择 JSON 文件", command=self.load_json)
        self.load_button.pack(pady=5)

        self.file_label = tk.Label(self, text="未选择文件", font=("Helvetica", 14))
        self.file_label.pack(pady=5)

        self.scroll_area = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=80, height=15, spacing3=5)
        self.scroll_area.pack(pady=5)

        self.save_dict_button = tk.Button(self, text="保存字典", command=self.save_dict)
        self.save_dict_button.pack(pady=5)

        self.save_json_button = tk.Button(self, text="保存字典并保存 JSON 文件", command=self.save_json)
        self.save_json_button.pack(pady=5)

        self.process_button = tk.Button(self, text="运行", command=self.process_data)
        self.process_button.pack(pady=5)

        self.quote_button = tk.Button(self, text="Quote", command=self.quote_data)
        self.quote_button.pack(pady=5)

        self.result_label = tk.Label(self, text="", wraplength=600)
        self.result_label.pack(pady=5)

        self.save_result_button = tk.Button(self, text="保存结果为文本文件", command=self.save_result, state=tk.DISABLED)
        self.save_result_button.pack(pady=5)

    def load_json(self):
        file_path = filedialog.askopenfilename(title="选择 JSON 文件", filetypes=[("JSON files", "*.json")])
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    self.original_data = json.load(file)
                    self.edited_data = self.original_data.copy()
                self.file_label.config(text=f"文件: {file_path}")
                self.display_data()
            except Exception as e:
                messagebox.showerror("错误", f"无法读取文件: {e}")

    def display_data(self):
        self.scroll_area.delete(1.0, tk.END)
        self.entries = {}
        for key, value in self.edited_data.items():
            label = tk.Label(self.scroll_area, text=f"{key}: ")
            entry = tk.Entry(self.scroll_area, bg="lightyellow", relief="solid", bd=2)
            entry.insert(0, str(value))
            self.entries[key] = entry
            self.scroll_area.window_create(tk.END, window=label)
            self.scroll_area.window_create(tk.END, window=entry)
            self.scroll_area.insert(tk.END, "\n\n")

    def save_dict(self):
        try:
            for key, entry in self.entries.items():
                self.edited_data[key] = entry.get()
            messagebox.showinfo("成功", "字典已保存")
        except Exception as e:
            messagebox.showerror("错误", f"保存字典时出错: {e}")

    def save_json(self):
        try:
            for key, entry in self.entries.items():
                self.edited_data[key] = entry.get()
            file_path = filedialog.asksaveasfilename(title="保存 JSON 文件", defaultextension=".json", filetypes=[("JSON files", "*.json")])
            if file_path:
                with open(file_path, 'w') as file:
                    json.dump(self.edited_data, file, indent=4)
                messagebox.showinfo("成功", "字典和 JSON 文件已保存")
        except Exception as e:
            messagebox.showerror("错误", f"保存字典或 JSON 文件时出错: {e}")

    def process_data(self):
        try:
            for key, entry in self.entries.items():
                self.edited_data[key] = entry.get()
            result = user_defined_function(self.edited_data)
            self.result_label.config(text=result)
            self.result = result
            self.save_result_button.config(state=tk.NORMAL)
        except Exception as e:
            messagebox.showerror("错误", f"处理数据时出错: {e}")

    def quote_data(self):
        try:
            target_param = simpledialog.askstring("输入目标参数", "目标参数:")
            if target_param:
                for key, entry in self.entries.items():
                    self.edited_data[key] = entry.get()
                result = quote_function(target_param, self.edited_data)
                self.result_label.config(text=result)
                self.result = result
                self.save_result_button.config(state=tk.NORMAL)
        except Exception as e:
            messagebox.showerror("错误", f"处理数据时出错: {e}")

    def save_result(self):
        try:
            file_path = filedialog.asksaveasfilename(title="保存文本文件", defaultextension=".txt", filetypes=[("Text files", "*.txt")])
            if file_path:
                with open(file_path, 'w') as file:
                    file.write(self.result)
                messagebox.showinfo("成功", "结果已保存为文本文件")
        except Exception as e:
            messagebox.showerror("错误", f"保存结果时出错: {e}")

if __name__ == "__main__":
    app = JSONEditorApp()
    app.mainloop()
