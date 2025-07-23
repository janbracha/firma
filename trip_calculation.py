from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QFormLayout, QLabel, QComboBox, QMessageBox, QTableWidget, QTableWidgetItem
from PyQt6.QtCore import QDate
from database import connect
import random
from fuel_management import FuelManagementWindow  # Import správy tankování
from PyQt6.QtCore import Qt



class TripCalculationWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Výpočet Knihy jízd")
        self.setGeometry(200, 200, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        # Formulář pro zadání vstupních údajů
        form_layout = QFormLayout()


        # Výběr měsíce
        self.month_box = QComboBox()
        self.month_box.addItems(["Leden", "Únor", "Březen", "Duben", "Květen", "Červen",
                                 "Červenec", "Srpen", "Září", "Říjen", "Listopad", "Prosinec"])
        form_layout.addRow(QLabel("Měsíc:"), self.month_box)
        self.month_box.currentIndexChanged.connect(self.update_fuel_display)

        # Výběr roku
        self.year_box = QComboBox()
        current_year = QDate.currentDate().year()
        self.year_box.addItems([str(y) for y in range(current_year, current_year - 10, -1)])
        form_layout.addRow(QLabel("Rok:"), self.year_box)

        # Množství paliva za měsíc
        self.monthly_fuel_label = QLabel("Množství paliva za zvolený měsíc: N/A")
        form_layout.addRow(QLabel("Množství paliva za zvolený měsíc:"), self.monthly_fuel_label)

        # Výběr vozidla
        self.vehicle_box = QComboBox()
        self.load_vehicles()
        form_layout.addRow(QLabel("Vozidlo:"), self.vehicle_box)

        layout.addLayout(form_layout)

        # Tlačítka
        self.generate_button = QPushButton("Generovat Knihu jízd")
        self.generate_button.clicked.connect(self.generate_trip_book)
        layout.addWidget(self.generate_button)

        self.manage_fuel_button = QPushButton("Správa tankování")
        self.manage_fuel_button.clicked.connect(self.show_fuel_management)
        layout.addWidget(self.manage_fuel_button)

        central_widget.setLayout(layout)

    def load_vehicles(self):
        """Načte seznam vozidel z databáze."""
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT registration FROM cars")
        vehicles = cursor.fetchall()
        conn.close()

        self.vehicle_box.addItems([vehicle[0] for vehicle in vehicles])

    def generate_trip_book(self):
        """Vygeneruje Knihu jízd na základě paliva v databázi."""
        self.trip_table = QTableWidget()  # Inicializace tabulky
        self.trip_table.setColumnCount(6)
        self.trip_table.setHorizontalHeaderLabels(["Datum", "Řidič", "Start", "Cíl", "Firma", "Vzdálenost (km)"])

        month_name = self.month_box.currentText()
        self.month_box.currentIndexChanged.connect(self.update_fuel_display)

        year = int(self.year_box.currentText())
        selected_vehicle = self.vehicle_box.currentText()

        # Převod měsíce na číslo
        months = ["Leden", "Únor", "Březen", "Duben", "Květen", "Červen",
                  "Červenec", "Srpen", "Září", "Říjen", "Listopad", "Prosinec"]
        month = months.index(month_name) + 1

        # Sečtení tankování pro dané vozidlo a měsíc
        conn = connect()
        cursor = conn.cursor()


        cursor.execute("""
            SELECT SUM(fuel_amount) FROM fuel_tankings
            WHERE vehicle=? AND substr(date, 4, 2)=? AND substr(date, 7, 4)=?
        """, (selected_vehicle, f"{month:02}", str(year)))

        fuel_quantity = cursor.fetchone()[0] or 0  # Pokud není tankování, nastavíme 0
        conn.close()

        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT consumption FROM cars WHERE registration=?", (selected_vehicle,))
        consumption = cursor.fetchone()[0]
        conn.close()

        # Výpočet celkového počtu km
        total_km = (fuel_quantity / consumption) * 100 if consumption else 0
        print(f"Výpočet km: {fuel_quantity} litrů / {consumption} * 100 = {total_km} km")


        # Načtení destinací a řidičů
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT start, destination, company, distance FROM destinations")
        destinations = cursor.fetchall()

        cursor.execute("SELECT first_name, last_name FROM drivers")
        drivers = cursor.fetchall()
        conn.close()

        trips = []
        remaining_km = total_km
        days_used = set()
        days_in_month = QDate(year, month, 1).daysInMonth()

        # Generování jízd rovnoměrně do měsíce
        while remaining_km > 0 and len(days_used) < days_in_month:
            destination = random.choice(destinations)
            driver = random.choice(drivers)
            trip_distance = destination[3]  # Vzdálenost jedné cesty
            round_trip_distance = trip_distance * 2  # Celková vzdálenost tam i zpět
            print(f"Zbývající km před jízdou: {remaining_km}")


            if remaining_km - round_trip_distance < 0:
                print(f"Po jízdě: zbývá {remaining_km} km, aktuální vzdálenost jízdy {round_trip_distance} km")

                break

            # Výběr volného dne (rovnoměrné rozložení jízd)
            available_days = set(range(1, days_in_month + 1)) - days_used
            if not available_days:
                break
            trip_day = random.choice(list(available_days))
            days_used.add(trip_day)
            trip_date = QDate(year, month, trip_day).toString("dd.MM.yyyy")

            trips.append({
                "datum": trip_date,
                "řidič": f"{driver[0]} {driver[1]}",
                "start": destination[0],
                "cíl": destination[1],
                "firma": destination[2],
                "vzdálenost": trip_distance,
                "vozidlo": selected_vehicle,
                "měsíc": month_name,
                "rok": str(year)
            })

            trips.append({
                "datum": trip_date,
                "řidič": f"{driver[0]} {driver[1]}",
                "start": destination[1],  # Zpáteční cesta
                "cíl": destination[0],
                "firma": destination[2],
                "vzdálenost": trip_distance,
                "vozidlo": selected_vehicle,
                "měsíc": month_name,
                "rok": str(year)
            })

            remaining_km -= round_trip_distance

        # Výpis výsledků s datem
        trip_summary = "\n".join([f"{trip['datum']} | {trip['řidič']} ({trip['vozidlo']}): {trip['start']} → {trip['cíl']} ({trip['vzdálenost']} km, Firma: {trip['firma']})" for trip in trips])

        # Vytvoření tabulky

        self.trip_table.setRowCount(len(trips))

        print(f"Celkový počet vygenerovaných jízd: {len(trips)}")

        self.trip_table.setHorizontalHeaderLabels(["Datum", "Řidič", "Start", "Cíl", "Firma", "Vzdálenost (km)"])
        self.trip_table.setSortingEnabled(True)  # Povolení řazení sloupců
    
  
        self.trip_table.sortItems(0, Qt.SortOrder(0))  # 0 znamená vzestupné řazení (Ascending)
        self.trip_table.resizeRowsToContents()  # Automatické přizpůsobení řádků
        self.trip_table.repaint()  # Vynutíme překreslení tabulky
        self.trip_table.update()  # Vynutíme aktualizaci tabulky
        self.trip_table.repaint()  # Překreslíme obsah tabulky





        # Naplnění tabulky daty
      

        for row_idx, trip in enumerate(trips):
            print(f"Přidávám do tabulky: řádek {row_idx}, datum: {trip['datum']}, vzdálenost: {trip['vzdálenost']}")

            if not all(trip.values()):  # Pokud nějaká hodnota chybí, neukládat do tabulky
                print(f"Varování: Chybějící data v záznamu {trip}")
                
                continue


            self.trip_table.setItem(row_idx, 0, QTableWidgetItem(trip["datum"]))
            for row in range(self.trip_table.rowCount()):
                for col in range(self.trip_table.columnCount()):
                    item = self.trip_table.item(row, col)
                    print(f"Řádek {row}, Sloupec {col}: {item.text() if item else '⚠️ NIC'}")




            self.trip_table.setItem(row_idx, 1, QTableWidgetItem(trip["řidič"]))
            self.trip_table.setItem(row_idx, 2, QTableWidgetItem(trip["start"]))
            self.trip_table.setItem(row_idx, 3, QTableWidgetItem(trip["cíl"]))
            self.trip_table.setItem(row_idx, 4, QTableWidgetItem(trip["firma"]))
            self.trip_table.setItem(row_idx, 5, QTableWidgetItem(str(trip["vzdálenost"])))
            self.trip_table.resizeRowsToContents()  # Automatické přizpůsobení řádků
            self.trip_table.repaint()  # Vynutíme překreslení tabulky


        # Zobrazení tabulky v okně
        self.trip_window = QWidget()
        self.trip_window.setWindowTitle("Vygenerovaná Kniha jízd")
        layout = QVBoxLayout()
        self.trip_table = QTableWidget()  # Správná inicializace
        self.trip_table.setColumnCount(6)
        self.trip_table.setHorizontalHeaderLabels(["Datum", "Řidič", "Start", "Cíl", "Firma", "Vzdálenost (km)"])
        layout.addWidget(self.trip_table)  # Přidání tabulky do okna
        self.trip_window.setLayout(layout)
        self.trip_window.show()

        self.trip_window.setLayout(layout)
        self.trip_window.show()

    def show_fuel_management(self):
        """Otevře okno pro správu tankování."""
        self.fuel_management_window = FuelManagementWindow()
        self.fuel_management_window.show()

    def update_fuel_display(self):
        print("update_fuel_display() byla zavolána!")

        """Načte množství paliva ihned po změně měsíce."""
        month_name = self.month_box.currentText()
        year = int(self.year_box.currentText())
        selected_vehicle = self.vehicle_box.currentText()

        # Převod měsíce na číslo
        months = ["Leden", "Únor", "Březen", "Duben", "Květen", "Červen",
                "Červenec", "Srpen", "Září", "Říjen", "Listopad", "Prosinec"]
        month = months.index(month_name) + 1

        # Debug výpis, abychom viděli, co se děje:
        print(f"Načítám palivo pro vozidlo: {selected_vehicle}, měsíc: {month}, rok: {year}")

        # Sečtení tankování z databáze
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT SUM(fuel_amount) FROM fuel_tankings
            WHERE vehicle=? AND substr(date, 4, 2)=? AND substr(date, 7, 4)=?
        """, (selected_vehicle, f"{month:02}", str(year)))
        fuel_quantity = cursor.fetchone()[0] or 0
        conn.close()

        print(f"Výsledek SQL dotazu: {fuel_quantity} litrů")  # Debug výpis

        # Zobrazení množství paliva na stránce
        print(f"Aktualizuji GUI: {fuel_quantity} litrů")

        self.monthly_fuel_label.setText(f"Množství paliva za zvolený měsíc: {fuel_quantity} litrů")
        self.monthly_fuel_label.repaint()  # Vynutíme okamžité překreslení
        print(f"Text štítku po změně: {self.monthly_fuel_label.text()}")


