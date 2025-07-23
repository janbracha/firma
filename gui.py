from PyQt6.QtWidgets import (
    QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QHBoxLayout,
    QMenuBar, QMenu, QMessageBox, QGroupBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from database import create_tables
from invoice_management import InvoiceManagementWindow
from company_managment import CompanyManagementWindow
from cash_journal import CashJournalWindow
from trip_book import TripBookWindow
from user_management import UserManager
from simple_login import SimpleLoginDialog
from company_settings import CompanySettingsWindow
from user_management_window import UserManagementWindow
from role_management_window import RoleManagementWindow
from document_management_window import DocumentManagementWindow

class InvoiceApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_user = None
        self.invoice_window = None
        self.company_window = None
        self.cash_journal_window = None
        self.trip_book_window = None
        self.company_settings_window = None
        self.user_management_window = None
        self.role_management_window = None
        
        self.setWindowTitle("Správa firmy - Projekt & Develop s.r.o.")
        self.setGeometry(200, 200, 900, 700)
        
        # Přihlášení uživatele
        if not self.login():
            return
        
        # Inicializace databáze
        create_tables()
        
        # Inicializace oken po přihlášení
        self.init_windows()
        self.init_ui()
        self.setup_menu()

    
    def login(self):
        """Zobrazí dialog pro přihlášení"""
        login_dialog = SimpleLoginDialog()
        if login_dialog.exec() == login_dialog.DialogCode.Accepted:
            self.current_user = login_dialog.get_current_user()
            return True
        else:
            return False
    
    def init_windows(self):
        """Inicializuje okna aplikace"""
        self.invoice_window = InvoiceManagementWindow()
        self.company_window = CompanyManagementWindow()
        self.cash_journal_window = CashJournalWindow()
        self.trip_book_window = TripBookWindow()
        self.company_settings_window = CompanySettingsWindow()
        self.user_management_window = UserManagementWindow()
    
    def init_ui(self):
        """Inicializuje uživatelské rozhraní"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        # Hlavička s informacemi o uživateli
        header_layout = QHBoxLayout()
        
        welcome_label = QLabel(f"<h2>Vítejte ve správě firmy</h2><p>Přihlášen jako: <b>{self.current_user['full_name']}</b> ({self.current_user['role']})</p>")
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        header_layout.addWidget(welcome_label)
        
        logout_button = QPushButton("Odhlásit se")
        logout_button.clicked.connect(self.logout)
        logout_button.setStyleSheet("""
            QPushButton {
                background-color: #E74C3C;
                color: white;
                font-size: 12px;
                padding: 8px 16px;
                border-radius: 12px;
                max-width: 120px;
            }
            QPushButton:hover {
                background-color: #C0392B;
            }
        """)
        header_layout.addWidget(logout_button)
        
        layout.addLayout(header_layout)

        # Základní funkce
        main_group = QGroupBox("Základní funkce")
        main_layout = QVBoxLayout()
        
        # Tlačítka pro jednotlivé sekce s kontrolou oprávnění
        if UserManager.has_permission(self.current_user['role'], 'invoices'):
            self.manage_invoices_button = QPushButton("Správa faktur")
            self.manage_invoices_button.clicked.connect(self.show_invoice_management)
            main_layout.addWidget(self.manage_invoices_button)

        if UserManager.has_permission(self.current_user['role'], 'companies'):
            self.manage_companies_button = QPushButton("Správa firem")
            self.manage_companies_button.clicked.connect(self.show_company_management)
            main_layout.addWidget(self.manage_companies_button)

        if UserManager.has_permission(self.current_user['role'], 'cash_journal'):
            self.manage_cash_journal_button = QPushButton("Pokladní deník")
            self.manage_cash_journal_button.clicked.connect(self.show_cash_journal)
            main_layout.addWidget(self.manage_cash_journal_button)

        if UserManager.has_permission(self.current_user['role'], 'trip_book'):
            self.manage_trip_book_button = QPushButton("Kniha jízd")
            self.manage_trip_book_button.clicked.connect(self.show_trip_book)
            main_layout.addWidget(self.manage_trip_book_button)
        
        main_group.setLayout(main_layout)
        layout.addWidget(main_group)
        
        # Systémové funkce (pouze pro admina)
        if UserManager.has_permission(self.current_user['role'], 'all'):
            system_group = QGroupBox("Systémové funkce")
            system_layout = QVBoxLayout()
            
            self.company_settings_button = QPushButton("Nastavení firmy")
            self.company_settings_button.clicked.connect(self.show_company_settings)
            system_layout.addWidget(self.company_settings_button)
            
            self.user_management_button = QPushButton("Správa uživatelů")
            self.user_management_button.clicked.connect(self.show_user_management)
            system_layout.addWidget(self.user_management_button)
            
            self.role_management_button = QPushButton("Správa rolí")
            self.role_management_button.clicked.connect(self.show_role_management)
            system_layout.addWidget(self.role_management_button)
            
            self.document_management_button = QPushButton("📎 Správa dokumentů")
            self.document_management_button.clicked.connect(self.show_document_management)
            system_layout.addWidget(self.document_management_button)
            
            system_group.setLayout(system_layout)
            layout.addWidget(system_group)

        central_widget.setLayout(layout)
        
        # Stylizace UI (stejná jako ostatní sekce)
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
    
    def setup_menu(self):
        """Nastavuje menu aplikace"""
        menubar = self.menuBar()
        
        # Soubor menu
        file_menu = menubar.addMenu('Soubor')
        
        logout_action = QAction('Odhlásit se', self)
        logout_action.triggered.connect(self.logout)
        file_menu.addAction(logout_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction('Ukončit', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Systém menu (pouze pro admina)
        if UserManager.has_permission(self.current_user['role'], 'all'):
            system_menu = menubar.addMenu('Systém')
            
            company_settings_action = QAction('Nastavení firmy', self)
            company_settings_action.triggered.connect(self.show_company_settings)
            system_menu.addAction(company_settings_action)
            
            user_management_action = QAction('Správa uživatelů', self)
            user_management_action.triggered.connect(self.show_user_management)
            system_menu.addAction(user_management_action)
            
            role_management_action = QAction('Správa rolí', self)
            role_management_action.triggered.connect(self.show_role_management)
            system_menu.addAction(role_management_action)
            
            document_management_action = QAction('Správa dokumentů', self)
            document_management_action.triggered.connect(self.show_document_management)
            system_menu.addAction(document_management_action)
        
        # Nápověda menu
        help_menu = menubar.addMenu('Nápověda')
        
        about_action = QAction('O aplikaci', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def logout(self):
        """Odhlášení uživatele"""
        reply = QMessageBox.question(self, 'Odhlášení', 
                                   'Opravdu se chcete odhlásit?',
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            self.current_user = None
            self.close()
            # Restartování aplikace
            import sys
            from PyQt6.QtWidgets import QApplication
            app = QApplication.instance()
            if app:
                app.quit()
                QApplication.exit()
    
    def show_about(self):
        """Zobrazí dialog O aplikaci"""
        QMessageBox.about(self, "O aplikaci", 
                         "Správa firmy v1.0\n"
                         "Projekt & Develop s.r.o.\n\n"
                         "Systém pro správu faktur, firem a účetnictví.")
    
    def show_company_settings(self):
        """Zobrazí nastavení firmy"""
        if not self.company_settings_window:
            self.company_settings_window = CompanySettingsWindow()
        self.company_settings_window.show()
    
    def show_user_management(self):
        """Zobrazí správu uživatelů"""
        # Vždycky vytvoříme novou instanci pro zajištění aktuálních dat
        self.user_management_window = UserManagementWindow()
        self.user_management_window.show()

    def show_role_management(self):
        """Zobrazí správu rolí"""
        # Vždycky vytvoříme novou instanci pro zajištění aktuálních dat
        self.role_management_window = RoleManagementWindow()
        self.role_management_window.show()

    def show_document_management(self):
        """Zobrazí správu dokumentů"""
        # Vždycky vytvoříme novou instanci pro zajištění aktuálních dat
        self.document_management_window = DocumentManagementWindow(
            title_suffix="Všechny dokumenty"
        )
        self.document_management_window.show()

    def show_invoice_management(self):
        if not self.invoice_window:
            self.invoice_window = InvoiceManagementWindow()
        self.invoice_window.show()

    def show_company_management(self):
        if not self.company_window:
            self.company_window = CompanyManagementWindow()
        self.company_window.show()

    def show_cash_journal(self):
        if not self.cash_journal_window:
            self.cash_journal_window = CashJournalWindow()
        self.cash_journal_window.show()

    def show_trip_book(self):
        if not self.trip_book_window:
            self.trip_book_window = TripBookWindow()
        self.trip_book_window.show()
