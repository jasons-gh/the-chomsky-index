import pandas as pd
import platform
import search
import sys
import webbrowser
from bs4 import BeautifulSoup
from pathlib import Path
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, QRunnable, QThreadPool, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QButtonGroup, QLabel
from unidecode import unidecode


results_sorted = []


class WorkerSignals(QObject):
    search_signal = pyqtSignal(object)


class Worker(QRunnable):
    def __init__(self, fn):
        super(Worker, self).__init__()
        self.fn = fn
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        results_sorted = self.fn()
        self.signals.search_signal.emit(results_sorted)


class Ui_MainWindow(object):

    def __init__(self):
        self.threadpool = QThreadPool()
        # print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())
        self.base_df = pd.read_hdf(Path(self.base_path()) / 'h5' / 'base_df.h5', 'base_df')
        self.settings = {'Print': True, 'Video': True}


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1209, 851)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 120, 215))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 120, 215))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipBase, brush)
        MainWindow.setPalette(palette)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 1209, 851))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.frame = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        self.frame.setMaximumSize(QtCore.QSize(1100, 16777215))
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit = QtWidgets.QLineEdit(self.frame)
        font = QtGui.QFont(self.os_font('name'), self.os_font('size'), weight=QtGui.QFont.Light)
        self.lineEdit.setFont(font)
        self.lineEdit.setFrame(False)
        self.lineEdit.setAttribute(QtCore.Qt.WA_MacShowFocusRect, False)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.Search = QtWidgets.QPushButton(self.frame)
        self.Search.setMinimumSize(QtCore.QSize(125, 0))
        font = QtGui.QFont(self.os_font('name'), self.os_font('size'), weight=QtGui.QFont.Light)
        self.Search.setFont(font)
        self.Search.setFlat(True)
        self.Search.setObjectName("Search")
        self.Search.setStyleSheet("QPushButton {background-color: white}"
                                  "QPushButton:hover {background-color: white}"
                                  "QPushButton:pressed {border: solid}"
                                  "QPushButton:pressed {border-width: 1px}"
                                  "QPushButton:pressed {border-top-color: #808080}"
                                  "QPushButton:pressed {border-left-color: #808080}"
                                  "QPushButton:pressed {border-right-color: #CDCDCD}"
                                  "QPushButton:pressed {border-bottom-color: #CDCDCD}")
        
        self.Search.clicked.connect(self.search_button_worker)


        self.horizontalLayout.addWidget(self.Search)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.line = QtWidgets.QFrame(self.frame)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.PlaceholderText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.PlaceholderText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.PlaceholderText, brush)
        self.line.setPalette(palette)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.Settings = QtWidgets.QPushButton(self.frame)
        self.Settings.setMinimumSize(QtCore.QSize(125, 0))
        font = QtGui.QFont(self.os_font('name'), self.os_font('size'), weight=QtGui.QFont.Light)
        self.Settings.setFont(font)
        self.Settings.setFlat(True)
        self.Settings.setObjectName("Settings")
        self.Settings.setStyleSheet("QPushButton {background-color: white}"
                                 "QPushButton:hover {background-color: white}"
                                 "QPushButton:pressed {border: solid}"
                                 "QPushButton:pressed {border-width: 1px}"
                                 "QPushButton:pressed {border-top-color: #808080}"
                                 "QPushButton:pressed {border-left-color: #808080}"
                                 "QPushButton:pressed {border-right-color: #CDCDCD}"
                                 "QPushButton:pressed {border-bottom-color: #CDCDCD}")
        
        self.Settings.clicked.connect(self.settings_button)

        self.horizontalLayout_2.addWidget(self.Settings)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout_4.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem3)
        self.verticalLayout_4.addLayout(self.verticalLayout_2)
        self.gridLayout_2.addWidget(self.frame, 0, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 0, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def search_function(self, MainWindow, results_sorted):
        self.buttongroup = QButtonGroup()
        self.buttongroup.buttonClicked[int].connect(self.open_button)
        for i, result in enumerate(results_sorted):
            self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
            self.horizontalLayout_3.setObjectName("horizontalLayout_" + str(i))
            self.textEdit = QtWidgets.QTextEdit(self.frame)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize((20 if platform.system() == 'Darwin' else 12))
            
            fontMetrics = QtGui.QFontMetrics(font)
            context_font_size = fontMetrics.size(0, str(result[2])).width()
            name_font_size = fontMetrics.size(0, str(result[1])).width()
            self.textEdit.setMinimumSize(QtCore.QSize(0, 60 + 25 * ((int(context_font_size / 900) + 1) + (int(name_font_size / 900) + 1))))
            self.textEdit.setMaximumSize(QtCore.QSize(16777215, 60 + 25 * ((int(context_font_size / 900) + 1) + (int(name_font_size / 900) + 1))))
       
            self.textEdit.setFont(font)
            self.textEdit.setFrameShape(QtWidgets.QFrame.NoFrame)
            self.textEdit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            self.textEdit.setObjectName("textEdit_" + str(i))
            self.horizontalLayout_3.addWidget(self.textEdit)
            spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
            self.horizontalLayout_3.addItem(spacerItem1)
            self.Open_1 = QtWidgets.QPushButton(self.frame)

            self.buttongroup.addButton(self.Open_1, i)

            self.Open_1.setMinimumSize(QtCore.QSize(125, 0))
            font = QtGui.QFont(self.os_font('name'), self.os_font('size'), weight=QtGui.QFont.Light)
            self.Open_1.setFont(font)
            self.Open_1.setFlat(True)
            self.Open_1.setObjectName("Open_" + str(i))
            self.Open_1.setStyleSheet("QPushButton {background-color: white}"
                              "QPushButton:hover {background-color: white}"
                              "QPushButton:pressed {border: solid}"
                              "QPushButton:pressed {border-width: 1px}"
                              "QPushButton:pressed {border-top-color: #808080}"
                              "QPushButton:pressed {border-left-color: #808080}"
                              "QPushButton:pressed {border-right-color: #CDCDCD}"
                              "QPushButton:pressed {border-bottom-color: #CDCDCD}")
            self.horizontalLayout_3.addWidget(self.Open_1)
            self.verticalLayout_2.addLayout(self.horizontalLayout_3)
            spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
            self.verticalLayout_2.addItem(spacerItem2)
        
            _translate = QtCore.QCoreApplication.translate
            self.textEdit.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Arial\'; font-size:" + ("20" if platform.system() == 'Darwin' else "12") + "pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">" + str(result[2]) + "</p></body></html>"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:" + ("20" if platform.system() == 'Darwin' else "12") + "pt; font-weight:600;\">" + str(result[1])[:85] + "</span></p></body></html>"))
            self.Open_1.setText(_translate("MainWindow", "Open"))


    def open_button(self, id):
        if 'youtube.com' in results_sorted[id][3]:
            if platform.system() == 'Darwin':
                webbrowser.get("Safari").open(results_sorted[id][3])
            else:
                webbrowser.open(results_sorted[id][3])
        else:
            # webbrowser module may ignore hash in url
            # use JavaScript to edit file to load as if hash were entered
            file_url = results_sorted[id][3].split('#')[0]
            anchor = results_sorted[id][3][len(file_url):]

            soup = BeautifulSoup(open(file_url), "html.parser")
            original_tag = soup.head
            new_tag = soup.new_tag("script", id="scrollToHash", type="text/javascript")
            original_tag.append(new_tag)
            new_tag.string = """function scrollToHash(hash) {
                                location.hash = \"""" + anchor + """\";
                                }
                                window.onload = scrollToHash();"""
                                
            with open(file_url, 'w') as f:
                f.write(unidecode(str(soup.prettify())))
                if platform.system() == 'Darwin':
                    webbrowser.get("Safari").open('file://' + file_url)
                else:
                    webbrowser.open('file://' + file_url)

                    


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Search.setText(_translate("MainWindow", "Search"))
        self.Settings.setText(_translate("MainWindow", "Settings"))


    def search_button_worker(self):
        worker = Worker(self.search_button_signal)
        worker.signals.search_signal.connect(self.search_button_slot)

        self.threadpool.start(worker) 


    def search_button_signal(self):
        global results_sorted

        results_sorted = search.search_results(self.lineEdit.text(), self.base_df, self.base_path(), self.settings)

        return results_sorted


    def search_button_slot(self, results_sorted):
        self.clear_function(False)
        self.search_function(MainWindow, results_sorted)
    
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem3)


    def clear_function(self, spacer):

        try:
            i = 0
            while self.frame.findChild(QtWidgets.QPushButton, "Open_" + str(i)) != None:
                self.frame.findChild(QtWidgets.QPushButton, "Open_" + str(i)).deleteLater()
                i+=1

            i = 0
            while self.frame.findChild(QtWidgets.QTextEdit, "textEdit_" + str(i)) != None:
                self.frame.findChild(QtWidgets.QTextEdit, "textEdit_" + str(i)).deleteLater()
                i+=1

            for i in reversed(range(self.verticalLayout_2.count())):  #range(len(results_sorted)+10): #
                if isinstance(self.verticalLayout_2.itemAt(i), QtWidgets.QSpacerItem):
                    self.verticalLayout_2.takeAt(0)

            self.frame.findChild(QtWidgets.QPushButton, "Video").deleteLater()

            self.frame.findChild(QtWidgets.QPushButton, "Print").deleteLater()

            self.frame.findChild(QtWidgets.QLabel, "Format").deleteLater()

        except Exception as e:
            print(e)
    
        if spacer:
            spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
            self.verticalLayout_2.addItem(spacerItem3)


    def settings_button(self):
        self.clear_function(True)

        self.Format = QtWidgets.QLabel(self.frame)
        self.Format.setAlignment(QtCore.Qt.AlignCenter)
        self.Format.setObjectName("Format")
        # self.verticalLayout_2.addWidget(self.Format)

        self.Format.setMinimumSize(QtCore.QSize(125, 0))
        font = QtGui.QFont(self.os_font('name'), self.os_font('size'))
        self.Format.setFont(font)

        self.Format.setObjectName("Format")
        if platform.system() != 'Darwin':
            self.Format.setStyleSheet("QLabel {font-weight: bold}")
        
        self.verticalLayout_2.insertWidget(0, self.Format)

        _translate = QtCore.QCoreApplication.translate
        self.Format.setText(_translate("MainWindow", "Format"))


        self.Print = QtWidgets.QPushButton(self.frame)
        self.Print.setMinimumSize(QtCore.QSize(125, 0))
        font = QtGui.QFont(self.os_font('name'), self.os_font('size'), weight=QtGui.QFont.Light)
        self.Print.setFont(font)
        self.Print.setFlat(True)
        self.Print.setObjectName("Print")
        self.Print.setStyleSheet("QPushButton {background-color: white}"
                                 "QPushButton:hover {background-color: white}"
                                 "QPushButton:pressed {border: solid}"
                                 "QPushButton:pressed {border-width: 0px}"
                                 + ("" if self.settings['Print'] else "QPushButton {text-decoration: line-through}"))

        self.Print.clicked.connect(lambda state, setting='Print': self.settings_function(setting))

        _translate = QtCore.QCoreApplication.translate
        self.Print.setText(_translate("MainWindow", "Print"))

        self.verticalLayout_2.insertWidget(1, self.Print)
        # self.horizontalLayout_2.addWidget(self.Print)


        self.Video = QtWidgets.QPushButton(self.frame)
        self.Video.setMinimumSize(QtCore.QSize(125, 0))
        font = QtGui.QFont(self.os_font('name'), self.os_font('size'), weight=QtGui.QFont.Light)
        self.Video.setFont(font)
        self.Video.setFlat(True)
        self.Video.setObjectName("Video")
        self.Video.setStyleSheet("QPushButton {background-color: white}"
                                 "QPushButton:hover {background-color: white}"
                                 "QPushButton:pressed {border: solid}"
                                 "QPushButton:pressed {border-width: 0px}"
                                 + ("" if self.settings['Video'] else "QPushButton {text-decoration: line-through}"))

        self.Video.clicked.connect(lambda state, setting='Video': self.settings_function(setting))

        _translate = QtCore.QCoreApplication.translate
        self.Video.setText(_translate("MainWindow", "Video"))

        self.verticalLayout_2.insertWidget(2, self.Video)
        # self.horizontalLayout_2.addWidget(self.Video)


    def settings_function(self, setting):
        self.settings[setting] = not self.settings[setting]
        
        
        self.Print.setStyleSheet("QPushButton {background-color: white}"
                                 "QPushButton:hover {background-color: white}"
                                 "QPushButton:pressed {border: solid}"
                                 "QPushButton:pressed {border-width: 0px}"
                                 + ("" if self.settings['Print'] else "QPushButton {text-decoration: line-through}"))
        

        self.Video.setStyleSheet("QPushButton {background-color: white}"
                                 "QPushButton:hover {background-color: white}"
                                 "QPushButton:pressed {border: solid}"
                                 "QPushButton:pressed {border-width: 0px}"
                                 + ("" if self.settings['Video'] else "QPushButton {text-decoration: line-through}"))


    def base_path(self):
        try:
            if platform.system() == 'Darwin':
                base_path = Path(sys._MEIPASS).resolve()
            else:
                base_path = sys._MEIPASS
        except Exception:
            # if platform.system() == 'Darwin':
            base_path = Path(__file__).parent.resolve()
            # else:
                # base_path = Path(__file__).parent
    
        return Path(base_path)


    def os_font(self, font_property):
        if platform.system() == 'Windows':
            font_name = 'Segoe UI Light'
            font_size = 20
    
        if platform.system() == 'Darwin':
            font_name = 'Gill Sans'
            font_size = 32

        if platform.system() == 'Linux':
            font_name = 'Sawasdee'
            font_size = 20
            
        if font_property == 'name':
            return font_name
        
        if font_property == 'size':
            return font_size


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.setWindowTitle("The Chomsky Index")
    MainWindow.setWindowIcon(QtGui.QIcon(str(ui.base_path() / 'png' / 'icon_white.png')))
    MainWindow.show()
    sys.exit(app.exec_())
