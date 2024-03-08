import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QIcon, QPixmap
import psycopg2

qtCreatorFile = "ProjectUI.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class milestone1(QMainWindow):
    def __init__(self):
        super(milestone1, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.loadStates()
        self.ui.stateList.currentTextChanged.connect(self.stateChanged)
        self.ui.cityList.itemSelectionChanged.connect(self.cityChanged)

    def executeSQL(self, sqlStr):
        try:
            conn = psycopg2.connect("dbname='milestone1db' user='postgres' host='localhost' password='12345'")
        except:
            print('Unable to connect to the database!')
        curr = conn.cursor()
        curr.execute(sqlStr)
        conn.commit()
        results = curr.fetchall()
        conn.close()
        return results

    def loadStates(self):
        self.ui.stateList.clear()
        sqlStr = "SELECT distinct state  FROM business ORDER BY state;"
        try:
            results = self.executeSQL(sqlStr)
            for row in results:
                self.ui.stateList.addItem(row[0])
        except:
            print("Query Failed")
        self.ui.stateList.setCurrentIndex(-1)
        self.ui.stateList.clearEditText()

    def stateChanged(self):
        self.ui.cityList.clear()
        state = self.ui.stateList.currentText()
        if (self.ui.stateList.currentIndex() >=0):
            sqlStr = "SELECT distinct city FROM business WHERE state ='" + state + "' ORDER BY city;"
            try:
                results = self.executeSQL(sqlStr)
                for row in results:
                    self.ui.cityList.addItem(row[0])
            except:
                print("Query Failed")
            for i in reversed(range(self.ui.businessTable.rowCount())):
                self.ui.businessTable.removeRow(i)
            sqlStr = "SELECT name, city, state FROM business WHERE state ='" + state + "' ORDER BY city;"
            try:
                results = self.executeSQL(sqlStr)
                style = "::section {""background-color: #f3f3f3; }"
                self.ui.businessTable.horizontalHeader().setStyleSheet(style)
                self.ui.businessTable.setColumnCount(len(results[0]))
                self.ui.businessTable.setRowCount(len(results))
                self.ui.businessTable.setHorizontalHeaderLabels(['Business Name', 'City', 'State'])
                self.ui.businessTable.resizeColumnsToContents()
                self.ui.businessTable.setColumnWidth(0,300)
                self.ui.businessTable.setColumnWidth(1,100)
                self.ui.businessTable.setColumnWidth(2,50)
                currentRowCount = 0
                for row in results:
                    for colCount in range (0, len(results[0])):
                        self.ui.businessTable.setItem(currentRowCount, colCount, QTableWidgetItem(row[colCount]))
                    currentRowCount += 1
            except:
                print("Query Failed")

    def cityChanged(self):
        if (self.ui.stateList.currentIndex() >=0) and (len(self.ui.cityList.selectedItems()) > 0):
            state = self.ui.stateList.currentText()
            city = self.ui.cityList.selectedItems()[0].text()
            sqlStr = "SELECT name, city, state FROM business WHERE state ='" + state + "' AND city ='" + city + "' ORDER BY name;"
            try:
                results = self.executeSQL(sqlStr)
                style = "::section {""background-color: #f3f3f3; }"
                self.ui.businessTable.horizontalHeader().setStyleSheet(style)
                self.ui.businessTable.setColumnCount(len(results[0]))
                self.ui.businessTable.setRowCount(len(results))
                self.ui.businessTable.setHorizontalHeaderLabels(['Business Name', 'City', 'State'])
                self.ui.businessTable.resizeColumnsToContents()
                self.ui.businessTable.setColumnWidth(0,300)
                self.ui.businessTable.setColumnWidth(1,100)
                self.ui.businessTable.setColumnWidth(2,50)
                currentRowCount = 0
                for row in results:
                    for colCount in range (0, len(results[0])):
                        self.ui.businessTable.setItem(currentRowCount, colCount, QTableWidgetItem(row[colCount]))
                    currentRowCount += 1
            except:
                print("Query Failed")
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = milestone1()
    window.show()
    sys.exit(app.exec_())
