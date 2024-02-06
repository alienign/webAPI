import os
import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt


SCREEN_SIZE = [600, 450]


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.lon = input()
        self.lat = input()
        self.delta = input()
        self.getImage()

    def getImage(self):
        import requests
        api_server = "http://static-maps.yandex.ru/1.x/"

        params = {
            "ll": ",".join([self.lon, self.lat]),
            "spn": ",".join([self.delta, self.delta]),
            "l": "map"
        }
        response = requests.get(api_server, params=params)

        if not response:
            print("Ошибка выполнения запроса:")
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        # Запишем полученное изображение в файл.
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')

        ## Изображение
        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.image.setPixmap(self.pixmap)

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            self.delta = str(float(self.delta) + 0.01)
            self.getImage()
        elif event.key() == Qt.Key_PageDown:
            if float(self.delta) - 0.01 != 0:
                self.delta = str(float(self.delta) - 0.01)
                self.getImage()
            else:
                sys.exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())