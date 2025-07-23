from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QDialog, QFormLayout, QLabel, QDateEdit, QComboBox, QLineEdit, QMessageBox
from PyQt6.QtCore import QDate
from database import connect

class FuelManagementWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Správa tankování")
        self.setGeometry(200, 200, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        # Použití stejného stylu jako v hlavní aplikaci
        self.setStyleSheet("""
            * {
                font-family: 'Inter', 'Roboto', sans-serif;
                color: #2C3E50;
            }

            QWidget {
                background: #F2F2F2;
                border: 1px solid rgba(0, 0, 0, 0.1);
            }

            QPushButton {
                background-color: #6C85A3;
                color: white;
                font-size: 16px;
                padding: 12px;
                border-radius: 18px;
                border: none;
            }

            QPushButton:hover {
                background-color: #5A7393;
            }

            QTableWidget {
                background-color: white;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                gridline-color: #E0E0E0;
            }

            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #E0E0E0;
            }

            QTableWidget::item:selected {
                background-color: #6C85A3;
                color: white;
            }

            QHeaderView::section {
                background-color: #6C85A3;
                color: white;
                padding: 10px;
                border: none;
                font-weight: bold;
            }

            QLabel {
                background: transparent;
                border: none;
                color: #2C3E50;
                font-size: 14px;
            }

            QComboBox, QLineEdit, QDateEdit {
                background-color: white;
                border: 2px solid #E0E0E0;
                border-radius: 8px;
                padding: 8px;
                color: #2C3E50;
            }

            QComboBox:focus, QLineEdit:focus, QDateEdit:focus {
                border-color: #6C85A3;
            }
        """)

        # Tabulka tankování
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Datum", "Vozidlo", "Množství paliva (litry)"])
        layout.addWidget(self.table)

        self.load_fuel_data()

        # Tlačítka pro správu tankování
        self.add_button = QPushButton("Přidat tankování")
        self.add_button.clicked.connect(self.add_fuel)
        layout.addWidget(self.add_button)

        self.edit_button = QPushButton("Upravit tankování")
        self.edit_button.clicked.connect(self.edit_fuel)
        layout.addWidget(self.edit_button)

        self.delete_button = QPushButton("Smazat tankování")
        self.delete_button.clicked.connect(self.delete_fuel)
        layout.addWidget(self.delete_button)

        central_widget.setLayout(layout)

    def add_fuel(self):
        """Otevře formulář pro přidání tankování."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Nové tankování")
        layout = QFormLayout()

        date_input = QDateEdit()
        date_input.setCalendarPopup(True)
        date_input.setDate(QDate.currentDate())
        layout.addRow(QLabel("Datum:"), date_input)

        vehicle_box = QComboBox()
        self.load_vehicles(vehicle_box)
        layout.addRow(QLabel("Vozidlo:"), vehicle_box)

        fuel_input = QLineEdit()
        layout.addRow(QLabel("Množství paliva (litry):"), fuel_input)

        save_button = QPushButton("Uložit tankování")
        layout.addWidget(save_button)

        def save_fuel():
            """Uloží tankování do databáze."""
            conn = connect()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO fuel_tankings (date, vehicle, fuel_amount) VALUES (?, ?, ?)
            """, (date_input.date().toString("dd.MM.yyyy"), vehicle_box.currentText(), fuel_input.text()))
            conn.commit()
            conn.close()

            self.load_fuel_data()
            QMessageBox.information(self, "Úspěch", "Tankování bylo úspěšně přidáno!")
            dialog.accept()

        save_button.clicked.connect(save_fuel)
        dialog.setLayout(layout)
        dialog.exec()

    def load_fuel_data(self):
        """Načte seznam tankování z databáze a zobrazí ho v tabulce."""
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT date, vehicle, fuel_amount FROM fuel_tankings")
        rows = cursor.fetchall()
        conn.close()

        self.table.setRowCount(len(rows))
        for row_idx, row in enumerate(rows):
            for col_idx, value in enumerate(row):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

    def edit_fuel(self):
        """Otevře formulář pro úpravu tankování."""
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Chyba", "Nebyl vybrán žádný záznam!")
            return

        fuel_data = [self.table.item(selected_row, col).text() for col in range(self.table.columnCount())]

        dialog = QDialog(self)
        dialog.setWindowTitle("Upravit tankování")
        layout = QFormLayout()

        date_input = QDateEdit()
        date_input.setCalendarPopup(True)
        date_input.setDate(QDate.fromString(fuel_data[0], "dd.MM.yyyy"))
        layout.addRow(QLabel("Datum:"), date_input)

        vehicle_box = QComboBox()
        self.load_vehicles(vehicle_box)
        vehicle_box.setCurrentText(fuel_data[1])
        layout.addRow(QLabel("Vozidlo:"), vehicle_box)

        fuel_input = QLineEdit(fuel_data[2])
        layout.addRow(QLabel("Množství paliva (litry):"), fuel_input)

        save_button = QPushButton("Uložit změny")
        layout.addWidget(save_button)

        def save_changes():
            """Uloží změny tankování."""
            conn = connect()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE fuel_tankings SET date=?, vehicle=?, fuel_amount=? WHERE date=? AND vehicle=? AND fuel_amount=?
            """, (date_input.date().toString("dd.MM.yyyy"), vehicle_box.currentText(), fuel_input.text(), fuel_data[0], fuel_data[1], fuel_data[2]))
            conn.commit()
            conn.close()

            self.load_fuel_data()
            QMessageBox.information(self, "Úspěch", "Tankování bylo úspěšně upraveno!")
            dialog.accept()

        save_button.clicked.connect(save_changes)
        dialog.setLayout(layout)
        dialog.exec()

    def delete_fuel(self):
        """Smaže vybrané tankování."""
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Chyba", "Nebyl vybrán žádný záznam!")
            return

        fuel_data = [self.table.item(selected_row, col).text() for col in range(self.table.columnCount())]

       
        confirm = QMessageBox.question(self, "Potvrzení", f"Opravdu chceš smazat tankování ze dne {fuel_data[0]}?",
                               QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)


        
        if confirm == QMessageBox.StandardButton.Yes:

            conn = connect()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM fuel_tankings WHERE date=? AND vehicle=? AND fuel_amount=?", (fuel_data[0], fuel_data[1], fuel_data[2]))
            conn.commit()
            conn.close()

            self.load_fuel_data()
            QMessageBox.information(self, "Úspěch", f"Tankování dne {fuel_data[0]} bylo smazáno!")

    def load_vehicles(self, combo_box):
        """Načte seznam vozidel z databáze do ComboBoxu."""
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT registration FROM cars")
        vehicles = cursor.fetchall()
        conn.close()

        combo_box.addItems([vehicle[0] for vehicle in vehicles])
