#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PyQt6.QtWidgets import QApplication
from database import create_tables
from gui import InvoiceApp

def test_main_application():
    """Test hlavní aplikace"""
    print("=== Test hlavní aplikace ===")
    
    # Vytvoření tabulek v databázi (jako v main.py)
    create_tables()
    print("Databázové tabulky vytvořeny/zkontrolovány")
    
    # Spuštění aplikace
    app = QApplication(sys.argv)
    window = InvoiceApp()
    window.show()
    
    print("Aplikace spuštěna")
    print("Navigujte do 'Výpočet knihy jízd' pro test generování")
    print("Očekávané výsledky v knihě jízd:")
    print("✅ Všech 16 řádků vyplněných")
    print("✅ Řidiči z databáze: Jan Bracha, Vera Brachova")
    print("✅ Destinace z databáze: Praha, Brno, Budějovice, atd.")
    print("✅ Každá destinace použita tam i zpět")
    
    return app.exec()

if __name__ == "__main__":
    test_main_application()
