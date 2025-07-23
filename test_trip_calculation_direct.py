#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PyQt6.QtWidgets import QApplication
from trip_calculation import TripCalculationWindow

def test_trip_calculation_directly():
    """Test přímého spuštění TripCalculationWindow"""
    print("=== Test TripCalculationWindow ===")
    
    app = QApplication(sys.argv)
    
    # Vytvoření okna pro výpočet knihy jízd
    trip_window = TripCalculationWindow()
    trip_window.show()
    
    print("Okno 'Výpočet knihy jízd' otevřeno")
    print("Klikněte na 'Generovat knihu jízd' pro test")
    print("Očekávané výsledky:")
    print("- 16 jízd pro 8 destinací (každá tam a zpět)")
    print("- Všechny řádky vyplněné")
    print("- Použití databázových řidičů a destinací")
    
    return app.exec()

if __name__ == "__main__":
    test_trip_calculation_directly()
