import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.con = sqlite3.connect("coffee.sqlite")
        self.pushButton.clicked.connect(self.update_table)
        self.update_table()

    def update_table(self):
        cur = self.con.cursor()
        result = cur.execute("SELECT coffee.id, coffee.name, degrees.degree, forms.form,"
                             "coffee.taste, coffee.price, coffee.volume "
                             "FROM coffee, degrees, forms "
                             "WHERE degrees.id = coffee.degree "
                             "AND forms.id = coffee.form").fetchall()
        self.tableWidget.setRowCount(len(result))
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
