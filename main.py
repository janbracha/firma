import sys

from PyQt6.QtWidgets import QApplication

from database import create_tables
from gui import InvoiceApp

create_tables()  # musí být zavoláno při startu programu

app = QApplication(sys.argv)
window = InvoiceApp()
window.show()
sys.exit(app.exec())
