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

        # Success:
        self.ui.successfulRefresh.clicked.connect(self.succRefreshPressed)
        # Connection for popRefreshPressed:
        self.ui.popularRefresh.clicked.connect(self.popRefreshPressed)

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
            except Exception as e:
                print("[totalPop] Query Failed", e)
            sqlStr = "SELECT meanincome FROM zipcodedata WHERE zipcode ='" + zip + "';"
            try:
                results = self.executeSQL2(sqlStr)
                self.ui.averageIncome.setPlainText(str(results[0][0]))
            except Exception as e:
                print("[avgIncome] Query Failed", e)
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

    # TODO
    # New-new-new succRefreshPressed function to filter businesses based on average rating, no star ratings displayed (because opinions/subvective I suppose), and sort:
    def succRefreshPressed(self):

        for i in reversed(range(self.ui.businessTable_3.rowCount())):
            self.ui.businessTable_3.removeRow(i)

        if len(self.ui.zipList.selectedItems()) > 0:
            zip_code = self.ui.zipList.selectedItems()[0].text()
            average_rating = self.calculateAverageRatingZIP(zip_code) # calculateAverageRating above gets average rating of the state (ZIP is zip code)/
            if average_rating is not None:
                if len(self.ui.categoryList.selectedItems()) > 0:
                    category = self.ui.categoryList.selectedItems()[0].text()
                    sqlStr = "SELECT distinct name, street_add, city, num_reviews, review_rating, num_checkins FROM Business JOIN categories ON Business.id = Categories.business WHERE"
                    conditionsAdded = 0
                    sqlStr += " zipcode ='" + zip_code + "' AND review_rating > " + str(average_rating) + " AND category = '" + category + "' "
                    conditionsAdded += 1
                else:
                    sqlStr = "SELECT distinct name, street_add, city, num_reviews, review_rating, num_checkins FROM Business JOIN categories ON Business.id = Categories.business WHERE"
                    conditionsAdded = 0
                    sqlStr += " zipcode ='" + zip_code + "' AND review_rating > " + str(average_rating) + " "
                    conditionsAdded += 1

                sqlStr += "ORDER BY review_rating DESC, name;"  # Sort by Average Rating in descending order and then by Business Name
                try:
                    results = self.executeSQL2(sqlStr)
                    # style = "::section {""background-color: #f3f3f3; }"
                    style = "::section {""background-color: #FFE6E6; }" # @Override w/ Pink 
                    self.ui.businessTable_3.horizontalHeader().setStyleSheet(style)
                    self.ui.businessTable_3.setColumnCount(len(results[0]) - 1)  # Exclude Business Rating column
                    self.ui.businessTable_3.setRowCount(len(results))
                    self.ui.businessTable_3.setHorizontalHeaderLabels(['Business Name', 'Address', 'City', 'Number of Reviews', 'Average Rating', 'Number of Check-Ins'])
                    currentRowCount = 0
                    for row in results:
                        for colCount in range(0, len(results[0])):
                            if colCount != 3:  # Skip inserting Business Rating column
                                self.ui.businessTable_3.setItem(currentRowCount, colCount, QTableWidgetItem(str(row[colCount])))
                        currentRowCount += 1
                    self.ui.businessTable_3.resizeColumnsToContents()
                except Exception as e:
                    print("SuccRefresh Query Failed -> ", e)

        

    def calculateAverageRating(self, city):
        sqlStr = "SELECT AVG(review_rating) FROM Business WHERE city = '" + city + "'"
        try:
            result = self.executeSQL2(sqlStr)
            if result and result[0][0]:
                return result[0][0]
            else:
                return None
        except Exception as e:
            print("Failed to calculate average rating:", e)
            return None
        
    def calculateAverageRatingZIP(self, zip_code):
        sqlStr = "SELECT AVG(review_rating) FROM Business WHERE zipcode = '" + zip_code + "'"
        try:
            result = self.executeSQL2(sqlStr)
            if result and result[0][0]:
                return result[0][0]
            else:
                return None
        except Exception as e:
            print("Failed to calculate average rating:", e)
            return None
        

    # TODO        
    # Function to determine and display popular businesses
    def popRefreshPressed(self):
        for i in reversed(range(self.ui.businessTable_2.rowCount())):
            self.ui.businessTable_2.removeRow(i)
        
        if len(self.ui.zipList.selectedItems()) > 0:
            zip_code = self.ui.zipList.selectedItems()[0].text()
            if len(self.ui.categoryList.selectedItems()) > 0:
                category = self.ui.categoryList.selectedItems()[0].text()
                
                # Query to calculate average num_checkins and num_reviews for the given zip code and category
                avg_checkins_sql = "SELECT AVG(num_checkins) FROM Business WHERE zipcode = '" + zip_code + "' AND id IN (SELECT business FROM Categories WHERE category = '" + category + "')"
                avg_reviews_sql = "SELECT AVG(num_reviews) FROM Business WHERE zipcode = '" + zip_code + "' AND id IN (SELECT business FROM Categories WHERE category = '" + category + "')"
                
                try:
                    avg_checkins = self.executeSQL2(avg_checkins_sql)[0][0]
                    avg_reviews = self.executeSQL2(avg_reviews_sql)[0][0]
                    
                    # Query to fetch popular businesses
                    # popular_sql = "SELECT name, street_add, city, num_reviews, review_rating, num_checkins FROM Business WHERE zipcode = '" + zip_code + "' AND id IN (SELECT business FROM Categories WHERE category = '" + category + "') AND num_reviews > " + str(avg_reviews) + " AND num_checkins > " + str(avg_checkins) + " ORDER BY num_reviews DESC"
                    popular_sql = "SELECT name, street_add, city, num_reviews, review_rating, num_checkins FROM Business WHERE zipcode = '" + zip_code + "' AND id IN (SELECT business FROM Categories WHERE category = '" + category + "') AND num_reviews > " + str(avg_reviews) + " AND num_checkins > " + str(avg_checkins) + " ORDER BY num_reviews DESC, num_checkins DESC, name ASC"
                    
                    try:
                        results = self.executeSQL2(popular_sql)
                        
                        style = "::section {""background-color: #e6e6fa; }"  # Light violet colored
                        self.ui.businessTable_2.horizontalHeader().setStyleSheet(style)
                        self.ui.businessTable_2.setColumnCount(len(results[0]))
                        self.ui.businessTable_2.setRowCount(len(results))
                        self.ui.businessTable_2.setHorizontalHeaderLabels(['Business Name', 'Address', 'City', 'Number of Reviews', 'Average Rating', 'Number of Check-Ins'])
                        
                        currentRowCount = 0
                        for row in results:
                            for colCount in range(0, len(results[0])):
                                self.ui.businessTable_2.setItem(currentRowCount, colCount, QTableWidgetItem(str(row[colCount])))
                            currentRowCount += 1
                        
                        self.ui.businessTable_2.resizeColumnsToContents()
                    
                    except Exception as e:
                        print("PopRefresh Query Failed -> ", e)
                
                except Exception as e:
                    print("Failed to calculate average checkins and reviews:", e)
    

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


