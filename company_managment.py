from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTableWidget, QPushButton, QTableWidgetItem, \
    QDialog, QFormLayout, QLabel, QLineEdit, QMessageBox

from companies import fetch_companies, add_company, update_company
from database import connect


class CompanyManagementWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Správa firem")
        self.setGeometry(200, 200, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        # Tabulka firem
        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(["Název firmy", "IČO", "DIČ", "Bankovní účet", "Kontakt", "Adresa"])
        layout.addWidget(self.table)

        self.load_companies()

        # Tlačítka pro správu firem
        self.add_button = QPushButton("Přidat firmu")
        self.add_button.clicked.connect(self.add_company)
        layout.addWidget(self.add_button)

        self.edit_button = QPushButton("Upravit firmu")
        self.edit_button.clicked.connect(self.edit_company)
        layout.addWidget(self.edit_button)

        self.delete_button = QPushButton("Smazat firmu")
        self.delete_button.clicked.connect(self.delete_company)
        layout.addWidget(self.delete_button)

        central_widget.setLayout(layout)
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
                box-shadow: 3px 3px 8px rgba(0, 0, 0, 0.15);
                transition: background-color 0.2s ease-in-out;
            }

            QPushButton:hover {
                background-color: #5A7393;
            }
        """)

    def load_companies(self):
        """Načte firmy do tabulky."""
        rows = fetch_companies()
        self.table.setRowCount(len(rows))
        for row_idx, row in enumerate(rows):
            for col_idx, value in enumerate(row):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

    def add_company(self):
        """Otevře dialog pro přidání nové firmy."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Nová firma")
        layout = QFormLayout()

        name_input = QLineEdit()
        layout.addRow(QLabel("Název firmy:"), name_input)

        ico_input = QLineEdit()
        layout.addRow(QLabel("IČO:"), ico_input)

        dic_input = QLineEdit()
        layout.addRow(QLabel("DIČ:"), dic_input)

        bank_input = QLineEdit()
        layout.addRow(QLabel("Bankovní účet:"), bank_input)

        contact_input = QLineEdit()
        layout.addRow(QLabel("Kontakt:"), contact_input)

        address_input = QLineEdit()
        layout.addRow(QLabel("Adresa:"), address_input)

        save_button = QPushButton("Uložit firmu")
        layout.addWidget(save_button)

        def save_company():
            add_company(name_input.text(), ico_input.text(), dic_input.text(), bank_input.text(), contact_input.text(), address_input.text())
            self.load_companies()
            QMessageBox.information(self, "Úspěch", f"Firma '{name_input.text()}' byla přidána!")
            dialog.accept()

        save_button.clicked.connect(save_company)
        dialog.setLayout(layout)
        dialog.exec()

    def edit_company(self):
        """Otevře dialog pro úpravu vybrané firmy."""
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Chyba", "Nebyla vybrána žádná firma!")
            return

        company_name = self.table.item(selected_row, 0).text()
        company_data = [self.table.item(selected_row, col).text() for col in range(self.table.columnCount())]

        dialog = QDialog(self)
        dialog.setWindowTitle("Upravit firmu")
        layout = QFormLayout()

        name_input = QLineEdit(company_data[0])
        layout.addRow(QLabel("Název firmy:"), name_input)

        ico_input = QLineEdit(company_data[1])
        layout.addRow(QLabel("IČO:"), ico_input)

        dic_input = QLineEdit(company_data[2])
        layout.addRow(QLabel("DIČ:"), dic_input)

        bank_input = QLineEdit(company_data[3])
        layout.addRow(QLabel("Bankovní účet:"), bank_input)

        contact_input = QLineEdit(company_data[4])
        layout.addRow(QLabel("Kontakt:"), contact_input)

        address_input = QLineEdit(company_data[5])
        layout.addRow(QLabel("Adresa:"), address_input)

        save_button = QPushButton("Uložit změny")
        layout.addWidget(save_button)

        def save_changes():
            updated_data = (
                name_input.text(), ico_input.text(), dic_input.text(),
                bank_input.text(), contact_input.text(), address_input.text()
            )
            update_company(company_name, updated_data)
            self.load_companies()
            QMessageBox.information(self, "Úspěch", f"Firma '{name_input.text()}' byla upravena!")
            dialog.accept()

        save_button.clicked.connect(save_changes)
        dialog.setLayout(layout)
        dialog.exec()

    def delete_company(self):
        """Smaže vybranou firmu po potvrzení uživatelem."""
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Chyba", "Nebyla vybrána žádná firma!")
            return

        company_name = self.table.item(selected_row, 0).text()

        confirmation = QMessageBox.question(
            self, "Potvrzení smazání",
            f"Opravdu chcete smazat firmu '{company_name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirmation == QMessageBox.StandardButton.Yes:
            conn = connect()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM companies WHERE name=?", (company_name,))
            conn.commit()
            conn.close()
            self.load_companies()
            QMessageBox.information(self, "Úspěch", f"Firma '{company_name}' byla smazána!")


    @staticmethod
    def fetch_companies():
        """Načte všechny firmy z databáze správně jako seznam tuple."""
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT name, ico, dic, bank, contact, address FROM companies")
        data = cursor.fetchall()  # Vrací seznam tuple [(název, ico, dic, bank, contact, adresa), ...]
        conn.close()
        return data

    @staticmethod
    def fetch_company_names():
        """Načte názvy firem z databáze pro výběr v rozbalovacím seznamu."""
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM companies")
        data = [row[0] for row in cursor.fetchall()]  # Vrací seznam názvů firem
        conn.close()
        return data



