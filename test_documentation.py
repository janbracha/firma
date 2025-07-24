#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test skript pro ověření funkcionality dokumentačního okna
"""

import sys
from PyQt6.QtWidgets import QApplication
from documentation_window import DocumentationWindow

def test_documentation_window():
    """Testuje dokumentační okno"""
    app = QApplication(sys.argv)
    
    # Vytvoří a zobrazí dokumentační okno
    doc_window = DocumentationWindow()
    doc_window.show()
    
    print("✅ Dokumentační okno bylo úspěšně vytvořeno a zobrazeno!")
    print("📚 Taby v okně:")
    
    # Vypíše názvy všech tabů
    for i in range(doc_window.tab_widget.count()):
        tab_text = doc_window.tab_widget.tabText(i)
        print(f"   {i+1}. {tab_text}")
    
    print("\n🎯 Test dokončen - okno můžete zavřít!")
    
    # Spustí aplikaci
    sys.exit(app.exec())

if __name__ == "__main__":
    test_documentation_window()
