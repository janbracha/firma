from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QPushButton, QTableWidgetItem, 
    QDialog, QFormLayout, QLabel, QLineEdit, QMessageBox, QFrame, QScrollArea, QGridLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from database import connect

class VehicleManagementWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Správa vozidel - Projekt & Develop s.r.o.")
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
        self.load_vehicles()

    def create_header(self, layout):
        """Vytvoří moderní hlavičku"""
        header_frame = QFrame()
        header_frame.setObjectName("headerFrame")
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(20, 20, 20, 20)
        
        # Levá část - informace o sekci
        left_layout = QVBoxLayout()
        
        title_label = QLabel("🚗 Správa vozidel")
        title_label.setObjectName("titleLabel")
        left_layout.addWidget(title_label)
        
        subtitle_label = QLabel("Registrace a správa vozového parku")
        subtitle_label.setObjectName("subtitleLabel")
        left_layout.addWidget(subtitle_label)
        
        header_layout.addLayout(left_layout)
        header_layout.addStretch()
        
        layout.addWidget(header_frame)
    
    def create_content(self, layout):
        """Vytvoří hlavní obsah okna"""
        
        # Akce s kartami
        actions_frame = self.create_section_frame("⚡ Rychlé akce", "Správa a operace s vozidly")
        actions_grid = QGridLayout()
        actions_grid.setSpacing(15)
        
        # Karty akcí
        actions = [
            ("➕ Přidat vozidlo", "Registrovat nové vozidlo", self.add_vehicle),
            ("✏️ Upravit vozidlo", "Upravit údaje vozidla", self.edit_vehicle),
            ("🗑️ Smazat vozidlo", "Odstranit vozidlo ze systému", self.delete_vehicle),
        ]
        
        for i, (title, desc, func) in enumerate(actions):
            card = self.create_action_card(title, desc, func)
            actions_grid.addWidget(card, 0, i)
        
        actions_frame.layout().addLayout(actions_grid)
        layout.addWidget(actions_frame)
        
        # Tabulka vozidel
        table_frame = self.create_section_frame("📋 Seznam vozidel", "Přehled všech registrovaných vozidel")
        
        # Tabulka vozidel
        self.table = QTableWidget(0, 4)
        self.table.setObjectName("dataTable")
        self.table.setHorizontalHeaderLabels([
            "Registrační značka", "Typ vozidla", "Vlastník", "Spotřeba (l/100km)"
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
        """Otevře moderní formulář pro přidání vozidla."""
        dialog = QDialog(self)
        dialog.setWindowTitle("➕ Přidat nové vozidlo")
        dialog.setFixedSize(550, 450)  # Zvětšeno pro lepší zobrazení
        dialog.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
            }
            QLabel {
                color: white;
                font-weight: bold;
                font-size: 15px;
                font-family: 'Inter', 'Roboto', sans-serif;
            }
            QLineEdit {
                background: white;
                border: 2px solid rgba(255,255,255,0.3);
                border-radius: 8px;
                padding: 12px 15px;
                font-size: 15px;
                font-family: 'Inter', 'Roboto', sans-serif;
                min-height: 20px;
                min-width: 250px;
                color: #2c3e50;
            }
            QLineEdit:focus {
                border: 2px solid #3498db;
                outline: none;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3498db, stop:1 #2980b9);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-weight: bold;
                font-size: 15px;
                font-family: 'Inter', 'Roboto', sans-serif;
                min-height: 20px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2980b9, stop:1 #21618c);
            }
        """)
        
        layout = QVBoxLayout(dialog)
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Hlavička
        title_label = QLabel("🚗 Registrace nového vozidla")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; margin-bottom: 20px;")
        layout.addWidget(title_label)

        # Formulář
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        
        registration_input = QLineEdit()
        registration_input.setPlaceholderText("1A2 3456")
        registration_input.setMinimumHeight(35)
        registration_input.setMinimumWidth(250)
        form_layout.addRow("Registrační značka:", registration_input)

        type_input = QLineEdit()
        type_input.setPlaceholderText("Osobní auto, nákladní...")
        type_input.setMinimumHeight(35)
        type_input.setMinimumWidth(250)
        form_layout.addRow("Typ vozidla:", type_input)

        owner_input = QLineEdit()
        owner_input.setPlaceholderText("Jméno vlastníka")
        owner_input.setMinimumHeight(35)
        owner_input.setMinimumWidth(250)
        form_layout.addRow("Vlastník:", owner_input)

        consumption_input = QLineEdit()
        consumption_input.setPlaceholderText("7.5")
        consumption_input.setMinimumHeight(35)
        consumption_input.setMinimumWidth(250)
        form_layout.addRow("Spotřeba (l/100km):", consumption_input)

        layout.addLayout(form_layout)
        
        # Tlačítka
        button_layout = QHBoxLayout()
        
        cancel_button = QPushButton("❌ Zrušit")
        cancel_button.clicked.connect(dialog.reject)
        button_layout.addWidget(cancel_button)
        
        save_button = QPushButton("✅ Uložit vozidlo")
        button_layout.addWidget(save_button)
        
        layout.addLayout(button_layout)

        def save_vehicle():
            """Uloží vozidlo do databáze."""
            if not all([registration_input.text(), type_input.text(), owner_input.text(), 
                       consumption_input.text()]):
                QMessageBox.warning(dialog, "Chyba", "Všechna pole musí být vyplněna!")
                return
                
            try:
                conn = connect()
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO cars (registration, type, owner, consumption) 
                    VALUES (?, ?, ?, ?)
                """, (registration_input.text(), type_input.text(), owner_input.text(), 
                     float(consumption_input.text())))
                conn.commit()
                conn.close()

                self.load_vehicles()
                QMessageBox.information(dialog, "✅ Úspěch", "Vozidlo bylo úspěšně přidáno!")
                dialog.accept()
            except Exception as e:
                QMessageBox.critical(dialog, "Chyba", f"Chyba při ukládání: {str(e)}")

        save_button.clicked.connect(save_vehicle)
        dialog.exec()

    def edit_vehicle(self):
        """Otevře moderní formulář pro úpravu vozidla."""
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "⚠️ Chyba", "Nebyl vybrán žádný záznam k úpravě!")
            return

        vehicle_data = [self.table.item(selected_row, col).text() for col in range(self.table.columnCount())]

        dialog = QDialog(self)
        dialog.setWindowTitle("✏️ Upravit vozidlo")
        dialog.setFixedSize(550, 450)  # Zvětšeno pro lepší zobrazení
        dialog.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
            }
            QLabel {
                color: white;
                font-weight: bold;
                font-size: 15px;
                font-family: 'Inter', 'Roboto', sans-serif;
            }
            QLineEdit {
                background: white;
                border: 2px solid rgba(255,255,255,0.3);
                border-radius: 8px;
                padding: 12px 15px;
                font-size: 15px;
                font-family: 'Inter', 'Roboto', sans-serif;
                min-height: 20px;
                min-width: 250px;
                color: #2c3e50;
            }
            QLineEdit:focus {
                border: 2px solid #e67e22;
                outline: none;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e67e22, stop:1 #d35400);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-weight: bold;
                font-size: 15px;
                font-family: 'Inter', 'Roboto', sans-serif;
                min-height: 20px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #d35400, stop:1 #a04000);
            }
        """)
        
        layout = QVBoxLayout(dialog)
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Hlavička
        title_label = QLabel(f"🔧 Úprava vozidla: {vehicle_data[0]}")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; margin-bottom: 20px;")
        layout.addWidget(title_label)

        # Formulář
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        
        registration_input = QLineEdit(vehicle_data[0])
        registration_input.setMinimumHeight(35)
        registration_input.setMinimumWidth(250)
        form_layout.addRow("Registrační značka:", registration_input)

        type_input = QLineEdit(vehicle_data[1])
        type_input.setMinimumHeight(35)
        type_input.setMinimumWidth(250)
        form_layout.addRow("Typ vozidla:", type_input)

        owner_input = QLineEdit(vehicle_data[2])
        owner_input.setMinimumHeight(35)
        owner_input.setMinimumWidth(250)
        form_layout.addRow("Vlastník:", owner_input)

        consumption_input = QLineEdit(vehicle_data[3])
        consumption_input.setMinimumHeight(35)
        consumption_input.setMinimumWidth(250)
        form_layout.addRow("Spotřeba (l/100km):", consumption_input)

        layout.addLayout(form_layout)
        
        # Tlačítka
        button_layout = QHBoxLayout()
        
        cancel_button = QPushButton("❌ Zrušit")
        cancel_button.clicked.connect(dialog.reject)
        button_layout.addWidget(cancel_button)
        
        save_button = QPushButton("💾 Uložit změny")
        button_layout.addWidget(save_button)
        
        layout.addLayout(button_layout)

        def save_changes():
            """Uloží změny vozidla."""
            if not all([registration_input.text(), type_input.text(), owner_input.text(), 
                       consumption_input.text()]):
                QMessageBox.warning(dialog, "Chyba", "Všechna pole musí být vyplněna!")
                return
                
            try:
                conn = connect()
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE cars SET registration=?, type=?, owner=?, consumption=? 
                    WHERE registration=?
                """, (registration_input.text(), type_input.text(), owner_input.text(), 
                     float(consumption_input.text()), vehicle_data[0]))
                conn.commit()
                conn.close()

                self.load_vehicles()
                QMessageBox.information(dialog, "✅ Úspěch", "Vozidlo bylo úspěšně upraveno!")
                dialog.accept()
            except Exception as e:
                QMessageBox.critical(dialog, "Chyba", f"Chyba při ukládání: {str(e)}")

        save_button.clicked.connect(save_changes)
        dialog.exec()

    def delete_vehicle(self):
        """Smaže vozidlo s moderním potvrzovacím dialogem."""
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "⚠️ Chyba", "Nebyl vybrán žádný záznam ke smazání!")
            return

        vehicle_registration = self.table.item(selected_row, 0).text()
        vehicle_type = self.table.item(selected_row, 1).text()
        vehicle_owner = self.table.item(selected_row, 2).text()
        
        # Moderní potvrzovací dialog
        reply = QMessageBox.question(
            self, 
            "🗑️ Potvrzení smazání",
            f"Opravdu chcete smazat vozidlo?\n\n"
            f"🚗 {vehicle_type}\n"
            f"🔢 SPZ: {vehicle_registration}\n"
            f"👤 Vlastník: {vehicle_owner}\n\n"
            f"Tato akce je nevratná!",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                conn = connect()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM cars WHERE registration=?", (vehicle_registration,))
                conn.commit()
                conn.close()

                self.load_vehicles()
                QMessageBox.information(self, "✅ Úspěch", f"Vozidlo {vehicle_registration} bylo úspěšně smazáno!")
            except Exception as e:
                QMessageBox.critical(self, "❌ Chyba", f"Chyba při mazání vozidla: {str(e)}")
