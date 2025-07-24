from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QFrame, QScrollArea, QGridLayout, QLabel
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from driver_management import DriverManagementWindow  # Import nové stránky
from vehicle_management import VehicleManagementWindow  # Import správce vozidel
from destination_management import DestinationManagementWindow  # Import správce destinací
from trip_calculation import TripCalculationWindow  # Import nové stránky
from fuel_management import FuelManagementWindow  # Import správy tankování


class TripBookWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kniha jízd - Projekt & Develop s.r.o.")
        self.setGeometry(200, 200, 1200, 800)

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
        
        title_label = QLabel("🚛 Kniha jízd")
        title_label.setObjectName("titleLabel")
        left_layout.addWidget(title_label)
        
        subtitle_label = QLabel("Správa dopravy, vozidel a evidencí cest")
        subtitle_label.setObjectName("subtitleLabel")
        left_layout.addWidget(subtitle_label)
        
        header_layout.addLayout(left_layout)
        header_layout.addStretch()
        
        layout.addWidget(header_frame)
    
    def create_content(self, layout):
        """Vytvoří hlavní obsah okna"""
        
        # Správa základních údajů
        basics_frame = self.create_section_frame("⚙️ Základní správa", "Správa řidičů, vozidel a destinací")
        basics_grid = QGridLayout()
        basics_grid.setSpacing(15)
        
        # Karty základních funkcí
        basic_actions = [
            ("👨‍💼 Správa řidičů", "Správa seznamu řidičů", self.show_driver_management),
            ("🚗 Správa vozidel", "Registrace a správa vozového parku", self.show_vehicle_management),
            ("📍 Správa destinací", "Zadávání a správa cílových míst", self.show_destination_management),
            ("⛽ Správa tankování", "Evidence a správa záznamů tankování", self.show_fuel_management),
        ]
        
        # Rozložení karet do řádků (2 karty na řádek)
        for i, (title, desc, func) in enumerate(basic_actions):
            card = self.create_action_card(title, desc, func)
            row = i // 2
            col = i % 2
            basics_grid.addWidget(card, row, col)
        
        basics_frame.layout().addLayout(basics_grid)
        layout.addWidget(basics_frame)
        
        # Výpočty a evidence
        calculations_frame = self.create_section_frame("📊 Výpočty a evidence", "Kalkulace a reporty knihy jízd")
        calculations_grid = QGridLayout()
        calculations_grid.setSpacing(15)
        
        # Karta pro výpočty
        calc_card = self.create_action_card(
            "📈 Výpočet knihy jízd", 
            "Kalkulace nákladů a sestavení knihy jízd", 
            self.show_trip_calculation
        )
        calculations_grid.addWidget(calc_card, 0, 0)
        
        calculations_frame.layout().addLayout(calculations_grid)
        layout.addWidget(calculations_frame)

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
        card.setFixedSize(320, 120)
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
        """)

    def show_driver_management(self):
        """Otevře okno pro správu řidičů."""
        self.driver_window = DriverManagementWindow()
        self.driver_window.show()

    def show_vehicle_management(self):
        """Otevře okno pro správu vozidel."""
        self.vehicle_window = VehicleManagementWindow()
        self.vehicle_window.show()

    def show_destination_management(self):
        """Otevře okno pro správu destinací."""
        self.destination_window = DestinationManagementWindow()
        self.destination_window.show()

    def show_fuel_management(self):
        """Otevře okno pro správu tankování."""
        self.fuel_window = FuelManagementWindow()
        self.fuel_window.show()

    def show_trip_calculation(self):
        """Otevře okno pro výpočet knihy jízd."""
        self.trip_calculation_window = TripCalculationWindow()
        self.trip_calculation_window.show()