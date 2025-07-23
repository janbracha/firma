from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTableWidget, QPushButton, QTableWidgetItem, QDialog, QFormLayout, QLabel, QLineEdit, QMessageBox
from database import connect

class DriverManagementWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Správa řidičů")
        self.setGeometry(200, 200, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        # Tabulka řidičů
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Titul", "Jméno", "Příjmení", "Funkce"])
        layout.addWidget(self.table)

        self.load_drivers()

        # Tlačítka pro správu řidičů
        self.add_button = QPushButton("Přidat řidiče")
        self.add_button.clicked.connect(self.add_driver)
        layout.addWidget(self.add_button)

        self.edit_button = QPushButton("Upravit řidiče")
        self.edit_button.clicked.connect(self.edit_driver)
        layout.addWidget(self.edit_button)

        self.delete_button = QPushButton("Smazat řidiče")
        self.delete_button.clicked.connect(self.delete_driver)
        layout.addWidget(self.delete_button)

        central_widget.setLayout(layout)

    def load_drivers(self):
        """Načte řidiče z databáze a zobrazí v tabulce."""
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT title, first_name, last_name, role FROM drivers")
        rows = cursor.fetchall()
        conn.close()

        self.table.setRowCount(len(rows))
        for row_idx, row in enumerate(rows):
            for col_idx, value in enumerate(row):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

    def add_driver(self):
        """Otevře formulář pro přidání řidiče."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Nový řidič")
        layout = QFormLayout()

        title_input = QLineEdit()
        layout.addRow(QLabel("Titul:"), title_input)

        first_name_input = QLineEdit()
        layout.addRow(QLabel("Jméno:"), first_name_input)

        last_name_input = QLineEdit()
        layout.addRow(QLabel("Příjmení:"), last_name_input)

        role_input = QLineEdit()
        layout.addRow(QLabel("Funkce:"), role_input)

        save_button = QPushButton("Uložit řidiče")
        layout.addWidget(save_button)

        def save_driver():
            """Uloží řidiče do databáze."""
            conn = connect()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO drivers (title, first_name, last_name, role) VALUES (?, ?, ?, ?)
            """, (title_input.text(), first_name_input.text(), last_name_input.text(), role_input.text()))
            conn.commit()
            conn.close()

            self.load_drivers()
            QMessageBox.information(self, "Úspěch", "Řidič byl úspěšně přidán!")
            dialog.accept()

        save_button.clicked.connect(save_driver)
        dialog.setLayout(layout)
        dialog.exec()

    def edit_driver(self):
        """Otevře formulář pro úpravu řidiče."""
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Chyba", "Nebyl vybrán žádný řidič!")
            return

        driver_data = [self.table.item(selected_row, col).text() for col in range(self.table.columnCount())]

        dialog = QDialog(self)
        dialog.setWindowTitle("Upravit řidiče")
        layout = QFormLayout()

        title_input = QLineEdit(driver_data[0])
        layout.addRow(QLabel("Titul:"), title_input)

        first_name_input = QLineEdit(driver_data[1])
        layout.addRow(QLabel("Jméno:"), first_name_input)

        last_name_input = QLineEdit(driver_data[2])
        layout.addRow(QLabel("Příjmení:"), last_name_input)

        role_input = QLineEdit(driver_data[3])
        layout.addRow(QLabel("Funkce:"), role_input)

        save_button = QPushButton("Uložit změny")
        layout.addWidget(save_button)

        def save_changes():
            """Uloží změny řidiče."""
            conn = connect()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE drivers SET title=?, first_name=?, last_name=?, role=? WHERE first_name=? AND last_name=?
            """, (title_input.text(), first_name_input.text(), last_name_input.text(), role_input.text(), driver_data[1], driver_data[2]))
            conn.commit()
            conn.close()

            self.load_drivers()
            QMessageBox.information(self, "Úspěch", "Řidič byl úspěšně upraven!")
            dialog.accept()

        save_button.clicked.connect(save_changes)
        dialog.setLayout(layout)
        dialog.exec()

    def delete_driver(self):
        """Smaže řidiče."""
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Chyba", "Nebyl vybrán žádný řidič!")
            return

        driver_name = self.table.item(selected_row, 1).text()
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM drivers WHERE first_name=?", (driver_name,))
        conn.commit()
        conn.close()

        self.load_drivers()
        QMessageBox.information(self, "Úspěch", f"Řidič {driver_name} byl smazán!")
