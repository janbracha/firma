from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QPushButton, QTableWidgetItem, 
    QDialog, QFormLayout, QLabel, QLineEdit, QMessageBox, QFrame, QScrollArea, QGridLayout, 
    QComboBox, QDateEdit, QTextEdit, QDoubleSpinBox
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont
from database import connect

class AssetManagementWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Správa hmotného majetku - Projekt & Develop s.r.o.")
        self.setGeometry(200, 200, 1200, 800)
        
        # Databázové připojení
        self.db = connect()

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
        self.load_assets()

    def create_header(self, layout):
        """Vytvoří moderní hlavičku"""
        header_frame = QFrame()
        header_frame.setObjectName("headerFrame")
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(20, 20, 20, 20)
        
        # Levá část - informace o sekci
        left_layout = QVBoxLayout()
        
        title_label = QLabel("🏢 Správa hmotného majetku")
        title_label.setObjectName("titleLabel")
        left_layout.addWidget(title_label)
        
        subtitle_label = QLabel("Evidence a správa dlouhodobého hmotného majetku")
        subtitle_label.setObjectName("subtitleLabel")
        left_layout.addWidget(subtitle_label)
        
        header_layout.addLayout(left_layout)
        header_layout.addStretch()
        
        layout.addWidget(header_frame)
    
    def create_content(self, layout):
        """Vytvoří hlavní obsah okna"""
        
        # Akce s kartami
        actions_frame = self.create_section_frame("⚡ Rychlé akce", "Správa a operace s majetkem")
        actions_grid = QGridLayout()
        actions_grid.setSpacing(15)
        
        # Karty akcí
        actions = [
            ("➕ Přidat majetek", "Evidovat nový majetek", self.add_asset),
            ("✏️ Upravit majetek", "Upravit údaje majetku", self.edit_asset),
            ("🗑️ Vyřadit majetek", "Vyřadit majetek z evidence", self.delete_asset),
            ("📊 Odpisy majetku", "Správa a výpočet odpisů", self.manage_depreciation),
        ]
        
        for i, (title, desc, func) in enumerate(actions):
            card = self.create_action_card(title, desc, func)
            row = i // 2
            col = i % 2
            actions_grid.addWidget(card, row, col)
        
        actions_frame.layout().addLayout(actions_grid)
        layout.addWidget(actions_frame)
        
        # Tabulka majetku
        table_frame = self.create_section_frame("📋 Seznam majetku", "Přehled veškerého evidovaného majetku")
        
        # Tabulka majetku
        self.table = QTableWidget(0, 8)
        self.table.setObjectName("dataTable")
        self.table.setHorizontalHeaderLabels([
            "ID", "Název", "Kategorie", "Pořizovací cena", "Datum pořízení", 
            "Odpisy celkem", "Zůstatková cena", "Stav"
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
        card.setFixedSize(280, 120)
        card.setCursor(Qt.CursorShape.PointingHandCursor)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(8)
        
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
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(99, 125, 168, 1.0),
                    stop:1 rgba(102, 126, 234, 1.0));
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
                margin-bottom: 20px;
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
                font-size: 16px;
                selection-background-color: rgba(108, 133, 163, 0.2);
            }
            
            #dataTable::item {
                padding: 8px;
                border: none;
            }
            
            #dataTable::item:selected {
                background: rgba(108, 133, 163, 0.3);
                color: #2c3e50;
            }
            
            QHeaderView::section {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(108, 133, 163, 0.8),
                    stop:1 rgba(108, 133, 163, 0.6));
                color: white;
                font-weight: bold;
                font-size: 11px;
                padding: 8px;
                border: none;
                border-right: 1px solid rgba(255, 255, 255, 0.3);
            }
        """)

    def load_assets(self):
        """Načte majetek z databáze a zobrazí v tabulce."""
        try:
            cursor = self.db.cursor()
            cursor.execute("""
                SELECT id, name, category, purchase_price, purchase_date, 
                       total_depreciation, book_value, status 
                FROM assets 
                ORDER BY purchase_date DESC
            """)
            rows = cursor.fetchall()

            self.table.setRowCount(len(rows))
            for row_idx, row in enumerate(rows):
                for col_idx, value in enumerate(row):
                    if col_idx in [3, 5, 6]:  # Cenové sloupce
                        if value is not None:
                            formatted_value = f"{float(value):,.2f} Kč"
                        else:
                            formatted_value = "0,00 Kč"
                        self.table.setItem(row_idx, col_idx, QTableWidgetItem(formatted_value))
                    else:
                        self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value) if value else ""))
        except Exception as e:
            QMessageBox.critical(self, "Chyba", f"Chyba při načítání majetku: {str(e)}")

    def add_asset(self):
        """Otevře formulář pro přidání majetku."""
        dialog = AssetDialog()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            try:
                cursor = self.db.cursor()
                cursor.execute("""
                    INSERT INTO assets (name, category, description, purchase_price, 
                                      purchase_date, depreciation_method, useful_life, 
                                      total_depreciation, book_value, status) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    dialog.name_edit.text(),
                    dialog.category_combo.currentText(),
                    dialog.description_edit.toPlainText(),
                    dialog.price_edit.value(),
                    dialog.date_edit.date().toString("yyyy-MM-dd"),
                    dialog.method_combo.currentText(),
                    dialog.life_edit.value(),
                    0.0,  # počáteční odpisy
                    dialog.price_edit.value(),  # počáteční zůstatková cena
                    "Aktivní"
                ))
                self.db.commit()
                self.load_assets()
                QMessageBox.information(self, "Úspěch", "Majetek byl úspěšně přidán!")
            except Exception as e:
                QMessageBox.critical(self, "Chyba", f"Chyba při přidávání majetku: {str(e)}")

    def edit_asset(self):
        """Otevře formulář pro úpravu majetku."""
        current_row = self.table.currentRow()
        if current_row >= 0:
            asset_id = self.table.item(current_row, 0).text()
            
            # Načteme data majetku
            cursor = self.db.cursor()
            cursor.execute("""
                SELECT name, category, description, purchase_price, purchase_date, 
                       depreciation_method, useful_life, status 
                FROM assets WHERE id = ?
            """, (asset_id,))
            result = cursor.fetchone()
            
            if result:
                dialog = AssetDialog()
                dialog.name_edit.setText(result[0] or "")
                dialog.category_combo.setCurrentText(result[1] or "")
                dialog.description_edit.setPlainText(result[2] or "")
                dialog.price_edit.setValue(float(result[3]) if result[3] else 0.0)
                dialog.date_edit.setDate(QDate.fromString(result[4], "yyyy-MM-dd"))
                dialog.method_combo.setCurrentText(result[5] or "")
                dialog.life_edit.setValue(int(result[6]) if result[6] else 0)
                
                if dialog.exec() == QDialog.DialogCode.Accepted:
                    try:
                        cursor.execute("""
                            UPDATE assets 
                            SET name = ?, category = ?, description = ?, purchase_price = ?, 
                                purchase_date = ?, depreciation_method = ?, useful_life = ?
                            WHERE id = ?
                        """, (
                            dialog.name_edit.text(),
                            dialog.category_combo.currentText(),
                            dialog.description_edit.toPlainText(),
                            dialog.price_edit.value(),
                            dialog.date_edit.date().toString("yyyy-MM-dd"),
                            dialog.method_combo.currentText(),
                            dialog.life_edit.value(),
                            asset_id
                        ))
                        self.db.commit()
                        self.load_assets()
                        QMessageBox.information(self, "Úspěch", "Majetek byl úspěšně upraven!")
                    except Exception as e:
                        QMessageBox.critical(self, "Chyba", f"Chyba při upravování majetku: {str(e)}")
        else:
            QMessageBox.warning(self, "Upozornění", "Vyberte majetek pro úpravu!")

    def delete_asset(self):
        """Vyřadí majetek z evidence."""
        current_row = self.table.currentRow()
        if current_row >= 0:
            asset_name = self.table.item(current_row, 1).text()
            
            reply = QMessageBox.question(
                self, 
                "Potvrzení vyřazení", 
                f"Opravdu chcete vyřadit majetek '{asset_name}' z evidence?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                asset_id = self.table.item(current_row, 0).text()
                try:
                    cursor = self.db.cursor()
                    cursor.execute("UPDATE assets SET status = 'Vyřazeno' WHERE id = ?", (asset_id,))
                    self.db.commit()
                    self.load_assets()
                    QMessageBox.information(self, "Úspěch", "Majetek byl úspěšně vyřazen!")
                except Exception as e:
                    QMessageBox.critical(self, "Chyba", f"Chyba při vyřazování majetku: {str(e)}")
        else:
            QMessageBox.warning(self, "Upozornění", "Vyberte majetek pro vyřazení!")

    def manage_depreciation(self):
        """Zobrazí správu odpisů."""
        dialog = DepreciationDialog(self.get_active_assets())
        if dialog.exec() == QDialog.DialogCode.Accepted:
            try:
                cursor = self.db.cursor()
                asset_id = dialog.asset_combo.currentData()
                monthly_depreciation = dialog.monthly_depreciation_edit.value()
                
                # Aktualizace celkových odpisů
                cursor.execute("""
                    UPDATE assets 
                    SET total_depreciation = total_depreciation + ?,
                        book_value = purchase_price - (total_depreciation + ?),
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                """, (monthly_depreciation, monthly_depreciation, asset_id))
                
                self.db.commit()
                self.load_assets()
                QMessageBox.information(self, "Úspěch", "Odpis byl úspěšně zaznamenán!")
            except Exception as e:
                QMessageBox.critical(self, "Chyba", f"Chyba při zaznamenání odpisu: {str(e)}")

    def get_active_assets(self):
        """Vrátí seznam aktivního majetku"""
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT id, name FROM assets WHERE status = 'Aktivní'")
            return cursor.fetchall()
        except:
            return []

    def closeEvent(self, event):
        """Uzavře databázové připojení při zavření okna"""
        if hasattr(self, 'db'):
            self.db.close()
        event.accept()


class AssetDialog(QDialog):
    """Dialog pro přidání/úpravu majetku"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Hmotný majetek")
        self.setFixedSize(500, 600)
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f6fa;
            }
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #2c3e50;
                margin-bottom: 5px;
            }
            QLineEdit, QComboBox, QTextEdit, QDateEdit, QDoubleSpinBox, QSpinBox {
                padding: 10px;
                border: 2px solid #e1e8ed;
                border-radius: 8px;
                font-size: 16px;
                background: white;
                margin-bottom: 10px;
            }
            QLineEdit:focus, QComboBox:focus, QTextEdit:focus, 
            QDateEdit:focus, QDoubleSpinBox:focus, QSpinBox:focus {
                border-color: #3498db;
            }
            QTextEdit {
                min-height: 80px;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3498db, stop:1 #2980b9);
                color: white;
                border: none;
                padding: 12px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 16px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5dade2, stop:1 #3498db);
            }
            QPushButton:pressed {
                background: #2980b9;
            }
            QPushButton[text="Zrušit"] {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #95a5a6, stop:1 #7f8c8d);
            }
            QPushButton[text="Zrušit"]:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #bdc3c7, stop:1 #95a5a6);
            }
        """)
        
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Formulář
        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Název majetku")
        form_layout.addRow("Název:", self.name_edit)
        
        self.category_combo = QComboBox()
        self.category_combo.addItems([
            "Budovy a stavby",
            "Stroje a zařízení", 
            "Dopravní prostředky",
            "Inventář",
            "Výpočetní technika",
            "Software",
            "Ostatní"
        ])
        form_layout.addRow("Kategorie:", self.category_combo)
        
        self.description_edit = QTextEdit()
        self.description_edit.setPlaceholderText("Popis majetku")
        form_layout.addRow("Popis:", self.description_edit)
        
        self.price_edit = QDoubleSpinBox()
        self.price_edit.setMaximum(999999999.99)
        self.price_edit.setSuffix(" Kč")
        form_layout.addRow("Pořizovací cena:", self.price_edit)
        
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        form_layout.addRow("Datum pořízení:", self.date_edit)
        
        self.method_combo = QComboBox()
        self.method_combo.addItems([
            "Rovnoměrné",
            "Zrychlené", 
            "Neodpisuje se"
        ])
        form_layout.addRow("Metoda odpisování:", self.method_combo)
        
        self.life_edit = QDoubleSpinBox()
        self.life_edit.setMaximum(50)
        self.life_edit.setSuffix(" let")
        self.life_edit.setValue(4)
        form_layout.addRow("Doba odpisování:", self.life_edit)
        
        layout.addLayout(form_layout)
        
        # Tlačítka
        button_layout = QHBoxLayout()
        
        self.cancel_button = QPushButton("Zrušit")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)
        
        self.save_button = QPushButton("Uložit")
        self.save_button.clicked.connect(self.accept)
        button_layout.addWidget(self.save_button)
        
        layout.addLayout(button_layout)


