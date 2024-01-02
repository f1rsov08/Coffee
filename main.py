import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QWidget


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.con = sqlite3.connect("coffee.sqlite")
        self.pushButton.clicked.connect(self.update_table)
        self.addButton.clicked.connect(self.add_coffee)
        self.editButton.clicked.connect(self.edit_coffee)
        self.update_table()

    def update_table(self):
        cur = self.con.cursor()
        self.table = cur.execute("SELECT coffee.id, coffee.name, degrees.degree, forms.form,"
                                 "coffee.taste, coffee.price, coffee.volume "
                                 "FROM coffee, degrees, forms "
                                 "WHERE degrees.id = coffee.degree "
                                 "AND forms.id = coffee.form").fetchall()
        self.tableWidget.setRowCount(len(self.table))
        for i, elem in enumerate(self.table):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

    def add_coffee(self):
        self.addForm = addEditCoffeeForm(self)
        self.addForm.show()
        self.statusbar.showMessage('')

    def edit_coffee(self):
        items = self.tableWidget.selectedItems()
        if items:
            self.editForm = addEditCoffeeForm(self, self.table[items[0].row()])
            self.editForm.show()
            self.statusbar.showMessage('')
        else:
            self.statusbar.showMessage('Ничего не выбрано')


class addEditCoffeeForm(QWidget):
    def __init__(self, parent, item=None):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.parent = parent
        if item is not None:
            self.item = item
            self.pushButton.setText('Сохранить')
            self.pushButton.clicked.connect(self.save)
            self.name.setText(self.item[1])
            self.degree.setCurrentIndex(self.degree.findText(self.item[2]))
            self.form.setCurrentIndex(self.form.findText(self.item[3]))
            self.taste.setText(self.item[4])
            self.price.setValue(self.item[5])
            self.volume.setValue(self.item[6])
        else:
            self.pushButton.clicked.connect(self.add)

    def save(self):
        cur = self.parent.con.cursor()
        cur.execute(f"UPDATE coffee "
                    f"SET name = '{self.name.text()}', "
                    f"degree = {self.degree.currentIndex() + 1}, "
                    f"form = {self.form.currentIndex() + 1},"
                    f"taste = '{self.taste.text()}',"
                    f"price = {self.price.value()}, "
                    f"volume = {self.volume.value()} "
                    f"WHERE id = {self.item[0]}")
        self.parent.con.commit()
        self.parent.update_table()
        self.close()

    def add(self):
        cur = self.parent.con.cursor()
        cur.execute(f"INSERT INTO coffee(name, degree, form, taste, price, volume) "
                    f"VALUES('{self.name.text()}', "
                    f"{self.degree.currentIndex() + 1}, "
                    f"{self.form.currentIndex() + 1}, "
                    f"'{self.taste.text()}', "
                    f"{self.price.value()}, "
                    f"{self.volume.value()})")
        self.parent.con.commit()
        self.parent.update_table()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
