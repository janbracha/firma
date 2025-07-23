from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTableWidget, QPushButton, QTableWidgetItem, QDialog, QFormLayout, QLabel, QLineEdit, QMessageBox
from database import connect

class VehicleManagementWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Správa vozidel")
        self.setGeometry(200, 200, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        # Tabulka vozidel
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Registrační značka", "Typ vozidla", "Vlastník", "Spotřeba (l/100 km)"])
        layout.addWidget(self.table)

        self.load_vehicles()

        # Tlačítka pro správu vozidel
        self.add_button = QPushButton("Přidat vozidlo")
        self.add_button.clicked.connect(self.add_vehicle)
        layout.addWidget(self.add_button)

        self.edit_button = QPushButton("Upravit vozidlo")
        self.edit_button.clicked.connect(self.edit_vehicle)
        layout.addWidget(self.edit_button)

        self.delete_button = QPushButton("Smazat vozidlo")
        self.delete_button.clicked.connect(self.delete_vehicle)
        layout.addWidget(self.delete_button)

        central_widget.setLayout(layout)

    def load_vehicles(self):
        """Načte vozidla z databáze a zobrazí v tabulce."""
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT registration, type, owner, consumption FROM cars")
        rows = cursor.fetchall()
        conn.close()

        self.table.setRowCount(len(rows))
        for row_idx, row in enumerate(rows):
            for col_idx, value in enumerate(row):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

    def add_vehicle(self):
        """Otevře formulář pro přidání vozidla."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Nové vozidlo")
        layout = QFormLayout()

        registration_input = QLineEdit()
        layout.addRow(QLabel("Registrační značka:"), registration_input)

        type_input = QLineEdit()
        layout.addRow(QLabel("Typ vozidla:"), type_input)

        owner_input = QLineEdit()
        layout.addRow(QLabel("Vlastník:"), owner_input)

        consumption_input = QLineEdit()
        layout.addRow(QLabel("Spotřeba (l/100 km):"), consumption_input)

        save_button = QPushButton("Uložit vozidlo")
        layout.addWidget(save_button)

        def save_vehicle():
            """Uloží vozidlo do databáze."""
            conn = connect()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO cars (registration, type, owner, consumption) VALUES (?, ?, ?, ?)
            """, (registration_input.text(), type_input.text(), owner_input.text(), consumption_input.text()))
            conn.commit()
            conn.close()

            self.load_vehicles()
            QMessageBox.information(self, "Úspěch", "Vozidlo bylo úspěšně přidáno!")
            dialog.accept()

        save_button.clicked.connect(save_vehicle)
        dialog.setLayout(layout)
        dialog.exec()

    def edit_vehicle(self):
        """Otevře formulář pro úpravu vozidla."""
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Chyba", "Nebyl vybrán žádný záznam!")
            return

        vehicle_data = [self.table.item(selected_row, col).text() for col in range(self.table.columnCount())]

        dialog = QDialog(self)
        dialog.setWindowTitle("Upravit vozidlo")
        layout = QFormLayout()

        registration_input = QLineEdit(vehicle_data[0])
        layout.addRow(QLabel("Registrační značka:"), registration_input)

        type_input = QLineEdit(vehicle_data[1])
        layout.addRow(QLabel("Typ vozidla:"), type_input)

        owner_input = QLineEdit(vehicle_data[2])
        layout.addRow(QLabel("Vlastník:"), owner_input)

        consumption_input = QLineEdit(vehicle_data[3])
        layout.addRow(QLabel("Spotřeba (l/100 km):"), consumption_input)

        save_button = QPushButton("Uložit změny")
        layout.addWidget(save_button)

        def save_changes():
            """Uloží změny vozidla."""
            conn = connect()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE cars SET registration=?, type=?, owner=?, consumption=? WHERE registration=?
            """, (registration_input.text(), type_input.text(), owner_input.text(), consumption_input.text(), vehicle_data[0]))
            conn.commit()
            conn.close()

            self.load_vehicles()
            QMessageBox.information(self, "Úspěch", "Vozidlo bylo úspěšně upraveno!")
            dialog.accept()

        save_button.clicked.connect(save_changes)
        dialog.setLayout(layout)
        dialog.exec()

    def delete_vehicle(self):
        """Smaže vozidlo."""
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Chyba", "Nebyl vybrán žádný záznam!")
            return

        vehicle_reg = self.table.item(selected_row, 0).text()
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cars WHERE registration=?", (vehicle_reg,))
        conn.commit()
        conn.close()

        self.load_vehicles()
        QMessageBox.information(self, "Úspěch", f"Vozidlo {vehicle_reg} bylo smazáno!")
