from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import json


class ShowDataset(QDialog):
    def __init__(self, parent=None):
        super(ShowDataset, self).__init__(parent)
        self.setModal(True)
        self.resize(800, 600)
        self.setWindowTitle("Show Dataset")
        self.setFixedWidth(800)
        self.adjustSize()

        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderLabels(
            ["product name", "product quantity", "product price", "product code", "product brand"])

        self.populateTable()

        layout = QVBoxLayout()
        layout.addWidget(self.tableWidget)
        self.setLayout(layout)

    def populateTable(self):
        data_product = "Database/addproducts.json"
        try:
            with open(data_product, 'r') as file_handle:
                products_data = json.load(file_handle)
                self.tableWidget.setRowCount(len(products_data))
                for row, user in enumerate(products_data):

                    for col, key in enumerate(
                            ["product name", "product quantity", "product price", "product code", "product brand"]):
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
                    self.tableWidget.setCellWidget(row, 4, button_widget)  # Set at column index 4

                    edit_button.clicked.connect(lambda _, row=row: self.edit_product(row))
                    delete_button.clicked.connect(lambda _, row=row: self.deleteUser(row))

        except IOError as e:
            print("Error opening the file:", e)

        self.tableWidget.resizeColumnsToContents()

    def edit_product(self, row):
        data_product = "Database/addproducts.json"
        try:
            with open(data_product, 'r') as file_handle:
                products_data = json.load(file_handle)
                product_data = products_data[row]

                print("Editing user:", product_data)

                with open(data_product, 'w') as file_handle:
                    json.dump(products_data, file_handle, indent=4)
                    print("User data updated")

        except (IOError, IndexError) as e:
            print("Error:", e)

    def deleteUser(self, row):
        delete_product = "Database/addproducts.json"
        try:
            with open(delete_product, 'r') as file_handle:
                products_data = json.load(file_handle)
                product_data = products_data[row]

                reply = QMessageBox.question(self, "Delete User",
                                             f"Are you sure you want to delete {product_data['product name']}?",
                                             QMessageBox.Yes | QMessageBox.No,
                                             QMessageBox.No)

                if reply == QMessageBox.Yes:
                    del products_data[row]
                    with open(delete_product, 'w') as file_handle:
                        json.dump(products_data, file_handle, indent=4)
                        print("User data updated")

                    self.populateTable()

        except (IOError, IndexError) as e:
            print("Error:", e)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    dialog = ShowDataset()
    dialog.show()
    sys.exit(app.exec_())
