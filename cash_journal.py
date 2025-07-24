from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QPushButton, QTableWidgetItem,
    QDialog, QFormLayout, QLabel, QLineEdit, QMessageBox, QComboBox, QDateEdit,
    QFrame, QScrollArea, QGridLayout
)
from PyQt6.QtCore import QDate, Qt
from PyQt6.QtGui import QFont, QBrush, QColor
from database import connect


class CashJournalWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pokladní deník - Projekt & Develop s.r.o.")
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
        self.load_cash_journal()

    def create_header(self, layout):
        """Vytvoří moderní hlavičku"""
        header_frame = QFrame()
        header_frame.setObjectName("headerFrame")
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(20, 20, 20, 20)
        
        # Levá část - informace o sekci
        left_layout = QVBoxLayout()
        
        title_label = QLabel("💰 Pokladní deník")
        title_label.setObjectName("titleLabel")
        left_layout.addWidget(title_label)
        
        subtitle_label = QLabel("Evidence příjmů a výdajů pokladny")
        subtitle_label.setObjectName("subtitleLabel")
        left_layout.addWidget(subtitle_label)
        
        header_layout.addLayout(left_layout)
        header_layout.addStretch()
        
        layout.addWidget(header_frame)
    
    def create_content(self, layout):
        """Vytvoří hlavní obsah okna"""
        
        # Akce s kartami
        actions_frame = self.create_section_frame("⚡ Rychlé akce", "Správa záznamů pokladny")
        actions_grid = QGridLayout()
        actions_grid.setSpacing(15)
        
        # Karty akcí
        actions = [
            ("➕ Přidat záznam", "Nový příjem nebo výdaj", self.add_entry),
            ("✏️ Upravit záznam", "Upravit vybraný záznam", self.edit_entry),
            ("🗑️ Smazat záznam", "Odstranit záznam", self.delete_entry),
            ("⚙️ Počáteční stav", "Nastavit základní zůstatek", self.set_initial_balance),
        ]
        
        for i, (title, desc, func) in enumerate(actions):
            card = self.create_action_card(title, desc, func)
            actions_grid.addWidget(card, i // 2, i % 2)
        
        actions_frame.layout().addLayout(actions_grid)
        layout.addWidget(actions_frame)
        
        # Tabulka záznamů
        table_frame = self.create_section_frame("📋 Záznamy pokladny", "Přehled všech pohybů v pokladně")
        
        # Tabulka pokladního deníku
        self.table = QTableWidget(0, 7)
        self.table.setObjectName("dataTable")
        self.table.setHorizontalHeaderLabels([
            "ID", "Typ", "Datum", "Jméno", "Částka", "Poznámka", "Zůstatek"
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
    
    def load_cash_journal(self):
        """Načte pokladní deník z databáze a vizuálně zvýrazní transakce barevným pozadím."""
        # Blokujeme signály pro zabránění varování dataChanged
        self.table.blockSignals(True)
        
        try:
            conn = connect()
            cursor = conn.cursor()

            cursor.execute("SELECT id, type, date, person, amount, note, balance FROM cash_journal ORDER BY date ASC")
            rows = cursor.fetchall()
            conn.close()

            # Vyčistíme tabulku a nastavíme počet řádků
            self.table.clearContents()
            self.table.setRowCount(len(rows))

            for row_idx, row in enumerate(rows):
                for col_idx, value in enumerate(row):
                    item = QTableWidgetItem(str(value))

                    # Barevné pozadí řádku podle typu transakce
                    if row[1] == "Příjem":  # Pokud je typ Příjem
                        item.setBackground(QBrush(QColor("#C8E6C9")))  # Světle zelené pozadí
                    elif row[1] == "Výdaj":  # Pokud je typ Výdaj
                        item.setBackground(QBrush(QColor("#FFCC80")))  # Světle oranžové pozadí
                    elif row[1] == "Počáteční stav":  # Pokud je typ Počáteční stav
                        item.setBackground(QBrush(QColor("#E1BEE7")))  # Světle magenta pozadí
                    
                    # Zvýraznění aktuálního stavu pokladny (poslední řádek)
                    if col_idx == 6 and row_idx == len(rows) - 1:  
                        item.setFont(QFont("Arial", 14, QFont.Weight.Bold))  
                        
                        # Barevné zvýraznění zůstatku (zelená pokud kladný, červená pokud záporný)
                        if float(value) >= 0:
                            item.setForeground(QBrush(QColor("green")))
                        else:
                            item.setForeground(QBrush(QColor("red")))

                    self.table.setItem(row_idx, col_idx, item)

            # Skryjeme ID sloupec
            self.table.setColumnHidden(0, True)
            
        finally:
            # Obnovíme signály
            self.table.blockSignals(False)

    def add_entry(self):
        """Otevře dialog pro přidání nového záznamu do pokladního deníku."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Nový záznam")
        layout = QFormLayout()

        type_box = QComboBox()
        type_box.addItems(["Příjem", "Výdaj"])
        layout.addRow(QLabel("Typ:"), type_box)

        date_input = QDateEdit()
        date_input.setCalendarPopup(True)
        date_input.setDate(QDate.currentDate())
        layout.addRow(QLabel("Datum:"), date_input)

        person_input = QLineEdit()
        layout.addRow(QLabel("Jméno:"), person_input)

        amount_input = QLineEdit()
        layout.addRow(QLabel("Částka:"), amount_input)

        note_input = QLineEdit()
        layout.addRow(QLabel("Poznámka:"), note_input)

        save_button = QPushButton("Uložit záznam")
        layout.addWidget(save_button)

        def save_entry():
            """Uloží nový záznam do databáze a správně aktualizuje zůstatek."""
            try:
                conn = connect()
                cursor = conn.cursor()

                # Získání posledního známého zůstatku (nejnovější transakce)
                cursor.execute("SELECT balance FROM cash_journal ORDER BY id DESC LIMIT 1")
                last_balance = cursor.fetchone()
                last_balance = last_balance[0] if last_balance else 0  # Pokud není žádný záznam, počáteční stav je 0

                # Výpočet nového zůstatku - podporuje čárku i tečku jako desetinnou čárku
                amount_text = amount_input.text().replace(",", ".")
                amount = float(amount_text)
                new_balance = last_balance + amount if type_box.currentText() == "Příjem" else last_balance - amount

                # Vložení nové transakce s aktualizovaným zůstatkem
                cursor.execute("""
                    INSERT INTO cash_journal (type, date, person, amount, note, balance)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (type_box.currentText(), date_input.date().toString("yyyy-MM-dd"), person_input.text(),
                    amount, note_input.text(), new_balance))

                conn.commit()
                conn.close()

                self.load_cash_journal()
                QMessageBox.information(self, "Úspěch", "Záznam byl úspěšně přidán!")
                dialog.accept()
            except ValueError:
                QMessageBox.warning(self, "Chyba", "Částka musí být číslo!")
            except Exception as e:
                QMessageBox.critical(self, "Chyba", f"Nastala chyba: {str(e)}")

        save_button.clicked.connect(save_entry)
        dialog.setLayout(layout)
        dialog.exec()

    def delete_entry(self):
        """Smaže vybraný záznam z pokladního deníku."""
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Chyba", "Nebyl vybrán žádný záznam!")
            return

        entry_id = self.table.item(selected_row, 0).text()  # Získání ID z prvního sloupce

        # Potvrzení smazání
        reply = QMessageBox.question(self, "Potvrzení", 
                                   "Opravdu chcete smazat vybraný záznam?",
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                conn = connect()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM cash_journal WHERE id=?", (entry_id,))
                conn.commit()
                conn.close()

                self.load_cash_journal()
                QMessageBox.information(self, "Úspěch", f"Záznam byl úspěšně smazán!")
            except Exception as e:
                QMessageBox.critical(self, "Chyba", f"Nastala chyba při mazání: {str(e)}")

    def set_initial_balance(self):
        """Otevře dialog pro zadání počátečního stavu pokladny."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Počáteční stav pokladny")
        layout = QFormLayout()

        balance_input = QLineEdit()
        layout.addRow(QLabel("Počáteční zůstatek:"), balance_input)

        save_button = QPushButton("Uložit počáteční stav")
        layout.addWidget(save_button)

        def save_initial_balance():
            """Uloží počáteční stav pokladny do databáze."""
            try:
                initial_amount_text = balance_input.text().replace(",", ".")
                initial_amount = float(initial_amount_text)
                conn = connect()
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO cash_journal (type, date, person, amount, note, balance) 
                    VALUES ('Počáteční stav', ?, 'Systém', ?, 'Zadáno uživatelem', ?)
                """, (QDate.currentDate().toString("yyyy-MM-dd"), initial_amount, initial_amount))
                conn.commit()
                conn.close()

                self.load_cash_journal()
                QMessageBox.information(self, "Úspěch", "Počáteční stav pokladny byl uložen!")
                dialog.accept()
            except ValueError:
                QMessageBox.warning(self, "Chyba", "Částka musí být číslo!")
            except Exception as e:
                QMessageBox.critical(self, "Chyba", f"Nastala chyba: {str(e)}")

        save_button.clicked.connect(save_initial_balance)
        dialog.setLayout(layout)
        dialog.exec()

    def edit_entry(self):
        """Otevře dialog pro úpravu vybraného záznamu."""
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Chyba", "Nebyl vybrán žádný záznam!")
            return

        # Získání hodnot z tabulky (ID je skryté, ale stále přístupné)
        entry_id = self.table.item(selected_row, 0).text()  # ID z prvního sloupce
        entry_data = [self.table.item(selected_row, col).text() for col in range(1, self.table.columnCount())]

        dialog = QDialog(self)
        dialog.setWindowTitle("Upravit záznam")
        layout = QFormLayout()

        type_box = QComboBox()
        type_box.addItems(["Příjem", "Výdaj", "Počáteční stav"])
        type_box.setCurrentText(entry_data[0])  # Typ je na indexu 0 (po ID)
        layout.addRow(QLabel("Typ:"), type_box)

        date_input = QDateEdit()
        date_input.setCalendarPopup(True)
        date_input.setDate(QDate.fromString(entry_data[1], "yyyy-MM-dd"))  # Datum na indexu 1
        layout.addRow(QLabel("Datum:"), date_input)

        person_input = QLineEdit(entry_data[2])  # Jméno na indexu 2
        layout.addRow(QLabel("Jméno:"), person_input)

        amount_input = QLineEdit(entry_data[3])  # Částka na indexu 3
        layout.addRow(QLabel("Částka:"), amount_input)

        note_input = QLineEdit(entry_data[4])  # Poznámka na indexu 4
        layout.addRow(QLabel("Poznámka:"), note_input)

        save_button = QPushButton("Uložit změny")
        layout.addWidget(save_button)

        def save_changes():
            """Uloží upravený záznam do databáze."""
            try:
                amount_text = amount_input.text().replace(",", ".")
                amount = float(amount_text)
                conn = connect()
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE cash_journal
                    SET type=?, date=?, person=?, amount=?, note=? 
                    WHERE id=?
                """, (type_box.currentText(), date_input.date().toString("yyyy-MM-dd"), person_input.text(), 
                    amount, note_input.text(), entry_id))

                conn.commit()
                conn.close()

                self.load_cash_journal()
                QMessageBox.information(self, "Úspěch", "Záznam byl úspěšně upraven!")
                dialog.accept()
            except ValueError:
                QMessageBox.warning(self, "Chyba", "Částka musí být číslo!")
            except Exception as e:
                QMessageBox.critical(self, "Chyba", f"Nastala chyba: {str(e)}")

        save_button.clicked.connect(save_changes)
        dialog.setLayout(layout)
        dialog.exec()
