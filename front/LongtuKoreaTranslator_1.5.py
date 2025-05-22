# -*- coding: utf-8 -*-

import functools
import logging
import os

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline

from settings import GLOSSARY_DICT, PROJECT_ID
from translate_with_custom_model import translate_texts, FileTranslateFactory

logging.basicConfig(level=logging.DEBUG)


class DocumentTranslateThread(QThread):
    progress_bar_setVisible = pyqtSignal(bool)
    document_enabled = pyqtSignal(bool)
    progress_bar_init = pyqtSignal(int)
    progress_bar_updateNum = pyqtSignal(int)

    def __init__(self,
                 file_path_source: str,
                 translator: pipeline
                 ):
        """
        :param file_path_source: your_source file path
        :param translator: transformers.pipeline
        """
        super().__init__()
        self.file_path = file_path_source
        self.translator = translator
        logging.debug("{0} successfully initialized.".format(self.__class__.__name__))

    def run(self):
        try:
            # 显示进度条、禁用按钮
            self.progress_bar_setVisible.emit(True)
            self.document_enabled.emit(False)
            # 翻译文件
            file_type = os.path.splitext(self.file_path)[1].lstrip(".")
            file_translator = FileTranslateFactory().create_document_translator(file_type)
            file_translator.translate(self.file_path,
                                      self.translator,
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

        model_name = "models/nllb-200-1.3B/zh2ko_0907"
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.translator_zh2ko = pipeline("translation", model=model, tokenizer=tokenizer,
                                         src_lang="zho_Hans", tgt_lang="kor_Hang",
                                         device="cuda:0")
        self.translator_ko2zh = pipeline("translation", model=model, tokenizer=tokenizer,
                                         src_lang="kor_Hang", tgt_lang="zho_Hans",
                                         device="cuda:0")

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
        self.Korean2ChinesePushButton.setVisible(False)  # 由于确实韩到中的模型，所以暂时禁用该功能
        self.chineseDocumentPushButton = QtWidgets.QPushButton(Dialog)
        self.chineseDocumentPushButton.setGeometry(QtCore.QRect(180, 250, 90, 40))
        self.chineseDocumentPushButton.setObjectName("ChineseDocument")
        self.koreanDocumentPushButton = QtWidgets.QPushButton(Dialog)
        self.koreanDocumentPushButton.setGeometry(QtCore.QRect(180, 500, 90, 40))
        self.koreanDocumentPushButton.setObjectName("KoreanDocument")
        self.koreanDocumentPushButton.setVisible(False)  # 由于确实韩到中的模型，所以暂时禁用该功能
        self.progressBar = QtWidgets.QProgressBar(Dialog)
        self.progressBar.setGeometry(QtCore.QRect(600, 510, 181, 71))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(True)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setObjectName("progressBar")
        self.progressBar.setVisible(False)

        self.retranslateUi(Dialog)
        self.Chinese2KoreanPushButton.clicked.connect(
            functools.partial(self.text_translate_clicked, self.translator_zh2ko, self.chineseTextEdit,
                              self.koreanTextEdit))  # type: ignore
        self.Korean2ChinesePushButton.clicked.connect(
            functools.partial(self.text_translate_clicked, self.translator_ko2zh, self.koreanTextEdit,
                              self.chineseTextEdit))  # type: ignore
        self.chineseDocumentPushButton.clicked.connect(
            functools.partial(self.document_translate_clicked, self.translator_zh2ko))  # type: ignore
        self.koreanDocumentPushButton.clicked.connect(
            functools.partial(self.document_translate_clicked, self.translator_ko2zh))  # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "LongtuKoreaTranslator"))
        self.Chinese2KoreanPushButton.setText(_translate("Dialog", "中 -> 한"))
        self.Korean2ChinesePushButton.setText(_translate("Dialog", "한 -> 中"))
        self.chineseDocumentPushButton.setText(_translate("Dialog", "文件"))
        self.koreanDocumentPushButton.setText(_translate("Dialog", "파일"))

    def text_translate_clicked(self,
                               translator: pipeline,
                               source_QTextEdit: QtWidgets.QTextEdit,
                               target_QTextEdit: QtWidgets.QTextEdit):
        target_QTextEdit.clear()
        lines = source_QTextEdit.toPlainText().split('\n')
        # filter
        lines = [line for line in lines if len(line) > 0]
        text_translated = translate_texts(lines, translator)
        text_translated = "\n".join(text_translated)
        target_QTextEdit.append(text_translated)

    def document_translate_clicked(self,
                                   translator: pipeline):
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
            self.document_translate_thread = DocumentTranslateThread(file_path, translator)

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


if __name__ == "__main__":
    import sys

    # GUI程序

    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
