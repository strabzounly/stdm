# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_document_downloader_win.ui'
#
# Created: Thu Jun 18 14:34:47 2020
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_DocumentDownloader(object):
    def setupUi(self, DocumentDownloader):
        DocumentDownloader.setObjectName(_fromUtf8("DocumentDownloader"))
        DocumentDownloader.resize(690, 638)
        self.centralwidget = QtGui.QWidget(DocumentDownloader)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_4.setSpacing(6)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.twDocument = QtGui.QTabWidget(self.centralwidget)
        self.twDocument.setObjectName(_fromUtf8("twDocument"))
        self.tbDownload = QtGui.QWidget()
        self.tbDownload.setObjectName(_fromUtf8("tbDownload"))
        self.verticalLayout = QtGui.QVBoxLayout(self.tbDownload)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox_2 = QtGui.QGroupBox(self.tbDownload)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.rbKoboMedia = QtGui.QRadioButton(self.groupBox_2)
        self.rbKoboMedia.setAutoExclusive(False)
        self.rbKoboMedia.setObjectName(_fromUtf8("rbKoboMedia"))
        self.horizontalLayout.addWidget(self.rbKoboMedia)
        self.rbSupportDoc = QtGui.QRadioButton(self.groupBox_2)
        self.rbSupportDoc.setAutoExclusive(False)
        self.rbSupportDoc.setObjectName(_fromUtf8("rbSupportDoc"))
        self.horizontalLayout.addWidget(self.rbSupportDoc)
        self.verticalLayout.addWidget(self.groupBox_2)
        self.groupBox = QtGui.QGroupBox(self.tbDownload)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.groupBox)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_2.addWidget(self.label)
        self.txtDataSource = QtGui.QLineEdit(self.groupBox)
        self.txtDataSource.setMaxLength(200)
        self.txtDataSource.setObjectName(_fromUtf8("txtDataSource"))
        self.horizontalLayout_2.addWidget(self.txtDataSource)
        self.btnBrowseSource = QtGui.QPushButton(self.groupBox)
        self.btnBrowseSource.setObjectName(_fromUtf8("btnBrowseSource"))
        self.horizontalLayout_2.addWidget(self.btnBrowseSource)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_7 = QtGui.QGroupBox(self.tbDownload)
        self.groupBox_7.setObjectName(_fromUtf8("groupBox_7"))
        self.gridLayout_4 = QtGui.QGridLayout(self.groupBox_7)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.label_4 = QtGui.QLabel(self.groupBox_7)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout_4.addWidget(self.label_4, 0, 0, 1, 1)
        self.label_5 = QtGui.QLabel(self.groupBox_7)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout_4.addWidget(self.label_5, 1, 0, 1, 1)
        self.edtKoboUsername = QtGui.QLineEdit(self.groupBox_7)
        self.edtKoboUsername.setReadOnly(False)
        self.edtKoboUsername.setObjectName(_fromUtf8("edtKoboUsername"))
        self.gridLayout_4.addWidget(self.edtKoboUsername, 1, 1, 1, 1)
        self.edtKoboPassword = QtGui.QLineEdit(self.groupBox_7)
        self.edtKoboPassword.setEchoMode(QtGui.QLineEdit.Password)
        self.edtKoboPassword.setObjectName(_fromUtf8("edtKoboPassword"))
        self.gridLayout_4.addWidget(self.edtKoboPassword, 2, 1, 1, 1)
        self.edtMediaUrl = QtGui.QLineEdit(self.groupBox_7)
        self.edtMediaUrl.setReadOnly(False)
        self.edtMediaUrl.setObjectName(_fromUtf8("edtMediaUrl"))
        self.gridLayout_4.addWidget(self.edtMediaUrl, 0, 1, 1, 1)
        self.label_6 = QtGui.QLabel(self.groupBox_7)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout_4.addWidget(self.label_6, 2, 0, 1, 1)
        self.verticalLayout.addWidget(self.groupBox_7)
        self.groupBox_8 = QtGui.QGroupBox(self.tbDownload)
        self.groupBox_8.setObjectName(_fromUtf8("groupBox_8"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupBox_8)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label_7 = QtGui.QLabel(self.groupBox_8)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout_2.addWidget(self.label_7, 0, 0, 1, 1)
        self.edtFamilyFolder = QtGui.QLineEdit(self.groupBox_8)
        self.edtFamilyFolder.setObjectName(_fromUtf8("edtFamilyFolder"))
        self.gridLayout_2.addWidget(self.edtFamilyFolder, 0, 1, 1, 1)
        self.cbFamilyPhoto = QtGui.QCheckBox(self.groupBox_8)
        self.cbFamilyPhoto.setCheckable(True)
        self.cbFamilyPhoto.setObjectName(_fromUtf8("cbFamilyPhoto"))
        self.gridLayout_2.addWidget(self.cbFamilyPhoto, 0, 2, 1, 1)
        self.tbFamilyFolder = QtGui.QToolButton(self.groupBox_8)
        self.tbFamilyFolder.setObjectName(_fromUtf8("tbFamilyFolder"))
        self.gridLayout_2.addWidget(self.tbFamilyFolder, 0, 3, 1, 1)
        self.btnFamilyBrowse = QtGui.QPushButton(self.groupBox_8)
        self.btnFamilyBrowse.setObjectName(_fromUtf8("btnFamilyBrowse"))
        self.gridLayout_2.addWidget(self.btnFamilyBrowse, 0, 4, 1, 1)
        self.label_8 = QtGui.QLabel(self.groupBox_8)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout_2.addWidget(self.label_8, 1, 0, 1, 1)
        self.edtSignFolder = QtGui.QLineEdit(self.groupBox_8)
        self.edtSignFolder.setObjectName(_fromUtf8("edtSignFolder"))
        self.gridLayout_2.addWidget(self.edtSignFolder, 1, 1, 1, 1)
        self.cbSign = QtGui.QCheckBox(self.groupBox_8)
        self.cbSign.setObjectName(_fromUtf8("cbSign"))
        self.gridLayout_2.addWidget(self.cbSign, 1, 2, 1, 1)
        self.tbSignFolder = QtGui.QToolButton(self.groupBox_8)
        self.tbSignFolder.setObjectName(_fromUtf8("tbSignFolder"))
        self.gridLayout_2.addWidget(self.tbSignFolder, 1, 3, 1, 1)
        self.btnSignFolder = QtGui.QPushButton(self.groupBox_8)
        self.btnSignFolder.setObjectName(_fromUtf8("btnSignFolder"))
        self.gridLayout_2.addWidget(self.btnSignFolder, 1, 4, 1, 1)
        self.label_9 = QtGui.QLabel(self.groupBox_8)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout_2.addWidget(self.label_9, 2, 0, 1, 1)
        self.edtHouseFolder = QtGui.QLineEdit(self.groupBox_8)
        self.edtHouseFolder.setObjectName(_fromUtf8("edtHouseFolder"))
        self.gridLayout_2.addWidget(self.edtHouseFolder, 2, 1, 1, 1)
        self.cbHousePhoto = QtGui.QCheckBox(self.groupBox_8)
        self.cbHousePhoto.setObjectName(_fromUtf8("cbHousePhoto"))
        self.gridLayout_2.addWidget(self.cbHousePhoto, 2, 2, 1, 1)
        self.tbHouseFolder = QtGui.QToolButton(self.groupBox_8)
        self.tbHouseFolder.setObjectName(_fromUtf8("tbHouseFolder"))
        self.gridLayout_2.addWidget(self.tbHouseFolder, 2, 3, 1, 1)
        self.btnHouseFolder = QtGui.QPushButton(self.groupBox_8)
        self.btnHouseFolder.setObjectName(_fromUtf8("btnHouseFolder"))
        self.gridLayout_2.addWidget(self.btnHouseFolder, 2, 4, 1, 1)
        self.label_11 = QtGui.QLabel(self.groupBox_8)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.gridLayout_2.addWidget(self.label_11, 3, 0, 1, 1)
        self.edtHousePic = QtGui.QLineEdit(self.groupBox_8)
        self.edtHousePic.setObjectName(_fromUtf8("edtHousePic"))
        self.gridLayout_2.addWidget(self.edtHousePic, 3, 1, 1, 1)
        self.cbHousePic = QtGui.QCheckBox(self.groupBox_8)
        self.cbHousePic.setObjectName(_fromUtf8("cbHousePic"))
        self.gridLayout_2.addWidget(self.cbHousePic, 3, 2, 1, 1)
        self.tbHousePic = QtGui.QToolButton(self.groupBox_8)
        self.tbHousePic.setObjectName(_fromUtf8("tbHousePic"))
        self.gridLayout_2.addWidget(self.tbHousePic, 3, 3, 1, 1)
        self.btnHousePic = QtGui.QPushButton(self.groupBox_8)
        self.btnHousePic.setObjectName(_fromUtf8("btnHousePic"))
        self.gridLayout_2.addWidget(self.btnHousePic, 3, 4, 1, 1)
        self.label_12 = QtGui.QLabel(self.groupBox_8)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.gridLayout_2.addWidget(self.label_12, 4, 0, 1, 1)
        self.edtIdPic = QtGui.QLineEdit(self.groupBox_8)
        self.edtIdPic.setObjectName(_fromUtf8("edtIdPic"))
        self.gridLayout_2.addWidget(self.edtIdPic, 4, 1, 1, 1)
        self.cbIdPic = QtGui.QCheckBox(self.groupBox_8)
        self.cbIdPic.setObjectName(_fromUtf8("cbIdPic"))
        self.gridLayout_2.addWidget(self.cbIdPic, 4, 2, 1, 1)
        self.tbIdPic = QtGui.QToolButton(self.groupBox_8)
        self.tbIdPic.setObjectName(_fromUtf8("tbIdPic"))
        self.gridLayout_2.addWidget(self.tbIdPic, 4, 3, 1, 1)
        self.btnIdPic = QtGui.QPushButton(self.groupBox_8)
        self.btnIdPic.setObjectName(_fromUtf8("btnIdPic"))
        self.gridLayout_2.addWidget(self.btnIdPic, 4, 4, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_2)
        self.verticalLayout.addWidget(self.groupBox_8)
        self.twDocument.addTab(self.tbDownload, _fromUtf8(""))
        self.tbUpload = QtGui.QWidget()
        self.tbUpload.setObjectName(_fromUtf8("tbUpload"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.tbUpload)
        self.verticalLayout_3.setSpacing(15)
        self.verticalLayout_3.setContentsMargins(-1, -1, -1, 9)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.groupBox_5 = QtGui.QGroupBox(self.tbUpload)
        self.groupBox_5.setObjectName(_fromUtf8("groupBox_5"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout(self.groupBox_5)
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.rbScannedDoc = QtGui.QRadioButton(self.groupBox_5)
        self.rbScannedDoc.setObjectName(_fromUtf8("rbScannedDoc"))
        self.horizontalLayout_5.addWidget(self.rbScannedDoc)
        self.verticalLayout_3.addWidget(self.groupBox_5)
        self.groupBox_4 = QtGui.QGroupBox(self.tbUpload)
        self.groupBox_4.setObjectName(_fromUtf8("groupBox_4"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.groupBox_4)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tbScannedDoc = QtGui.QToolButton(self.groupBox_4)
        self.tbScannedDoc.setObjectName(_fromUtf8("tbScannedDoc"))
        self.gridLayout.addWidget(self.tbScannedDoc, 0, 3, 1, 1)
        self.edtScannedDoc = QtGui.QLineEdit(self.groupBox_4)
        self.edtScannedDoc.setObjectName(_fromUtf8("edtScannedDoc"))
        self.gridLayout.addWidget(self.edtScannedDoc, 0, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.groupBox_4)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.cbScannedDoc = QtGui.QCheckBox(self.groupBox_4)
        self.cbScannedDoc.setObjectName(_fromUtf8("cbScannedDoc"))
        self.gridLayout.addWidget(self.cbScannedDoc, 0, 2, 1, 1)
        self.btnScannedDoc = QtGui.QPushButton(self.groupBox_4)
        self.btnScannedDoc.setObjectName(_fromUtf8("btnScannedDoc"))
        self.gridLayout.addWidget(self.btnScannedDoc, 0, 4, 1, 1)
        self.label_3 = QtGui.QLabel(self.groupBox_4)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.label_10 = QtGui.QLabel(self.groupBox_4)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.gridLayout.addWidget(self.label_10, 2, 0, 1, 1)
        self.label_13 = QtGui.QLabel(self.groupBox_4)
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.gridLayout.addWidget(self.label_13, 3, 0, 1, 1)
        self.edtScannedHseMap = QtGui.QLineEdit(self.groupBox_4)
        self.edtScannedHseMap.setObjectName(_fromUtf8("edtScannedHseMap"))
        self.gridLayout.addWidget(self.edtScannedHseMap, 1, 1, 1, 1)
        self.edtScannedHsePic = QtGui.QLineEdit(self.groupBox_4)
        self.edtScannedHsePic.setObjectName(_fromUtf8("edtScannedHsePic"))
        self.gridLayout.addWidget(self.edtScannedHsePic, 2, 1, 1, 1)
        self.edtScannedIdDoc = QtGui.QLineEdit(self.groupBox_4)
        self.edtScannedIdDoc.setObjectName(_fromUtf8("edtScannedIdDoc"))
        self.gridLayout.addWidget(self.edtScannedIdDoc, 3, 1, 1, 1)
        self.cbScannedHseMap = QtGui.QCheckBox(self.groupBox_4)
        self.cbScannedHseMap.setObjectName(_fromUtf8("cbScannedHseMap"))
        self.gridLayout.addWidget(self.cbScannedHseMap, 1, 2, 1, 1)
        self.cbScannedHsePic = QtGui.QCheckBox(self.groupBox_4)
        self.cbScannedHsePic.setObjectName(_fromUtf8("cbScannedHsePic"))
        self.gridLayout.addWidget(self.cbScannedHsePic, 2, 2, 1, 1)
        self.cbScannedIdDoc = QtGui.QCheckBox(self.groupBox_4)
        self.cbScannedIdDoc.setObjectName(_fromUtf8("cbScannedIdDoc"))
        self.gridLayout.addWidget(self.cbScannedIdDoc, 3, 2, 1, 1)
        self.tbScannedHseMap = QtGui.QToolButton(self.groupBox_4)
        self.tbScannedHseMap.setObjectName(_fromUtf8("tbScannedHseMap"))
        self.gridLayout.addWidget(self.tbScannedHseMap, 1, 3, 1, 1)
        self.tbScannedHsePic = QtGui.QToolButton(self.groupBox_4)
        self.tbScannedHsePic.setObjectName(_fromUtf8("tbScannedHsePic"))
        self.gridLayout.addWidget(self.tbScannedHsePic, 2, 3, 1, 1)
        self.tbScannedIdDoc = QtGui.QToolButton(self.groupBox_4)
        self.tbScannedIdDoc.setObjectName(_fromUtf8("tbScannedIdDoc"))
        self.gridLayout.addWidget(self.tbScannedIdDoc, 3, 3, 1, 1)
        self.btnScannedHseMap = QtGui.QPushButton(self.groupBox_4)
        self.btnScannedHseMap.setObjectName(_fromUtf8("btnScannedHseMap"))
        self.gridLayout.addWidget(self.btnScannedHseMap, 1, 4, 1, 1)
        self.btnScannedHsePic = QtGui.QPushButton(self.groupBox_4)
        self.btnScannedHsePic.setObjectName(_fromUtf8("btnScannedHsePic"))
        self.gridLayout.addWidget(self.btnScannedHsePic, 2, 4, 1, 1)
        self.btnScannedIdDoc = QtGui.QPushButton(self.groupBox_4)
        self.btnScannedIdDoc.setObjectName(_fromUtf8("btnScannedIdDoc"))
        self.gridLayout.addWidget(self.btnScannedIdDoc, 3, 4, 1, 1)
        self.verticalLayout_5.addLayout(self.gridLayout)
        self.verticalLayout_3.addWidget(self.groupBox_4)
        spacerItem = QtGui.QSpacerItem(20, 227, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.twDocument.addTab(self.tbUpload, _fromUtf8(""))
        self.verticalLayout_4.addWidget(self.twDocument)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        spacerItem1 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.btnDownload = QtGui.QPushButton(self.centralwidget)
        self.btnDownload.setMinimumSize(QtCore.QSize(200, 0))
        self.btnDownload.setObjectName(_fromUtf8("btnDownload"))
        self.horizontalLayout_4.addWidget(self.btnDownload)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.verticalLayout_4.addLayout(self.horizontalLayout_4)
        self.gbProgress = QtGui.QGroupBox(self.centralwidget)
        self.gbProgress.setObjectName(_fromUtf8("gbProgress"))
        self.gridLayout_7 = QtGui.QGridLayout(self.gbProgress)
        self.gridLayout_7.setObjectName(_fromUtf8("gridLayout_7"))
        self.edtProgress = QtGui.QTextEdit(self.gbProgress)
        self.edtProgress.setReadOnly(True)
        self.edtProgress.setObjectName(_fromUtf8("edtProgress"))
        self.gridLayout_7.addWidget(self.edtProgress, 0, 0, 1, 1)
        self.verticalLayout_4.addWidget(self.gbProgress)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.btnClose = QtGui.QPushButton(self.centralwidget)
        self.btnClose.setObjectName(_fromUtf8("btnClose"))
        self.horizontalLayout_3.addWidget(self.btnClose)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        DocumentDownloader.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(DocumentDownloader)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        DocumentDownloader.setStatusBar(self.statusbar)

        self.retranslateUi(DocumentDownloader)
        self.twDocument.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(DocumentDownloader)

    def retranslateUi(self, DocumentDownloader):
        DocumentDownloader.setWindowTitle(_translate("DocumentDownloader", "Download and Upload Documents", None))
        self.groupBox_2.setTitle(_translate("DocumentDownloader", "Document Type:", None))
        self.rbKoboMedia.setText(_translate("DocumentDownloader", "Claims File Documents", None))
        self.rbSupportDoc.setText(_translate("DocumentDownloader", "Supporting Documents", None))
        self.groupBox.setTitle(_translate("DocumentDownloader", "Source:", None))
        self.label.setText(_translate("DocumentDownloader", "Dataset", None))
        self.btnBrowseSource.setText(_translate("DocumentDownloader", "Browse", None))
        self.groupBox_7.setTitle(_translate("DocumentDownloader", "Kobo Settings", None))
        self.label_4.setText(_translate("DocumentDownloader", "Media URL:", None))
        self.label_5.setText(_translate("DocumentDownloader", "Kobo Username:", None))
        self.label_6.setText(_translate("DocumentDownloader", "Kobo Password:", None))
        self.groupBox_8.setTitle(_translate("DocumentDownloader", "Local Document Folders:", None))
        self.label_7.setText(_translate("DocumentDownloader", "Family Photos:", None))
        self.cbFamilyPhoto.setText(_translate("DocumentDownloader", "Download", None))
        self.tbFamilyFolder.setText(_translate("DocumentDownloader", "...", None))
        self.btnFamilyBrowse.setText(_translate("DocumentDownloader", "Browse ...", None))
        self.label_8.setText(_translate("DocumentDownloader", "Signatures:", None))
        self.cbSign.setText(_translate("DocumentDownloader", "Download", None))
        self.tbSignFolder.setText(_translate("DocumentDownloader", "...", None))
        self.btnSignFolder.setText(_translate("DocumentDownloader", "Browse ...", None))
        self.label_9.setText(_translate("DocumentDownloader", "House Map:", None))
        self.cbHousePhoto.setText(_translate("DocumentDownloader", "Download", None))
        self.tbHouseFolder.setText(_translate("DocumentDownloader", "...", None))
        self.btnHouseFolder.setText(_translate("DocumentDownloader", "Browse ...", None))
        self.label_11.setText(_translate("DocumentDownloader", "House Picture:", None))
        self.cbHousePic.setText(_translate("DocumentDownloader", "Download", None))
        self.tbHousePic.setText(_translate("DocumentDownloader", "...", None))
        self.btnHousePic.setText(_translate("DocumentDownloader", "Browse ...", None))
        self.label_12.setText(_translate("DocumentDownloader", "ID Picture:", None))
        self.cbIdPic.setText(_translate("DocumentDownloader", "Download", None))
        self.tbIdPic.setText(_translate("DocumentDownloader", "...", None))
        self.btnIdPic.setText(_translate("DocumentDownloader", "Browse ...", None))
        self.twDocument.setTabText(self.twDocument.indexOf(self.tbDownload), _translate("DocumentDownloader", "Download", None))
        self.groupBox_5.setTitle(_translate("DocumentDownloader", "Document Type:", None))
        self.rbScannedDoc.setText(_translate("DocumentDownloader", "Scanned Documents", None))
        self.groupBox_4.setTitle(_translate("DocumentDownloader", "Local Documents Folder:", None))
        self.tbScannedDoc.setText(_translate("DocumentDownloader", "...", None))
        self.label_2.setText(_translate("DocumentDownloader", "Certificate:", None))
        self.cbScannedDoc.setText(_translate("DocumentDownloader", "Upload", None))
        self.btnScannedDoc.setText(_translate("DocumentDownloader", "Browse ...", None))
        self.label_3.setText(_translate("DocumentDownloader", "House Map:", None))
        self.label_10.setText(_translate("DocumentDownloader", "House Picture:", None))
        self.label_13.setText(_translate("DocumentDownloader", "ID Document:", None))
        self.cbScannedHseMap.setText(_translate("DocumentDownloader", "Upload", None))
        self.cbScannedHsePic.setText(_translate("DocumentDownloader", "Upload", None))
        self.cbScannedIdDoc.setText(_translate("DocumentDownloader", "Upload", None))
        self.tbScannedHseMap.setText(_translate("DocumentDownloader", "...", None))
        self.tbScannedHsePic.setText(_translate("DocumentDownloader", "...", None))
        self.tbScannedIdDoc.setText(_translate("DocumentDownloader", "...", None))
        self.btnScannedHseMap.setText(_translate("DocumentDownloader", "Browse ...", None))
        self.btnScannedHsePic.setText(_translate("DocumentDownloader", "Browse ...", None))
        self.btnScannedIdDoc.setText(_translate("DocumentDownloader", "Browse ...", None))
        self.twDocument.setTabText(self.twDocument.indexOf(self.tbUpload), _translate("DocumentDownloader", "Upload", None))
        self.btnDownload.setText(_translate("DocumentDownloader", "Download", None))
        self.gbProgress.setTitle(_translate("DocumentDownloader", "Download progress:", None))
        self.btnClose.setText(_translate("DocumentDownloader", "Close", None))

