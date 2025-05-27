# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'GUI_BASE.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import files_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1062, 869)
        MainWindow.setMinimumSize(QSize(1000, 720))
        palette = QPalette()
        brush = QBrush(QColor(255, 255, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.WindowText, brush)
        brush1 = QBrush(QColor(0, 0, 0, 0))
        brush1.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Button, brush1)
        brush2 = QBrush(QColor(66, 73, 90, 255))
        brush2.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Light, brush2)
        brush3 = QBrush(QColor(55, 61, 75, 255))
        brush3.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Midlight, brush3)
        brush4 = QBrush(QColor(22, 24, 30, 255))
        brush4.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Dark, brush4)
        brush5 = QBrush(QColor(29, 32, 40, 255))
        brush5.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Mid, brush5)
        brush6 = QBrush(QColor(210, 210, 210, 255))
        brush6.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Text, brush6)
        palette.setBrush(QPalette.Active, QPalette.BrightText, brush)
        palette.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette.setBrush(QPalette.Active, QPalette.Base, brush1)
        palette.setBrush(QPalette.Active, QPalette.Window, brush1)
        brush7 = QBrush(QColor(0, 0, 0, 255))
        brush7.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Shadow, brush7)
        brush8 = QBrush(QColor(85, 170, 255, 255))
        brush8.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Highlight, brush8)
        palette.setBrush(QPalette.Active, QPalette.Link, brush8)
        brush9 = QBrush(QColor(255, 0, 127, 255))
        brush9.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.LinkVisited, brush9)
        palette.setBrush(QPalette.Active, QPalette.AlternateBase, brush4)
        brush10 = QBrush(QColor(44, 49, 60, 255))
        brush10.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.ToolTipBase, brush10)
        palette.setBrush(QPalette.Active, QPalette.ToolTipText, brush6)
        palette.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Button, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Light, brush2)
        palette.setBrush(QPalette.Inactive, QPalette.Midlight, brush3)
        palette.setBrush(QPalette.Inactive, QPalette.Dark, brush4)
        palette.setBrush(QPalette.Inactive, QPalette.Mid, brush5)
        palette.setBrush(QPalette.Inactive, QPalette.Text, brush6)
        palette.setBrush(QPalette.Inactive, QPalette.BrightText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Base, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Window, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Shadow, brush7)
        palette.setBrush(QPalette.Inactive, QPalette.Highlight, brush8)
        palette.setBrush(QPalette.Inactive, QPalette.Link, brush8)
        palette.setBrush(QPalette.Inactive, QPalette.LinkVisited, brush9)
        palette.setBrush(QPalette.Inactive, QPalette.AlternateBase, brush4)
        palette.setBrush(QPalette.Inactive, QPalette.ToolTipBase, brush10)
        palette.setBrush(QPalette.Inactive, QPalette.ToolTipText, brush6)
        palette.setBrush(QPalette.Disabled, QPalette.WindowText, brush4)
        palette.setBrush(QPalette.Disabled, QPalette.Button, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Light, brush2)
        palette.setBrush(QPalette.Disabled, QPalette.Midlight, brush3)
        palette.setBrush(QPalette.Disabled, QPalette.Dark, brush4)
        palette.setBrush(QPalette.Disabled, QPalette.Mid, brush5)
        palette.setBrush(QPalette.Disabled, QPalette.Text, brush4)
        palette.setBrush(QPalette.Disabled, QPalette.BrightText, brush)
        palette.setBrush(QPalette.Disabled, QPalette.ButtonText, brush4)
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Window, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Shadow, brush7)
        brush11 = QBrush(QColor(51, 153, 255, 255))
        brush11.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.Highlight, brush11)
        palette.setBrush(QPalette.Disabled, QPalette.Link, brush8)
        palette.setBrush(QPalette.Disabled, QPalette.LinkVisited, brush9)
        palette.setBrush(QPalette.Disabled, QPalette.AlternateBase, brush10)
        palette.setBrush(QPalette.Disabled, QPalette.ToolTipBase, brush10)
        palette.setBrush(QPalette.Disabled, QPalette.ToolTipText, brush6)
        MainWindow.setPalette(palette)
        font = QFont()
        font.setFamily(u"Segoe UI")
        font.setPointSize(10)
        MainWindow.setFont(font)
        MainWindow.setStyleSheet(u"QMainWindow {background: transparent; }\n"
"QToolTip {\n"
"	color: #ffffff;\n"
"	background-color: rgba(27, 29, 35, 160);\n"
"	border: 1px solid rgb(40, 40, 40);\n"
"	border-radius: 2px;\n"
"}")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"background: transparent;\n"
"color: rgb(210, 210, 210);")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(10, 10, 10, 10)
        self.frame_main = QFrame(self.centralwidget)
        self.frame_main.setObjectName(u"frame_main")
        self.frame_main.setStyleSheet(u"/* LINE EDIT */\n"
"QLineEdit {\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(27, 29, 35);\n"
"	padding-left: 10px;\n"
"}\n"
"QLineEdit:hover {\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QLineEdit:focus {\n"
"	border: 2px solid rgb(91, 101, 124);\n"
"}\n"
"\n"
"/* SCROLL BARS */\n"
"QScrollBar:horizontal {\n"
"    border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    height: 14px;\n"
"    margin: 0px 21px 0 21px;\n"
"	border-radius: 0px;\n"
"}\n"
"QScrollBar::handle:horizontal {\n"
"    background: rgb(85, 170, 255);\n"
"    min-width: 25px;\n"
"	border-radius: 7px\n"
"}\n"
"QScrollBar::add-line:horizontal {\n"
"    border: none;\n"
"    background: rgb(55, 63, 77);\n"
"    width: 20px;\n"
"	border-top-right-radius: 7px;\n"
"    border-bottom-right-radius: 7px;\n"
"    subcontrol-position: right;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::sub-line:horizontal {\n"
"    border: none;\n"
"    background: rgb(55, 63, 77);\n"
"    width: 20px;\n"
""
                        "	border-top-left-radius: 7px;\n"
"    border-bottom-left-radius: 7px;\n"
"    subcontrol-position: left;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal\n"
"{\n"
"     background: none;\n"
"}\n"
"QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal\n"
"{\n"
"     background: none;\n"
"}\n"
" QScrollBar:vertical {\n"
"	border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    width: 14px;\n"
"    margin: 21px 0 21px 0;\n"
"	border-radius: 0px;\n"
" }\n"
" QScrollBar::handle:vertical {	\n"
"	background: rgb(85, 170, 255);\n"
"    min-height: 25px;\n"
"	border-radius: 7px\n"
" }\n"
" QScrollBar::add-line:vertical {\n"
"     border: none;\n"
"    background: rgb(55, 63, 77);\n"
"     height: 20px;\n"
"	border-bottom-left-radius: 7px;\n"
"    border-bottom-right-radius: 7px;\n"
"     subcontrol-position: bottom;\n"
"     subcontrol-origin: margin;\n"
" }\n"
" QScrollBar::sub-line:vertical {\n"
"	border: none;\n"
"    background: rgb(55, 63"
                        ", 77);\n"
"     height: 20px;\n"
"	border-top-left-radius: 7px;\n"
"    border-top-right-radius: 7px;\n"
"     subcontrol-position: top;\n"
"     subcontrol-origin: margin;\n"
" }\n"
" QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
"     background: none;\n"
" }\n"
"\n"
" QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
"     background: none;\n"
" }\n"
"\n"
"/* CHECKBOX */\n"
"QCheckBox::indicator {\n"
"    border: 3px solid rgb(52, 59, 72);\n"
"	width: 15px;\n"
"	height: 15px;\n"
"	border-radius: 10px;\n"
"    background: rgb(44, 49, 60);\n"
"}\n"
"QCheckBox::indicator:hover {\n"
"    border: 3px solid rgb(58, 66, 81);\n"
"}\n"
"QCheckBox::indicator:checked {\n"
"    background: 3px solid rgb(52, 59, 72);\n"
"	border: 3px solid rgb(52, 59, 72);	\n"
"	background-image: url(:/16x16/icons/16x16/cil-check-alt.png);\n"
"}\n"
"\n"
"/* RADIO BUTTON */\n"
"QRadioButton::indicator {\n"
"    border: 3px solid rgb(52, 59, 72);\n"
"	width: 15px;\n"
"	height: 15px;\n"
"	border-radius"
                        ": 10px;\n"
"    background: rgb(44, 49, 60);\n"
"}\n"
"QRadioButton::indicator:hover {\n"
"    border: 3px solid rgb(58, 66, 81);\n"
"}\n"
"QRadioButton::indicator:checked {\n"
"    background: 3px solid rgb(94, 106, 130);\n"
"	border: 3px solid rgb(52, 59, 72);	\n"
"}\n"
"\n"
"/* COMBOBOX */\n"
"QComboBox{\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(27, 29, 35);\n"
"	padding: 5px;\n"
"	padding-left: 10px;\n"
"}\n"
"QComboBox:hover{\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QComboBox::drop-down {\n"
"	subcontrol-origin: padding;\n"
"	subcontrol-position: top right;\n"
"	width: 25px; \n"
"	border-left-width: 3px;\n"
"	border-left-color: rgba(39, 44, 54, 150);\n"
"	border-left-style: solid;\n"
"	border-top-right-radius: 3px;\n"
"	border-bottom-right-radius: 3px;	\n"
"	background-image: url(:/16x16/icons/16x16/cil-arrow-bottom.png);\n"
"	background-position: center;\n"
"	background-repeat: no-reperat;\n"
" }\n"
"QComboBox QAbstractItemView {\n"
"	color: rgb("
                        "85, 170, 255);	\n"
"	background-color: rgb(27, 29, 35);\n"
"	padding: 10px;\n"
"	selection-background-color: rgb(39, 44, 54);\n"
"}\n"
"\n"
"/* SLIDERS */\n"
"QSlider::groove:horizontal {\n"
"    border-radius: 9px;\n"
"    height: 18px;\n"
"	margin: 0px;\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QSlider::groove:horizontal:hover {\n"
"	background-color: rgb(55, 62, 76);\n"
"}\n"
"QSlider::handle:horizontal {\n"
"    background-color: rgb(85, 170, 255);\n"
"    border: none;\n"
"    height: 18px;\n"
"    width: 18px;\n"
"    margin: 0px;\n"
"	border-radius: 9px;\n"
"}\n"
"QSlider::handle:horizontal:hover {\n"
"    background-color: rgb(105, 180, 255);\n"
"}\n"
"QSlider::handle:horizontal:pressed {\n"
"    background-color: rgb(65, 130, 195);\n"
"}\n"
"\n"
"QSlider::groove:vertical {\n"
"    border-radius: 9px;\n"
"    width: 18px;\n"
"    margin: 0px;\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QSlider::groove:vertical:hover {\n"
"	background-color: rgb(55, 62, 76);\n"
"}\n"
"QSlider::handle:verti"
                        "cal {\n"
"    background-color: rgb(85, 170, 255);\n"
"	border: none;\n"
"    height: 18px;\n"
"    width: 18px;\n"
"    margin: 0px;\n"
"	border-radius: 9px;\n"
"}\n"
"QSlider::handle:vertical:hover {\n"
"    background-color: rgb(105, 180, 255);\n"
"}\n"
"QSlider::handle:vertical:pressed {\n"
"    background-color: rgb(65, 130, 195);\n"
"}\n"
"\n"
"")
        self.frame_main.setFrameShape(QFrame.NoFrame)
        self.frame_main.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame_main)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame_top = QFrame(self.frame_main)
        self.frame_top.setObjectName(u"frame_top")
        self.frame_top.setMinimumSize(QSize(0, 65))
        self.frame_top.setMaximumSize(QSize(16777215, 65))
        self.frame_top.setStyleSheet(u"background-color: transparent;")
        self.frame_top.setFrameShape(QFrame.NoFrame)
        self.frame_top.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_top)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.frame_toggle = QFrame(self.frame_top)
        self.frame_toggle.setObjectName(u"frame_toggle")
        self.frame_toggle.setMaximumSize(QSize(70, 16777215))
        self.frame_toggle.setStyleSheet(u"background-color: rgb(27, 29, 35);")
        self.frame_toggle.setFrameShape(QFrame.NoFrame)
        self.frame_toggle.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_toggle)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.btn_toggle_menu = QPushButton(self.frame_toggle)
        self.btn_toggle_menu.setObjectName(u"btn_toggle_menu")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_toggle_menu.sizePolicy().hasHeightForWidth())
        self.btn_toggle_menu.setSizePolicy(sizePolicy)
        self.btn_toggle_menu.setStyleSheet(u"QPushButton {\n"
"	background-image: url(:/24x24/icons/24x24/cil-menu.png);\n"
"	background-position: center;\n"
"	background-repeat: no-reperat;\n"
"	border: none;\n"
"	background-color: rgb(27, 29, 35);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(33, 37, 43);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(85, 170, 255);\n"
"}")

        self.verticalLayout_3.addWidget(self.btn_toggle_menu)


        self.horizontalLayout_3.addWidget(self.frame_toggle)

        self.frame_top_right = QFrame(self.frame_top)
        self.frame_top_right.setObjectName(u"frame_top_right")
        self.frame_top_right.setStyleSheet(u"background: transparent;")
        self.frame_top_right.setFrameShape(QFrame.NoFrame)
        self.frame_top_right.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_top_right)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frame_top_btns = QFrame(self.frame_top_right)
        self.frame_top_btns.setObjectName(u"frame_top_btns")
        self.frame_top_btns.setMaximumSize(QSize(16777215, 42))
        self.frame_top_btns.setStyleSheet(u"background-color: rgba(27, 29, 35, 200)")
        self.frame_top_btns.setFrameShape(QFrame.NoFrame)
        self.frame_top_btns.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame_top_btns)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.frame_label_top_btns = QFrame(self.frame_top_btns)
        self.frame_label_top_btns.setObjectName(u"frame_label_top_btns")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.frame_label_top_btns.sizePolicy().hasHeightForWidth())
        self.frame_label_top_btns.setSizePolicy(sizePolicy1)
        self.frame_label_top_btns.setFrameShape(QFrame.NoFrame)
        self.frame_label_top_btns.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_10 = QHBoxLayout(self.frame_label_top_btns)
        self.horizontalLayout_10.setSpacing(0)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(5, 0, 10, 0)
        self.frame_icon_top_bar = QFrame(self.frame_label_top_btns)
        self.frame_icon_top_bar.setObjectName(u"frame_icon_top_bar")
        self.frame_icon_top_bar.setMaximumSize(QSize(30, 30))
        self.frame_icon_top_bar.setStyleSheet(u"background: transparent;\n"
"background-image: url(:/16x16/icons/16x16/cil-terminal.png);\n"
"background-position: center;\n"
"background-repeat: no-repeat;\n"
"")
        self.frame_icon_top_bar.setFrameShape(QFrame.StyledPanel)
        self.frame_icon_top_bar.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_10.addWidget(self.frame_icon_top_bar)

        self.label_title_bar_top = QLabel(self.frame_label_top_btns)
        self.label_title_bar_top.setObjectName(u"label_title_bar_top")
        font1 = QFont()
        font1.setFamily(u"Segoe UI")
        font1.setPointSize(10)
        font1.setBold(True)
        font1.setWeight(75)
        self.label_title_bar_top.setFont(font1)
        self.label_title_bar_top.setStyleSheet(u"background: transparent;\n"
"")

        self.horizontalLayout_10.addWidget(self.label_title_bar_top)


        self.horizontalLayout_4.addWidget(self.frame_label_top_btns)

        self.frame_btns_right = QFrame(self.frame_top_btns)
        self.frame_btns_right.setObjectName(u"frame_btns_right")
        sizePolicy1.setHeightForWidth(self.frame_btns_right.sizePolicy().hasHeightForWidth())
        self.frame_btns_right.setSizePolicy(sizePolicy1)
        self.frame_btns_right.setMaximumSize(QSize(120, 16777215))
        self.frame_btns_right.setFrameShape(QFrame.NoFrame)
        self.frame_btns_right.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.frame_btns_right)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)

        self.horizontalLayout_4.addWidget(self.frame_btns_right, 0, Qt.AlignRight)


        self.verticalLayout_2.addWidget(self.frame_top_btns)

        self.frame_top_info = QFrame(self.frame_top_right)
        self.frame_top_info.setObjectName(u"frame_top_info")
        self.frame_top_info.setMaximumSize(QSize(16777215, 65))
        self.frame_top_info.setStyleSheet(u"background-color: rgb(39, 44, 54);")
        self.frame_top_info.setFrameShape(QFrame.NoFrame)
        self.frame_top_info.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.frame_top_info)
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(10, 0, 10, 0)
        self.label_top_info_1 = QLabel(self.frame_top_info)
        self.label_top_info_1.setObjectName(u"label_top_info_1")
        self.label_top_info_1.setMaximumSize(QSize(16777215, 15))
        font2 = QFont()
        font2.setFamily(u"Segoe UI")
        self.label_top_info_1.setFont(font2)
        self.label_top_info_1.setStyleSheet(u"color: rgb(98, 103, 111); ")

        self.horizontalLayout_8.addWidget(self.label_top_info_1)

        self.label_top_info_2 = QLabel(self.frame_top_info)
        self.label_top_info_2.setObjectName(u"label_top_info_2")
        self.label_top_info_2.setMinimumSize(QSize(0, 0))
        self.label_top_info_2.setMaximumSize(QSize(250, 20))
        font3 = QFont()
        font3.setFamily(u"Segoe UI")
        font3.setBold(True)
        font3.setWeight(75)
        self.label_top_info_2.setFont(font3)
        self.label_top_info_2.setStyleSheet(u"color: rgb(98, 103, 111);")
        self.label_top_info_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_8.addWidget(self.label_top_info_2)


        self.verticalLayout_2.addWidget(self.frame_top_info)


        self.horizontalLayout_3.addWidget(self.frame_top_right)


        self.verticalLayout.addWidget(self.frame_top)

        self.frame_center = QFrame(self.frame_main)
        self.frame_center.setObjectName(u"frame_center")
        sizePolicy.setHeightForWidth(self.frame_center.sizePolicy().hasHeightForWidth())
        self.frame_center.setSizePolicy(sizePolicy)
        self.frame_center.setStyleSheet(u"background-color: rgb(40, 44, 52);")
        self.frame_center.setFrameShape(QFrame.NoFrame)
        self.frame_center.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_center)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frame_left_menu = QFrame(self.frame_center)
        self.frame_left_menu.setObjectName(u"frame_left_menu")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.frame_left_menu.sizePolicy().hasHeightForWidth())
        self.frame_left_menu.setSizePolicy(sizePolicy2)
        self.frame_left_menu.setMinimumSize(QSize(70, 0))
        self.frame_left_menu.setMaximumSize(QSize(70, 16777215))
        self.frame_left_menu.setLayoutDirection(Qt.LeftToRight)
        self.frame_left_menu.setStyleSheet(u"background-color: rgb(27, 29, 35);")
        self.frame_left_menu.setFrameShape(QFrame.NoFrame)
        self.frame_left_menu.setFrameShadow(QFrame.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.frame_left_menu)
        self.verticalLayout_5.setSpacing(1)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.frame_menus = QFrame(self.frame_left_menu)
        self.frame_menus.setObjectName(u"frame_menus")
        self.frame_menus.setFrameShape(QFrame.NoFrame)
        self.frame_menus.setFrameShadow(QFrame.Raised)
        self.layout_menus = QVBoxLayout(self.frame_menus)
        self.layout_menus.setSpacing(0)
        self.layout_menus.setObjectName(u"layout_menus")
        self.layout_menus.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout_5.addWidget(self.frame_menus, 0, Qt.AlignTop)

        self.frame_extra_menus = QFrame(self.frame_left_menu)
        self.frame_extra_menus.setObjectName(u"frame_extra_menus")
        sizePolicy2.setHeightForWidth(self.frame_extra_menus.sizePolicy().hasHeightForWidth())
        self.frame_extra_menus.setSizePolicy(sizePolicy2)
        self.frame_extra_menus.setFrameShape(QFrame.NoFrame)
        self.frame_extra_menus.setFrameShadow(QFrame.Raised)
        self.layout_menu_bottom = QVBoxLayout(self.frame_extra_menus)
        self.layout_menu_bottom.setSpacing(10)
        self.layout_menu_bottom.setObjectName(u"layout_menu_bottom")
        self.layout_menu_bottom.setContentsMargins(0, 0, 0, 25)

        self.verticalLayout_5.addWidget(self.frame_extra_menus, 0, Qt.AlignBottom)


        self.horizontalLayout_2.addWidget(self.frame_left_menu)

        self.frame_content_right = QFrame(self.frame_center)
        self.frame_content_right.setObjectName(u"frame_content_right")
        self.frame_content_right.setStyleSheet(u"background-color: rgb(44, 49, 60);")
        self.frame_content_right.setFrameShape(QFrame.NoFrame)
        self.frame_content_right.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frame_content_right)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.frame_content = QFrame(self.frame_content_right)
        self.frame_content.setObjectName(u"frame_content")
        self.frame_content.setFrameShape(QFrame.NoFrame)
        self.frame_content.setFrameShadow(QFrame.Raised)
        self.verticalLayout_9 = QVBoxLayout(self.frame_content)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(5, 5, 5, 5)
        self.stackedWidget = QStackedWidget(self.frame_content)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setStyleSheet(u"background: transparent;")
        self.page_home = QWidget()
        self.page_home.setObjectName(u"page_home")
        self.verticalLayout_10 = QVBoxLayout(self.page_home)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.EmpleadosBox = QComboBox(self.page_home)
        self.EmpleadosBox.setObjectName(u"EmpleadosBox")

        self.gridLayout_2.addWidget(self.EmpleadosBox, 1, 1, 1, 1)

        self.label_6 = QLabel(self.page_home)
        self.label_6.setObjectName(u"label_6")
        font4 = QFont()
        font4.setFamily(u"Segoe UI")
        font4.setPointSize(40)
        self.label_6.setFont(font4)
        self.label_6.setStyleSheet(u"")
        self.label_6.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.label_6, 0, 0, 1, 2)

        self.label_2 = QLabel(self.page_home)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(0, 150))
        self.label_2.setMaximumSize(QSize(942, 150))

        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)

        self.label_3 = QLabel(self.page_home)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_2.addWidget(self.label_3, 2, 0, 1, 1)

        self.codeReaderInput = QLineEdit(self.page_home)
        self.codeReaderInput.setObjectName(u"codeReaderInput")

        self.gridLayout_2.addWidget(self.codeReaderInput, 2, 1, 1, 1)


        self.verticalLayout_10.addLayout(self.gridLayout_2)

        self.WidgetTabla = QWidget(self.page_home)
        self.WidgetTabla.setObjectName(u"WidgetTabla")

        self.verticalLayout_10.addWidget(self.WidgetTabla)

        self.btnRegisterVale = QPushButton(self.page_home)
        self.btnRegisterVale.setObjectName(u"btnRegisterVale")
        self.btnRegisterVale.setMinimumSize(QSize(150, 30))
        font5 = QFont()
        font5.setFamily(u"Segoe UI")
        font5.setPointSize(9)
        self.btnRegisterVale.setFont(font5)
        self.btnRegisterVale.setStyleSheet(u"QPushButton {\n"
"	border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(57, 65, 80);\n"
"	border: 2px solid rgb(61, 70, 86);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(35, 40, 49);\n"
"	border: 2px solid rgb(43, 50, 61);\n"
"}")
        icon = QIcon()
        icon.addFile(u":/16x16/icons/16x16/cil-folder-open.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btnRegisterVale.setIcon(icon)

        self.verticalLayout_10.addWidget(self.btnRegisterVale)

        self.btnActualizarDB = QPushButton(self.page_home)
        self.btnActualizarDB.setObjectName(u"btnActualizarDB")
        self.btnActualizarDB.setMinimumSize(QSize(150, 30))
        self.btnActualizarDB.setFont(font5)
        self.btnActualizarDB.setStyleSheet(u"QPushButton {\n"
"	border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(57, 65, 80);\n"
"	border: 2px solid rgb(61, 70, 86);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(35, 40, 49);\n"
"	border: 2px solid rgb(43, 50, 61);\n"
"}")
        self.btnActualizarDB.setIcon(icon)

        self.verticalLayout_10.addWidget(self.btnActualizarDB)

        self.EliminarTODO = QPushButton(self.page_home)
        self.EliminarTODO.setObjectName(u"EliminarTODO")
        self.EliminarTODO.setMinimumSize(QSize(150, 30))
        self.EliminarTODO.setFont(font5)
        self.EliminarTODO.setStyleSheet(u"QPushButton {\n"
"	color: rgb(255, 0, 0);\n"
"	border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(57, 65, 80);\n"
"	border: 2px solid rgb(61, 70, 86);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(35, 40, 49);\n"
"	border: 2px solid rgb(43, 50, 61);\n"
"}")
        self.EliminarTODO.setIcon(icon)

        self.verticalLayout_10.addWidget(self.EliminarTODO)

        self.stackedWidget.addWidget(self.page_home)
        self.create_user = QWidget()
        self.create_user.setObjectName(u"create_user")
        self.create_user.setMaximumSize(QSize(16777215, 749))
        self.verticalLayout_11 = QVBoxLayout(self.create_user)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_15 = QVBoxLayout()
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.label = QLabel(self.create_user)
        self.label.setObjectName(u"label")

        self.verticalLayout_15.addWidget(self.label)


        self.verticalLayout_11.addLayout(self.verticalLayout_15)

        self.frame_div_content_7 = QFrame(self.create_user)
        self.frame_div_content_7.setObjectName(u"frame_div_content_7")
        self.frame_div_content_7.setMinimumSize(QSize(0, 110))
        self.frame_div_content_7.setMaximumSize(QSize(16777215, 110))
        self.frame_div_content_7.setStyleSheet(u"background-color: rgb(41, 45, 56);\n"
"border-radius: 5px;\n"
"")
        self.frame_div_content_7.setFrameShape(QFrame.NoFrame)
        self.frame_div_content_7.setFrameShadow(QFrame.Raised)
        self.verticalLayout_44 = QVBoxLayout(self.frame_div_content_7)
        self.verticalLayout_44.setSpacing(0)
        self.verticalLayout_44.setObjectName(u"verticalLayout_44")
        self.verticalLayout_44.setContentsMargins(0, 0, 0, 0)
        self.frame_title_wid_8 = QFrame(self.frame_div_content_7)
        self.frame_title_wid_8.setObjectName(u"frame_title_wid_8")
        self.frame_title_wid_8.setMaximumSize(QSize(16777215, 35))
        self.frame_title_wid_8.setStyleSheet(u"background-color: rgb(39, 44, 54);")
        self.frame_title_wid_8.setFrameShape(QFrame.StyledPanel)
        self.frame_title_wid_8.setFrameShadow(QFrame.Raised)
        self.verticalLayout_45 = QVBoxLayout(self.frame_title_wid_8)
        self.verticalLayout_45.setObjectName(u"verticalLayout_45")
        self.labelBoxNombreEmpleado = QLabel(self.frame_title_wid_8)
        self.labelBoxNombreEmpleado.setObjectName(u"labelBoxNombreEmpleado")
        self.labelBoxNombreEmpleado.setFont(font1)
        self.labelBoxNombreEmpleado.setStyleSheet(u"")

        self.verticalLayout_45.addWidget(self.labelBoxNombreEmpleado)


        self.verticalLayout_44.addWidget(self.frame_title_wid_8)

        self.frame_content_wid_8 = QFrame(self.frame_div_content_7)
        self.frame_content_wid_8.setObjectName(u"frame_content_wid_8")
        self.frame_content_wid_8.setFrameShape(QFrame.NoFrame)
        self.frame_content_wid_8.setFrameShadow(QFrame.Raised)
        self.verticalLayout_46 = QVBoxLayout(self.frame_content_wid_8)
        self.verticalLayout_46.setObjectName(u"verticalLayout_46")
        self.verticalLayout_47 = QVBoxLayout()
        self.verticalLayout_47.setObjectName(u"verticalLayout_47")
        self.verticalLayout_47.setContentsMargins(-1, -1, -1, 0)
        self.Nombre_Empleado = QLineEdit(self.frame_content_wid_8)
        self.Nombre_Empleado.setObjectName(u"Nombre_Empleado")
        self.Nombre_Empleado.setMinimumSize(QSize(0, 30))
        self.Nombre_Empleado.setStyleSheet(u"QLineEdit {\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(27, 29, 35);\n"
"	padding-left: 10px;\n"
"}\n"
"QLineEdit:hover {\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QLineEdit:focus {\n"
"	border: 2px solid rgb(91, 101, 124);\n"
"}")

        self.verticalLayout_47.addWidget(self.Nombre_Empleado)


        self.verticalLayout_46.addLayout(self.verticalLayout_47)


        self.verticalLayout_44.addWidget(self.frame_content_wid_8)


        self.verticalLayout_11.addWidget(self.frame_div_content_7)

        self.frame_div_content_11 = QFrame(self.create_user)
        self.frame_div_content_11.setObjectName(u"frame_div_content_11")
        self.frame_div_content_11.setMinimumSize(QSize(0, 110))
        self.frame_div_content_11.setMaximumSize(QSize(16777215, 110))
        self.frame_div_content_11.setStyleSheet(u"background-color: rgb(41, 45, 56);\n"
"border-radius: 5px;\n"
"")
        self.frame_div_content_11.setFrameShape(QFrame.NoFrame)
        self.frame_div_content_11.setFrameShadow(QFrame.Raised)
        self.verticalLayout_49 = QVBoxLayout(self.frame_div_content_11)
        self.verticalLayout_49.setSpacing(0)
        self.verticalLayout_49.setObjectName(u"verticalLayout_49")
        self.verticalLayout_49.setContentsMargins(0, 0, 0, 0)
        self.frame_title_wid_12 = QFrame(self.frame_div_content_11)
        self.frame_title_wid_12.setObjectName(u"frame_title_wid_12")
        self.frame_title_wid_12.setMaximumSize(QSize(16777215, 35))
        self.frame_title_wid_12.setStyleSheet(u"background-color: rgb(39, 44, 54);")
        self.frame_title_wid_12.setFrameShape(QFrame.StyledPanel)
        self.frame_title_wid_12.setFrameShadow(QFrame.Raised)
        self.verticalLayout_61 = QVBoxLayout(self.frame_title_wid_12)
        self.verticalLayout_61.setObjectName(u"verticalLayout_61")
        self.labelBoxBlenderInstalation_17 = QLabel(self.frame_title_wid_12)
        self.labelBoxBlenderInstalation_17.setObjectName(u"labelBoxBlenderInstalation_17")
        self.labelBoxBlenderInstalation_17.setFont(font1)
        self.labelBoxBlenderInstalation_17.setStyleSheet(u"")

        self.verticalLayout_61.addWidget(self.labelBoxBlenderInstalation_17)


        self.verticalLayout_49.addWidget(self.frame_title_wid_12)

        self.frame_content_wid_12 = QFrame(self.frame_div_content_11)
        self.frame_content_wid_12.setObjectName(u"frame_content_wid_12")
        self.frame_content_wid_12.setFrameShape(QFrame.NoFrame)
        self.frame_content_wid_12.setFrameShadow(QFrame.Raised)
        self.verticalLayout_62 = QVBoxLayout(self.frame_content_wid_12)
        self.verticalLayout_62.setObjectName(u"verticalLayout_62")
        self.verticalLayout_63 = QVBoxLayout()
        self.verticalLayout_63.setObjectName(u"verticalLayout_63")
        self.verticalLayout_63.setContentsMargins(-1, -1, -1, 0)
        self.Cedula_Empleado = QLineEdit(self.frame_content_wid_12)
        self.Cedula_Empleado.setObjectName(u"Cedula_Empleado")
        self.Cedula_Empleado.setMinimumSize(QSize(0, 30))
        self.Cedula_Empleado.setStyleSheet(u"QLineEdit {\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(27, 29, 35);\n"
"	padding-left: 10px;\n"
"}\n"
"QLineEdit:hover {\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QLineEdit:focus {\n"
"	border: 2px solid rgb(91, 101, 124);\n"
"}")

        self.verticalLayout_63.addWidget(self.Cedula_Empleado)


        self.verticalLayout_62.addLayout(self.verticalLayout_63)


        self.verticalLayout_49.addWidget(self.frame_content_wid_12)


        self.verticalLayout_11.addWidget(self.frame_div_content_11)

        self.frame_div_content_12 = QFrame(self.create_user)
        self.frame_div_content_12.setObjectName(u"frame_div_content_12")
        self.frame_div_content_12.setMinimumSize(QSize(0, 110))
        self.frame_div_content_12.setMaximumSize(QSize(16777215, 110))
        self.frame_div_content_12.setStyleSheet(u"background-color: rgb(41, 45, 56);\n"
"border-radius: 5px;\n"
"")
        self.frame_div_content_12.setFrameShape(QFrame.NoFrame)
        self.frame_div_content_12.setFrameShadow(QFrame.Raised)
        self.verticalLayout_64 = QVBoxLayout(self.frame_div_content_12)
        self.verticalLayout_64.setSpacing(0)
        self.verticalLayout_64.setObjectName(u"verticalLayout_64")
        self.verticalLayout_64.setContentsMargins(0, 0, 0, 0)
        self.frame_title_wid_13 = QFrame(self.frame_div_content_12)
        self.frame_title_wid_13.setObjectName(u"frame_title_wid_13")
        self.frame_title_wid_13.setMaximumSize(QSize(16777215, 35))
        self.frame_title_wid_13.setStyleSheet(u"background-color: rgb(39, 44, 54);")
        self.frame_title_wid_13.setFrameShape(QFrame.StyledPanel)
        self.frame_title_wid_13.setFrameShadow(QFrame.Raised)
        self.verticalLayout_65 = QVBoxLayout(self.frame_title_wid_13)
        self.verticalLayout_65.setObjectName(u"verticalLayout_65")
        self.la = QLabel(self.frame_title_wid_13)
        self.la.setObjectName(u"la")
        self.la.setFont(font1)
        self.la.setStyleSheet(u"")

        self.verticalLayout_65.addWidget(self.la)


        self.verticalLayout_64.addWidget(self.frame_title_wid_13)

        self.frame_content_wid_13 = QFrame(self.frame_div_content_12)
        self.frame_content_wid_13.setObjectName(u"frame_content_wid_13")
        self.frame_content_wid_13.setFrameShape(QFrame.NoFrame)
        self.frame_content_wid_13.setFrameShadow(QFrame.Raised)
        self.verticalLayout_66 = QVBoxLayout(self.frame_content_wid_13)
        self.verticalLayout_66.setObjectName(u"verticalLayout_66")
        self.verticalLayout_67 = QVBoxLayout()
        self.verticalLayout_67.setObjectName(u"verticalLayout_67")
        self.verticalLayout_67.setContentsMargins(-1, -1, -1, 0)
        self.Celular_Empleado = QLineEdit(self.frame_content_wid_13)
        self.Celular_Empleado.setObjectName(u"Celular_Empleado")
        self.Celular_Empleado.setMinimumSize(QSize(0, 30))
        self.Celular_Empleado.setStyleSheet(u"QLineEdit {\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(27, 29, 35);\n"
"	padding-left: 10px;\n"
"}\n"
"QLineEdit:hover {\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QLineEdit:focus {\n"
"	border: 2px solid rgb(91, 101, 124);\n"
"}")

        self.verticalLayout_67.addWidget(self.Celular_Empleado)


        self.verticalLayout_66.addLayout(self.verticalLayout_67)


        self.verticalLayout_64.addWidget(self.frame_content_wid_13)


        self.verticalLayout_11.addWidget(self.frame_div_content_12)

        self.frame_div_content_13 = QFrame(self.create_user)
        self.frame_div_content_13.setObjectName(u"frame_div_content_13")
        self.frame_div_content_13.setMinimumSize(QSize(0, 110))
        self.frame_div_content_13.setMaximumSize(QSize(16777215, 110))
        self.frame_div_content_13.setStyleSheet(u"background-color: rgb(41, 45, 56);\n"
"border-radius: 5px;\n"
"")
        self.frame_div_content_13.setFrameShape(QFrame.NoFrame)
        self.frame_div_content_13.setFrameShadow(QFrame.Raised)
        self.verticalLayout_68 = QVBoxLayout(self.frame_div_content_13)
        self.verticalLayout_68.setSpacing(0)
        self.verticalLayout_68.setObjectName(u"verticalLayout_68")
        self.verticalLayout_68.setContentsMargins(0, 0, 0, 0)
        self.frame_title_wid_14 = QFrame(self.frame_div_content_13)
        self.frame_title_wid_14.setObjectName(u"frame_title_wid_14")
        self.frame_title_wid_14.setMaximumSize(QSize(16777215, 35))
        self.frame_title_wid_14.setStyleSheet(u"background-color: rgb(39, 44, 54);")
        self.frame_title_wid_14.setFrameShape(QFrame.StyledPanel)
        self.frame_title_wid_14.setFrameShadow(QFrame.Raised)
        self.verticalLayout_69 = QVBoxLayout(self.frame_title_wid_14)
        self.verticalLayout_69.setObjectName(u"verticalLayout_69")
        self.labelBoxCorreo = QLabel(self.frame_title_wid_14)
        self.labelBoxCorreo.setObjectName(u"labelBoxCorreo")
        self.labelBoxCorreo.setFont(font1)
        self.labelBoxCorreo.setStyleSheet(u"")

        self.verticalLayout_69.addWidget(self.labelBoxCorreo)


        self.verticalLayout_68.addWidget(self.frame_title_wid_14)

        self.frame_content_wid_14 = QFrame(self.frame_div_content_13)
        self.frame_content_wid_14.setObjectName(u"frame_content_wid_14")
        self.frame_content_wid_14.setFrameShape(QFrame.NoFrame)
        self.frame_content_wid_14.setFrameShadow(QFrame.Raised)
        self.verticalLayout_70 = QVBoxLayout(self.frame_content_wid_14)
        self.verticalLayout_70.setObjectName(u"verticalLayout_70")
        self.verticalLayout_71 = QVBoxLayout()
        self.verticalLayout_71.setObjectName(u"verticalLayout_71")
        self.verticalLayout_71.setContentsMargins(-1, -1, -1, 0)
        self.Correo_Empleado = QLineEdit(self.frame_content_wid_14)
        self.Correo_Empleado.setObjectName(u"Correo_Empleado")
        self.Correo_Empleado.setMinimumSize(QSize(0, 30))
        self.Correo_Empleado.setStyleSheet(u"QLineEdit {\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(27, 29, 35);\n"
"	padding-left: 10px;\n"
"}\n"
"QLineEdit:hover {\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QLineEdit:focus {\n"
"	border: 2px solid rgb(91, 101, 124);\n"
"}")

        self.verticalLayout_71.addWidget(self.Correo_Empleado)


        self.verticalLayout_70.addLayout(self.verticalLayout_71)


        self.verticalLayout_68.addWidget(self.frame_content_wid_14)


        self.verticalLayout_11.addWidget(self.frame_div_content_13)

        self.btnAgregarEmpleado = QPushButton(self.create_user)
        self.btnAgregarEmpleado.setObjectName(u"btnAgregarEmpleado")
        self.btnAgregarEmpleado.setMinimumSize(QSize(150, 30))
        self.btnAgregarEmpleado.setFont(font5)
        self.btnAgregarEmpleado.setStyleSheet(u"QPushButton {\n"
"	border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(57, 65, 80);\n"
"	border: 2px solid rgb(61, 70, 86);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(35, 40, 49);\n"
"	border: 2px solid rgb(43, 50, 61);\n"
"}")
        self.btnAgregarEmpleado.setIcon(icon)

        self.verticalLayout_11.addWidget(self.btnAgregarEmpleado)

        self.stackedWidget.addWidget(self.create_user)
        self.page_widgets = QWidget()
        self.page_widgets.setObjectName(u"page_widgets")
        self.verticalLayout_6 = QVBoxLayout(self.page_widgets)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.frame = QFrame(self.page_widgets)
        self.frame.setObjectName(u"frame")
        self.frame.setStyleSheet(u"border-radius: 5px;")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frame)
        self.gridLayout.setObjectName(u"gridLayout")
        self.frame_div_content_4 = QFrame(self.frame)
        self.frame_div_content_4.setObjectName(u"frame_div_content_4")
        self.frame_div_content_4.setMinimumSize(QSize(0, 110))
        self.frame_div_content_4.setMaximumSize(QSize(16777215, 110))
        self.frame_div_content_4.setStyleSheet(u"background-color: rgb(41, 45, 56);\n"
"border-radius: 5px;\n"
"")
        self.frame_div_content_4.setFrameShape(QFrame.NoFrame)
        self.frame_div_content_4.setFrameShadow(QFrame.Raised)
        self.verticalLayout_32 = QVBoxLayout(self.frame_div_content_4)
        self.verticalLayout_32.setSpacing(0)
        self.verticalLayout_32.setObjectName(u"verticalLayout_32")
        self.verticalLayout_32.setContentsMargins(0, 0, 0, 0)
        self.frame_title_wid_5 = QFrame(self.frame_div_content_4)
        self.frame_title_wid_5.setObjectName(u"frame_title_wid_5")
        self.frame_title_wid_5.setMaximumSize(QSize(16777215, 35))
        self.frame_title_wid_5.setStyleSheet(u"background-color: rgb(39, 44, 54);")
        self.frame_title_wid_5.setFrameShape(QFrame.StyledPanel)
        self.frame_title_wid_5.setFrameShadow(QFrame.Raised)
        self.verticalLayout_33 = QVBoxLayout(self.frame_title_wid_5)
        self.verticalLayout_33.setObjectName(u"verticalLayout_33")
        self.labelBoxBlenderInstalation_13 = QLabel(self.frame_title_wid_5)
        self.labelBoxBlenderInstalation_13.setObjectName(u"labelBoxBlenderInstalation_13")
        self.labelBoxBlenderInstalation_13.setFont(font1)
        self.labelBoxBlenderInstalation_13.setStyleSheet(u"")

        self.verticalLayout_33.addWidget(self.labelBoxBlenderInstalation_13)


        self.verticalLayout_32.addWidget(self.frame_title_wid_5)

        self.frame_content_wid_5 = QFrame(self.frame_div_content_4)
        self.frame_content_wid_5.setObjectName(u"frame_content_wid_5")
        self.frame_content_wid_5.setFrameShape(QFrame.NoFrame)
        self.frame_content_wid_5.setFrameShadow(QFrame.Raised)
        self.verticalLayout_34 = QVBoxLayout(self.frame_content_wid_5)
        self.verticalLayout_34.setObjectName(u"verticalLayout_34")
        self.verticalLayout_35 = QVBoxLayout()
        self.verticalLayout_35.setObjectName(u"verticalLayout_35")
        self.verticalLayout_35.setContentsMargins(-1, -1, -1, 0)
        self.CampoTipoTrabajo = QLineEdit(self.frame_content_wid_5)
        self.CampoTipoTrabajo.setObjectName(u"CampoTipoTrabajo")
        self.CampoTipoTrabajo.setMinimumSize(QSize(0, 30))
        self.CampoTipoTrabajo.setStyleSheet(u"QLineEdit {\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(27, 29, 35);\n"
"	padding-left: 10px;\n"
"}\n"
"QLineEdit:hover {\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QLineEdit:focus {\n"
"	border: 2px solid rgb(91, 101, 124);\n"
"}")

        self.verticalLayout_35.addWidget(self.CampoTipoTrabajo)


        self.verticalLayout_34.addLayout(self.verticalLayout_35)


        self.verticalLayout_32.addWidget(self.frame_content_wid_5)


        self.gridLayout.addWidget(self.frame_div_content_4, 0, 0, 1, 1)

        self.frame_div_content_1 = QFrame(self.frame)
        self.frame_div_content_1.setObjectName(u"frame_div_content_1")
        self.frame_div_content_1.setMinimumSize(QSize(926, 110))
        self.frame_div_content_1.setMaximumSize(QSize(16777215, 110))
        self.frame_div_content_1.setStyleSheet(u"background-color: rgb(41, 45, 56);\n"
"border-radius: 5px;\n"
"")
        self.frame_div_content_1.setFrameShape(QFrame.NoFrame)
        self.frame_div_content_1.setFrameShadow(QFrame.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.frame_div_content_1)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.frame_title_wid_1 = QFrame(self.frame_div_content_1)
        self.frame_title_wid_1.setObjectName(u"frame_title_wid_1")
        self.frame_title_wid_1.setMaximumSize(QSize(16777215, 35))
        self.frame_title_wid_1.setStyleSheet(u"background-color: rgb(39, 44, 54);")
        self.frame_title_wid_1.setFrameShape(QFrame.StyledPanel)
        self.frame_title_wid_1.setFrameShadow(QFrame.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.frame_title_wid_1)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.labelBoxBlenderInstalation = QLabel(self.frame_title_wid_1)
        self.labelBoxBlenderInstalation.setObjectName(u"labelBoxBlenderInstalation")
        self.labelBoxBlenderInstalation.setFont(font1)
        self.labelBoxBlenderInstalation.setStyleSheet(u"")

        self.verticalLayout_8.addWidget(self.labelBoxBlenderInstalation)


        self.verticalLayout_7.addWidget(self.frame_title_wid_1)

        self.frame_content_wid_1 = QFrame(self.frame_div_content_1)
        self.frame_content_wid_1.setObjectName(u"frame_content_wid_1")
        self.frame_content_wid_1.setFrameShape(QFrame.NoFrame)
        self.frame_content_wid_1.setFrameShadow(QFrame.Raised)
        self.verticalLayout_12 = QVBoxLayout(self.frame_content_wid_1)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_27 = QVBoxLayout()
        self.verticalLayout_27.setSpacing(1)
        self.verticalLayout_27.setObjectName(u"verticalLayout_27")
        self.verticalLayout_27.setSizeConstraint(QLayout.SetMinimumSize)
        self.verticalLayout_27.setContentsMargins(-1, -1, -1, 0)
        self.CampoReferenciaTrabajo = QLineEdit(self.frame_content_wid_1)
        self.CampoReferenciaTrabajo.setObjectName(u"CampoReferenciaTrabajo")
        self.CampoReferenciaTrabajo.setMinimumSize(QSize(0, 30))
        self.CampoReferenciaTrabajo.setStyleSheet(u"QLineEdit {\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(27, 29, 35);\n"
"	padding-left: 10px;\n"
"}\n"
"QLineEdit:hover {\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QLineEdit:focus {\n"
"	border: 2px solid rgb(91, 101, 124);\n"
"}")

        self.verticalLayout_27.addWidget(self.CampoReferenciaTrabajo)


        self.verticalLayout_12.addLayout(self.verticalLayout_27)


        self.verticalLayout_7.addWidget(self.frame_content_wid_1)

        self.frame_content_wid_1.raise_()
        self.frame_title_wid_1.raise_()

        self.gridLayout.addWidget(self.frame_div_content_1, 2, 0, 1, 1)

        self.frame_div_content_6 = QFrame(self.frame)
        self.frame_div_content_6.setObjectName(u"frame_div_content_6")
        self.frame_div_content_6.setMinimumSize(QSize(0, 110))
        self.frame_div_content_6.setMaximumSize(QSize(16777215, 110))
        self.frame_div_content_6.setStyleSheet(u"background-color: rgb(41, 45, 56);\n"
"border-radius: 5px;\n"
"")
        self.frame_div_content_6.setFrameShape(QFrame.NoFrame)
        self.frame_div_content_6.setFrameShadow(QFrame.Raised)
        self.verticalLayout_40 = QVBoxLayout(self.frame_div_content_6)
        self.verticalLayout_40.setSpacing(0)
        self.verticalLayout_40.setObjectName(u"verticalLayout_40")
        self.verticalLayout_40.setContentsMargins(0, 0, 0, 0)
        self.frame_title_wid_7 = QFrame(self.frame_div_content_6)
        self.frame_title_wid_7.setObjectName(u"frame_title_wid_7")
        self.frame_title_wid_7.setMaximumSize(QSize(16777215, 35))
        self.frame_title_wid_7.setStyleSheet(u"background-color: rgb(39, 44, 54);")
        self.frame_title_wid_7.setFrameShape(QFrame.StyledPanel)
        self.frame_title_wid_7.setFrameShadow(QFrame.Raised)
        self.verticalLayout_41 = QVBoxLayout(self.frame_title_wid_7)
        self.verticalLayout_41.setObjectName(u"verticalLayout_41")
        self.labelBoxBlenderInstalation_15 = QLabel(self.frame_title_wid_7)
        self.labelBoxBlenderInstalation_15.setObjectName(u"labelBoxBlenderInstalation_15")
        self.labelBoxBlenderInstalation_15.setFont(font1)
        self.labelBoxBlenderInstalation_15.setStyleSheet(u"")

        self.verticalLayout_41.addWidget(self.labelBoxBlenderInstalation_15)


        self.verticalLayout_40.addWidget(self.frame_title_wid_7)

        self.frame_content_wid_7 = QFrame(self.frame_div_content_6)
        self.frame_content_wid_7.setObjectName(u"frame_content_wid_7")
        self.frame_content_wid_7.setFrameShape(QFrame.NoFrame)
        self.frame_content_wid_7.setFrameShadow(QFrame.Raised)
        self.verticalLayout_42 = QVBoxLayout(self.frame_content_wid_7)
        self.verticalLayout_42.setObjectName(u"verticalLayout_42")
        self.verticalLayout_43 = QVBoxLayout()
        self.verticalLayout_43.setObjectName(u"verticalLayout_43")
        self.verticalLayout_43.setContentsMargins(-1, -1, -1, 0)
        self.CampoNumeroTicket = QLineEdit(self.frame_content_wid_7)
        self.CampoNumeroTicket.setObjectName(u"CampoNumeroTicket")
        self.CampoNumeroTicket.setMinimumSize(QSize(0, 30))
        self.CampoNumeroTicket.setStyleSheet(u"QLineEdit {\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(27, 29, 35);\n"
"	padding-left: 10px;\n"
"}\n"
"QLineEdit:hover {\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QLineEdit:focus {\n"
"	border: 2px solid rgb(91, 101, 124);\n"
"}")

        self.verticalLayout_43.addWidget(self.CampoNumeroTicket)


        self.verticalLayout_42.addLayout(self.verticalLayout_43)


        self.verticalLayout_40.addWidget(self.frame_content_wid_7)


        self.gridLayout.addWidget(self.frame_div_content_6, 1, 0, 1, 1)


        self.verticalLayout_6.addWidget(self.frame)

        self.frame_3 = QFrame(self.page_widgets)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(0, 150))
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_9 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.frame_div_content_8 = QFrame(self.frame_3)
        self.frame_div_content_8.setObjectName(u"frame_div_content_8")
        self.frame_div_content_8.setMinimumSize(QSize(0, 110))
        self.frame_div_content_8.setMaximumSize(QSize(16777215, 110))
        self.frame_div_content_8.setStyleSheet(u"background-color: rgb(41, 45, 56);\n"
"border-radius: 5px;\n"
"")
        self.frame_div_content_8.setFrameShape(QFrame.NoFrame)
        self.frame_div_content_8.setFrameShadow(QFrame.Raised)
        self.verticalLayout_48 = QVBoxLayout(self.frame_div_content_8)
        self.verticalLayout_48.setSpacing(0)
        self.verticalLayout_48.setObjectName(u"verticalLayout_48")
        self.verticalLayout_48.setContentsMargins(0, 0, 0, 0)
        self.frame_title_wid_9 = QFrame(self.frame_div_content_8)
        self.frame_title_wid_9.setObjectName(u"frame_title_wid_9")
        self.frame_title_wid_9.setMaximumSize(QSize(16777215, 35))
        self.frame_title_wid_9.setStyleSheet(u"background-color: rgb(39, 44, 54);")
        self.frame_title_wid_9.setFrameShape(QFrame.StyledPanel)
        self.frame_title_wid_9.setFrameShadow(QFrame.Raised)
        self.verticalLayout_50 = QVBoxLayout(self.frame_title_wid_9)
        self.verticalLayout_50.setObjectName(u"verticalLayout_50")
        self.labelBoxBlenderInstalation_19 = QLabel(self.frame_title_wid_9)
        self.labelBoxBlenderInstalation_19.setObjectName(u"labelBoxBlenderInstalation_19")
        self.labelBoxBlenderInstalation_19.setFont(font1)
        self.labelBoxBlenderInstalation_19.setStyleSheet(u"")

        self.verticalLayout_50.addWidget(self.labelBoxBlenderInstalation_19)


        self.verticalLayout_48.addWidget(self.frame_title_wid_9)

        self.frame_content_wid_9 = QFrame(self.frame_div_content_8)
        self.frame_content_wid_9.setObjectName(u"frame_content_wid_9")
        self.frame_content_wid_9.setFrameShape(QFrame.NoFrame)
        self.frame_content_wid_9.setFrameShadow(QFrame.Raised)
        self.verticalLayout_51 = QVBoxLayout(self.frame_content_wid_9)
        self.verticalLayout_51.setObjectName(u"verticalLayout_51")
        self.verticalLayout_57 = QVBoxLayout()
        self.verticalLayout_57.setObjectName(u"verticalLayout_57")
        self.verticalLayout_57.setContentsMargins(-1, -1, -1, 0)
        self.CampoColor = QLineEdit(self.frame_content_wid_9)
        self.CampoColor.setObjectName(u"CampoColor")
        self.CampoColor.setMinimumSize(QSize(0, 30))
        self.CampoColor.setStyleSheet(u"QLineEdit {\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(27, 29, 35);\n"
"	padding-left: 10px;\n"
"}\n"
"QLineEdit:hover {\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QLineEdit:focus {\n"
"	border: 2px solid rgb(91, 101, 124);\n"
"}")

        self.verticalLayout_57.addWidget(self.CampoColor)


        self.verticalLayout_51.addLayout(self.verticalLayout_57)


        self.verticalLayout_48.addWidget(self.frame_content_wid_9)


        self.horizontalLayout_9.addWidget(self.frame_div_content_8)

        self.frame_div_content_10 = QFrame(self.frame_3)
        self.frame_div_content_10.setObjectName(u"frame_div_content_10")
        self.frame_div_content_10.setMinimumSize(QSize(0, 110))
        self.frame_div_content_10.setMaximumSize(QSize(16777215, 110))
        self.frame_div_content_10.setStyleSheet(u"background-color: rgb(41, 45, 56);\n"
"border-radius: 5px;\n"
"")
        self.frame_div_content_10.setFrameShape(QFrame.NoFrame)
        self.frame_div_content_10.setFrameShadow(QFrame.Raised)
        self.verticalLayout_55 = QVBoxLayout(self.frame_div_content_10)
        self.verticalLayout_55.setSpacing(0)
        self.verticalLayout_55.setObjectName(u"verticalLayout_55")
        self.verticalLayout_55.setContentsMargins(0, 0, 0, 0)
        self.frame_title_wid_11 = QFrame(self.frame_div_content_10)
        self.frame_title_wid_11.setObjectName(u"frame_title_wid_11")
        self.frame_title_wid_11.setMaximumSize(QSize(16777215, 35))
        self.frame_title_wid_11.setStyleSheet(u"background-color: rgb(39, 44, 54);")
        self.frame_title_wid_11.setFrameShape(QFrame.StyledPanel)
        self.frame_title_wid_11.setFrameShadow(QFrame.Raised)
        self.verticalLayout_56 = QVBoxLayout(self.frame_title_wid_11)
        self.verticalLayout_56.setObjectName(u"verticalLayout_56")
        self.labelBoxBlenderInstalation_21 = QLabel(self.frame_title_wid_11)
        self.labelBoxBlenderInstalation_21.setObjectName(u"labelBoxBlenderInstalation_21")
        self.labelBoxBlenderInstalation_21.setFont(font1)
        self.labelBoxBlenderInstalation_21.setStyleSheet(u"")

        self.verticalLayout_56.addWidget(self.labelBoxBlenderInstalation_21)


        self.verticalLayout_55.addWidget(self.frame_title_wid_11)

        self.frame_content_wid_11 = QFrame(self.frame_div_content_10)
        self.frame_content_wid_11.setObjectName(u"frame_content_wid_11")
        self.frame_content_wid_11.setFrameShape(QFrame.NoFrame)
        self.frame_content_wid_11.setFrameShadow(QFrame.Raised)
        self.verticalLayout_59 = QVBoxLayout(self.frame_content_wid_11)
        self.verticalLayout_59.setObjectName(u"verticalLayout_59")
        self.verticalLayout_60 = QVBoxLayout()
        self.verticalLayout_60.setObjectName(u"verticalLayout_60")
        self.verticalLayout_60.setContentsMargins(-1, -1, -1, 0)
        self.CampoValor = QLineEdit(self.frame_content_wid_11)
        self.CampoValor.setObjectName(u"CampoValor")
        self.CampoValor.setMinimumSize(QSize(0, 30))
        self.CampoValor.setStyleSheet(u"QLineEdit {\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(27, 29, 35);\n"
"	padding-left: 10px;\n"
"}\n"
"QLineEdit:hover {\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QLineEdit:focus {\n"
"	border: 2px solid rgb(91, 101, 124);\n"
"}")

        self.verticalLayout_60.addWidget(self.CampoValor)


        self.verticalLayout_59.addLayout(self.verticalLayout_60)


        self.verticalLayout_55.addWidget(self.frame_content_wid_11)


        self.horizontalLayout_9.addWidget(self.frame_div_content_10)

        self.frame_div_content_5 = QFrame(self.frame_3)
        self.frame_div_content_5.setObjectName(u"frame_div_content_5")
        self.frame_div_content_5.setMinimumSize(QSize(0, 110))
        self.frame_div_content_5.setMaximumSize(QSize(16777215, 110))
        self.frame_div_content_5.setStyleSheet(u"background-color: rgb(41, 45, 56);\n"
"border-radius: 5px;\n"
"")
        self.frame_div_content_5.setFrameShape(QFrame.NoFrame)
        self.frame_div_content_5.setFrameShadow(QFrame.Raised)
        self.verticalLayout_36 = QVBoxLayout(self.frame_div_content_5)
        self.verticalLayout_36.setSpacing(0)
        self.verticalLayout_36.setObjectName(u"verticalLayout_36")
        self.verticalLayout_36.setContentsMargins(0, 0, 0, 0)
        self.frame_title_wid_6 = QFrame(self.frame_div_content_5)
        self.frame_title_wid_6.setObjectName(u"frame_title_wid_6")
        self.frame_title_wid_6.setMaximumSize(QSize(16777215, 35))
        self.frame_title_wid_6.setStyleSheet(u"background-color: rgb(39, 44, 54);")
        self.frame_title_wid_6.setFrameShape(QFrame.StyledPanel)
        self.frame_title_wid_6.setFrameShadow(QFrame.Raised)
        self.verticalLayout_37 = QVBoxLayout(self.frame_title_wid_6)
        self.verticalLayout_37.setObjectName(u"verticalLayout_37")
        self.labelBoxBlenderInstalation_14 = QLabel(self.frame_title_wid_6)
        self.labelBoxBlenderInstalation_14.setObjectName(u"labelBoxBlenderInstalation_14")
        self.labelBoxBlenderInstalation_14.setFont(font1)
        self.labelBoxBlenderInstalation_14.setStyleSheet(u"")

        self.verticalLayout_37.addWidget(self.labelBoxBlenderInstalation_14)


        self.verticalLayout_36.addWidget(self.frame_title_wid_6)

        self.frame_content_wid_6 = QFrame(self.frame_div_content_5)
        self.frame_content_wid_6.setObjectName(u"frame_content_wid_6")
        self.frame_content_wid_6.setFrameShape(QFrame.NoFrame)
        self.frame_content_wid_6.setFrameShadow(QFrame.Raised)
        self.verticalLayout_38 = QVBoxLayout(self.frame_content_wid_6)
        self.verticalLayout_38.setObjectName(u"verticalLayout_38")
        self.verticalLayout_39 = QVBoxLayout()
        self.verticalLayout_39.setObjectName(u"verticalLayout_39")
        self.verticalLayout_39.setContentsMargins(-1, -1, -1, 0)
        self.CampoTalla = QLineEdit(self.frame_content_wid_6)
        self.CampoTalla.setObjectName(u"CampoTalla")
        self.CampoTalla.setMinimumSize(QSize(0, 30))
        self.CampoTalla.setStyleSheet(u"QLineEdit {\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(27, 29, 35);\n"
"	padding-left: 10px;\n"
"}\n"
"QLineEdit:hover {\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QLineEdit:focus {\n"
"	border: 2px solid rgb(91, 101, 124);\n"
"}")

        self.verticalLayout_39.addWidget(self.CampoTalla)


        self.verticalLayout_38.addLayout(self.verticalLayout_39)


        self.verticalLayout_36.addWidget(self.frame_content_wid_6)


        self.horizontalLayout_9.addWidget(self.frame_div_content_5)

        self.frame_div_content_9 = QFrame(self.frame_3)
        self.frame_div_content_9.setObjectName(u"frame_div_content_9")
        self.frame_div_content_9.setMinimumSize(QSize(0, 110))
        self.frame_div_content_9.setMaximumSize(QSize(16777215, 110))
        self.frame_div_content_9.setStyleSheet(u"background-color: rgb(41, 45, 56);\n"
"border-radius: 5px;\n"
"")
        self.frame_div_content_9.setFrameShape(QFrame.NoFrame)
        self.frame_div_content_9.setFrameShadow(QFrame.Raised)
        self.verticalLayout_52 = QVBoxLayout(self.frame_div_content_9)
        self.verticalLayout_52.setSpacing(0)
        self.verticalLayout_52.setObjectName(u"verticalLayout_52")
        self.verticalLayout_52.setContentsMargins(0, 0, 0, 0)
        self.frame_title_wid_10 = QFrame(self.frame_div_content_9)
        self.frame_title_wid_10.setObjectName(u"frame_title_wid_10")
        self.frame_title_wid_10.setMaximumSize(QSize(16777215, 35))
        self.frame_title_wid_10.setStyleSheet(u"background-color: rgb(39, 44, 54);")
        self.frame_title_wid_10.setFrameShape(QFrame.StyledPanel)
        self.frame_title_wid_10.setFrameShadow(QFrame.Raised)
        self.verticalLayout_53 = QVBoxLayout(self.frame_title_wid_10)
        self.verticalLayout_53.setObjectName(u"verticalLayout_53")
        self.labelBoxBlenderInstalation_20 = QLabel(self.frame_title_wid_10)
        self.labelBoxBlenderInstalation_20.setObjectName(u"labelBoxBlenderInstalation_20")
        self.labelBoxBlenderInstalation_20.setFont(font1)
        self.labelBoxBlenderInstalation_20.setStyleSheet(u"")

        self.verticalLayout_53.addWidget(self.labelBoxBlenderInstalation_20)


        self.verticalLayout_52.addWidget(self.frame_title_wid_10)

        self.frame_content_wid_10 = QFrame(self.frame_div_content_9)
        self.frame_content_wid_10.setObjectName(u"frame_content_wid_10")
        self.frame_content_wid_10.setFrameShape(QFrame.NoFrame)
        self.frame_content_wid_10.setFrameShadow(QFrame.Raised)
        self.verticalLayout_54 = QVBoxLayout(self.frame_content_wid_10)
        self.verticalLayout_54.setObjectName(u"verticalLayout_54")
        self.verticalLayout_58 = QVBoxLayout()
        self.verticalLayout_58.setObjectName(u"verticalLayout_58")
        self.verticalLayout_58.setContentsMargins(-1, -1, -1, 0)
        self.CampoTotalProducido = QLineEdit(self.frame_content_wid_10)
        self.CampoTotalProducido.setObjectName(u"CampoTotalProducido")
        self.CampoTotalProducido.setMinimumSize(QSize(0, 30))
        self.CampoTotalProducido.setStyleSheet(u"QLineEdit {\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(27, 29, 35);\n"
"	padding-left: 10px;\n"
"}\n"
"QLineEdit:hover {\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QLineEdit:focus {\n"
"	border: 2px solid rgb(91, 101, 124);\n"
"}")

        self.verticalLayout_58.addWidget(self.CampoTotalProducido)


        self.verticalLayout_54.addLayout(self.verticalLayout_58)


        self.verticalLayout_52.addWidget(self.frame_content_wid_10)


        self.horizontalLayout_9.addWidget(self.frame_div_content_9)

        self.pushButtonGuardar = QPushButton(self.frame_3)
        self.pushButtonGuardar.setObjectName(u"pushButtonGuardar")
        self.pushButtonGuardar.setMinimumSize(QSize(150, 30))
        self.pushButtonGuardar.setFont(font5)
        self.pushButtonGuardar.setStyleSheet(u"QPushButton {\n"
"	border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(57, 65, 80);\n"
"	border: 2px solid rgb(61, 70, 86);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgb(35, 40, 49);\n"
"	border: 2px solid rgb(43, 50, 61);\n"
"}")
        self.pushButtonGuardar.setIcon(icon)

        self.horizontalLayout_9.addWidget(self.pushButtonGuardar)

        self.PreviwImage = QGraphicsView(self.frame_3)
        self.PreviwImage.setObjectName(u"PreviwImage")

        self.horizontalLayout_9.addWidget(self.PreviwImage)


        self.verticalLayout_6.addWidget(self.frame_3)

        self.stackedWidget.addWidget(self.page_widgets)

        self.verticalLayout_9.addWidget(self.stackedWidget)


        self.verticalLayout_4.addWidget(self.frame_content)

        self.frame_grip = QFrame(self.frame_content_right)
        self.frame_grip.setObjectName(u"frame_grip")
        self.frame_grip.setMinimumSize(QSize(0, 25))
        self.frame_grip.setMaximumSize(QSize(16777215, 25))
        self.frame_grip.setStyleSheet(u"background-color: rgb(33, 37, 43);")
        self.frame_grip.setFrameShape(QFrame.NoFrame)
        self.frame_grip.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.frame_grip)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 2, 0)
        self.frame_label_bottom = QFrame(self.frame_grip)
        self.frame_label_bottom.setObjectName(u"frame_label_bottom")
        self.frame_label_bottom.setFrameShape(QFrame.NoFrame)
        self.frame_label_bottom.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.frame_label_bottom)
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(10, 0, 10, 0)
        self.label_credits = QLabel(self.frame_label_bottom)
        self.label_credits.setObjectName(u"label_credits")
        self.label_credits.setFont(font2)
        self.label_credits.setStyleSheet(u"color: rgb(98, 103, 111);")

        self.horizontalLayout_7.addWidget(self.label_credits)

        self.label_version = QLabel(self.frame_label_bottom)
        self.label_version.setObjectName(u"label_version")
        self.label_version.setMaximumSize(QSize(100, 16777215))
        self.label_version.setFont(font2)
        self.label_version.setStyleSheet(u"color: rgb(98, 103, 111);")
        self.label_version.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_7.addWidget(self.label_version)


        self.horizontalLayout_6.addWidget(self.frame_label_bottom)

        self.frame_size_grip = QFrame(self.frame_grip)
        self.frame_size_grip.setObjectName(u"frame_size_grip")
        self.frame_size_grip.setMaximumSize(QSize(20, 20))
        self.frame_size_grip.setStyleSheet(u"QSizeGrip {\n"
"	background-image: url(:/16x16/icons/16x16/cil-size-grip.png);\n"
"	background-position: center;\n"
"	background-repeat: no-reperat;\n"
"}")
        self.frame_size_grip.setFrameShape(QFrame.NoFrame)
        self.frame_size_grip.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_6.addWidget(self.frame_size_grip)


        self.verticalLayout_4.addWidget(self.frame_grip)


        self.horizontalLayout_2.addWidget(self.frame_content_right)


        self.verticalLayout.addWidget(self.frame_center)


        self.horizontalLayout.addWidget(self.frame_main)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.btn_toggle_menu.setText("")
        self.label_title_bar_top.setText(QCoreApplication.translate("MainWindow", u"Creacion de Tareas", None))
        self.label_top_info_1.setText(QCoreApplication.translate("MainWindow", u"Gestion de Tareas", None))
        self.label_top_info_2.setText(QCoreApplication.translate("MainWindow", u"| HOME", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Lectura de codigos de Barras", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; font-weight:600;\">Seleccionar Empleado</span></p></body></html>", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; font-weight:600;\">Ingresar Codigo</span></p></body></html>", None))
        self.btnRegisterVale.setText(QCoreApplication.translate("MainWindow", u"Guardar a Excel", None))
        self.btnActualizarDB.setText(QCoreApplication.translate("MainWindow", u"Generar Excel", None))
        self.EliminarTODO.setText(QCoreApplication.translate("MainWindow", u"ELIMINAR TODO", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; font-weight:600;\">A\u00f1adir Empleado</span></p></body></html>", None))
        self.labelBoxNombreEmpleado.setText(QCoreApplication.translate("MainWindow", u"Nombre Empleado", None))
