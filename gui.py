from PyQt6.QtWidgets import (
    QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
)
from database import create_tables
from invoice_management import InvoiceManagementWindow
from company_managment import CompanyManagementWindow
from cash_journal import CashJournalWindow
from trip_book import TripBookWindow  # Nový import pro Knihu jízd

class InvoiceApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.invoice_window = InvoiceManagementWindow()
        self.company_window = CompanyManagementWindow()
        self.cash_journal_window = CashJournalWindow()
        self.trip_book_window = TripBookWindow()  # Přidáno nové okno pro Knihu jízd
        self.setWindowTitle("Správa faktur")
        self.setGeometry(200, 200, 800, 600)

        create_tables()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        welcome_label = QLabel("<h2>Vítejte ve správě firmy Projekt & Develop s.r.o.</h2>")
        layout.addWidget(welcome_label)

        # Tlačítka pro jednotlivé sekce
        self.manage_invoices_button = QPushButton("Správa faktur")
        self.manage_invoices_button.clicked.connect(self.show_invoice_management)
        layout.addWidget(self.manage_invoices_button)

        self.manage_companies_button = QPushButton("Správa firem")
        self.manage_companies_button.clicked.connect(self.show_company_management)
        layout.addWidget(self.manage_companies_button)

        self.manage_cash_journal_button = QPushButton("Pokladní deník")
        self.manage_cash_journal_button.clicked.connect(self.show_cash_journal)
        layout.addWidget(self.manage_cash_journal_button)

        self.manage_trip_book_button = QPushButton("Kniha jízd")  # Přidáno nové tlačítko
        self.manage_trip_book_button.clicked.connect(self.show_trip_book)
        layout.addWidget(self.manage_trip_book_button)

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
        """)

    def show_invoice_management(self):
        self.invoice_window.show()

    def show_company_management(self):
        self.company_window.show()

    def show_cash_journal(self):
        self.cash_journal_window.show()

    def show_trip_book(self):  # Funkce pro otevření okna Kniha jízd
        self.trip_book_window.show()
