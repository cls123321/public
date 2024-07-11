import tkinter as tk
from tkinter import filedialog, messagebox
import json


# 用户定义的函数（示例）
def user_defined_function(data):
    # 假设函数进行某种处理，这里简单返回字典的长度
    return f"字典内容: {json.dumps(data, indent=4)}"


class JSONEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("JSON 文件编辑器")

        self.original_data = {}
        self.edited_data = {}

        self.load_button = tk.Button(root, text="选择 JSON 文件", command=self.load_json)
        self.load_button.pack(pady=10)

        self.frame = tk.Frame(root, background="white")
        self.frame.pack(pady=10)

        self.save_dict_button = tk.Button(root, text="保存字典", command=self.save_dict)
        self.save_dict_button.pack(pady=10)

        self.save_json_button = tk.Button(root, text="保存字典并保存 JSON 文件", command=self.save_json)
        self.save_json_button.pack(pady=10)

        self.process_button = tk.Button(root, text="运行", command=self.process_data)
        self.process_button.pack(pady=10)

        self.result_label = tk.Label(root, text="")
        self.result_label.pack(pady=10)

        self.save_result_button = tk.Button(root, text="保存结果为文本文件", command=self.save_result)
        self.save_result_button.pack(pady=10)
        self.save_result_button.config(state=tk.DISABLED)

    def load_json(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    self.original_data = json.load(file)
                    self.edited_data = self.original_data.copy()
                self.display_data()
            except Exception as e:
                messagebox.showerror("错误", f"无法读取文件: {e}")

    def display_data(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        self.entries = {}
        row = 0
        for key, value in self.edited_data.items():
            label = tk.Label(self.frame, text=key, background="white")
            label.grid(row=row, column=0, padx=5, pady=5)

            entry = tk.Entry(self.frame, background="lightgray")
            entry.grid(row=row, column=1, padx=5, pady=5)
            entry.insert(0, str(value))
            self.entries[key] = entry
            row += 1

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
            file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
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

    def save_result(self):
        try:
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
            if file_path:
                with open(file_path, 'w') as file:
                    file.write(self.result)
                messagebox.showinfo("成功", "结果已保存为文本文件")
        except Exception as e:
            messagebox.showerror("错误", f"保存结果时出错: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = JSONEditorApp(root)
    root.mainloop()