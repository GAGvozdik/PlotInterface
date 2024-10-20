# https://scikit-gstat.readthedocs.io/en/latest/install.html
import skgstat as skg
from .example1 import Example1
from .example2 import Example2
from .example3 import Example3
from .example4 import Example4
from .example5 import Example5
from .example6 import Example6
from .example7 import Example7
from PyQt5.QtWidgets import QApplication
import sys


class AllExamples(Example7, Example6, Example5, Example4, Example3, Example2, Example1):
    def __init__(self):
        super().__init__()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    with open("styles/darkTheme.qss", "r") as f:
        style = f.read()
        app.setStyleSheet(style)

    window = AllExamples()
    window.show()
    sys.exit(app.exec_())



