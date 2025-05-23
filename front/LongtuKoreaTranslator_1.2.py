# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'front_page.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
from PyQt5 import QtCore, QtWidgets
from translate import *
from settings import *
import functools

from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal

import logging

logging.basicConfig(level=logging.DEBUG)


class DocumentTranslateThread(QThread):
    progress_bar_setVisible = pyqtSignal(bool)
    document_enabled = pyqtSignal(bool)
    progress_bar_init = pyqtSignal(int)
    progress_bar_updateNum = pyqtSignal(int)

    def __init__(self,
                 file_path_source: str,
                 project_id: str,
                 source_language_code: str,
                 target_language_code: str,
                 glossary_id: str
                 ):
        """
        :param file_path_source: your_source file path
        :param project_id: your project id
        :param source_language_code: source language code
        :param target_language_code: target language code
        :param glossary_id: your glossary id
        """
        super().__init__()
        self.file_path = file_path_source
        self.project_id = project_id
        self.source_language_code = source_language_code
        self.target_language_code = target_language_code
        self.glossary_id = glossary_id
        logging.debug("{0} successfully initialized.".format(self.__class__.__name__))

    def run(self):
        try:
            # 显示进度条、禁用按钮
            self.progress_bar_setVisible.emit(True)
            self.document_enabled.emit(False)
            # 翻译文件
            file_type = os.path.splitext(self.file_path)[1]
            # Excel File
            if file_type == ".xlsx":
                translate_excel_file(self.file_path,
                                     self.project_id,
                                     self.source_language_code,
                                     self.target_language_code,
                                     self.glossary_id,
                                     self.progress_bar_init,
                                     self.progress_bar_updateNum)
            # csv File
            elif file_type == ".csv":
                translate_csv_file(self.file_path,
                                   self.project_id,
                                   self.source_language_code,
                                   self.target_language_code,
                                   self.glossary_id,
                                   self.progress_bar_init,
                                   self.progress_bar_updateNum)
            # txt File
            elif file_type == ".txt":
                translate_txt_file(self.file_path,
                                   self.project_id,
                                   self.source_language_code,
                                   self.target_language_code,
                                   self.glossary_id,
                                   self.progress_bar_init,
                                   self.progress_bar_updateNum)
            else:
                pass
            # 隐藏进度条、启用按钮
            self.progress_bar_setVisible.emit(False)
            self.document_enabled.emit(True)
        except Exception as e:
            logging.error("Exception occurred: {0}".format(str(e)))


