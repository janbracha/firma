from PyQt6.QtCore import QDate, Qt
from PyQt6.QtWidgets import (
    QDialog, QFormLayout, QLabel, QLineEdit, QComboBox, QDateEdit,
    QMessageBox, QFileDialog, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QTableWidget, QPushButton, QTableWidgetItem, QFrame, QScrollArea, QGridLayout
)
from PyQt6.QtGui import QFont
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
        self.setWindowTitle("Správa faktur - Projekt & Develop s.r.o.")
        self.setGeometry(200, 200, 1200, 800)

        # Hlavní widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Hlavní scroll area pro responsive design
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_area.setWidget(scroll_content)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.addWidget(scroll_area)
        
        layout = QVBoxLayout(scroll_content)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # Moderní hlavička
        self.create_header(layout)
        
        # Hlavní obsah
        self.create_content(layout)
        
        # Aplikace stylů
        self.apply_modern_styles()

        # Načtení dat
        self.load_invoices()

    def create_header(self, layout):
        """Vytvoří moderní hlavičku"""
        header_frame = QFrame()
        header_frame.setObjectName("headerFrame")
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(20, 20, 20, 20)
        
        # Levá část - informace o sekci
        left_layout = QVBoxLayout()
        
        title_label = QLabel("📊 Správa faktur")
        title_label.setObjectName("titleLabel")
        left_layout.addWidget(title_label)
        
        subtitle_label = QLabel("Vystavování a správa všech faktur")
        subtitle_label.setObjectName("subtitleLabel")
        left_layout.addWidget(subtitle_label)
        
        header_layout.addLayout(left_layout)
        header_layout.addStretch()
        
        layout.addWidget(header_frame)
    
    def create_content(self, layout):
        """Vytvoří hlavní obsah okna"""
        
        # Akce s kartami
        actions_frame = self.create_section_frame("⚡ Rychlé akce", "Správa a operace s fakturami")
        actions_grid = QGridLayout()
        actions_grid.setSpacing(15)
        
        # Karty akcí
        actions = [
            ("➕ Zařazení faktury do evidence", "Evidovat novou fakturu v systému", self.add_invoice),
            ("✏️ Upravit fakturu", "Upravit vybranou fakturu", self.edit_invoice),
            ("🗑️ Smazat fakturu", "Odstranit fakturu ze systému", self.delete_invoice),
            ("📄 Export do PDF", "Exportovat vybranou fakturu", self.export_to_pdf),
            ("📚 Export všech", "Exportovat všechny faktury", self.export_all_to_pdf),
        ]
        
        for i, (title, desc, func) in enumerate(actions):
            card = self.create_action_card(title, desc, func)
            actions_grid.addWidget(card, i // 3, i % 3)
        
        actions_frame.layout().addLayout(actions_grid)
        layout.addWidget(actions_frame)
        
        # Tabulka faktur
        table_frame = self.create_section_frame("📋 Seznam faktur", "Přehled všech faktur v systému")
        
        # Tabulka faktur
        self.table = QTableWidget(0, 13)
        self.table.setObjectName("dataTable")
        self.table.setHorizontalHeaderLabels([
            "ID", "Číslo faktury", "Typ", "Příjemce", "Výdejce", "Datum vystavení", 
            "Datum plnění", "Datum splatnosti", "Částka bez DPH", "DPH", "Celkem", "Status", "Poznámka"
        ])
        
        # Nastavení tabulky
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        
        table_frame.layout().addWidget(self.table)
        layout.addWidget(table_frame)

    def create_section_frame(self, title, subtitle):
        """Vytvoří rám pro sekci"""
        frame = QFrame()
        frame.setObjectName("sectionFrame")
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(25, 20, 25, 20)
        layout.setSpacing(15)
        
        # Hlavička sekce
        header_layout = QVBoxLayout()
        
        title_label = QLabel(title)
        title_label.setObjectName("sectionTitle")
        header_layout.addWidget(title_label)
        
        subtitle_label = QLabel(subtitle)
        subtitle_label.setObjectName("sectionSubtitle")
        header_layout.addWidget(subtitle_label)
        
        layout.addLayout(header_layout)
        
        return frame
    
    def create_action_card(self, title, description, callback):
        """Vytvoří kartu pro akci"""
        card = QFrame()
        card.setObjectName("actionCard")
        card.setFixedSize(280, 100)
        card.setCursor(Qt.CursorShape.PointingHandCursor)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(5)
        
        title_label = QLabel(title)
        title_label.setObjectName("cardTitle")
        layout.addWidget(title_label)
        
        desc_label = QLabel(description)
        desc_label.setObjectName("cardDescription")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
        
        layout.addStretch()
        
        # Kliknutí na kartu
        def mousePressEvent(event):
            if event.button() == Qt.MouseButton.LeftButton:
                callback()
        
        card.mousePressEvent = mousePressEvent
        
        return card

    def apply_modern_styles(self):
        """Aplikuje moderní styly"""
        self.setStyleSheet("""
            /* Hlavní okno */
            QMainWindow {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            }
            
            /* Scroll area */
            QScrollArea {
                border: none;
                background: transparent;
            }
            
            /* Header */
            #headerFrame {
                background: rgba(255, 255, 255, 0.95);
                border-radius: 15px;
                border: 1px solid rgba(255, 255, 255, 0.3);
            }
            
            #titleLabel {
                font-size: 24px;
                font-weight: bold;
                color: #2c3e50;
                margin: 0;
            }
            
            #subtitleLabel {
                font-size: 14px;
                color: #7f8c8d;
                margin: 0;
            }
            
            /* Sekce */
            #sectionFrame {
                background: rgba(255, 255, 255, 0.95);
                border-radius: 15px;
                border: 1px solid rgba(255, 255, 255, 0.3);
                margin-bottom: 20px;
            }
            
            #sectionTitle {
                font-size: 18px;
                font-weight: bold;
                color: #2c3e50;
                margin-bottom: 5px;
            }
            
            #sectionSubtitle {
                font-size: 13px;
                color: #7f8c8d;
                margin-bottom: 15px;
            }
            
            /* Karty akcí */
            #actionCard {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(255, 255, 255, 0.9),
                    stop:1 rgba(247, 249, 252, 0.9));
                border: 2px solid rgba(108, 133, 163, 0.1);
                border-radius: 12px;
                margin: 5px;
            }
            
            #actionCard:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(255, 255, 255, 1.0),
                    stop:1 rgba(240, 248, 255, 1.0));
                border: 2px solid rgba(108, 133, 163, 0.3);
            }
            
            #cardTitle {
                font-size: 14px;
                font-weight: bold;
                color: #2c3e50;
                margin-bottom: 3px;
            }
            
            #cardDescription {
                font-size: 12px;
                color: #7f8c8d;
                line-height: 1.3;
            }
            
            /* Tabulka */
            #dataTable {
                background: white;
                alternate-background-color: #f8f9fa;
                border: 1px solid rgba(108, 133, 163, 0.2);
                border-radius: 8px;
                gridline-color: rgba(108, 133, 163, 0.1);
                selection-background-color: rgba(52, 152, 219, 0.2);
            }
            
            #dataTable::item {
                padding: 8px;
                border: none;
            }
            
            #dataTable::item:selected {
                background: rgba(52, 152, 219, 0.3);
                color: #2c3e50;
            }
            
            QHeaderView::section {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(108, 133, 163, 0.9),
                    stop:1 rgba(95, 116, 143, 0.9));
                color: white;
                padding: 10px;
                border: none;
                font-weight: bold;
                font-size: 12px;
            }
            
            QHeaderView::section:hover {
                background: rgba(95, 116, 143, 1.0);
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
        """Otevře moderní dialogové okno pro přidání faktury"""
        dialog = self.create_modern_dialog("Zařazení faktury do evidence", "Evidování nové faktury v systému")
        layout = dialog.content_layout
        
        # Formulář pro fakturu
        form_frame = QFrame()
        form_frame.setObjectName("formFrame")
        form_layout = QFormLayout(form_frame)
        form_layout.setSpacing(15)
        form_layout.setContentsMargins(20, 20, 20, 20)

        invoice_number_input = QLineEdit()
        invoice_number_input.setObjectName("modernInput")
        form_layout.addRow(self.create_label("Číslo faktury:"), invoice_number_input)

        type_box = QComboBox()
        type_box.setObjectName("modernCombo")
        type_box.addItems(["Přijatá", "Vydaná"])
        form_layout.addRow(self.create_label("Typ faktury:"), type_box)

        company_names = fetch_company_names()

        recipient_box = QComboBox()
        recipient_box.setObjectName("modernCombo")
        recipient_box.addItems(company_names)
        form_layout.addRow(self.create_label("Příjemce:"), recipient_box)

        issuer_box = QComboBox()
        issuer_box.setObjectName("modernCombo")
        issuer_box.addItems(company_names)
        form_layout.addRow(self.create_label("Výdejce:"), issuer_box)

        issue_date = QDateEdit()
        issue_date.setObjectName("modernDate")
        issue_date.setCalendarPopup(True)
        issue_date.setDate(QDate.currentDate())
        form_layout.addRow(self.create_label("Datum vystavení:"), issue_date)

        tax_date = QDateEdit()
        tax_date.setObjectName("modernDate")
        tax_date.setCalendarPopup(True)
        tax_date.setDate(QDate.currentDate())
        form_layout.addRow(self.create_label("Datum plnění:"), tax_date)

        due_date = QDateEdit()
        due_date.setObjectName("modernDate")
        due_date.setCalendarPopup(True)
        due_date.setDate(QDate.currentDate())
        form_layout.addRow(self.create_label("Datum splatnosti:"), due_date)

        amount_input = QLineEdit()
        amount_input.setObjectName("modernInput")
        form_layout.addRow(self.create_label("Částka bez DPH:"), amount_input)

        tax_input = QLineEdit()
        tax_input.setObjectName("modernInput")
        form_layout.addRow(self.create_label("Částka DPH:"), tax_input)

        total_input = QLineEdit()
        total_input.setObjectName("modernInput")
        form_layout.addRow(self.create_label("Celková částka:"), total_input)

        status_box = QComboBox()
        status_box.setObjectName("modernCombo")
        status_box.addItems(["Čeká na platbu", "Zaplaceno", "Stornováno"])
        form_layout.addRow(self.create_label("Status faktury:"), status_box)

        note_input = QLineEdit()
        note_input.setObjectName("modernInput")
        form_layout.addRow(self.create_label("Poznámka:"), note_input)

        layout.addWidget(form_frame)

        # Tlačítka
        button_frame = QFrame()
        button_layout = QHBoxLayout(button_frame)
        button_layout.addStretch()
        
        cancel_button = QPushButton("Zrušit")
        cancel_button.setObjectName("cancelButton")
        cancel_button.clicked.connect(dialog.reject)
        button_layout.addWidget(cancel_button)
        
        save_button = QPushButton("💾 Uložit fakturu")
        save_button.setObjectName("saveButton")
        button_layout.addWidget(save_button)
        
        layout.addWidget(button_frame)

        def save_invoice():
            """Uloží fakturu do databáze a zobrazí potvrzení."""
            try:
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
            except ValueError:
                QMessageBox.warning(self, "Chyba", "Prosím zadejte správné číselné hodnoty!")

        save_button.clicked.connect(save_invoice)
        
        # Aplikace stylů na dialog
        self.apply_dialog_styles(dialog)
        dialog.exec()

    def create_modern_dialog(self, title, subtitle):
        """Vytvoří moderní dialog s hlavičkou"""
        dialog = QDialog(self)
        dialog.setWindowTitle(title)
        dialog.setFixedSize(500, 700)
        dialog.setModal(True)
        
        main_layout = QVBoxLayout(dialog)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Hlavička
        header_frame = QFrame()
        header_frame.setObjectName("dialogHeader")
        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(30, 20, 30, 20)
        
        title_label = QLabel(title)
        title_label.setObjectName("dialogTitle")
        header_layout.addWidget(title_label)
        
        subtitle_label = QLabel(subtitle)
        subtitle_label.setObjectName("dialogSubtitle")
        header_layout.addWidget(subtitle_label)
        
        main_layout.addWidget(header_frame)
        
        # Obsah
        content_frame = QFrame()
        content_frame.setObjectName("dialogContent")
        dialog.content_layout = QVBoxLayout(content_frame)
        dialog.content_layout.setContentsMargins(30, 20, 30, 30)
        dialog.content_layout.setSpacing(20)
        
        main_layout.addWidget(content_frame)
        
        return dialog
    
    def create_label(self, text):
        """Vytvoří moderní label"""
        label = QLabel(text)
        label.setObjectName("formLabel")
        return label
    
    def apply_dialog_styles(self, dialog):
        """Aplikuje moderní styly na dialog"""
        dialog.setStyleSheet("""
            QDialog {
                background: white;
                border-radius: 15px;
            }
            
            #dialogHeader {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
                border-radius: 15px 15px 0 0;
            }
            
            #dialogTitle {
                font-size: 18px;
                font-weight: bold;
                color: white;
                margin: 0;
            }
            
            #dialogSubtitle {
                font-size: 13px;
                color: rgba(255, 255, 255, 0.9);
                margin: 0;
            }
            
            #dialogContent {
                background: white;
                border-radius: 0 0 15px 15px;
            }
            
            #formFrame {
                background: rgba(248, 249, 252, 0.8);
                border: 1px solid rgba(108, 133, 163, 0.2);
                border-radius: 10px;
                padding: 10px;
            }
            
            #formLabel {
                font-weight: bold;
                color: #2c3e50;
                font-size: 13px;
            }
            
            #modernInput {
                padding: 10px;
                border: 2px solid rgba(108, 133, 163, 0.2);
                border-radius: 8px;
                font-size: 13px;
                background: white;
            }
            
            #modernInput:focus {
                border: 2px solid #3498db;
                outline: none;
            }
            
            #modernCombo {
                padding: 8px;
                border: 2px solid rgba(108, 133, 163, 0.2);
                border-radius: 8px;
                font-size: 13px;
                background: white;
            }
            
            #modernCombo:focus {
                border: 2px solid #3498db;
            }
            
            #modernDate {
                padding: 8px;
                border: 2px solid rgba(108, 133, 163, 0.2);
                border-radius: 8px;
                font-size: 13px;
                background: white;
            }
            
            #modernDate:focus {
                border: 2px solid #3498db;
            }
            
            #saveButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #27ae60, stop:1 #229954);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-weight: bold;
                font-size: 14px;
            }
            
            #saveButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #229954, stop:1 #1e8449);
            }
            
            #cancelButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #95a5a6, stop:1 #7f8c8d);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-weight: bold;
                font-size: 14px;
            }
            
            #cancelButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #7f8c8d, stop:1 #6c7b7d);
            }
        """)

    def add_invoice_old(self):
        """Otevře dialogové okno pro přidání faktury a uloží ji do databáze."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Zařazení faktury do evidence")
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
        """Otevře moderní dialogové okno pro úpravu faktury"""
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Upozornění", "Prosím vyberte fakturu k úpravě!")
            return
            
        invoice_id = self.table.item(selected_row, 0).text()
        
        rows = fetch_all_invoices()
        invoice_data = next((row for row in rows if str(row[0]) == invoice_id), None)

        if not invoice_data:
            QMessageBox.warning(self, "Chyba", "Faktura nebyla nalezena!")
            return

        dialog = self.create_modern_dialog("Upravit fakturu", f"Úprava faktury č. {invoice_data[1]}")
        layout = dialog.content_layout
        
        # Formulář pro fakturu
        form_frame = QFrame()
        form_frame.setObjectName("formFrame")
        form_layout = QFormLayout(form_frame)
        form_layout.setSpacing(15)
        form_layout.setContentsMargins(20, 20, 20, 20)

        invoice_number_input = QLineEdit(invoice_data[1])
        invoice_number_input.setObjectName("modernInput")
        form_layout.addRow(self.create_label("Číslo faktury:"), invoice_number_input)

        type_box = QComboBox()
        type_box.setObjectName("modernCombo")
        type_box.addItems(["Přijatá", "Vydaná"])
        type_box.setCurrentText(invoice_data[2])
        form_layout.addRow(self.create_label("Typ faktury:"), type_box)

        company_names = fetch_company_names()
        
        recipient_box = QComboBox()
        recipient_box.setObjectName("modernCombo")
        recipient_box.addItems(company_names)
        recipient_box.setCurrentText(invoice_data[3])
        form_layout.addRow(self.create_label("Příjemce:"), recipient_box)

        issuer_box = QComboBox()
        issuer_box.setObjectName("modernCombo")
        issuer_box.addItems(company_names)
        issuer_box.setCurrentText(invoice_data[4])
        form_layout.addRow(self.create_label("Výdejce:"), issuer_box)

        issue_date = QDateEdit()
        issue_date.setObjectName("modernDate")
        issue_date.setCalendarPopup(True)
        issue_date.setDate(QDate.fromString(invoice_data[5], "yyyy-MM-dd"))
        form_layout.addRow(self.create_label("Datum vystavení:"), issue_date)

        tax_date = QDateEdit()
        tax_date.setObjectName("modernDate")
        tax_date.setCalendarPopup(True)
        tax_date.setDate(QDate.fromString(invoice_data[6], "yyyy-MM-dd"))
        form_layout.addRow(self.create_label("Datum plnění:"), tax_date)

        due_date = QDateEdit()
        due_date.setObjectName("modernDate")
        due_date.setCalendarPopup(True)
        due_date.setDate(QDate.fromString(invoice_data[7], "yyyy-MM-dd"))
        form_layout.addRow(self.create_label("Datum splatnosti:"), due_date)

        amount_input = QLineEdit(str(invoice_data[8]))
        amount_input.setObjectName("modernInput")
        form_layout.addRow(self.create_label("Částka bez DPH:"), amount_input)

        tax_input = QLineEdit(str(invoice_data[9]))
        tax_input.setObjectName("modernInput")
        form_layout.addRow(self.create_label("Částka DPH:"), tax_input)

        total_input = QLineEdit(str(invoice_data[10]))
        total_input.setObjectName("modernInput")
        form_layout.addRow(self.create_label("Celková částka:"), total_input)

        status_box = QComboBox()
        status_box.setObjectName("modernCombo")
        status_box.addItems(["Čeká na platbu", "Zaplaceno", "Stornováno"])
        status_box.setCurrentText(str(invoice_data[11]))
        form_layout.addRow(self.create_label("Status faktury:"), status_box)

        note_input = QLineEdit(invoice_data[12])
        note_input.setObjectName("modernInput")
        form_layout.addRow(self.create_label("Poznámka:"), note_input)

        layout.addWidget(form_frame)

        # Tlačítka
        button_frame = QFrame()
        button_layout = QHBoxLayout(button_frame)
        button_layout.addStretch()
        
        cancel_button = QPushButton("Zrušit")
        cancel_button.setObjectName("cancelButton")
        cancel_button.clicked.connect(dialog.reject)
        button_layout.addWidget(cancel_button)
        
        save_button = QPushButton("💾 Uložit změny")
        save_button.setObjectName("saveButton")
        button_layout.addWidget(save_button)
        
        layout.addWidget(button_frame)

        def save_changes():
            """Uloží změny faktury a zobrazí potvrzení."""
            try:
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
            except ValueError:
                QMessageBox.warning(self, "Chyba", "Prosím zadejte správné číselné hodnoty!")

        save_button.clicked.connect(save_changes)
        
        # Aplikace stylů na dialog
        self.apply_dialog_styles(dialog)
        dialog.exec()

    def edit_invoice_old(self):
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

