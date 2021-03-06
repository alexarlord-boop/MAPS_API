from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel
from PyQt5.QtGui import QPixmap
import requests
import geocoder


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('UI.ui', self)
        self.pushButton.clicked.connect(self.change_pos_by_line)
        self.pushButton_2.clicked.connect(self.change_l)
        self.pushButton_3.clicked.connect(self.change_l)
        self.pushButton_4.clicked.connect(self.change_l)
        self.pushButton_5.clicked.connect(self.clear)
        self.setWindowTitle('MAP')

        # self.setGeometry(200, 200, 300, 300)

        self.api_key = "40d1649f-0493-4b70-98ba-98533de7710b"
        self.coords = '90,0'
        self.pointer = None
        self.zoom = 1
        self.delta = 0
        self.layer = 'sat'
        self.api_server = f"https://static-maps.yandex.ru/1.x/"

        self.params = {
            "ll": self.coords,
            "z": str(self.zoom),
            "size": '650,450',
            "l": "sat"
            # "pt": self.coords + ',pm'
        }

    def keyPressEvent(self, event):
        # print('pressed:', event.key())
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

    def change_pos_by_line(self):
        self.coords = ','.join(list(reversed(list(map(str, geocoder.location(self.lineEdit.text()).latlng)))))
        print(self.coords)
        self.pointer = self.coords
        if self.coords == '':
            self.coords = '90,0'
            self.params = self.params = {
                "ll": self.coords,
                "z": str(self.zoom),
                "size": '650,450',
                "l": self.layer
            }
        else:
            self.params = {
                "ll": self.coords,
                "z": str(self.zoom),
                "size": '650,450',
                "l": self.layer,
                "pt": self.coords + ',pm2rdm'
            }
        self.update_map()
        # self.params["pt"] = self.coords + ',pm2rdm'

    def clear(self):
        self.lineEdit.setText('')
        self.change_pos_by_line()
        self.lineEdit_2.setText('1')
        self.pointer = None
        self.change_zoom()
        self.update_map()

    def change_pos(self, pos):
        self.coords = pos
        self.params = {
            "ll": self.coords,
            "z": str(self.zoom),
            "size": '650,450',
            "l": self.layer
        }

    def change_tile(self, side, k):
        n = 2 ** self.zoom
        tile_size = 180 / n
        lng, lat = list(map(float, self.coords.split(',')))
        if side == 'h':
            new_lng = lng + k * tile_size
            if -180 > new_lng or new_lng > 180:
                pass
            else:
                new_coords = ','.join([str(new_lng), str(lat)])
                self.change_pos(new_coords)
                if bool(self.pointer) is True:
                    self.params["pt"] = self.pointer + ',pm2rdm'
                self.update_map()
        if side == 'v':
            new_lat = lat + k * tile_size
            if -90 > new_lat or new_lat > 89:
                pass
            else:
                new_coords = ','.join([str(lng), str(new_lat)])
                self.change_pos(new_coords)
                if bool(self.pointer) is True:
                    self.params["pt"] = self.pointer + ',pm2rdm'
                self.update_map()

    def change_zoom(self, d=0):
        if d == 0:
            self.zoom = int(self.lineEdit_2.text())
        else:
            if self.zoom + d not in range(0, 18):
                pass
            else:
                self.zoom += d
        self.lineEdit_2.setText(str(self.zoom))
        self.params["z"] = str(self.zoom)
        self.update_map()

    def change_l(self):
        sender = self.sender()
        if sender.objectName()[-1] == '2':
            self.layer = 'map'
        if sender.objectName()[-1] == '3':
            self.layer = 'sat'
        if sender.objectName()[-1] == '4':
            self.layer = 'sat,skl'
        self.params["l"] = self.layer
        self.update_map()

    def load_image(self, file_name):
        pixmap = QPixmap(file_name)
        # self.label = QLabel(self)
        self.label.setPixmap(pixmap)
        self.label.resize(pixmap.width(), pixmap.height())
        # self.resize(pixmap.width(), pixmap.height())

    def update_map(self):
        # self.update_params()
        # print("map update")
        self.get_map()
        self.load_image('map.png')


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    ex = App()
    ex.update_map()
    ex.show()
    sys.exit(app.exec_())
