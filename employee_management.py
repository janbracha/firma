from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFrame, QScrollArea, 
    QGridLayout, QLabel, QPushButton, QComboBox, QDateEdit, QTableWidget, 
    QTableWidgetItem, QMessageBox, QDialog, QFormLayout, QLineEdit, QTextEdit,
    QSpinBox, QDoubleSpinBox, QCheckBox
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont
from database import connect
from employee_dialogs import PositionChangeDialog, ContractManagementDialog, TrainingManagementDialog

class EmployeeManagementWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Správa zaměstnanců - Projekt & Develop s.r.o.")
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
        self.create_employee_tables()
        self.load_employees()

    def create_header(self, layout):
        """Vytvoří moderní hlavičku"""
        header_frame = QFrame()
        header_frame.setObjectName("headerFrame")
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(20, 20, 20, 20)
        
        # Levá část - informace o sekci
        left_layout = QVBoxLayout()
        
        title_label = QLabel("👥 Správa zaměstnanců")
        title_label.setObjectName("titleLabel")
        left_layout.addWidget(title_label)
        
        subtitle_label = QLabel("Evidence zaměstnanců, pozic a pracovních vztahů")
        subtitle_label.setObjectName("subtitleLabel")
        left_layout.addWidget(subtitle_label)
        
        header_layout.addLayout(left_layout)
        header_layout.addStretch()
        
        layout.addWidget(header_frame)
    
    def create_content(self, layout):
        """Vytvoří hlavní obsah okna"""
        
        # Akce s kartami
        actions_frame = self.create_section_frame("⚡ Rychlé akce", "Správa zaměstnanců a pracovních vztahů")
        actions_grid = QGridLayout()
        actions_grid.setSpacing(15)
        
        # Karty akcí
        actions = [
            ("➕ Nový zaměstnanec", "Přidat zaměstnance", self.add_employee),
            ("📝 Úprava pozice", "Změnit pozici zaměstnance", self.change_position),
            ("💰 Mzdy a odměny", "Správa mezd", self.manage_salaries),
            ("📊 Docházka", "Evidence docházky", self.manage_attendance),
            ("📋 Smlouvy", "Správa smluv", self.manage_contracts),
            ("🎓 Školení", "Evidence školení", self.manage_training),
        ]
        
        for i, (title, desc, func) in enumerate(actions):
            card = self.create_action_card(title, desc, func)
            actions_grid.addWidget(card, i // 3, i % 3)
        
        actions_frame.layout().addLayout(actions_grid)
        layout.addWidget(actions_frame)
        
        # Přehled zaměstnanců
        stats_frame = self.create_section_frame("📊 Přehled", "Statistiky zaměstnanců")
        stats_grid = QGridLayout()
        stats_grid.setSpacing(15)
        
        # Karty statistik
        self.total_card = self.create_stat_card("👥 Celkem zaměstnanců", "0", "blue")
        self.active_card = self.create_stat_card("✅ Aktivní", "0", "green")
        self.departments_card = self.create_stat_card("🏢 Oddělení", "0", "purple")
        self.salary_card = self.create_stat_card("💰 Celkové mzdy", "0 Kč", "orange")
        
        stats_grid.addWidget(self.total_card, 0, 0)
        stats_grid.addWidget(self.active_card, 0, 1)
        stats_grid.addWidget(self.departments_card, 0, 2)
        stats_grid.addWidget(self.salary_card, 0, 3)
        
        stats_frame.layout().addLayout(stats_grid)
        layout.addWidget(stats_frame)
        
        # Tabulka zaměstnanců
        table_frame = self.create_section_frame("👥 Seznam zaměstnanců", "Přehled všech zaměstnanců")
        
        # Tabulka
        self.table = QTableWidget(0, 10)
        self.table.setObjectName("dataTable")
        self.table.setHorizontalHeaderLabels([
            "ID", "Jméno", "Příjmení", "Pozice", "Oddělení", 
            "Nastup", "Mzda", "Telefon", "Email", "Status"
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
                    stop:0 rgba(155, 89, 182, 1.0),
                    stop:1 rgba(142, 68, 173, 1.0));
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
                border: 2px solid rgba(155, 89, 182, 0.1);
                border-radius: 12px;
                margin: 5px;
            }
            
            #actionCard:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(255, 255, 255, 1.0),
                    stop:1 rgba(248, 245, 255, 1.0));
                border: 2px solid rgba(155, 89, 182, 0.3);
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
            
            #statCard_green {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(46, 204, 113, 0.9),
                    stop:1 rgba(39, 174, 96, 0.9));
                border-radius: 12px;
                border: 2px solid rgba(39, 174, 96, 0.3);
            }
            
            #statCard_purple {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(155, 89, 182, 0.9),
                    stop:1 rgba(142, 68, 173, 0.9));
                border-radius: 12px;
                border: 2px solid rgba(142, 68, 173, 0.3);
            }
            
            #statCard_orange {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(230, 126, 34, 0.9),
                    stop:1 rgba(211, 84, 0, 0.9));
                border-radius: 12px;
                border: 2px solid rgba(211, 84, 0, 0.3);
            }
            
            #statTitle {
                font-size: 12px;
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
                border: 1px solid rgba(155, 89, 182, 0.2);
                border-radius: 8px;
                gridline-color: rgba(155, 89, 182, 0.1);
                font-size: 12px;
                selection-background-color: rgba(155, 89, 182, 0.2);
            }
            
            QHeaderView::section {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(155, 89, 182, 0.8),
                    stop:1 rgba(155, 89, 182, 0.6));
                color: white;
                font-weight: bold;
                font-size: 11px;
                padding: 8px;
                border: none;
                border-right: 1px solid rgba(255, 255, 255, 0.3);
            }
        """)

    def create_employee_tables(self):
        """Vytvoří tabulky pro správu zaměstnanců"""
        try:
            cursor = self.db.cursor()
            
            # Tabulka zaměstnanců
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS employees (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    position TEXT,
                    department TEXT,
                    hire_date TEXT,
                    birth_date TEXT,
                    phone TEXT,
                    email TEXT,
                    address TEXT,
                    salary REAL,
                    active INTEGER DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Tabulka mezd
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS employee_salaries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    employee_id INTEGER,
                    month TEXT,
                    base_salary REAL,
                    overtime REAL,
                    bonus REAL,
                    deductions REAL,
                    net_salary REAL,
                    paid_date TEXT,
                    FOREIGN KEY (employee_id) REFERENCES employees (id)
                )
            """)
            
            # Tabulka docházky
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS employee_attendance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    employee_id INTEGER,
                    date TEXT,
                    start_time TEXT,
                    end_time TEXT,
                    break_time INTEGER DEFAULT 0,
                    overtime INTEGER DEFAULT 0,
                    absence_type TEXT,
                    notes TEXT,
                    FOREIGN KEY (employee_id) REFERENCES employees (id)
                )
            """)
            
            self.db.commit()
        except Exception as e:
            QMessageBox.critical(self, "Chyba", f"Chyba při vytváření tabulek: {str(e)}")

    def load_employees(self):
        """Načte seznam zaměstnanců"""
        try:
            cursor = self.db.cursor()
            cursor.execute("""
                SELECT id, first_name, last_name, position, department, 
                       hire_date, salary, phone, email, active
                FROM employees 
                ORDER BY last_name, first_name
            """)
            rows = cursor.fetchall()

            self.table.setRowCount(len(rows))
            
            total_employees = len(rows)
            active_count = 0
            departments = set()
            total_salary = 0
            
            for row_idx, row in enumerate(rows):
                # Formátování dat pro zobrazení
                formatted_row = list(row)
                
                # Status
                status = "Aktivní" if row[9] else "Neaktivní"
                formatted_row[9] = status
                
                # Mzda
                if row[6]:
                    formatted_row[6] = f"{float(row[6]):,.0f} Kč"
                    total_salary += float(row[6])
                else:
                    formatted_row[6] = "Nenastaveno"
                
                # Telefon a email - zkrácení pro lepší zobrazení
                if row[7] and len(row[7]) > 15:
                    formatted_row[7] = row[7][:12] + "..."
                if row[8] and len(row[8]) > 20:
                    formatted_row[8] = row[8][:17] + "..."
                
                for col_idx, value in enumerate(formatted_row):
                    self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value) if value else ""))
                
                # Statistiky
                if row[9]:  # active
                    active_count += 1
                if row[4]:  # department
                    departments.add(row[4])
                    
            # Aktualizace karet
            self.update_stat_card(self.total_card, str(total_employees))
            self.update_stat_card(self.active_card, str(active_count))
            self.update_stat_card(self.departments_card, str(len(departments)))
            self.update_stat_card(self.salary_card, f"{total_salary:,.0f} Kč")
            
        except Exception as e:
            QMessageBox.critical(self, "Chyba", f"Chyba při načítání zaměstnanců: {str(e)}")
    
    def update_stat_card(self, card, value):
        """Aktualizuje hodnotu ve statistické kartě"""
        layout = card.layout()
        if layout and layout.count() > 1:
            value_label = layout.itemAt(1).widget()
            if value_label:
                value_label.setText(value)

    def add_employee(self):
        """Přidá nového zaměstnance"""
        dialog = EmployeeDialog()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            try:
                cursor = self.db.cursor()
                cursor.execute("""
                    INSERT INTO employees (first_name, last_name, position, department, 
                                         hire_date, birth_date, phone, email, address, salary, active) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    dialog.first_name_edit.text(),
                    dialog.last_name_edit.text(),
                    dialog.position_edit.text(),
                    dialog.department_edit.text(),
                    dialog.hire_date_edit.date().toString("yyyy-MM-dd"),
                    dialog.birth_date_edit.date().toString("yyyy-MM-dd"),
                    dialog.phone_edit.text(),
                    dialog.email_edit.text(),
                    dialog.address_edit.toPlainText(),
                    dialog.salary_edit.value() if dialog.salary_edit.value() > 0 else None,
                    1 if dialog.active_check.isChecked() else 0
                ))
                self.db.commit()
                self.load_employees()
                QMessageBox.information(self, "Úspěch", "Zaměstnanec byl úspěšně přidán!")
            except Exception as e:
                QMessageBox.critical(self, "Chyba", f"Chyba při přidávání zaměstnance: {str(e)}")

    def change_position(self):
        """Změní pozici zaměstnance"""
        try:
            dialog = PositionChangeDialog(self.get_employees(), self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                self.save_position_change(dialog)
                QMessageBox.information(self, "Úspěch", "Pozice zaměstnance byla úspěšně změněna!")
                self.load_employees()
        except Exception as e:
            QMessageBox.critical(self, "Chyba", f"Chyba při změně pozice: {str(e)}")

    def manage_salaries(self):
        """Správa mezd"""
        dialog = SalaryManagementDialog(self.get_employees())
        if dialog.exec() == QDialog.DialogCode.Accepted:
            try:
                cursor = self.db.cursor()
                cursor.execute("""
                    INSERT INTO employee_salaries (employee_id, month, base_salary, 
                                                 overtime, bonus, deductions, net_salary, paid_date) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    dialog.employee_combo.currentData(),
                    dialog.month_edit.text(),
                    dialog.base_salary_edit.value(),
                    dialog.overtime_edit.value(),
                    dialog.bonus_edit.value(),
                    dialog.deductions_edit.value(),
                    dialog.calculate_net_salary(),
                    dialog.paid_date_edit.date().toString("yyyy-MM-dd") if dialog.paid_check.isChecked() else None
                ))
                self.db.commit()
                QMessageBox.information(self, "Úspěch", "Mzda byla úspěšně zaznamenána!")
            except Exception as e:
                QMessageBox.critical(self, "Chyba", f"Chyba při zaznamenání mzdy: {str(e)}")

    def get_employees(self):
        """Vrátí seznam aktivních zaměstnanců"""
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT id, first_name || ' ' || last_name FROM employees WHERE active = 1")
            return cursor.fetchall()
        except:
            return []

    def manage_attendance(self):
        """Evidence docházky"""
        dialog = AttendanceDialog(self.get_employees())
        if dialog.exec() == QDialog.DialogCode.Accepted:
            try:
                cursor = self.db.cursor()
                cursor.execute("""
                    INSERT INTO employee_attendance (employee_id, date, start_time, 
                                                   end_time, break_time, overtime, absence_type, notes) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    dialog.employee_combo.currentData(),
                    dialog.date_edit.date().toString("yyyy-MM-dd"),
                    dialog.start_time_edit.text() if dialog.start_time_edit.text() else None,
                    dialog.end_time_edit.text() if dialog.end_time_edit.text() else None,
                    dialog.break_edit.value(),
                    dialog.overtime_edit.value(),
                    dialog.absence_combo.currentText() if dialog.absence_combo.currentText() != "Žádná" else None,
                    dialog.notes_edit.toPlainText()
                ))
                self.db.commit()
                QMessageBox.information(self, "Úspěch", "Docházka byla úspěšně zaznamenána!")
            except Exception as e:
                QMessageBox.critical(self, "Chyba", f"Chyba při zaznamenání docházky: {str(e)}")

    def save_position_change(self, dialog):
        """Uloží změnu pozice"""
        try:
            cursor = self.db.cursor()
            employee_id = dialog.employee_combo.currentData()
            new_position = dialog.position_edit.text()
            new_department = dialog.department_combo.currentText()
            new_salary = dialog.salary_edit.value()
            notes = dialog.notes_edit.toPlainText()
            
            # Aktualizace zaměstnance
            cursor.execute("""
                UPDATE employees 
                SET position = ?, department = ?
                WHERE id = ?
            """, (new_position, new_department, employee_id))
            
            # Záznam do historie mezd
            cursor.execute("""
                INSERT INTO employee_salaries (employee_id, month, base_salary, notes)
                VALUES (?, ?, ?, ?)
            """, (
                employee_id,
                QDate.currentDate().toString("yyyy-MM"),
                new_salary,
                f"Změna pozice: {notes}"
            ))
            
            self.db.commit()
        except Exception as e:
            QMessageBox.critical(self, "Chyba", f"Chyba při ukládání změny pozice: {str(e)}")

    def manage_contracts(self):
        """Správa smluv"""
        try:
            dialog = ContractManagementDialog(self.get_employees(), self)
            dialog.exec()
        except Exception as e:
            QMessageBox.critical(self, "Chyba", f"Chyba při správě smluv: {str(e)}")

    def manage_training(self):
        """Evidence školení"""
        try:
            dialog = TrainingManagementDialog(self.get_employees(), self)
            dialog.exec()
        except Exception as e:
            QMessageBox.critical(self, "Chyba", f"Chyba při evidenci školení: {str(e)}")

    def closeEvent(self, event):
        """Uzavře databázové připojení při zavření okna"""
        if hasattr(self, 'db'):
            self.db.close()
        event.accept()


