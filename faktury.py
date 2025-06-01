import sys
import sqlite3
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QTableWidget,
    QTableWidgetItem,
    QDialog,
    QFormLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QMessageBox,
    QDateEdit)
from PyQt6.QtCore import QDate

class InvoiceApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Správa faktur")
        self.setGeometry(200, 200, 800, 600)

        # Připojení k databázi
        self.conn = sqlite3.connect("invoices.db")
        self.cursor = self.conn.cursor()
        self.create_tables()

        # Hlavní widget a rozložení
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        # Tabulka faktur
        self.table = QTableWidget(0, 10)
        self.table.setHorizontalHeaderLabels([
            "ID", "Typ", "Příjemce", "Výdejce", "Datum vyst.",
            "Datum plnění", "Datum splat.", "Částka bez DPH", "DPH", "Celkem"
        ])
        layout.addWidget(self.table)

        # Tlačítka pro akce
        self.add_button = QPushButton("Přidat fakturu")
        self.add_button.clicked.connect(self.add_invoice)

        self.delete_button = QPushButton("Smazat fakturu")
        self.delete_button.clicked.connect(self.delete_invoice)

        self.edit_button = QPushButton("Upravit fakturu")
        self.edit_button.clicked.connect(self.edit_invoice)

        self.manage_companies_button = QPushButton("Správa firem")
        self.manage_companies_button.clicked.connect(self.manage_companies)

        layout.addWidget(self.add_button)
        layout.addWidget(self.delete_button)
        layout.addWidget(self.edit_button)
        layout.addWidget(self.manage_companies_button)

        central_widget.setLayout(layout)

        # Načtení faktur do tabulky
        self.load_invoices()

    def create_tables(self):
        """Vytvoří tabulky v databázi, pokud ještě neexistují."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS invoices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT,
                recipient TEXT,
                issuer TEXT,
                issue_date TEXT,
                tax_date TEXT,
                due_date TEXT,
                amount_no_tax REAL,
                tax REAL,
                total REAL
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS companies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                ico TEXT,
                address TEXT
            )
        """)

        self.conn.commit()

    def load_invoices(self):
        """Načte faktury z databáze a zobrazí je v tabulce."""
        self.cursor.execute("SELECT * FROM invoices")
        rows = self.cursor.fetchall()
        self.table.setRowCount(len(rows))
        for row_idx, row in enumerate(rows):
            for col_idx, value in enumerate(row):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

    def load_companies(self, combo_box):
        """Načte firmy z databáze a zobrazí je v ComboBoxu."""
        self.cursor.execute("SELECT name FROM companies")
        companies = self.cursor.fetchall()
        combo_box.clear()
        for company in companies:
            combo_box.addItem(company[0])

    def manage_companies(self):
        """Otevře okno pro správu firem."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Správa firem")
        layout = QVBoxLayout()

        # Tabulka firem
        self.company_table = QTableWidget(0, 3)
        self.company_table.setHorizontalHeaderLabels(["Název", "IČO", "Adresa"])
        layout.addWidget(self.company_table)
        self.load_company_list()

        form_layout = QFormLayout()
        name_input = QLineEdit()
        form_layout.addRow(QLabel("Název firmy:"), name_input)

        ico_input = QLineEdit()
        form_layout.addRow(QLabel("IČO:"), ico_input)

        address_input = QLineEdit()
        form_layout.addRow(QLabel("Adresa:"), address_input)

        save_button = QPushButton("Přidat firmu")
        save_button.clicked.connect(
            lambda: self.add_company(
                name_input.text(),
                ico_input.text(),
                address_input.text()))
        form_layout.addWidget(save_button)

        layout.addLayout(form_layout)
        dialog.setLayout(layout)
        dialog.exec()

    def load_company_list(self):
        """Načte seznam firem a zobrazí je v tabulce."""
        self.cursor.execute("SELECT name, ico, address FROM companies")
        rows = self.cursor.fetchall()
        self.company_table.setRowCount(len(rows))
        for row_idx, row in enumerate(rows):
            for col_idx, value in enumerate(row):
                self.company_table.setItem(
                    row_idx, col_idx, QTableWidgetItem(
                        str(value)))

    def add_company(self, name, ico, address):
        """Uloží novou firmu do databáze."""
        if name:
            self.cursor.execute(
                "INSERT INTO companies (name, ico, address) VALUES (?, ?, ?)",
                (name,
                 ico,
                 address))
            self.conn.commit()
            self.load_company_list()

    def delete_invoice(self):
        """Smaže vybranou fakturu z databáze."""
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            invoice_id = self.table.item(selected_row, 0).text()
            self.cursor.execute("DELETE FROM invoices WHERE id=?", (invoice_id,))
            self.conn.commit()
            self.load_invoices()

####novy kod
    def delete_invoice(self):
        """Smaže vybranou fakturu z databáze po potvrzení uživatelem."""
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            invoice_id = self.table.item(selected_row, 0).text()

            # Zobrazení potvrzovacího dialogu
            confirmation = QMessageBox.question(
                self, "Potvrzení smazání", 
                f"Opravdu chcete smazat fakturu ID {invoice_id}?", 
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            # Pokud uživatel klikne na "Ano", faktura se smaže
            if confirmation == QMessageBox.StandardButton.Yes:
                self.cursor.execute("DELETE FROM invoices WHERE id=?", (invoice_id,))
                self.conn.commit()
                self.load_invoices()
                print(f"Faktura ID {invoice_id} byla úspěšně smazána.")


##### konec noveho kkodu 
    def add_invoice(self):
        """Otevře formulář pro přidání nové faktury a uloží ji do databáze."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Nová faktura")
        layout = QFormLayout()

        # Formulářové prvky
        type_box = QComboBox()
        type_box.addItems(["Přijatá", "Vydaná"])
        layout.addRow(QLabel("Typ faktury:"), type_box)

        recipient_box = QComboBox()
        self.load_companies(recipient_box)
        layout.addRow(QLabel("Příjemce:"), recipient_box)

        issuer_box = QComboBox()
        self.load_companies(issuer_box)
        layout.addRow(QLabel("Výdejce:"), issuer_box)

        issue_date = QDateEdit()
        issue_date.setCalendarPopup(True)
        issue_date.setDate(QDate.currentDate())
        layout.addRow(QLabel("Datum vystavení:"), issue_date)

        tax_date = QDateEdit()
        tax_date.setCalendarPopup(True)
        tax_date.setDate(QDate.currentDate())
        layout.addRow(QLabel("Datum plnění:"), tax_date)

        due_date = QDateEdit()
        due_date.setCalendarPopup(True)
        due_date.setDate(QDate.currentDate())
        layout.addRow(QLabel("Datum splatnosti:"), due_date)

        amount_input = QLineEdit()
        layout.addRow(QLabel("Částka bez DPH:"), amount_input)

        tax_input = QLineEdit()
        layout.addRow(QLabel("Částka DPH:"), tax_input)

        total_input = QLineEdit()
        layout.addRow(QLabel("Celková částka:"), total_input)

        # Funkce pro uložení faktury
        def save_invoice():
            self.cursor.execute(
                """
                INSERT INTO invoices (type, recipient, issuer, issue_date, tax_date, due_date, amount_no_tax, tax, total)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (type_box.currentText(),
                 recipient_box.currentText(),
                 issuer_box.currentText(),
                 issue_date.date().toString("yyyy-MM-dd"),
                 tax_date.date().toString("yyyy-MM-dd"),
                 due_date.date().toString("yyyy-MM-dd"),
                 float(
                    amount_input.text()),
                    float(
                    tax_input.text()),
                    float(
                    total_input.text())))
            self.conn.commit()
            self.load_invoices()  # Aktualizace tabulky
            dialog.accept()  # Zavření okna

        # Přidání tlačítka pro uložení faktury
        save_button = QPushButton("Uložit fakturu")
        save_button.clicked.connect(save_invoice)
        layout.addRow(save_button)

        dialog.setLayout(layout)
        dialog.exec()

    def edit_invoice(self):
        """Umožní upravit vybranou fakturu."""
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            invoice_id = self.table.item(selected_row, 0).text()

            # Načtení aktuálních dat faktury
            self.cursor.execute("SELECT * FROM invoices WHERE id=?", (invoice_id,))
            invoice_data = self.cursor.fetchone()
            if not invoice_data:
                return

            # Vytvoření dialogového okna pro úpravu faktury
            dialog = QDialog(self)
            dialog.setWindowTitle("Upravit fakturu")
            layout = QFormLayout()

            type_box = QComboBox()
            type_box.addItems(["Přijatá", "Vydaná"])
            type_box.setCurrentText(invoice_data[1])
            layout.addRow(QLabel("Typ faktury:"), type_box)

            recipient_input = QLineEdit(invoice_data[2])
            layout.addRow(QLabel("Příjemce:"), recipient_input)

            issuer_input = QLineEdit(invoice_data[3])
            layout.addRow(QLabel("Výdejce:"), issuer_input)

            issue_date = QDateEdit()
            issue_date.setCalendarPopup(True)
            issue_date.setDate(QDate.fromString(invoice_data[4], "yyyy-MM-dd"))
            layout.addRow(QLabel("Datum vystavení:"), issue_date)

            tax_date = QDateEdit()
            tax_date.setCalendarPopup(True)
            tax_date.setDate(QDate.fromString(invoice_data[5], "yyyy-MM-dd"))
            layout.addRow(QLabel("Datum plnění:"), tax_date)

            due_date = QDateEdit()
            due_date.setCalendarPopup(True)
            due_date.setDate(QDate.fromString(invoice_data[6], "yyyy-MM-dd"))
            layout.addRow(QLabel("Datum splatnosti:"), due_date)

            amount_input = QLineEdit(str(invoice_data[7]))
            layout.addRow(QLabel("Částka bez DPH:"), amount_input)

            tax_input = QLineEdit(str(invoice_data[8]))
            layout.addRow(QLabel("Částka DPH:"), tax_input)

            total_input = QLineEdit(str(invoice_data[9]))
            layout.addRow(QLabel("Celková částka:"), total_input)

            # Funkce pro uložení změn
            def save_changes():
                self.cursor.execute("""
                    UPDATE invoices 
                    SET type=?, recipient=?, issuer=?, issue_date=?, tax_date=?, due_date=?, amount_no_tax=?, tax=?, total=? 
                    WHERE id=?
                """, (
                    type_box.currentText(), recipient_input.text(), issuer_input.text(),
                    issue_date.date().toString("yyyy-MM-dd"), tax_date.date().toString("yyyy-MM-dd"), due_date.date().toString("yyyy-MM-dd"),
                    float(amount_input.text()), float(tax_input.text()), float(total_input.text()), invoice_id
                ))
                self.conn.commit()
                self.load_invoices()  # Aktualizace tabulky
                dialog.accept()  # Zavření dialogu

            # Přidání tlačítka pro uložení změn
            save_button = QPushButton("Uložit změny")
            save_button.clicked.connect(save_changes)
            layout.addRow(save_button)

            dialog.setLayout(layout)
            dialog.exec()


# Spuštění aplikace
app = QApplication(sys.argv)
window = InvoiceApp()
window.show()
sys.exit(app.exec())
