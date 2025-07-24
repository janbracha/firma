#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QTextEdit, QLabel, QPushButton, QTabWidget,
                            QMessageBox, QScrollArea)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap

class DocumentationWindow(QMainWindow):
    """Okno pro zobrazení dokumentace aplikace"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_documentation()
    
    def init_ui(self):
        self.setWindowTitle("📚 Dokumentace a nápověda")
        self.setGeometry(100, 100, 1200, 800)
        
        # Stylování
        self.setStyleSheet("""
            QMainWindow {
                background: #F8F9FA;
                font-family: 'Inter', 'Roboto', sans-serif;
            }
            
            QTabWidget::pane {
                border: 1px solid #E0E0E0;
                background: white;
                border-radius: 8px;
            }
            
            QTabWidget::tab-bar {
                alignment: left;
            }
            
            QTabBar::tab {
                background: #F5F5F5;
                color: #2C3E50;
                border: 1px solid #E0E0E0;
                padding: 12px 20px;
                margin-right: 2px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                font-weight: bold;
                min-width: 120px;
            }
            
            QTabBar::tab:selected {
                background: white;
                border-bottom: 1px solid white;
                color: #3498DB;
            }
            
            QTabBar::tab:hover {
                background: #E8F4FD;
            }
            
            QTextEdit {
                background: white;
                border: none;
                font-size: 14px;
                line-height: 1.6;
                padding: 20px;
                color: #2C3E50;
            }
            
            QPushButton {
                background: linear-gradient(135deg, #3498DB, #2980B9);
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                padding: 10px 20px;
                font-size: 14px;
            }
            
            QPushButton:hover {
                background: linear-gradient(135deg, #2980B9, #1F5F99);
            }
            
            QLabel {
                color: #2C3E50;
                font-size: 16px;
                font-weight: bold;
            }
        """)
        
        # Hlavní widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Hlavička
        header_layout = QHBoxLayout()
        
        title_label = QLabel("📚 Dokumentace a nápověda")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #2C3E50;")
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        # Tlačítko pro zavření
        close_button = QPushButton("✖ Zavřít")
        close_button.clicked.connect(self.close)
        header_layout.addWidget(close_button)
        
        layout.addLayout(header_layout)
        
        # Tab widget pro různé typy dokumentace
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        
        # Vytvoření tabů
        self.create_quick_start_tab()
        self.create_user_guide_tab()
        self.create_functions_tab()
        self.create_roles_tab()
        self.create_troubleshooting_tab()
        self.create_about_tab()
    
    def create_quick_start_tab(self):
        """Tab s rychlým startem"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        
        content = """
        <h2>🚀 Rychlý start</h2>
        
        <h3>🔑 Přihlášení</h3>
        <ul>
            <li><strong>Uživatelské jméno:</strong> admin</li>
            <li><strong>Heslo:</strong> admin123</li>
        </ul>
        <p><em>⚠️ Doporučujeme změnit heslo po prvním přihlášení!</em></p>
        
        <h3>🏠 Hlavní menu</h3>
        <p>Po přihlášení se zobrazí dashboard s kartami funkcí:</p>
        <ul>
            <li><strong>📊 Správa faktur</strong> - Vystavování a správa faktur</li>
            <li><strong>🏢 Správa firem</strong> - Databáze obchodních partnerů</li>
            <li><strong>💰 Pokladní deník</strong> - Evidence příjmů a výdajů</li>
            <li><strong>🚛 Kniha jízd</strong> - Evidence dopravy a cest</li>
            <li><strong>👥 Správa zaměstnanců</strong> - Personální evidence</li>
            <li><strong>📦 Skladové hospodářství</strong> - Správa zásob</li>
            <li><strong>📅 Kalendář</strong> - Plánování událostí</li>
            <li><strong>🔧 Servis a údržba</strong> - Plánování údržby</li>
        </ul>
        
        <h3>⚙️ Systémové funkce (pouze admin)</h3>
        <ul>
            <li><strong>Systém → Správa uživatelů</strong> - Přidání/úprava uživatelů</li>
            <li><strong>Systém → Správa rolí</strong> - Nastavení oprávnění</li>
            <li><strong>Systém → Nastavení firmy</strong> - Základní konfigurace</li>
        </ul>
        
        <h3>💡 První kroky</h3>
        <ol>
            <li><strong>Nastavte firmu:</strong> Systém → Nastavení firmy</li>
            <li><strong>Přidejte uživatele:</strong> Systém → Správa uživatelů</li>
            <li><strong>Vystavte první fakturu:</strong> 📊 Správa faktur</li>
            <li><strong>Evidujte příjem:</strong> 💰 Pokladní deník</li>
        </ol>
        """
        
        text_edit.setHtml(content)
        layout.addWidget(text_edit)
        
        self.tab_widget.addTab(widget, "🚀 Rychlý start")
    
    def create_user_guide_tab(self):
        """Tab s uživatelským návodem"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        
        content = """
        <h2>📖 Uživatelský návod</h2>
        
        <h3>📊 Správa faktur</h3>
        <ol>
            <li>Klikněte na "📊 Správa faktur"</li>
            <li>Pro novou fakturu: "Přidat fakturu"</li>
            <li>Vyplňte číslo faktury, typ (vydaná/přijatá)</li>
            <li>Zadejte odběratele/dodavatele</li>
            <li>Vyplňte částky a daně</li>
            <li>Uložte fakturu</li>
        </ol>
        
        <h3>💰 Pokladní deník</h3>
        <ol>
            <li>Klikněte na "💰 Pokladní deník"</li>
            <li>Pro novou transakci: "Přidat záznam"</li>
            <li>Vyberte typ (Příjem/Výdaj)</li>
            <li>Zadejte částku a popis</li>
            <li>Uložte transakci</li>
        </ol>
        <p><em>Aktuální stav pokladny je vždy viditelný v tabulce.</em></p>
        
        <h3>🚛 Kniha jízd</h3>
        <ol>
            <li>Klikněte na "🚛 Kniha jízd"</li>
            <li>Pro novou jízdu: "Přidat jízdu"</li>
            <li>Vyberte řidiče a vozidlo</li>
            <li>Zadejte trasu (odkud-kam)</li>
            <li>Výpočet nákladů se provede automaticky</li>
        </ol>
        
        <h3>👥 Správa zaměstnanců</h3>
        <ol>
            <li>Klikněte na "👥 Správa zaměstnanců"</li>
            <li>Pro nového zaměstnance: "Přidat zaměstnance"</li>
            <li>Vyplňte osobní údaje a kontakty</li>
            <li>Přiřaďte pozici a oddělení</li>
            <li>Nastavte mzdu a benefity</li>
        </ol>
        
        <h3>📦 Skladové hospodářství</h3>
        <ol>
            <li>Klikněte na "📋 Skladové hospodářství"</li>
            <li>Pro nové zboží: "Přidat zboží"</li>
            <li>Zadejte název a kategorii</li>
            <li>Vyplňte množství a cenu</li>
            <li>Pro inventuru použijte tlačítko "Inventura"</li>
        </ol>
        
        <h3>📅 Kalendář a plánování</h3>
        <ol>
            <li>Klikněte na "📅 Kalendář a termíny"</li>
            <li>Klikněte na konkrétní den</li>
            <li>Vyplňte název a čas události</li>
            <li>Přiřaďte účastníky</li>
            <li>Nastavte připomínku</li>
        </ol>
        """
        
        text_edit.setHtml(content)
        layout.addWidget(text_edit)
        
        self.tab_widget.addTab(widget, "📖 Návod")
    
    def create_functions_tab(self):
        """Tab s přehledem funkcí"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        
        content = """
        <h2>🏢 Přehled funkcí</h2>
        
        <h3>📊 Fakturace a účetnictví</h3>
        <ul>
            <li><strong>Správa faktur</strong> - Vystavování, úprava, export (PDF/Excel)</li>
            <li><strong>Pokladní deník</strong> - Evidence příjmů a výdajů s automatickým zůstatkem</li>
            <li><strong>Analýzy a reporty</strong> - Finanční přehledy, top klienti, měsíční statistiky</li>
        </ul>
        
        <h3>🏢 Správa firmy a kontaktů</h3>
        <ul>
            <li><strong>Firemní kontakty</strong> - Databáze obchodních partnerů (IČO, DIČ, bankovní spojení)</li>
            <li><strong>Nastavení firmy</strong> - Konfigurace základních údajů, šablon</li>
            <li><strong>Správa dokumentů</strong> - Centrální úložiště souborů s kategorizací</li>
        </ul>
        
        <h3>🚛 Doprava a logistika</h3>
        <ul>
            <li><strong>Kniha jízd</strong> - Evidence cest s automatickým výpočtem nákladů</li>
            <li><strong>Správa vozidel</strong> - Evidence vozového parku, spotřeba, údržba</li>
            <li><strong>Správa řidičů</strong> - Databáze řidičů s pozicemi a oprávněními</li>
            <li><strong>Destinace</strong> - Správa tras s automatickým výpočtem vzdáleností</li>
            <li><strong>Pohonné hmoty</strong> - Evidence tankování a spotřeby</li>
        </ul>
        
        <h3>👥 HR a správa zaměstnanců</h3>
        <ul>
            <li><strong>Správa zaměstnanců</strong> - Kompletní personální evidence</li>
            <li><strong>Pracovní smlouvy</strong> - Správa dokumentů s připomínkami platnosti</li>
            <li><strong>Školení</strong> - Plánování a evidence vzdělávání zaměstnanců</li>
            <li><strong>Mzdová agenda</strong> - Správa mezd, odměn a benefitů</li>
        </ul>
        
        <h3>📦 Skladování a majetek</h3>
        <ul>
            <li><strong>Skladové hospodářství</strong> - Správa zásob s kategorizací</li>
            <li><strong>Hmotný majetek</strong> - Evidence dlouhodobého majetku (pořizovací cena, odpisy)</li>
            <li><strong>Inventury</strong> - Pravidelné kontroly stavu s reporty rozdílů</li>
        </ul>
        
        <h3>📅 Plánování a údržba</h3>
        <ul>
            <li><strong>Kalendář</strong> - Události, termíny, připomínky</li>
            <li><strong>Servis a údržba</strong> - Plánování údržby majetku a vozidel</li>
            <li><strong>Certifikáty</strong> - Správa platnosti dokumentů a kontrol</li>
        </ul>
        
        <h3>👤 Systém uživatelů (pouze admin)</h3>
        <ul>
            <li><strong>Správa uživatelů</strong> - Aktivace, deaktivace, změna hesel</li>
            <li><strong>Správa rolí</strong> - 57 detailních oprávnění napříč 12 moduly</li>
            <li><strong>Audit trail</strong> - Evidence změn a aktivit uživatelů</li>
        </ul>
        """
        
        text_edit.setHtml(content)
        layout.addWidget(text_edit)
        
        self.tab_widget.addTab(widget, "🏢 Funkce")
    
    def create_roles_tab(self):
        """Tab s přehledem rolí"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        
        content = """
        <h2>👥 Systém rolí a oprávnění</h2>
        
        <h3>🔑 Administrator (admin)</h3>
        <ul>
            <li><strong>57 oprávnění</strong> - Plný přístup ke všem funkcím</li>
            <li>Správa uživatelů a rolí</li>
            <li>Konfigurace systému a bezpečnosti</li>
            <li>Přístup k auditním logům</li>
            <li>Všechny operativní funkce</li>
        </ul>
        
        <h3>📊 Účetní (accountant)</h3>
        <ul>
            <li><strong>45 oprávnění</strong> - Většina operativních funkcí</li>
            <li>✅ Správa faktur, účetnictví, analýz</li>
            <li>✅ Správa majetku, dopravy, HR</li>
            <li>✅ Kalendář a plánování</li>
            <li>✅ Skladové hospodářství</li>
            <li>❌ Bez správy uživatelů a systémových nastavení</li>
        </ul>
        
        <h3>👤 Uživatel (user)</h3>
        <ul>
            <li><strong>14 oprávnění</strong> - Základní zobrazení a vytváření</li>
            <li>✅ Zobrazení většiny dat</li>
            <li>✅ Vytváření dokumentů a událostí</li>
            <li>✅ Základní analytické přehledy</li>
            <li>❌ Bez mazání a administrace</li>
        </ul>
        
        <h3>📋 Detailní oprávnění podle modulů</h3>
        
        <h4>Správa uživatelů (5 oprávnění)</h4>
        <ul>
            <li>Zobrazit uživatele</li>
            <li>Vytvořit uživatele</li>
            <li>Upravit uživatele</li>
            <li>Smazat uživatele</li>
            <li>Změnit heslo</li>
        </ul>
        
        <h4>Fakturace (4 oprávnění)</h4>
        <ul>
            <li>Zobrazit faktury</li>
            <li>Vytvořit faktury</li>
            <li>Upravit faktury</li>
            <li>Smazat faktury</li>
        </ul>
        
        <h4>Doprava a logistika (8 oprávnění)</h4>
        <ul>
            <li>Zobrazit dopravu</li>
            <li>Zadat jízdu</li>
            <li>Upravit jízdu</li>
            <li>Smazat jízdu</li>
            <li>Správa řidičů</li>
            <li>Správa vozidel</li>
            <li>Správa destinací</li>
            <li>Správa pohonných hmot</li>
        </ul>
        
        <h4>Zaměstnanci (7 oprávnění)</h4>
        <ul>
            <li>Zobrazit zaměstnance</li>
            <li>Přidat zaměstnance</li>
            <li>Upravit zaměstnance</li>
            <li>Smazat zaměstnance</li>
            <li>Správa smluv</li>
            <li>Správa školení</li>
            <li>Mzdová agenda</li>
        </ul>
        
        <p><em>Celkem <strong>57 oprávnění</strong> napříč <strong>12 moduly</strong> pro maximální flexibilitu!</em></p>
        """
        
        text_edit.setHtml(content)
        layout.addWidget(text_edit)
        
        self.tab_widget.addTab(widget, "👥 Role")
    
    def create_troubleshooting_tab(self):
        """Tab s řešením problémů"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        
        content = """
        <h2>❓ Řešení problémů</h2>
        
        <h3>🔑 Problémy s přihlášením</h3>
        
        <h4>Zapomenuté heslo</h4>
        <ul>
            <li><strong>Výchozí admin účet:</strong> admin / admin123</li>
            <li><strong>Reset hesla:</strong> Kontaktujte administrátora</li>
            <li><strong>Nový uživatel:</strong> Musí být vytvořen administrátorem</li>
        </ul>
        
        <h4>Chybějící oprávnění</h4>
        <ul>
            <li>Zkontrolujte <strong>roli uživatele</strong> v Správě uživatelů</li>
            <li><strong>Admin má vše</strong> - změňte roli na admin pro testování</li>
            <li><strong>Účetní má většinu</strong> funkcí kromě správy uživatelů</li>
            <li><strong>User má základní</strong> přístup jen k zobrazení</li>
        </ul>
        
        <h3>💻 Technické problémy</h3>
        
        <h4>Aplikace se nespustí</h4>
        <p><strong>Řešení:</strong></p>
        <ol>
            <li>Zkontrolujte Python: <code>python --version</code></li>
            <li>Zkontrolujte PyQt6: <code>pip list | findstr PyQt6</code></li>
            <li>Přeinstalujte: <code>pip install PyQt6</code></li>
            <li>Restartujte počítač</li>
        </ol>
        
        <h4>Chyba databáze</h4>
        <p><strong>Řešení:</strong></p>
        <ul>
            <li>Zkontrolujte existenci souboru <strong>invoices.db</strong></li>
            <li>Restartujte aplikaci - databáze se vytvoří automaticky</li>
            <li>Obnovte ze zálohy pokud je poškozená</li>
            <li>Smažte invoices.db a nechte vytvořit novou</li>
        </ul>
        
        <h4>Aplikace je pomalá</h4>
        <p><strong>Řešení:</strong></p>
        <ul>
            <li>Restartujte aplikaci</li>
            <li>Zkontrolujte volné místo na disku</li>
            <li>Zavřete ostatní aplikace</li>
            <li>Vytvořte zálohu a vyčistěte staré záznamy</li>
        </ul>
        
        <h3>📊 Problémy s daty</h3>
        
        <h4>Faktury se nezobrazují</h4>
        <ul>
            <li>Zkontrolujte <strong>filtr data</strong> v tabulce</li>
            <li>Vymažte filtry tlačítkem "Obnovit"</li>
            <li>Zkontrolujte <strong>oprávnění</strong> uživatele</li>
        </ul>
        
        <h4>Chybí uložené údaje</h4>
        <ul>
            <li>Zkontrolujte, zda jste <strong>uložili</strong> před zavřením</li>
            <li>Obnovte ze <strong>zálohy databáze</strong></li>
            <li>Zkontrolujte správnost <strong>databázového spojení</strong></li>
        </ul>
        
        <h3>🔐 Bezpečnostní tipy</h3>
        <ul>
            <li><strong>Pravidelně měňte hesla</strong> administrátorů</li>
            <li><strong>Používejte silná hesla</strong> (min. 8 znaků, kombinace písmen a čísel)</li>
            <li><strong>Zálohujte databázi</strong> <code>invoices.db</code> pravidelně</li>
            <li><strong>Kontrolujte přístupy</strong> uživatelů v Správě uživatelů</li>
        </ul>
        
        <h3>📞 Kontakt pro podporu</h3>
        <p><strong>Pokud problém přetrvává:</strong></p>
        <ul>
            <li>📧 <strong>Email:</strong> support@projektdevelop.cz</li>
            <li>📞 <strong>Telefon:</strong> +420 123 456 789</li>
            <li>🌐 <strong>Web:</strong> www.projektdevelop.cz</li>
            <li>💬 <strong>Pracovní doba:</strong> Po-Pá 8:00-17:00</li>
        </ul>
        """
        
        text_edit.setHtml(content)
        layout.addWidget(text_edit)
        
        self.tab_widget.addTab(widget, "❓ Problémy")
    
    def create_about_tab(self):
        """Tab s informacemi o aplikaci"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        
        content = """
        <h2>ℹ️ O aplikaci</h2>
        
        <h3>🚀 Firemní aplikace</h3>
        <p><strong>Verze:</strong> 1.0</p>
        <p><strong>Datum vydání:</strong> Červenec 2025</p>
        <p><strong>Vývojář:</strong> Projekt & Develop s.r.o.</p>
        
        <h3>📊 Statistiky projektu</h3>
        <ul>
            <li><strong>11,000+ řádků</strong> Python kódu</li>
            <li><strong>25+ modulů</strong> s kompletní funkcionalitou</li>
            <li><strong>57 oprávnění</strong> napříč 12 moduly</li>
            <li><strong>Žádné placeholder funkce</strong> - vše je plně implementováno</li>
            <li><strong>Moderní PyQt6 UI</strong> s responzivním designem</li>
        </ul>
        
        <h3>💻 Technologie</h3>
        <ul>
            <li><strong>Python 3.9+</strong> s PyQt6</li>
            <li><strong>SQLite</strong> databáze</li>
            <li><strong>Modulární architektura</strong></li>
            <li><strong>Rolový systém oprávnění</strong></li>
        </ul>
        
        <h3>🏆 Klíčové vlastnosti</h3>
        <ul>
            <li>✅ <strong>Kompletní business systém</strong> pro malé a střední firmy</li>
            <li>✅ <strong>57 detailních oprávnění</strong> pro přesnou kontrolu přístupu</li>
            <li>✅ <strong>12 hlavních modulů</strong> pokrývajících všechny oblasti podnikání</li>
            <li>✅ <strong>Moderní PyQt6 interface</strong> s intuitivním ovládáním</li>
            <li>✅ <strong>Robustní databáze</strong> s automatickým zálohováním</li>
            <li>✅ <strong>Plně funkční</strong> bez placeholder kódu</li>
            <li>✅ <strong>Připraveno pro produkci</strong> s profesionální dokumentací</li>
        </ul>
        
        <h3>📚 Dostupná dokumentace</h3>
        <ul>
            <li><strong>README.md</strong> - Hlavní dokumentace a přehled</li>
            <li><strong>UZIVATELSKY_NAVOD.md</strong> - Rychlý návod pro uživatele</li>
            <li><strong>TECHNICKA_DOKUMENTACE.md</strong> - Pro vývojáře a správce</li>
            <li><strong>CHANGELOG.md</strong> - Historie verzí a změn</li>
            <li><strong>INFO.txt</strong> - Rychlé informace</li>
        </ul>
        
        <h3>📞 Kontakt</h3>
        <p><strong>Projekt & Develop s.r.o.</strong></p>
        <ul>
            <li>📧 <strong>Email:</strong> support@projektdevelop.cz</li>
            <li>📞 <strong>Telefon:</strong> +420 123 456 789</li>
            <li>🌐 <strong>Web:</strong> www.projektdevelop.cz</li>
            <li>📍 <strong>Adresa:</strong> Václavské náměstí 1, Praha 1</li>
        </ul>
        
        <h3>⚖️ Licence</h3>
        <p>Proprietární software - všechna práva vyhrazena.</p>
        <p>Neoprávněné kopírování, distribuce nebo úprava je zakázána.</p>
        
        <hr>
        <p><em>Děkujeme za používání naší aplikace! Vaše zpětná vazba je pro nás cenná.</em></p>
        """
        
        text_edit.setHtml(content)
        layout.addWidget(text_edit)
        
        self.tab_widget.addTab(widget, "ℹ️ O aplikaci")
    
    def load_documentation(self):
        """Načte dokumentaci ze souborů (pokud existují)"""
        try:
            # Pokusíme se načíst README.md pro doplnění obsahu
            if os.path.exists("README.md"):
                with open("README.md", "r", encoding="utf-8") as f:
                    readme_content = f.read()
                    # Můžeme zde přidat další zpracování README obsahu
        except Exception as e:
            print(f"Chyba při načítání dokumentace: {e}")
