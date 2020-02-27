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
            "l": "sat"

            # "pt": self.coords + ',pm'
        }

    def keyPressEvent(self, event):
        print('pressed:', event.key())
        if event.key() == 16777238:
            self.change_zoom(1)
        if event.key() == 16777239:
            self.change_zoom(-1)
        if event.key() == 52:
            self.change_tile('h', -1)  # left
        if event.key() == 54:
            self.change_tile('h', 1)  # right
        if event.key() == 50:
            self.change_tile('v', -1)  # down
        if event.key() == 56:
            self.change_tile('v', 1)  # up

    def get_map(self):
        response = requests.get(self.api_server, params=self.params)
        with open("map.png", 'wb') as f:
            f.write(response.content)

    def change_pos(self, data=None):
        if data is None:
            place = ','.join(list(reversed(list(map(str, geocoder.location(self.lineEdit.text()).latlng)))))
        else:
            place = data
        # print(place)
        self.coords = place
        self.params["ll"] = self.coords
        # self.params["pt"] = self.coords + ',pm2rdm'

    def change_tile(self, side, k):

        n = 2 ** self.zoom
        tile_size = 180 / n
        print(n, tile_size)

        lng, lat = list(map(float, self.coords.split(',')))
        new_coords = self.coords
        print(lng, lat)

        if side == 'h':
            new_lng = lng + k * tile_size
            if -180 > new_lng or new_lng > 180:
                new_lng = lng
            new_coords = ','.join([str(new_lng), str(lat)])

        if side == 'v':
            new_lat = lat + k * tile_size
            if -90 > new_lat or new_lat > 90:
                new_lat = lat
            new_coords = ','.join([str(lng), str(new_lat)])

        self.change_pos(new_coords)
        self.update_map()
        print(new_coords)

    def change_zoom(self, d=0):
        if d == 0:
            self.zoom = int(self.lineEdit_2.text())
        else:
            self.zoom = self.zoom + d
        if self.zoom not in range(0, 18):
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
