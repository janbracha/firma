from PyQt6.QtWidgets import (
    QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QHBoxLayout,
    QMenuBar, QMenu, QMessageBox, QGroupBox, QGridLayout, QFrame, QScrollArea
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QAction, QFont, QIcon
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
from asset_management import AssetManagementWindow
from analytics_reports import AnalyticsReportsWindow
from calendar_schedule import CalendarScheduleWindow
from warehouse_management import WarehouseManagementWindow
from employee_management import EmployeeManagementWindow
from service_maintenance import ServiceMaintenanceWindow

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
        """Inicializuje moderní uživatelské rozhraní"""
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
        
        # Dashboard sekcе
        self.create_dashboard(layout)
        
        # Aplikace stylů
        self.apply_modern_styles()
    
    def create_header(self, layout):
        """Vytvoří moderní hlavičku"""
        header_frame = QFrame()
        header_frame.setObjectName("headerFrame")
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(20, 20, 20, 20)
        
        # Levá část - welcome
        left_layout = QVBoxLayout()
        
        title_label = QLabel("Správa firmy")
        title_label.setObjectName("titleLabel")
        left_layout.addWidget(title_label)
        
        subtitle_label = QLabel("Projekt & Develop s.r.o.")
        subtitle_label.setObjectName("subtitleLabel")
        left_layout.addWidget(subtitle_label)
        
        user_label = QLabel(f"Přihlášen jako: {self.current_user['full_name']} ({self.current_user['role']})")
        user_label.setObjectName("userLabel")
        left_layout.addWidget(user_label)
        
        header_layout.addLayout(left_layout)
        header_layout.addStretch()
        
        # Pravá část - logout
        logout_button = QPushButton("Odhlásit se")
        logout_button.setObjectName("logoutButton")
        logout_button.clicked.connect(self.logout)
        logout_button.setFixedSize(120, 40)
        header_layout.addWidget(logout_button)
        
        layout.addWidget(header_frame)
    
    def create_dashboard(self, layout):
        """Vytvoří dashboard s kartami"""
        
        # Základní funkce
        if self.has_basic_permissions():
            basic_frame = self.create_section_frame("💼 Základní funkce", "Správa běžných úkolů")
            basic_grid = QGridLayout()
            basic_grid.setSpacing(15)
            
            row, col = 0, 0
            
            if UserManager.has_permission(self.current_user['role'], 'invoices'):
                card = self.create_function_card("📊 Správa faktur", 
                                                "Vystavování a správa faktur", 
                                                self.show_invoice_management)
                basic_grid.addWidget(card, row, col)
                col += 1
                
            if UserManager.has_permission(self.current_user['role'], 'companies'):
                if col >= 2:  # Nový řádek po 2 kartách
                    row += 1
                    col = 0
                card = self.create_function_card("🏢 Správa firem", 
                                                "Správa firemních kontaktů", 
                                                self.show_company_management)
                basic_grid.addWidget(card, row, col)
                col += 1
                
            if UserManager.has_permission(self.current_user['role'], 'cash_journal'):
                if col >= 2:
                    row += 1
                    col = 0
                card = self.create_function_card("💰 Pokladní deník", 
                                                "Evidence příjmů a výdajů", 
                                                self.show_cash_journal)
                basic_grid.addWidget(card, row, col)
                col += 1
                
            if UserManager.has_permission(self.current_user['role'], 'trip_book'):
                if col >= 2:
                    row += 1
                    col = 0
                card = self.create_function_card("🚛 Kniha jízd", 
                                                "Evidence cest a dopravy", 
                                                self.show_trip_book)
                basic_grid.addWidget(card, row, col)
                col += 1
            
            # Správa dokumentů - dostupná pro všechny uživatele
            if col >= 2:
                row += 1
                col = 0
            card = self.create_function_card("📎 Správa dokumentů", 
                                            "Správa příloh a souborů", 
                                            self.show_document_management)
            basic_grid.addWidget(card, row, col)
            col += 1
            
            # Správa hmotného majetku - dostupná pro všechny uživatele
            if col >= 2:
                row += 1
                col = 0
            card = self.create_function_card("🏢 Správa hmotného majetku", 
                                            "Evidence dlouhodobého majetku", 
                                            self.show_asset_management)
            basic_grid.addWidget(card, row, col)
            col += 1
            
            # Analýzy a reporty - dostupné pro všechny uživatele
            if col >= 2:
                row += 1
                col = 0
            card = self.create_function_card("📈 Analýzy a reporty", 
                                            "Finanční analýzy a statistiky", 
                                            self.show_analytics_reports)
            basic_grid.addWidget(card, row, col)
            col += 1
            
            # Kalendář a termíny - dostupný pro všechny uživatele
            if col >= 2:
                row += 1
                col = 0
            card = self.create_function_card("📅 Kalendář a termíny", 
                                            "Plánování událostí a připomínek", 
                                            self.show_calendar_schedule)
            basic_grid.addWidget(card, row, col)
            col += 1
            
            # Skladové hospodářství - dostupné pro všechny uživatele
            if col >= 2:
                row += 1
                col = 0
            card = self.create_function_card("📋 Skladové hospodářství", 
                                            "Správa materiálu a zboží", 
                                            self.show_warehouse_management)
            basic_grid.addWidget(card, row, col)
            col += 1
            
            # Správa zaměstnanců - dostupná pro všechny uživatele
            if col >= 2:
                row += 1
                col = 0
            card = self.create_function_card("👥 Správa zaměstnanců", 
                                            "Evidence zaměstnanců a mezd", 
                                            self.show_employee_management)
            basic_grid.addWidget(card, row, col)
            col += 1
            
            # Servis a údržba - dostupný pro všechny uživatele
            if col >= 2:
                row += 1
                col = 0
            card = self.create_function_card("🔧 Servis a údržba", 
                                            "Plánování a evidence servisu", 
                                            self.show_service_maintenance)
            basic_grid.addWidget(card, row, col)
            
            basic_frame.layout().addLayout(basic_grid)
            layout.addWidget(basic_frame)
        
        # Systémové funkce (pouze pro admin)
        if UserManager.has_permission(self.current_user['role'], 'all'):
            admin_frame = self.create_section_frame("⚙️ Systémové funkce", "Správa systému a uživatelů")
            admin_grid = QGridLayout()
            admin_grid.setSpacing(15)
            
            cards = [
                ("👤 Správa uživatelů", "Správa uživatelských účtů", self.show_user_management),
                ("🔐 Správa rolí", "Nastavení oprávnění", self.show_role_management),
                ("🏭 Nastavení firmy", "Konfigurace společnosti", self.show_company_settings),
            ]
            
            for i, (title, desc, func) in enumerate(cards):
                card = self.create_function_card(title, desc, func)
                admin_grid.addWidget(card, i // 2, i % 2)
            
            admin_frame.layout().addLayout(admin_grid)
            layout.addWidget(admin_frame)
    
    def has_basic_permissions(self):
        """Kontroluje, zda má uživatel nějaká základní oprávnění"""
        permissions = ['invoices', 'companies', 'cash_journal', 'trip_book']
        return any(UserManager.has_permission(self.current_user['role'], perm) for perm in permissions)
    
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
    
    def create_function_card(self, title, description, callback):
        """Vytvoří kartu pro funkci"""
        card = QFrame()
        card.setObjectName("functionCard")
        card.setFixedSize(280, 120)
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
                font-size: 28px;
                font-weight: bold;
                color: #2c3e50;
                margin: 0;
            }
            
            #subtitleLabel {
                font-size: 16px;
                color: #7f8c8d;
                margin: 0;
            }
            
            #userLabel {
                font-size: 14px;
                color: #34495e;
                margin-top: 5px;
            }
            
            #logoutButton {
                background: linear-gradient(135deg, #e74c3c, #c0392b);
                color: white;
                border: none;
                border-radius: 20px;
                font-weight: bold;
                font-size: 14px;
            }
            
            #logoutButton:hover {
                background: linear-gradient(135deg, #c0392b, #a93226);
                transform: translateY(-1px);
            }
            
            /* Sekce */
            #sectionFrame {
                background: rgba(255, 255, 255, 0.95);
                border-radius: 15px;
                border: 1px solid rgba(255, 255, 255, 0.3);
                margin-bottom: 20px;
            }
            
            #sectionTitle {
                font-size: 20px;
                font-weight: bold;
                color: #2c3e50;
                margin-bottom: 5px;
            }
            
            #sectionSubtitle {
                font-size: 14px;
                color: #7f8c8d;
                margin-bottom: 15px;
            }
            
            /* Karty funkcí */
            #functionCard {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(255, 255, 255, 0.9),
                    stop:1 rgba(247, 249, 252, 0.9));
                border: 2px solid rgba(108, 133, 163, 0.1);
                border-radius: 12px;
                margin: 5px;
            }
            
            #functionCard:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(255, 255, 255, 1.0),
                    stop:1 rgba(240, 248, 255, 1.0));
                border: 2px solid rgba(108, 133, 163, 0.3);
                transform: translateY(-2px);
            }
            
            #cardTitle {
                font-size: 16px;
                font-weight: bold;
                color: #2c3e50;
                margin-bottom: 5px;
            }
            
            #cardDescription {
                font-size: 13px;
                color: #7f8c8d;
                line-height: 1.4;
            }
            
            /* Menu bar */
            QMenuBar {
                background: rgba(44, 62, 80, 0.95);
                color: white;
                border: none;
                padding: 5px;
            }
            
            QMenuBar::item {
                background: transparent;
                padding: 8px 16px;
                border-radius: 6px;
                margin: 2px;
            }
            
            QMenuBar::item:selected {
                background: rgba(52, 152, 219, 0.8);
            }
            
            QMenu {
                background: rgba(255, 255, 255, 0.98);
                border: 1px solid rgba(149, 165, 166, 0.3);
                border-radius: 8px;
                padding: 5px;
            }
            
            QMenu::item {
                padding: 8px 20px;
                border-radius: 4px;
                color: #2c3e50;
            }
            
            QMenu::item:selected {
                background: rgba(52, 152, 219, 0.1);
                color: #2980b9;
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

    def show_asset_management(self):
        """Zobrazí správu hmotného majetku"""
        self.asset_management_window = AssetManagementWindow()
        self.asset_management_window.show()

    def show_analytics_reports(self):
        """Zobrazí analýzy a reporty"""
        self.analytics_reports_window = AnalyticsReportsWindow()
        self.analytics_reports_window.show()

    def show_calendar_schedule(self):
        """Zobrazí kalendář a termíny"""
        self.calendar_schedule_window = CalendarScheduleWindow()
        self.calendar_schedule_window.show()

    def show_warehouse_management(self):
        """Zobrazí skladové hospodářství"""
        self.warehouse_management_window = WarehouseManagementWindow()
        self.warehouse_management_window.show()

    def show_employee_management(self):
        """Zobrazí správu zaměstnanců"""
        self.employee_management_window = EmployeeManagementWindow()
        self.employee_management_window.show()

    def show_service_maintenance(self):
        """Zobrazí servis a údržbu"""
        self.service_maintenance_window = ServiceMaintenanceWindow()
        self.service_maintenance_window.show()
