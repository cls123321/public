import sys
import json
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, scrolledtext

# 用户定义的函数（示例）
def user_defined_function(data):
    # 假设函数进行某种处理，这里简单返回一个新的字典
    return {"处理后的键1": "处理后的值1", "处理后的键2": "处理后的值2"}

# 新的用户定义的函数，接受目标参数和字典
def quote_function(param1, param2, data):
    # 示例函数，返回目标参数和字典的一个组合字典
    return {f"目标参数_{param1}": data, "浮点数": param2}

class JSONEditorApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("JSON 文件编辑器")
        self.geometry("700x600")

        self.original_data = {}
        self.edited_data = {}

        self.create_widgets()

    def create_widgets(self):
        self.canvas = tk.Canvas(self)
        self.scroll_y = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scroll_x = tk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)

        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scroll_y.set, xscrollcommand=self.scroll_x.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scroll_y.pack(side="right", fill="y")
        self.scroll_x.pack(side="bottom", fill="x")

        self.load_button = tk.Button(self.scrollable_frame, text="选择 JSON 文件", command=self.load_json)
        self.load_button.pack(pady=5)

        self.file_label = tk.Label(self.scrollable_frame, text="未选择文件", font=("Helvetica", 14))
        self.file_label.pack(pady=5)

        self.scroll_area = scrolledtext.ScrolledText(self.scrollable_frame, wrap=tk.WORD, width=80, height=15, spacing3=5)
        self.scroll_area.pack(pady=5)

        self.button_frame = tk.Frame(self.scrollable_frame)
        self.button_frame.pack(pady=5)

        self.save_dict_button = tk.Button(self.button_frame, text="保存字典", command=self.save_dict)
        self.save_dict_button.pack(side=tk.LEFT, padx=5)

        self.save_json_button = tk.Button(self.button_frame, text="保存字典并保存 JSON 文件", command=self.save_json)
        self.save_json_button.pack(side=tk.LEFT, padx=5)

        self.process_button = tk.Button(self.scrollable_frame, text="运行", command=self.process_data)
        self.process_button.pack(pady=5)

        self.quote_button = tk.Button(self.scrollable_frame, text="Quote", command=self.quote_data)
        self.quote_button.pack(pady=5)

        self.result_area = scrolledtext.ScrolledText(self.scrollable_frame, wrap=tk.WORD, width=80, height=10, spacing3=5, font=("Helvetica", 14))
        self.result_area.pack(pady=5)
        self.result_area.config(state=tk.DISABLED)

        self.save_result_button = tk.Button(self.scrollable_frame, text="保存结果为文本文件", command=self.save_result, state=tk.DISABLED)
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
            entry = tk.Entry(self.scroll_area, bg="lightyellow", relief="solid", bd=2, width=50, font=('Helvetica', 12))
            # 将值转换为字符串，但不使用 json.dumps，以避免双重编码
            entry.insert(0, str(value) if not isinstance(value, (dict, list)) else json.dumps(value, ensure_ascii=False))
            self.entries[key] = (entry, type(value))
            self.scroll_area.window_create(tk.END, window=label)
            self.scroll_area.window_create(tk.END, window=entry)

    def save_dict(self):
        try:
            for key, (entry, value_type) in self.entries.items():
                value = entry.get()
                if value_type == int:
                    try:
                        self.edited_data[key] = int(value)
                    except ValueError:
                        messagebox.showerror("错误", f"键 {key} 的值必须是整数")
                        return
                elif value_type == float:
                    try:
                        self.edited_data[key] = float(value)
                    except ValueError:
                        messagebox.showerror("错误", f"键 {key} 的值必须是浮点数")
                        return
                elif value_type == list or value_type == dict:
                    try:
                        self.edited_data[key] = json.loads(value)
                    except json.JSONDecodeError:
                        messagebox.showerror("错误", f"键 {key} 的值必须是有效的 JSON")
                        return
                elif value_type == bool:
                    self.edited_data[key] = value.lower() == 'true'
                elif value_type == type(None):
                    self.edited_data[key] = None
                else:
                    self.edited_data[key] = value
            messagebox.showinfo("成功", "字典已保存")
        except Exception as e:
            messagebox.showerror("错误", f"保存字典时出错: {e}")

    def save_json(self):
        try:
            self.save_dict()
            file_path = filedialog.asksaveasfilename(title="保存 JSON 文件", defaultextension=".json", filetypes=[("JSON files", "*.json")])
            if file_path:
                with open(file_path, 'w') as file:
                    json.dump(self.edited_data, file, indent=4, ensure_ascii=False)
                messagebox.showinfo("成功", "字典和 JSON 文件已保存")
        except Exception as e:
            messagebox.showerror("错误", f"保存字典或 JSON 文件时出错: {e}")

    def process_data(self):
        try:
            self.save_dict()
            result = user_defined_function(self.edited_data)
            self.display_result(result)
            self.result = result
            self.save_result_button.config(state=tk.NORMAL)
        except Exception as e:
            messagebox.showerror("错误", f"处理数据时出错: {e}")

    def quote_data(self):
        try:
            param1 = simpledialog.askstring("输入第一个目标参数", "目标参数1:")
            if param1:
                param2 = simpledialog.askfloat("输入第二个目标参数", "目标参数2 (浮点数):")
                if param2 is not None:
                    self.save_dict()
                    result = quote_function(param1, param2, self.edited_data)
                    self.display_result(result)
                    self.result = result
                    self.save_result_button.config(state=tk.NORMAL)
        except Exception as e:
            messagebox.showerror("错误", f"处理数据时出错: {e}")

    def display_result(self, result):
        self.result_area.config(state=tk.NORMAL)
        self.result_area.delete(1.0, tk.END)
        self.result_area.insert(tk.END, json.dumps(result, indent=4, ensure_ascii=False))
        self.result_area.config(state=tk.DISABLED)

    def save_result(self):
        try:
            file_path = filedialog.asksaveasfilename(title="保存文本文件", defaultextension=".txt", filetypes=[("Text files", "*.txt")])
            if file_path:
                with open(file_path, 'w') as file:
                    file.write(json.dumps(self.result, indent=4, ensure_ascii=False))
                messagebox.showinfo("成功", "结果已保存为文本文件")
        except Exception as e:
            messagebox.showerror("错误", f"保存结果时出错: {e}")

if __name__ == "__main__":
    app = JSONEditorApp()
    app.mainloop()
