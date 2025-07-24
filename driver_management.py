from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QPushButton, QTableWidgetItem, 
    QDialog, QFormLayout, QLabel, QLineEdit, QMessageBox, QFrame, QScrollArea, QGridLayout, QComboBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from database import connect

class DriverManagementWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Správa řidičů - Projekt & Develop s.r.o.")
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
        self.load_drivers()

    def create_header(self, layout):
        """Vytvoří moderní hlavičku"""
        header_frame = QFrame()
        header_frame.setObjectName("headerFrame")
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(20, 20, 20, 20)
        
        # Levá část - informace o sekci
        left_layout = QVBoxLayout()
        
        title_label = QLabel("👨‍💼 Správa řidičů")
        title_label.setObjectName("titleLabel")
        left_layout.addWidget(title_label)
        
        subtitle_label = QLabel("Registrace a správa řidičů vozového parku")
        subtitle_label.setObjectName("subtitleLabel")
        left_layout.addWidget(subtitle_label)
        
        header_layout.addLayout(left_layout)
        header_layout.addStretch()
        
        layout.addWidget(header_frame)
    
    def create_content(self, layout):
        """Vytvoří hlavní obsah okna"""
        
        # Akce s kartami
        actions_frame = self.create_section_frame("⚡ Rychlé akce", "Správa a operace s řidiči")
        actions_grid = QGridLayout()
        actions_grid.setSpacing(15)
        
        # Karty akcí
        actions = [
            ("➕ Přidat řidiče", "Registrovat nového řidiče", self.add_driver),
            ("✏️ Upravit řidiče", "Upravit údaje řidiče", self.edit_driver),
            ("🗑️ Smazat řidiče", "Odstranit řidiče ze systému", self.delete_driver),
        ]
        
        for i, (title, desc, func) in enumerate(actions):
            card = self.create_action_card(title, desc, func)
            actions_grid.addWidget(card, 0, i)
        
        actions_frame.layout().addLayout(actions_grid)
        layout.addWidget(actions_frame)
        
        # Tabulka řidičů
        table_frame = self.create_section_frame("📋 Seznam řidičů", "Přehled všech registrovaných řidičů")
        
        # Tabulka řidičů
        self.table = QTableWidget(0, 4)
        self.table.setObjectName("dataTable")
        self.table.setHorizontalHeaderLabels([
            "ID", "Titul", "Jméno", "Příjmení"
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

    def load_drivers(self):
        """Načte řidiče z databáze a zobrazí v tabulce."""
        cursor = self.db.cursor()
        cursor.execute("SELECT id, title, first_name, last_name FROM drivers")
        rows = cursor.fetchall()

        self.table.setRowCount(len(rows))
        for row_idx, row in enumerate(rows):
            for col_idx, value in enumerate(row):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

    def add_driver(self):
        """Otevře formulář pro přidání řidiče."""
        dialog = DriverDialog()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            try:
                cursor = self.db.cursor()
                cursor.execute("""
                    INSERT INTO drivers (title, first_name, last_name, role) 
                    VALUES (?, ?, ?, ?)
                """, (dialog.title_edit.text(), dialog.name_edit.text(), 
                     dialog.surname_edit.text(), dialog.role_combo.currentText()))
                self.db.commit()
                self.load_drivers()
                QMessageBox.information(self, "Úspěch", "Řidič byl úspěšně přidán!")
            except Exception as e:
                QMessageBox.critical(self, "Chyba", f"Chyba při přidávání řidiče: {str(e)}")

    def edit_driver(self):
        """Otevře formulář pro úpravu řidiče."""
        current_row = self.table.currentRow()
        if current_row >= 0:
            driver_id = self.table.item(current_row, 0).text()
            
            # Načteme data řidiče
            cursor = self.db.cursor()
            cursor.execute("SELECT title, first_name, last_name, role FROM drivers WHERE id = ?", (driver_id,))
            result = cursor.fetchone()
            
            if result:
                dialog = DriverDialog()
                dialog.title_edit.setText(result[0] or "")
                dialog.name_edit.setText(result[1] or "")
                dialog.surname_edit.setText(result[2] or "")
                
                # Nastavíme role v comboboxu
                index = dialog.role_combo.findText(result[3] or "")
                if index >= 0:
                    dialog.role_combo.setCurrentIndex(index)
                
                if dialog.exec() == QDialog.DialogCode.Accepted:
                    try:
                        cursor.execute("""
                            UPDATE drivers 
                            SET title = ?, first_name = ?, last_name = ?, role = ?
                            WHERE id = ?
                        """, (dialog.title_edit.text(), dialog.name_edit.text(), 
                             dialog.surname_edit.text(), dialog.role_combo.currentText(), driver_id))
                        self.db.commit()
                        self.load_drivers()
                        QMessageBox.information(self, "Úspěch", "Řidič byl úspěšně upraven!")
                    except Exception as e:
                        QMessageBox.critical(self, "Chyba", f"Chyba při upravování řidiče: {str(e)}")
        else:
            QMessageBox.warning(self, "Upozornění", "Vyberte řidiče pro úpravu!")

    def delete_driver(self):
        """Smaže řidiče."""
        current_row = self.table.currentRow()
        if current_row >= 0:
            driver_name = f"{self.table.item(current_row, 2).text()} {self.table.item(current_row, 3).text()}"
            
            reply = QMessageBox.question(
                self, 
                "Potvrzení smazání", 
                f"Opravdu chcete smazat řidiče '{driver_name}'?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                driver_id = self.table.item(current_row, 0).text()
                try:
                    cursor = self.db.cursor()
                    cursor.execute("DELETE FROM drivers WHERE id = ?", (driver_id,))
                    self.db.commit()
                    self.load_drivers()
                    QMessageBox.information(self, "Úspěch", "Řidič byl úspěšně smazán!")
                except Exception as e:
                    QMessageBox.critical(self, "Chyba", f"Chyba při mazání řidiče: {str(e)}")
        else:
            QMessageBox.warning(self, "Upozornění", "Vyberte řidiče pro smazání!")

    def closeEvent(self, event):
        """Uzavře databázové připojení při zavření okna"""
        if hasattr(self, 'db'):
            self.db.close()
        event.accept()


class DriverDialog(QDialog):
    """Dialog pro přidání/úpravu řidiče"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Řidič")
        self.setFixedSize(400, 300)
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
            QLineEdit, QComboBox {
                padding: 10px;
                border: 2px solid #e1e8ed;
                border-radius: 8px;
                font-size: 16px;
                background: white;
                margin-bottom: 10px;
            }
            QLineEdit:focus, QComboBox:focus {
                border-color: #3498db;
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
        
        self.title_edit = QLineEdit()
        self.title_edit.setPlaceholderText("Např. Ing., Mgr.")
        form_layout.addRow("Titul:", self.title_edit)
        
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Zadejte jméno")
        form_layout.addRow("Jméno:", self.name_edit)
        
        self.surname_edit = QLineEdit()
        self.surname_edit.setPlaceholderText("Zadejte příjmení")
        form_layout.addRow("Příjmení:", self.surname_edit)
        
        self.role_combo = QComboBox()
        self.role_combo.addItems([
            "Řidič",
            "Hlavní řidič", 
            "Řidič-mechanik",
            "Dispečer",
            "Vedoucí dopravy"
        ])
        form_layout.addRow("Pozice:", self.role_combo)
        
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
