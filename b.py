import sys
import json
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton,
                             QLabel, QLineEdit, QFileDialog, QMessageBox, QFormLayout, QScrollArea, QInputDialog)


# 用户定义的函数（示例）
def user_defined_function(data):
    # 假设函数进行某种处理，这里简单返回字典的长度
    return f"字典内容: {json.dumps(data, indent=4)}"


# 新的用户定义的函数，接受目标参数和字典
def quote_function(target_param, data):
    # 示例函数，返回目标参数和字典的一个组合字符串
    return f"目标参数: {target_param}, 字典内容: {json.dumps(data, indent=4)}"


class JSONEditorApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("JSON 文件编辑器")
        self.setGeometry(100, 100, 600, 400)

        self.original_data = {}
        self.edited_data = {}

        self.layout = QVBoxLayout()

        self.load_button = QPushButton("选择 JSON 文件")
        self.load_button.clicked.connect(self.load_json)
        self.layout.addWidget(self.load_button)

        self.form_layout = QFormLayout()

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_content.setLayout(self.form_layout)
        self.scroll_area.setWidget(self.scroll_content)
        self.layout.addWidget(self.scroll_area)

        self.save_dict_button = QPushButton("保存字典")
        self.save_dict_button.clicked.connect(self.save_dict)
        self.layout.addWidget(self.save_dict_button)

        self.save_json_button = QPushButton("保存字典并保存 JSON 文件")
        self.save_json_button.clicked.connect(self.save_json)
        self.layout.addWidget(self.save_json_button)

        self.process_button = QPushButton("运行")
        self.process_button.clicked.connect(self.process_data)
        self.layout.addWidget(self.process_button)

        self.quote_button = QPushButton("Quote")
        self.quote_button.clicked.connect(self.quote_data)
        self.layout.addWidget(self.quote_button)

        self.result_label = QLabel("")
        self.layout.addWidget(self.result_label)

        self.save_result_button = QPushButton("保存结果为文本文件")
        self.save_result_button.clicked.connect(self.save_result)
        self.save_result_button.setEnabled(False)
        self.layout.addWidget(self.save_result_button)

        self.setLayout(self.layout)

    def load_json(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择 JSON 文件", "", "JSON files (*.json)")
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    self.original_data = json.load(file)
                    self.edited_data = self.original_data.copy()
                self.display_data()
            except Exception as e:
                QMessageBox.critical(self, "错误", f"无法读取文件: {e}")

    def display_data(self):
        for i in reversed(range(self.form_layout.count())):
            self.form_layout.itemAt(i).widget().setParent(None)

        self.entries = {}
        for key, value in self.edited_data.items():
            label = QLabel(key)
            entry = QLineEdit()
            entry.setText(str(value))
            self.form_layout.addRow(label, entry)
            self.entries[key] = entry

    def save_dict(self):
        try:
            for key, entry in self.entries.items():
                self.edited_data[key] = entry.text()
            QMessageBox.information(self, "成功", "字典已保存")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存字典时出错: {e}")

    def save_json(self):
        try:
            for key, entry in self.entries.items():
                self.edited_data[key] = entry.text()
            file_path, _ = QFileDialog.getSaveFileName(self, "保存 JSON 文件", "", "JSON files (*.json)")
            if file_path:
                with open(file_path, 'w') as file:
                    json.dump(self.edited_data, file, indent=4)
                QMessageBox.information(self, "成功", "字典和 JSON 文件已保存")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存字典或 JSON 文件时出错: {e}")

    def process_data(self):
        try:
            for key, entry in self.entries.items():
                self.edited_data[key] = entry.text()
            result = user_defined_function(self.edited_data)
            self.result_label.setText(result)
            self.result = result
            self.save_result_button.setEnabled(True)
        except Exception as e:
            QMessageBox.critical(self, "错误", f"处理数据时出错: {e}")

    def quote_data(self):
        try:
            target_param, ok = QInputDialog.getText(self, "输入目标参数", "目标参数:")
            if ok and target_param:
                for key, entry in self.entries.items():
                    self.edited_data[key] = entry.text()
                result = quote_function(target_param, self.edited_data)
                self.result_label.setText(result)
                self.result = result
                self.save_result_button.setEnabled(True)
        except Exception as e:
            QMessageBox.critical(self, "错误", f"处理数据时出错: {e}")

    def save_result(self):
        try:
            file_path, _ = QFileDialog.getSaveFileName(self, "保存文本文件", "", "Text files (*.txt)")
            if file_path:
                with open(file_path, 'w') as file:
                    file.write(self.result)
                QMessageBox.information(self, "成功", "结果已保存为文本文件")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存结果时出错: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = JSONEditorApp()
    window.show()
    sys.exit(app.exec_())