class DepreciationDialog(QDialog):
    """Dialog pro správu odpisů"""
    
    def __init__(self, assets, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Správa odpisů")
        self.setFixedSize(500, 400)
        self.assets = assets
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f6fa;
            }
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #2c3e50;
                margin-bottom: 5px;
            }
            QComboBox, QDoubleSpinBox, QLineEdit {
                padding: 10px;
                border: 2px solid #e1e8ed;
                border-radius: 8px;
                font-size: 16px;
                background: white;
                margin-bottom: 10px;
            }
            QComboBox:focus, QDoubleSpinBox:focus, QLineEdit:focus {
                border-color: #f39c12;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f39c12, stop:1 #e67e22);
                color: white;
                border: none;
                padding: 12px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 16px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f5b041, stop:1 #f39c12);
            }
        """)
        
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Formulář
        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        
        # Výběr majetku
        asset_label = QLabel("🏢 Výběr majetku")
        asset_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #f39c12; margin-top: 10px;")
        form_layout.addRow(asset_label)
        
        self.asset_combo = QComboBox()
        for asset_id, asset_name in self.assets:
            self.asset_combo.addItem(asset_name, asset_id)
        self.asset_combo.currentTextChanged.connect(self.calculate_suggested_depreciation)
        form_layout.addRow("Majetek:", self.asset_combo)
        
        # Odpisy
        depreciation_label = QLabel("📉 Odpisy")
        depreciation_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #f39c12; margin-top: 15px;")
        form_layout.addRow(depreciation_label)
        
        self.monthly_depreciation_edit = QDoubleSpinBox()
        self.monthly_depreciation_edit.setMaximum(999999.99)
        self.monthly_depreciation_edit.setSuffix(" Kč")
        form_layout.addRow("Měsíční odpis:", self.monthly_depreciation_edit)
        
        self.suggested_edit = QLineEdit()
        self.suggested_edit.setReadOnly(True)
        self.suggested_edit.setPlaceholderText("Doporučený odpis se zobrazí zde")
        form_layout.addRow("Doporučený odpis:", self.suggested_edit)
        
        # Informační text
        info_label = QLabel("""