# JOHNS COMMENTS during working (pls don't delete until finished with popularity, too, I ref these):
"""
        for i in reversed(range(self.ui.businessTable_3.rowCount())):
            self.ui.businessTable_3.removeRow(i)

        if len(self.ui.cityList.selectedItems()) > 0:
            city = self.ui.cityList.selectedItems()[0].text()
            average_rating = self.calculateAverageRating(city) # calculateAverageRating above gets average rating of the city.
            if average_rating is not None:
                if len(self.ui.categoryList.selectedItems()) > 0:
                    category = self.ui.categoryList.selectedItems()[0].text()
                    sqlStr = "SELECT distinct name, street_add, city, num_reviews, review_rating, num_checkins FROM Business JOIN categories ON Business.id = Categories.business WHERE"
                    conditionsAdded = 0
                    sqlStr += " city ='" + city + "' AND review_rating > " + str(average_rating) + " AND category = '" + category + "' "
                    conditionsAdded += 1
                else:
                    sqlStr = "SELECT distinct name, street_add, city, num_reviews, review_rating, num_checkins FROM Business JOIN categories ON Business.id = Categories.business WHERE"
                    conditionsAdded = 0
                    sqlStr += " city ='" + city + "' AND review_rating > " + str(average_rating) + " "
                    conditionsAdded += 1

                sqlStr += "ORDER BY review_rating DESC, name;"  # Sort by Average Rating in descending order and then by Business Name
                try:
                    results = self.executeSQL2(sqlStr)
                    # style = "::section {""background-color: #f3f3f3; }"
                    style = "::section {""background-color: #FFE6E6; }" # @Override w/ Pink 
                    self.ui.businessTable_3.horizontalHeader().setStyleSheet(style)
                    self.ui.businessTable_3.setColumnCount(len(results[0]) - 1)  # Exclude Business Rating column
                    self.ui.businessTable_3.setRowCount(len(results))
                    self.ui.businessTable_3.setHorizontalHeaderLabels(['Business Name', 'Address', 'City', 'Number of Reviews', 'Average Rating', 'Number of Check-Ins'])
                    currentRowCount = 0
                    for row in results:
                        for colCount in range(0, len(results[0])):
                            if colCount != 3:  # Skip inserting Business Rating column
                                self.ui.businessTable_3.setItem(currentRowCount, colCount, QTableWidgetItem(str(row[colCount])))
                        currentRowCount += 1
                    self.ui.businessTable_3.resizeColumnsToContents()
                except Exception as e:
                    print("SuccRefresh Query Failed -> ", e)
"""

