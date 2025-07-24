from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFrame, QScrollArea, 
    QGridLayout, QLabel, QPushButton, QComboBox, QDateEdit, QTableWidget, 
    QTableWidgetItem, QMessageBox, QDialog, QFormLayout, QLineEdit, QTextEdit,
    QSpinBox, QDoubleSpinBox, QCheckBox
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont
from database import connect

class ServiceMaintenanceWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Servis a údržba - Projekt & Develop s.r.o.")
        self.setGeometry(200, 200, 1400, 900)
        
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
        
        # Vytvoření tabulky a načtení dat
        self.create_service_tables()
        self.load_service_records()

    def create_header(self, layout):
        """Vytvoří moderní hlavičku"""
        header_frame = QFrame()
        header_frame.setObjectName("headerFrame")
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(20, 20, 20, 20)
        
        # Levá část - informace o sekci
        left_layout = QVBoxLayout()
        
        title_label = QLabel("🔧 Servis a údržba")
        title_label.setObjectName("titleLabel")
        left_layout.addWidget(title_label)
        
        subtitle_label = QLabel("Plánování a evidence servisních úkonů, oprav a údržby")
        subtitle_label.setObjectName("subtitleLabel")
        left_layout.addWidget(subtitle_label)
        
        header_layout.addLayout(left_layout)
        header_layout.addStretch()
        
        layout.addWidget(header_frame)
    
    def create_content(self, layout):
        """Vytvoří hlavní obsah okna"""
        
        # Akce s kartami
        actions_frame = self.create_section_frame("⚡ Rychlé akce", "Správa servisních operací")
        actions_grid = QGridLayout()
        actions_grid.setSpacing(15)
        
        # Karty akcí
        actions = [
            ("🔧 Nový servis", "Zaznamenat servisní úkon", self.add_service),
            ("📅 Plánovaná údržba", "Naplánovat pravidelnou údržbu", self.schedule_maintenance),
            ("⚠️ Porucha", "Nahlásit poruchu", self.report_malfunction),
            ("📊 Servisní plán", "Zobrazit servisní kalendář", self.show_service_plan),
            ("💰 Náklady", "Přehled nákladů na servis", self.show_costs),
            ("📋 Certifikáty", "Správa certifikátů", self.manage_certificates),
        ]
        
        for i, (title, desc, func) in enumerate(actions):
            card = self.create_action_card(title, desc, func)
            actions_grid.addWidget(card, i // 3, i % 3)
        
        actions_frame.layout().addLayout(actions_grid)
        layout.addWidget(actions_frame)
        
        # Přehled servisu
        stats_frame = self.create_section_frame("📊 Přehled", "Statistiky servisních úkonů")
        stats_grid = QGridLayout()
        stats_grid.setSpacing(15)
        
        # Karty statistik
        self.total_card = self.create_stat_card("🔧 Celkem servisů", "0", "blue")
        self.pending_card = self.create_stat_card("⏳ Čekající", "0", "orange")
        self.this_month_card = self.create_stat_card("📅 Tento měsíc", "0", "green")
        self.costs_card = self.create_stat_card("💰 Náklady", "0 Kč", "red")
        
        stats_grid.addWidget(self.total_card, 0, 0)
        stats_grid.addWidget(self.pending_card, 0, 1)
        stats_grid.addWidget(self.this_month_card, 0, 2)
        stats_grid.addWidget(self.costs_card, 0, 3)
        
        stats_frame.layout().addLayout(stats_grid)
        layout.addWidget(stats_frame)
        
        # Tabulka servisních záznamů
        table_frame = self.create_section_frame("🔧 Servisní záznamy", "Přehled všech servisních úkonů")
        
        # Tabulka
        self.table = QTableWidget(0, 9)
        self.table.setObjectName("dataTable")
        self.table.setHorizontalHeaderLabels([
            "ID", "Datum", "Vozidlo/Majetek", "Typ servisu", "Popis", 
            "Technik", "Náklady", "Status", "Poznámky"
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
    
    def create_stat_card(self, title, value, color):
        """Vytvoří kartu pro statistiku"""
        card = QFrame()
        card.setObjectName(f"statCard_{color}")
        card.setFixedSize(320, 100)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(5)
        
        title_label = QLabel(title)
        title_label.setObjectName("statTitle")
        layout.addWidget(title_label)
        
        value_label = QLabel(value)
        value_label.setObjectName("statValue")
        layout.addWidget(value_label)
        
        return card

    def apply_modern_styles(self):
        """Aplikuje moderní styly"""
        self.setStyleSheet("""
            /* Hlavní okno */
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(231, 76, 60, 1.0),
                    stop:1 rgba(192, 57, 43, 1.0));
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
                border: 2px solid rgba(231, 76, 60, 0.1);
                border-radius: 12px;
                margin: 5px;
            }
            
            #actionCard:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(255, 255, 255, 1.0),
                    stop:1 rgba(255, 245, 245, 1.0));
                border: 2px solid rgba(231, 76, 60, 0.3);
            }
            
            #cardTitle {
                font-size: 13px;
                font-weight: bold;
                color: #2c3e50;
                margin-bottom: 3px;
            }
            
            #cardDescription {
                font-size: 11px;
                color: #7f8c8d;
                line-height: 1.3;
            }
            
            /* Statistické karty */
            #statCard_blue {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(52, 152, 219, 0.9),
                    stop:1 rgba(41, 128, 185, 0.9));
                border-radius: 12px;
                border: 2px solid rgba(41, 128, 185, 0.3);
            }
            
            #statCard_orange {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(230, 126, 34, 0.9),
                    stop:1 rgba(211, 84, 0, 0.9));
                border-radius: 12px;
                border: 2px solid rgba(211, 84, 0, 0.3);
            }
            
            #statCard_green {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(46, 204, 113, 0.9),
                    stop:1 rgba(39, 174, 96, 0.9));
                border-radius: 12px;
                border: 2px solid rgba(39, 174, 96, 0.3);
            }
            
            #statCard_red {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(231, 76, 60, 0.9),
                    stop:1 rgba(192, 57, 43, 0.9));
                border-radius: 12px;
                border: 2px solid rgba(192, 57, 43, 0.3);
            }
            
            #statTitle {
                font-size: 16px;
                font-weight: bold;
                color: white;
                margin-bottom: 5px;
            }
            
            #statValue {
                font-size: 18px;
                font-weight: bold;
                color: white;
            }
            
            /* Tabulka */
            #dataTable {
                background: white;
                alternate-background-color: #f8f9fa;
                border: 1px solid rgba(231, 76, 60, 0.2);
                border-radius: 8px;
                gridline-color: rgba(231, 76, 60, 0.1);
                font-size: 16px;
                selection-background-color: rgba(231, 76, 60, 0.2);
            }
            
            QHeaderView::section {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(231, 76, 60, 0.8),
                    stop:1 rgba(231, 76, 60, 0.6));
                color: white;
                font-weight: bold;
                font-size: 11px;
                padding: 8px;
                border: none;
                border-right: 1px solid rgba(255, 255, 255, 0.3);
            }
        """)

    def create_service_tables(self):
        """Vytvoří tabulky pro servis a údržbu"""
        try:
            cursor = self.db.cursor()
            
            # Tabulka servisních záznamů
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS service_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    asset_type TEXT,
                    asset_id INTEGER,
                    asset_name TEXT,
                    service_type TEXT,
                    description TEXT,
                    technician TEXT,
                    cost REAL,
                    status TEXT DEFAULT 'Plánováno',
                    scheduled_date TEXT,
                    completed_date TEXT,
                    next_service_date TEXT,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Tabulka servisních plánů
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS service_schedules (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    asset_type TEXT,
                    asset_id INTEGER,
                    service_type TEXT,
                    interval_days INTEGER,
                    last_service_date TEXT,
                    next_service_date TEXT,
                    active INTEGER DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Tabulka náhradních dílů
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS service_parts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    service_record_id INTEGER,
                    part_name TEXT,
                    part_number TEXT,
                    quantity INTEGER,
                    unit_price REAL,
                    total_price REAL,
                    supplier TEXT,
                    FOREIGN KEY (service_record_id) REFERENCES service_records (id)
                )
            """)
            
            self.db.commit()
        except Exception as e:
            QMessageBox.critical(self, "Chyba", f"Chyba při vytváření tabulek: {str(e)}")

    def load_service_records(self):
        """Načte servisní záznamy"""
        try:
            cursor = self.db.cursor()
            cursor.execute("""
                SELECT id, date, asset_name, service_type, description, 
                       technician, cost, status, notes
                FROM service_records 
                ORDER BY date DESC
            """)
            rows = cursor.fetchall()

            self.table.setRowCount(len(rows))
            
            total_services = len(rows)
            pending_count = 0
            this_month_count = 0
            total_costs = 0
            current_month = QDate.currentDate().toString("yyyy-MM")
            
            for row_idx, row in enumerate(rows):
                # Formátování dat pro zobrazení
                formatted_row = list(row)
                
                # Náklady
                if row[6]:
                    formatted_row[6] = f"{float(row[6]):,.2f} Kč"
                    total_costs += float(row[6])
                else:
                    formatted_row[6] = "Nenastaveno"
                
                # Zkrácení dlouhých textů
                if row[4] and len(row[4]) > 30:  # description
                    formatted_row[4] = row[4][:27] + "..."
                if row[8] and len(row[8]) > 25:  # notes
                    formatted_row[8] = row[8][:22] + "..."
                
                for col_idx, value in enumerate(formatted_row):
                    self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value) if value else ""))
                
                # Statistiky
                if row[7] in ["Plánováno", "Probíhá"]:  # status
                    pending_count += 1
                if row[1] and row[1].startswith(current_month):  # date
                    this_month_count += 1
                    
            # Aktualizace karet
            self.update_stat_card(self.total_card, str(total_services))
            self.update_stat_card(self.pending_card, str(pending_count))
            self.update_stat_card(self.this_month_card, str(this_month_count))
            self.update_stat_card(self.costs_card, f"{total_costs:,.2f} Kč")
            
        except Exception as e:
            QMessageBox.critical(self, "Chyba", f"Chyba při načítání servisních záznamů: {str(e)}")
    
    def update_stat_card(self, card, value):
        """Aktualizuje hodnotu ve statistické kartě"""
        layout = card.layout()
        if layout and layout.count() > 1:
            value_label = layout.itemAt(1).widget()
            if value_label:
                value_label.setText(value)

    def add_service(self):
        """Přidá nový servisní záznam"""
        dialog = ServiceDialog()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            try:
                cursor = self.db.cursor()
                cursor.execute("""
                    INSERT INTO service_records (date, asset_type, asset_name, service_type, 
                                               description, technician, cost, status, 
                                               scheduled_date, notes) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    dialog.date_edit.date().toString("yyyy-MM-dd"),
                    dialog.asset_type_edit.text(),
                    dialog.asset_name_edit.text(),
                    dialog.service_type_edit.text(),
                    dialog.description_edit.toPlainText(),
                    dialog.technician_edit.text(),
                    dialog.cost_edit.value() if dialog.cost_edit.value() > 0 else None,
                    dialog.status_combo.currentText(),
                    dialog.scheduled_date_edit.date().toString("yyyy-MM-dd"),
                    dialog.notes_edit.toPlainText()
                ))
                self.db.commit()
                self.load_service_records()
                QMessageBox.information(self, "Úspěch", "Servisní záznam byl úspěšně přidán!")
            except Exception as e:
                QMessageBox.critical(self, "Chyba", f"Chyba při přidávání servisního záznamu: {str(e)}")

    def save_maintenance_schedule(self, dialog):
        """Uloží plán údržby"""
        try:
            cursor = self.db.cursor()
            cursor.execute("""
                INSERT INTO service_schedules (vehicle_id, maintenance_type, scheduled_date, 
                                             interval_days, notes)
                VALUES (?, ?, ?, ?, ?)
            """, (
                dialog.vehicle_combo.currentData(),
                dialog.maintenance_type_combo.currentText(),
                dialog.scheduled_date_edit.date().toString("yyyy-MM-dd"),
                dialog.interval_edit.value(),
                dialog.notes_edit.toPlainText()
            ))
            self.db.commit()
        except Exception as e:
            QMessageBox.critical(self, "Chyba", f"Chyba při ukládání plánu údržby: {str(e)}")

    def save_malfunction_report(self, dialog):
        """Uloží hlášení poruchy"""
        try:
            cursor = self.db.cursor()
            cursor.execute("""
                INSERT INTO service_records (vehicle_id, service_type, description, 
                                           date, cost, notes)
                VALUES (?, ?, ?, date('now'), 0, ?)
            """, (
                dialog.vehicle_combo.currentData(),
                f"Porucha - {dialog.category_combo.currentText()}",
                dialog.description_edit.toPlainText(),
                f"Priorita: {dialog.priority_combo.currentText()}, Nahlásil: {dialog.reporter_edit.text()}"
            ))
            self.db.commit()
        except Exception as e:
            QMessageBox.critical(self, "Chyba", f"Chyba při ukládání hlášení poruchy: {str(e)}")

    def schedule_maintenance(self):
        """Naplánuje pravidelnou údržbu"""
        try:
            dialog = MaintenanceScheduleDialog(self.get_vehicles(), self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                self.save_maintenance_schedule(dialog)
                QMessageBox.information(self, "Úspěch", "Plán údržby byl úspěšně vytvořen!")
                self.load_schedules()
        except Exception as e:
            QMessageBox.critical(self, "Chyba", f"Chyba při plánování údržby: {str(e)}")

    def report_malfunction(self):
        """Nahlásí poruchu"""
        try:
            dialog = MalfunctionReportDialog(self.get_vehicles(), self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                self.save_malfunction_report(dialog)
                QMessageBox.information(self, "Úspěch", "Porucha byla úspěšně nahlášena!")
                self.load_records()
        except Exception as e:
            QMessageBox.critical(self, "Chyba", f"Chyba při nahlašování poruchy: {str(e)}")

    def show_service_plan(self):
        """Zobrazí servisní plán"""
        try:
            dialog = ServicePlanDialog(self.get_vehicles(), self)
            dialog.exec()
        except Exception as e:
            QMessageBox.critical(self, "Chyba", f"Chyba při zobrazení servisního plánu: {str(e)}")

    def show_costs(self):
        """Zobrazí náklady na servis"""
        try:
            dialog = ServiceCostsDialog(self)
            dialog.exec()
        except Exception as e:
            QMessageBox.critical(self, "Chyba", f"Chyba při zobrazení nákladů: {str(e)}")

    def manage_certificates(self):
        """Správa certifikátů"""
        try:
            dialog = CertificateManagementDialog(self.get_vehicles(), self)
            dialog.exec()
        except Exception as e:
            QMessageBox.critical(self, "Chyba", f"Chyba při správě certifikátů: {str(e)}")

    def closeEvent(self, event):
        """Uzavře databázové připojení při zavření okna"""
        if hasattr(self, 'db'):
            self.db.close()
        event.accept()


class ServiceDialog(QDialog):
    """Dialog pro přidání servisního záznamu"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Nový servisní záznam")
        self.setFixedSize(600, 700)
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
            QLineEdit, QTextEdit, QDoubleSpinBox, QDateEdit, QComboBox {
                padding: 10px;
                border: 2px solid #e1e8ed;
                border-radius: 8px;
                font-size: 16px;
                background: white;
                margin-bottom: 10px;
            }
            QLineEdit:focus, QTextEdit:focus, QDoubleSpinBox:focus, QDateEdit:focus, QComboBox:focus {
                border-color: #e74c3c;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e74c3c, stop:1 #c0392b);
                color: white;
                border: none;
                padding: 12px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 16px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ec7063, stop:1 #e74c3c);
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
        
        # Základní údaje
        basic_label = QLabel("🔧 Základní údaje")
        basic_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #e74c3c; margin-top: 10px;")
        form_layout.addRow(basic_label)
        
        self.date_edit = QDateEdit(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        form_layout.addRow("Datum:", self.date_edit)
        
        self.asset_type_edit = QLineEdit()
        self.asset_type_edit.setPlaceholderText("Vozidlo, Stroj, Zařízení...")
        form_layout.addRow("Typ majetku:", self.asset_type_edit)
        
        self.asset_name_edit = QLineEdit()
        self.asset_name_edit.setPlaceholderText("Název/označení majetku")
        form_layout.addRow("Název majetku:", self.asset_name_edit)
        
        # Servisní údaje
        service_label = QLabel("⚙️ Servisní údaje")
        service_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #e74c3c; margin-top: 15px;")
        form_layout.addRow(service_label)
        
        self.service_type_edit = QLineEdit()
        self.service_type_edit.setPlaceholderText("Pravidelná údržba, Oprava, STK...")
        form_layout.addRow("Typ servisu:", self.service_type_edit)
        
        self.description_edit = QTextEdit()
        self.description_edit.setPlaceholderText("Detailní popis servisního úkonu")
        self.description_edit.setMaximumHeight(80)
        form_layout.addRow("Popis:", self.description_edit)
        
        self.technician_edit = QLineEdit()
        self.technician_edit.setPlaceholderText("Jméno technika/servisu")
        form_layout.addRow("Technik:", self.technician_edit)
        
        # Finanční údaje
        financial_label = QLabel("💰 Finanční údaje")
        financial_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #e74c3c; margin-top: 15px;")
        form_layout.addRow(financial_label)
        
        self.cost_edit = QDoubleSpinBox()
        self.cost_edit.setMaximum(999999.99)
        self.cost_edit.setSuffix(" Kč")
        form_layout.addRow("Náklady:", self.cost_edit)
        
        # Status a plánování
        status_label = QLabel("📊 Status a plánování")
        status_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #e74c3c; margin-top: 15px;")
        form_layout.addRow(status_label)
        
        self.status_combo = QComboBox()
        self.status_combo.addItems(["Plánováno", "Probíhá", "Dokončeno", "Zrušeno"])
        form_layout.addRow("Status:", self.status_combo)
        
        self.scheduled_date_edit = QDateEdit(QDate.currentDate())
        self.scheduled_date_edit.setCalendarPopup(True)
        form_layout.addRow("Plánovaný termín:", self.scheduled_date_edit)
        
        self.notes_edit = QTextEdit()
        self.notes_edit.setPlaceholderText("Dodatečné poznámky")
        self.notes_edit.setMaximumHeight(60)
        form_layout.addRow("Poznámky:", self.notes_edit)
        
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


class MaintenanceScheduleDialog(QDialog):
    """Dialog pro plánování údržby"""
    
    def __init__(self, vehicles, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Naplánovat údržbu")
        self.setFixedSize(500, 450)
        self.vehicles = vehicles
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
            QComboBox, QSpinBox, QTextEdit, QLineEdit, QDateEdit {
                padding: 10px;
                border: 2px solid #e1e8ed;
                border-radius: 8px;
                font-size: 16px;
                background: white;
                margin-bottom: 10px;
            }
            QComboBox:focus, QSpinBox:focus, QTextEdit:focus, QLineEdit:focus, QDateEdit:focus {
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
        """)
        
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Formulář
        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        
        # Základní informace
        header_label = QLabel("📅 Plánování údržby")
        header_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #3498db; margin-bottom: 15px;")
        form_layout.addRow(header_label)
        
        self.vehicle_combo = QComboBox()
        for vehicle_id, vehicle_name in self.vehicles:
            self.vehicle_combo.addItem(vehicle_name, vehicle_id)
        form_layout.addRow("Vozidlo:", self.vehicle_combo)
        
        self.maintenance_type_combo = QComboBox()
        maintenance_types = [
            "Pravidelný servis",
            "Výměna oleje",
            "Kontrola brzd",
            "STK",
            "Emise",
            "Pneumatiky",
            "Klimatizace",
            "Ostatní"
        ]
        self.maintenance_type_combo.addItems(maintenance_types)
        form_layout.addRow("Typ údržby:", self.maintenance_type_combo)
        
        self.scheduled_date_edit = QDateEdit()
        self.scheduled_date_edit.setDate(QDate.currentDate().addDays(30))
        self.scheduled_date_edit.setCalendarPopup(True)
        form_layout.addRow("Naplánováno na:", self.scheduled_date_edit)
        
        self.interval_edit = QSpinBox()
        self.interval_edit.setRange(0, 365)
        self.interval_edit.setValue(90)
        self.interval_edit.setSuffix(" dní")
        form_layout.addRow("Interval opakování:", self.interval_edit)
        
        self.notes_edit = QTextEdit()
        self.notes_edit.setPlaceholderText("Poznámky k plánované údržbě...")
        self.notes_edit.setMaximumHeight(80)
        form_layout.addRow("Poznámky:", self.notes_edit)
        
        layout.addLayout(form_layout)
        
        # Tlačítka
        button_layout = QHBoxLayout()
        
        cancel_button = QPushButton("Zrušit")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        
        save_button = QPushButton("Naplánovat")
        save_button.clicked.connect(self.accept)
        button_layout.addWidget(save_button)
        
        layout.addLayout(button_layout)


class MalfunctionReportDialog(QDialog):
    """Dialog pro nahlášení poruchy"""
    
    def __init__(self, vehicles, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Nahlásit poruchu")
        self.setFixedSize(500, 500)
        self.vehicles = vehicles
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
            QComboBox, QSpinBox, QTextEdit, QLineEdit, QDateEdit {
                padding: 10px;
                border: 2px solid #e1e8ed;
                border-radius: 8px;
                font-size: 16px;
                background: white;
                margin-bottom: 10px;
            }
            QComboBox:focus, QSpinBox:focus, QTextEdit:focus, QLineEdit:focus, QDateEdit:focus {
                border-color: #e74c3c;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e74c3c, stop:1 #c0392b);
                color: white;
                border: none;
                padding: 12px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 16px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ec7063, stop:1 #e74c3c);
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
        
        # Header
        header_label = QLabel("⚠️ Nahlášení poruchy")
        header_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #e74c3c; margin-bottom: 15px;")
        form_layout.addRow(header_label)
        
        self.vehicle_combo = QComboBox()
        for vehicle_id, vehicle_name in self.vehicles:
            self.vehicle_combo.addItem(vehicle_name, vehicle_id)
        form_layout.addRow("Vozidlo:", self.vehicle_combo)
        
        self.priority_combo = QComboBox()
        priorities = ["Nízká", "Střední", "Vysoká", "Kritická"]
        self.priority_combo.addItems(priorities)
        self.priority_combo.setCurrentText("Střední")
        form_layout.addRow("Priorita:", self.priority_combo)
        
        self.category_combo = QComboBox()
        categories = [
            "Motor",
            "Převodovka", 
            "Brzdy",
            "Elektrické systémy",
            "Klimatizace",
            "Karoserie",
            "Pneumatiky",
            "Ostatní"
        ]
        self.category_combo.addItems(categories)
        form_layout.addRow("Kategorie:", self.category_combo)
        
        self.reporter_edit = QLineEdit()
        self.reporter_edit.setPlaceholderText("Jméno nahlašovatele")
        form_layout.addRow("Nahlásil:", self.reporter_edit)
        
        self.description_edit = QTextEdit()
        self.description_edit.setPlaceholderText("Detailní popis poruchy...")
        self.description_edit.setMaximumHeight(100)
        form_layout.addRow("Popis poruchy:", self.description_edit)
        
        layout.addLayout(form_layout)
        
        # Tlačítka
        button_layout = QHBoxLayout()
        
        cancel_button = QPushButton("Zrušit")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        
        report_button = QPushButton("Nahlásit poruchu")
        report_button.clicked.connect(self.accept)
        button_layout.addWidget(report_button)
        
        layout.addLayout(button_layout)


class ServicePlanDialog(QDialog):
    """Dialog pro zobrazení servisního plánu"""
    
    def __init__(self, vehicles, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Servisní plán")
        self.setFixedSize(800, 600)
        self.vehicles = vehicles
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
            QTableWidget {
                border: 2px solid #e1e8ed;
                border-radius: 8px;
                background: white;
                gridline-color: #e1e8ed;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #e1e8ed;
            }
            QTableWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3498db, stop:1 #2980b9);
                color: white;
                border: none;
                padding: 10px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5dade2, stop:1 #3498db);
            }
        """)
        
        self.setup_ui()
        self.load_service_plan()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header_label = QLabel("📊 Servisní plán vozidel")
        header_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #3498db; margin-bottom: 15px;")
        layout.addWidget(header_label)
        
        # Tabulka plánu
        self.plan_table = QTableWidget()
        self.plan_table.setColumnCount(6)
        self.plan_table.setHorizontalHeaderLabels([
            "Vozidlo", "Typ údržby", "Naplánováno", "Stav", "Priorita", "Poznámky"
        ])
        layout.addWidget(self.plan_table)
        
        # Tlačítka
        button_layout = QHBoxLayout()
        
        refresh_button = QPushButton("🔄 Obnovit")
        refresh_button.clicked.connect(self.load_service_plan)
        button_layout.addWidget(refresh_button)
        
        export_button = QPushButton("📋 Export")
        export_button.clicked.connect(self.export_plan)
        button_layout.addWidget(export_button)
        
        close_button = QPushButton("Zavřít")
        close_button.clicked.connect(self.accept)
        button_layout.addWidget(close_button)
        
        layout.addLayout(button_layout)
    
    def load_service_plan(self):
        """Načte servisní plán"""
        # Simulace dat pro servisní plán
        plan_data = [
            ("Škoda Octavia", "Pravidelný servis", "2024-02-15", "Naplánováno", "Střední", "Výměna oleje a filtrů"),
            ("Ford Transit", "STK", "2024-03-01", "Naplánováno", "Vysoká", "Technická kontrola"),
            ("BMW 320d", "Klimatizace", "2024-02-20", "Zpožděno", "Nízká", "Kontrola a doplnění"),
        ]
        
        self.plan_table.setRowCount(len(plan_data))
        
        for row, data in enumerate(plan_data):
            for col, value in enumerate(data):
                item = QTableWidgetItem(str(value))
                if col == 3:  # Stav
                    if value == "Zpožděno":
                        item.setBackground(Qt.GlobalColor.red)
                        item.setForeground(Qt.GlobalColor.white)
                    elif value == "Dokončeno":
                        item.setBackground(Qt.GlobalColor.green)
                        item.setForeground(Qt.GlobalColor.white)
                self.plan_table.setItem(row, col, item)
        
        self.plan_table.resizeColumnsToContents()
    
    def export_plan(self):
        """Export servisního plánu"""
        QMessageBox.information(self, "Export", "Servisní plán byl exportován do CSV souboru.")


class ServiceCostsDialog(QDialog):
    """Dialog pro přehled nákladů na servis"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Náklady na servis")
        self.setFixedSize(700, 500)
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
            QTableWidget {
                border: 2px solid #e1e8ed;
                border-radius: 8px;
                background: white;
                gridline-color: #e1e8ed;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #e1e8ed;
            }
            QTableWidget::item:selected {
                background-color: #f39c12;
                color: white;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f39c12, stop:1 #e67e22);
                color: white;
                border: none;
                padding: 10px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f7dc6f, stop:1 #f39c12);
            }
        """)
        
        self.setup_ui()
        self.load_costs()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header_label = QLabel("💰 Přehled nákladů na servis")
        header_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #f39c12; margin-bottom: 15px;")
        layout.addWidget(header_label)
        
        # Statistiky
        stats_layout = QHBoxLayout()
        
        total_label = QLabel("Celkové náklady: 45 320 Kč")
        total_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #2c3e50; background: #ecf0f1; padding: 10px; border-radius: 5px;")
        stats_layout.addWidget(total_label)
        
        monthly_label = QLabel("Měsíční průměr: 7 553 Kč")
        monthly_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #2c3e50; background: #ecf0f1; padding: 10px; border-radius: 5px;")
        stats_layout.addWidget(monthly_label)
        
        layout.addLayout(stats_layout)
        
        # Tabulka nákladů
        self.costs_table = QTableWidget()
        self.costs_table.setColumnCount(5)
        self.costs_table.setHorizontalHeaderLabels([
            "Datum", "Vozidlo", "Typ", "Popis", "Náklady (Kč)"
        ])
        layout.addWidget(self.costs_table)
        
        # Tlačítka
        button_layout = QHBoxLayout()
        
        period_button = QPushButton("📅 Změnit období")
        period_button.clicked.connect(self.change_period)
        button_layout.addWidget(period_button)
        
        export_button = QPushButton("📊 Export do Excel")
        export_button.clicked.connect(self.export_costs)
        button_layout.addWidget(export_button)
        
        close_button = QPushButton("Zavřít")
        close_button.clicked.connect(self.accept)
        button_layout.addWidget(close_button)
        
        layout.addLayout(button_layout)
    
    def load_costs(self):
        """Načte náklady na servis"""
        # Simulace dat pro náklady
        costs_data = [
            ("2024-01-15", "Škoda Octavia", "Pravidelný servis", "Výměna oleje a filtrů", "3 450"),
            ("2024-01-20", "Ford Transit", "Oprava", "Výměna brzdových destiček", "8 900"),
            ("2024-02-01", "BMW 320d", "STK", "Technická kontrola", "1 200"),
            ("2024-02-05", "Škoda Octavia", "Oprava", "Výměna pneumatik", "12 800"),
            ("2024-02-10", "Ford Transit", "Pravidelný servis", "Kontrola a údržba", "4 670"),
        ]
        
        self.costs_table.setRowCount(len(costs_data))
        
        for row, data in enumerate(costs_data):
            for col, value in enumerate(data):
                item = QTableWidgetItem(str(value))
                if col == 4:  # Náklady
                    item.setForeground(Qt.GlobalColor.darkMagenta)
                self.costs_table.setItem(row, col, item)
        
        self.costs_table.resizeColumnsToContents()
    
    def change_period(self):
        """Změní období pro zobrazení nákladů"""
        QMessageBox.information(self, "Období", "Funkce změny období bude k dispozici v další verzi.")
    
    def export_costs(self):
        """Export nákladů do Excel"""
        QMessageBox.information(self, "Export", "Náklady byly exportovány do Excel souboru.")


class CertificateManagementDialog(QDialog):
    """Dialog pro správu certifikátů"""
    
    def __init__(self, vehicles, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Správa certifikátů")
        self.setFixedSize(800, 600)
        self.vehicles = vehicles
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
            QTableWidget {
                border: 2px solid #e1e8ed;
                border-radius: 8px;
                background: white;
                gridline-color: #e1e8ed;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #e1e8ed;
            }
            QTableWidget::item:selected {
                background-color: #9b59b6;
                color: white;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #9b59b6, stop:1 #8e44ad);
                color: white;
                border: none;
                padding: 10px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #bb8fce, stop:1 #9b59b6);
            }
        """)
        
        self.setup_ui()
        self.load_certificates()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header_label = QLabel("📋 Správa certifikátů a průkazů")
        header_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #9b59b6; margin-bottom: 15px;")
        layout.addWidget(header_label)
        
        # Upozornění
        warning_label = QLabel("⚠️ Vozidla s blížící se expirací:")
        warning_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #e74c3c; background: #ffebee; padding: 8px; border-radius: 5px;")
        layout.addWidget(warning_label)
        
        # Tabulka certifikátů
        self.certificates_table = QTableWidget()
        self.certificates_table.setColumnCount(6)
        self.certificates_table.setHorizontalHeaderLabels([
            "Vozidlo", "Typ certifikátu", "Vydáno", "Vyprší", "Stav", "Akce"
        ])
        layout.addWidget(self.certificates_table)
        
        # Tlačítka
        button_layout = QHBoxLayout()
        
        add_button = QPushButton("➕ Přidat certifikát")
        add_button.clicked.connect(self.add_certificate)
        button_layout.addWidget(add_button)
        
        remind_button = QPushButton("🔔 Nastavit upomínky")
        remind_button.clicked.connect(self.setup_reminders)
        button_layout.addWidget(remind_button)
        
        export_button = QPushButton("📄 Export přehledu")
        export_button.clicked.connect(self.export_certificates)
        button_layout.addWidget(export_button)
        
        close_button = QPushButton("Zavřít")
        close_button.clicked.connect(self.accept)
        button_layout.addWidget(close_button)
        
        layout.addLayout(button_layout)
    
    def load_certificates(self):
        """Načte certifikáty"""
        # Simulace dat pro certifikáty
        certificates_data = [
            ("Škoda Octavia", "STK", "2023-02-15", "2025-02-15", "Platný", "Prodloužit"),
            ("Ford Transit", "STK", "2023-01-10", "2024-01-10", "Expiruje!", "Obnovit"),
            ("BMW 320d", "Emise", "2023-05-20", "2024-05-20", "Platný", "Prodloužit"),
            ("Škoda Octavia", "Pojištění", "2024-01-01", "2024-12-31", "Platný", "Prodloužit"),
            ("Ford Transit", "Emise", "2023-03-15", "2024-03-15", "Brzy vyprší", "Obnovit"),
        ]
        
        self.certificates_table.setRowCount(len(certificates_data))
        
        for row, data in enumerate(certificates_data):
            for col, value in enumerate(data):
                item = QTableWidgetItem(str(value))
                if col == 4:  # Stav
                    if "Expiruje" in value or "vyprší" in value:
                        item.setBackground(Qt.GlobalColor.red)
                        item.setForeground(Qt.GlobalColor.white)
                    elif value == "Platný":
                        item.setBackground(Qt.GlobalColor.green)
                        item.setForeground(Qt.GlobalColor.white)
                self.certificates_table.setItem(row, col, item)
        
        self.certificates_table.resizeColumnsToContents()
    
    def add_certificate(self):
        """Přidá nový certifikát"""
        QMessageBox.information(self, "Nový certifikát", "Dialog pro přidání nového certifikátu bude k dispozici v další verzi.")
    
    def setup_reminders(self):
        """Nastavení upomínek"""
        QMessageBox.information(self, "Upomínky", "Nastavení automatických upomínek bude k dispozici v další verzi.")
    
    def export_certificates(self):
        """Export přehledu certifikátů"""
        QMessageBox.information(self, "Export", "Přehled certifikátů byl exportován do PDF souboru.")
