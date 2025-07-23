#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton
from PyQt6.QtCore import Qt

def test_gui_table_filling():
    """Test konkrétního problému s naplňováním tabulky v GUI"""
    
    app = QApplication(sys.argv)
    
    # Vytvoření okna
    window = QMainWindow()
    window.setWindowTitle("Debug test naplňování tabulky")
    window.setGeometry(200, 200, 1000, 600)
    
    central_widget = QWidget()
    window.setCentralWidget(central_widget)
    layout = QVBoxLayout()
    central_widget.setLayout(layout)
    
    # Testovací data - přesně taková jaká generuje aplikace
    test_trips = []
    for i in range(16):
        test_trips.append({
            "datum": f"{15+i}.07.2025",
            "řidič": f"Řidič {i+1}",
            "start": f"Start {i+1}",
            "cíl": f"Cíl {i+1}",
            "firma": f"Firma {i+1}",
            "vzdálenost": 100 + i*10
        })
    
    print(f"Generováno {len(test_trips)} testovacích záznamů")
    
    # Vytvoření tabulky STEJNĚ jako v aplikaci
    table = QTableWidget()
    table.setColumnCount(6)
    table.setHorizontalHeaderLabels(["Datum", "Řidič", "Start", "Cíl", "Firma", "Vzdálenost (km)"])
    
    # NEJPRVE nastavíme počet řádků
    table.setRowCount(len(test_trips))
    print(f"Nastaveno {len(test_trips)} řádků v tabulce")
    
    # POVOLÍME řazení PŘED naplněním (stejně jako v aplikaci)
    table.setSortingEnabled(True)
    print("Řazení povoleno")
    
    # Naplnění tabulky
    actual_row = 0
    for i, trip in enumerate(test_trips):
        print(f"Zpracovávám záznam {i+1}: {trip}")
        
        # Kontrola základních údajů (stejná jako v aplikaci)
        if not trip.get("datum") or not trip.get("řidič") or not trip.get("start") or not trip.get("cíl"):
            print(f"  -> Přeskakuji prázdný záznam")
            continue

        print(f"  -> Vkládám do řádku {actual_row}")
        table.setItem(actual_row, 0, QTableWidgetItem(str(trip["datum"])))
        table.setItem(actual_row, 1, QTableWidgetItem(str(trip["řidič"])))
        table.setItem(actual_row, 2, QTableWidgetItem(str(trip["start"])))
        table.setItem(actual_row, 3, QTableWidgetItem(str(trip["cíl"])))
        table.setItem(actual_row, 4, QTableWidgetItem(str(trip["firma"] or "")))
        table.setItem(actual_row, 5, QTableWidgetItem(str(trip["vzdálenost"])))
        actual_row += 1

    print(f"Vloženo {actual_row} řádků")
    
    # SEŘADÍME podle data (stejně jako v aplikaci)
    table.sortItems(0, Qt.SortOrder.AscendingOrder)
    print("Tabulka seřazena podle data")
    
    # UPRAVÍME počet řádků na skutečný počet
    table.setRowCount(actual_row)
    print(f"Upraveno na {actual_row} řádků")
    
    layout.addWidget(table)
    
    # Tlačítko pro kontrolu obsahu tabulky
    def check_table_content():
        print("\n=== KONTROLA OBSAHU TABULKY ===")
        print(f"Počet řádků v tabulce: {table.rowCount()}")
        print(f"Počet sloupců v tabulce: {table.columnCount()}")
        
        empty_rows = 0
        for row in range(table.rowCount()):
            print(f"\nŘádek {row}:")
            row_empty = True
            for col in range(table.columnCount()):
                item = table.item(row, col)
                if item and item.text():
                    print(f"  Sloupec {col}: '{item.text()}'")
                    row_empty = False
                else:
                    print(f"  Sloupec {col}: PRÁZDNÝ")
            
            if row_empty:
                empty_rows += 1
                print(f"  -> CELÝ ŘÁDEK JE PRÁZDNÝ!")
        
        print(f"\nCelkem prázdných řádků: {empty_rows}")
        print("==============================\n")
    
    check_button = QPushButton("Zkontroluj obsah tabulky")
    check_button.clicked.connect(check_table_content)
    layout.addWidget(check_button)
    
    # Okamžitá kontrola po naplnění
    check_table_content()
    
    window.show()
    return app.exec()

if __name__ == "__main__":
    test_gui_table_filling()
