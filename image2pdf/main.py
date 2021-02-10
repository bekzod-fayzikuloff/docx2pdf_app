import os
import time
import sys
from PIL import Image

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


def image_convert(path):
    image1 = Image.open(f'{path}')
    im1 = image1.convert('RGB')
    im1.save(f'{path[:-4]}.pdf')


class MyButtonForConvert(QPushButton):
    __stylesheet__ = '''
        QPushButton{
            background-color: #8D838E;
            color: #E1E1E1;
            border-radius: 6px;        
        }
        QPushButton:hover {
        background-color:rgb(31,101,163);
        }
        QPushButton:pressed {
        background-color:rgb(31,101,163);
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
        self.setText("<font color='#756DAC'><b>Перетените сюда (.png или jpg.) файл</b></font>")
        self.setStyleSheet('''
            QLabel{
                border: 3px dashed #5D42B9;
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
        win.label.setText("<font color='#756DAC'><b>Начался процесс конвертации</b></font>")
        try:
            image_convert(self.path)
            win.label.setFont(QFont('SansSerif', 9, QFont.StyleItalic))
            win.label.setText(
                "<font color='#756DAC'><b>Конвертация заверщена (перетените сюда (.png или jpg.) файл)</b></font>"
            )
        except Exception as e:
            win.label.setText(
                f"<font color='#756DAC'><b>Простите не удалось провести конвертацию {e}</b></font>"
            )


class Window(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Img2PDF')
        self.setStyleSheet("background-color: #F0F0F0;")
        self.setWindowIcon(QIcon(resource_path(r'ico\pdf_logo.png')))
        self.resize(440, 300)
        self.init_ui()
        self.setAcceptDrops(True)

    def init_ui(self):
        global convertBtn
        self.label = MyLabel()

        convertBtn = MyButtonForConvert('convert')
        convertBtn.setEnabled(False)
        convertBtn.clicked.connect(self.convert)

        self.fileBtn = MyButtonForConvert('select image')
        self.fileBtn.clicked.connect(self.select_file)

        self.hBox = QHBoxLayout()
        self.hBox.addWidget(convertBtn)
        self.hBox.addWidget(self.fileBtn)

        self.vBox = QVBoxLayout()
        self.vBox.addWidget(self.label)
        self.vBox.addLayout(self.hBox)

        self.setLayout(self.vBox)

    def convert(self):
        self.thread = MyThread(file_path)
        self.thread.start()
        # print(file_path)
        convertBtn.setEnabled(False)

    def select_file(self):
        global file_path
        path_to_file = QFileDialog.getOpenFileName(self)[0]
        file_path = path_to_file
        # print(path_to_file)
        if path_to_file != '':
            convertBtn.setEnabled(True)


# *********************************************************** #
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    print("--- {} секунд ---".format(time.time() - start_time))
    sys.exit(app.exec())

