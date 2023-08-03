from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QFont
import json, time, random
class Bill_generate:

    data = "Database/addproducts.json"
    users = "Database/addusers.json"

    product_name = 0
    def __init__(self) -> None:
        pass
    def search_products(self, search1, spinbox, paid):
        Bill_generate.__search_product__(self, search1, spinbox, paid)

    def __search_product__(self, search1, spinbox, paid):
        try:
            search_text = search1.text()
            with open(Bill_generate.data, "r") as f:
                data = json.load(f)

            found_products = []
            for product in data:
                if search_text.lower() in product["product name"].lower() or search_text.lower() in product["product code"].lower():
                    found_products.append(product)

            if found_products:
                product = found_products[0]
                self.search_label.setText(f"Product: {product['product name']}, Price: {product['product price']}")
                product_price = product['product price']
                product_name = product['product name']
                total_product_price = int(spinbox.text())
                t = 0
                if(total_product_price == 0):
                    t = product_price * 1

                else:
                    t = total_product_price * product_price
                self.search_total2.setText(str(t))
                paid_amount = float(paid.text())
                change = paid_amount - t
                if change > 0:
                    self.search_change1.setStyleSheet("background-color: white; color: red")
                else:
                    self.search_change1.setStyleSheet("background-color: white; color: green")
                self.search_change1.setText(str(change))
            else:
                self.search_label.setText("Product not available.")

            bill_content = "==================== Your Bill ===================\n"
            bill_content += f"Product: ====> {product_name}\n"
            bill_content += f"Product Price: ====> {product_price}\n"
            bill_content += f"Total Product bought: ====> {total_product_price}\n"
            bill_content += f"Total Amount: ====> {t}\n"
            bill_content += f"Paid Amount: ====> {paid_amount}\n"
            bill_content += f"Change: ====> {change}\n"
            bill_content += f"time: ====> {time.ctime()}\n"
            bill_content += f"code : ====> {random.randint(1000000, 9999999)}\n"
            bill_content += "=================== ******** ===================\n"

            printer = QPrinter(QPrinter.HighResolution)
            dialog = QPrintDialog(printer, self)
            if dialog.exec_() == QPrintDialog.Accepted:
                painter = QPainter()
                painter.begin(printer)
                font = QFont()
                font.setPointSize(12)
                painter.setFont(font)
                painter.drawText(printer.pageRect(), Qt.AlignCenter, bill_content)
                painter.end()

            # kot content
            kot_content = "==================== Kitchen Order Ticket ===================\n"
            kot_content += f"Product: ====> {product_name}\n"
            kot_content += f"time: ====> {time.ctime()}\n"
            kot_content += f"code : ====> {random.randint(1000000, 9999999)}\n"
            kot_content += "=================== ******** ===================\n"

            if dialog.exec_() == QPrintDialog.Accepted:
                painter = QPainter()
                painter.begin(printer)
                font = QFont()
                font.setPointSize(12)
                painter.setFont(font)
                painter.drawText(printer.pageRect(), Qt.AlignCenter, kot_content)
                painter.end()

        except Exception as e:
            print(e)

    def usercredentials(self):
        self.__usersCredentials__()

    def __usersCredentials__(self):

        with open (Bill_generate.users, 'r') as users:
            users = json.load(users)
            # print(users)

            for user in users:
                print ("First name: ", user['Firstname'])
                print ("Last name", user['lastname'])
                print ("Username: ", user['username'])
                print("Role: ", user['role'])
                print("salary: ", user['salary'])
                print("National Id: ", user['National ID'])
                print("blood group: ", user['Blood Type'])
d= Bill_generate()
d.usercredentials()

