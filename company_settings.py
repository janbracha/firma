#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QLineEdit, QPushButton, QTextEdit, QFileDialog,
                            QMessageBox, QGroupBox, QFormLayout, QTabWidget,
                            QScrollArea, QComboBox, QSpinBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QIcon
import os
from database import connect

class CompanySettings:
    """Správa nastavení firmy"""
    
    @staticmethod
    def get_company_settings():
        """Načte nastavení firmy z databáze"""
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM company_settings WHERE id = 1")
        settings = cursor.fetchone()
        conn.close()
        
        if settings:
            return {
                'company_name': settings[1],
                'address': settings[2],
                'city': settings[3],
                'postal_code': settings[4],
                'country': settings[5],
                'phone': settings[6],
                'email': settings[7],
                'website': settings[8],
                'ico': settings[9],
                'dic': settings[10],
                'logo_path': settings[11],
                'invoice_template': settings[12],
                'invoice_footer': settings[13],
                'default_currency': settings[14],
                'tax_rate': settings[15]
            }
        return None
    
    @staticmethod
    def save_company_settings(settings):
        """Uloží nastavení firmy do databáze"""
        conn = connect()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                UPDATE company_settings SET
                    company_name = ?,
                    address = ?,
                    city = ?,
                    postal_code = ?,
                    country = ?,
                    phone = ?,
                    email = ?,
                    website = ?,
                    ico = ?,
                    dic = ?,
                    logo_path = ?,
                    invoice_template = ?,
                    invoice_footer = ?,
                    default_currency = ?,
                    tax_rate = ?
                WHERE id = 1
            """, (
                settings['company_name'],
                settings['address'],
                settings['city'],
                settings['postal_code'],
                settings['country'],
                settings['phone'],
                settings['email'],
                settings['website'],
                settings['ico'],
                settings['dic'],
                settings['logo_path'],
                settings['invoice_template'],
                settings['invoice_footer'],
                settings['default_currency'],
                settings['tax_rate']
            ))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            conn.close()
            return False


class CompanySettingsWindow(QMainWindow):
    """Okno pro správu nastavení firmy"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_settings()
        
    def init_ui(self):
        self.setWindowTitle("Nastavení firmy")
        self.setGeometry(100, 100, 800, 700)
        
        # Použití stejného stylu jako v ostatních modulech
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
            
            QLineEdit, QTextEdit, QComboBox, QSpinBox {
                background-color: white;
                border: 2px solid #E0E0E0;
                border-radius: 8px;
                padding: 8px;
                color: #2C3E50;
                font-size: 14px;
            }
            
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QSpinBox:focus {
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
            
            QPushButton:pressed {
                background-color: #4A6383;
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
            
            QTabWidget::pane {
                border: 2px solid #E0E0E0;
                border-radius: 10px;
                background: white;
            }
            
            QTabBar::tab {
                background: #E8E8E8;
                color: #2C3E50;
                padding: 12px 24px;
                margin-right: 2px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }
            
            QTabBar::tab:selected {
                background: #6C85A3;
                color: white;
            }
            
            QTabBar::tab:hover {
                background: #D4DBE4;
            }
        """)
        
        # Vytvoření centrálního widgetu
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Hlavní layout
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Záložky
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        
        # Záložka - Základní údaje
        self.create_basic_info_tab()
        
        # Záložka - Fakturační nastavení
        self.create_invoice_settings_tab()
        
        # Záložka - Logo a vzhled
        self.create_logo_tab()
        
        # Tlačítka
        button_layout = QHBoxLayout()
        
        self.save_button = QPushButton("Uložit změny")
        self.save_button.clicked.connect(self.save_settings)
        button_layout.addWidget(self.save_button)
        
        self.cancel_button = QPushButton("Zrušit")
        self.cancel_button.clicked.connect(self.close)
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
    
    def create_basic_info_tab(self):
        """Vytvoří záložku se základními údaji"""
        tab = QWidget()
        self.tab_widget.addTab(tab, "Základní údaje")
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        tab_layout = QVBoxLayout()
        tab.setLayout(tab_layout)
        tab_layout.addWidget(scroll)
        
        content_widget = QWidget()
        scroll.setWidget(content_widget)
        layout = QVBoxLayout()
        content_widget.setLayout(layout)
        
        # Skupina - Identifikace firmy
        company_group = QGroupBox("Identifikace firmy")
        company_layout = QFormLayout()
        
        self.company_name_input = QLineEdit()
        company_layout.addRow(QLabel("Název firmy:"), self.company_name_input)
        
        self.ico_input = QLineEdit()
        company_layout.addRow(QLabel("IČO:"), self.ico_input)
        
        self.dic_input = QLineEdit()
        company_layout.addRow(QLabel("DIČ:"), self.dic_input)
        
        company_group.setLayout(company_layout)
        layout.addWidget(company_group)
        
        # Skupina - Adresa
        address_group = QGroupBox("Adresa")
        address_layout = QFormLayout()
        
        self.address_input = QLineEdit()
        address_layout.addRow(QLabel("Ulice a číslo:"), self.address_input)
        
        self.city_input = QLineEdit()
        address_layout.addRow(QLabel("Město:"), self.city_input)
        
        self.postal_code_input = QLineEdit()
        address_layout.addRow(QLabel("PSČ:"), self.postal_code_input)
        
        self.country_input = QLineEdit()
        address_layout.addRow(QLabel("Země:"), self.country_input)
        
        address_group.setLayout(address_layout)
        layout.addWidget(address_group)
        
        # Skupina - Kontakt
        contact_group = QGroupBox("Kontaktní údaje")
        contact_layout = QFormLayout()
        
        self.phone_input = QLineEdit()
        contact_layout.addRow(QLabel("Telefon:"), self.phone_input)
        
        self.email_input = QLineEdit()
        contact_layout.addRow(QLabel("E-mail:"), self.email_input)
        
        self.website_input = QLineEdit()
        contact_layout.addRow(QLabel("Web:"), self.website_input)
        
        contact_group.setLayout(contact_layout)
        layout.addWidget(contact_group)
        
        layout.addStretch()
    
    def create_invoice_settings_tab(self):
        """Vytvoří záložku s nastavením fakturace"""
        tab = QWidget()
        self.tab_widget.addTab(tab, "Fakturační nastavení")
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        tab_layout = QVBoxLayout()
        tab.setLayout(tab_layout)
        tab_layout.addWidget(scroll)
        
        content_widget = QWidget()
        scroll.setWidget(content_widget)
        layout = QVBoxLayout()
        content_widget.setLayout(layout)
        
        # Skupina - Základní nastavení
        basic_group = QGroupBox("Základní nastavení")
        basic_layout = QFormLayout()
        
        self.currency_combo = QComboBox()
        self.currency_combo.addItems(["CZK", "EUR", "USD"])
        basic_layout.addRow(QLabel("Výchozí měna:"), self.currency_combo)
        
        self.tax_rate_input = QSpinBox()
        self.tax_rate_input.setRange(0, 50)
        self.tax_rate_input.setSuffix(" %")
        basic_layout.addRow(QLabel("Sazba DPH:"), self.tax_rate_input)
        
        basic_group.setLayout(basic_layout)
        layout.addWidget(basic_group)
        
        # Skupina - Šablona faktury
        template_group = QGroupBox("Šablona faktury")
        template_layout = QVBoxLayout()
        
        self.invoice_template_input = QTextEdit()
        self.invoice_template_input.setMaximumHeight(150)
        self.invoice_template_input.setPlaceholderText("Vlastní hlavička faktury...")
        template_layout.addWidget(QLabel("Hlavička faktury:"))
        template_layout.addWidget(self.invoice_template_input)
        
        self.invoice_footer_input = QTextEdit()
        self.invoice_footer_input.setMaximumHeight(100)
        self.invoice_footer_input.setPlaceholderText("Patička faktury - bankovní údaje, podmínky...")
        template_layout.addWidget(QLabel("Patička faktury:"))
        template_layout.addWidget(self.invoice_footer_input)
        
        template_group.setLayout(template_layout)
        layout.addWidget(template_group)
        
        layout.addStretch()
    
    def create_logo_tab(self):
        """Vytvoří záložku s logem a vzhledem"""
        tab = QWidget()
        self.tab_widget.addTab(tab, "Logo a vzhled")
        
        layout = QVBoxLayout()
        tab.setLayout(layout)
        
        # Skupina - Logo firmy
        logo_group = QGroupBox("Logo firmy")
        logo_layout = QVBoxLayout()
        
        # Náhled loga
        self.logo_label = QLabel()
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.logo_label.setFixedSize(200, 100)
        self.logo_label.setStyleSheet("border: 2px dashed #E0E0E0; background: white;")
        self.logo_label.setText("Žádné logo")
        logo_layout.addWidget(self.logo_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Tlačítka pro logo
        logo_button_layout = QHBoxLayout()
        
        self.load_logo_button = QPushButton("Načíst logo")
        self.load_logo_button.clicked.connect(self.load_logo)
        logo_button_layout.addWidget(self.load_logo_button)
        
        self.remove_logo_button = QPushButton("Odebrat logo")
        self.remove_logo_button.clicked.connect(self.remove_logo)
        self.remove_logo_button.setStyleSheet("""
            QPushButton {
                background-color: #E74C3C;
                color: white;
            }
            QPushButton:hover {
                background-color: #C0392B;
            }
        """)
        logo_button_layout.addWidget(self.remove_logo_button)
        
        logo_layout.addLayout(logo_button_layout)
        
        # Cesta k logu
        self.logo_path_input = QLineEdit()
        self.logo_path_input.setReadOnly(True)
        self.logo_path_input.setPlaceholderText("Není vybráno žádné logo")
        logo_layout.addWidget(QLabel("Cesta k logu:"))
        logo_layout.addWidget(self.logo_path_input)
        
        logo_group.setLayout(logo_layout)
        layout.addWidget(logo_group)
        
        layout.addStretch()
    
    def load_logo(self):
        """Načte logo firmy"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Vyberte logo firmy",
            "",
            "Obrázky (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        
        if file_path:
            self.logo_path_input.setText(file_path)
            
            # Zobrazení náhledu
            pixmap = QPixmap(file_path)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(180, 80, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                self.logo_label.setPixmap(scaled_pixmap)
            else:
                self.logo_label.setText("Chyba při načítání")
    
    def remove_logo(self):
        """Odebere logo"""
        self.logo_path_input.clear()
        self.logo_label.clear()
        self.logo_label.setText("Žádné logo")
    
    def load_settings(self):
        """Načte nastavení z databáze"""
        settings = CompanySettings.get_company_settings()
        
        if settings:
            self.company_name_input.setText(settings['company_name'] or "")
            self.address_input.setText(settings['address'] or "")
            self.city_input.setText(settings['city'] or "")
            self.postal_code_input.setText(settings['postal_code'] or "")
            self.country_input.setText(settings['country'] or "")
            self.phone_input.setText(settings['phone'] or "")
            self.email_input.setText(settings['email'] or "")
            self.website_input.setText(settings['website'] or "")
            self.ico_input.setText(settings['ico'] or "")
            self.dic_input.setText(settings['dic'] or "")
            self.logo_path_input.setText(settings['logo_path'] or "")
            self.invoice_template_input.setPlainText(settings['invoice_template'] or "")
            self.invoice_footer_input.setPlainText(settings['invoice_footer'] or "")
            
            # Nastavení comboboxu a spinboxu
            currency_index = self.currency_combo.findText(settings['default_currency'] or "CZK")
            if currency_index >= 0:
                self.currency_combo.setCurrentIndex(currency_index)
            
            self.tax_rate_input.setValue(settings['tax_rate'] or 21)
            
            # Načtení loga
            if settings['logo_path'] and os.path.exists(settings['logo_path']):
                pixmap = QPixmap(settings['logo_path'])
                if not pixmap.isNull():
                    scaled_pixmap = pixmap.scaled(180, 80, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                    self.logo_label.setPixmap(scaled_pixmap)
    
    def save_settings(self):
        """Uloží nastavení do databáze"""
        settings = {
            'company_name': self.company_name_input.text(),
            'address': self.address_input.text(),
            'city': self.city_input.text(),
            'postal_code': self.postal_code_input.text(),
            'country': self.country_input.text(),
            'phone': self.phone_input.text(),
            'email': self.email_input.text(),
            'website': self.website_input.text(),
            'ico': self.ico_input.text(),
            'dic': self.dic_input.text(),
            'logo_path': self.logo_path_input.text(),
            'invoice_template': self.invoice_template_input.toPlainText(),
            'invoice_footer': self.invoice_footer_input.toPlainText(),
            'default_currency': self.currency_combo.currentText(),
            'tax_rate': self.tax_rate_input.value()
        }
        
        if CompanySettings.save_company_settings(settings):
            QMessageBox.information(self, "Úspěch", "Nastavení bylo úspěšně uloženo!")
            self.close()
        else:
            QMessageBox.critical(self, "Chyba", "Nepodařilo se uložit nastavení!")


def main():
    """Hlavní funkce pro testování"""
    import sys
    from PyQt6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    window = CompanySettingsWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
