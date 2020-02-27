from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel
from PyQt5.QtGui import QPixmap
import requests
import geocoder


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('UI.ui', self)
        self.pushButton.clicked.connect(self.update_params)

        self.setWindowTitle('Тест')
        # self.setGeometry(200, 200, 300, 300)

        self.api_key = "40d1649f-0493-4b70-98ba-98533de7710b"
        self.coords = '44.6736646,40.7696272'
        self.zoom = 1
        self.delta = 0
        self.api_server = f"https://static-maps.yandex.ru/1.x/"

        self.params = {
            "ll": self.coords,
            "z": str(self.zoom),
            "size": '650,450',
            "l": "sat",
            # {долгота},{широта},{стиль}{цвет}{размер}{контент} '37.44,55.818,pma
            "pt": self.coords + ',pm'
        }

    def keyPressEvent(self, event):
        print('pressed:', event.key())
        if event.key() == 16777238:
            self.change_zoom(1)
        if event.key() == 16777239:
            self.change_zoom(-1)
        # self.update_map()

    def get_map(self):
        response = requests.get(self.api_server, params=self.params)
        with open("map.png", 'wb') as f:
            f.write(response.content)
            # print('get map')

    def change_pos(self):
        place = ','.join(list(reversed(list(map(str, geocoder.location(self.lineEdit.text()).latlng)))))
        # print(place)
        self.coords = place
        self.params["ll"] = self.coords
        self.params["pt"] = self.coords + ',pm2rdm'

    def change_zoom(self, d=0):
        if d == 0:
            self.zoom = int(self.lineEdit_2.text())
        else:
            self.zoom = self.zoom + d
        if self.zoom not in range(1, 18):
            self.zoom -= d
            print('back')
        self.params["z"] = str(self.zoom)
        self.lineEdit_2.setText(str(self.zoom))
        self.update_map()
        print(d, self.zoom)

    def load_image(self, file_name):
        pixmap = QPixmap(file_name)
        # self.label = QLabel(self)
        self.label.setPixmap(pixmap)
        self.label.resize(pixmap.width(), pixmap.height())
        # self.resize(pixmap.width(), pixmap.height())

    def update_params(self):
        self.change_pos()
        self.change_zoom()

    def update_map(self):
        self.get_map()
        self.load_image('map.png')


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    ex = App()
    ex.load_image("map.png")
    ex.show()
    sys.exit(app.exec_())
