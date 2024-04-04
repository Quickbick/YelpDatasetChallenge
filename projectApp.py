import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QIcon, QPixmap
import psycopg2

qtCreatorFile = "ProjectUI.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class milestone2(QMainWindow):
    def __init__(self):
        super(milestone2, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.loadStatesYelp()
        self.loadCategories()
        self.ui.stateList_2.currentTextChanged.connect(self.stateChangedYelp)
        self.ui.cityList_2.itemSelectionChanged.connect(self.cityChangedYelp)
        self.ui.zipList.itemSelectionChanged.connect(self.zipChanged)
        self.ui.categoryList.itemSelectionChanged.connect(self.categoryChanged)

        #Legacy Code From Milestone 1
        self.loadStates()
        self.ui.stateList.currentTextChanged.connect(self.stateChanged)
        self.ui.cityList.itemSelectionChanged.connect(self.cityChanged)

    def executeSQL2(self, sqlStr):
        try:
            conn = psycopg2.connect("dbname='milestone2db' user='postgres' host='localhost' password='12345'") #dbname and password should match database and password for whoever will demo
        except:
            print('Unable to connect to the database!')
        curr = conn.cursor()
        curr.execute(sqlStr)
        conn.commit()
        results = curr.fetchall()
        conn.close()
        return results
    
    def loadStatesYelp(self):
        self.ui.stateList_2.clear()
        sqlStr = "SELECT distinct state  FROM Business ORDER BY state;" #check table name is correct after FROM
        try:
            results = self.executeSQL2(sqlStr)
            for row in results:
                self.ui.stateList_2.addItem(row[0])
        except:
            print("Query Failed")
        self.ui.stateList_2.setCurrentIndex(-1)
        self.ui.stateList_2.clearEditText()

    def loadCategories(self):
        self.ui.categoryList.clear()
        sqlStr = "SELECT distinct category  FROM Categories ORDER BY category"
        try:
            results = self.executeSQL2(sqlStr)
            for row in results:
                self.ui.categoryList.addItem(row[0])
        except:
            print("Query Failed")

    def stateChangedYelp(self):
        self.ui.categoryList.clearSelection()
        self.ui.cityList_2.clear()
        state = self.ui.stateList_2.currentText()
        if (self.ui.stateList_2.currentIndex() >=0):
            sqlStr = "SELECT distinct city FROM Business WHERE state ='" + state + "' ORDER BY city;" #check table name
            try:
                results = self.executeSQL2(sqlStr)
                for row in results:
                    self.ui.cityList_2.addItem(row[0])
            except:
                print("Query Failed")
            for i in reversed(range(self.ui.businessTable_2.rowCount())):
                self.ui.businessTable_2.removeRow(i)
            sqlStr = "SELECT name, city, state, zipcode FROM Business WHERE state ='" + state + "' ORDER BY city;"
            try:
                results = self.executeSQL2(sqlStr)
                style = "::section {""background-color: #f3f3f3; }"
                self.ui.businessTable_2.horizontalHeader().setStyleSheet(style)
                self.ui.businessTable_2.setColumnCount(len(results[0]))
                self.ui.businessTable_2.setRowCount(len(results))
                self.ui.businessTable_2.setHorizontalHeaderLabels(['Business Name', 'City', 'State', 'Zip Code'])
                self.ui.businessTable_2.resizeColumnsToContents()
                self.ui.businessTable_2.setColumnWidth(0,300)
                self.ui.businessTable_2.setColumnWidth(1,100)
                self.ui.businessTable_2.setColumnWidth(2,50)
                currentRowCount = 0
                for row in results:
                    for colCount in range (0, len(results[0])):
                        self.ui.businessTable_2.setItem(currentRowCount, colCount, QTableWidgetItem(row[colCount]))
                    currentRowCount += 1
            except:
                print("Query Failed")

    def cityChangedYelp(self):
        self.ui.categoryList.clearSelection()
        self.ui.zipList.clear()
        if (len(self.ui.cityList_2.selectedItems()) > 0):
            city = self.ui.cityList_2.selectedItems()[0].text()
            sqlStr = "SELECT distinct zipcode FROM Business WHERE city ='" + city + "' ORDER BY zipcode;" #check table name
            try:
                results = self.executeSQL2(sqlStr)
                for row in results:
                    self.ui.zipList.addItem(row[0])
            except:
                print("Query Failed")
            for i in reversed(range(self.ui.businessTable_2.rowCount())):
                self.ui.businessTable_2.removeRow(i)
            sqlStr = "SELECT name, city, state, zipcode FROM Business WHERE city ='" + city + "' ORDER BY zipcode;"
            try:
                results = self.executeSQL2(sqlStr)
                style = "::section {""background-color: #f3f3f3; }"
                self.ui.businessTable_2.horizontalHeader().setStyleSheet(style)
                self.ui.businessTable_2.setColumnCount(len(results[0]))
                self.ui.businessTable_2.setRowCount(len(results))
                self.ui.businessTable_2.setHorizontalHeaderLabels(['Business Name', 'City', 'State', 'Zip Code'])
                self.ui.businessTable_2.resizeColumnsToContents()
                self.ui.businessTable_2.setColumnWidth(0,300)
                self.ui.businessTable_2.setColumnWidth(1,100)
                self.ui.businessTable_2.setColumnWidth(2,50)
                currentRowCount = 0
                for row in results:
                    for colCount in range (0, len(results[0])):
                        self.ui.businessTable_2.setItem(currentRowCount, colCount, QTableWidgetItem(row[colCount]))
                    currentRowCount += 1
            except:
                print("Query Failed")

    def zipChanged(self):
        self.ui.categoryList.clearSelection()
        if (len(self.ui.zipList.selectedItems()) > 0):
            zip = self.ui.zipList.selectedItems()[0].text()
            for i in reversed(range(self.ui.businessTable_2.rowCount())):
                self.ui.businessTable_2.removeRow(i)
            sqlStr = "SELECT name, city, state, zipcode FROM business WHERE zipcode ='" + zip + "' ORDER BY name;"
            try:
                results = self.executeSQL2(sqlStr)
                style = "::section {""background-color: #f3f3f3; }"
                self.ui.businessTable_2.horizontalHeader().setStyleSheet(style)
                self.ui.businessTable_2.setColumnCount(len(results[0]))
                self.ui.businessTable_2.setRowCount(len(results))
                self.ui.businessTable_2.setHorizontalHeaderLabels(['Business Name', 'City', 'State', 'Zip Code'])
                self.ui.businessTable_2.resizeColumnsToContents()
                self.ui.businessTable_2.setColumnWidth(0,300)
                self.ui.businessTable_2.setColumnWidth(1,100)
                self.ui.businessTable_2.setColumnWidth(2,50)
                currentRowCount = 0
                for row in results:
                    for colCount in range (0, len(results[0])):
                        self.ui.businessTable_2.setItem(currentRowCount, colCount, QTableWidgetItem(row[colCount]))
                    currentRowCount += 1
            except:
                print("Query Failed")

    def categoryChanged(self):
        if (len(self.ui.categoryList.selectedItems()) > 0 & len(self.ui.categoryList.selectedItems()) > 0):
            category = self.ui.categoryList.selectedItems()[0].text()
            zip = self.ui.zipList.currentItem()
            for i in reversed(range(self.ui.businessTable_2.rowCount())):
                self.ui.businessTable_2.removeRow(i)
            sqlStr = "SELECT name, city, state, zip, category FROM business WHERE category ='" + category + "' AND zipcode ='" + zip + "' ORDER BY name;"
            try:
                results = self.executeSQL2(sqlStr)
                style = "::section {""background-color: #f3f3f3; }"
                self.ui.businessTable_2.horizontalHeader().setStyleSheet(style)
                self.ui.businessTable_2.setColumnCount(len(results[0]))
                self.ui.businessTable_2.setRowCount(len(results))
                self.ui.businessTable_2.setHorizontalHeaderLabels(['Business Name', 'City', 'State', 'Zip Code'])
                self.ui.businessTable_2.resizeColumnsToContents()
                self.ui.businessTable_2.setColumnWidth(0,300)
                self.ui.businessTable_2.setColumnWidth(1,100)
                self.ui.businessTable_2.setColumnWidth(2,50)
                currentRowCount = 0
                for row in results:
                    for colCount in range (0, len(results[0])):
                        self.ui.businessTable_2.setItem(currentRowCount, colCount, QTableWidgetItem(row[colCount]))
                    currentRowCount += 1
            except:
                print("Query Failed")


    #Legacy Code From Milestone 1 Below This
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
    window = milestone2()
    window.show()
    sys.exit(app.exec_())
