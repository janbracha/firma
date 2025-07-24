# 📖 Rychlý návod pro uživatele

## 🚀 Spuštění aplikace

1. **Poklikejte** na `start_app.bat` NEBO spusťte `python main.py`
2. **Přihlaste se:**
   - Uživatelské jméno: `admin`
   - Heslo: `admin123`

## 🏠 Hlavní menu

Po přihlášení se zobrazí dashboard s kartami funkcí:

### 📊 **Základní funkce**
- **📊 Správa faktur** - Vystavování a správa faktur
- **🏢 Správa firem** - Databáze obchodních partnerů  
- **💰 Pokladní deník** - Evidence příjmů a výdajů
- **🚛 Kniha jízd** - Evidence dopravy a cest
- **📎 Správa dokumentů** - Nahrávání a archivace souborů
- **🏢 Správa hmotného majetku** - Evidence dlouhodobého majetku
- **📈 Analýzy a reporty** - Finanční přehledy a statistiky
- **📅 Kalendář a termíny** - Plánování událostí
- **📋 Skladové hospodářství** - Správa zásob
- **👥 Správa zaměstnanců** - Personální evidence
- **🔧 Servis a údržba** - Plánování údržby

### ⚙️ **Systémové funkce** (pouze admin)
- **Systém → Nastavení firmy** - Základní konfigurace
- **Systém → Správa uživatelů** - Přidání/úprava uživatelů
- **Systém → Správa rolí** - Nastavení oprávnění

## 👤 Role uživatelů

### 🔑 **Admin** - Plný přístup
- Všechny funkce + správa uživatelů

### 📊 **Účetní** - Operativní funkce  
- Faktury, účetnictví, majetek, doprava, HR

### 👤 **Uživatel** - Základní funkce
- Zobrazení dat, vytváření dokumentů

## 💡 Rychlé tipy

### ✅ **Přidání nové faktury**
1. Klikněte "📊 Správa faktur"
2. "Přidat fakturu" 
3. Vyplňte údaje a uložte

### ✅ **Evidence platby**
1. Klikněte "💰 Pokladní deník"
2. "Přidat záznam"
3. Vyberte Příjem/Výdaj a částku

### ✅ **Nahrání dokumentu**
1. Klikněte "📎 Správa dokumentů" 
2. "Nahrát dokument"
3. Vyberte soubor a kategorii

### ✅ **Přidání zaměstnance**
1. Klikněte "👥 Správa zaměstnanců"
2. "Přidat zaměstnance"
3. Vyplňte osobní údaje

### ✅ **Změna hesla**
1. Systém → Správa uživatelů (admin)
2. Vyberte uživatele → "Změnit heslo"

## 🔐 Bezpečnost

- **Silná hesla** - min. 8 znaků, kombinace písmen a čísel
- **Pravidelné zálohování** - kopírujte `invoices.db`
- **Odhlašování** - vždy se odhlaste po práci

## 📞 Pomoc

**Technická podpora:**
- 📧 support@projektdevelop.cz  
- 📞 +420 123 456 789

**Nejčastější problémy:**
- **Aplikace se nespustí** → Zkontrolujte Python a PyQt6
- **Zapomenuté heslo** → Kontaktujte administrátora
- **Chybí oprávnění** → Zkontrolujte přiřazenou roli
