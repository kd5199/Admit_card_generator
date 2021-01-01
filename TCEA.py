# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TCEA.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.pagesizes import A5
from reportlab.platypus import TableStyle
from reportlab.lib import colors
from reportlab.platypus import Table
import sqlite3
import datetime
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.pagesizes import A5,landscape
from reportlab.lib.pagesizes import A4
from reportlab.platypus import TableStyle
from reportlab.lib import colors
from reportlab.platypus import Image
from reportlab.platypus import Table
from reportlab.pdfgen import canvas
from PyQt5.QtWidgets import QMessageBox
import PyPDF2
import webbrowser as wb
import os
import abc_rc
from barcode import ISBN13,EAN14,Code39
from barcode.writer import ImageWriter

class Ui_MainWindow(object):


    def generate_pdf(self):

        name  = self.tableWidget.item(self.tableWidget.currentRow(),1).text()
        Fname = self.tableWidget.item(self.tableWidget.currentRow(),2).text()
        dob = self.tableWidget.item(self.tableWidget.currentRow(), 3).text()
        level = self.tableWidget.item(self.tableWidget.currentRow(), 4).text()
        branch = self.tableWidget.item(self.tableWidget.currentRow(), 5).text()
        regid = self.tableWidget.item(self.tableWidget.currentRow(), 6).text()


        info = [
            ['Name : {}'.format(name)], ['Father\'s name : {}'.format( Fname)],
            ['Level : {}'.format(level)],[ 'Branch : {}'.format( branch)],
            ['Registration ID : {}'.format(regid)],[ 'DoB : {}'.format( dob)]

        ]

        picFN = '{}.jpg'.format(regid)
        with open(picFN, 'wb') as f:
            Code39(regid, writer=ImageWriter()).write(f)



        buffer = 'buffer.pdf'
        fileName = '{}.pdf'.format(regid)
        pdf = SimpleDocTemplate(buffer, pagesize=A4, leftMargin=20, rightMargin=20,
                                topMargin=80, bottomMargin=300)

        print("HERE1")

        picture = Image('logo.jpg')
        picture.drawWidth = 150
        picture.drawHeight = 150
        picTable = Table([[picture]], 150, 150, )



        print('here2')
        picture = Image(picFN)
        picture.drawWidth = 125
        picture.drawHeight = 50
        picTable2 = Table([[picture]], 375, 150, hAlign="BOTTOM")

        info_table = Table(info, 200, 20)
        print('here2')
        # add style
        info_style = TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTSIZE', (0, 0), (-1, -1), 15),

            ('BOTTOMPADDING', (0, 0), (-1, -1), 5)
            # ('BOTTOMPADDING', (0, -1), (-1, -1), 5)

        ])

        product_style1 = TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), -5),
        ])

        # 3) Add borders('GRID', (0, 0), (-1, -1), 1, colors.purple),
        product_style2 = TableStyle([
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)])

        """
        product_table.setStyle(product_style2)
        amount_table.setStyle(product_style1)"""

        # print("Style created")

        picTable.setStyle(info_style)
        info_table.setStyle(info_style)
        infopic = Table([[info_table, picTable]], [400, 150])
        picTable2.setStyle(product_style1)
        infopic.setStyle(info_style)
        mainTable = Table([[infopic], [picTable2, " "]])
        elems = []
        elems.append(mainTable)
        # print("Appended")

        print('here')

        pdf.build(elems)
        # wb.open_new(r'{}/{}'.format(os.getcwd(), buffer))

        pdf_file = "WM.pdf"
        watermark = buffer
        merged_file = fileName
        input_file = open(pdf_file, 'rb')
        input_pdf = PyPDF2.PdfFileReader(pdf_file)
        watermark_file = open(watermark, 'rb')
        watermark_pdf = PyPDF2.PdfFileReader(watermark_file)
        pdf_page = input_pdf.getPage(0)
        watermark_page = watermark_pdf.getPage(0)
        pdf_page.mergePage(watermark_page)
        output = PyPDF2.PdfFileWriter()
        output.addPage(pdf_page)
        merged_file = open(fileName, 'wb')
        output.write(merged_file)
        merged_file.close()
        watermark_file.close()
        input_file.close()

        wb.open_new(r'{}/{}'.format(os.getcwd(), fileName))





    def add_info(self):
            self.conn = sqlite3.connect("TCEA.db")
            self.query = "INSERT INTO Info( Branch, Prefix, Startf) VALUES ('{}','{}',{})".format(
                    self.Branchtoadd.text(),
                    self.Rolltoadd.text(),
                    self.notostartfrom.text()
                    )
            self.conn.execute(self.query)
            self.conn.commit()
            self.show_db

    def branch_to_search(self):
        self.conn = sqlite3.connect("TCEA.db")
        self.query = "SELECT Branch FROM Info"
        self.lis = self.conn.cursor().execute(self.query)
        self.conn.commit()
        self.branch.clear()
        self.m = self.lis.fetchall()
        self.m = list(dict.fromkeys(self.m))
        for k in self.m:
            self.branch.addItem(str(k).strip("(',')"))
        self.conn.commit()

    def show_db(self):
        self.conn = sqlite3.connect("TCEA.db")
        self.query = "SELECT * FROM Numerica"
        self.result = self.conn.execute(self.query)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(9)
        self.tableWidget.setHorizontalHeaderLabels([" SL ", " Name ", " FName ", " DoB ", " Level ", " Branch ", " RegID. ", " Contact ", " Address "])

        for row_number, row_data in enumerate(self.result):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
        self.conn.commit()


    def add_to_db(self):



        self.conn = sqlite3.connect("TCEA.db")
        self.query = "INSERT INTO Numerica( Name, FName , DoB , Level , Branch , Contact , Address) VALUES ('{}','{}','{}','{}','{}','{}','{}')".format(self.name.text(),
                                                                                                                                                        self.Fname.text(),
                                                                                                                                                        self.dob.text(),
                                                                                                                                                        self.level.value(),
                                                                                                                                                        self.branch.currentText(),
                                                                                                                                                        self.contact.text(),
                                                                                                                                                        self.address.text())
        self.conn.execute(self.query)
        self.conn.commit()


        self.query  = "SELECT SL FROM (SELECT * FROM Numerica ORDER BY ROWNUM DESC) WHERE ROWNUM = 1 "
        self.lis = self.conn.cursor().execute(self.query)
        self.conn.commit()
        self.m = self.lis.fetchall()
        self.m = list(dict.fromkeys(self.m))
        for k in self.m:
            self.slno = int(str(k).strip("(',')"))
        self.conn.commit()

        self.regid = 'NMRCATCEA'+str(10000+self.slno)

        self.query = "UPDATE Numerica SET RegID = {} WHERE Name = '{}' AND FName = '{}' AND DoB = '{}' AND Level = '{}' AND" \
                     " Branch = '{}' AND Contact ='{}' AND Address='{}'".format(self.regid,
                                                                    self.name.text(),
                                                                    self.Fname.text(),
                                                                    self.dob.text(),
                                                                    self.level.value(),
                                                                    self.branch.currentText(),
                                                                    self.contact.text(),
                                                                    self.address.text())
        self.conn.execute(self.query)
        self.conn.commit()
        self.show_db()




    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1069, 795)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/newPrefix/SmoothLogo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("QPushButton { color: black; background-color: white;background: rgba(255,255,255,50%) }\n"
        "QWidget{font-style: italic;font-weight: 500; font-family: Helvetica;font-size:18px}\n"
        "QLineEdit:hover{ border-style: solid #FF6347}\n"
        "QPushButton:hover { color: green }\n"
        "QRadioButton:!hover { color: black;background: transparent }\n"
        "QRadioButton:hover { color: red }\n"
        "/*QTableWidget:!hover{background: qlineargradient(spread:pad, x1:0.45911, y1:0.007, x2:0.463873, y2:1, stop:0 rgba(51, 71, 228, 233), stop:1 rgba(255, 255, 255, 255));background: transparent}*/\n"
        "/*QTextBrowser:!hover{background:qlineargradient(spread:pad, x1:0.432, y1:1, x2:0.506, y2:0, stop:0 rgba(57, 162, 25, 133), stop:1 rgba(255, 255, 255, 255));background: transparent}*/\n"
        "\n"
        "QTableWidget:!hover{background: rgba(255,255,255,50%)}\n"
        "QTextBrowser:!hover{background: rgba(255,255,255,50%)}\n"
        "\n"
        "QTableWidget:hover{background: rgb(255,255,255)}\n"
        "QTextBrowser:hover{background: rgb(255,255,255)}\n"
        "\n"
        "QTabBar::tab:selected {background: qlineargradient(spread:pad, x1:0.46, y1:0, x2:0.482955, y2:1, stop:0 rgba(0, 255, 18, 180), stop:1 rgba(255, 255, 255, 255))}\n"
        "QTabBar::tab:!selected:hover { background:qlineargradient(spread:pad, x1:0.45911, y1:0.007, x2:0.463873, y2:1, stop:0 rgba(51, 71, 228, 233), stop:1 rgba(255, 255, 255, 255))}\n"
        "QTabBar::tab:top, QTabBar::tab:bottom {\n"
        "    min-width: 8ex;\n"
        "    margin-right: -1px;\n"
        "    padding: 5px 10px 5px 10px;\n"
        "}\n"
        "\n"
        "QDoubleSpinBox:hover{  background :qlineargradient(spread:pad, x1:0, y1:0.517, x2:1, y2:0.5, stop:0 rgba(90, 173, 228, 255), stop:1 rgba(255, 255, 255, 255));background: rgba(255,255,255,50%) }\n"
        "\n"
        "QLineEdit{font-style: italic}\n"
        "QTextBrowser{font-style: italic;}\n"
        "QLabel{ font-family: Helvetica;font-weight: bold}\n"
        "QLineEdit{border: none; border-bottom: 1px solid #717072 }\n"
        "QDateEdit{border: none; border-bottom: 1px solid #717072;background: rgba(255,255,255,50%)}\n"
        "QSpinBox{border: none; border-bottom: 1px solid #717072;background: rgba(255,255,255,50%) }\n"
        "\n"
        "QDoubleSpinBox{border: none; border-bottom: 1px solid #717072 }\n"
        "QLabel{backgroud:transparent}\n"
        "\n"
        "QFrame{background: url(:/newPrefix/bg3.jpg)}\n"
        "\n"
        "\n"
        "QLineEdit:!hover{background: rgba(255,255,255,50%)}\n"
        "QComboBox{background: rgba(255,255,255,50%)}\n"
        "\n"
        "\n"
        "")
        MainWindow.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setObjectName("gridLayout")
        self.tableWidget = QtWidgets.QTableWidget(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy)
        self.tableWidget.setRowCount(5)
        self.tableWidget.setColumnCount(10)
        self.tableWidget.setObjectName("tableWidget")
        self.gridLayout.addWidget(self.tableWidget, 4, 0, 1, 1)
        self.line = QtWidgets.QFrame(self.frame)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 1, 0, 1, 1)
        self.line_2 = QtWidgets.QFrame(self.frame)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout.addWidget(self.line_2, 3, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.selected = QtWidgets.QRadioButton(self.frame)
        self.selected.setObjectName("selected")
        self.horizontalLayout_8.addWidget(self.selected)
        self.all = QtWidgets.QRadioButton(self.frame)
        self.all.setObjectName("all")
        self.horizontalLayout_8.addWidget(self.all)
        self.line_13 = QtWidgets.QFrame(self.frame)
        self.line_13.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_13.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_13.setObjectName("line_13")
        self.horizontalLayout_8.addWidget(self.line_13)
        self.label_14 = QtWidgets.QLabel(self.frame)
        self.label_14.setObjectName("label_14")
        self.horizontalLayout_8.addWidget(self.label_14)
        self.pdfs = QtWidgets.QComboBox(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pdfs.sizePolicy().hasHeightForWidth())
        self.pdfs.setSizePolicy(sizePolicy)
        self.pdfs.setObjectName("pdfs")
        self.horizontalLayout_8.addWidget(self.pdfs)
        self.print = QtWidgets.QPushButton(self.frame)
        self.print.setObjectName("print")
        self.horizontalLayout_8.addWidget(self.print)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.generate = QtWidgets.QPushButton(self.frame)
        self.generate.setObjectName("generate")
        self.generate.clicked.connect(self.generate_pdf)

        self.horizontalLayout_3.addWidget(self.generate)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.gridLayout.addLayout(self.verticalLayout, 8, 0, 1, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.Eventnames = QtWidgets.QComboBox(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Eventnames.sizePolicy().hasHeightForWidth())
        self.Eventnames.setSizePolicy(sizePolicy)
        self.Eventnames.setObjectName("Eventnames")
        self.horizontalLayout.addWidget(self.Eventnames)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.Eventtoadd = QtWidgets.QLineEdit(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Eventtoadd.sizePolicy().hasHeightForWidth())
        self.Eventtoadd.setSizePolicy(sizePolicy)
        self.Eventtoadd.setObjectName("Eventtoadd")
        self.horizontalLayout_2.addWidget(self.Eventtoadd)
        self.line_5 = QtWidgets.QFrame(self.frame)
        self.line_5.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.horizontalLayout_2.addWidget(self.line_5)
        self.label_10 = QtWidgets.QLabel(self.frame)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_2.addWidget(self.label_10)
        self.Branchtoadd = QtWidgets.QLineEdit(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Branchtoadd.sizePolicy().hasHeightForWidth())
        self.Branchtoadd.setSizePolicy(sizePolicy)
        self.Branchtoadd.setObjectName("Branchtoadd")
        self.horizontalLayout_2.addWidget(self.Branchtoadd)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_11 = QtWidgets.QLabel(self.frame)
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_4.addWidget(self.label_11)
        self.Rolltoadd = QtWidgets.QLineEdit(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Rolltoadd.sizePolicy().hasHeightForWidth())
        self.Rolltoadd.setSizePolicy(sizePolicy)
        self.Rolltoadd.setObjectName("Rolltoadd")
        self.horizontalLayout_4.addWidget(self.Rolltoadd)
        self.line_6 = QtWidgets.QFrame(self.frame)
        self.line_6.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.horizontalLayout_4.addWidget(self.line_6)
        self.label_12 = QtWidgets.QLabel(self.frame)
        self.label_12.setObjectName("label_12")
        self.horizontalLayout_4.addWidget(self.label_12)
        self.notostartfrom = QtWidgets.QLineEdit(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.notostartfrom.sizePolicy().hasHeightForWidth())
        self.notostartfrom.setSizePolicy(sizePolicy)
        self.notostartfrom.setObjectName("notostartfrom")
        self.horizontalLayout_4.addWidget(self.notostartfrom)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.addinfo = QtWidgets.QPushButton(self.frame)
        self.addinfo.setObjectName("addinfo")
        self.horizontalLayout_10.addWidget(self.addinfo)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem3)
        self.verticalLayout_2.addLayout(self.horizontalLayout_10)
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_9.addWidget(self.label_3)
        self.filter = QtWidgets.QComboBox(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.filter.sizePolicy().hasHeightForWidth())
        self.filter.setSizePolicy(sizePolicy)
        self.filter.setObjectName("filter")
        self.horizontalLayout_9.addWidget(self.filter)
        self.searchkey = QtWidgets.QLineEdit(self.frame)
        self.searchkey.setObjectName("searchkey")
        self.horizontalLayout_9.addWidget(self.searchkey)
        self.search = QtWidgets.QPushButton(self.frame)
        self.search.setObjectName("search")
        self.horizontalLayout_9.addWidget(self.search)
        self.edit = QtWidgets.QPushButton(self.frame)
        self.edit.setObjectName("edit")
        self.horizontalLayout_9.addWidget(self.edit)
        self.delete_2 = QtWidgets.QPushButton(self.frame)
        self.delete_2.setObjectName("delete_2")
        self.horizontalLayout_9.addWidget(self.delete_2)
        self.showall = QtWidgets.QPushButton(self.frame)
        self.showall.setObjectName("showall")
        self.showall.clicked.connect(self.show_db)


        self.horizontalLayout_9.addWidget(self.showall)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem4)
        self.gridLayout.addLayout(self.horizontalLayout_9, 6, 0, 1, 1)
        self.line_3 = QtWidgets.QFrame(self.frame)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.gridLayout.addWidget(self.line_3, 5, 0, 1, 1)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_4 = QtWidgets.QLabel(self.frame)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_5.addWidget(self.label_4)
        self.name = QtWidgets.QLineEdit(self.frame)
        self.name.setObjectName("name")
        self.horizontalLayout_5.addWidget(self.name)
        self.line_7 = QtWidgets.QFrame(self.frame)
        self.line_7.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_7.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_7.setObjectName("line_7")
        self.horizontalLayout_5.addWidget(self.line_7)
        self.label_6 = QtWidgets.QLabel(self.frame)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_5.addWidget(self.label_6)
        self.dob = QtWidgets.QDateEdit(self.frame)
        self.dob.setObjectName("dob")
        self.horizontalLayout_5.addWidget(self.dob)
        self.line_8 = QtWidgets.QFrame(self.frame)
        self.line_8.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_8.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_8.setObjectName("line_8")
        self.horizontalLayout_5.addWidget(self.line_8)
        self.label_8 = QtWidgets.QLabel(self.frame)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_5.addWidget(self.label_8)
        self.level = QtWidgets.QSpinBox(self.frame)
        self.level.setObjectName("level")
        self.horizontalLayout_5.addWidget(self.level)
        self.line_9 = QtWidgets.QFrame(self.frame)
        self.line_9.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_9.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_9.setObjectName("line_9")
        self.horizontalLayout_5.addWidget(self.line_9)
        self.label_13 = QtWidgets.QLabel(self.frame)
        self.label_13.setObjectName("label_13")
        self.horizontalLayout_5.addWidget(self.label_13)
        self.contact = QtWidgets.QLineEdit(self.frame)
        self.contact.setObjectName("contact")
        self.horizontalLayout_5.addWidget(self.contact)
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_5 = QtWidgets.QLabel(self.frame)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_6.addWidget(self.label_5)
        self.Fname = QtWidgets.QLineEdit(self.frame)
        self.Fname.setObjectName("Fname")
        self.horizontalLayout_6.addWidget(self.Fname)
        self.line_10 = QtWidgets.QFrame(self.frame)
        self.line_10.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_10.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_10.setObjectName("line_10")
        self.horizontalLayout_6.addWidget(self.line_10)
        self.label_7 = QtWidgets.QLabel(self.frame)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_6.addWidget(self.label_7)
        self.address = QtWidgets.QLineEdit(self.frame)
        self.address.setObjectName("address")
        self.horizontalLayout_6.addWidget(self.address)
        self.line_11 = QtWidgets.QFrame(self.frame)
        self.line_11.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_11.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_11.setObjectName("line_11")
        self.horizontalLayout_6.addWidget(self.line_11)
        self.label_9 = QtWidgets.QLabel(self.frame)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_6.addWidget(self.label_9)
        self.branch = QtWidgets.QComboBox(self.frame)
        self.branch.setObjectName("branch")
        self.horizontalLayout_6.addWidget(self.branch)
        self.line_12 = QtWidgets.QFrame(self.frame)
        self.line_12.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_12.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_12.setObjectName("line_12")
        self.horizontalLayout_6.addWidget(self.line_12)
        self.save = QtWidgets.QPushButton(self.frame)
        self.save.setObjectName("save")
        self.horizontalLayout_6.addWidget(self.save)
        self.verticalLayout_3.addLayout(self.horizontalLayout_6)
        self.gridLayout.addLayout(self.verticalLayout_3, 2, 0, 1, 1)
        self.line_4 = QtWidgets.QFrame(self.frame)
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.gridLayout.addWidget(self.line_4, 7, 0, 1, 1)
        self.gridLayout_2.addWidget(self.frame, 0, 0, 1, 1)
        self.show_db()
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Smooothware - TCEA Admit Card Generator "))
        self.selected.setText(_translate("MainWindow", "For Selected"))
        self.all.setText(_translate("MainWindow", "For All"))
        self.label_14.setText(_translate("MainWindow", "Search"))
        self.print.setText(_translate("MainWindow", "Print"))
        self.generate.setText(_translate("MainWindow", "Generate Admit Card"))
        self.label.setText(_translate("MainWindow", "Event Title :  "))
        self.label_2.setText(_translate("MainWindow", "Add Event"))
        self.Eventtoadd.setPlaceholderText(_translate("MainWindow", "Enter Event Name To Add"))
        self.label_10.setText(_translate("MainWindow", "Add Branch"))
        self.Branchtoadd.setPlaceholderText(_translate("MainWindow", "Enter Branch"))
        self.label_11.setText(_translate("MainWindow", "Roll No. Prefix"))
        self.Rolltoadd.setPlaceholderText(_translate("MainWindow", "Enter Roll No. Prefix"))
        self.label_12.setText(_translate("MainWindow", "Start From"))
        self.notostartfrom.setPlaceholderText(_translate("MainWindow", "Enter No. To Start From"))
        self.addinfo.setText(_translate("MainWindow", "Add"))
        self.label_3.setText(_translate("MainWindow", "Fllter : "))
        self.searchkey.setPlaceholderText(_translate("MainWindow", "Enter Name OR Branch"))
        self.search.setText(_translate("MainWindow", "Search"))
        self.edit.setText(_translate("MainWindow", "Edit"))
        self.delete_2.setText(_translate("MainWindow", "Delete"))
        self.showall.setText(_translate("MainWindow", "Show All"))
        self.label_4.setText(_translate("MainWindow", "Name"))
        self.label_6.setText(_translate("MainWindow", "DoB"))
        self.label_8.setText(_translate("MainWindow", "Level"))
        self.label_13.setText(_translate("MainWindow", "Contact"))
        self.label_5.setText(_translate("MainWindow", "Father\'s Name"))
        self.label_7.setText(_translate("MainWindow", "Address"))
        self.label_9.setText(_translate("MainWindow", "Branch"))
        self.save.setText(_translate("MainWindow", "Save"))
import abc_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