#if QT_CONFIG(whatsthis)
        self.Nombre_Empleado.setWhatsThis(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>_</p></body></html>", None))
#endif // QT_CONFIG(whatsthis)
        self.Nombre_Empleado.setText("")
        self.Nombre_Empleado.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Your Password", None))
        self.labelBoxBlenderInstalation_17.setText(QCoreApplication.translate("MainWindow", u"Cedula", None))
        self.Cedula_Empleado.setText("")
        self.Cedula_Empleado.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Your Password", None))
        self.la.setText(QCoreApplication.translate("MainWindow", u"Numero de Celular", None))
        self.Celular_Empleado.setText("")
        self.Celular_Empleado.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Your Password", None))
        self.labelBoxCorreo.setText(QCoreApplication.translate("MainWindow", u"Correo Electronico", None))
        self.Correo_Empleado.setText("")
        self.Correo_Empleado.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Your Password", None))
        self.btnAgregarEmpleado.setText(QCoreApplication.translate("MainWindow", u"Guardar Empleado", None))
        self.labelBoxBlenderInstalation_13.setText(QCoreApplication.translate("MainWindow", u"Tipo de trabajo", None))
        self.CampoTipoTrabajo.setText("")
        self.CampoTipoTrabajo.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Your Password", None))
        self.labelBoxBlenderInstalation.setText(QCoreApplication.translate("MainWindow", u"Referencia de trabajo", None))
        self.CampoReferenciaTrabajo.setText("")
        self.CampoReferenciaTrabajo.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Your Password", None))
        self.labelBoxBlenderInstalation_15.setText(QCoreApplication.translate("MainWindow", u"Numero de ticket", None))
        self.CampoNumeroTicket.setText("")
        self.CampoNumeroTicket.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Your Password", None))
        self.labelBoxBlenderInstalation_19.setText(QCoreApplication.translate("MainWindow", u"Color", None))
        self.CampoColor.setText("")
        self.CampoColor.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Your Password", None))
        self.labelBoxBlenderInstalation_21.setText(QCoreApplication.translate("MainWindow", u"Valor", None))
        self.CampoValor.setText("")
        self.CampoValor.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Your Password", None))
        self.labelBoxBlenderInstalation_14.setText(QCoreApplication.translate("MainWindow", u"Talla", None))
        self.CampoTalla.setText("")
        self.CampoTalla.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Your Password", None))
        self.labelBoxBlenderInstalation_20.setText(QCoreApplication.translate("MainWindow", u"Total Producido", None))
        self.CampoTotalProducido.setText("")
        self.CampoTotalProducido.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Your Password", None))
        self.pushButtonGuardar.setText(QCoreApplication.translate("MainWindow", u"Guardar tarea", None))
        self.label_credits.setText("")
        self.label_version.setText(QCoreApplication.translate("MainWindow", u"v1.0.0", None))
    # retranslateUi

