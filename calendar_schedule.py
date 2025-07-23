from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFrame, QScrollArea, 
    QGridLayout, QLabel, QPushButton, QComboBox, QDateEdit, QTableWidget, 
    QTableWidgetItem, QMessageBox, QDialog, QFormLayout, QLineEdit, QTextEdit,
    QTimeEdit, QCheckBox, QSpinBox
)
from PyQt6.QtCore import Qt, QDate, QTime, QTimer
from PyQt6.QtGui import QFont
from database import connect
from datetime import datetime, timedelta

class CalendarScheduleWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kalendář a termíny - Projekt & Develop s.r.o.")
        self.setGeometry(200, 200, 1300, 850)
        
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
        self.load_events()
        
        # Timer pro kontrolu připomínek
        self.reminder_timer = QTimer()
        self.reminder_timer.timeout.connect(self.check_reminders)
        self.reminder_timer.start(60000)  # Každou minutu

    def create_header(self, layout):
        """Vytvoří moderní hlavičku"""
        header_frame = QFrame()
        header_frame.setObjectName("headerFrame")
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(20, 20, 20, 20)
        
        # Levá část - informace o sekci
        left_layout = QVBoxLayout()
        
        title_label = QLabel("📅 Kalendář a termíny")
        title_label.setObjectName("titleLabel")
        left_layout.addWidget(title_label)
        
        subtitle_label = QLabel("Plánování úkolů, schůzek a připomínek")
        subtitle_label.setObjectName("subtitleLabel")
        left_layout.addWidget(subtitle_label)
        
        header_layout.addLayout(left_layout)
        header_layout.addStretch()
        
        layout.addWidget(header_frame)
    
    def create_content(self, layout):
        """Vytvoří hlavní obsah okna"""
        
        # Akce s kartami
        actions_frame = self.create_section_frame("⚡ Rychlé akce", "Správa událostí a připomínek")
        actions_grid = QGridLayout()
        actions_grid.setSpacing(15)
        
        # Karty akcí
        actions = [
            ("➕ Nová událost", "Přidat schůzku nebo úkol", self.add_event),
            ("⏰ Připomínky", "Správa připomínek", self.manage_reminders),
            ("📋 Úkoly", "Zobrazit nevyřízené úkoly", self.show_tasks),
            ("📊 Přehled týdne", "Týdenní plán", self.show_weekly_overview),
        ]
        
        for i, (title, desc, func) in enumerate(actions):
            card = self.create_action_card(title, desc, func)
            actions_grid.addWidget(card, 0, i)
        
        actions_frame.layout().addLayout(actions_grid)
        layout.addWidget(actions_frame)
        
        # Filtrování
        filter_frame = self.create_section_frame("🔍 Filtrování", "Zobrazení událostí podle kritérií")
        filter_layout = QHBoxLayout()
        
        # Datum od
        filter_layout.addWidget(QLabel("Od:"))
        self.date_from = QDateEdit()
        self.date_from.setDate(QDate.currentDate())
        self.date_from.setCalendarPopup(True)
        self.date_from.dateChanged.connect(self.load_events)
        filter_layout.addWidget(self.date_from)
        
        # Datum do
        filter_layout.addWidget(QLabel("Do:"))
        self.date_to = QDateEdit()
        self.date_to.setDate(QDate.currentDate().addDays(30))
        self.date_to.setCalendarPopup(True)
        self.date_to.dateChanged.connect(self.load_events)
        filter_layout.addWidget(self.date_to)
        
        # Typ události
        filter_layout.addWidget(QLabel("Typ:"))
        self.type_filter = QComboBox()
        self.type_filter.addItems(["Všechny", "Schůzka", "Úkol", "Připomínka", "Servis", "Splatnost"])
        self.type_filter.currentTextChanged.connect(self.load_events)
        filter_layout.addWidget(self.type_filter)
        
        # Status
        filter_layout.addWidget(QLabel("Status:"))
        self.status_filter = QComboBox()
        self.status_filter.addItems(["Všechny", "Plánováno", "Probíhá", "Dokončeno", "Zrušeno"])
        self.status_filter.currentTextChanged.connect(self.load_events)
        filter_layout.addWidget(self.status_filter)
        
        filter_layout.addStretch()
        
        filter_frame.layout().addLayout(filter_layout)
        layout.addWidget(filter_frame)
        
        # Tabulka událostí
        table_frame = self.create_section_frame("📋 Seznam událostí", "Přehled všech naplánovaných událostí")
        
        # Tabulka událostí
        self.table = QTableWidget(0, 7)
        self.table.setObjectName("dataTable")
        self.table.setHorizontalHeaderLabels([
            "ID", "Název", "Typ", "Datum", "Čas", "Status", "Popis"
        ])
        
        # Nastavení tabulky
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.doubleClicked.connect(self.edit_event)
        
        table_frame.layout().addWidget(self.table)
        
        # Tlačítka pro správu
        buttons_layout = QHBoxLayout()
        
        edit_btn = QPushButton("✏️ Upravit")
        edit_btn.clicked.connect(self.edit_event)
        buttons_layout.addWidget(edit_btn)
        
        delete_btn = QPushButton("🗑️ Smazat")
        delete_btn.clicked.connect(self.delete_event)
        buttons_layout.addWidget(delete_btn)
        
        complete_btn = QPushButton("✅ Dokončit")
        complete_btn.clicked.connect(self.complete_event)
        buttons_layout.addWidget(complete_btn)
        
        buttons_layout.addStretch()
        
        table_frame.layout().addLayout(buttons_layout)
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
        card.setFixedSize(300, 120)
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
                    stop:0 rgba(142, 68, 173, 1.0),
                    stop:1 rgba(109, 89, 122, 1.0));
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
                border: 2px solid rgba(142, 68, 173, 0.1);
                border-radius: 12px;
                margin: 5px;
            }
            
            #actionCard:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(255, 255, 255, 1.0),
                    stop:1 rgba(240, 248, 255, 1.0));
                border: 2px solid rgba(142, 68, 173, 0.3);
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
                border: 1px solid rgba(142, 68, 173, 0.2);
                border-radius: 8px;
                gridline-color: rgba(142, 68, 173, 0.1);
                font-size: 12px;
                selection-background-color: rgba(142, 68, 173, 0.2);
            }
            
            #dataTable::item {
                padding: 8px;
                border: none;
            }
            
            #dataTable::item:selected {
                background: rgba(142, 68, 173, 0.3);
                color: #2c3e50;
            }
            
            QHeaderView::section {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(142, 68, 173, 0.8),
                    stop:1 rgba(142, 68, 173, 0.6));
                color: white;
                font-weight: bold;
                font-size: 11px;
                padding: 8px;
                border: none;
                border-right: 1px solid rgba(255, 255, 255, 0.3);
            }
            
            /* Tlačítka */
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #9b59b6, stop:1 #8e44ad);
                color: white;
                border: none;
                padding: 10px 15px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 12px;
                margin: 2px;
            }
            
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #be7bd6, stop:1 #9b59b6);
            }
            
            /* Combo boxy a datum editory */
            QComboBox, QDateEdit {
                padding: 8px;
                border: 2px solid #e1e8ed;
                border-radius: 6px;
                font-size: 11px;
                background: white;
                margin: 2px;
            }
            
            QComboBox:focus, QDateEdit:focus {
                border-color: #9b59b6;
            }
        """)

    def load_events(self):
        """Načte události z databáze a zobrazí v tabulce."""
        try:
            date_from = self.date_from.date().toString("yyyy-MM-dd")
            date_to = self.date_to.date().toString("yyyy-MM-dd")
            type_filter = self.type_filter.currentText()
            status_filter = self.status_filter.currentText()
            
            cursor = self.db.cursor()
            
            query = """
                SELECT id, title, event_type, event_date, event_time, status, description 
                FROM calendar_events 
                WHERE event_date BETWEEN ? AND ?
            """
            params = [date_from, date_to]
            
            if type_filter != "Všechny":
                query += " AND event_type = ?"
                params.append(type_filter)
                
            if status_filter != "Všechny":
                query += " AND status = ?"
                params.append(status_filter)
                
            query += " ORDER BY event_date, event_time"
            
            cursor.execute(query, params)
            rows = cursor.fetchall()

            self.table.setRowCount(len(rows))
            for row_idx, row in enumerate(rows):
                for col_idx, value in enumerate(row):
                    self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value) if value else ""))
                    
        except Exception as e:
            # Tabulka ještě neexistuje, vytvoříme ji
            self.create_calendar_table()
            QMessageBox.information(self, "Info", "Kalendářová tabulka byla vytvořena. Zkuste znovu.")

    def create_calendar_table(self):
        """Vytvoří tabulku pro kalendář v databázi"""
        try:
            cursor = self.db.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS calendar_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    event_type TEXT,
                    event_date TEXT,
                    event_time TEXT,
                    end_date TEXT,
                    end_time TEXT,
                    status TEXT DEFAULT 'Plánováno',
                    reminder_minutes INTEGER DEFAULT 15,
                    reminder_sent BOOLEAN DEFAULT 0,
                    recurring BOOLEAN DEFAULT 0,
                    recurring_type TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            self.db.commit()
        except Exception as e:
            QMessageBox.critical(self, "Chyba", f"Chyba při vytváření tabulky: {str(e)}")

    def add_event(self):
        """Otevře formulář pro přidání události."""
        dialog = EventDialog()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            try:
                cursor = self.db.cursor()
                cursor.execute("""
                    INSERT INTO calendar_events (title, description, event_type, event_date, 
                                               event_time, reminder_minutes, status) 
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    dialog.title_edit.text(),
                    dialog.description_edit.toPlainText(),
                    dialog.type_combo.currentText(),
                    dialog.date_edit.date().toString("yyyy-MM-dd"),
                    dialog.time_edit.time().toString("HH:mm"),
                    dialog.reminder_spin.value(),
                    "Plánováno"
                ))
                self.db.commit()
                self.load_events()
                QMessageBox.information(self, "Úspěch", "Událost byla úspěšně přidána!")
            except Exception as e:
                QMessageBox.critical(self, "Chyba", f"Chyba při přidávání události: {str(e)}")

    def edit_event(self):
        """Upraví vybranou událost."""
        current_row = self.table.currentRow()
        if current_row >= 0:
            event_id = self.table.item(current_row, 0).text()
            
            # Načteme data události
            cursor = self.db.cursor()
            cursor.execute("""
                SELECT title, description, event_type, event_date, event_time, 
                       reminder_minutes, status 
                FROM calendar_events WHERE id = ?
            """, (event_id,))
            result = cursor.fetchone()
            
            if result:
                dialog = EventDialog()
                dialog.title_edit.setText(result[0] or "")
                dialog.description_edit.setPlainText(result[1] or "")
                dialog.type_combo.setCurrentText(result[2] or "")
                dialog.date_edit.setDate(QDate.fromString(result[3], "yyyy-MM-dd"))
                dialog.time_edit.setTime(QTime.fromString(result[4], "HH:mm"))
                dialog.reminder_spin.setValue(int(result[5]) if result[5] else 15)
                
                if dialog.exec() == QDialog.DialogCode.Accepted:
                    try:
                        cursor.execute("""
                            UPDATE calendar_events 
                            SET title = ?, description = ?, event_type = ?, event_date = ?, 
                                event_time = ?, reminder_minutes = ?
                            WHERE id = ?
                        """, (
                            dialog.title_edit.text(),
                            dialog.description_edit.toPlainText(),
                            dialog.type_combo.currentText(),
                            dialog.date_edit.date().toString("yyyy-MM-dd"),
                            dialog.time_edit.time().toString("HH:mm"),
                            dialog.reminder_spin.value(),
                            event_id
                        ))
                        self.db.commit()
                        self.load_events()
                        QMessageBox.information(self, "Úspěch", "Událost byla úspěšně upravena!")
                    except Exception as e:
                        QMessageBox.critical(self, "Chyba", f"Chyba při upravování události: {str(e)}")
        else:
            QMessageBox.warning(self, "Upozornění", "Vyberte událost pro úpravu!")

    def delete_event(self):
        """Smaže vybranou událost."""
        current_row = self.table.currentRow()
        if current_row >= 0:
            event_title = self.table.item(current_row, 1).text()
            
            reply = QMessageBox.question(
                self, 
                "Potvrzení smazání", 
                f"Opravdu chcete smazat událost '{event_title}'?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                event_id = self.table.item(current_row, 0).text()
                try:
                    cursor = self.db.cursor()
                    cursor.execute("DELETE FROM calendar_events WHERE id = ?", (event_id,))
                    self.db.commit()
                    self.load_events()
                    QMessageBox.information(self, "Úspěch", "Událost byla úspěšně smazána!")
                except Exception as e:
                    QMessageBox.critical(self, "Chyba", f"Chyba při mazání události: {str(e)}")
        else:
            QMessageBox.warning(self, "Upozornění", "Vyberte událost pro smazání!")

    def complete_event(self):
        """Označí událost jako dokončenou."""
        current_row = self.table.currentRow()
        if current_row >= 0:
            event_id = self.table.item(current_row, 0).text()
            try:
                cursor = self.db.cursor()
                cursor.execute("UPDATE calendar_events SET status = 'Dokončeno' WHERE id = ?", (event_id,))
                self.db.commit()
                self.load_events()
                QMessageBox.information(self, "Úspěch", "Událost byla označena jako dokončená!")
            except Exception as e:
                QMessageBox.critical(self, "Chyba", f"Chyba při dokončování události: {str(e)}")
        else:
            QMessageBox.warning(self, "Upozornění", "Vyberte událost pro dokončení!")

    def manage_reminders(self):
        """Zobrazí správu připomínek."""
        QMessageBox.information(self, "⏰ Připomínky", 
                              "Funkce správy připomínek je aktivní.\n\n"
                              "Systém kontroluje:\n"
                              "• Nadcházející události\n"
                              "• Splatnosti faktur\n"
                              "• Servisní termíny\n\n"
                              "Připomínky se zobrazují automaticky.")

    def show_tasks(self):
        """Zobrazí nevyřízené úkoly."""
        try:
            cursor = self.db.cursor()
            cursor.execute("""
                SELECT title, event_date FROM calendar_events 
                WHERE status = 'Plánováno' AND event_type = 'Úkol'
                ORDER BY event_date
            """)
            tasks = cursor.fetchall()
            
            if tasks:
                task_list = "\n".join([f"• {task[0]} ({task[1]})" for task in tasks])
                QMessageBox.information(self, "📋 Nevyřízené úkoly", f"Úkoly k vyřízení:\n\n{task_list}")
            else:
                QMessageBox.information(self, "📋 Úkoly", "Žádné nevyřízené úkoly!")
                
        except Exception as e:
            QMessageBox.critical(self, "Chyba", f"Chyba při načítání úkolů: {str(e)}")

    def show_weekly_overview(self):
        """Zobrazí týdenní přehled."""
        try:
            from datetime import datetime, timedelta
            
            # Získání začátku a konce týdne
            today = datetime.now()
            start_of_week = today - timedelta(days=today.weekday())
            end_of_week = start_of_week + timedelta(days=6)
            
            cursor = self.db.cursor()
            cursor.execute("""
                SELECT title, event_date, event_time, event_type, status
                FROM calendar_events 
                WHERE event_date BETWEEN ? AND ?
                ORDER BY event_date, event_time
            """, (
                start_of_week.strftime('%Y-%m-%d'),
                end_of_week.strftime('%Y-%m-%d')
            ))
            events = cursor.fetchall()
            
            # Sestavení přehledu
            weekly_text = f"📅 Týdenní přehled ({start_of_week.strftime('%d.%m')} - {end_of_week.strftime('%d.%m.%Y')})\n\n"
            
            if events:
                current_date = None
                for event in events:
                    event_date = datetime.strptime(event[1], '%Y-%m-%d')
                    
                    # Nový den
                    if current_date != event_date.date():
                        current_date = event_date.date()
                        day_name = ['Pondělí', 'Úterý', 'Středa', 'Čtvrtek', 'Pátek', 'Sobota', 'Neděle'][event_date.weekday()]
                        weekly_text += f"\n🗓️ {day_name} {event_date.strftime('%d.%m')}\n"
                    
                    # Událost
                    time_str = event[2] if event[2] else "Celý den"
                    status_icon = "✅" if event[4] == "Dokončeno" else "⏳"
                    type_icon = "📋" if event[3] == "Úkol" else "📅"
                    
                    weekly_text += f"  {status_icon} {type_icon} {time_str} - {event[0]}\n"
            else:
                weekly_text += "📭 Tento týden nemáte naplánované žádné události."
            
            # Zobrazení v dialogu
            dialog = WeeklyViewDialog(weekly_text, self)
            dialog.exec()
            
        except Exception as e:
            QMessageBox.critical(self, "Chyba", f"Chyba při načítání týdenního přehledu: {str(e)}")

    def check_reminders(self):
        """Kontroluje připomínky každou minutu."""
        try:
            cursor = self.db.cursor()
            now = datetime.now()
            
            # Kontrola událostí s připomínkami
            cursor.execute("""
                SELECT id, title, event_date, event_time, reminder_minutes 
                FROM calendar_events 
                WHERE status = 'Plánováno' AND reminder_sent = 0
            """)
            events = cursor.fetchall()
            
            for event_id, title, event_date, event_time, reminder_minutes in events:
                event_datetime = datetime.strptime(f"{event_date} {event_time}", "%Y-%m-%d %H:%M")
                reminder_time = event_datetime - timedelta(minutes=reminder_minutes)
                
                if now >= reminder_time:
                    QMessageBox.information(self, "⏰ Připomínka", 
                                          f"Připomínka události:\n\n"
                                          f"📅 {title}\n"
                                          f"🕐 {event_date} v {event_time}")
                    
                    # Označit připomínku jako odeslanou
                    cursor.execute("UPDATE calendar_events SET reminder_sent = 1 WHERE id = ?", (event_id,))
                    self.db.commit()
                    
        except Exception as e:
            print(f"Chyba při kontrole připomínek: {e}")

    def closeEvent(self, event):
        """Uzavře databázové připojení při zavření okna"""
        if hasattr(self, 'db'):
            self.db.close()
        event.accept()


class EventDialog(QDialog):
    """Dialog pro přidání/úpravu události"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Událost")
        self.setFixedSize(500, 600)
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f6fa;
            }
            QLabel {
                font-size: 12px;
                font-weight: bold;
                color: #2c3e50;
                margin-bottom: 5px;
            }
            QLineEdit, QComboBox, QTextEdit, QDateEdit, QTimeEdit, QSpinBox {
                padding: 10px;
                border: 2px solid #e1e8ed;
                border-radius: 8px;
                font-size: 12px;
                background: white;
                margin-bottom: 10px;
            }
            QLineEdit:focus, QComboBox:focus, QTextEdit:focus, 
            QDateEdit:focus, QTimeEdit:focus, QSpinBox:focus {
                border-color: #9b59b6;
            }
            QTextEdit {
                min-height: 80px;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #9b59b6, stop:1 #8e44ad);
                color: white;
                border: none;
                padding: 12px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #be7bd6, stop:1 #9b59b6);
            }
            QPushButton:pressed {
                background: #8e44ad;
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
        self.title_edit.setPlaceholderText("Název události")
        form_layout.addRow("Název:", self.title_edit)
        
        self.type_combo = QComboBox()
        self.type_combo.addItems([
            "Schůzka",
            "Úkol", 
            "Připomínka",
            "Servis",
            "Splatnost",
            "Ostatní"
        ])
        form_layout.addRow("Typ:", self.type_combo)
        
        self.description_edit = QTextEdit()
        self.description_edit.setPlaceholderText("Popis události")
        form_layout.addRow("Popis:", self.description_edit)
        
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        form_layout.addRow("Datum:", self.date_edit)
        
        self.time_edit = QTimeEdit()
        self.time_edit.setTime(QTime.currentTime())
        form_layout.addRow("Čas:", self.time_edit)
        
        self.reminder_spin = QSpinBox()
        self.reminder_spin.setMaximum(1440)  # Max 24 hodin
        self.reminder_spin.setValue(15)
        self.reminder_spin.setSuffix(" min")
        form_layout.addRow("Připomínka před:", self.reminder_spin)
        
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


class WeeklyViewDialog(QDialog):
    """Dialog pro zobrazení týdenního přehledu"""
    
    def __init__(self, weekly_text, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Týdenní přehled")
        self.setFixedSize(600, 500)
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f6fa;
            }
            QTextEdit {
                border: 2px solid #e1e8ed;
                border-radius: 8px;
                font-size: 12px;
                background: white;
                font-family: 'Courier New', monospace;
                line-height: 1.4;
                padding: 15px;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3498db, stop:1 #2980b9);
                color: white;
                border: none;
                padding: 12px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 12px;
                min-width: 100px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5dade2, stop:1 #3498db);
            }
        """)
        
        self.setup_ui(weekly_text)
    
    def setup_ui(self, weekly_text):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Text area
        self.text_edit = QTextEdit()
        self.text_edit.setPlainText(weekly_text)
        self.text_edit.setReadOnly(True)
        layout.addWidget(self.text_edit)
        
        # Tlačítka
        button_layout = QHBoxLayout()
        
        self.close_button = QPushButton("Zavřít")
        self.close_button.clicked.connect(self.accept)
        button_layout.addStretch()
        button_layout.addWidget(self.close_button)
        
        layout.addLayout(button_layout)
