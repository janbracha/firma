from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTableWidget, QPushButton, QTableWidgetItem, QDialog, QFormLayout, QLabel, QLineEdit, QMessageBox
from database import connect

class DestinationManagementWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Zadávání destinací")
        self.setGeometry(200, 200, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        # Tabulka destinací se 5 sloupci
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["Start", "Cíl", "Firma / Adresa", "Vzdálenost (km)", "Poznámka"])
        layout.addWidget(self.table)

        self.load_destinations()

        # Tlačítka pro správu destinací
        self.add_button = QPushButton("Přidat destinaci")
        self.add_button.clicked.connect(self.add_destination)
        layout.addWidget(self.add_button)

        self.edit_button = QPushButton("Upravit destinaci")
        self.edit_button.clicked.connect(self.edit_destination)
        layout.addWidget(self.edit_button)

        self.delete_button = QPushButton("Smazat destinaci")
        self.delete_button.clicked.connect(self.delete_destination)
        layout.addWidget(self.delete_button)

        central_widget.setLayout(layout)

    def load_destinations(self):
        """Načte destinace z databáze a zobrazí v tabulce."""
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT start, destination, company, distance, note FROM destinations")
        rows = cursor.fetchall()
        conn.close()

        self.table.setRowCount(len(rows))
        for row_idx, row in enumerate(rows):
            for col_idx, value in enumerate(row):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

    def add_destination(self):
        """Otevře formulář pro přidání destinace."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Nová destinace")
        layout = QFormLayout()

        start_input = QLineEdit()
        layout.addRow(QLabel("Start:"), start_input)

        destination_input = QLineEdit()
        layout.addRow(QLabel("Cíl:"), destination_input)

        company_input = QLineEdit()
        layout.addRow(QLabel("Firma / Adresa:"), company_input)

        distance_input = QLineEdit()
        layout.addRow(QLabel("Vzdálenost (km):"), distance_input)

        note_input = QLineEdit()
        layout.addRow(QLabel("Poznámka:"), note_input)

        save_button = QPushButton("Uložit destinaci")
        layout.addWidget(save_button)

        def save_destination():
            """Uloží destinaci do databáze."""
            conn = connect()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO destinations (start, destination, company, distance, note) VALUES (?, ?, ?, ?, ?)
            """, (start_input.text(), destination_input.text(), company_input.text(), distance_input.text(), note_input.text()))
            conn.commit()
            conn.close()

            self.load_destinations()
            QMessageBox.information(self, "Úspěch", "Destinace byla úspěšně přidána!")
            dialog.accept()

        save_button.clicked.connect(save_destination)
        dialog.setLayout(layout)
        dialog.exec()

    def edit_destination(self):
        """Otevře formulář pro úpravu destinace."""
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Chyba", "Nebyl vybrán žádný záznam!")
            return

        destination_data = [self.table.item(selected_row, col).text() for col in range(self.table.columnCount())]

        dialog = QDialog(self)
        dialog.setWindowTitle("Upravit destinaci")
        layout = QFormLayout()

        start_input = QLineEdit(destination_data[0])
        layout.addRow(QLabel("Start:"), start_input)

        destination_input = QLineEdit(destination_data[1])
        layout.addRow(QLabel("Cíl:"), destination_input)

        company_input = QLineEdit(destination_data[2])
        layout.addRow(QLabel("Firma / Adresa:"), company_input)

        distance_input = QLineEdit(destination_data[3])
        layout.addRow(QLabel("Vzdálenost (km):"), distance_input)

        note_input = QLineEdit(destination_data[4])
        layout.addRow(QLabel("Poznámka:"), note_input)

        save_button = QPushButton("Uložit změny")
        layout.addWidget(save_button)

        def save_changes():
            """Uloží změny destinace."""
            conn = connect()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE destinations SET start=?, destination=?, company=?, distance=?, note=? WHERE start=? AND destination=?
            """, (start_input.text(), destination_input.text(), company_input.text(), distance_input.text(), note_input.text(), destination_data[0], destination_data[1]))
            conn.commit()
            conn.close()

            self.load_destinations()
            QMessageBox.information(self, "Úspěch", "Destinace byla úspěšně upravena!")
            dialog.accept()

        save_button.clicked.connect(save_changes)
        dialog.setLayout(layout)
        dialog.exec()

    def delete_destination(self):
        """Smaže destinaci."""
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Chyba", "Nebyl vybrán žádný záznam!")
            return

        start_name = self.table.item(selected_row, 0).text()
        destination_name = self.table.item(selected_row, 1).text()

        conn = connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM destinations WHERE start=? AND destination=?", (start_name, destination_name))
        conn.commit()
        conn.close()

        self.load_destinations()
        QMessageBox.information(self, "Úspěch", f"Destinace {start_name} → {destination_name} byla smazána!")
