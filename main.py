# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Qt Designer.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import optimizer

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(20, 40, 761, 481))
        self.tabWidget.setObjectName("tabWidget")
        self.Model = QtWidgets.QWidget()
        self.Model.setObjectName("Model")
        self.frame = QtWidgets.QFrame(self.Model)
        self.frame.setGeometry(QtCore.QRect(10, 10, 731, 431))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.stackedWidget = QtWidgets.QStackedWidget(self.frame)
        self.stackedWidget.setGeometry(QtCore.QRect(10, 10, 421, 311))
        self.stackedWidget.setObjectName("stackedWidget")
        self.Home = QtWidgets.QWidget()
        self.Home.setObjectName("Home")
        self.label_6 = QtWidgets.QLabel(self.Home)
        self.label_6.setGeometry(QtCore.QRect(10, 20, 401, 271))
        self.label_6.setText("")
        self.label_6.setPixmap(QtGui.QPixmap("assets/variables.png"))
        self.label_6.setScaledContents(False)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.stackedWidget.addWidget(self.Home)
        self.Dm_page = QtWidgets.QWidget()
        self.Dm_page.setObjectName("Dm_page")
        self.label = QtWidgets.QLabel(self.Dm_page)
        self.label.setGeometry(QtCore.QRect(130, 90, 60, 16))
        self.label.setObjectName("label")
        self.stackedWidget.addWidget(self.Dm_page)
        self.Df_page = QtWidgets.QWidget()
        self.Df_page.setObjectName("Df_page")
        self.label_2 = QtWidgets.QLabel(self.Df_page)
        self.label_2.setGeometry(QtCore.QRect(200, 100, 60, 16))
        self.label_2.setObjectName("label_2")
        self.stackedWidget.addWidget(self.Df_page)
        self.D_page = QtWidgets.QWidget()
        self.D_page.setObjectName("D_page")
        self.label_3 = QtWidgets.QLabel(self.D_page)
        self.label_3.setGeometry(QtCore.QRect(220, 150, 60, 16))
        self.label_3.setObjectName("label_3")
        self.stackedWidget.addWidget(self.D_page)
        self.Wm_page = QtWidgets.QWidget()
        self.Wm_page.setObjectName("Wm_page")
        self.label_4 = QtWidgets.QLabel(self.Wm_page)
        self.label_4.setGeometry(QtCore.QRect(280, 170, 60, 16))
        self.label_4.setObjectName("label_4")
        self.stackedWidget.addWidget(self.Wm_page)
        self.N_page = QtWidgets.QWidget()
        self.N_page.setObjectName("N_page")
        self.label_5 = QtWidgets.QLabel(self.N_page)
        self.label_5.setGeometry(QtCore.QRect(280, 160, 60, 16))
        self.label_5.setObjectName("label_5")
        self.stackedWidget.addWidget(self.N_page)
        self.groupBox = QtWidgets.QGroupBox(self.frame)
        self.groupBox.setGeometry(QtCore.QRect(450, 176, 256, 231))
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.btn_Dm = QtWidgets.QPushButton(self.groupBox)
        self.btn_Dm.setObjectName("btn_Dm")
        self.verticalLayout.addWidget(self.btn_Dm)
        self.btn_Df = QtWidgets.QPushButton(self.groupBox)
        self.btn_Df.setObjectName("btn_Df")
        self.verticalLayout.addWidget(self.btn_Df)
        self.btn_D = QtWidgets.QPushButton(self.groupBox)
        self.btn_D.setObjectName("btn_D")
        self.verticalLayout.addWidget(self.btn_D)
        self.btn_Wm = QtWidgets.QPushButton(self.groupBox)
        self.btn_Wm.setObjectName("btn_Wm")
        self.verticalLayout.addWidget(self.btn_Wm)
        self.btn_N = QtWidgets.QPushButton(self.groupBox)
        self.btn_N.setObjectName("btn_N")
        self.verticalLayout.addWidget(self.btn_N)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.textBrowser_model = QtWidgets.QTextBrowser(self.frame)
        self.textBrowser_model.setGeometry(QtCore.QRect(450, 30, 256, 141))
        self.textBrowser_model.setObjectName("textBrowser_model")
        self.groupBox_8 = QtWidgets.QGroupBox(self.frame)
        self.groupBox_8.setGeometry(QtCore.QRect(19, 319, 411, 91))
        self.groupBox_8.setObjectName("groupBox_8")
        self.tabWidget.addTab(self.Model, "")
        self.Optimizer = QtWidgets.QWidget()
        self.Optimizer.setObjectName("Optimizer")
        self.groupBox_2 = QtWidgets.QGroupBox(self.Optimizer)
        self.groupBox_2.setGeometry(QtCore.QRect(390, 10, 351, 211))
        self.groupBox_2.setObjectName("groupBox_2")
        self.tableWidget = QtWidgets.QTableWidget(self.groupBox_2)
        self.tableWidget.setGeometry(QtCore.QRect(10, 30, 331, 171))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(5)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        
        # Connect signal to slot
        self.tableWidget.cellChanged.connect(lambda row, col: self.on_tableWidget_cellChanged(row, col, self.textBrowser_output))

        # Attributes to store values
        self.tableValues = [[None] * self.tableWidget.columnCount() for _ in range(self.tableWidget.rowCount())]

        self.groupBox_3 = QtWidgets.QGroupBox(self.Optimizer)
        self.groupBox_3.setGeometry(QtCore.QRect(390, 230, 351, 121))
        self.groupBox_3.setObjectName("groupBox_3")
        self.pushButton = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton.setGeometry(QtCore.QRect(10, 20, 113, 32))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 50, 113, 32))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_3.setGeometry(QtCore.QRect(230, 20, 113, 32))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_4.setGeometry(QtCore.QRect(120, 20, 113, 32))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_5.setGeometry(QtCore.QRect(230, 50, 113, 32))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_6 = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_6.setGeometry(QtCore.QRect(120, 50, 113, 32))
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_8 = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_8.setGeometry(QtCore.QRect(10, 80, 113, 32))
        self.pushButton_8.setObjectName("pushButton_8")
        self.pushButton_7 = QtWidgets.QPushButton(self.Optimizer)
        self.pushButton_7.setGeometry(QtCore.QRect(500, 370, 113, 32))
        self.pushButton_7.setObjectName("pushButton_7")
        self.stackedWidget_2 = QtWidgets.QStackedWidget(self.Optimizer)
        self.stackedWidget_2.setGeometry(QtCore.QRect(9, 9, 371, 431))
        self.stackedWidget_2.setObjectName("stackedWidget_2")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.label_7 = QtWidgets.QLabel(self.page)
        self.label_7.setGeometry(QtCore.QRect(0, 0, 351, 291))
        self.label_7.setText("")
        self.label_7.setPixmap(QtGui.QPixmap("Images/Optimizer/Picture1.png"))
        self.label_7.setObjectName("label_7")
        self.groupBox_9 = QtWidgets.QGroupBox(self.page)
        self.groupBox_9.setGeometry(QtCore.QRect(-1, 299, 371, 131))
        self.groupBox_9.setObjectName("groupBox_9")
        self.textBrowser_optimizer = QtWidgets.QTextBrowser(self.groupBox_9)
        self.textBrowser_optimizer.setGeometry(QtCore.QRect(0, 21, 371, 191))
        self.textBrowser_optimizer.setObjectName("textBrowser_optimizer")
        self.stackedWidget_2.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.stackedWidget_2.addWidget(self.page_2)
        self.tabWidget.addTab(self.Optimizer, "")
        self.Output = QtWidgets.QWidget()
        self.Output.setObjectName("Output")
        self.stackedWidget_3 = QtWidgets.QStackedWidget(self.Output)
        self.stackedWidget_3.setGeometry(QtCore.QRect(10, 10, 371, 331))
        self.stackedWidget_3.setObjectName("stackedWidget_3")
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setObjectName("page_3")
        self.label_8 = QtWidgets.QLabel(self.page_3)
        self.label_8.setGeometry(QtCore.QRect(20, 30, 341, 271))
        self.label_8.setText("")
        self.label_8.setPixmap(QtGui.QPixmap("Images/Output/Picture1.png"))
        self.label_8.setScaledContents(True)
        self.label_8.setObjectName("label_8")
        self.stackedWidget_3.addWidget(self.page_3)
        self.page_4 = QtWidgets.QWidget()
        self.page_4.setObjectName("page_4")
        self.stackedWidget_3.addWidget(self.page_4)
        self.groupBox_4 = QtWidgets.QGroupBox(self.Output)
        self.groupBox_4.setGeometry(QtCore.QRect(400, 9, 341, 211))
        self.groupBox_4.setObjectName("groupBox_4")
        self.textBrowser_output = QtWidgets.QTextBrowser(self.groupBox_4)
        self.textBrowser_output.setGeometry(QtCore.QRect(40, 40, 251, 151))
        self.textBrowser_output.setObjectName("textBrowser_output")
        self.groupBox_5 = QtWidgets.QGroupBox(self.Output)
        self.groupBox_5.setGeometry(QtCore.QRect(400, 230, 341, 101))
        self.groupBox_5.setObjectName("groupBox_5")
        self.groupBox_6 = QtWidgets.QGroupBox(self.Output)
        self.groupBox_6.setGeometry(QtCore.QRect(400, 340, 341, 101))
        self.groupBox_6.setObjectName("groupBox_6")
        self.groupBox_7 = QtWidgets.QGroupBox(self.Output)
        self.groupBox_7.setGeometry(QtCore.QRect(10, 370, 371, 71))
        self.groupBox_7.setObjectName("groupBox_7")
        self.progressBar = QtWidgets.QProgressBar(self.groupBox_7)
        self.progressBar.setGeometry(QtCore.QRect(10, 30, 351, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.tabWidget.addTab(self.Output, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 36))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.stackedWidget.setCurrentIndex(0)
        self.stackedWidget_2.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Dm"))
        self.label_2.setText(_translate("MainWindow", "Df"))
        self.label_3.setText(_translate("MainWindow", "D"))
        self.label_4.setText(_translate("MainWindow", "Wm"))
        self.label_5.setText(_translate("MainWindow", "N"))
        self.groupBox.setTitle(_translate("MainWindow", "Design Variables"))
        self.btn_Dm.setText(_translate("MainWindow", "Dm: mean tire diameter"))
        self.btn_Df.setText(_translate("MainWindow", "Df: outer wheel flange diamter"))
        self.btn_D.setText(_translate("MainWindow", "D: rim diameter"))
        self.btn_Wm.setText(_translate("MainWindow", "Wm: mean overall tire width"))
        self.btn_N.setText(_translate("MainWindow", "N: ply rating"))
        self.textBrowser_model.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'.AppleSystemUIFont\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Background of the following design variables</p></body></html>"))
        self.groupBox_8.setTitle(_translate("MainWindow", "Welcome!"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Model), _translate("MainWindow", "Model"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Optimization Varaibles (optional)"))
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "Dm"))
        item = self.tableWidget.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "Df"))
        item = self.tableWidget.verticalHeaderItem(2)
        item.setText(_translate("MainWindow", "D"))
        item = self.tableWidget.verticalHeaderItem(3)
        item.setText(_translate("MainWindow", "Wm"))
        item = self.tableWidget.verticalHeaderItem(4)
        item.setText(_translate("MainWindow", "N"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "L.B."))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "U.B."))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Init."))
        self.groupBox_3.setTitle(_translate("MainWindow", "Optimizer Selection"))
        self.pushButton.setText(_translate("MainWindow", "Baseline"))
        self.pushButton_2.setText(_translate("MainWindow", "RS"))
        self.pushButton_3.setText(_translate("MainWindow", "GA"))
        self.pushButton_4.setText(_translate("MainWindow", "CSP"))
        self.pushButton_5.setText(_translate("MainWindow", "PSO"))
        self.pushButton_6.setText(_translate("MainWindow", "BayesOps"))
        self.pushButton_8.setText(_translate("MainWindow", "openMDAO"))
        self.pushButton_7.setText(_translate("MainWindow", "Run Oprimizer"))
        self.groupBox_9.setTitle(_translate("MainWindow", "Optimizer descrpition"))
        self.textBrowser_optimizer.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'.AppleSystemUIFont\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:18pt;\">Pros and cons.</span></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Optimizer), _translate("MainWindow", "Optimizer"))
        self.groupBox_4.setTitle(_translate("MainWindow", "Optimizer & Requirements:"))
        self.groupBox_5.setTitle(_translate("MainWindow", "Output Varaibles:"))
        self.groupBox_6.setTitle(_translate("MainWindow", "Expected Performance: "))
        self.groupBox_7.setTitle(_translate("MainWindow", "Progress Bar:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Output), _translate("MainWindow", "Output"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))

    def on_tableWidget_cellChanged(self, row, column, text_browser):
        item = self.tableWidget.item(row, column)
        if item:
            value = item.text()
            print(f"Cell at ({row}, {column}) changed to: {value}")

            # Store the value in the attribute
            self.tableValues[row][column] = value
            # Update the QTextBrowser
            self.update_text_browser(text_browser)

    def update_text_browser(self, text_browser):
        # Clear existing content
        text_browser.clear()

        # Add table values to QTextBrowser
        text_browser.append("Requirements:")
        for row in self.tableValues:
            text_browser.append('\t'.join(str(cell) for cell in row))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    
    # Connect the variables button's clicked signal to a lambda function
    ui.btn_Dm.clicked.connect(lambda: ui.stackedWidget.setCurrentIndex(1))
    ui.btn_Df.clicked.connect(lambda: ui.stackedWidget.setCurrentIndex(2))
    ui.btn_D.clicked.connect(lambda: ui.stackedWidget.setCurrentIndex(3))
    ui.btn_Wm.clicked.connect(lambda: ui.stackedWidget.setCurrentIndex(4))
    ui.btn_N.clicked.connect(lambda: ui.stackedWidget.setCurrentIndex(5))
    
    MainWindow.show()
    sys.exit(app.exec_())