class EmployeeDialog(QDialog):
    """Dialog pro přidání/úpravu zaměstnance"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Nový zaměstnanec")
        self.setFixedSize(700, 750)  # Zvětšeno pro lepší zobrazení
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f6fa;
            }
            QLabel {
                font-size: 15px;
                font-weight: bold;
                color: #2c3e50;
                margin-bottom: 5px;
                font-family: 'Inter', 'Roboto', sans-serif;
            }
            QLineEdit, QTextEdit, QDoubleSpinBox, QDateEdit {
                padding: 12px 15px;
                border: 2px solid rgba(108, 133, 163, 0.2);
                border-radius: 8px;
                font-size: 15px;
                font-family: 'Inter', 'Roboto', sans-serif;
                background: white;
                margin-bottom: 10px;
                min-height: 20px;
                min-width: 250px;
                color: #2c3e50;
            }
            QLineEdit:focus, QTextEdit:focus, QDoubleSpinBox:focus, QDateEdit:focus {
                border: 2px solid #9b59b6;
                outline: none;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #9b59b6, stop:1 #8e44ad);
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 15px;
                font-family: 'Inter', 'Roboto', sans-serif;
                min-height: 20px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #bb76c6, stop:1 #9b59b6);
            }
            QCheckBox {
                font-size: 15px;
                color: #2c3e50;
                spacing: 8px;
                font-family: 'Inter', 'Roboto', sans-serif;
            }
        """)
        
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Formulář
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        
        # Osobní údaje
        personal_label = QLabel("📝 Osobní údaje")
        personal_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #9b59b6; margin-top: 10px;")
        form_layout.addRow(personal_label)
        
        self.first_name_edit = QLineEdit()
        self.first_name_edit.setPlaceholderText("Křestní jméno")
        self.first_name_edit.setMinimumHeight(35)
        self.first_name_edit.setMinimumWidth(250)
        form_layout.addRow("Jméno:", self.first_name_edit)
        
        self.last_name_edit = QLineEdit()
        self.last_name_edit.setPlaceholderText("Příjmení")
        self.last_name_edit.setMinimumHeight(35)
        self.last_name_edit.setMinimumWidth(250)
        form_layout.addRow("Příjmení:", self.last_name_edit)
        
        self.birth_date_edit = QDateEdit(QDate.currentDate().addYears(-25))
        self.birth_date_edit.setCalendarPopup(True)
        self.birth_date_edit.setMinimumHeight(35)
        self.birth_date_edit.setMinimumWidth(250)
        form_layout.addRow("Datum narození:", self.birth_date_edit)
        
        # Kontaktní údaje
        contact_label = QLabel("📞 Kontaktní údaje")
        contact_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #9b59b6; margin-top: 15px;")
        form_layout.addRow(contact_label)
        
        self.phone_edit = QLineEdit()
        self.phone_edit.setPlaceholderText("+420 123 456 789")
        self.phone_edit.setMinimumHeight(35)
        self.phone_edit.setMinimumWidth(250)
        form_layout.addRow("Telefon:", self.phone_edit)
        
        self.email_edit = QLineEdit()
        self.email_edit.setPlaceholderText("jmeno@email.cz")
        self.email_edit.setMinimumHeight(35)
        self.email_edit.setMinimumWidth(250)
        form_layout.addRow("Email:", self.email_edit)
        
        self.address_edit = QTextEdit()
        self.address_edit.setPlaceholderText("Adresa bydliště")
        self.address_edit.setMaximumHeight(80)
        self.address_edit.setMinimumHeight(60)
        self.address_edit.setMinimumWidth(250)
        form_layout.addRow("Adresa:", self.address_edit)
        
        # Pracovní údaje
        work_label = QLabel("💼 Pracovní údaje")
        work_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #9b59b6; margin-top: 15px;")
        form_layout.addRow(work_label)
        
        self.position_edit = QLineEdit()
        self.position_edit.setPlaceholderText("Název pozice")
        self.position_edit.setMinimumHeight(35)
        self.position_edit.setMinimumWidth(250)
        form_layout.addRow("Pozice:", self.position_edit)
        
        self.department_edit = QLineEdit()
        self.department_edit.setPlaceholderText("Název oddělení")
        self.department_edit.setMinimumHeight(35)
        self.department_edit.setMinimumWidth(250)
        form_layout.addRow("Oddělení:", self.department_edit)
        
        self.hire_date_edit = QDateEdit(QDate.currentDate())
        self.hire_date_edit.setCalendarPopup(True)
        self.hire_date_edit.setMinimumHeight(35)
        self.hire_date_edit.setMinimumWidth(250)
        form_layout.addRow("Datum nástupu:", self.hire_date_edit)
        
        self.salary_edit = QDoubleSpinBox()
        self.salary_edit.setMaximum(999999.99)
        self.salary_edit.setSuffix(" Kč")
        self.salary_edit.setMinimumHeight(35)
        self.salary_edit.setMinimumWidth(250)
        form_layout.addRow("Mzda:", self.salary_edit)
        
        self.active_check = QCheckBox("Aktivní zaměstnanec")
        self.active_check.setChecked(True)
        form_layout.addRow(self.active_check)
        
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


