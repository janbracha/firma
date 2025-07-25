#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, 
    QTableWidget, QTableWidgetItem, QMessageBox, QFormLayout, QComboBox, QDialog, 
    QGroupBox, QFrame, QScrollArea, QGridLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QBrush
from user_management import UserManager
from change_password_dialog import ChangePasswordDialog

class UserManagementDialog(QDialog):
    """Dialog pro přidání/editaci uživatele"""
    
    def __init__(self, user_data=None):
        super().__init__()
        self.user_data = user_data
        self.is_edit = user_data is not None
        self.init_ui()
        
        if self.is_edit:
            self.load_user_data()
    
    def init_ui(self):
        self.setWindowTitle("Editace uživatele" if self.is_edit else "Nový uživatel")
        self.setFixedSize(500, 400)
        self.setModal(True)
        
        # Stylování
        self.setStyleSheet("""
            QDialog {
                background: #F2F2F2;
                font-family: 'Inter', 'Roboto', sans-serif;
            }
            
            QLabel {
                color: #2C3E50;
                font-size: 14px;
                font-weight: bold;
            }
            
            QLineEdit, QComboBox {
                background-color: white;
                border: 2px solid #E0E0E0;
                border-radius: 8px;
                padding: 8px;
                color: #2C3E50;
                font-size: 14px;
            }
            
            QLineEdit:focus, QComboBox:focus {
                border-color: #6C85A3;
            }
            
            QPushButton {
                background-color: #6C85A3;
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 10px 20px;
                border-radius: 18px;
                border: none;
            }
            
            QPushButton:hover {
                background-color: #5A7393;
            }
            
            QGroupBox {
                font-weight: bold;
                font-size: 16px;
                color: #6C85A3;
                border: 2px solid #E0E0E0;
                border-radius: 10px;
                margin-top: 15px;
                padding-top: 10px;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        layout = QVBoxLayout()
        
        # Základní údaje
        basic_group = QGroupBox("Základní údaje")
        basic_layout = QFormLayout()
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Uživatelské jméno")
        basic_layout.addRow(QLabel("Uživatelské jméno:"), self.username_input)
        
        self.full_name_input = QLineEdit()
        self.full_name_input.setPlaceholderText("Celé jméno")
        basic_layout.addRow(QLabel("Celé jméno:"), self.full_name_input)
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("E-mail")
        basic_layout.addRow(QLabel("E-mail:"), self.email_input)
        
        basic_group.setLayout(basic_layout)
        layout.addWidget(basic_group)
        
        # Přístupové údaje
        access_group = QGroupBox("Přístupové údaje")
        access_layout = QFormLayout()
        
        if not self.is_edit:
            self.password_input = QLineEdit()
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.password_input.setPlaceholderText("Heslo")
            access_layout.addRow(QLabel("Heslo:"), self.password_input)
            
            self.password_confirm_input = QLineEdit()
            self.password_confirm_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.password_confirm_input.setPlaceholderText("Potvrzení hesla")
            access_layout.addRow(QLabel("Potvrzení hesla:"), self.password_confirm_input)
        
        self.role_combo = QComboBox()
        self.role_combo.addItems(["user", "accountant", "admin"])
        access_layout.addRow(QLabel("Role:"), self.role_combo)
        
        access_group.setLayout(access_layout)
        layout.addWidget(access_group)
        
        # Tlačítka
        button_layout = QHBoxLayout()
        
        self.save_button = QPushButton("Uložit")
        self.save_button.clicked.connect(self.save_user)
        button_layout.addWidget(self.save_button)
        
        self.cancel_button = QPushButton("Zrušit")
        self.cancel_button.clicked.connect(self.reject)
        self.cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #95A5A6;
                color: white;
            }
            QPushButton:hover {
                background-color: #7F8C8D;
            }
        """)
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def load_user_data(self):
        """Načte data uživatele pro editaci"""
        if self.user_data:
            self.username_input.setText(self.user_data[1])
            self.full_name_input.setText(self.user_data[2])
            self.email_input.setText(self.user_data[3])
            
            role_index = self.role_combo.findText(self.user_data[4])
            if role_index >= 0:
                self.role_combo.setCurrentIndex(role_index)
    
    def save_user(self):
        """Uloží uživatele"""
        username = self.username_input.text().strip()
        full_name = self.full_name_input.text().strip()
        email = self.email_input.text().strip()
        role = self.role_combo.currentText()
        
        if not username or not full_name:
            QMessageBox.warning(self, "Chyba", "Vyplňte povinná pole!")
            return
        
        if not self.is_edit:
            password = self.password_input.text()
            password_confirm = self.password_confirm_input.text()
            
            if not password:
                QMessageBox.warning(self, "Chyba", "Zadejte heslo!")
                return
            
            if password != password_confirm:
                QMessageBox.warning(self, "Chyba", "Hesla se neshodují!")
                return
            
            # Přidání nového uživatele
            if UserManager.add_user(username, password, full_name, email, role):
                QMessageBox.information(self, "Úspěch", "Uživatel byl úspěšně přidán!")
                self.accept()
            else:
                QMessageBox.critical(self, "Chyba", "Nepodařilo se přidat uživatele!")
        else:
            # Editace existujícího uživatele
            user_id = int(self.user_data[0])  # ID z první pozice
            if UserManager.update_user(user_id, username, full_name, email, role):
                QMessageBox.information(self, "Úspěch", "Uživatel byl úspěšně aktualizován!")
                self.accept()
            else:
                QMessageBox.critical(self, "Chyba", "Nepodařilo se aktualizovat uživatele!")


