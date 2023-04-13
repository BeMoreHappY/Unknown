import json

from PyQt6 import QtWidgets, uic, QtCore, QtGui
from PyQt6.QtCore import Qt, QPoint, QPropertyAnimation, QEasingCurve, QUrl
from ui_main import Ui_MainWindow
import os
from kameleoo import Kameleo
from philips import philipsBot
from threading import Thread
from multiprocessing import Process, Lock

import sys
import resources
#APIIIIII
#AIzaSyCl2AeXZGjCmSGPHJtR6WV0_HAZffbjo-s

class window(QtWidgets.QMainWindow):
    db = None
    stylesheet = None

    def __init__(self, database):
        super().__init__()
        self.db = database
        self.setUI()
        self.lock = Lock()

    def deleteROW(self):
        try:
            row = self.ui.tableWidget.currentRow()
            self.db.delFromTable(self.ui.tableWidget.item(row, 0).text())
            self.ui.tableWidget.clear()
            self.ui.tableWidget.setHorizontalHeaderLabels(
                ["ID", "Imie i nazwisko", "Email", "Hasło", "adres", "Proxy", "Path"])
            self.loadData()
        except:
            print("Nie zaznaczono elementu!")

    def setUI(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.stylesheet = self.ui.styleSheet

        self.ui.toggleButton.clicked.connect(lambda: self.toggleMenu(True))

        # CLOSE APP
        self.ui.closeAppBtn.clicked.connect(lambda: MainApp.exit())

        # MINIMIZE
        self.ui.minimizeAppBtn.clicked.connect(lambda: self.showMinimized())

        # SET PAGE
        self.ui.stackedWidget.setCurrentWidget(self.ui.home)
        self.ui.btn_home.setStyleSheet(self.ui.btn_home.styleSheet() + "background-color: rgb(40, 44, 52)")

        # TABBLE
        self.ui.tableWidget.setColumnWidth(0, 60)
        self.ui.tableWidget.setHorizontalHeaderLabels(
            ["ID", "Imie i nazwisko", "Email", "Hasło", "adres", "Proxy", "port", "Path"])

        # BTN CLICKED
        self.ui.btn_home.clicked.connect(self.buttonClick)
        self.ui.btn_widgets.clicked.connect(self.buttonClick)
        self.ui.btn_new.clicked.connect(self.buttonClick)
        self.ui.btn_botPage.clicked.connect(self.buttonClick)
        self.ui.btn_deleteFromDB.clicked.connect(self.deleteROW)
        self.ui.btn_loadFromDB.clicked.connect(self.startKameleoProfile)
        self.ui.btn_create.clicked.connect(self.createProfile)
        self.ui.btn_path.clicked.connect(self.choosePath)
        self.ui.btn_PassSave.clicked.connect(self.buttonClick)
        self.ui.btn_ProxySave.clicked.connect(self.buttonClick)
        self.ui.btn_PortSave.clicked.connect(self.buttonClick)
        self.ui.btn_PathSave.clicked.connect(self.buttonClick)
    def mousePressEvent(self, event):
        self.oldPos = event.globalPosition().toPoint()
    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPosition().toPoint() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPosition().toPoint()
    def loadData(self):
        i = 0

        for row in self.db.getAllData():
            print(row)
            self.ui.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(str(row[0])))
            self.ui.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(row[1]))
            self.ui.tableWidget.setItem(i, 2, QtWidgets.QTableWidgetItem(row[2]))
            self.ui.tableWidget.setItem(i, 3, QtWidgets.QTableWidgetItem(row[3]))
            self.ui.tableWidget.setItem(i, 4, QtWidgets.QTableWidgetItem(row[4]))
            self.ui.tableWidget.setItem(i, 5, QtWidgets.QTableWidgetItem(row[5]))
            self.ui.tableWidget.setItem(i, 6, QtWidgets.QTableWidgetItem(str(row[6])))
            self.ui.tableWidget.setItem(i, 7, QtWidgets.QTableWidgetItem(row[7]))
            i += 1
    def toggleMenu(self, enable):
        if enable:
            # GET WIDTH
            width = self.ui.leftMenuBg.width()
            maxExtend = 200
            standard = 60

            # SET MAX WIDTH
            if width == 60:
                widthExtended = maxExtend
            else:
                widthExtended = standard

            # ANIMATION
            self.animation = QPropertyAnimation(self.ui.leftMenuBg, b"minimumWidth")
            self.animation.setDuration(20)
            self.animation.setStartValue(width)
            self.animation.setEndValue(widthExtended)
            self.animation.setEasingCurve(QEasingCurve.Type.InOutQuart)
            self.animation.start()
    def choosePath(self):
        fpath = QtWidgets.QFileDialog.getExistingDirectoryUrl(self, "Choose directory",
                                                              QUrl().fromLocalFile(os.path.expanduser("~/Desktop")))
        self.ui.pathLine.setText(fpath.path()[1:] + '/')
    def buttonClick(self):
        # GET BUTTON CLICKED
        btn = self.sender()
        btnName = btn.objectName()

        # SHOW HOME PAGE
        if btnName == "btn_home":
            self.ui.stackedWidget.setCurrentWidget(self.ui.home)
            self.ui.btn_home.setStyleSheet(
                "background-color: rgb(40, 44, 52); background-image: url(:/icons/images/icons/cil-home.png);")
            # UIFunctions.resetStyle(self, btnName)
            # btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))
        else:
            self.ui.btn_home.setStyleSheet("background-image: url(:/icons/images/icons/cil-home.png);")

        # SHOW WIDGETS PAGE
        if btnName == "btn_widgets":
            self.loadData()
            self.ui.stackedWidget.setCurrentWidget(self.ui.widgets)
            self.ui.btn_widgets.setStyleSheet(
                "background-color: rgb(40, 44, 52); background-image: url(:/icons/images/icons/cil-folder-open.png);")
            # UIFunctions.resetStyle(self, btnName)
            # btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))
        else:
            self.ui.btn_widgets.setStyleSheet("background-image: url(:/icons/images/icons/cil-folder-open.png);")

        if btnName == "btn_new":

            #self.ui.portLine.setText(str(self.db.getLastPort() + 1))
            self.loadRemember()
            self.ui.stackedWidget.setCurrentWidget(self.ui.createPage)
            self.ui.btn_new.setStyleSheet(
                "background-color: rgb(40, 44, 52); background-image: url(:/icons/images/icons/cil-file.png);")
        else:
            self.ui.btn_new.setStyleSheet("background-image: url(:/icons/images/icons/cil-file.png);")

        if btnName == "btn_botPage":
            self.ui.stackedWidget.setCurrentWidget(self.ui.botPage)
            self.ui.btn_botPage.setStyleSheet(
                "background-color: rgb(40, 44, 52); background-image: url(:/icons/images/icons/cil-user.png);")
        else:
            self.ui.btn_botPage.setStyleSheet("background-image: url(:/icons/images/icons/cil-user.png);")

        if btnName == "btn_PassSave":
            self.setRemember(btnName, self.ui.passwordLine.text())

        if btnName == "btn_ProxySave":
            self.setRemember(btnName, self.ui.proxyLine.text())

        if btnName == "btn_PortSave":
            self.setRemember(btnName, self.ui.portLine.text())

        if btnName == "btn_PathSave":
            self.setRemember(btnName, self.ui.pathLine.text())
        # PRINT BTN NAME
        print(f'Button "{btnName}" pressed!')
    def createProfile(self):
        name = self.ui.nameLine.text()
        email = self.ui.emailLine.text()
        password = self.ui.passwordLine.text()
        adres = self.ui.addressLine.text()
        proxy = self.ui.proxyLine.text()
        port = self.ui.portLine.text()
        path = self.ui.pathLine.text()

        for child in self.ui.frame.findChildren(QtWidgets.QLineEdit):
            child.clear()

        kameleo = Kameleo(fullName=name, IP=proxy, proxyPort=int(port), path=path)
        kameleo.startProfile()
        kameleo.stopProfile()
        kameleo.saveProfile()
        self.db.addToTable([name, email, password, adres, proxy, int(port), path, str(kameleo.profile.id)])
    def startKameleoProfile(self):
        try:
            data = self.getRowDatabase()
            #kameleo = Kameleo(profile_id=data[8], path=data[7] + data[1] + ".kameleo")
            #kameleo.startProfile()
            p = Process(target=philipsBot, args=(data, self.lock))
            p.start()


        except:
            pass
    def getRowDatabase(self):
        row = self.ui.tableWidget.currentRow()
        ID = self.ui.tableWidget.item(row, 0).text()
        return self.db.getRowData(int(ID))
    def setRemember(self, what, value):
        if os.path.isfile("rememberData.txt") and os.path.getsize("rememberData.txt") > 0:
            with open("rememberData.txt", "r") as f:
                data = json.load(f)
            print(data)
            with open("rememberData.txt", "w") as f:
                if what in data:
                    if data[what] == value:
                        data[what] = ""
                    else:
                        data[what] = value
                else:
                    data[what] = value
                json.dump(data, f, indent=5)
        else:
            with open("rememberData.txt", "w") as f:
                data = {what: value}
                json.dump(data, f, indent=5)
    def loadRemember(self):
        if os.path.isfile("rememberData.txt") and os.path.getsize("rememberData.txt") > 0:
            with open("rememberData.txt", "r") as f:
                data = json.load(f)
            for i in data:
                if i == "btn_PassSave":
                    self.ui.passwordLine.setText(data[i])
                elif i == "btn_ProxySave":
                    self.ui.proxyLine.setText(data[i])
                elif i == "btn_PortSave":
                    self.ui.portLine.setText(data[i])
                elif i == "btn_PathSave":
                    self.ui.pathLine.setText(data[i])
