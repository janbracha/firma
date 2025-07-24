import sys
import os
from PyQt6.QtWidgets import QApplication, QMessageBox

def main():
    """Hlavní funkce aplikace s error handlingem"""
    
    # Základní informace o aplikaci
    APP_NAME = "Firemní aplikace - Projekt & Develop s.r.o."
    APP_VERSION = "1.0"
    
    try:
        # Import závislostí
        from database import create_tables
        from gui import InvoiceApp
        
        # Vytvoření databázových tabulek
        print(f"🚀 Spouštění {APP_NAME} v{APP_VERSION}")
        print("📊 Inicializace databáze...")
        create_tables()
        print("✅ Databáze připravena")
        
        # Vytvoření aplikace
        app = QApplication(sys.argv)
        app.setApplicationName(APP_NAME)
        app.setApplicationVersion(APP_VERSION)
        
        # Hlavní okno
        print("🖥️  Načítání GUI...")
        window = InvoiceApp()
        
        # Kontrola úspěšného přihlášení
        if hasattr(window, 'current_user') and window.current_user:
            print(f"👤 Přihlášen uživatel: {window.current_user.get('username', 'Neznámý')}")
            print("✅ Aplikace připravena k použití")
            window.show()
            sys.exit(app.exec())
        else:
            print("❌ Přihlášení bylo zrušeno")
            sys.exit(0)
            
    except ImportError as e:
        error_msg = f"Chybí závislosti: {str(e)}\n\nNainstalujte PyQt6: pip install PyQt6"
        print(f"❌ ImportError: {error_msg}")
        if 'QApplication' in locals():
            QMessageBox.critical(None, "Chyba závislostí", error_msg)
        sys.exit(1)
        
    except Exception as e:
        error_msg = f"Neočekávaná chyba při spouštění: {str(e)}"
        print(f"❌ Error: {error_msg}")
        if 'QApplication' in locals():
            QMessageBox.critical(None, "Chyba aplikace", error_msg)
        sys.exit(1)

if __name__ == "__main__":
    main()