💡 Doporučené odpisy:
• Lineární metoda: pořizovací cena / doba použitelnosti
• Běžná doba použitelnosti: 4-6 let (IT), 10-20 let (stroje)
• Minimální doba: 3 roky pro většinu majetku
        """)
        info_label.setStyleSheet("""
            font-size: 11px; 
            color: #7f8c8d; 
            background: #ecf0f1; 
            padding: 15px; 
            border-radius: 8px;
            margin-top: 10px;
        """)
        form_layout.addRow(info_label)
        
        layout.addLayout(form_layout)
        
        # Tlačítka
        button_layout = QHBoxLayout()
        
        self.cancel_button = QPushButton("Zrušit")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)
        
        self.save_button = QPushButton("Zaznamenat odpis")
        self.save_button.clicked.connect(self.accept)
        button_layout.addWidget(self.save_button)
        
        layout.addLayout(button_layout)
        
        # Výpočet při načtení
        if self.assets:
            self.calculate_suggested_depreciation()
    
    def calculate_suggested_depreciation(self):
        """Vypočítá doporučený odpis"""
        try:
            from database import connect
            asset_id = self.asset_combo.currentData()
            if asset_id:
                db = connect()
                cursor = db.cursor()
                cursor.execute("SELECT purchase_price, useful_life FROM assets WHERE id = ?", (asset_id,))
                result = cursor.fetchone()
                db.close()
                
                if result and result[0] and result[1]:
                    purchase_price = result[0]
                    useful_life_years = result[1]
                    
                    # Měsíční odpis
                    monthly_depreciation = purchase_price / (useful_life_years * 12)
                    self.suggested_edit.setText(f"{monthly_depreciation:,.2f} Kč")
                    self.monthly_depreciation_edit.setValue(monthly_depreciation)
                else:
                    self.suggested_edit.setText("Nelze vypočítat - chybí data")
        except Exception as e:
            self.suggested_edit.setText(f"Chyba: {str(e)}")
