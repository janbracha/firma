#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem

def test_table_display():
    """Test zobrazení tabulky s testovacími daty"""
    
    # Testovací data podobná reálným datům
    test_trips = [
        {"datum": "18.07.2025", "řidič": "Jan Bracha", "start": "Nedabyle", "cíl": "Praha", "firma": "Alza", "vzdálenost": 150},
        {"datum": "18.07.2025", "řidič": "Vera Brachova", "start": "Praha", "cíl": "Nedabyle", "firma": "Alza", "vzdálenost": 150},
        {"datum": "20.07.2025", "řidič": "Jan Bracha", "start": "Nedabyle", "cíl": "Brno", "firma": "Packeta", "vzdálenost": 200},
        {"datum": "20.07.2025", "řidič": "Jan Bracha", "start": "Brno", "cíl": "Nedabyle", "firma": "Packeta", "vzdálenost": 200},
    ]
    
    app = QApplication(sys.argv)
    
    # Vytvoření okna
    window = QMainWindow()
    window.setWindowTitle("Test zobrazení tabulky")
    window.setGeometry(200, 200, 800, 400)
    
    central_widget = QWidget()
    window.setCentralWidget(central_widget)
    layout = QVBoxLayout()
    central_widget.setLayout(layout)
    
    # Vytvoření tabulky
    table = QTableWidget()
    table.setColumnCount(6)
    table.setHorizontalHeaderLabels(["Datum", "Řidič", "Start", "Cíl", "Firma", "Vzdálenost (km)"])
    
    # NEJPRVE nastavíme počet řádků
    table.setRowCount(len(test_trips))
    print(f"Nastaveno {len(test_trips)} řádků v tabulce")
    
    # Naplnění tabulky stejnou logikou jako v aplikaci
    actual_row = 0
    for trip in test_trips:
        # Kontrola základních údajů (stejná jako v aplikaci)
        if not trip.get("datum") or not trip.get("řidič") or not trip.get("start") or not trip.get("cíl"):
            print(f"Přeskakuji prázdný záznam: {trip}")
            continue

        print(f"Vkládám řádek {actual_row}: {trip['datum']} - {trip['řidič']}")
        table.setItem(actual_row, 0, QTableWidgetItem(str(trip["datum"])))
        table.setItem(actual_row, 1, QTableWidgetItem(str(trip["řidič"])))
        table.setItem(actual_row, 2, QTableWidgetItem(str(trip["start"])))
        table.setItem(actual_row, 3, QTableWidgetItem(str(trip["cíl"])))
        table.setItem(actual_row, 4, QTableWidgetItem(str(trip["firma"] or "")))
        table.setItem(actual_row, 5, QTableWidgetItem(str(trip["vzdálenost"])))
        actual_row += 1

    # Upravení počtu řádků tabulky na skutečný počet záznamů
    table.setRowCount(actual_row)
    print(f"Finální počet řádků: {actual_row}")
    
    layout.addWidget(table)
    
    print(f"Zobrazeno {actual_row} řádků z {len(test_trips)} testovacích záznamů")
    
    window.show()
    return app.exec()

if __name__ == "__main__":
    test_table_display()
