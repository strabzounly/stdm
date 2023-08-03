import os
from os import path
from os.path import (
        isfile, 
        join
    )
import fnmatch
import shutil
import sys
import copy
from collections import OrderedDict
from datetime import datetime
import hashlib
import requests

import time

from PyQt4.QtGui import (
        QApplication,
        QDialog,
        QMainWindow,
        QFileDialog,
        QMessageBox,
        QLineEdit,
        QColor
  )

from PyQt4 import QtNetwork

from PyQt4.QtCore import (
    Qt,
    QObject,
    pyqtSignal,
    QFile,
    QFileInfo,
    SIGNAL,
    QSignalMapper,
    QThread,
    QUrl,
    QFile,
    QIODevice,
    QByteArray
)

from stdm.data.importexport import (
    vectorFileDir,
    setVectorFileDir
)

from stdm.settings import (
        current_profile,
        get_media_url,
        get_kobo_user,
        get_kobo_pass,
        get_family_photo,
        get_sign_photo,
        get_house_photo,
        get_house_pic,
        get_id_pic,
        get_scanned_doc,
        get_scanned_hse_map,
        get_scanned_hse_pic,
        get_scanned_id_doc,
        get_scanned_family_photo,
        get_scanned_signature,
        save_media_url,
        save_kobo_user,
        save_kobo_pass,
        save_family_photo,
        save_sign_photo,
        save_house_photo,
        save_house_pic,
        save_id_pic,
        save_scanned_doc,
        save_scanned_hse_map,
        save_scanned_hse_pic,
        save_scanned_id_doc,
        save_scanned_family_photo,
        save_scanned_signature
        )

from stdm.settings.registryconfig import (
        RegistryConfig,
        NETWORK_DOC_RESOURCE
)

from stdm.utils.util import mapfile_section

from stdm.data.pg_utils import (
    get_last_id,
    get_value_by_column,
    pg_create_supporting_document,
    pg_create_parent_supporting_document,
    pg_fix_auto_sequence
)

from stdm.data.importexport.reader import OGRReader

from ui_document_downloader_win import Ui_DocumentDownloader
from stdm.data.importexport.document_downloader import KB_DocumentDownloader
from urllib.parse import urlparse

DOWNLOAD_DOCS = 0
UPLOAD_DOCS = 1

class DownloadRequest(QtNetwork.QNetworkRequest):
    def __init__(self, src_url, dest_url, parent):
        self._src_url = src_url
        self._dest_url = dest_url
        self.parent = parent
        QtNetwork.QNetworkRequest.__init__(self, QUrl(src_url))

    @property
    def src_url(self):
        return self._src_url

    @property
    def dest_url(self):
        return self._dest_url

    def handle_download_response(self, reply):
        err = reply.error()
        if err == QtNetwork.QNetworkReply.NoError:
            msg = 'Downloaded File: {}'.format(self.dest_url)
            self.parent.download_progress.emit(KoboDownloader.INFORMATION, msg)
            bytes = reply.readAll()
            file = QFile(self.dest_url)
            file.open(QIODevice.WriteOnly)
            file.write(bytes)
        else:
            msg = "ERROR downloading file : {}".format(self.src_url)
            self.parent.download_progress.emit(KoboDownloader.ERROR, msg)


