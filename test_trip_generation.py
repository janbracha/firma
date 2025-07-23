#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PyQt6.QtWidgets import QApplication
from trip_calculation import TripCalculationWindow

# Test script pro novou logiku generování knihy jízd
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Vytvoření okna pro výpočet knihy jízd
    trip_window = TripCalculationWindow()
    trip_window.show()
    
    print("Test aplikace spuštěn - otevřeno okno 'Výpočet knihy jízd'")
    print("Zkontrolujte:")
    print("1. Zda se načítají řidiči a destinace z databáze")
    print("2. Zda každá destinace je použita 2x (tam a zpět)")
    print("3. Zda celkové km odpovídají předpokládaným km")
    
    sys.exit(app.exec())
