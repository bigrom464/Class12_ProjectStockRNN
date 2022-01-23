from PyQt5 import QtCore as qtc, QtGui as qtg, QtWidgets as qtw
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar

import sys
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

import stock_model as sm


class GraphWindow(qtw.QMainWindow):
    def __init__(self, dataframe, parent=None):
        super(GraphWindow, self).__init__(parent)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.df = dataframe['Close']

        # creating a Vertical Box layout
        layout = qtw.QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

        widget = qtw.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.plot()

    # To plot the points from self.df
    def plot(self):
        # clearing old figure
        self.figure.clear()
        # create an axis
        ax = self.figure.add_subplot(111)
        # plot data
        ax.plot(self.df)
        self.canvas.draw()

    # To close the graph
    def close(self):
        self.toolbar.close()
        self.canvas.close()


class MainWidget(qtw.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(
            "Foresight | A Python Stock Prediction Application")

        self.predictGraph = self.searchGraph = self.ticker = self.date = None
        grid = qtw.QGridLayout()  # initialize base layout

        # Create Create ticker Input Box including: Title, Input Box, Buttons
        ticker_box = qtw.QVBoxLayout()
        ticker_box.addSpacerItem(qtw.QSpacerItem(80, 80))

        label = qtw.QLabel("Stock Ticker")
        label.setFont(qtg.QFont('Calibri', 14))
        ticker_box.addWidget(label)

        ticker_input = qtw.QLineEdit(placeholderText='Enter Stock Ticker...')
        ticker_input.setMinimumHeight(40)
        ticker_box.addWidget(ticker_input)

        ticker_actions = qtw.QHBoxLayout()
        ticker_run = qtw.QPushButton(
            "Run", clicked=lambda: run_ticker())
        ticker_run.setMinimumHeight(40)
        ticker_change = qtw.QPushButton(
            "Change", clicked=lambda: change_ticker())
        ticker_change.setMinimumHeight(40)
        ticker_change.setDisabled(True)

        ticker_actions.addWidget(ticker_run)
        ticker_actions.addWidget(ticker_change)
        ticker_box.addLayout(ticker_actions)

        ticker_box.addSpacerItem(qtw.QSpacerItem(80, 80))
        ticker_box.insertStretch(-1, 1)

        grid.addLayout(ticker_box, 0, 0)

        # Create date search Input Box including: Title, Input Box, Buttons
        date_box = qtw.QVBoxLayout()
        date_box.addSpacerItem(qtw.QSpacerItem(80, 80))

        label = qtw.QLabel("Search Stock Value [Month]")
        label.setFont(qtg.QFont('Calibri', 14))
        date_box.addWidget(label)

        date_input = qtw.QLineEdit(placeholderText='yyyy-mm-dd between {} and {}'.format(
            sm.getIPO(), qtc.QDate.currentDate().toString(qtc.Qt.ISODate)))
        date_input.setValidator(qtg.QRegExpValidator(
            qtc.QRegExp('\d{4}\-\d{2}\-\d{2}')))
        date_input.setMinimumHeight(40)
        date_box.addWidget(date_input)

        date_actions = qtw.QHBoxLayout()
        date_run = qtw.QPushButton(
            "Search", clicked=lambda: run_date())
        date_run.setMinimumHeight(40)
        date_change = qtw.QPushButton(
            "Change", clicked=lambda: change_date())
        date_change.setMinimumHeight(40)
        date_change.setDisabled(True)

        date_actions.addWidget(date_run)
        date_actions.addWidget(date_change)
        date_box.addLayout(date_actions)

        date_box.addSpacerItem(qtw.QSpacerItem(80, 80))
        date_box.insertStretch(-1, 1)
        grid.addLayout(date_box, 0, 1)

        self.setLayout(grid)  # Set grid as main layout

        def run_ticker():
            if ticker_input.text() == "":
                showDialog()  # Display dialog on invalid input
            else:
                # Disable further input during processing
                ticker_input.setDisabled(True)
                ticker_run.setDisabled(True)
                ticker_change.setDisabled(False)

                self.ticker = ticker_input.text()
                ipo = sm.getIPO(self.ticker)
                today = qtc.QDate.currentDate().toString(qtc.Qt.ISODate)

                date_input.setPlaceholderText('yyyy-mm-dd between {} and {}'.format(
                    ipo, today))  # Change valid dates according to IPO

                # Plot real and then predicted values
                self.predictGraph = GraphWindow(
                    sm.getPlotData(self.ticker, ipo, today))
                grid.addWidget(self.predictGraph, 1, 0)  # Add to layout

        def change_ticker():  # Change ticker
            ticker_input.clear()
            self.ticker = ""

            ticker_input.setDisabled(False)  # Allow user to change input
            ticker_run.setDisabled(False)
            ticker_change.setDisabled(True)

            self.predictGraph.close()  # Close displayed graph

        def run_date():
            if date_input.text() == "":
                showDialog()  # Display dialog on invalid input
            else:
                # Disable further input during processing
                date_input.setDisabled(True)
                date_run.setDisabled(True)
                date_change.setDisabled(False)

                self.date = date_input.text()
                self.searchGraph = GraphWindow(
                    sm.getPlotData(self.ticker, self.date[:8] + '01', sm.getMaxDate(self.date)))  # Plot zoomed in graph
                grid.addWidget(self.searchGraph, 1, 1)  # Add to layout

        def change_date():  # Change date for zoom
            date_input.clear()
            self.date = ""

            date_input.setDisabled(False)  # Allow user to change input
            date_run.setDisabled(False)
            date_change.setDisabled(True)

            self.searchGraph.close()  # Close displayed graph

        def showDialog():  # Display Error on Invalid Input
            msg = qtw.QMessageBox()
            msg.setIcon(qtw.QMessageBox.Information)

            msg.setText("Invalid Input. Please Try Again")
            msg.setWindowTitle("Error")
            msg.setStandardButtons(qtw.QMessageBox.Ok)
            msg.exec_()


# Main Function
if __name__ == "__main__":
    app = qtw.QApplication([])

    widget = MainWidget()
    widget.setFixedHeight(750)
    widget.setFixedWidth(1800)
    widget.show()  # Display MainWidget

    sys.exit(app.exec_())  # Execute PyQt Application
