# FlunkyStats - Generator Statistika Flunky-ja

FlunkyStats je Python skripta za generiranje detaljnih statistika i vizualizacija iz podataka Flunky-ja.

## 📋 Sadržaj
- [Struktura Direktorija](#struktura-direktorija)
- [Sistemski Zahtjevi](#sistemski-zahtjevi)
- [Instalacija](#instalacija)
- [Format CSV Datoteke](#format-csv-datoteke)
- [Kako Pokrenuti](#kako-pokrenuti)
- [Generirani Rezultati](#generirani-rezultati)
- [Rješavanje Problema](#rješavanje-problema)

## � Struktura Direktorija

FlunkyStats koristi sljedeću strukturu mapa:

```
FlunkyStats/
├── data/                           # CSV datoteke (input i cleaned)
│   ├── jesen.csv                  # Originalna CSV datoteka
│   └── cleaned_jesen.csv          # Očišćena CSV datoteka
├── visualizations/                 # Generirani rezultati
│   └── [Naziv]_[Godina]/          # Specifična mapa za turnir
│       ├── 00_overview_statistics.png
│       ├── 01_piva_po_danu.png
│       ├── ...
│       └── [Naziv]_[Godina]_Complete_Report.pdf
├── clean_csv.py                   # Skripta za čišćenje podataka
├── generate_visuals.py              # Glavna skripta za generiranje
└── README.md                      # Ova datoteka
```

## �🔧 Instalacija

### Korak 1: Instalirajte Python

1. **Preuzmite Python**:
   - Idite na https://www.python.org/downloads/
   - Kliknite "Download Python 3.x.x" (najnovija verzija)

2. **Instalirajte Python**:
   - Pokrenite preuzetu `.exe` datoteku
   - **VAŽNO**: Označite "Add Python to PATH" tijekom instalacije
   - Kliknite "Install Now"

3. **Provjerite instalaciju**:
   - Otvorite Command Prompt (Win + R, utipkajte `cmd`, Enter)
   - Utipkajte: `python --version`
   - Trebali biste vidjeti verziju Pythona (npr. "Python 3.11.2")

### Korak 2: Instalirajte Potrebne Module

Otvorite Command Prompt i utipkajte sljedeće naredbe:

```cmd
pip install pandas
pip install matplotlib
pip install seaborn
pip install numpy
```

**Alternativno**, možete koristiti requirements.txt datoteku:
```cmd
pip install -r requirements.txt
```

## 📊 Format CSV Datoteke

Vaša CSV datoteka mora imati sljedeći format:

### Lokacija datoteke
- **Stavi CSV datoteku u `data/` mapu**
- Naziv datoteke: `jesen.csv` (ili bilo koje ime, ali promijenite u skripti)

### Struktura stupaca
```csv
Sekcija,ImePrezime,DatumRođenja,Dan1,Dan2,Dan3,Dan4,Dan5,Dan6,Dan7
Sekcija A,Marko Marić,15.03.1995,3,2,1,0,4,2,1
Sekcija B,Ana Anić,22.07.1992,2,3,2,1,3,1,2
```

### Objašnjenje stupaca:
- **Sekcija**: Naziv sekcije (npr. "Sekcija A", "Grupa 1")
- **ImePrezime**: Ime i prezime sudionika
- **DatumRođenja**: Datum rođenja u formatu `dd.mm.yyyy`
- **Dan1-Dan7**: Broj popijenih piva po danima (brojevi 0-99)

### Važne napomene:
- CSV datoteka mora biti u UTF-8 kodiranju
- Koristite zarez (`,`) kao separator
- Datumi rođenja moraju biti u formatu `dd.mm.yyyy`
- Brojevi piva moraju biti cijeli brojevi

## ▶️ Kako Pokrenuti

### Korak 1: Priprema Podataka

1. **Kreirajte `data/` mapu** u FlunkyStats direktoriju
2. **Stavite CSV datoteku** u `data/` mapu (npr. `data/jesen.csv`)
3. **Pokrenite čišćenje podataka**:
   ```cmd
   cd putanja\do\FlunkyStats
   python clean_csv.py
   ```
   - Ovo će kreirati `data/cleaned_jesen.csv` datoteku

### Korak 2: Generiranje Vizualizacija

```cmd
python generate_visuals.py
```

### Korak 3: Provjera Rezultata

Provjerite mapu `visualizations/[Naziv]_[Godina]/` za generirane slike i PDF.

## 📈 Generirani Rezultati

### PNG Slike
- `00_overview_statistics.png` - Pregled statistika turnira
- `01_piva_po_danu.png` - Dnevna konzumacija piva
- `02_aktivni_ljudi_po_danu.png` - Dnevno sudjelovanje
- `03_ukupno_top10.png` - Top 10+ ukupno piva
- `03_ukupno_svi.png` - Svi sudionici ukupno piva (tablica)
- `04_max_piva_top10.png` - Top 10+ max piva u danu
- `04_max_piva_svi.png` - Svi sudionici max piva u danu (tablica)
- `05_sekcije_piva_po_osobi.png` - Rangiranje sekcija
- `06_cv_top10.png` - Top 10+ konzistentnost
- `06_cv_svi.png` - Svi sudionici konzistentnost (tablica)
- `07_line_graph_godine.png` - Prosjek po godinama

### PDF Izvještaj
- `Jesen_2025_Complete_Report.pdf` - Sveobuhvatan PDF s 8 glavnih grafova

## 🛠️ Rješavanje Problema

### Problem: "python nije prepoznat kao naredba"
**Rješenje**: Python nije dodan u PATH varijablu
1. Reinstalirajte Python i označite "Add Python to PATH"
2. Ili dodajte Python ručno u PATH varijable

### Problem: "No module named 'pandas'"
**Rješenje**: Modul nije instaliran
```cmd
pip install pandas matplotlib seaborn numpy
```

### Problem: "Permission denied"
**Rješenje**: Pokrenite Command Prompt kao administrator

### Problem: CSV se ne čita ispravno
**Rješenje**: 
1. Provjerite da li je CSV datoteka u `data/` mapi
2. Provjerite da li CSV ima ispravne stupce
3. Provjerite UTF-8 kodiranje
4. Provjerite format datuma (dd.mm.yyyy)

### Problem: Nema generiranih slika
**Rješenje**:
1. Provjerite da li postoji `data/` mapa s CSV datotekama
2. Pokrenite `clean_csv.py` prije `generate_visuals.py`
3. Provjerite da li postoji `data/cleaned_jesen.csv`
4. Provjerite da li se kreira `visualizations/[Naziv]_[Godina]/` mapa

## 📝 Konfiguracija

Za različita događanja, promijenite ove varijable u `generate_visuals.py`:

```python
GODINA = 2025                   # Godina terena
NAZIV_TERENA = "Jesen"          # Naziv terena
REFERENCE_DATE = "2024-09-20"   # Referentni datum za godine
```