import os
import time
import sys
import docx2pdf

from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QHBoxLayout,
                             QVBoxLayout, QLabel, QFileDialog)
from PyQt5.QtCore import Qt, QThread
# *******************************************************************************#
start_time = time.time()


def resource_path(relative):
    """
    Функция которая возваращает
    абсолютный путь к данной директории
    """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative)
    else:
        return os.path.join(os.path.abspath("."), relative)


class MyButtonForConvert(QPushButton):
    __stylesheet__ = '''
        QPushButton{
            background-color: #3C3F41;
            color: #E1E1E1;
            border-radius: 6px;        
        }
        QPushButton:hover {
        background-color: #198754;
        }
        QPushButton:pressed {
        background-color: #198754;
        }
    '''

    def __init__(self, text_on_btn=None):
        super().__init__()
        self.text_on_btn = text_on_btn
        self.setMinimumHeight(20)
        self.setFont(QFont('SansSerif', 10, QFont.Bold))
        self.setText(self.text_on_btn)
        self.setStyleSheet(MyButtonForConvert.__stylesheet__)


class MyLabel(QLabel):

    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignCenter)
        self.setFont(QFont('SansSerif', 11, QFont.StyleItalic))
        self.setText("<font color='#756DAC'><b>Перетените сюда (.doxc) файл</b></font>")
        self.setStyleSheet('''
            QLabel{
                border: 3px dashed #9146FF;
            }
        ''')
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasImage:
            global file_path
            event.setDropAction(Qt.CopyAction)
            file_path = event.mimeData().urls()[0].toLocalFile()
            convertBtn.setEnabled(True)
            event.accept()
        else:
            event.ignore()


class MyThread(QThread):

    def __init__(self, path):
        super().__init__()
        self.path = path

    def run(self) -> None:
        if self.path[-5:] == '.docx' or '.' not in self.path:
            win.label.setText("<font color='#756DAC'><b>Начался процесс конвертации</b></font>")
            try:
                docx2pdf.convert(self.path)
                win.label.setFont(QFont('SansSerif', 9, QFont.StyleItalic))
                win.label.setText(
                    "<font color='#756DAC'><b>Конвертация заверщена (перетените сюда (.doxc) файл)</b></font>"
                )
            except:
                win.label.setText(
                    "<font color='#756DAC'><b>Простите не удалось провести конвертацию</b></font>"
                )
        else:
            win.label.setText("<font color='#756DAC'><b>Вы указали неправильный формат файла</b></font>")


class Window(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Word2PDF')
        self.setStyleSheet("background-color: #F0F0F0;")
        self.setWindowIcon(QIcon(resource_path(r'icons\pdf_logo.png')))
        self.resize(440, 300)
        self.init_ui()
        self.setAcceptDrops(True)

    def init_ui(self):
        global convertBtn
        self.label = MyLabel()

        convertBtn = MyButtonForConvert('convert')
        convertBtn.setEnabled(False)
        convertBtn.clicked.connect(self.convert)

        self.folderBtn = MyButtonForConvert('select folder')
        self.folderBtn.setIcon(QIcon(resource_path(r'icons\folders.png')))
        self.folderBtn.clicked.connect(self.select_folder)

        self.hBox = QHBoxLayout()
        self.hBox.addWidget(convertBtn)
        self.hBox.addWidget(self.folderBtn)

        self.vBox = QVBoxLayout()
        self.vBox.addWidget(self.label)
        self.vBox.addLayout(self.hBox)

        self.setLayout(self.vBox)

    def convert(self):
        self.thread = MyThread(file_path)
        self.thread.start()
        print(file_path)
        convertBtn.setEnabled(False)

    def select_folder(self):
        global file_path
        directory = QFileDialog.getExistingDirectory(self)
        file_path = directory
        print(directory)
        if directory != '':
            convertBtn.setEnabled(True)


# *********************************************************** #
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    print("--- {} секунд ---".format(time.time() - start_time))
    sys.exit(app.exec())