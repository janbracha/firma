from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QTableWidget, QPushButton, QTableWidgetItem, QDialog, QFormLayout, 
                             QLabel, QLineEdit, QMessageBox, QScrollArea, QFrame)
from PyQt6.QtCore import Qt
from database import connect

class DestinationManagementWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🗺️ Správa destinací")
        self.setGeometry(100, 100, 1200, 800)
        
        # Hlavní scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Hlavní widget
        main_widget = QWidget()
        scroll_area.setWidget(main_widget)
        self.setCentralWidget(scroll_area)
        
        # Hlavní layout
        layout = QVBoxLayout(main_widget)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(25)
        
        # Aplikování moderních stylů
        self.apply_modern_styles()
        
        # Vytvoření obsahu
        self.create_header(layout)
        self.create_content(layout)
        
        # Načtení dat
        self.load_destinations()

    def create_header(self, layout):
        """Vytvoří moderní hlavičku"""
        header_frame = QFrame()
        header_frame.setObjectName("headerFrame")
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(20, 20, 20, 20)
        
        # Levá část - informace o sekci
        left_layout = QVBoxLayout()
        
        title_label = QLabel("🗺️ Správa destinací")
        title_label.setObjectName("titleLabel")
        left_layout.addWidget(title_label)
        
        subtitle_label = QLabel("Registrace a správa cílových destinací")
        subtitle_label.setObjectName("subtitleLabel")
        left_layout.addWidget(subtitle_label)
        
        header_layout.addLayout(left_layout)
        header_layout.addStretch()
        
        layout.addWidget(header_frame)
    
    def create_content(self, layout):
        """Vytvoří hlavní obsah okna"""
        
        # Akce s kartami
        actions_frame = self.create_section_frame("⚡ Rychlé akce", "Správa a operace s destinacemi")
        actions_grid = QGridLayout()
        actions_grid.setSpacing(15)
        
        # Karty akcí
        actions = [
            ("➕ Přidat destinaci", "Registrovat novou destinaci", self.add_destination),
            ("✏️ Upravit destinaci", "Upravit údaje destinace", self.edit_destination),
            ("🗑️ Smazat destinaci", "Odstranit destinaci ze systému", self.delete_destination),
        ]
        
        for i, (title, desc, func) in enumerate(actions):
            card = self.create_action_card(title, desc, func)
            actions_grid.addWidget(card, 0, i)
        
        actions_frame.layout().addLayout(actions_grid)
        layout.addWidget(actions_frame)
        
        # Tabulka destinací
        table_frame = self.create_section_frame("📋 Seznam destinací", "Přehled všech registrovaných destinací")
        
        # Tabulka destinací
        self.table = QTableWidget(0, 6)
        self.table.setObjectName("dataTable")
        self.table.setHorizontalHeaderLabels([
            "ID", "Start", "Cíl", "Firma/Adresa", "Vzdálenost (km)", "Poznámka"
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

    def load_destinations(self):
        """Načte destinace z databáze a zobrazí v tabulce."""
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT id, start, destination, company, distance, note FROM destinations")
        rows = cursor.fetchall()
        conn.close()

        self.table.setRowCount(len(rows))
        for row_idx, row in enumerate(rows):
            for col_idx, value in enumerate(row):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

    def add_destination(self):
        """Otevře moderní formulář pro přidání destinace."""
        dialog = QDialog(self)
        dialog.setWindowTitle("➕ Přidat novou destinaci")
        dialog.setFixedSize(450, 400)
        dialog.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
            }
            QLabel {
                color: white;
                font-weight: bold;
                font-size: 14px;
            }
            QLineEdit {
                background: white;
                border: 2px solid rgba(255,255,255,0.3);
                border-radius: 8px;
                padding: 10px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 2px solid #3498db;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3498db, stop:1 #2980b9);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px;
                font-weight: bold;
                font-size: 14px;
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
        title_label = QLabel("🗺️ Registrace nové destinace")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; margin-bottom: 20px;")
        layout.addWidget(title_label)

        # Formulář
        form_layout = QFormLayout()
        form_layout.setSpacing(12)
        
        start_input = QLineEdit()
        start_input.setPlaceholderText("Praha, Brno, Ostrava...")
        form_layout.addRow("Start:", start_input)

        destination_input = QLineEdit()
        destination_input.setPlaceholderText("Vídeň, Bratislava...")
        form_layout.addRow("Cíl:", destination_input)

        company_input = QLineEdit()
        company_input.setPlaceholderText("ABC s.r.o., Hlavní 123...")
        form_layout.addRow("Firma/Adresa:", company_input)

        distance_input = QLineEdit()
        distance_input.setPlaceholderText("150")
        form_layout.addRow("Vzdálenost (km):", distance_input)

        note_input = QLineEdit()
        note_input.setPlaceholderText("Poznámka k trase...")
        form_layout.addRow("Poznámka:", note_input)

        layout.addLayout(form_layout)
        
        # Tlačítka
        button_layout = QHBoxLayout()
        
        cancel_button = QPushButton("❌ Zrušit")
        cancel_button.clicked.connect(dialog.reject)
        button_layout.addWidget(cancel_button)
        
        save_button = QPushButton("✅ Uložit destinaci")
        button_layout.addWidget(save_button)
        
        layout.addLayout(button_layout)

        def save_destination():
            """Uloží destinaci do databáze."""
            if not all([start_input.text(), destination_input.text(), distance_input.text()]):
                QMessageBox.warning(dialog, "Chyba", "Start, cíl a vzdálenost musí být vyplněny!")
                return
                
            try:
                conn = connect()
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO destinations (start, destination, company, distance, note) 
                    VALUES (?, ?, ?, ?, ?)
                """, (start_input.text(), destination_input.text(), company_input.text(), 
                     float(distance_input.text()), note_input.text()))
                conn.commit()
                conn.close()

                self.load_destinations()
                QMessageBox.information(dialog, "✅ Úspěch", "Destinace byla úspěšně přidána!")
                dialog.accept()
            except Exception as e:
                QMessageBox.critical(dialog, "Chyba", f"Chyba při ukládání: {str(e)}")

        save_button.clicked.connect(save_destination)
        dialog.exec()

    def edit_destination(self):
        """Otevře moderní formulář pro úpravu destinace."""
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "⚠️ Chyba", "Nebyl vybrán žádný záznam k úpravě!")
            return

        destination_data = [self.table.item(selected_row, col).text() for col in range(self.table.columnCount())]

        dialog = QDialog(self)
        dialog.setWindowTitle("✏️ Upravit destinaci")
        dialog.setFixedSize(450, 400)
        dialog.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
            }
            QLabel {
                color: white;
                font-weight: bold;
                font-size: 14px;
            }
            QLineEdit {
                background: white;
                border: 2px solid rgba(255,255,255,0.3);
                border-radius: 8px;
                padding: 10px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 2px solid #e67e22;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e67e22, stop:1 #d35400);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px;
                font-weight: bold;
                font-size: 14px;
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
        title_label = QLabel(f"🔧 Úprava destinace ID: {destination_data[0]}")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; margin-bottom: 20px;")
        layout.addWidget(title_label)

        # Formulář
        form_layout = QFormLayout()
        form_layout.setSpacing(12)
        
        start_input = QLineEdit(destination_data[1])
        form_layout.addRow("Start:", start_input)

        destination_input = QLineEdit(destination_data[2])
        form_layout.addRow("Cíl:", destination_input)

        company_input = QLineEdit(destination_data[3])
        form_layout.addRow("Firma/Adresa:", company_input)

        distance_input = QLineEdit(destination_data[4])
        form_layout.addRow("Vzdálenost (km):", distance_input)

        note_input = QLineEdit(destination_data[5])
        form_layout.addRow("Poznámka:", note_input)

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
            """Uloží změny destinace."""
            if not all([start_input.text(), destination_input.text(), distance_input.text()]):
                QMessageBox.warning(dialog, "Chyba", "Start, cíl a vzdálenost musí být vyplněny!")
                return
                
            try:
                conn = connect()
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE destinations SET start=?, destination=?, company=?, distance=?, note=? 
                    WHERE id=?
                """, (start_input.text(), destination_input.text(), company_input.text(), 
                     float(distance_input.text()), note_input.text(), destination_data[0]))
                conn.commit()
                conn.close()

                self.load_destinations()
                QMessageBox.information(dialog, "✅ Úspěch", "Destinace byla úspěšně upravena!")
                dialog.accept()
            except Exception as e:
                QMessageBox.critical(dialog, "Chyba", f"Chyba při ukládání: {str(e)}")

        save_button.clicked.connect(save_changes)
        dialog.exec()

    def delete_destination(self):
        """Smaže destinaci s moderním potvrzovacím dialogem."""
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "⚠️ Chyba", "Nebyl vybrán žádný záznam ke smazání!")
            return

        destination_id = self.table.item(selected_row, 0).text()
        start_name = self.table.item(selected_row, 1).text()
        destination_name = self.table.item(selected_row, 2).text()
        
        # Moderní potvrzovací dialog
        reply = QMessageBox.question(
            self, 
            "🗑️ Potvrzení smazání",
            f"Opravdu chcete smazat destinaci?\n\n"
            f"🗺️ {start_name} → {destination_name}\n\n"
            f"Tato akce je nevratná!",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                conn = connect()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM destinations WHERE id=?", (destination_id,))
                conn.commit()
                conn.close()

                self.load_destinations()
                QMessageBox.information(self, "✅ Úspěch", f"Destinace {start_name} → {destination_name} byla úspěšně smazána!")
            except Exception as e:
                QMessageBox.critical(self, "❌ Chyba", f"Chyba při mazání destinace: {str(e)}")
