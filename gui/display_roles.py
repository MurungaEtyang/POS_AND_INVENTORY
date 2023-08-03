from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import json


class show_Dataset(QDialog):
    def __init__(self, parent=None):
        super(show_Dataset, self).__init__(parent)
        self.setModal(True)
        self.resize(800, 600)
        self.setWindowTitle("Show Dataset")
        self.setFixedWidth(300)
        self.adjustSize()

        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(
            ["roles"])


        self.populateTable()

        layout = QVBoxLayout()
        layout.addWidget(self.tableWidget)
        self.setLayout(layout)

    def populateTable(self):
        users_file = "../Database/role.json"
        try:
            with open(users_file, 'r') as file_handle:
                users_data = json.load(file_handle)
                self.tableWidget.setRowCount(len(users_data))
                for row, user in enumerate(users_data):

                    for col, key in enumerate(
                            ["role"]):
                        item = QTableWidgetItem(str(user.get(key, "")))
                        self.tableWidget.setItem(row, col, item)

                    edit_button = QPushButton("Edit")
                    edit_button.setStyleSheet("background-color: green")
                    delete_button = QPushButton("Delete")
                    delete_button.setStyleSheet("background-color: red")
                    button_widget = QWidget()
                    button_layout = QHBoxLayout(button_widget)
                    button_layout.addWidget(edit_button)
                    button_layout.addWidget(delete_button)
                    button_layout.setContentsMargins(0, 0, 0, 0)
                    button_layout.setAlignment(Qt.AlignCenter)
                    button_widget.setLayout(button_layout)
                    self.tableWidget.setCellWidget(row, 1, button_widget)

                    edit_button.clicked.connect(lambda _, r=row: self.editUser(r))
                    delete_button.clicked.connect(lambda _, r=row: self.deleteUser(r))

        except IOError as e:
            print("Error opening the file:", e)

        self.tableWidget.resizeColumnsToContents()

    def editUser(self, row):
        users_file = "../Database/role.json"
        try:
            with open(users_file, 'r') as file_handle:
                users_data = json.load(file_handle)
                user_data = users_data[row]

                print("Editing role:", user_data)

                with open(users_file, 'w') as file_handle:
                    json.dump(users_data, file_handle, indent=4)
                    print("role data updated")

        except (IOError, IndexError) as e:
            print("Error:", e)

    def deleteUser(self, row):
        users_file = "../Database/role.json"
        try:
            with open(users_file, 'r') as file_handle:
                users_data = json.load(file_handle)
                user_data = users_data[row]
                
                reply = QMessageBox.question(self, "Delete role",
                                            f"Are you sure you want to delete {user_data['role']}?",
                                            QMessageBox.Yes | QMessageBox.No,
                                            QMessageBox.No)

                if reply == QMessageBox.Yes:
                    del users_data[row]
                    with open(users_file, 'w') as file_handle:
                        json.dump(users_data, file_handle, indent=4)
                        print("User data updated")

                    self.populateTable()

        except (IOError, IndexError) as e:
            print("Error:", e)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    dialog = show_Dataset()
    dialog.show()
    sys.exit(app.exec_())
