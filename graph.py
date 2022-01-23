import sys
import PyQt5.QtWidgets as qtw
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import pandas as pd


class GraphWindow(qtw.QMainWindow):
    def __init__(self, dataframe, parent=None):
        super(GraphWindow, self).__init__(parent)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.button = qtw.QPushButton('Plot')
        self.df = dataframe
        self.button.clicked.connect(self.plot)

        # creating a Vertical Box layout
        layout = qtw.QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.button)

        widget = qtw.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.show()

    # action called by the push button
    def plot(self):
        print(type(self.df))
        # clearing old figure
        self.figure.clear()

        # create an axis
        ax = self.figure.add_subplot(111)

        # plot data
        ax.plot(self.df)
        self.canvas.draw()


# driver code
if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)

    df = pd.read_csv('TSLA.csv', skiprows=[])
    df['Date'] = pd.to_datetime(df.Date, format='%Y-%m-%d')  # format data
    df.index = df['Date']

    main = GraphWindow(df['Close'])
    main.show()
    sys.exit(app.exec_())