"""
        for i in reversed(range(self.ui.businessTable_3.rowCount())):
            self.ui.businessTable_3.removeRow(i)

        if len(self.ui.cityList.selectedItems()) > 0:
            city = self.ui.cityList.selectedItems()[0].text()
            average_rating = self.calculateAverageRating(city) # calculateAverageRating above gets average rating of the city.
            if average_rating is not None:
                sqlStr = "SELECT distinct name, street_add, city, num_reviews, review_rating, num_checkins FROM Business JOIN categories ON Business.id = Categories.business WHERE"
                conditionsAdded = 0
                sqlStr += " city ='" + city + "' AND review_rating > " + str(average_rating) + " "
                conditionsAdded += 1
                sqlStr += "ORDER BY review_rating DESC, name;"  # Sort by Average Rating in descending order and then by Business Name
                try:
                    results = self.executeSQL2(sqlStr)
                    # style = "::section {""background-color: #f3f3f3; }"
                    style = "::section {""background-color: #FFE6E6; }" # @Override w/ Pink 
                    self.ui.businessTable_3.horizontalHeader().setStyleSheet(style)
                    self.ui.businessTable_3.setColumnCount(len(results[0]) - 1)  # Exclude Business Rating column
                    self.ui.businessTable_3.setRowCount(len(results))
                    self.ui.businessTable_3.setHorizontalHeaderLabels(['Business Name', 'Address', 'City', 'Number of Reviews', 'Average Rating', 'Number of Check-Ins'])
                    currentRowCount = 0
                    for row in results:
                        for colCount in range(0, len(results[0])):
                            if colCount != 3:  # Skip inserting Business Rating column
                                self.ui.businessTable_3.setItem(currentRowCount, colCount, QTableWidgetItem(str(row[colCount])))
                        currentRowCount += 1
                    self.ui.businessTable_3.resizeColumnsToContents()
                except Exception as e:
                    print("SuccRefresh Query Failed -> ", e)
"""

