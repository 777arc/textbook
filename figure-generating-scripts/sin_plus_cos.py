import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLabel, QSizePolicy, QSlider, QSpacerItem, QVBoxLayout, QWidget, QGridLayout
import pyqtgraph as pg # sudo pip3 install pyqtgraph
import numpy as np

class Slider(QWidget):
    def __init__(self, minimum, maximum, prefix):
        super(Slider, self).__init__()
        self.verticalLayout = QVBoxLayout(self)
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignHCenter)
        self.verticalLayout.addWidget(self.label)
        self.slider = QSlider(self)
        self.slider.setOrientation(Qt.Horizontal)
        self.verticalLayout.addWidget(self.slider)
        self.minimum = minimum
        self.maximum = maximum
        self.prefix = prefix
        self.slider.valueChanged.connect(self.setLabelValue)
        self.setLabelValue(self.slider.value())
        
    def setLabelValue(self, value):
        self.x = self.minimum + (float(value) / (self.slider.maximum() - self.slider.minimum())) * (self.maximum - self.minimum)
        self.label.setText(self.prefix + "{0:.2g}".format(self.x))

class Widget(QWidget):
    def __init__(self):
        super(Widget, self).__init__()
        self.setFixedWidth(800) 
        self.setFixedHeight(550) 
        self.Layout = QGridLayout(self)
        self.w1 = Slider(-2, 2, 'I = ')
        self.Layout.addWidget(self.w1, 0, 0)
        self.w2 = Slider(-2, 2, 'Q = ')
        self.Layout.addWidget(self.w2, 1, 0)
        self.win = pg.GraphicsLayoutWidget()
        self.Layout.addWidget(self.win, 2, 0)
        self.plot = self.win.addPlot()
        self.plot.addLegend()
        self.curve_I = self.plot.plot(pen='r', name="I*cos()")
        self.curve_Q = self.plot.plot(pen='b', name="Q*sin()")
        self.curve_sum = self.plot.plot(pen='g', name="I*cos() + Q*sin()")
        self.update_plot()
        self.plot.setXRange(0, 150)
        self.plot.setYRange(-3, 3)
        self.w1.slider.valueChanged.connect(self.update_plot)
        self.w2.slider.valueChanged.connect(self.update_plot)
        
    def update_plot(self):
        x = np.linspace(0, 10, 150)
        self.curve_I.setData(self.w1.x*np.cos(x))
        self.curve_Q.setData(self.w2.x*np.sin(x))
        self.curve_sum.setData(self.w1.x*np.cos(x) + self.w2.x*np.sin(x))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Widget()
    w.show()
    sys.exit(app.exec_())
