from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTableWidget, QPushButton, QTableWidgetItem, \
    QDialog, QFormLayout, QLabel, QLineEdit, QMessageBox, QComboBox, QDateEdit
from PyQt6.QtCore import QDate
from database import connect
from PyQt6.QtGui import QFont, QBrush, QColor


class CashJournalWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pokladní deník")
        self.setGeometry(200, 200, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        # Tabulka pokladního deníku
        self.table = QTableWidget(0, 7)
        self.table.setHorizontalHeaderLabels(["ID", "Typ", "Datum", "Jméno", "Částka", "Poznámka", "Zůstatek"])
        layout.addWidget(self.table)

        self.load_cash_journal()

        # Tlačítka pro správu pokladního deníku
        self.add_button = QPushButton("Přidat záznam")
        self.add_button.clicked.connect(self.add_entry)
        layout.addWidget(self.add_button)

        self.delete_button = QPushButton("Smazat záznam")
        self.delete_button.clicked.connect(self.delete_entry)
        layout.addWidget(self.delete_button)

        self.edit_button = QPushButton("Upravit záznam")
        self.edit_button.clicked.connect(self.edit_entry)
        layout.addWidget(self.edit_button)

        self.initial_balance_button = QPushButton("Nastavit počáteční stav")
        self.initial_balance_button.clicked.connect(self.set_initial_balance)
        layout.addWidget(self.initial_balance_button)

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

    def load_cash_journal(self):
        """Načte pokladní deník z databáze a vizuálně zvýrazní transakce barevným pozadím."""
        conn = connect()
        cursor = conn.cursor()

        cursor.execute("SELECT id, type, date, person, amount, note, balance FROM cash_journal ORDER BY date ASC")
        rows = cursor.fetchall()
        conn.close()

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