"""
        for i in reversed(range(self.ui.businessTable_3.rowCount())):
            self.ui.businessTable_3.removeRow(i)

        if len(self.ui.cityList.selectedItems()) > 0:
            city = self.ui.cityList.selectedItems()[0].text()
            average_rating = self.calculateAverageRating(city)
            if average_rating is not None:
                sqlStr = "SELECT name, street_add, city, stars, num_reviews, review_rating, num_checkins " \
                        "FROM Business JOIN Categories ON Business.id = Categories.business " \
                        "WHERE city ='" + city + "' AND review_rating > " + str(average_rating) + " " \
                        "ORDER BY name;"
                try:
                    results = self.executeSQL2(sqlStr)
                    style = "::section {""background-color: #f3f3f3; }"
                    self.ui.businessTable_3.horizontalHeader().setStyleSheet(style)
                    self.ui.businessTable_3.setColumnCount(len(results[0]))
                    self.ui.businessTable_3.setRowCount(len(results))
                    self.ui.businessTable_3.setHorizontalHeaderLabels(['Business Name', 'Address', 'City', 'Business Rating', 'Number of Reviews', 'Average Rating', 'Number of Check-Ins'])
                    currentRowCount = 0
                    for row in results:
                        for colCount in range(0, len(results[0])):
                            self.ui.businessTable_3.setItem(currentRowCount, colCount, QTableWidgetItem(str(row[colCount])))
                        currentRowCount += 1
                    self.ui.businessTable_3.resizeColumnsToContents()
                except Exception as e:
                    print("SuccRefresh Query Failed -> ", e)
"""
"""
    def succRefreshPressed(self):
        for i in reversed(range(self.ui.businessTable_3.rowCount())):
            self.ui.businessTable_3.removeRow(i)
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
            self.ui.businessTable_3.horizontalHeader().setStyleSheet(style)
            self.ui.businessTable_3.setColumnCount(len(results[0]))
            self.ui.businessTable_3.setRowCount(len(results))
            self.ui.businessTable_3.setHorizontalHeaderLabels(['Business Name', 'Address', 'City', 'Business Rating', 'Number of Reviews', 'Average Rating', 'Number of Check-Ins'])
            currentRowCount = 0
            for row in results:
                for colCount in range (0, len(results[0])):
                    self.ui.businessTable_3.setItem(currentRowCount, colCount, QTableWidgetItem(str(row[colCount])))
                currentRowCount += 1
            self.ui.businessTable_3.resizeColumnsToContents()
        except Exception as e:
            print("SuccRefresh Query Failed -> ", e)
        # pass
"""
# Old pop attempts
"""
    def popRefreshPressed(self):
        for i in reversed(range(self.ui.businessTable_2.rowCount())):
            self.ui.businessTable_2.removeRow(i)

        if len(self.ui.zipList.selectedItems()) > 0:
            zip_code = self.ui.zipList.selectedItems()[0].text()
            average_num_reviews = self.calculateAverageNumReviewsZIP(zip_code) 
            average_num_checkins = self.calculateAverageNumCheckinsZIP(zip_code) 

            if average_num_reviews is not None and average_num_checkins is not None:
                if len(self.ui.categoryList.selectedItems()) > 0:
                    category = self.ui.categoryList.selectedItems()[0].text()
                    sqlStr = "SELECT distinct name, street_add, city, num_reviews, num_checkins FROM Business WHERE"
                    conditionsAdded = 0
                    sqlStr += " zipcode ='" + zip_code + "' AND num_reviews > " + str(average_num_reviews) + " AND num_checkins > " + str(average_num_checkins) + " AND category = '" + category + "' "
                    conditionsAdded += 1
                else:
                    sqlStr = "SELECT distinct name, street_add, city, num_reviews, num_checkins FROM Business WHERE"
                    conditionsAdded = 0
                    sqlStr += " zipcode ='" + zip_code + "' AND num_reviews > " + str(average_num_reviews) + " AND num_checkins > " + str(average_num_checkins) + " "
                    conditionsAdded += 1

                sqlStr += "ORDER BY name;"
                try:
                    results = self.executeSQL2(sqlStr)
                    style = "::section {""background-color: #e6e6fa; }"  # Light purple/violet color
                    self.ui.businessTable_2.horizontalHeader().setStyleSheet(style)
                    self.ui.businessTable_2.setColumnCount(len(results[0]))
                    self.ui.businessTable_2.setRowCount(len(results))
                    self.ui.businessTable_2.setHorizontalHeaderLabels(['Business Name', 'Address', 'City', 'Number of Reviews', 'Number of Check-Ins'])
                    currentRowCount = 0
                    for row in results:
                        for colCount in range(0, len(results[0])):
                            self.ui.businessTable_2.setItem(currentRowCount, colCount, QTableWidgetItem(str(row[colCount])))
                        currentRowCount += 1
                    self.ui.businessTable_2.resizeColumnsToContents()
                except Exception as e:
                    print("PopRefresh Query Failed -> ", e)
"""