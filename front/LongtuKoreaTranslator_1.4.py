# -*- coding: utf-8 -*-

import functools
import logging
import os

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal

from settings import GLOSSARY_DICT, PRIVATE_KEY_NAME, PROJECT_ID
from translate import translate_texts, FileTranslateFactory

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
                 glossary_id: str = None
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
            file_type = os.path.splitext(self.file_path)[1].lstrip(".")
            translator = FileTranslateFactory().create_document_translator(file_type)
            translator.translate(self.file_path,
                                 self.project_id,
                                 self.source_language_code,
                                 self.target_language_code,
                                 glossary_id=self.glossary_id,
                                 progress_bar_init=self.progress_bar_init,
                                 progress_bar_num=self.progress_bar_updateNum)
            # 隐藏进度条、启用按钮
            self.progress_bar_setVisible.emit(False)
            self.document_enabled.emit(True)
        except Exception as e:
            logging.error("Exception occurred: {0}".format(str(e)))


class Ui_Dialog(object):
    def __init__(self):
        self.document_translate_thread = None
        self.project_id = PROJECT_ID
        self.glossary_dict = GLOSSARY_DICT
        self.glossary_id = None

    def setupUi(self, Dialog):

        Dialog.setObjectName("Dialog")
        Dialog.resize(800, 600)
        self.chineseTextEdit = QtWidgets.QTextEdit(Dialog)
        self.chineseTextEdit.setGeometry(QtCore.QRect(70, 60, 640, 160))
        self.chineseTextEdit.setObjectName("ChineseEdit")
        self.koreanTextEdit = QtWidgets.QTextEdit(Dialog)
        self.koreanTextEdit.setGeometry(QtCore.QRect(70, 320, 640, 160))
        self.koreanTextEdit.setObjectName("KoreanEdit")
        self.Chinese2KoreanPushButton = QtWidgets.QPushButton(Dialog)
        self.Chinese2KoreanPushButton.setGeometry(QtCore.QRect(70, 250, 90, 40))
        self.Chinese2KoreanPushButton.setObjectName("Chinese2Korean")
        self.Korean2ChinesePushButton = QtWidgets.QPushButton(Dialog)
        self.Korean2ChinesePushButton.setGeometry(QtCore.QRect(70, 500, 90, 40))
        self.Korean2ChinesePushButton.setObjectName("Korean2Chinese")
        self.chineseDocumentPushButton = QtWidgets.QPushButton(Dialog)
        self.chineseDocumentPushButton.setGeometry(QtCore.QRect(180, 250, 90, 40))
        self.chineseDocumentPushButton.setObjectName("ChineseDocument")
        self.koreanDocumentPushButton = QtWidgets.QPushButton(Dialog)
        self.koreanDocumentPushButton.setGeometry(QtCore.QRect(180, 500, 90, 40))
        self.koreanDocumentPushButton.setObjectName("KoreanDocument")
        self.progressBar = QtWidgets.QProgressBar(Dialog)
        self.progressBar.setGeometry(QtCore.QRect(600, 510, 181, 71))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(True)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setObjectName("progressBar")
        self.progressBar.setVisible(False)
        self.glossaryComboBox = QtWidgets.QComboBox(Dialog)
        self.glossaryComboBox.setGeometry(QtCore.QRect(469, 540, 110, 40))
        self.glossaryComboBox.setObjectName("glossaryComboBox")
        self.glossaryComboBox.addItem("")

        self.retranslateUi(Dialog)
        self.Chinese2KoreanPushButton.clicked.connect(
            functools.partial(self.text_translate_clicked, "zh-CN", "ko", self.chineseTextEdit,
                              self.koreanTextEdit))  # type: ignore
        self.Korean2ChinesePushButton.clicked.connect(
            functools.partial(self.text_translate_clicked, "ko", "zh-CN", self.koreanTextEdit,
                              self.chineseTextEdit))  # type: ignore
        self.chineseDocumentPushButton.clicked.connect(
            functools.partial(self.document_translate_clicked, "zh-CN", "ko"))  # type: ignore
        self.koreanDocumentPushButton.clicked.connect(
            functools.partial(self.document_translate_clicked, "ko", "zh-CN"))  # type: ignore
        self.glossaryComboBox.currentTextChanged.connect(self.glossary_selected)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "LongtuKoreaTranslator"))
        self.Chinese2KoreanPushButton.setText(_translate("Dialog", "中 -> 한"))
        self.Korean2ChinesePushButton.setText(_translate("Dialog", "한 -> 中"))
        self.chineseDocumentPushButton.setText(_translate("Dialog", "文件"))
        self.koreanDocumentPushButton.setText(_translate("Dialog", "파일"))
        self.glossaryComboBox.setItemText(0, _translate("Dialog", "术语表/용어집"))
        self.glossaryComboBox.addItems(self.glossary_dict.keys())

    def text_translate_clicked(self,
                               source_language_code: str,
                               target_language_code: str,
                               source_QTextEdit: QtWidgets.QTextEdit,
                               target_QTextEdit: QtWidgets.QTextEdit):
        target_QTextEdit.clear()
        lines = source_QTextEdit.toPlainText().split('\n')
        # filter
        lines = [line for line in lines if len(line) > 0]
        text_translated = translate_texts(lines, self.project_id,
                                          source_language_code,
                                          target_language_code,
                                          glossary_id=self.glossary_id)
        text_translated = "\n".join(text_translated)
        target_QTextEdit.append(text_translated)

    def document_translate_clicked(self,
                                   source_language_code: str,
                                   target_language_code: str, ):
        # 设置文件对话框参数并显示
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.ReadOnly
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Select a file", "",
                                                             "Excel Files (*.xlsx);;Text Files (*.txt);;CSV Files (*.csv);;TSV Files (*.tsv)",
                                                             options=options)
        # 如果
        if file_path == "":
            return
        else:
            # 大坑解决：如果实例化这个线程类的时候没有定义为类变量而只是使用局部变量，则这个函数结束运行后会自动销毁，造成难以排查的bug。
            self.document_translate_thread = DocumentTranslateThread(file_path,
                                                                     self.project_id,
                                                                     source_language_code,
                                                                     target_language_code,
                                                                     glossary_id=self.glossary_id)

            self.document_translate_thread.progress_bar_setVisible.connect(self.setVisible_progress_bar)
            self.document_translate_thread.document_enabled.connect(self.set_document_enabled)
            self.document_translate_thread.progress_bar_init.connect(self.init_progress_bar)
            self.document_translate_thread.progress_bar_updateNum.connect(self.updateNum_progress_bar)
            logging.debug("Starting document translate thread.")
            self.document_translate_thread.start()

    def setVisible_progress_bar(self, visible: bool):
        self.progressBar.setVisible(visible)

    def set_document_enabled(self, enabled: bool):
        self.chineseDocumentPushButton.setEnabled(enabled)
        self.koreanDocumentPushButton.setEnabled(enabled)

    def init_progress_bar(self, max_num: int):
        # Initialize the progress bar
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(max_num)
        self.progressBar.setValue(0)

    def updateNum_progress_bar(self, value: int):
        # Update Progress Bar
        self.progressBar.setValue(value)

    def glossary_selected(self):
        self.glossary_id = self.glossary_dict.get(self.glossaryComboBox.currentText(), None)


if __name__ == "__main__":
    import sys


    # 设置环境变量
    def resource_path(relative_path):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath('.'), relative_path)


    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = resource_path(PRIVATE_KEY_NAME)

    # GUI程序

    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