class DocumentDownloader(QMainWindow, Ui_DocumentDownloader):
    def __init__(self, plugin):
        QMainWindow.__init__(self, plugin.iface.mainWindow())

        self.setWindowFlags( 
                Qt.Window|
                Qt.WindowTitleHint|
                Qt.WindowMinimizeButtonHint|
                Qt.WindowSystemMenuHint|
                Qt.WindowCloseButtonHint|
                Qt.CustomizeWindowHint)

        self.setupUi(self)

        self.btnBrowseSource.clicked.connect(self.set_source_file)
        self.btnUploadFile.clicked.connect(self.set_upload_file)

        self.rbKoboMedia.clicked.connect(self.kobo_media_clicked)
        self.rbSupportDoc.clicked.connect(self.support_doc_clicked)
        self.rbScannedDoc.clicked.connect(self.scanned_doc_clicked)
        self.rbCSV.clicked.connect(self.csv_clicked)

        self.tbFamilyFolder.clicked.connect(self.family_folder)
        self.tbSignFolder.clicked.connect(self.sign_folder)
        self.tbHouseFolder.clicked.connect(self.house_folder)
        self.tbHousePic.clicked.connect(self.house_pic_folder)
        self.tbIdPic.clicked.connect(self.id_pic_folder)
        self.tbScannedDoc.clicked.connect(self.scanned_doc_folder)
        self.tbScannedHseMap.clicked.connect(self.scanned_hse_map_folder)
        self.tbScannedHsePic.clicked.connect(self.scanned_hse_pic_folder)
        self.tbScannedIdDoc.clicked.connect(self.scanned_id_doc_folder)
        self.tbScannedFamilyPhoto.clicked.connect(self.scanned_family_photo)
        self.tbScannedSignature.clicked.connect(self.scanned_signature)

        self.btnDownload.clicked.connect(self.download_media)
        self.btnDownload.setStyleSheet("QPushButton{ background-color: rgb(85,255,127) }")

        self.btnFamilyBrowse.clicked.connect(self.show_family_folder)
        self.btnSignFolder.clicked.connect(self.show_sign_folder)
        self.btnHouseFolder.clicked.connect(self.show_house_folder)
        self.btnHousePic.clicked.connect(self.show_house_pic_folder)
        self.btnIdPic.clicked.connect(self.show_id_pic_folder)
        self.btnScannedDoc.clicked.connect(self.show_scanned_doc_folder)
        self.btnScannedHseMap.clicked.connect(self.show_scanned_hse_map_folder)
        self.btnScannedHsePic.clicked.connect(self.show_scanned_hse_pic_folder)
        self.btnScannedIdDoc.clicked.connect(self.show_scanned_id_doc_folder)
        self.btnScannedFamilyPhoto.clicked.connect(self.show_scanned_family_photo)
        self.btnScannedSignature.clicked.connect(self.show_scanned_signature)

        self.cbFamilyPhoto.toggled.connect(self.enable_family_photo)
        self.cbSign.toggled.connect(self.enable_signature)
        self.cbHousePhoto.toggled.connect(self.enable_house_photo)
        self.cbHousePic.toggled.connect(self.enable_house_pic)
        self.cbIdPic.toggled.connect(self.enable_id_pic)

        self.cbScannedDoc.toggled.connect(self.enable_scanned_doc)
        self.cbScannedHseMap.toggled.connect(self.enable_scanned_hse_map)
        self.cbScannedHsePic.toggled.connect(self.enable_scanned_hse_pic)
        self.cbScannedIdDoc.toggled.connect(self.enable_scanned_id_doc)
        self.cbScannedFamilyPhoto.toggled.connect(self.enable_scanned_family_photo)
        self.cbScannedSignature.toggled.connect(self.enable_scanned_signature)

        self.btnClose.clicked.connect(self.close_window)

        #Data Reader
        self.dataReader = None
        self.curr_profile = current_profile()

        self.twDocument.setCurrentIndex(0)
        self.twDocument.currentChanged.connect(self.page_changed)

        self.read_kobo_defaults()
        self.check_download_all()

        self.rbKoboMedia.setChecked(True)
        self.toggleSupportDoc(False)
        self.toggleScannedDoc(False)

        self.downloader_mode = DOWNLOAD_DOCS

    def hideWindow(self):
        self.hide()

    def kobo_media_clicked(self):
        if self.rbKoboMedia.isChecked():
            self.rbScannedDoc.setChecked(False)
            self.rbSupportDoc.setChecked(False)
            self.toggleKoboOptions(True)
            self.toggleSupportDoc(False)
            self.toggleScannedDoc(False)
            self.btnDownload.setEnabled(True)
            self.btnDownload.setStyleSheet("QPushButton{ background-color: rgb(85,255,127) }")
        else:
            self.toggleKoboOptions(False)
            self.disable_download_button()

    def support_doc_clicked(self):
        self.btnDownload.setText('Download')
        if self.rbSupportDoc.isChecked():
            self.rbScannedDoc.setChecked(False)
            self.rbKoboMedia.setChecked(False)
            self.toggleSupportDoc(True)
            self.toggleKoboSettings(True)
            self.toggleMediaFolders(False)
            self.toggleScannedDoc(False)
            self.btnDownload.setEnabled(True)
            self.btnDownload.setStyleSheet("QPushButton{ background-color: rgb(85,255,127) }")
        else:
            self.toggleSupportDoc(False)
            self.toggleKoboSettings(False)
            self.disable_download_button()

    def scanned_doc_clicked(self):
        self.rbScannedDoc.setChecked(True)
        self.rbKoboMedia.setChecked(False)
        self.rbSupportDoc.setChecked(False)
        self.toggleSupportDoc(False)
        self.toggleKoboSettings(False)
        self.toggleMediaFolders(False)
        self.toggle_csv_files(False)
        self.toggleScannedDoc(True)
        self.btnDownload.setEnabled(True)
        self.btnDownload.setStyleSheet("QPushButton{ background-color: rgb(255,85,0) }")

    def csv_clicked(self):
        self.rbScannedDoc.setChecked(False)
        self.rbKoboMedia.setChecked(False)
        self.rbSupportDoc.setChecked(False)
        self.toggleSupportDoc(False)
        self.toggleKoboSettings(False)
        self.toggleMediaFolders(False)
        self.toggleScannedDoc(False)
        self.toggle_csv_files(True)
        self.btnDownload.setEnabled(True)
        self.btnDownload.setStyleSheet("QPushButton{ background-color: rgb(255,85,0) }")


    def toggleScannedDoc(self, mode):
        self._toggleScannedDoc(mode)
        self._toggleScannedHseMap(mode)
        self._toggleScannedHsePic(mode)
        self._toggleScannedIdDoc(mode)

    def toggle_csv_files(self, mode):
        self.edtUploadFile.setEnabled(mode)
        self.enable_scanned_family_photo(mode)
        self.enable_scanned_signature(mode)


    def _toggleScannedDoc(self, mode):
        self.edtScannedDoc.setEnabled(mode)
        self.cbScannedDoc.setEnabled(mode)
        self.tbScannedDoc.setEnabled(mode)
        self.btnScannedDoc.setEnabled(mode)

    def _toggleScannedHseMap(self, mode):
        self.edtScannedHseMap.setEnabled(mode)
        self.cbScannedHseMap.setEnabled(mode)
        self.tbScannedHseMap.setEnabled(mode)
        self.btnScannedHseMap.setEnabled(mode)

    def _toggleScannedHsePic(self, mode):
        self.edtScannedHsePic.setEnabled(mode)
        self.cbScannedHsePic.setEnabled(mode)
        self.tbScannedHsePic.setEnabled(mode)
        self.btnScannedHsePic.setEnabled(mode)
    
    def _toggleScannedIdDoc(self, mode):
        self.edtScannedIdDoc.setEnabled(mode)
        self.cbScannedIdDoc.setEnabled(mode)
        self.tbScannedIdDoc.setEnabled(mode)
        self.btnScannedIdDoc.setEnabled(mode)

    def toggleKoboOptions(self, mode):
        self.toggleKoboSettings(mode)
        self.toggleMediaFolders(mode)

    def toggleSupportDoc(self, mode):
        self.edtHousePic.setEnabled(mode)
        self.cbHousePic.setEnabled(mode)
        self.tbHousePic.setEnabled(mode)
        self.btnHousePic.setEnabled(mode)

        self.edtIdPic.setEnabled(mode)
        self.cbIdPic.setEnabled(mode)
        self.tbIdPic.setEnabled(mode)
        self.btnIdPic.setEnabled(mode)

    def toggleMediaFolders(self, mode):
        self.edtFamilyFolder.setEnabled(mode)
        self.edtSignFolder.setEnabled(mode)
        self.edtHouseFolder.setEnabled(mode)
        self.tbFamilyFolder.setEnabled(mode)
        self.tbSignFolder.setEnabled(mode)
        self.tbHouseFolder.setEnabled(mode)
        self.btnFamilyBrowse.setEnabled(mode)
        self.btnSignFolder.setEnabled(mode)
        self.btnHouseFolder.setEnabled(mode)

        self.cbFamilyPhoto.setEnabled(mode)
        self.cbSign.setEnabled(mode)
        self.cbHousePhoto.setEnabled(mode)

    def toggleKoboSettings(self, mode):
        self.edtMediaUrl.setEnabled(mode)
        self.edtKoboUsername.setEnabled(mode)
        self.edtKoboPassword.setEnabled(mode)

    def read_kobo_defaults(self):
        self.edtMediaUrl.setText(get_media_url())
        self.edtKoboUsername.setText(get_kobo_user())
        self.edtFamilyFolder.setText(get_family_photo())
        self.edtSignFolder.setText(get_sign_photo())
        self.edtHouseFolder.setText(get_house_photo())
        self.edtHousePic.setText(get_house_pic())
        self.edtIdPic.setText(get_id_pic())
        self.edtScannedDoc.setText(get_scanned_doc())
        self.edtScannedHseMap.setText(get_scanned_hse_map())
        self.edtScannedHsePic.setText(get_scanned_hse_pic())
        self.edtScannedIdDoc.setText(get_scanned_id_doc())
        self.edtScannedFamilyPhoto.setText(get_scanned_family_photo())
        self.edtScannedSignature.setText(get_scanned_signature())

    def check_download_all(self):
        self.cbFamilyPhoto.setCheckState(Qt.Checked)
        self.cbSign.setCheckState(Qt.Checked)
        self.cbHousePhoto.setCheckState(Qt.Checked)
        self.cbHousePic.setCheckState(Qt.Checked)
        self.cbIdPic.setCheckState(Qt.Checked)

        #self.cbScannedDoc.setCheckState(Qt.Checked)
        #self.cbScannedHseMap.setCheckState(Qt.Checked)
        #self.cbScannedHsePic.setCheckState(Qt.Checked)
        #self.cbScannedIdDoc.setCheckState(Qt.Checked)
        #self.cbScannedFamilyPhoto.setCheckState(Qt.Checked)
        #self.cbScannedSignature.setCheckState(Qt.Checked)

    def set_source_file(self):
        #Set the file path to the source file
        image_filters = "Comma Separated Value (*.csv);;ESRI Shapefile (*.shp);;AutoCAD DXF (*.dxf)" 
        source_file = QFileDialog.getOpenFileName(self,"Select Source File",vectorFileDir(),image_filters)
        if source_file != "":
            self.txtDataSource.setText(source_file) 

    def set_upload_file(self):
        filters = "Comma Separated Value (*.csv);;"
        source_file = QFileDialog.getOpenFileName(self, "Select Source File", "", filters)
        if source_file != "":
            self.edtUploadFile.setText(source_file)
        
    def family_folder(self):
        dflt_folder = self.edtFamilyFolder.text()
        folder = self.select_media_folder(dflt_folder)
        if folder != '':
            self.edtFamilyFolder.setText(folder)
            save_family_photo(folder)

    def sign_folder(self):
        dflt_folder = self.edtSignFolder.text()
        folder = self.select_media_folder(dflt_folder)
        if folder != '':
            self.edtSignFolder.setText(folder)
            save_sign_photo(folder)

    def house_folder(self):
        dflt_folder = self.edtHouseFolder.text()
        folder = self.select_media_folder(dflt_folder)
        if folder != '':
            self.edtHouseFolder.setText(folder)
            save_house_photo(folder)

    def house_pic_folder(self):
        dflt_folder = self.edtHousePic.text()
        folder = self.select_media_folder(dflt_folder)
        if folder != '':
            self.edtHousePic.setText(folder)
            save_house_pic(folder)

    def id_pic_folder(self):
        dflt_folder = self.edtIdPic.text()
        folder = self.select_media_folder(dflt_folder)
        if folder != '':
            self.edtIdPic.setText(folder)
            save_id_pic(folder)

    def scanned_doc_folder(self):
        dflt_folder = self.edtScannedDoc.text()
        folder = self.select_media_folder(dflt_folder)
        if folder != '':
            self.edtScannedDoc.setText(folder)
            save_scanned_doc(folder)

    def scanned_hse_map_folder(self):
        dflt_folder = self.edtScannedHseMap.text()
        folder = self.select_media_folder(dflt_folder)
        if folder != '':
            self.edtScannedHseMap.setText(folder)
            save_scanned_hse_map(folder)

    def scanned_hse_pic_folder(self):
        dflt_folder = self.edtScannedHsePic.text()
        folder = self.select_media_folder(dflt_folder)
        if folder != '':
            self.edtScannedHsePic.setText(folder)
            save_scanned_hse_pic(folder)

    def scanned_id_doc_folder(self):
        dflt_folder = self.edtScannedIdDoc.text()
        folder = self.select_media_folder(dflt_folder)
        if folder != '':
            self.edtScannedIdDoc.setText(folder)
            save_scanned_id_doc(folder)

    def scanned_family_photo(self):
        dflt_folder = self.edtScannedFamilyPhoto.text()
        folder = self.select_media_folder(dflt_folder)
        if folder != '':
            self.edtScannedFamilyPhoto.setText(folder)
            save_scanned_family_photo(folder)

    def scanned_signature(self):
        dflt_folder = self.edtScannedSignature.text()
        folder = self.select_media_folder(dflt_folder)
        if folder != '':
            self.edtScannedSignature.setText(folder)
            save_scanned_signature(folder)

    def select_media_folder(self, dflt_folder):
        title = self.tr("Folder to store media files")
        trans_path = QFileDialog.getExistingDirectory(self, title, dflt_folder)
        return trans_path

    def valid_credentials(self):
        if self.edtMediaUrl.text() == '':
            self.ErrorInfoMessage("Source of media files")
            return False

        if self.edtKoboUsername.text() == '':
            self.ErrorInfoMessage("Please enter username")
            return False

        if self.edtKoboPassword.text() == '':
            self.ErrorInfoMessage("Please enter password")
            return False

        return True

    def show_family_folder(self):
        self.browse_folder(self.edtFamilyFolder.text())

    def show_sign_folder(self):
        self.browse_folder(self.edtSignFolder.text()) 

    def show_house_folder(self):
        self.browse_folder(self.edtHouseFolder.text())

    def show_house_pic_folder(self):
        self.browse_folder(self.edtHousePic.text()) 

    def show_id_pic_folder(self):
        self.browse_folder(self.edtIdPic.text()) 

    def show_scanned_doc_folder(self):
        self.browse_folder(self.edtScannedDoc.text()) 

    def show_scanned_hse_map_folder(self):
        self.browse_folder(self.edtScannedHseMap.text()) 

    def show_scanned_hse_pic_folder(self):
        self.browse_folder(self.edtScannedHsePic.text()) 

    def show_scanned_id_doc_folder(self):
        self.browse_folder(self.edtScannedIdDoc.text()) 

    def show_scanned_family_photo(self):
        self.browse_folder(self.edtScannedFamilyPhoto.text())

    def show_scanned_signature(self):
        self.browse_folder(self.edtScannedSignature.text())

    def browse_folder(self, folder):
        if folder == '':
            return
        # windows
        if sys.platform.startswith('win32'):
            os.startfile(folder)

        # *nix systems
        if sys.platform.startswith('linux'):
            subprocess.Popen(['xdg-open', folder])
        
        # macOS
        if sys.platform.startswith('darwin'):
            subprocess.Popen(['open', folder])

    def enable_family_photo(self, checked):
        self.edtFamilyFolder.setEnabled(checked)

    def enable_signature(self, checked):
        self.edtSignFolder.setEnabled(checked)

    def enable_house_photo(self, checked):
        self.edtHouseFolder.setEnabled(checked)

    def enable_house_pic(self, checked):
        self.edtHousePic.setEnabled(checked)

    def enable_id_pic(self, checked):
        self.edtIdPic.setEnabled(checked)

    def enable_scanned_doc(self, checked):
        self.edtScannedDoc.setEnabled(checked)

    def enable_scanned_hse_map(self, checked):
        self.edtScannedHseMap.setEnabled(checked)

    def enable_scanned_hse_pic(self, checked):
        self.edtScannedHsePic.setEnabled(checked)

    def enable_scanned_id_doc(self, checked):
        self.edtScannedIdDoc.setEnabled(checked)

    def enable_scanned_family_photo(self, checked):
        self.edtScannedFamilyPhoto.setEnabled(checked)

    def enable_scanned_signature(self, checked):
        self.edtScannedSignature.setEnabled(checked)

    def ErrorInfoMessage(self, message):
        #Error Message Box
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(message)
        msg.exec_()

    def fetch_selected_cols(self, doc_cols):
        """
        Extract text containing path from QLineEdit objects, only
        select from QLineEdits that are Enabled.
        Returns dict of {'csv_column_name':'path'}
        """
        sel_cols = {}
        for k, v in doc_cols.iteritems():
            line_edit = self.findChild(QLineEdit, v)
            if line_edit is None: continue
            if line_edit.isEnabled():
                sel_cols[k.lower()]=line_edit.text()
        return sel_cols

    def get_key_field(self, doc_cols):
        """
        Return the column name in the CSV that represents
        a key field.
        """
        for k, v in doc_cols.iteritems():
            if v == 'KEY':
                return k

    def fetch_doc_cols(self, media_columns):
        """
        Reads values from the mapfile to create a dict of
        {'csv_column_name':name_of_QLineEdit_with_dest_path}
        e.g. {'House Picture':'edtHousePic'}
        :rtype dict
        """
        cols = {}
        for k,v in media_columns.iteritems():
            a_col = unicode(k, 'utf-8').encode('ascii', 'ignore')
            cols[a_col] = v
        return cols

    def kobo_download_started(self, msg):
        self.btnDownload.setEnabled(False)
        self.edtProgress.append(msg+" started...")
        QApplication.processEvents()

    def kobo_download_completed(self, msg):
        self.btnDownload.setEnabled(True)
        self.edtProgress.setTextColor(QColor(51, 182, 45))
        self.edtProgress.setFontWeight(75)
        self.edtProgress.append(msg+" completed.")
        self.downloader_thread.quit()

    def kobo_download_progress(self, info_id, msg):
        clr = QColor('black')
        if info_id == 0: clr = QColor('black') #information
        if info_id == 1: clr = QColor(255, 170, 0) #Warning
        if info_id == 2: clr = QColor('red') #Error

        if info_id in [3,4,5]:
            self.update_progress_status(info_id)
            return
        self.edt_progress_update(clr,None,msg,True)
        QApplication.processEvents()

    def edt_progress_update(self, textcolor, textweight, msg, newline=False):
        if not textcolor is None:
            self.edtProgress.setTextColor(textcolor)
        if not textweight is None:
            self.edtProgress.setFontWeight(textweight)
        if not newline:
            self.edtProgress.textCursor().insertText(msg)
        else:
            self.edtProgress.append(msg)

    def update_progress_status(self, DNLD_Status_id):
        if DNLD_Status_id == 3: # Success
            self.edt_progress_update(
                QColor(51, 182, 45),
                None,
                'Success',
                False
            )

        if DNLD_Status_id == 4: # Failed
            self.edt_progress_update(
                QColor('red'),
                None,
                'Failed',
                False
            )

        if DNLD_Status_id == 5: # File Already Exists
            self.edt_progress_update(
                QColor(255,170,0),
                None,
                'Already Exists',
                False
            )
        
    def _downloader_thread_started(self):
        self.kobo_downloader.start_download()

    def _uploader_thread_started(self):
        if self.rbScannedDoc.isChecked():
            self.kobo_downloader.start_scanned_documents()
            return

        self.kobo_downloader.start_upload()

    def fix_auto_sequence(self):
        pg_fix_auto_sequence('oc_household_supporting_document', 'oc_household_supporting_document_id_seq')

    def download_media(self):
        self.fix_auto_sequence()

        # Uplaod documents
        if self.twDocument.currentIndex() == 1:

            if self.rbScannedDoc.isChecked():
                self.process_scanned_docs('scan')
                self.ErrorInfoMessage("Done uploading documents.")
                return

            # Download documents

            if self.edtUploadFile.text() == "":
                if self.cbScannedFamilyPhoto.isChecked() or self.cbScannedSignature.isChecked():
                    self.ErrorInfoMessage('Please select a source file.')
                    return
            else:
                self.process_scanned_docs('csv')
                return

        if self.txtDataSource.text() == "":
            self.ErrorInfoMessage("Please select a source file.")
            return

        if not QFile.exists(unicode(self.txtDataSource.text())):
            self.ErrorInfoMessage("The specified source file does not exist.")
            return

        if self.rbKoboMedia.isChecked():
            save_location = 'media-column'
            upload_after = False

        if self.rbSupportDoc.isChecked():
            save_location = 'support-doc-column'
            upload_after = True

        src_cols = mapfile_section(save_location)
        doc_types = mapfile_section('doc-types')
        media_columns = mapfile_section(save_location)
        doc_cols =self.fetch_doc_cols(media_columns)
        sel_cols = self.fetch_selected_cols(doc_cols)
        key_field = self.get_key_field(doc_cols)

        if not self.valid_credentials():
            return

        credentials = (self.edtKoboUsername.text(), self.edtKoboPassword.text())
        
        kobo_url = self.edtMediaUrl.text()
        save_media_url(kobo_url)
        save_kobo_user(credentials[0])

        support_doc_map = mapfile_section('support-doc-map')

        parent_ref_column = support_doc_map['parent_ref_column']

        self.kobo_downloader = KoboDownloader(
                self,
                OGRReader(unicode(self.txtDataSource.text())),
                sel_cols, key_field, doc_types, credentials, kobo_url, support_doc_map,
                self.curr_profile, upload_after, parent_ref_column)

        self.downloader_thread = QThread(self)
        self.kobo_downloader.moveToThread(self.downloader_thread)

        self.kobo_downloader.download_started.connect(self.kobo_download_started)
        self.kobo_downloader.download_progress.connect(self.kobo_download_progress)
        self.kobo_downloader.download_completed.connect(self.kobo_download_completed)

        self.downloader_thread.started.connect(self._downloader_thread_started)
        self.downloader_thread.finished.connect(self.downloader_thread.deleteLater)

        self.downloader_thread.start()

    def close_window(self):
        self.close()

    def process_scanned_docs(self, filename_src):
        """
        filename_src: Where to extract the name of the scanned document
        'scan' - Filename is extracted from the actual file.
        'csv' - Filename is picked from the CSV file
        """
        doc_types = mapfile_section('doc-types')
        if filename_src == 'scan':
            src_cols = mapfile_section('scanned-doc-column')
        else:
            src_cols = mapfile_section('csv-doc-column')
        
        sel_cols = self.fetch_selected_cols(src_cols)

        key_field = self.get_key_field(src_cols)
        support_doc_map = mapfile_section('support-doc-map')
        
        if filename_src == 'scan':
            parent_ref_column = support_doc_map['scanned_certificate']
        else:
            parent_ref_column = support_doc_map['supporting_docs']

        self.kobo_downloader = KoboDownloader(
                self,
                OGRReader(unicode(self.edtUploadFile.text())),
                sel_cols, 
                key_field, 
                doc_types, 
                ('',''), 
                '', 
                support_doc_map,
                self.curr_profile,
                True,
                parent_ref_column,
                ref_type='str')

        self.downloader_thread = QThread(self)
        self.kobo_downloader.moveToThread(self.downloader_thread)

        self.kobo_downloader.download_started.connect(self.kobo_download_started)
        self.kobo_downloader.download_progress.connect(self.kobo_download_progress)
        self.kobo_downloader.download_completed.connect(self.kobo_download_completed)

        self.downloader_thread.started.connect(self._uploader_thread_started)
        self.downloader_thread.finished.connect(self.downloader_thread.deleteLater)

        self.downloader_thread.start()

    def disable_download_button(self):
        self.btnDownload.setEnabled(False)
        self.btnDownload.setStyleSheet("")

    def page_changed(self, page_index):
        self.disable_download_button()
        if page_index == 0:
            self.downloader_mode = DOWNLOAD_DOCS
            self.btnDownload.setText('Download')
            self.gbProgress.setTitle("Download Progress:")

            if self.rbKoboMedia.isChecked():
                self.kobo_media_clicked()

            if self.rbSupportDoc.isChecked():
                self.support_doc_clicked()

        if page_index == 1:
            self.downloader_mode = UPLOAD_DOCS
            self.btnDownload.setText('Upload')
            self.gbProgress.setTitle("Upload Progress:")
            self.scanned_doc_clicked()
        

