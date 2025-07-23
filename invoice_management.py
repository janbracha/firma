from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import (
    QDialog, QFormLayout, QLabel, QLineEdit, QComboBox, QDateEdit,
    QMessageBox, QFileDialog
)
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTableWidget, QPushButton, QTableWidgetItem
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, PageBreak

from companies import fetch_company_names
from database import fetch_all_invoices
from invoices import add_invoice
from invoices import update_invoice, delete_invoice


class InvoiceManagementWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Správa faktur")
        self.setGeometry(200, 200, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        # Tabulka faktur
        self.table = QTableWidget(0, 13)
        self.table.setHorizontalHeaderLabels([
            "ID", "Číslo faktury", "Typ", "Příjemce", "Výdejce", "Datum vystavení", 
            "Datum plnění", "Datum splatnosti", "Částka bez DPH", "DPH", "Celkem", "Status", "Poznámka"
        ])
        layout.addWidget(self.table)

        self.load_invoices()

        # Tlačítka pro správu faktur
        self.add_button = QPushButton("Přidat fakturu")
        self.add_button.clicked.connect(self.add_invoice)
        layout.addWidget(self.add_button)

        self.edit_button = QPushButton("Upravit fakturu")
        self.edit_button.clicked.connect(self.edit_invoice)
        layout.addWidget(self.edit_button)

        self.delete_button = QPushButton("Smazat fakturu")
        self.delete_button.clicked.connect(self.delete_invoice)
        layout.addWidget(self.delete_button)

        self.export_button = QPushButton("Exportovat fakturu do PDF")
        self.export_button.clicked.connect(self.export_to_pdf)
        layout.addWidget(self.export_button)

        self.export_all_button = QPushButton("Exportovat všechny faktury do PDF")
        self.export_all_button.clicked.connect(self.export_all_to_pdf)
        layout.addWidget(self.export_all_button)


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

    def load_invoices(self):
        """Načte faktury z databáze a zobrazí je v tabulce."""
        rows = fetch_all_invoices()
        self.table.setRowCount(len(rows))
        for row_idx, row in enumerate(rows):
            for col_idx, value in enumerate(row):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

    def add_invoice(self):
        """Otevře dialogové okno pro přidání faktury a uloží ji do databáze."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Nová faktura")
        layout = QFormLayout()

        invoice_number_input = QLineEdit()
        layout.addRow(QLabel("Číslo faktury:"), invoice_number_input)

        type_box = QComboBox()
        type_box.addItems(["Přijatá", "Vydaná"])
        layout.addRow(QLabel("Typ faktury:"), type_box)

        company_names = fetch_company_names()

        recipient_box = QComboBox()
        recipient_box.addItems(company_names)
        layout.addRow(QLabel("Příjemce:"), recipient_box)

        issuer_box = QComboBox()
        issuer_box.addItems(company_names)
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

        status_box = QComboBox()
        status_box.addItems(["Čeká na platbu", "Zaplaceno", "Stornováno"])
        layout.addRow(QLabel("Status faktury:"), status_box)

        note_input = QLineEdit()
        layout.addRow(QLabel("Poznámka:"), note_input)

        save_button = QPushButton("Uložit fakturu")
        layout.addWidget(save_button)

        def save_invoice():
            """Uloží fakturu do databáze a zobrazí potvrzení."""
            data = (
                invoice_number_input.text(), type_box.currentText(),
                recipient_box.currentText(), issuer_box.currentText(),
                issue_date.date().toString("yyyy-MM-dd"),
                tax_date.date().toString("yyyy-MM-dd"),
                due_date.date().toString("yyyy-MM-dd"),
                float(amount_input.text()), float(tax_input.text()),
                float(total_input.text()), status_box.currentText(), note_input.text()
            )
            add_invoice(data)
            self.load_invoices()
            QMessageBox.information(self, "Úspěch", f"Faktura '{invoice_number_input.text()}' byla úspěšně přidána!")
            dialog.accept()

        save_button.clicked.connect(save_invoice)
        dialog.setLayout(layout)
        dialog.exec()

    def edit_invoice(self):
        """Otevře dialogové okno pro úpravu faktury."""
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            invoice_id = self.table.item(selected_row, 0).text()
            
            rows = fetch_all_invoices()
            invoice_data = next((row for row in rows if str(row[0]) == invoice_id), None)

            if not invoice_data:
                return

            dialog = QDialog(self)
            dialog.setWindowTitle("Upravit fakturu")
            layout = QFormLayout()

            invoice_number_input = QLineEdit(invoice_data[1])
            layout.addRow(QLabel("Číslo faktury:"), invoice_number_input)

            company_names = fetch_company_names()
            recipient_box = QComboBox()
            recipient_box.addItems(company_names)
            recipient_box.setCurrentText(invoice_data[2])
            layout.addRow(QLabel("Příjemce:"), recipient_box)
###addede
            type_box = QComboBox()
            type_box.addItems(["Přijatá", "Vydaná"])
            type_box.setCurrentText(invoice_data[2])  # Nastavení aktuální hodnoty
            layout.addRow(QLabel("Typ faktury:"), type_box)

####konec  editace 

            issuer_box = QComboBox()
            issuer_box.addItems(company_names)
            issuer_box.setCurrentText(invoice_data[3])
            layout.addRow(QLabel("Výdejce:"), issuer_box)

            issue_date = QDateEdit()
            issue_date.setCalendarPopup(True)
            issue_date.setDate(QDate.fromString(invoice_data[5], "yyyy-MM-dd"))
            layout.addRow(QLabel("Datum vystavení:"), issue_date)

            tax_date = QDateEdit()
            tax_date.setCalendarPopup(True)
            tax_date.setDate(QDate.fromString(invoice_data[5], "yyyy-MM-dd"))
            layout.addRow(QLabel("Datum plnění:"), tax_date)

            due_date = QDateEdit()
            due_date.setCalendarPopup(True)
            due_date.setDate(QDate.fromString(invoice_data[6], "yyyy-MM-dd"))
            layout.addRow(QLabel("Datum splatnosti:"), due_date)

            amount_input = QLineEdit(str(invoice_data[8]))
            layout.addRow(QLabel("Částka bez DPH:"), amount_input)

            tax_input = QLineEdit(str(invoice_data[9]))
            layout.addRow(QLabel("Částka DPH:"), tax_input)

            total_input = QLineEdit(str(invoice_data[10]))
            layout.addRow(QLabel("Celková částka:"), total_input)

            status_box = QComboBox()
            status_box.addItems(["Čeká na platbu", "Zaplaceno", "Stornováno"])
           
            status_box.setCurrentText(str(invoice_data[11]))  # Převedení na string
            layout.addRow(QLabel("Status faktury:"), status_box)

            note_input = QLineEdit(invoice_data[12])
            layout.addRow(QLabel("Poznámka:"), note_input)

            save_button = QPushButton("Uložit změny")
            layout.addWidget(save_button)


            def save_changes():
                """Uloží změny faktury a zobrazí potvrzení."""
                updated_data = (
                    invoice_number_input.text(), type_box.currentText(),
                    recipient_box.currentText(), issuer_box.currentText(),
                    issue_date.date().toString("yyyy-MM-dd"),
                    tax_date.date().toString("yyyy-MM-dd"),
                    due_date.date().toString("yyyy-MM-dd"),
                    float(amount_input.text()), float(tax_input.text()),
                    float(total_input.text()), status_box.currentText(), note_input.text()
                )
                update_invoice(invoice_id, updated_data)
                self.load_invoices()
                QMessageBox.information(self, "Úspěch", f"Faktura '{invoice_number_input.text()}' byla úspěšně upravena!")
                dialog.accept()



            save_button.clicked.connect(save_changes)
            dialog.setLayout(layout)
            dialog.exec()

    def export_to_pdf(self):
        """Export vybrané faktury do PDF se stejným stylem jako v aplikaci."""
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Chyba", "Nejdříve vyberte fakturu k exportu!")
            return
        
        invoice_data = [self.table.item(selected_row, col).text() for col in range(self.table.columnCount())]
        filename = f"Faktura_{invoice_data[0]}.pdf"

        doc = SimpleDocTemplate(filename, pagesize=A4)
        elements = []

        styles = getSampleStyleSheet()
        title_style = styles["Title"]
        title_style.fontName = "Helvetica-Bold"
        title_style.fontSize = 18
        title_style.textColor = colors.HexColor("#2C3E50")  # Tmavě modrá jako v aplikaci

        normal_style = styles["Normal"]
        normal_style.fontSize = 12
        normal_style.textColor = colors.HexColor("#2C3E50")

        elements.append(Paragraph(f"Faktura č. {invoice_data[1]}", title_style))
        elements.append(Paragraph(f"Příjemce: {invoice_data[2]}", normal_style))
        elements.append(Paragraph(f"Výdejce: {invoice_data[3]}", normal_style))
        elements.append(Paragraph(f"Datum vystavení: {invoice_data[4]}", normal_style))
        elements.append(Paragraph(f"Datum splatnosti: {invoice_data[5]}", normal_style))

        table_data = [
            ["Částka bez DPH", "Částka DPH", "Celkem", "Status"],
            [invoice_data[7], invoice_data[8], invoice_data[9], invoice_data[10]]
        ]

        table = Table(table_data, colWidths=[50 * mm, 50 * mm, 50 * mm, 40 * mm])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#6C85A3")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
            ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#F2F2F2")),
            ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#6C85A3")),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#6C85A3")),
        ]))

        elements.append(table)
        doc.build(elements)

        QMessageBox.information(self, "Export dokončen", f"Faktura byla exportována jako {filename}!")

    def export_all_to_pdf(self):
        """Export všech faktur do jednoho PDF souboru se stránkováním."""
        rows = fetch_all_invoices()
        if not rows:
            QMessageBox.warning(self, "Chyba", "Žádné faktury k exportu!")
            return
        
        export_path, _ = QFileDialog.getSaveFileName(self, "Uložit faktury jako PDF", "Všechny_faktury.pdf", "PDF Files (*.pdf)")
        if not export_path:
            return

        doc = SimpleDocTemplate(export_path, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()
        
        title_style = styles["Title"]
        title_style.fontName = "Helvetica-Bold"
        title_style.fontSize = 18
        title_style.textColor = colors.HexColor("#2C3E50")

        normal_style = styles["Normal"]
        normal_style.fontSize = 12
        normal_style.textColor = colors.HexColor("#2C3E50")

        for invoice_data in rows:
            elements.append(Paragraph(f"Faktura č. {invoice_data[1]}", title_style))
            elements.append(Paragraph(f"Příjemce: {invoice_data[2]}", normal_style))
            elements.append(Paragraph(f"Výdejce: {invoice_data[3]}", normal_style))
            elements.append(Paragraph(f"Datum vystavení: {invoice_data[5]}", normal_style))
            elements.append(Paragraph(f"Datum splatnosti: {invoice_data[6]}", normal_style))

            table_data = [
                ["Částka bez DPH", "Částka DPH", "Celkem", "Status"],
                [invoice_data[8], invoice_data[9], invoice_data[10], invoice_data[11]]
            ]

            table = Table(table_data, colWidths=[50 * mm, 50 * mm, 50 * mm, 40 * mm])
            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#6C85A3")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
                ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#F2F2F2")),
                ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#6C85A3")),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#6C85A3")),
            ]))

            elements.append(table)
            elements.append(PageBreak())  # Oddělení faktur na nové stránky

        doc.build(elements)
        QMessageBox.information(self, "Export dokončen", f"Všechny faktury byly exportovány jako {export_path}!")

    def delete_invoice(self):
        """Smaže vybranou fakturu po potvrzení uživatelem."""
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Chyba", "Nebyla vybrána žádná faktura!")
            return

        invoice_id = self.table.item(selected_row, 0).text()

        confirmation = QMessageBox.question(
            self, "Potvrzení smazání",
            f"Opravdu chcete smazat fakturu ID {invoice_id}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirmation == QMessageBox.StandardButton.Yes:
            delete_invoice(invoice_id)
            self.load_invoices()