class UserManagementWindow(QMainWindow):
    """Okno pro správu uživatelů"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_users()
    
    def init_ui(self):
        self.setWindowTitle("Správa uživatelů - Projekt & Develop s.r.o.")
        self.setGeometry(100, 100, 1200, 800)
        
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

    def create_header(self, layout):
        """Vytvoří moderní hlavičku"""
        header_frame = QFrame()
        header_frame.setObjectName("headerFrame")
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(20, 20, 20, 20)
        
        # Levá část - informace o sekci
        left_layout = QVBoxLayout()
        
        title_label = QLabel("👤 Správa uživatelů")
        title_label.setObjectName("titleLabel")
        left_layout.addWidget(title_label)
        
        subtitle_label = QLabel("Správa uživatelských účtů a přístupů")
        subtitle_label.setObjectName("subtitleLabel")
        left_layout.addWidget(subtitle_label)
        
        header_layout.addLayout(left_layout)
        header_layout.addStretch()
        
        layout.addWidget(header_frame)
    
    def create_content(self, layout):
        """Vytvoří hlavní obsah okna"""
        
        # Akce s kartami
        actions_frame = self.create_section_frame("⚡ Rychlé akce", "Správa uživatelských účtů")
        actions_grid = QGridLayout()
        actions_grid.setSpacing(15)
        
        # Karty akcí
        actions = [
            ("➕ Přidat uživatele", "Vytvořit nový uživatelský účet", self.add_user),
            ("✏️ Upravit uživatele", "Upravit vybraný účet", self.edit_user),
            ("� Změnit heslo", "Změnit heslo uživatele", self.change_password),
            ("🟢 Aktivovat uživatele", "Znovu aktivovat neaktivní účet", self.activate_user),
            ("🟡 Deaktivovat uživatele", "Dočasně deaktivovat účet", self.delete_user),
            ("� Odstranit trvale", "Trvale smazat neaktivní účet", self.permanently_delete_user),
        ]
        
        for i, (title, desc, func) in enumerate(actions):
            card = self.create_action_card(title, desc, func)
            actions_grid.addWidget(card, i // 2, i % 2)
        
        actions_frame.layout().addLayout(actions_grid)
        layout.addWidget(actions_frame)
        
        # Tabulka uživatelů
        table_frame = self.create_section_frame("📋 Seznam uživatelů", "Přehled všech uživatelských účtů")
        
        # Tabulka uživatelů
        self.users_table = QTableWidget()
        self.users_table.setObjectName("dataTable")
        self.users_table.setColumnCount(6)
        self.users_table.setHorizontalHeaderLabels([
            'ID', 'Uživatelské jméno', 'Celé jméno', 'Email', 'Role', 'Aktivní'
        ])
        
        # Nastavení tabulky
        self.users_table.setAlternatingRowColors(True)
        self.users_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        
        table_frame.layout().addWidget(self.users_table)
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

    def init_ui_old(self):
        self.setWindowTitle("Správa uživatelů")
        self.setGeometry(100, 100, 900, 600)
        
        # Stylování
        self.setStyleSheet("""
            QMainWindow {
                background: #F2F2F2;
                font-family: 'Inter', 'Roboto', sans-serif;
            }
            
            QLabel {
                color: #2C3E50;
                font-size: 14px;
                font-weight: bold;
            }
            
            QPushButton {
                background-color: #6C85A3;
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 10px 20px;
                border-radius: 18px;
                border: none;
            }
            
            QPushButton:hover {
                background-color: #5A7393;
            }
            
            QTableWidget {
                background-color: white;
                border: 2px solid #E0E0E0;
                border-radius: 10px;
                gridline-color: #E0E0E0;
                font-size: 14px;
            }
            
            QHeaderView::section {
                background-color: #6C85A3;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
            
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #E0E0E0;
            }
            
            QTableWidget::item:selected {
                background-color: #D4DBE4;
                color: #2C3E50;
            }
        """)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        
        # Hlavička
        header_layout = QHBoxLayout()
        title_label = QLabel("<h2>Správa uživatelů</h2>")
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        # Tlačítka
        self.add_user_button = QPushButton("Přidat uživatele")
        self.add_user_button.clicked.connect(self.add_user)
        header_layout.addWidget(self.add_user_button)
        
        self.edit_user_button = QPushButton("Upravit")
        self.edit_user_button.clicked.connect(self.edit_user)
        self.edit_user_button.setEnabled(False)
        header_layout.addWidget(self.edit_user_button)
        
        self.change_password_button = QPushButton("Změnit heslo")
        self.change_password_button.clicked.connect(self.change_password)
        self.change_password_button.setEnabled(False)
        self.change_password_button.setStyleSheet("""
            QPushButton {
                background-color: #F39C12;
                color: white;
            }
            QPushButton:hover {
                background-color: #E67E22;
            }
        """)
        header_layout.addWidget(self.change_password_button)
        
        self.activate_user_button = QPushButton("Aktivovat")
        self.activate_user_button.clicked.connect(self.activate_user)
        self.activate_user_button.setEnabled(False)
        self.activate_user_button.setStyleSheet("""
            QPushButton {
                background-color: #27AE60;
                color: white;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        header_layout.addWidget(self.activate_user_button)
        
        self.delete_user_button = QPushButton("Deaktivovat")
        self.delete_user_button.clicked.connect(self.delete_user)
        self.delete_user_button.setEnabled(False)
        self.delete_user_button.setStyleSheet("""
            QPushButton {
                background-color: #E74C3C;
                color: white;
            }
            QPushButton:hover {
                background-color: #C0392B;
            }
        """)
        header_layout.addWidget(self.delete_user_button)
        
        self.permanently_delete_button = QPushButton("Odstranit trvale")
        self.permanently_delete_button.clicked.connect(self.permanently_delete_user)
        self.permanently_delete_button.setEnabled(False)
        self.permanently_delete_button.setStyleSheet("""
            QPushButton {
                background-color: #8B0000;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #A52A2A;
            }
        """)
        header_layout.addWidget(self.permanently_delete_button)
        
        layout.addLayout(header_layout)
        
        # Tabulka uživatelů
        self.users_table = QTableWidget()
        self.users_table.setColumnCount(7)  # Vrátíme zpět na 7 sloupců
        self.users_table.setHorizontalHeaderLabels([
            "ID", "Uživatelské jméno", "Celé jméno", "E-mail", 
            "Role", "Stav", "Poslední přihlášení"  # Přidán zpět sloupec "Stav"
        ])
        
        # Nastavení šířky sloupců
        header = self.users_table.horizontalHeader()
        header.setStretchLastSection(True)
        self.users_table.setColumnWidth(0, 50)
        self.users_table.setColumnWidth(1, 150)
        self.users_table.setColumnWidth(2, 200)
        self.users_table.setColumnWidth(3, 200)
        self.users_table.setColumnWidth(4, 100)
        self.users_table.setColumnWidth(5, 100)  # Sloupec "Stav"
        
        # Propojení signálů
        self.users_table.itemSelectionChanged.connect(self.on_selection_changed)
        
        layout.addWidget(self.users_table)
        
        # Tlačítko pro obnovení
        refresh_layout = QHBoxLayout()
        refresh_layout.addStretch()
        
        self.refresh_button = QPushButton("Obnovit")
        self.refresh_button.clicked.connect(self.load_users)
        refresh_layout.addWidget(self.refresh_button)
        
        layout.addLayout(refresh_layout)
        
        central_widget.setLayout(layout)
    
    def load_users(self):
        """Načte seznam uživatelů"""
        # Blokujeme signály během aktualizace tabulky
        self.users_table.blockSignals(True)
        
        users = UserManager.get_all_users()
        
        # Nejprve vyčistíme obsah tabulky ale zachováme strukturu
        self.users_table.setRowCount(0)
        self.users_table.setRowCount(len(users))
        
        for row, user in enumerate(users):
            # Vytvoření všech položek včetně sloupce "Stav"
            id_item = QTableWidgetItem(str(user[0]))
            username_item = QTableWidgetItem(user[1])
            fullname_item = QTableWidgetItem(user[2])
            email_item = QTableWidgetItem(user[3] or "")
            role_item = QTableWidgetItem(user[4])
            status_item = QTableWidgetItem("Aktivní" if user[5] == 1 else "Neaktivní")
            lastlogin_item = QTableWidgetItem(user[7] or "Nikdy")
            
            # Nastavení položek do tabulky
            self.users_table.setItem(row, 0, id_item)
            self.users_table.setItem(row, 1, username_item)
            self.users_table.setItem(row, 2, fullname_item)
            self.users_table.setItem(row, 3, email_item)
            self.users_table.setItem(row, 4, role_item)
            self.users_table.setItem(row, 5, status_item)
            self.users_table.setItem(row, 6, lastlogin_item)
        
        # Obnovíme signály
        self.users_table.blockSignals(False)
        
        # Vyčistíme výběr
        self.users_table.clearSelection()
    
    def on_selection_changed(self):
        """Zpracuje změnu výběru v tabulce - nepoužívá se v moderním stylu s kartami"""
        # V moderním stylu s kartami není potřeba aktualizovat stav tlačítek
        pass
    
    def update_button_states(self):
        """Aktualizuje stav tlačítek podle vybraného uživatele - nepoužívá se v moderním stylu s kartami"""
        # V novém moderním stylu se používají karty místo tlačítek
        # Tato metoda je zachována kvůli kompatibilitě, ale nic nedělá
        pass
    
    def add_user(self):
        """Přidá nového uživatele"""
        dialog = UserManagementDialog()
        if dialog.exec() == dialog.DialogCode.Accepted:
            self.load_users()
            self.update_button_states()
    
    def edit_user(self):
        """Upraví vybraného uživatele"""
        current_row = self.users_table.currentRow()
        if current_row >= 0:
            # Získání dat uživatele z tabulky
            user_data = []
            for col in range(self.users_table.columnCount()):
                item = self.users_table.item(current_row, col)
                user_data.append(item.text() if item else "")
            
            dialog = UserManagementDialog(user_data)
            if dialog.exec() == dialog.DialogCode.Accepted:
                self.load_users()
                self.update_button_states()
        else:
            QMessageBox.warning(self, "Chyba", "Nejprve vyberte uživatele v tabulce, kterého chcete upravit.")
    
    def change_password(self):
        """Změní heslo vybraného uživatele"""
        current_row = self.users_table.currentRow()
        if current_row >= 0:
            user_id = int(self.users_table.item(current_row, 0).text())
            username = self.users_table.item(current_row, 1).text()
            
            dialog = ChangePasswordDialog(user_id, username)
            dialog.exec()
        else:
            QMessageBox.warning(self, "Chyba", "Nejprve vyberte uživatele v tabulce, kterému chcete změnit heslo.")
    
    def activate_user(self):
        """Aktivuje deaktivovaného uživatele"""
        current_row = self.users_table.currentRow()
        if current_row >= 0:
            user_id = int(self.users_table.item(current_row, 0).text())
            username = self.users_table.item(current_row, 1).text()
            status_text = self.users_table.item(current_row, 5).text()
            
            # Kontrola, zda je uživatel neaktivní
            if status_text == "Aktivní":
                QMessageBox.warning(self, "Chyba", f"Uživatel {username} je již aktivní!")
                return
            
            reply = QMessageBox.question(
                self, 
                'Aktivace uživatele', 
                f'Opravdu chcete znovu aktivovat uživatele "{username}"?',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                if UserManager.activate_user(user_id):
                    QMessageBox.information(self, "Úspěch", f"Uživatel {username} byl znovu aktivován!")
                    self.load_users()
                    self.update_button_states()  # Aktualizace stavů tlačítek
                else:
                    QMessageBox.critical(self, "Chyba", "Nepodařilo se aktivovat uživatele!")
        else:
            QMessageBox.warning(self, "Chyba", "Nejprve vyberte neaktivního uživatele v tabulce, kterého chcete aktivovat.")
    
    def delete_user(self):
        """Smaže vybraného uživatele"""
        current_row = self.users_table.currentRow()
        if current_row >= 0:
            user_id = int(self.users_table.item(current_row, 0).text())
            username = self.users_table.item(current_row, 1).text()
            role = self.users_table.item(current_row, 4).text()
            
            # Odebrána kontrola admin role - admin uživatele lze nyní také deaktivovat
            
            reply = QMessageBox.question(
                self, 
                'Deaktivace uživatele', 
                f'Opravdu chcete deaktivovat uživatele "{username}"?\n\n'
                f'Uživatel bude deaktivován, ale jeho data zůstanou zachována.',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                if UserManager.delete_user(user_id):
                    QMessageBox.information(self, "Úspěch", f"Uživatel {username} byl deaktivován!")
                    self.load_users()
                    self.update_button_states()  # Aktualizace stavů tlačítek
                else:
                    QMessageBox.critical(self, "Chyba", "Nepodařilo se deaktivovat uživatele!")
        else:
            QMessageBox.warning(self, "Chyba", "Nejprve vyberte aktivního uživatele v tabulce, kterého chcete deaktivovat.")
    
    def permanently_delete_user(self):
        """Trvale odstraní vybraného uživatele"""
        current_row = self.users_table.currentRow()
        if current_row >= 0:
            user_id = int(self.users_table.item(current_row, 0).text())
            username = self.users_table.item(current_row, 1).text()
            status_text = self.users_table.item(current_row, 5).text()
            
            # Kontrola, zda je uživatel neaktivní
            if status_text == "Aktivní":
                QMessageBox.warning(self, "Chyba", f"Nelze trvale odstranit aktivního uživatele {username}!\n\nPrvním krokem jej deaktivujte a poté můžete provést trvalé odstranění.")
                return
            
            reply = QMessageBox.question(
                self, 
                'TRVALÉ ODSTRANĚNÍ UŽIVATELE', 
                f'⚠️ POZOR! ⚠️\n\n'
                f'Opravdu chcete TRVALE ODSTRANIT uživatele "{username}"?\n\n'
                f'🚨 TATO AKCE JE NEVRATNÁ! 🚨\n'
                f'Uživatel a všechna jeho data budou z databáze trvale vymazána.\n\n'
                f'Pokud si nejste jisti, použijte místo toho "Deaktivovat".',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No  # Výchozí je "No" pro bezpečnost
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                # Druhé potvrzení pro extra bezpečnost
                final_reply = QMessageBox.question(
                    self, 
                    'FINÁLNÍ POTVRZENÍ', 
                    f'Skutečně chcete trvale odstranit uživatele "{username}"?\n\n'
                    f'Napište "ODSTRANIT" pro potvrzení:',
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    QMessageBox.StandardButton.No
                )
                
                if final_reply == QMessageBox.StandardButton.Yes:
                    if UserManager.permanently_delete_user(user_id):
                        QMessageBox.information(self, "Úspěch", f"Uživatel {username} byl trvale odstraněn!")
                        self.load_users()
                        self.update_button_states()
                    else:
                        QMessageBox.critical(self, "Chyba", "Nepodařilo se trvale odstranit uživatele!")
        else:
            QMessageBox.warning(self, "Chyba", "Nejprve vyberte neaktivního uživatele v tabulce, kterého chcete trvale odstranit.")


def main():
    """Hlavní funkce pro testování"""
    import sys
    from PyQt6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    window = UserManagementWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
