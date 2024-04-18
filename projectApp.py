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
        self.loadStates()
        self.loadCategories()
        self.ui.numBusinesses.setReadOnly(True)
        self.ui.totalPop.setReadOnly(True)
        self.ui.averageIncome.setReadOnly(True)
        style = "::section {""background-color: #ede8da; }"
        self.ui.numBusinesses.setStyleSheet(style)
        self.ui.totalPop.setStyleSheet(style)
        self.ui.averageIncome.setStyleSheet(style)
        self.ui.stateList.currentTextChanged.connect(self.stateChanged)
        self.ui.cityList.itemSelectionChanged.connect(self.cityChanged)
        self.ui.zipList.itemSelectionChanged.connect(self.zipChanged)
        self.ui.searchButton.clicked.connect(self.searchPressed)
        self.ui.categoryList.itemSelectionChanged.connect(self.categoryChanged)

    def executeSQL(self, sqlStr):
        try:
            conn = psycopg2.connect("dbname='milestone2db' user='postgres' host='localhost' password='12345'") #dbname and password should match database and password for whoever will demo
        except:
            print('Unable to connect to the database!')
        curr = conn.cursor()
        curr.execute(sqlStr)
        conn.commit()
        conn.close()

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
    
    #loads states into box
    def loadStates(self):
        self.ui.stateList.clear()
        sqlStr = "SELECT distinct state  FROM Business ORDER BY state;" #check table name is correct after FROM
        try:
            results = self.executeSQL2(sqlStr)
            for row in results:
                self.ui.stateList.addItem(row[0])
        except:
            print("Query Failed")
        self.ui.stateList.setCurrentIndex(-1)
        self.ui.stateList.clearEditText()

    def loadCategories(self):
        self.ui.categoryList.clear()
        sqlStr = "SELECT distinct category  FROM Categories ORDER BY category"
        try:
            results = self.executeSQL2(sqlStr)
            for row in results:
                self.ui.categoryList.addItem(row[0])
        except:
            print("Query Failed")

    def stateChanged(self):
        self.clearAll()
        self.ui.categoryList.clearSelection()
        self.ui.cityList.clear()
        state = self.ui.stateList.currentText()
        if (self.ui.stateList.currentIndex() >=0):
            sqlStr = "SELECT distinct city FROM Business WHERE state ='" + state + "' ORDER BY city;" #check table name
            try:
                results = self.executeSQL2(sqlStr)
                for row in results:
                    self.ui.cityList.addItem(row[0])
            except:
                print("Query Failed")

    def cityChanged(self):
        self.clearAll()
        self.ui.categoryList.clearSelection()
        self.ui.zipList.clear()
        if (len(self.ui.cityList.selectedItems()) > 0):
            city = self.ui.cityList.selectedItems()[0].text()
            sqlStr = "SELECT distinct zipcode FROM Business WHERE city ='" + city + "' ORDER BY zipcode;" #check table name
            try:
                results = self.executeSQL2(sqlStr)
                for row in results:
                    self.ui.zipList.addItem(row[0])
            except:
                print("Query Failed")

    def zipChanged(self):
        self.clearAll()
        if (len(self.ui.zipList.selectedItems()) > 0):
            zip = self.ui.zipList.selectedItems()[0].text()
            sqlStr = "SELECT COUNT(distinct id) FROM Business WHERE zipcode ='" + zip + "';"
            try:
                results = self.executeSQL2(sqlStr)
                self.ui.numBusinesses.setPlainText(str(results[0][0]))
            except:
                print("Query Failed")
            sqlStr = "SELECT population FROM zipcodedata WHERE zipcode ='" + zip + "';"
            try:
                results = self.executeSQL2(sqlStr)
                self.ui.totalPop.setPlainText(str(results[0][0]))
            except:
                print("Query Failed")
            sqlStr = "SELECT meanincome FROM zipcodedata WHERE zipcode ='" + zip + "';"
            try:
                results = self.executeSQL2(sqlStr)
                self.ui.averageIncome.setPlainText(str(results[0][0]))
            except:
                print("Query Failed")  
            for i in reversed(range(self.ui.categoryTable.rowCount())):
                self.ui.categoryTable.removeRow(i)
            sqlStr = "CREATE TABLE ZipAggregates AS SELECT zipcode, category, count(id) FROM Business b LEFT JOIN Categories c ON b.id = c.business GROUP BY b.zipcode, c.category;"
            try:
                self.executeSQL(sqlStr)
            except:
                print("Query Failed") 
            sqlStr = "SELECT count, category FROM ZipAggregates WHERE zipcode ='" + zip + "' ORDER BY count DESC;"
            try:
                results = self.executeSQL2(sqlStr)
                style = "::section {""background-color: #f3f3f3; }"
                self.ui.categoryTable.horizontalHeader().setStyleSheet(style)
                self.ui.categoryTable.setColumnCount(len(results[0]))
                self.ui.categoryTable.setRowCount(len(results))
                self.ui.categoryTable.setHorizontalHeaderLabels(['Businesses', 'Category'])
                currentRowCount = 0
                for row in results:
                    for colCount in range (0, len(results[0])):
                        self.ui.categoryTable.setItem(currentRowCount, colCount, QTableWidgetItem(str(row[colCount])))
                    currentRowCount += 1
                self.ui.categoryTable.resizeColumnsToContents()
            except:
                print("Query Failed")
            self.ui.categoryList.clear()
            sqlStr = "SELECT distinct category FROM ZipAggregates WHERE zipcode ='" + zip + "' ORDER BY category"
            results = self.executeSQL2(sqlStr)
            for row in results:
                self.ui.categoryList.addItem(row[0])
            sqlStr = "DROP TABLE IF EXISTS ZipAggregates;"
            try:
                self.executeSQL(sqlStr)
            except:
                print("Query Failed") 

    def searchPressed(self):
        for i in reversed(range(self.ui.businessTable.rowCount())):
            self.ui.businessTable.removeRow(i)
        sqlStr = "SELECT distinct name, street_add, city, stars, num_reviews, review_rating, num_checkins FROM Business JOIN categories ON Business.id = Categories.business WHERE"
        conditionsAdded = 0
        if (self.ui.stateList.currentIndex() >=0):
            state = self.ui.stateList.currentText()
            sqlStr = sqlStr + " state ='" + state + "' "
            conditionsAdded += 1
        if (len(self.ui.cityList.selectedItems()) > 0):
            city = self.ui.cityList.selectedItems()[0].text()
            if (conditionsAdded >= 1):
                sqlStr = sqlStr + "AND "
            sqlStr = sqlStr + "city ='" + city + "' "
            conditionsAdded += 1
        if (len(self.ui.zipList.selectedItems()) > 0):
            zip = self.ui.zipList.selectedItems()[0].text()
            if (conditionsAdded >= 1):
                sqlStr = sqlStr + "AND "
            sqlStr = sqlStr + "zipcode ='" + zip + "' "
            conditionsAdded += 1
        if (len(self.ui.categoryList.selectedItems()) > 0):
            category = self.ui.categoryList.selectedItems()[0].text()
            if (conditionsAdded >= 1):
                sqlStr = sqlStr + "AND "
            sqlStr = sqlStr + "category ='" + category + "' "
            conditionsAdded += 1
        sqlStr = sqlStr + "ORDER BY name;"
        try:
            results = self.executeSQL2(sqlStr)
            style = "::section {""background-color: #f3f3f3; }"
            self.ui.businessTable.horizontalHeader().setStyleSheet(style)
            self.ui.businessTable.setColumnCount(len(results[0]))
            self.ui.businessTable.setRowCount(len(results))
            self.ui.businessTable.setHorizontalHeaderLabels(['Business Name', 'Address', 'City', 'Business Rating', 'Number of Reviews', 'Average Rating', 'Number of Check-Ins'])
            currentRowCount = 0
            for row in results:
                for colCount in range (0, len(results[0])):
                    self.ui.businessTable.setItem(currentRowCount, colCount, QTableWidgetItem(str(row[colCount])))
                currentRowCount += 1
            self.ui.businessTable.resizeColumnsToContents()
        except:
            print("Query Failed")

    def categoryChanged(self):
        for i in reversed(range(self.ui.businessTable.rowCount())):
            self.ui.businessTable.removeRow(i)
        for i in reversed(range(self.ui.businessTable_2.rowCount())):
            self.ui.businessTable_2.removeRow(i)
        for i in reversed(range(self.ui.businessTable_3.rowCount())):
            self.ui.businessTable_3.removeRow(i)

    def clearAll(self):
        for i in reversed(range(self.ui.businessTable.rowCount())):
            self.ui.businessTable.removeRow(i)
        for i in reversed(range(self.ui.businessTable_2.rowCount())):
            self.ui.businessTable_2.removeRow(i)
        for i in reversed(range(self.ui.businessTable_3.rowCount())):
            self.ui.businessTable_3.removeRow(i)
        for i in reversed(range(self.ui.categoryTable.rowCount())):
                self.ui.categoryTable.removeRow(i)
        self.ui.categoryList.clear()
        self.ui.numBusinesses.clear()
        self.ui.totalPop.clear()
        self.ui.averageIncome.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = milestone2()
    window.show()
    sys.exit(app.exec_())


#Variables For GUI Access
# Popular Business Table - businessTable_2
# Successful Business Table - businessTable_3
# Popular Refresh Button - popularRefresh
# Successful Refresh Button - successfulRefresh