class KoboDownloader(QObject):
    download_started = pyqtSignal(unicode)
    #Signal contains message type and message
    download_progress = pyqtSignal(int, unicode)
    #Signal indicates True if the update succeeded, else False.
    download_completed = pyqtSignal(unicode)

    INFORMATION, WARNING, ERROR, SUCCESS, FAILED, EXISTS = range(0, 6)
    
    def __init__(self, ui, data_reader, sel_cols, key_field, 
            doc_types, credentials, kobo_url, support_doc_map, 
            curr_profile, upload_after, parent_ref_column, ref_type='int', parent=None):

        QObject.__init__(self, parent)

        self.ui = ui  # get the UI environment
        self.downloaded_files = {}      # key: key_field_value, value: list of tuple of (doc_type_id, dest_url)
        self.data_reader = data_reader
        self.selected_cols = sel_cols   
        self.key_field = key_field
        self.doc_types = doc_types
        self.credentials = credentials
        self.kobo_url = kobo_url
        self.support_doc_map = support_doc_map
        self.curr_profile = curr_profile
        self.upload_after = upload_after
        self.parent_ref_column = parent_ref_column
        self.ref_type = ref_type
        self.net_requests = []
        self.net_access_managers = []

    def start_download(self):
        self.download_started.emit('Download')
        downloaded_files = self.run()
        if self.upload_after:
            self.upload_downloaded_files(downloaded_files)
        self.download_completed.emit('Download')

    def start_scanned_documents(self):
        self.download_started.emit('Upload')
        dfiles = self.fetch_scanned_certificates()
        self.upload_downloaded_files(dfiles)
        self.download_completed.emit('Upload')

        #if self.ui.cbScannedHseMap.isChecked():
            #dfiles = self.fetch_scanned_docs('house plot map')
            #self.upload_downloaded_files(dfiles)

        #if self.ui.cbScannedHsePic.isChecked():
            #dfiles = self.fetch_scanned_docs('house photo')
            #self.upload_downloaded_files(dfiles)

        #if self.ui.cbScannedIdDoc.isChecked():
            #dfiles = self.fetch_scanned_docs('id document')
            #self.upload_downloaded_files(dfiles)

        #if self.ui.cbScannedFamilyPhoto.isChecked():
            #dfiles = self.fetch_scanned_docs('family photo')
            #self.upload_downloaded_files(dfiles)

        #if self.ui.cbScannedSign.isChecked():
            #dfiles = self.fetch_scanned_docs('signature')
            #self.upload_downloaded_files(dfiles)

    def check_iscustomfield(self, fieldname):
        csv_custom_columns = mapfile_section('csv-doc-specialcolumn')
        if csv_custom_columns is None:      
            return ''
        
        for k, v in csv_custom_columns.iteritems():
            line_edit = self.findChild(QLineEdit, v)
            key = unicode(k, 'utf-8').encode('ascii', 'ignore')
            fname = unicode(fieldname, 'utf-8').encode('ascii', 'ignore')
            if fname.lower() == key.lower():
                return v.lower()
        return ''

    def start_upload(self):
        file_names = []
        #key_field_value = 0
        src_cols = self.data_reader.getFields()
        lyr = self.data_reader.getLayer()
        lyr.ResetReading()
        feat_defn = lyr.GetLayerDefn()
        numFeat = lyr.GetFeatureCount()
        #ErrMessage(str(self.selected_cols))
        feat_len = len(lyr)
        for index, feat in enumerate(lyr):

            msg = 'Record: {} of {}'.format(str(index+1), str(feat_len))
            self.download_progress.emit(KoboDownloader.INFORMATION, msg)

            key_field_value = -1
            file_names = []
            # loop through the columns in the CSV file.
            for f in range(feat_defn.GetFieldCount()):
                field_defn = feat_defn.GetFieldDefn(f)
                field_name = field_defn.GetNameRef()
                a_field_name = unicode(field_name, 'utf-8').encode('ascii', 'ignore').lower()
                a_field_customtype = self.check_iscustomfield(field_name)
                # Get the Key Field value for later use
                if a_field_name == self.key_field:
                    key_field_value = feat.GetField(f)
                    #ErrMessage('SET Key Field Value = {}'.format(key_field_value))
                    continue

                # We are dealing with only columns that have been selected in the mapfile
                if a_field_customtype == '':
                    continue

                #dest_folder = ''
                field_value = feat.GetField(f)
                if field_value == '':
                    continue

                if a_field_customtype not in ['family_photo','signature']:
                    continue

                if a_field_customtype == 'family_photo':
                    if self.ui.cbScannedFamilyPhoto.isChecked():
                        file_names += self.make_upload_files(field_name, field_value, key_field_value)
                    else:
                        msg = 'Family photo - Not checked for upload!'
                        self.download_progress.emit(KoboDownloader.INFORMATION, msg)

                if a_field_customtype == 'signature':
                    if self.ui.cbScannedSignature.isChecked():
                        file_names += self.make_upload_files(field_name, field_value, key_field_value)
                    else:
                        msg = 'Signature - Not checked for upload!'
                        self.download_progress.emit(KoboDownloader.INFORMATION, msg)
            if key_field_value != -1:
                for fn in file_names:
                    if fn['key_field_value'] == -1:
                        fn['key_field_value'] = key_field_value
                if key_field_value in self.downloaded_files:
                    self.downloaded_files[key_field_value].extend(file_names)
                else:
                    self.downloaded_files[key_field_value] = copy.deepcopy(file_names)
        #ErrMessage(str(self.downloaded_files))

        self.download_started.emit('Upload')
        self.upload_downloaded_files(self.downloaded_files)
        self.download_completed.emit('Upload')
        
    def make_upload_files(self, field_name, field_value, key_field_value):
        file_names = []
        fname_type = self.check_iscustomfield(field_name)
        dest_folder = ''
        for k, v in self.selected_cols.iteritems():
            line_edit = self.findChild(QLineEdit, v)
            key = unicode(k, 'utf-8').encode('ascii', 'ignore')
            fname = unicode(field_name, 'utf-8').encode('ascii', 'ignore')
            if fname.lower() == key.lower():
                dest_folder = v
        if dest_folder == '':
            return file_names
        
        #self.selected_cols[field_name]
        dest_url = dest_folder + '\\'+field_value
        src_url = self.kobo_url+field_value

        if fname_type in self.doc_types:
            doc_type_id = self.doc_types[fname_type]
        else:
            doc_type_id = -1

        file_names.append(
                {'doc_type_id':doc_type_id, 
                 'key_field_value':key_field_value,
                 'filename':dest_url
                    })

        return file_names

    def check_field_is_fullurl(self, fieldname):
        media_column_fullurl = mapfile_section('media-column-url')
        if media_column_fullurl is None:
            return False
        
        for k, v in media_column_fullurl.iteritems():
            line_edit = self.findChild(QLineEdit, v)
            key = unicode(k, 'utf-8').encode('ascii', 'ignore')
            fname = unicode(fieldname, 'utf-8').encode('ascii', 'ignore')
            if fname.lower() == key.lower():
                if 'fullurl' == v.lower():
                    return True
        return False

    def run(self):
        file_names = []
        key_field_value = 0
        src_cols = self.data_reader.getFields()
        lyr = self.data_reader.getLayer()
        lyr.ResetReading()
        feat_defn = lyr.GetLayerDefn()
        numFeat = lyr.GetFeatureCount()

        feat_len = len(lyr)
        self.kobo_downloader_ex = KB_DocumentDownloader(
            self.credentials[0],
            self.credentials[1]
        )
        for index, feat in enumerate(lyr):

            msg = 'Record: {} of {}...'.format(str(index+1), str(feat_len))
            self.download_progress.emit(KoboDownloader.INFORMATION, msg)

            # loop through the columns in the CSV file.
            for f in range(feat_defn.GetFieldCount()):
                field_defn = feat_defn.GetFieldDefn(f)
                field_name = field_defn.GetNameRef()
                a_field_name = unicode(field_name, 'utf-8').encode('ascii', 'ignore').lower()

                # Get the Key Field value for later use
                if a_field_name == self.key_field:
                    key_field_value = feat.GetField(f)
                    continue

                # We are dealing with only columns that have been selected in the mapfile
                if a_field_name not in self.selected_cols.keys():
                    continue

                #dest_folder = ''
                dest_folder = self.selected_cols[a_field_name]
                field_value = feat.GetField(f)

                if field_value == '': continue
                if self.check_field_is_fullurl(field_name):
                    #src_url = u'{}'.format(field_value).replace('%2F','/')
                    src_url = field_value.replace('%2F','/')
                    asc_field_value = unicode(os.path.basename(src_url), 'utf-8').encode('ascii', 'ignore')
                    #ErrMessage(asc_field_value)
                else:
                    asc_field_value = unicode(
                        field_value,
                        'utf-8'
                    ).encode('ascii', 'ignore') #to fix arabic filename issue
                    src_url = self.kobo_url + asc_field_value


                dest_url = dest_folder + '\\' + asc_field_value                               
                #for my own test src_url = self.kobo_url+'1669887425606.jpg'

                dest_url = dest_folder + '\\'+field_value
                src_url = self.kobo_url.strip('\n')+field_value.strip('\n')

                msg = 'Preparing File: {} '.format(field_value)


                msg = u'Downloading File: {}... '.format(asc_field_value)
                status_code = -1
                if not path.exists(dest_url):
                    self.download_progress.emit(KoboDownloader.INFORMATION, msg)
                    # download file
                    if self.download(
                            src_url,
                            dest_url,
                            self.credentials[0],
                            self.credentials[1]
                        ): status_code = KoboDownloader.SUCCESS
                    else: status_code = KoboDownloader.FAILED
                else: status_code = KoboDownloader.EXISTS
                if status_code != -1: self.download_progress.emit(status_code, '')

                if a_field_name in self.doc_types:
                    doc_type_id = self.doc_types[a_field_name]
                else:
                    doc_type_id = -1

                file_names.append(
                        {'doc_type_id':doc_type_id, 
                         'key_field_value':key_field_value,
                         'filename':dest_url
                            })

            for fnames in file_names:
                fnames['key_field_value'] = key_field_value

            if key_field_value in self.downloaded_files:
                self.downloaded_files[key_field_value].extend(file_names)
            else:
                self.downloaded_files[key_field_value] = copy.deepcopy(file_names)

            file_names = []

        return self.downloaded_files

    def fetch_scanned_certificates(self):
        """
        Return a dict of {'filename':[{'doc_type_id', 'key_field_value', 'filename'}]}
        :filename: Physical name of the file on the disk
        :doc_type_id: Id picked from lookup "oc_check_household_document_type"
        :src_dir : Path where the file is found in the disk
        """
        dtype = 'scanned certificate'  
        dfiles = {}

        src_folder = self.selected_cols.get(dtype) # local folder with scanned certificates

        if src_folder is None or src_folder=='':
            return dfiles

        dtype_id = self.doc_types[dtype]  # ID for document of type "Scanned certificate" in table "check_document_type"

        for filename in os.listdir(src_folder):
            if fnmatch.fnmatch(filename, '*.pdf'):
                name, file_ext = os.path.splitext(filename)
                doc_src = []
                full_path = src_folder+'\\'+filename
                doc_src.append(
                        {'doc_type_id':dtype_id,
                         'key_field_value':unicode(name),
                         'filename':full_path})
                dfiles[unicode(name)]=doc_src
        return dfiles

    def fetch_scanned_docs(self, doc_type):
        """
        Return a dict of {'filename':[{'doc_type_id':, key_field_value':, 'filename':}]}
        :rtype dict:
        """
        dfiles = {}
        src_folder = self.selected_cols.get(doc_type)

        if src_folder is None or src_folder == '':
            return dfiles

        dtype_id = self.doc_types[doc_type]
        for filename in os.listdir(src_folder):
            if fnmatch.fnmatch(filename, '*.jpg'):
                name, file_ext = os.path.splitext(filename)
                orig_name = name
                # clean any postfix numbers in the filename
                split_name = name.split('_', 2)
                if len(split_name) > 1:
                    name = split_name[0]+'_'+split_name[1]
                else:
                    name = split_name[0]
                doc_src = []
                full_path = src_folder+'\\'+filename
                doc_src.append(
                        {'doc_type_id':dtype_id, 
                         'key_field_value':name, 
                         'filename':full_path})
                dfiles[orig_name]=doc_src
        return dfiles

    def upload_downloaded_files(self, downloaded_files):
        #1. Create and get ID from the supporting documents table
        #2. Get Household ID
        #3. Get ID of document type 
        #4. Create a record of entity_supporting_document
        if len(downloaded_files) == 0:
            return

        doc_type_cache = {}
        #ErrMessage(str(downloaded_files))
        msg = "Uploading files to STDM started ..."
        self.download_progress.emit(KoboDownloader.INFORMATION, msg)
        #ErrMessage(str(downloaded_files))
        for key, value in downloaded_files.iteritems():
            ref_code = value[0]['key_field_value']

            #ErrMessage(self.support_doc_map['parent_table'])
            #ErrMessage(str(ref_code))
            #ErrMessage(self.parent_ref_column)
            try:
                parent_id = self.get_parent_id(self.support_doc_map['parent_table'],
                                                     ref_code, self.parent_ref_column)
            except:
                parent_id = None

            if parent_id is None:
                msg = "ERROR. No record found for key: "+str(ref_code)
                self.download_progress.emit(KoboDownloader.ERROR, msg)
                continue

            for sfile in downloaded_files[key]:
                src_doc_type = sfile['doc_type_id'] 
                short_filename = sfile['key_field_value'] 
                full_filename = sfile['filename']  # full path of the source file

                if not os.path.exists(full_filename):
                    msg = "ERROR: File :"+full_filename+" does not exist!"
                    self.download_progress.emit(KoboDownloader.ERROR, msg)
                    continue

                msg = 'Uploading file: {}...'.format(short_filename)
                self.download_progress.emit(KoboDownloader.INFORMATION, msg)

                support_doc = self.make_supporting_doc_dict(full_filename, self.support_doc_map)

                found_error = False

                try:
                    result_obj = pg_create_supporting_document(support_doc)
                    next_support_doc_id = result_obj.fetchone()[0]
                    support_doc_table = self.support_doc_map['parent_support_table']
                except:
                    msg = "ERROR: pg_create_supporting_document: "+support_doc['doc_filename']
                    self.download_progress.emit(KoboDownloader.ERROR, msg)
                    found_error = True

                if found_error:
                    continue

                try:
                    # Create a record in the parent table supporting document table (oc_household_supporting_document)
                    # parent table is "oc_household"
                    self.create_supporting_doc(support_doc_table, next_support_doc_id, parent_id, int(src_doc_type))
                except:
                    msg = "ERROR: create_supporting_doc: "+str(parent_id)
                    self.download_progress.emit(KoboDownloader.ERROR, msg)
                    found_error = True

                if found_error:
                    continue

                try:
                    # copy file to STDM supporting document path
                    if src_doc_type in doc_type_cache:
                        doc_type = doc_type_cache[src_doc_type]
                    else:
                        doc_type = get_value_by_column(
                                self.support_doc_map['doc_type_table'], 'value', 'id', src_doc_type)
                        doc_type_cache[src_doc_type] = doc_type

                    new_filename = support_doc['doc_identifier']
                    self.create_new_support_doc_file(sfile, new_filename, doc_type, self.support_doc_map)
                    self.download_progress.emit(KoboDownloader.SUCCESS, '')
                except:
                    msg = "ERROR Copying File: "+full_filename
                    self.download_progress.emit(KoboDownloader.ERROR, msg)


    def get_parent_id(self, parent_table, value, parent_ref_column):
        """
         Given a unique reference, return a record "id" of the parent table ("oc_household")
        :param parent_table: Table where to get the ID.
        :param value : search value
        :param parent_ref_column: Column to find the value from
        :rtype : int
        """
        table_name = parent_table
        target_col = 'id'
        where_col = parent_ref_column
        if self.ref_type != 'int':
            value = "'"+value+"'"
        id = get_value_by_column(table_name, target_col, where_col, value)
        return id

    def make_supporting_doc_dict(self, doc_name, doc_map):
        doc_size = os.path.getsize(doc_name)
        path, filename = os.path.split(doc_name)
        ht = hashlib.sha1(filename.encode('utf-8'))
        document = {}
        document['support_doc_table'] = doc_map['main_table']
        document['creation_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        document['doc_identifier'] = ht.hexdigest()
        document['source_entity'] = doc_map['parent_table']
        document['doc_filename'] = filename
        document['document_size'] = doc_size
        return document

        # write to db
        #pg_create_supporting_document(document)

    def create_supporting_doc(self, table_name, next_doc_id, household_id, doc_type_id):
        pg_create_parent_supporting_document(table_name, next_doc_id, household_id, doc_type_id)

    def create_new_support_doc_file(self, old_file, new_filename, dtype, support_doc_map):
        self.reg_config = RegistryConfig()
        support_doc_path = self.reg_config.read([NETWORK_DOC_RESOURCE])
        old_file_type = old_file['doc_type_id']  #old_file[0]
        old_filename = old_file['filename']  #old_file[2]
        name, file_ext = os.path.splitext(old_filename)

        doc_path = support_doc_path.values()[0]
        profile_name = self.curr_profile.name
        entity_name = support_doc_map['parent_table']
        doc_type = dtype.replace(' ','_').lower()

        dest_path = doc_path+'/'+profile_name.lower()+'/'+entity_name+'/'+doc_type+'/'
        dest_filename = dest_path+new_filename+file_ext

        if not os.path.exists(dest_path):
            os.makedirs(dest_path)

        shutil.copy(old_filename, dest_filename)

    def download(self, src_url, dest_url, username, password):

        """

        self.dest_url = dest_url

        net_request = DownloadRequest(src_url, dest_url, self)
        net_access_manager = QtNetwork.QNetworkAccessManager()
        net_access_manager.finished.connect(net_request.handle_download_response)
        header_data = QByteArray('{}:{}'.format(username, password)).toBase64()
        net_request.setRawHeader('Authorization', 'Basic {}'.format(header_data))

        self.net_requests.append(net_request)

        net_access_manager.get(net_request)

        self.net_access_managers.append(net_access_manager)


    def download_request(self, src_url, dest_url, username, password):


        req = requests.get(src_url, auth=(username,password))
        with open(dest_url, 'wb') as f:
            f.write(req.content)
        return req.status_code == 200
        """
        if self.kobo_downloader_ex is None:
            self.kobo_downloader_ex = KB_DocumentDownloader(
                username,
                password  
            )
        return self.kobo_downloader_ex.kobo_download(
            src_url,
            dest_url
        ) 


    def fake_download(self, src_url, dest_url, username, password):
        return 200
        

def ErrMessage(message):
    #Error Message Box
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setText(message)
    msg.exec_()



        


        
