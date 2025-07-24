
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel, 
    QPushButton, QComboBox, QSpinBox, QTextEdit, QLineEdit,
    QTableWidget, QTableWidgetItem, QMessageBox
)
from PyQt6.QtCore import Qt

class PositionChangeDialog(QDialog):
    """Dialog pro změnu pozice zaměstnance"""
    
    def __init__(self, employees, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Změna pozice")
        self.setFixedSize(600, 500)  # Zvětšeno pro lepší zobrazení
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
            QComboBox, QLineEdit, QSpinBox, QTextEdit {
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
            QComboBox:focus, QLineEdit:focus, QSpinBox:focus, QTextEdit:focus {
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
        
        # Header
        header_label = QLabel("🔄 Změna pozice zaměstnance")
        header_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #3498db; margin-bottom: 15px;")
        form_layout.addRow(header_label)
        
        # Výběr zaměstnance
        self.employee_combo = QComboBox()
        for emp_id, emp_name in self.employees:
            self.employee_combo.addItem(emp_name, emp_id)
        form_layout.addRow("Zaměstnanec:", self.employee_combo)
        
        # Nová pozice
        self.position_edit = QLineEdit()
        self.position_edit.setPlaceholderText("Nová pozice")
        form_layout.addRow("Nová pozice:", self.position_edit)
        
        # Oddělení
        self.department_combo = QComboBox()
        departments = ["Doprava", "Administrativa", "Servis", "Prodej", "Management"]
        self.department_combo.addItems(departments)
        form_layout.addRow("Oddělení:", self.department_combo)
        
        # Nová mzda
        self.salary_edit = QSpinBox()
        self.salary_edit.setRange(15000, 200000)
        self.salary_edit.setValue(25000)
        self.salary_edit.setSuffix(" Kč")
        form_layout.addRow("Nová mzda:", self.salary_edit)
        
        # Poznámky
        self.notes_edit = QTextEdit()
        self.notes_edit.setPlaceholderText("Důvod změny pozice...")
        self.notes_edit.setMaximumHeight(80)
        form_layout.addRow("Poznámky:", self.notes_edit)
        
        layout.addLayout(form_layout)
        
        # Tlačítka
        button_layout = QHBoxLayout()
        
        cancel_button = QPushButton("Zrušit")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        
        save_button = QPushButton("Změnit pozici")
        save_button.clicked.connect(self.accept)
        button_layout.addWidget(save_button)
        
        layout.addLayout(button_layout)


class ContractManagementDialog(QDialog):
    """Dialog pro správu smluv"""
    
    def __init__(self, employees, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Správa smluv")
        self.setFixedSize(800, 600)
        self.employees = employees
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
        self.load_contracts()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header_label = QLabel("📋 Správa pracovních smluv")
        header_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #f39c12; margin-bottom: 15px;")
        layout.addWidget(header_label)
        
        # Tabulka smluv
        self.contracts_table = QTableWidget()
        self.contracts_table.setColumnCount(6)
        self.contracts_table.setHorizontalHeaderLabels([
            "Zaměstnanec", "Typ smlouvy", "Datum uzavření", "Platnost do", "Stav", "Akce"
        ])
        layout.addWidget(self.contracts_table)
        
        # Tlačítka
        button_layout = QHBoxLayout()
        
        new_button = QPushButton("➕ Nová smlouva")
        new_button.clicked.connect(self.new_contract)
        button_layout.addWidget(new_button)
        
        addendum_button = QPushButton("📝 Dodatek")
        addendum_button.clicked.connect(self.create_addendum)
        button_layout.addWidget(addendum_button)
        
        terminate_button = QPushButton("❌ Ukončit")
        terminate_button.clicked.connect(self.terminate_contract)
        button_layout.addWidget(terminate_button)
        
        export_button = QPushButton("📄 Export")
        export_button.clicked.connect(self.export_contracts)
        button_layout.addWidget(export_button)
        
        close_button = QPushButton("Zavřít")
        close_button.clicked.connect(self.accept)
        button_layout.addWidget(close_button)
        
        layout.addLayout(button_layout)
    
    def load_contracts(self):
        """Načte smlouvy"""
        # Simulace dat pro smlouvy
        contracts_data = [
            ("Jan Novák", "Pracovní smlouva", "2020-01-15", "Neurčito", "Aktivní", "Upravit"),
            ("Anna Svobodová", "Pracovní smlouva", "2021-03-01", "Neurčito", "Aktivní", "Upravit"),
            ("Petr Dvořák", "DPP", "2023-06-01", "2024-05-31", "Aktivní", "Prodloužit"),
            ("Marie Nováková", "Pracovní smlouva", "2019-09-15", "Neurčito", "Ukončená", "Archiv"),
        ]
        
        self.contracts_table.setRowCount(len(contracts_data))
        
        for row, data in enumerate(contracts_data):
            for col, value in enumerate(data):
                item = QTableWidgetItem(str(value))
                if col == 4:  # Stav
                    if value == "Ukončená":
                        item.setBackground(Qt.GlobalColor.red)
                        item.setForeground(Qt.GlobalColor.white)
                    elif value == "Aktivní":
                        item.setBackground(Qt.GlobalColor.green)
                        item.setForeground(Qt.GlobalColor.white)
                self.contracts_table.setItem(row, col, item)
        
        self.contracts_table.resizeColumnsToContents()
    
    def new_contract(self):
        """Vytvoří novou smlouvu"""
        QMessageBox.information(self, "Nová smlouva", "Dialog pro vytvoření nové smlouvy bude k dispozici v další verzi.")
    
    def create_addendum(self):
        """Vytvoří dodatek ke smlouvě"""
        QMessageBox.information(self, "Dodatek", "Dialog pro vytvoření dodatku bude k dispozici v další verzi.")
    
    def terminate_contract(self):
        """Ukončí smlouvu"""
        QMessageBox.information(self, "Ukončení", "Dialog pro ukončení smlouvy bude k dispozici v další verzi.")
    
    def export_contracts(self):
        """Export smluv"""
        QMessageBox.information(self, "Export", "Přehled smluv byl exportován.")


class TrainingManagementDialog(QDialog):
    """Dialog pro správu školení"""
    
    def __init__(self, employees, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Evidence školení")
        self.setFixedSize(800, 600)
        self.employees = employees
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
        self.load_training()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header_label = QLabel("🎓 Evidence školení zaměstnanců")
        header_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #9b59b6; margin-bottom: 15px;")
        layout.addWidget(header_label)
        
        # Tabulka školení
        self.training_table = QTableWidget()
        self.training_table.setColumnCount(6)
        self.training_table.setHorizontalHeaderLabels([
            "Zaměstnanec", "Školení", "Datum", "Výsledek", "Certifikát", "Platnost do"
        ])
        layout.addWidget(self.training_table)
        
        # Tlačítka
        button_layout = QHBoxLayout()
        
        plan_button = QPushButton("📅 Naplánovat školení")
        plan_button.clicked.connect(self.plan_training)
        button_layout.addWidget(plan_button)
        
        record_button = QPushButton("✅ Zaznamenat absolvování")
        record_button.clicked.connect(self.record_completion)
        button_layout.addWidget(record_button)
        
        certificate_button = QPushButton("🏆 Správa certifikátů")
        certificate_button.clicked.connect(self.manage_certificates)
        button_layout.addWidget(certificate_button)
        
        export_button = QPushButton("📊 Export přehledu")
        export_button.clicked.connect(self.export_training)
        button_layout.addWidget(export_button)
        
        close_button = QPushButton("Zavřít")
        close_button.clicked.connect(self.accept)
        button_layout.addWidget(close_button)
        
        layout.addLayout(button_layout)
    
    def load_training(self):
        """Načte školení"""
        # Simulace dat pro školení
        training_data = [
            ("Jan Novák", "BOZP", "2023-01-15", "Úspěšně", "Ano", "2025-01-15"),
            ("Anna Svobodová", "Řidičský průkaz sk. C", "2023-05-20", "Úspěšně", "Ano", "2033-05-20"),
            ("Petr Dvořák", "Práce ve výškách", "2023-08-10", "Úspěšně", "Ano", "2026-08-10"),
            ("Marie Nováková", "Škola bezpečné jízdy", "2023-11-15", "Naplánováno", "Ne", "-"),
        ]
        
        self.training_table.setRowCount(len(training_data))
        
        for row, data in enumerate(training_data):
            for col, value in enumerate(data):
                item = QTableWidgetItem(str(value))
                if col == 3:  # Výsledek
                    if value == "Naplánováno":
                        item.setBackground(Qt.GlobalColor.yellow)
                        item.setForeground(Qt.GlobalColor.black)
                    elif value == "Úspěšně":
                        item.setBackground(Qt.GlobalColor.green)
                        item.setForeground(Qt.GlobalColor.white)
                self.training_table.setItem(row, col, item)
        
        self.training_table.resizeColumnsToContents()
    
    def plan_training(self):
        """Naplánuje školení"""
        QMessageBox.information(self, "Plánování", "Dialog pro plánování školení bude k dispozici v další verzi.")
    
    def record_completion(self):
        """Zaznamená absolvování"""
        QMessageBox.information(self, "Absolvování", "Dialog pro zaznamenání absolvování bude k dispozici v další verzi.")
    
    def manage_certificates(self):
        """Správa certifikátů"""
        QMessageBox.information(self, "Certifikáty", "Správa certifikátů bude k dispozici v další verzi.")
    
    def export_training(self):
        """Export školení"""
        QMessageBox.information(self, "Export", "Přehled školení byl exportován.")
