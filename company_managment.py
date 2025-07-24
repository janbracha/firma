from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QPushButton, QTableWidgetItem, 
    QDialog, QFormLayout, QLabel, QLineEdit, QMessageBox, QFrame, QScrollArea, QGridLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from companies import fetch_companies, add_company, update_company
from database import connect


class CompanyManagementWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Správa firem - Projekt & Develop s.r.o.")
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
        self.load_companies()

    def create_header(self, layout):
        """Vytvoří moderní hlavičku"""
        header_frame = QFrame()
        header_frame.setObjectName("headerFrame")
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(20, 20, 20, 20)
        
        # Levá část - informace o sekci
        left_layout = QVBoxLayout()
        
        title_label = QLabel("🏢 Správa firem")
        title_label.setObjectName("titleLabel")
        left_layout.addWidget(title_label)
        
        subtitle_label = QLabel("Správa firemních kontaktů a dodavatelů")
        subtitle_label.setObjectName("subtitleLabel")
        left_layout.addWidget(subtitle_label)
        
        header_layout.addLayout(left_layout)
        header_layout.addStretch()
        
        layout.addWidget(header_frame)
    
    def create_content(self, layout):
        """Vytvoří hlavní obsah okna"""
        
        # Akce s kartami
        actions_frame = self.create_section_frame("⚡ Rychlé akce", "Správa a operace s firmami")
        actions_grid = QGridLayout()
        actions_grid.setSpacing(15)
        
        # Karty akcí
        actions = [
            ("➕ Přidat firmu", "Zaregistrovat novou firmu", self.add_company),
            ("✏️ Upravit firmu", "Upravit údaje firmy", self.edit_company),
            ("🗑️ Smazat firmu", "Odstranit firmu ze systému", self.delete_company),
        ]
        
        for i, (title, desc, func) in enumerate(actions):
            card = self.create_action_card(title, desc, func)
            actions_grid.addWidget(card, 0, i)
        
        actions_frame.layout().addLayout(actions_grid)
        layout.addWidget(actions_frame)
        
        # Tabulka firem
        table_frame = self.create_section_frame("📋 Seznam firem", "Přehled všech registrovaných firem")
        
        # Tabulka firem
        self.table = QTableWidget(0, 6)
        self.table.setObjectName("dataTable")
        self.table.setHorizontalHeaderLabels([
            "Název firmy", "IČO", "DIČ", "Bankovní účet", "Kontakt", "Adresa"
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
                font-size: 16px;
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
                font-size: 16px;
            }
            
            QHeaderView::section:hover {
                background: rgba(95, 116, 143, 1.0);
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
        """Otevře moderní dialogové okno pro přidání firmy"""
        dialog = self.create_modern_dialog("Nová firma", "Registrace nové firmy do systému")
        layout = dialog.content_layout
        
        # Formulář pro firmu
        form_frame = QFrame()
        form_frame.setObjectName("formFrame")
        form_layout = QFormLayout(form_frame)
        form_layout.setSpacing(15)
        form_layout.setContentsMargins(20, 20, 20, 20)

        name_input = QLineEdit()
        name_input.setObjectName("modernInput")
        form_layout.addRow(self.create_label("Název firmy:"), name_input)

        ico_input = QLineEdit()
        ico_input.setObjectName("modernInput")
        form_layout.addRow(self.create_label("IČO:"), ico_input)

        dic_input = QLineEdit()
        dic_input.setObjectName("modernInput")
        form_layout.addRow(self.create_label("DIČ:"), dic_input)

        bank_input = QLineEdit()
        bank_input.setObjectName("modernInput")
        form_layout.addRow(self.create_label("Bankovní účet:"), bank_input)

        contact_input = QLineEdit()
        contact_input.setObjectName("modernInput")
        form_layout.addRow(self.create_label("Kontakt:"), contact_input)

        address_input = QLineEdit()
        address_input.setObjectName("modernInput")
        form_layout.addRow(self.create_label("Adresa:"), address_input)

        layout.addWidget(form_frame)

        # Tlačítka
        button_frame = QFrame()
        button_layout = QHBoxLayout(button_frame)
        button_layout.addStretch()
        
        cancel_button = QPushButton("Zrušit")
        cancel_button.setObjectName("cancelButton")
        cancel_button.clicked.connect(dialog.reject)
        button_layout.addWidget(cancel_button)
        
        save_button = QPushButton("💾 Uložit firmu")
        save_button.setObjectName("saveButton")
        button_layout.addWidget(save_button)
        
        layout.addWidget(button_frame)

        def save_company():
            if not name_input.text().strip():
                QMessageBox.warning(self, "Chyba", "Název firmy je povinný!")
                return
                
            add_company(name_input.text(), ico_input.text(), dic_input.text(), 
                       bank_input.text(), contact_input.text(), address_input.text())
            self.load_companies()
            QMessageBox.information(self, "Úspěch", f"Firma '{name_input.text()}' byla přidána!")
            dialog.accept()

        save_button.clicked.connect(save_company)
        
        # Aplikace stylů na dialog
        self.apply_dialog_styles(dialog)
        dialog.exec()

    def create_modern_dialog(self, title, subtitle):
        """Vytvoří moderní dialog s hlavičkou"""
        dialog = QDialog(self)
        dialog.setWindowTitle(title)
        dialog.setFixedSize(500, 600)
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

    def add_company_old(self):
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
        """Otevře moderní dialogové okno pro úpravu firmy"""
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Upozornění", "Prosím vyberte firmu k úpravě!")
            return

        company_name = self.table.item(selected_row, 0).text()
        company_data = [self.table.item(selected_row, col).text() for col in range(self.table.columnCount())]

        dialog = self.create_modern_dialog("Upravit firmu", f"Úprava údajů firmy {company_name}")
        layout = dialog.content_layout
        
        # Formulář pro firmu
        form_frame = QFrame()
        form_frame.setObjectName("formFrame")
        form_layout = QFormLayout(form_frame)
        form_layout.setSpacing(15)
        form_layout.setContentsMargins(20, 20, 20, 20)

        name_input = QLineEdit(company_data[0])
        name_input.setObjectName("modernInput")
        form_layout.addRow(self.create_label("Název firmy:"), name_input)

        ico_input = QLineEdit(company_data[1])
        ico_input.setObjectName("modernInput")
        form_layout.addRow(self.create_label("IČO:"), ico_input)

        dic_input = QLineEdit(company_data[2])
        dic_input.setObjectName("modernInput")
        form_layout.addRow(self.create_label("DIČ:"), dic_input)

        bank_input = QLineEdit(company_data[3])
        bank_input.setObjectName("modernInput")
        form_layout.addRow(self.create_label("Bankovní účet:"), bank_input)

        contact_input = QLineEdit(company_data[4])
        contact_input.setObjectName("modernInput")
        form_layout.addRow(self.create_label("Kontakt:"), contact_input)

        address_input = QLineEdit(company_data[5])
        address_input.setObjectName("modernInput")
        form_layout.addRow(self.create_label("Adresa:"), address_input)

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
            if not name_input.text().strip():
                QMessageBox.warning(self, "Chyba", "Název firmy je povinný!")
                return
                
            updated_data = (
                name_input.text(), ico_input.text(), dic_input.text(),
                bank_input.text(), contact_input.text(), address_input.text()
            )
            update_company(company_name, updated_data)
            self.load_companies()
            QMessageBox.information(self, "Úspěch", f"Firma '{name_input.text()}' byla upravena!")
            dialog.accept()

        save_button.clicked.connect(save_changes)
        
        # Aplikace stylů na dialog
        self.apply_dialog_styles(dialog)
        dialog.exec()

    def edit_company_old(self):
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



