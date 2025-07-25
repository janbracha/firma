# 🚀 Firemní aplikace - Kompletní systém pro správu firmy

> **Verze 1.0** | Projekt & Develop s.r.o. | Aktualizováno: Červenec 2025

## 🎯 RYCHLÝ START

### ✅ Nejjednodušší způsob:
**Poklikejte na soubor `start_app.bat`**

### 🔧 Alternativní způsob:
1. Otevřete PowerShell nebo Command Prompt
2. Přejděte do složky projektu: `cd C:\git\firma`
3. Aktivujte virtuální prostředí: `.venv\Scripts\activate`
4. Spusťte aplikaci: `python main.py`

### 🔑 První přihlášení:
- **Uživatelské jméno:** `admin`
- **Heslo:** `admin123`

⚠️ **Po prvním přihlášení doporučujeme změnit heslo!**

### 📚 NOVÁ FUNKCE: Integrovaná nápověda
**Přístup k nápovědě přímo v aplikaci:**

1. **Menu:** Nápověda → 📚 Uživatelský návod
2. **Klávesová zkratka:** F1
3. **Dashboard:** Karta "📚 Nápověda a návody"

**Obsahuje 6 sekcí:**
- 🚀 Rychlý start
- 📖 Uživatelský návod  
- 🏢 Přehled funkcí
- 👥 Systém rolí
- ❓ Řešení problémů
- ℹ️ O aplikaci

## 📊 O APLIKACI

### Statistiky projektu:
- **11,000+ řádků** Python kódu
- **25+ modulů** s kompletní funkcionalitou  
- **57 oprávnění** napříč 12 moduly
- **Žádné placeholder funkce** - vše je plně implementováno
- **Moderní PyQt6 UI** s responzivním designem

### Technologie:
- **Python 3.9+** s PyQt6
- **SQLite** databáze 
- **Modulární architektura**
- **Rolový systém oprávnění**

## 🏢 KOMPLETNÍ FUNKCE APLIKACE

### 📊 **Fakturace a účetnictví**
- **Správa faktur** - Vystavování, úprava, export (PDF/Excel)
- **Pokladní deník** - Evidence příjmů a výdajů s automatickým zůstatkem
- **Analýzy a reporty** - Finanční přehledy, top klienti, měsíční statistiky

### 🏢 **Správa firmy a kontaktů**
- **Firemní kontakty** - Databáze obchodních partnerů (IČO, DIČ, bankovní spojení)
- **Nastavení firmy** - Konfigurace základních údajů, šablon
- **Správa dokumentů** - Centrální úložiště souborů s kategorizací

### 🚛 **Doprava a logistika**
- **Kniha jízd** - Evidence cest s automatickým výpočtem nákladů
- **Správa vozidel** - Evidence vozového parku, spotřeba, údržba
- **Správa řidičů** - Databáze řidičů s pozicemi a oprávněními
- **Destinace** - Správa tras s automatickým výpočtem vzdáleností
- **Pohonné hmoty** - Evidence tankování a spotřeby

### 👥 **HR a správa zaměstnanců**
- **Správa zaměstnanců** - Kompletní personální evidence
- **Pracovní smlouvy** - Správa dokumentů s připomínkami platnosti
- **Školení** - Plánování a evidence vzdělávání zaměstnanců
- **Mzdová agenda** - Správa mezd, odměn a benefitů

### 📦 **Skladování a majetek**
- **Skladové hospodářství** - Správa zásob s kategorizací
- **Hmotný majetek** - Evidence dlouhodobého majetku (pořizovací cena, odpisy)
- **Inventury** - Pravidelné kontroly stavu s reporty rozdílů

### 📅 **Plánování a údržba**
- **Kalendář** - Události, termíny, připomínky
- **Servis a údržba** - Plánování údržby majetku a vozidel
- **Certifikáty** - Správa platnosti dokumentů a kontrol

### 👤 **Systém uživatelů (pouze admin)**
- **Správa uživatelů** - Aktivace, deaktivace, změna hesel
- **Správa rolí** - 57 detailních oprávnění napříč 12 moduly
- **Audit trail** - Evidence změn a aktivit uživatelů

## 👥 SYSTÉM ROLÍ A OPRÁVNĚNÍ

### 🔑 **Administrator** (`admin`)
- **57 oprávnění** - Plný přístup ke všem funkcím
- Správa uživatelů a rolí
- Konfigurace systému a bezpečnosti

### 📊 **Účetní** (`accountant`)
- **45 oprávnění** - Většina operativních funkcí
- Správa faktur, účetnictví, analýz
- Správa majetku, dopravy, HR
- ❌ Bez správy uživatelů

### 👤 **Uživatel** (`user`)
- **14 oprávnění** - Základní zobrazení a vytváření
- Zobrazení většiny dat
- Vytváření dokumentů a událostí
- ❌ Bez mazání a administrace

## 📚 DOKUMENTACE

### 📖 **Návody pro uživatele**
- **[UZIVATELSKY_NAVOD.md](UZIVATELSKY_NAVOD.md)** - Rychlý průvodce použitím
- **[README.md](README.md)** - Tento soubor s kompletním přehledem

### 🔧 **Technická dokumentace**
- **[TECHNICKA_DOKUMENTACE.md](TECHNICKA_DOKUMENTACE.md)** - Pro vývojáře a správce
- **[CHANGELOG.md](CHANGELOG.md)** - Historie verzí a změn

### ℹ️ **Rychlé informace**
- **[INFO.txt](INFO.txt)** - Základní info v textovém formátu

## 🔐 BEZPEČNOST

### **Doporučení**
- Pravidelná změna hesel administrátorů
- Používání silných hesel (min. 8 znaků)
- Kontrola přístupových práv uživatelů
- Pravidelné zálohování databáze

### **Záloha dat**
```bash
# Ruční záloha databáze
copy invoices.db invoices_backup_YYYY-MM-DD.db
```

## ❓ ŘEŠENÍ PROBLÉMŮ

### **Aplikace se nespustí**
```bash
# Zkontrolujte Python a PyQt6
python --version
pip list | findstr PyQt6

# Přeinstalujte závislosti
pip install PyQt6
```

### **Problémy s přihlášením**
- **Výchozí admin:** admin/admin123
- **Zapomenuté heslo:** Kontaktujte administrátora
- **Chybí oprávnění:** Zkontrolujte přiřazenou roli

## 📞 PODPORA

**Technická podpora:**
- 📧 **Email:** support@projektdevelop.cz
- 📞 **Telefon:** +420 123 456 789
- 🌐 **Web:** www.projektdevelop.cz

**Vývojář:**
- **Společnost:** Projekt & Develop s.r.o.
- **Verze aplikace:** 1.0
- **Datum vydání:** Červenec 2025

---

## 🏆 SHRNUTÍ

✅ **Kompletní business systém** pro správu firmy  
✅ **57 detailních oprávnění** pro přesnou kontrolu přístupu  
✅ **12 hlavních modulů** pokrývajících všechny oblasti podnikání  
✅ **Moderní PyQt6 interface** s intuitivním ovládáním  
✅ **Plně funkční** bez placeholder kódu  
✅ **Připraveno pro produkci** s kompletní dokumentací

**Tato aplikace představuje kompletní řešení pro správu firmy s důrazem na jednoduchost, bezpečnost a funkcionalnost.**