class Ui_Dialog(object):
    def setupUi(self, Dialog):

        Dialog.setObjectName("Dialog")
        Dialog.resize(800, 600)
        self.ChineseEdit = QtWidgets.QTextEdit(Dialog)
        self.ChineseEdit.setGeometry(QtCore.QRect(70, 60, 640, 160))
        self.ChineseEdit.setObjectName("ChineseEdit")
        self.KoreanEdit = QtWidgets.QTextEdit(Dialog)
        self.KoreanEdit.setGeometry(QtCore.QRect(70, 320, 640, 160))
        self.KoreanEdit.setObjectName("KoreanEdit")
        self.Chinese2Korean = QtWidgets.QPushButton(Dialog)
        self.Chinese2Korean.setGeometry(QtCore.QRect(70, 250, 90, 40))
        self.Chinese2Korean.setObjectName("Chinese2Korean")
        self.Korean2Chinese = QtWidgets.QPushButton(Dialog)
        self.Korean2Chinese.setGeometry(QtCore.QRect(70, 500, 90, 40))
        self.Korean2Chinese.setObjectName("Korean2Chinese")
        self.ChineseDocument = QtWidgets.QPushButton(Dialog)
        self.ChineseDocument.setGeometry(QtCore.QRect(180, 250, 90, 40))
        self.ChineseDocument.setObjectName("ChineseDocument")
        self.KoreanDocument = QtWidgets.QPushButton(Dialog)
        self.KoreanDocument.setGeometry(QtCore.QRect(180, 500, 90, 40))
        self.KoreanDocument.setObjectName("KoreanDocument")
        self.progressBar = QtWidgets.QProgressBar(Dialog)
        self.progressBar.setGeometry(QtCore.QRect(600, 510, 181, 71))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(True)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setObjectName("progressBar")
        self.progressBar.setVisible(False)

        self.retranslateUi(Dialog)
        self.Chinese2Korean.clicked.connect(
            functools.partial(self.text_translate_clicked, "zh-CN", "ko", self.ChineseEdit,
                              self.KoreanEdit))  # type: ignore
        self.Korean2Chinese.clicked.connect(
            functools.partial(self.text_translate_clicked, "ko", "zh-CN", self.KoreanEdit,
                              self.ChineseEdit))  # type: ignore
        self.ChineseDocument.clicked.connect(
            functools.partial(self.document_translate_clicked, "zh-CN", "ko"))  # type: ignore
        self.KoreanDocument.clicked.connect(
            functools.partial(self.document_translate_clicked, "ko", "zh-CN"))  # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "LongtuKoreaTranslator"))
        self.Chinese2Korean.setText(_translate("Dialog", "中 -> 한"))
        self.Korean2Chinese.setText(_translate("Dialog", "한 -> 中"))
        self.ChineseDocument.setText(_translate("Dialog", "文档"))
        self.KoreanDocument.setText(_translate("Dialog", "문서"))

    def text_translate_clicked(self,
                               source_language_code: str,
                               target_language_code: str,
                               source_QTextEdit: QtWidgets.QTextEdit,
                               target_QTextEdit: QtWidgets.QTextEdit):
        target_QTextEdit.clear()
        for line in source_QTextEdit.toPlainText().split('\n'):
            # 过滤空白项
            if line == "":
                continue
            text_translated = translate_text_with_glossary(line, PROJECT_ID, source_language_code, target_language_code,
                                                           GLOSSARY_ID_ALL)
            target_QTextEdit.append(text_translated)

    def document_translate_clicked(self,
                                   source_language_code: str,
                                   target_language_code: str, ):
        # 设置文件对话框参数并显示
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.ReadOnly
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Select a file", "",
                                                             "Excel Files (*.xlsx);;Text Files (*.txt);;CSV Files (*.csv)",
                                                             options=options)
        # 如果
        if file_path == "":
            return
        else:
            # 大坑解决：如果实例化这个线程类的时候没有定义为类变量而只是使用局部变量，则这个函数结束运行后会自动销毁，造成难以排查的bug。
            self.document_translate_thread = DocumentTranslateThread(file_path,
                                                                     PROJECT_ID,
                                                                     source_language_code,
                                                                     target_language_code,
                                                                     GLOSSARY_ID_ALL)

            self.document_translate_thread.progress_bar_setVisible.connect(self.setVisible_progress_bar)
            self.document_translate_thread.document_enabled.connect(self.set_document_enabled)
            self.document_translate_thread.progress_bar_init.connect(self.init_progress_bar)
            self.document_translate_thread.progress_bar_updateNum.connect(self.updateNum_progress_bar)
            logging.debug("Starting document translate thread.")
            self.document_translate_thread.start()

    def setVisible_progress_bar(self, visible: bool):
        self.progressBar.setVisible(visible)

    def set_document_enabled(self, enabled: bool):
        self.ChineseDocument.setEnabled(enabled)
        self.KoreanDocument.setEnabled(enabled)

    def init_progress_bar(self, max_num: int):
        # Initialize the progress bar
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(max_num)
        self.progressBar.setValue(0)

    def updateNum_progress_bar(self, value: int):
        # Update Progress Bar
        self.progressBar.setValue(value)


if __name__ == "__main__":
    # 设置环境变量
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.abspath(PRIVATE_KEY_NAME)

    # GUI程序
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
