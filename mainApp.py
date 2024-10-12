from PyQt5.QtWidgets import QApplication
import numpy as np
import sys
from examples import Example4
import skgstat as skg

class MainApp(Example4):
    def __init__(self):
        super().__init__()

        self.tab5 = self.createTab('Ex5')
        self.ax51 = self.createAxes(111, 'plot 1', 'x', 'y', True, self.tabAtr('Ex5Figure'))



if __name__ == "__main__":
    app = QApplication(sys.argv)

    with open("darkTheme.qss", "r") as f:
        style = f.read()
        app.setStyleSheet(style)

    window = MainApp()
    window.show()
    sys.exit(app.exec_())