class SalaryManagementDialog(QDialog):
    """Dialog pro správu mezd"""
    
    def __init__(self, employees, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Správa mezd")
        self.setFixedSize(600, 700)  # Zvětšeno pro lepší zobrazení
        self.employees = employees
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f6fa;
            }
            QLabel {
                font-size: 15px;
                font-weight: bold;
                color: #2c3e50;
                margin-bottom: 5px;
                font-family: 'Inter', 'Roboto', sans-serif;
            }
            QComboBox, QLineEdit, QDoubleSpinBox, QDateEdit, QCheckBox {
                padding: 12px 15px;
                border: 2px solid rgba(108, 133, 163, 0.2);
                border-radius: 8px;
                font-size: 15px;
                font-family: 'Inter', 'Roboto', sans-serif;
                background: white;
                margin-bottom: 10px;
                min-height: 20px;
                min-width: 250px;
                color: #2c3e50;
            }
            QComboBox:focus, QLineEdit:focus, QDoubleSpinBox:focus, QDateEdit:focus {
                border: 2px solid #9b59b6;
                outline: none;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #9b59b6, stop:1 #8e44ad);
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 15px;
                font-family: 'Inter', 'Roboto', sans-serif;
                min-height: 20px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #bb76c6, stop:1 #9b59b6);
            }
            QCheckBox {
                font-size: 15px;
                color: #2c3e50;
                spacing: 8px;
                font-family: 'Inter', 'Roboto', sans-serif;
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
        basic_label = QLabel("👤 Základní údaje")
        basic_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #9b59b6; margin-top: 10px;")
        form_layout.addRow(basic_label)
        
        self.employee_combo = QComboBox()
        for emp_id, emp_name in self.employees:
            self.employee_combo.addItem(emp_name, emp_id)
        form_layout.addRow("Zaměstnanec:", self.employee_combo)
        
        self.month_edit = QLineEdit()
        self.month_edit.setPlaceholderText("YYYY-MM (např. 2024-01)")
        form_layout.addRow("Měsíc:", self.month_edit)
        
        # Mzdové složky
        salary_label = QLabel("💰 Mzdové složky")
        salary_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #9b59b6; margin-top: 15px;")
        form_layout.addRow(salary_label)
        
        self.base_salary_edit = QDoubleSpinBox()
        self.base_salary_edit.setMaximum(999999.99)
        self.base_salary_edit.setSuffix(" Kč")
        form_layout.addRow("Základní mzda:", self.base_salary_edit)
        
        self.overtime_edit = QDoubleSpinBox()
        self.overtime_edit.setMaximum(999999.99)
        self.overtime_edit.setSuffix(" Kč")
        form_layout.addRow("Přesčasy:", self.overtime_edit)
        
        self.bonus_edit = QDoubleSpinBox()
        self.bonus_edit.setMaximum(999999.99)
        self.bonus_edit.setSuffix(" Kč")
        form_layout.addRow("Bonusy:", self.bonus_edit)
        
        # Srážky
        deductions_label = QLabel("📉 Srážky")
        deductions_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #9b59b6; margin-top: 15px;")
        form_layout.addRow(deductions_label)
        
        self.deductions_edit = QDoubleSpinBox()
        self.deductions_edit.setMaximum(999999.99)
        self.deductions_edit.setSuffix(" Kč")
        form_layout.addRow("Celkové srážky:", self.deductions_edit)
        
        # Výplatní údaje
        payment_label = QLabel("💳 Výplata")
        payment_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #9b59b6; margin-top: 15px;")
        form_layout.addRow(payment_label)
        
        self.paid_check = QCheckBox("Již vyplaceno")
        form_layout.addRow(self.paid_check)
        
        self.paid_date_edit = QDateEdit(QDate.currentDate())
        self.paid_date_edit.setCalendarPopup(True)
        self.paid_date_edit.setEnabled(False)
        form_layout.addRow("Datum výplaty:", self.paid_date_edit)
        
        # Propojení checkbox s datem
        self.paid_check.toggled.connect(self.paid_date_edit.setEnabled)
        
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
    
    def calculate_net_salary(self):
        """Vypočítá čistou mzdu"""
        gross = self.base_salary_edit.value() + self.overtime_edit.value() + self.bonus_edit.value()
        net = gross - self.deductions_edit.value()
        return max(0, net)


class AttendanceDialog(QDialog):
    """Dialog pro evidenci docházky"""
    
    def __init__(self, employees, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Evidence docházky")
        self.setFixedSize(600, 700)  # Zvětšeno pro lepší zobrazení
        self.employees = employees
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f6fa;
            }
            QLabel {
                font-size: 15px;
                font-weight: bold;
                color: #2c3e50;
                margin-bottom: 5px;
                font-family: 'Inter', 'Roboto', sans-serif;
            }
            QComboBox, QLineEdit, QSpinBox, QDateEdit, QTextEdit {
                padding: 12px 15px;
                border: 2px solid rgba(108, 133, 163, 0.2);
                border-radius: 8px;
                font-size: 15px;
                font-family: 'Inter', 'Roboto', sans-serif;
                background: white;
                margin-bottom: 10px;
                min-height: 20px;
                min-width: 250px;
                color: #2c3e50;
            }
            QComboBox:focus, QLineEdit:focus, QSpinBox:focus, QDateEdit:focus, QTextEdit:focus {
                border: 2px solid #9b59b6;
                outline: none;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #9b59b6, stop:1 #8e44ad);
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 15px;
                font-family: 'Inter', 'Roboto', sans-serif;
                min-height: 20px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #bb76c6, stop:1 #9b59b6);
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
        basic_label = QLabel("👤 Základní údaje")
        basic_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #9b59b6; margin-top: 10px;")
        form_layout.addRow(basic_label)
        
        self.employee_combo = QComboBox()
        for emp_id, emp_name in self.employees:
            self.employee_combo.addItem(emp_name, emp_id)
        form_layout.addRow("Zaměstnanec:", self.employee_combo)
        
        self.date_edit = QDateEdit(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        form_layout.addRow("Datum:", self.date_edit)
        
        # Časy
        time_label = QLabel("⏰ Pracovní doba")
        time_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #9b59b6; margin-top: 15px;")
        form_layout.addRow(time_label)
        
        self.start_time_edit = QLineEdit()
        self.start_time_edit.setPlaceholderText("08:00")
        form_layout.addRow("Příchod:", self.start_time_edit)
        
        self.end_time_edit = QLineEdit()
        self.end_time_edit.setPlaceholderText("16:00")
        form_layout.addRow("Odchod:", self.end_time_edit)
        
        self.break_edit = QSpinBox()
        self.break_edit.setMaximum(480)  # 8 hodin v minutách
        self.break_edit.setSuffix(" min")
        self.break_edit.setValue(30)
        form_layout.addRow("Přestávka:", self.break_edit)
        
        self.overtime_edit = QSpinBox()
        self.overtime_edit.setMaximum(720)  # 12 hodin v minutách
        self.overtime_edit.setSuffix(" min")
        form_layout.addRow("Přesčas:", self.overtime_edit)
        
        # Absence
        absence_label = QLabel("🏥 Absence")
        absence_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #9b59b6; margin-top: 15px;")
        form_layout.addRow(absence_label)
        
        self.absence_combo = QComboBox()
        self.absence_combo.addItems([
            "Žádná", "Dovolená", "Nemoc", "Náhradní volno", 
            "Lékař", "Úřad", "Osobní překážky", "Jiné"
        ])
        form_layout.addRow("Typ absence:", self.absence_combo)
        
        self.notes_edit = QTextEdit()
        self.notes_edit.setPlaceholderText("Poznámky k docházce")
        self.notes_edit.setMaximumHeight(80)
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
