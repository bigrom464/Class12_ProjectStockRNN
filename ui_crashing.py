from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from PyQt5 import QtCore as qtc, QtGui as qtg, QtWidgets as qtw
import stock_model
import sys
import matplotlib
matplotlib.use('Qt5Agg')

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class GraphWindow(qtw.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(GraphWindow, self).__init__(*args, **kwargs)

        sc = MplCanvas(self, width=5, height=4, dpi=100)
        # sc.plot(plotpoints, label="Close Price History")
        sc.axes.plot([0, 1, 2, 3, 4], [10, 1, 20, 3, 40])
        toolbar = NavigationToolbar(sc, self)

        layout = qtw.QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(sc)

        widget = qtw.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.show()


class InputWindow(qtw.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(InputWindow, self).__init__(*args, **kwargs)

        box = qtw.QVBoxLayout()
        box.addSpacerItem(qtw.QSpacerItem(80, 80))

        label = qtw.QLabel(args[0])
        label.setFont(qtg.QFont('Calibri', 14))
        box.addWidget(label)

        inp = qtw.QLineEdit(placeholderText=args[1])
        inp.setMinimumHeight(40)
        box.addWidget(inp)

        actions = qtw.QHBoxLayout()
        run = qtw.QPushButton(
            args[2], clicked=lambda: run_action())
        run.setMinimumHeight(40)
        change = qtw.QPushButton(
            "Change", clicked=lambda: change_action())
        change.setMinimumHeight(40)
        change.setDisabled(True)

        actions.addWidget(run)
        actions.addWidget(change)
        box.addLayout(actions)

        box.addSpacerItem(qtw.QSpacerItem(80, 80))
        box.insertStretch(-1, 1)

        def run_action():
            if input.text() == "":
                showDialog()
            else:
                inp.setDisabled(True)
                run.setDisabled(True)
                change.setDisabled(False)

                # TODO: Integrate Code
                # self.graph1 = GraphWindow()
                # grid.addWidget(self.graph1, 1, 0)

        def change_action():
            inp.setDisabled(False)
            inp.clear()
            run.setDisabled(False)
            change.setDisabled(True)

            self.graph1.close()

        def showDialog():
            dig = qtw.QMessageBox()
            dig.setIcon(qtw.QMessageBox.Information)

            dig.setText("Invalid Input. Please Try Again")
            dig.setWindowTitle("Error")
            dig.setStandardButtons(qtw.QMessageBox.Ok)
            dig.exec_()


class MainWidget(qtw.QWidget):
    def __init__(self):
        super().__init__()

        grid = qtw.QGridLayout()

        # Create Ticker Input Box
        ticker_box = qtw.QVBoxLayout()
        ticker_box.addSpacerItem(qtw.QSpacerItem(80, 80))

        label = qtw.QLabel("Stock Ticker")
        label.setFont(qtg.QFont('Calibri', 14))
        ticker_box.addWidget(label)

        ticker_input = qtw.QLineEdit(
            placeholderText='Enter Stock Ticker...',
        )
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
        # ticker_box = InputWindow(
        # 'Stock Ticker', 'Enter Stock Ticker...', 'Run')
        grid.addLayout(ticker_box, 0, 0)

        # Create Date Search Input Box
        date_box = qtw.QVBoxLayout()
        date_box.addSpacerItem(qtw.QSpacerItem(80, 80))

        label = qtw.QLabel("Fetch/Predict Stock Value")
        label.setFont(qtg.QFont('Calibri', 14))
        date_box.addWidget(label)
        ticker='TSLA'
        date_input = qtw.QLineEdit(
            # TODO Get IPO Date
            placeholderText='mm/dd/yyyy after {}'.format(stock_model.get_ipo(ticker)),
            # qtc.QDate.currentDate().toString(qtc.Qt.ISODate)
        )
        date_input.setValidator(qtg.QRegExpValidator(
            qtc.QRegExp('\d{2}\/\d{2}\/\d{4}')))
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

        self.setLayout(grid)
        self.setWindowTitle(
            "Foresight | A Python Stock Prediction Application")

        self.graph1 = self.graph2 = None

        def run_ticker():
            if ticker_input.text() == "":
                showdialog()
            else:
                ticker_input.setDisabled(True)
                ticker_run.setDisabled(True)
                ticker_change.setDisabled(False)
                ticker=ticker_input.text()
                # TODO: Integrate Code
                self.graph1 = GraphWindow()
                grid.addWidget(self.graph1.canvas, 1, 0)

        def change_ticker():
            ticker_input.setDisabled(False)
            ticker_input.clear()
            ticker_run.setDisabled(False)
            ticker_change.setDisabled(True)

            self.graph1.close()

        def run_date():
            if date_input.text() == "":
                showdialog()
            else:
                date_input.setDisabled(True)
                date_run.setDisabled(True)
                date_change.setDisabled(False)

                # TODO: Integrate Code
                self.graph2 = GraphWindow()  # TODO: pass dataframe
                grid.addWidget(self.graph2, 1, 1)

        def change_date():
            date_input.setDisabled(False)
            date_input.clear()
            date_run.setDisabled(False)
            date_change.setDisabled(True)

            self.graph2.close()

        def showdialog():
            msg = qtw.QMessageBox()
            msg.setIcon(qtw.QMessageBox.Information)

            msg.setText("Invalid Input. Please Try Again")
            msg.setWindowTitle("Error")
            msg.setStandardButtons(qtw.QMessageBox.Ok)
            msg.exec_()


if __name__ == "__main__":
    app = qtw.QApplication([])

    widget = MainWidget()
    widget.setFixedHeight(750)
    widget.setFixedWidth(1250)
    widget.show()

    sys.exit(app.exec_())
