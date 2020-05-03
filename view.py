""" Basic gui to display the agent during its 
Q-Learning process
"""
import os
import numpy as np
import pickle

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

TAXI = QImage("./images/taxi.png")
CAR_CRASHED = QImage("./images/car_crashed.png")
ROAD_CLOSURE = QImage("./images/road_closure.png")
WALL = QImage("./images/wall.png")

TOPOLOGY_LOG = os.path.join("logs", "track_topology.npy")
MOVES_LOG = os.path.join("logs", "all_moves.obj")

# time between each display/step update in ms
TIME_BETWEEN_STEPS = 300


class Agent(QWidget):
    """ Define how the agent will be displayed """

    def __init__(self, x, y):
        super(Agent, self).__init__()

        self.setFixedSize(QSize(25, 25))
        self.x = x
        self.y = y

    def paintEvent(self, event):
        """ Set the style for the widget when it is called """
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        r = event.rect()
        outer, inner = Qt.blue, Qt.darkBlue

        p.drawPixmap(r, QPixmap(TAXI))

class Obstacle(QWidget):
    """ Define how the other elements  will be displayed """

    def __init__(self, x, y, mode):
        super(Obstacle, self).__init__()
        self.mode = mode
        self.x = x
        self.y = y
        if self.mode == 'wall':
            self.outer, self.inner = QColor('#9C27B0'), QColor('#00BCD4')
            self.setFixedSize(QSize(25, 25))
        elif self.mode == 'final':
            self.outer, self.inner = Qt.green, Qt.blue
            self.setFixedSize(QSize(25, 5))

        elif self.mode == 'crash' or self.mode == 'road_closure':
            self.outer, self.inner = Qt.red, Qt.darkRed
            self.setFixedSize(QSize(25, 25))
            
            

    def paintEvent(self, event):
        """ Set the style for the widget when it is called """
        p = QPainter(self)
        r = event.rect()
        if self.mode == 'final':
            p.setRenderHint(QPainter.Antialiasing)
            p.fillRect(r, QBrush(self.inner))
            pen = QPen(self.outer)
            pen.setWidth(5)
            p.setPen(pen)
            p.drawRect(r)

        elif self.mode == 'wall' or self.mode == 'crash':
            p.setRenderHint(QPainter.Antialiasing)
            p.fillRect(r, QBrush(self.inner))
            pen = QPen(self.outer)
            pen.setWidth(5)
            p.setPen(pen)
            p.drawRect(r)
            p.drawPixmap(r, QPixmap(WALL))
        if self.mode == 'road_closure':
            p.drawPixmap(r, QPixmap(ROAD_CLOSURE))
        elif self.mode == 'crash':
            p.drawPixmap(r, QPixmap(CAR_CRASHED))


class MainWindow(QMainWindow):
    """ Main window frame of the gui """
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # Initiate the timer
        self.timer = QBasicTimer()

        w = QWidget()
        hb = QHBoxLayout()
        self.episode_label = QLabel()
        self.episode_label.setAlignment(Qt.AlignLeft)
        self.episode_label.setFont(QFont("Fixed",14, weight=QFont.Bold))
        self.step_label = QLabel()
        self.step_label.setAlignment(Qt.AlignRight)
        self.step_label.setFont(QFont("Fixed",14, weight=QFont.Bold))

        hb.addWidget(self.episode_label)
        hb.addWidget(self.step_label)

        self.episode_timer = QTimer()
        self.episode_timer.timeout.connect(self.update_episode_timer)
        self.episode_timer.start(TIME_BETWEEN_STEPS)

        vb = QVBoxLayout()
        vb.addLayout(hb)

        self.grid = QGridLayout()
        self.grid.setSpacing(7)

        vb.addLayout(self.grid)
        w.setLayout(vb)
        self.setCentralWidget(w)

        self.get_episodes()
        self.obtain_sizes()
        self.init_map()
        self.show()

    def get_episodes(self):
        """ Draw all episode """
        with open(MOVES_LOG, 'rb') as log:
            self.all_moves = pickle.load(log)

    def obtain_sizes(self):
        """ Obtain the track topology and board sizes """
        self.length_all_episodes = len(self.all_moves)
        self.episode = 0
        self.step = 0
        # Add positions to the map
        self.topology = []
        self.topology = np.load(TOPOLOGY_LOG)
        self.top_dims = self.topology.shape

        
    def reset_map(self):
        """ Remove all blocks to start a new episode """
        for x in range(0, self.top_dims[1]):
            for y in range(0, self.top_dims[0]):
                try:
                    w = self.grid.itemAtPosition(y, x).widget()
                    w.setParent(None)
                except AttributeError:
                    pass

    def init_map(self):
        """ Initialize the board to prepare
        for a new episode
        """

        # Add road topology
        for x in range(0, self.top_dims[1]):
            for y in range(0, self.top_dims[0]):
                if self.topology[y, x] == 1:
                    w = Obstacle(x, y, 'wall')
                    self.grid.addWidget(w, y, x)
                elif self.topology[y, x] == 2:
                    w = Obstacle(x, y, 'road_closure')
                    self.grid.addWidget(w, y, x)
        # Add finish line
        for x in range(0, self.top_dims[1]):
            w = Obstacle(x, self.top_dims[0] + 1, 'final')
            self.grid.addWidget(w, self.top_dims[0] + 1, x)

    def place_new_widget(self, pos_x, pos_y):
        """ Place a new widget on the board """
        # Remove the old agent display if present
        try:
            self.w.setParent(None)
            
        except AttributeError:
            pass
        try:
            # If an obstacle exists at this place, display a crash
            if self.grid.itemAtPosition(pos_y, pos_x).widget():
                self.w = Obstacle(pos_x, pos_y, 'crash')
        # Otherwise, add a normal agent widget
        except AttributeError:
            self.w = Agent(pos_x, pos_y)
        self.grid.addWidget(self.w, pos_y, pos_x)

    def update_episode_timer(self):
        """ Execute a gui display update at every new timer event"""
        self.init_map()
        if self.episode < self.length_all_episodes:
            # Choose the mode to be displayed
            if self.episode == self.length_all_episodes - 1:
                mode = "Test"
            else:
                mode = "Training"

            self.episode_label.setText("{}".format(mode))
            
            if self.step < len(self.all_moves[self.episode]):
                pos_x, pos_y = self.all_moves[self.episode][self.step]
                self.step_label.setText("#{}".format(self.episode))
                self.place_new_widget(pos_x, pos_y)
                self.step += 1

            else:
                self.episode += 1
                self.step = 0
                self.reset_map()
            
if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    app.exec_()
