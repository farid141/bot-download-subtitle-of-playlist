from PySide6.QtWidgets import QApplication
from downsub_gui.DownsubGUI import DownsubGUI
import sys

app = QApplication(sys.argv)

window = DownsubGUI()

window.show()

app.exec()
