from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton
from driver_management import DriverManagementWindow  # Import nové stránky
from vehicle_management import VehicleManagementWindow  # Import správce vozidel
from destination_management import DestinationManagementWindow  # Import správce destinací
from trip_calculation import TripCalculationWindow  # Import nové stránky


class TripBookWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kniha jízd")
        self.setGeometry(200, 200, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        # Použití stejného stylu jako v hlavní aplikaci
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
            }

            QPushButton:hover {
                background-color: #5A7393;
            }
        """)

        # Prostor nahoře, aby tlačítka byla dole
        layout.addStretch()

        self.manage_drivers_button = QPushButton("Správa řidičů")
        self.manage_drivers_button.clicked.connect(self.show_driver_management)
        layout.addWidget(self.manage_drivers_button)

        self.manage_vehicles_button = QPushButton("Správa vozidel")
        self.manage_vehicles_button.clicked.connect(self.show_vehicle_management)
        layout.addWidget(self.manage_vehicles_button)


        self.enter_destinations_button = QPushButton("Zadávání destinací")
        self.enter_destinations_button.clicked.connect(self.show_destination_management)
        layout.addWidget(self.enter_destinations_button)

        self.trip_calculation_button = QPushButton("Výpočet knihy jízd")
        self.trip_calculation_button.clicked.connect(self.show_trip_calculation)
        layout.addWidget(self.trip_calculation_button)


        central_widget.setLayout(layout)

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

    def show_trip_calculation(self):
        """Otevře okno pro výpočet knihy jízd."""
        self.trip_calculation_window = TripCalculationWindow()
        self.trip_calculation_window.show()