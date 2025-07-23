#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QPushButton, QTableWidget, QTableWidgetItem,
                            QMessageBox, QGroupBox, QTextEdit)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from role_management import RoleManager, RoleDialog

class RoleManagementWindow(QMainWindow):
    """Okno pro správu rolí a oprávnění"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_roles()
    
    def init_ui(self):
        self.setWindowTitle("Správa rolí a oprávnění")
        self.setGeometry(100, 100, 1000, 700)
        
        # Stylování
        self.setStyleSheet("""
            QMainWindow {
                background: #F2F2F2;
                font-family: 'Inter', 'Roboto', sans-serif;
            }
            
            QLabel {
                color: #2C3E50;
                font-size: 14px;
            }
            
            QPushButton {
                background-color: #3498DB;
                color: white;
                border: none;
                padding: 8px 15px;
                font-size: 12px;
                border-radius: 5px;
                font-weight: bold;
            }
            
            QPushButton:hover {
                background-color: #2980B9;
            }
            
            QPushButton:disabled {
                background-color: #BDC3C7;
                color: #7F8C8D;
            }
            
            QTableWidget {
                background-color: white;
                border: 1px solid #BDC3C7;
                gridline-color: #ECF0F1;
                font-size: 12px;
            }
            
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #ECF0F1;
            }
            
            QTableWidget::item:selected {
                background-color: #3498DB;
                color: white;
            }
            
            QHeaderView::section {
                background-color: #34495E;
                color: white;
                padding: 10px;
                border: none;
                font-weight: bold;
            }
            
            QGroupBox {
                font-weight: bold;
                border: 2px solid #BDC3C7;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 10px 0 10px;
            }
        """)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        
        # Hlavní nadpis
        title_label = QLabel("Správa rolí a oprávnění")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # Tlačítka pro akce
        header_layout = QHBoxLayout()
        
        self.add_role_button = QPushButton("Přidat roli")
        self.add_role_button.clicked.connect(self.add_role)
        header_layout.addWidget(self.add_role_button)
        
        self.edit_role_button = QPushButton("Upravit roli")
        self.edit_role_button.clicked.connect(self.edit_role)
        self.edit_role_button.setEnabled(False)
        header_layout.addWidget(self.edit_role_button)
        
        self.delete_role_button = QPushButton("Smazat roli")
        self.delete_role_button.clicked.connect(self.delete_role)
        self.delete_role_button.setEnabled(False)
        self.delete_role_button.setStyleSheet("""
            QPushButton {
                background-color: #E74C3C;
                color: white;
            }
            QPushButton:hover {
                background-color: #C0392B;
            }
        """)
        header_layout.addWidget(self.delete_role_button)
        
        header_layout.addStretch()
        
        self.refresh_button = QPushButton("Obnovit")
        self.refresh_button.clicked.connect(self.load_roles)
        header_layout.addWidget(self.refresh_button)
        
        layout.addLayout(header_layout)
        
        # Hlavní obsah - rozdělený na role a detail
        content_layout = QHBoxLayout()
        
        # Levá strana - seznam rolí
        roles_group = QGroupBox("Role")
        roles_layout = QVBoxLayout()
        
        self.roles_table = QTableWidget()
        self.roles_table.setColumnCount(4)
        self.roles_table.setHorizontalHeaderLabels([
            "Název", "Popis", "Typ", "Vytvořeno"
        ])
        
        # Nastavení šířky sloupců
        header = self.roles_table.horizontalHeader()
        header.setStretchLastSection(True)
        self.roles_table.setColumnWidth(0, 200)
        self.roles_table.setColumnWidth(1, 300)
        self.roles_table.setColumnWidth(2, 100)
        
        # Propojení signálů
        self.roles_table.itemSelectionChanged.connect(self.on_role_selection_changed)
        
        roles_layout.addWidget(self.roles_table)
        roles_group.setLayout(roles_layout)
        
        content_layout.addWidget(roles_group, 1)
        
        # Pravá strana - detail role
        detail_group = QGroupBox("Oprávnění vybrané role")
        detail_layout = QVBoxLayout()
        
        self.permissions_display = QTextEdit()
        self.permissions_display.setReadOnly(True)
        self.permissions_display.setMaximumHeight(400)
        detail_layout.addWidget(self.permissions_display)
        
        detail_group.setLayout(detail_layout)
        content_layout.addWidget(detail_group, 1)
        
        layout.addLayout(content_layout)
        
        central_widget.setLayout(layout)
    
    def load_roles(self):
        """Načte seznam rolí"""
        roles = RoleManager.get_all_roles()
        
        self.roles_table.setRowCount(len(roles))
        
        for row, role in enumerate(roles):
            role_id, name, display_name, description, is_system, created_date, modified_date = role
            
            name_item = QTableWidgetItem(display_name)
            name_item.setData(Qt.ItemDataRole.UserRole, role_id)  # Uložení ID role
            
            description_item = QTableWidgetItem(description or "")
            type_item = QTableWidgetItem("Systémová" if is_system else "Uživatelská")
            created_item = QTableWidgetItem(created_date.split()[0] if created_date else "")
            
            self.roles_table.setItem(row, 0, name_item)
            self.roles_table.setItem(row, 1, description_item)
            self.roles_table.setItem(row, 2, type_item)
            self.roles_table.setItem(row, 3, created_item)
        
        # Vyčištění detailu
        self.permissions_display.clear()
    
    def on_role_selection_changed(self):
        """Zpracuje změnu výběru role"""
        selected_items = self.roles_table.selectedItems()
        has_selection = len(selected_items) > 0
        
        if has_selection:
            current_row = self.roles_table.currentRow()
            if current_row >= 0:
                # Získání informací o roli
                role_id = self.roles_table.item(current_row, 0).data(Qt.ItemDataRole.UserRole)
                role_name = self.roles_table.item(current_row, 0).text()
                is_system = self.roles_table.item(current_row, 2).text() == "Systémová"
                
                # Povolení/zakázání tlačítek
                self.edit_role_button.setEnabled(True)
                self.delete_role_button.setEnabled(not is_system)  # Systémové role nelze mazat
                
                # Načtení a zobrazení oprávnění
                self.load_role_permissions(role_id, role_name)
            else:
                self.edit_role_button.setEnabled(False)
                self.delete_role_button.setEnabled(False)
                self.permissions_display.clear()
        else:
            self.edit_role_button.setEnabled(False)
            self.delete_role_button.setEnabled(False)
            self.permissions_display.clear()
    
    def load_role_permissions(self, role_id, role_name):
        """Načte a zobrazí oprávnění vybrané role"""
        permissions = RoleManager.get_role_permissions(role_id)
        
        # Seskupení podle modulů
        modules = {}
        for perm in permissions:
            perm_id, perm_name, perm_display_name, perm_description, module = perm
            if module not in modules:
                modules[module] = []
            modules[module].append((perm_display_name, perm_description))
        
        # Sestavení textu
        text = f"<h3>Oprávnění role: {role_name}</h3>"
        
        if not permissions:
            text += "<p><i>Tato role nemá žádná oprávnění.</i></p>"
        else:
            for module_name, perms in modules.items():
                module_display_name = self.get_module_display_name(module_name)
                text += f"<h4>{module_display_name}</h4><ul>"
                
                for perm_display_name, perm_description in perms:
                    text += f"<li><b>{perm_display_name}</b>"
                    if perm_description:
                        text += f" - {perm_description}"
                    text += "</li>"
                
                text += "</ul>"
        
        self.permissions_display.setHtml(text)
    
    def get_module_display_name(self, module_name):
        """Převede systémový název modulu na zobrazovaný"""
        module_names = {
            'users': 'Správa uživatelů',
            'roles': 'Správa rolí',
            'invoices': 'Fakturace',
            'accounting': 'Účetnictví',
            'company': 'Nastavení firmy'
        }
        return module_names.get(module_name, module_name.capitalize())
    
    def add_role(self):
        """Přidá novou roli"""
        dialog = RoleDialog()
        if dialog.exec() == dialog.DialogCode.Accepted:
            self.load_roles()
    
    def edit_role(self):
        """Upraví vybranou roli"""
        current_row = self.roles_table.currentRow()
        if current_row >= 0:
            role_id = self.roles_table.item(current_row, 0).data(Qt.ItemDataRole.UserRole)
            
            # Načtení kompletních dat role
            roles = RoleManager.get_all_roles()
            role_data = None
            for role in roles:
                if role[0] == role_id:
                    role_data = role
                    break
            
            if role_data:
                dialog = RoleDialog(role_data)
                if dialog.exec() == dialog.DialogCode.Accepted:
                    self.load_roles()
    
    def delete_role(self):
        """Smaže vybranou roli"""
        current_row = self.roles_table.currentRow()
        if current_row >= 0:
            role_id = self.roles_table.item(current_row, 0).data(Qt.ItemDataRole.UserRole)
            role_name = self.roles_table.item(current_row, 0).text()
            
            reply = QMessageBox.question(
                self, 
                'Smazání role', 
                f'Opravdu chcete smazat roli "{role_name}"?\n\n'
                f'Tato akce je nevratná.',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                if RoleManager.delete_role(role_id):
                    QMessageBox.information(self, "Úspěch", f"Role {role_name} byla smazána!")
                    self.load_roles()
                else:
                    QMessageBox.critical(self, "Chyba", "Nepodařilo se smazat roli!")


def main():
    """Hlavní funkce pro testování"""
    import sys
    from PyQt6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    window = RoleManagementWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
