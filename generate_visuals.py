"""
FlunkyStats Visualization Generator
==================================

This script generates comprehensive charts and statistics for Flunky Ball tournament data.

Features:
- Daily beer consumption and participation analysis
- Individual rankings (total and single-day maximum)  
- Section-based performance comparisons
- Consistency analysis using Coefficient of Variation
- Age-based consumption patterns (line graph with gaps)
- Handles tied rankings by including all tied participants
- Generates both "Top 10+" and "All participants" versions

Input: cleaned_jesen.csv (processed tournament data)
Output: 10 PNG charts saved to ./visualizations/ folder

Chart Types:
1. Bar charts for daily totals and participation
2. Horizontal bar charts for individual rankings
3. Line graphs for age-based analysis
4. All charts include value labels and professional styling

Configuration:
- Update GODINA and NAZIV_TERENA constants for different tournaments
- Modify REFERENCE_DATE for accurate age calculations
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
from datetime import datetime

# ========== CONFIGURATION ==========
GODINA = 2025
NAZIV_TERENA = "Kordun Jesen"
REFERENCE_DATE = "2025-09-20"

# ========== SETUP ==========
# Configure plot styling for better appearance
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# Create output directory based on tournament name and year
output_dir = f'visualizations/{NAZIV_TERENA}_{GODINA}'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"Created '{output_dir}' directory")

# ========== DATA LOADING ==========
filename = 'jesen.csv'
df = pd.read_csv('data/cleaned_' + filename)
print(f"Loaded data: {len(df)} people, {len(df.columns)} columns")

# Convert beer consumption columns to integers (skip text columns)
for col in df.columns:
    if col not in ['Sekcija', 'ImePrezime', 'DatumRođenja']:
        df[col] = df[col].astype(int)

# ========== OVERVIEW STATISTICS TABLE ==========

# Calculate basic statistics
beer_columns = df.columns[3:10]  # Beer consumption columns (days)
total_people = len(df)

# Total beer consumption across all people and days
total_beers_consumed = df[beer_columns].sum().sum()

# Average beer per person per day
total_person_days = total_people * len(beer_columns)
avg_beer_per_person_per_day = total_beers_consumed / total_person_days

# People who drank every day (non-zero consumption all 7 days)
people_who_drank_every_day = ((df[beer_columns] > 0).sum(axis=1) == len(beer_columns)).sum()
percentage_daily_drinkers = (people_who_drank_every_day / total_people) * 100

# Total consumption per person
df_temp = df.copy()
df_temp['TotalConsumption'] = df_temp[beer_columns].sum(axis=1)
median_total_consumption = df_temp['TotalConsumption'].median()

# Additional interesting stats
max_single_day = df[beer_columns].max().max()
avg_total_per_person = df_temp['TotalConsumption'].mean()
people_who_never_drank = (df_temp['TotalConsumption'] == 0).sum()

# ========== VISUAL OVERVIEW STATISTICS TABLE ==========
print("Generating Overview Statistics Table...")

# Create visual table data - Croatian translation
table_data = [
    ["STATISTIKE KONZUMACIJE", ""],
    ["Prosječno popijeno dnevno po osobi", f"{avg_beer_per_person_per_day:.2f}"],
    ["Ukupno popijenih piva", f"{total_beers_consumed}"],
    ["", ""],
    ["SUDJELOVANJE", ""],
    ["Pili svaki dan", f"{people_who_drank_every_day} ({percentage_daily_drinkers:.1f}%)"],
    ["Nisu pili ništa", f"{people_who_never_drank} ({people_who_never_drank/total_people*100:.1f}%)"],
    ["Aktivni sudionici", f"{total_people - people_who_never_drank} ({(total_people-people_who_never_drank)/total_people*100:.1f}%)"],
    ["", ""],
    ["EKSTREMNE VRIJEDNOSTI", ""],
    ["Najviše piva u jednom dana", f"{max_single_day} piva"],
    ["Najviše piva ukupno", f"{df_temp['TotalConsumption'].max():.0f} piva"]
]

# Create figure and table
fig, ax = plt.subplots(figsize=(10, 10))
ax.axis('tight')
ax.axis('off')

# Create table
table = ax.table(cellText=table_data, 
                colWidths=[0.4, 0.6],
                cellLoc='left',
                loc='center',
                bbox=[0, 0, 1, 1])

# Style the table
table.auto_set_font_size(False)
table.set_fontsize(12)
table.scale(1, 2.2)

# Color formatting
data_row_counter = 0  # Counter for actual data rows only
for i, (key, value) in enumerate(table_data):
    # Header rows (section headers in ALL CAPS)
    if key in ('INFORMACIJE O TURNIRU', 'STATISTIKE KONZUMACIJE', 'SUDJELOVANJE', 'EKSTREMNE VRIJEDNOSTI'):
        table[(i, 0)].set_facecolor('#4472C4')
        table[(i, 0)].set_text_props(weight='bold', color='white')
        table[(i, 1)].set_facecolor('#4472C4')
        table[(i, 1)].set_text_props(weight='bold', color='white')
    # Empty separator rows
    elif key == "":
        table[(i, 0)].set_facecolor('#F2F2F2')
        table[(i, 1)].set_facecolor('#F2F2F2')
    # Data rows
    else:
        # Alternating row colors for better readability using data row counter
        if data_row_counter % 2 == 0:
            table[(i, 0)].set_facecolor('#FFFFFF')
            table[(i, 1)].set_facecolor('#FFFFFF')
        else:
            table[(i, 0)].set_facecolor('#E8F1FF')
            table[(i, 1)].set_facecolor('#E8F1FF')
        
        # Bold the labels
        table[(i, 0)].set_text_props(weight='bold')
        data_row_counter += 1  # Increment only for actual data rows

# Add title
fig.suptitle(f'{NAZIV_TERENA} {GODINA} - Pregled Statistika', 
             fontsize=18, fontweight='bold', y=0.98)

# Add border
for (row, col), cell in table.get_celld().items():
    cell.set_edgecolor('#CCCCCC')
    cell.set_linewidth(0.5)

plt.tight_layout()
plt.savefig(f'{output_dir}/00_overview_statistics.png', dpi=150, bbox_inches='tight')
plt.close()

# Clean up temporary dataframe
del df_temp

# ========== UTILITY FUNCTIONS ==========

def create_two_column_table(df, filename, title, value_column='Ukupno'):
    """
    Creates a two-column table visualization to save space.
    
    Args:
        df: DataFrame with Mjesto, ImePrezime, and value columns
        filename: Output filename
        title: Chart title
        value_column: Column name for values (default: 'Ukupno')
    """
    # Include all people (no filtering based on values)
    df_filtered = df.copy()
    
    # Prepare table data for all filtered entries
    table_data_all = []
    for _, row in df_filtered.iterrows():
        if value_column == 'CV':
            table_data_all.append([f"{int(row['Mjesto'])}.", row['ImePrezime'], f"{row[value_column]:.3f}"])
        else:
            table_data_all.append([f"{int(row['Mjesto'])}.", row['ImePrezime'], f"{int(row[value_column])}"])
    
    # Split the filtered data equally into two columns
    total_entries = len(table_data_all)
    entries_per_column = (total_entries + 1) // 2  # Ceiling division
    
    table_data_left = table_data_all[:entries_per_column]
    table_data_right = table_data_all[entries_per_column:]
    
    # Create figure - narrower width
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 10))
    fig.suptitle(title, fontsize=16, fontweight='bold', y=0.98)
    
    # Left column
    if table_data_left:
        table1 = ax1.table(cellText=table_data_left,
                          colLabels=['Mjesto', 'Ime i Prezime', 'Vrijednost'],
                          cellLoc='left',
                          loc='center',
                          colWidths=[0.15, 0.65, 0.2])
        table1.auto_set_font_size(False)
        table1.set_fontsize(9)
        table1.scale(1, 1.5)
        
        # Style the table
        for i in range(len(table_data_left) + 1):
            for j in range(3):
                cell = table1[i, j]
                if i == 0:  # Header
                    cell.set_facecolor('#4CAF50')
                    cell.set_text_props(weight='bold', color='white')
                else:
                    cell.set_facecolor('#f0f0f0' if i % 2 == 0 else 'white')
    
    ax1.axis('off')
    
    # Right column
    if table_data_right:
        table2 = ax2.table(cellText=table_data_right,
                          colLabels=['Mjesto', 'Ime i Prezime', 'Vrijednost'],
                          cellLoc='left',
                          loc='center',
                          colWidths=[0.15, 0.65, 0.2])
        table2.auto_set_font_size(False)
        table2.set_fontsize(9)
        table2.scale(1, 1.5)
        
        # Style the table
        for i in range(len(table_data_right) + 1):
            for j in range(3):
                cell = table2[i, j]
                if i == 0:  # Header
                    cell.set_facecolor('#4CAF50')
                    cell.set_text_props(weight='bold', color='white')
                else:
                    cell.set_facecolor('#f0f0f0' if i % 2 == 0 else 'white')
    
    ax2.axis('off')
    
    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches='tight')  # Reduced DPI back to original
    plt.close()

def get_top10_with_ties(df, value_column, ascending=False):
    """
    Returns the top 10+ entries, including all tied participants.
    
    Args:
        df: DataFrame to process
        value_column: Column name to rank by
        ascending: Sort order (False for descending/highest first)
    
    Returns:
        DataFrame with top 10+ entries including ties
    """
    # Sort by Mjesto (rank) which should already be calculated
    df_sorted = df.sort_values(by=['Mjesto', 'ImePrezime']).reset_index(drop=True)
    
    if len(df_sorted) <= 10:
        return df_sorted
    
    tenth_place_rank = df_sorted.iloc[9]['Mjesto']  # Get 10th place rank value
    # Include all people with rank <= 10th place rank (handles ties)
    return df_sorted[df_sorted['Mjesto'] <= tenth_place_rank]

def calculate_age(birth_date_str, reference_date=REFERENCE_DATE):
    """
    Calculate age from birth date string in dd.mm.yyyy format.
    
    Args:
        birth_date_str: Date string in format "dd.mm.yyyy"
        reference_date: Reference date for age calculation
    
    Returns:
        Age in years or None if invalid date
    """
    if not isinstance(birth_date_str, str) or birth_date_str in ["N/A", "0", ""]:
        return None
    
    try:
        # Parse birth date (dd.mm.yyyy format)
        day, month, year = birth_date_str.split('.')
        birth_date = datetime(int(year), int(month), int(day))
        
        # Parse reference date (yyyy-mm-dd format)
        ref_year, ref_month, ref_day = reference_date.split('-')
        reference = datetime(int(ref_year), int(ref_month), int(ref_day))
        
        # Calculate age
        age = reference.year - birth_date.year
        if (reference.month, reference.day) < (birth_date.month, birth_date.day):
            age -= 1
            
        return age
    except:
        return None

# === 1. DNEVNA KONZUMACIJA PIVA ===
print("Generating Chart 1: Daily beer consumption...")

# Calculate total beers consumed per day
df_dani = df.copy()
df_dani_sum = df_dani.iloc[:, 3:10].sum().reset_index()  # Sum beer columns (3-9)
df_dani_sum.columns = ['Dan', 'UkupnoPiva']
df_dani_sum = df_dani_sum.sort_values(by='Dan')

# Create bar chart
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(df_dani_sum['Dan'], df_dani_sum['UkupnoPiva'], 
              color='gold', edgecolor='black', linewidth=1.2)

# Styling
ax.set_title(f'{NAZIV_TERENA} {GODINA}\nUkupno Popijenih Piva Po Danu', 
             fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Dan', fontsize=14)
ax.set_ylabel('Broj Piva', fontsize=14)
ax.grid(axis='y', alpha=0.3, linestyle='--')

# Add value labels on top of bars
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 0.5, 
            f'{int(height)}', ha='center', va='bottom', 
            fontweight='bold', fontsize=12)

plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(f'{output_dir}/01_piva_po_danu.png', dpi=150, bbox_inches='tight')
plt.close()
del df_dani, df_dani_sum


# === 2. DNEVNA AKTIVNOST ===
print("Generating Chart 2: Daily participation...")

# Count active people per day (those who drank at least 1 beer) and convert to percentage
df_activity = df.copy()
total_people = len(df_activity)
daily_drinkers = {}
daily_percentages = {}
for col in df_activity.columns[3:10]:  # Beer consumption columns
    active_count = (df_activity[col] > 0).sum()
    daily_drinkers[col] = active_count
    daily_percentages[col] = (active_count / total_people) * 100

# Create bar chart
fig, ax = plt.subplots(figsize=(10, 6))
days = list(daily_percentages.keys())
percentages = list(daily_percentages.values())
bars = ax.bar(days, percentages, color='lightcoral', edgecolor='black', linewidth=1.2)

# Styling
ax.set_title(f'{NAZIV_TERENA} {GODINA}\nPostotak Aktivnih Sudionika Po Danu\n(od ukupno {total_people} sudionika, Aktivni = popili bar jednu pivu)', 
             fontsize=14, fontweight='bold', pad=20)
ax.set_xlabel('Dan', fontsize=14)
ax.set_ylabel('Postotak Aktivnih (%)', fontsize=14)
ax.grid(axis='y', alpha=0.3, linestyle='--')
ax.set_ylim(0, 100)  # Set y-axis from 0 to 100%

# Add value labels with both percentage and count
for i, bar in enumerate(bars):
    height = bar.get_height()
    day_key = days[i]
    count = daily_drinkers[day_key]
    ax.text(bar.get_x() + bar.get_width()/2., height + 1, 
            f'{height:.1f}%\n({count})', ha='center', va='bottom', 
            fontweight='bold', fontsize=10)

plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(f'{output_dir}/02_aktivni_ljudi_po_danu.png', dpi=150, bbox_inches='tight')
plt.close()
del df_activity, daily_drinkers

# === 3. UKUPNA KONZUMACIJA PIVA PO OSOBI ===
print("Generating Chart 3: Total consumption ranking...")

# Calculate total beer consumption per person and rank them
df_ukupno = df.copy()
df_ukupno['Ukupno'] = df_ukupno.iloc[:, 3:].sum(axis=1)  # Sum all beer columns
df_ukupno['Mjesto'] = df_ukupno['Ukupno'].rank(method='min', ascending=False).astype(int)
df_ukupno = df_ukupno.sort_values(by=['Mjesto', 'ImePrezime']).reset_index(drop=True)

# Get top 10 (including ties for 10th place)
top10 = get_top10_with_ties(df_ukupno, 'Ukupno')

# Create horizontal bar chart
fig, ax = plt.subplots(figsize=(12, 8))
bars = ax.barh(range(len(top10)), top10['Ukupno'], 
               color='lightcoral', edgecolor='darkred', linewidth=0.8)

# Styling
ax.set_yticks(range(len(top10)))
ax.set_yticklabels([f"{row['Mjesto']}. {row['ImePrezime']}" 
                    for _, row in top10.iterrows()], fontsize=10)
ax.set_title(f'{NAZIV_TERENA} {GODINA}\nTop 10 - Ukupno Popijenih Piva Kroz Cijeli Teren', 
             fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Broj Piva', fontsize=14)
ax.grid(axis='x', alpha=0.3, linestyle='--')
ax.invert_yaxis()

# Add value labels
for i, bar in enumerate(bars):
    width = bar.get_width()
    ax.text(width + 0.5, bar.get_y() + bar.get_height()/2, 
            f'{int(width)}', ha='left', va='center', 
            fontweight='bold', fontsize=10)

plt.tight_layout()
plt.savefig(f'{output_dir}/03_ukupno_top10.png', dpi=150, bbox_inches='tight')
plt.close()

# All people - Table format
create_two_column_table(df_ukupno, 
                       f'{output_dir}/03_ukupno_svi.png',
                       f'{NAZIV_TERENA} {GODINA}\nSvi - Ukupno Piva Kroz Cijeli Teren',
                       'Ukupno')

# === 4. NAJVIŠE PIVA U JEDNOM DANU ===
print("Generating Chart 4: Max in a single day ranking...")
df_max = df.copy()
df_max['MaxPiva'] = df_max.iloc[:, 3:10].max(axis=1)
df_max['Mjesto'] = df_max['MaxPiva'].rank(method='min', ascending=False).astype(int)
df_max = df_max.sort_values(by=['Mjesto', 'ImePrezime']).reset_index(drop=True)

# Top 10
top10 = get_top10_with_ties(df_max, 'MaxPiva')
fig, ax = plt.subplots(figsize=(12, 8))
bars = ax.barh(range(len(top10)), top10['MaxPiva'], color='orange')
ax.set_yticks(range(len(top10)))
ax.set_yticklabels([f"{row['Mjesto']}. {row['ImePrezime']}" for _, row in top10.iterrows()])
ax.set_title(f'{NAZIV_TERENA} {GODINA}\nTop 10 - Najviše Piva U Jednom Danu', fontsize=16, fontweight='bold')
ax.set_xlabel('Broj Piva', fontsize=14)
ax.grid(axis='x', alpha=0.3)
ax.invert_yaxis()

for i, bar in enumerate(bars):
    width = bar.get_width()
    ax.text(width + 0.1, bar.get_y() + bar.get_height()/2, f'{int(width)}',
            ha='left', va='center', fontweight='bold')

plt.tight_layout()
plt.savefig(f'{output_dir}/04_max_piva_top10.png', dpi=150, bbox_inches='tight')
plt.close()

# All people - Table formatcolWidths=[0.15, 0.55, 0.3])
create_two_column_table(df_max, 
                       f'{output_dir}/04_max_piva_svi.png',
                       f'{NAZIV_TERENA} {GODINA}\nSvi - Najviše Piva U Jednom Danu',
                       'MaxPiva')

# === 5. BROJ PIVA PO SEKCIJI U ODNOSU NA BROJ ČLANOVA ---
print("Generating Chart 5: Section average consumption...")
df_sekcija = df.copy()
df_sekcija['Ukupno'] = df_sekcija.iloc[:, 3:].sum(axis=1)
df_sekcija['Sekcija'] = df_sekcija['Sekcija'].str.split(' - ')
df_sekcija = df_sekcija.explode('Sekcija')
df_sekcija_grouped = df_sekcija.groupby('Sekcija').agg({'ImePrezime': 'count', 'Ukupno': 'sum'}).reset_index()
df_sekcija_grouped = df_sekcija_grouped.rename(columns={'ImePrezime': 'BrojOsoba', 'Ukupno': 'TotalPiva'})
df_sekcija_grouped['PivaPoOsobi'] = df_sekcija_grouped['TotalPiva'] / df_sekcija_grouped['BrojOsoba']
df_sekcija_grouped['Mjesto'] = df_sekcija_grouped['PivaPoOsobi'].rank(method='min', ascending=False).astype(int)
df_sekcija_grouped = df_sekcija_grouped.sort_values(by=['Mjesto', 'Sekcija']).reset_index(drop=True)

fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.bar(range(len(df_sekcija_grouped)), df_sekcija_grouped['PivaPoOsobi'], color='lightgreen', edgecolor='black')
ax.set_xticks(range(len(df_sekcija_grouped)))
ax.set_xticklabels([f"{row['Mjesto']}. {row['Sekcija']}" for _, row in df_sekcija_grouped.iterrows()], rotation=45, ha='right')
ax.set_title(f'{NAZIV_TERENA} {GODINA}\nNajžednija Sekcija Po Prosječnoj Konzumaciji\n(Piva po osobi u sekciji)', fontsize=14, fontweight='bold')
ax.set_ylabel('Prosjek Piva Po Članu Sekcije', fontsize=14)
ax.grid(axis='y', alpha=0.3)

for i, bar in enumerate(bars):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 0.1, f'{height:.1f}',
            ha='center', va='bottom', fontweight='bold', fontsize=10)

plt.tight_layout()
plt.savefig(f'{output_dir}/05_sekcije_piva_po_osobi.png', dpi=150, bbox_inches='tight')
plt.close()

# === 6. STABILNOST KONZUMACIJE PO DANIMA ===
print("Generating Chart 6: Consistency ranking (Coefficient of Variation)...")
df_cv = df.copy()
df_cv['MinDan'] = df_cv.iloc[:, 3:10].min(axis=1)
df_cv['Prosjek'] = df_cv.iloc[:, 3:10].mean(axis=1).round(2)
df_cv['StdDev'] = df_cv.iloc[:, 3:10].std(axis=1).round(2)
df_cv['CV'] = (df_cv['StdDev'] / df_cv['Prosjek']).round(3)
df_cv = df_cv[df_cv['CV'].notna() & df_cv['CV'].apply(lambda x: x != float('inf'))]
df_cv['Mjesto'] = df_cv['CV'].rank(method='min', ascending=True).astype(int)
df_cv = df_cv.sort_values(by=['Mjesto', 'ImePrezime']).reset_index(drop=True)

# Top 10 (including ties)
top10 = get_top10_with_ties(df_cv, 'CV', ascending=True)
fig, ax = plt.subplots(figsize=(12, 8))
bars = ax.barh(range(len(top10)), top10['CV'], color='purple', alpha=0.7)
ax.set_yticks(range(len(top10)))
ax.set_yticklabels([f"{row['Mjesto']}. {row['ImePrezime']}" for _, row in top10.iterrows()])
ax.set_title(f'{NAZIV_TERENA} {GODINA}\nTop 10 - Konzistentnost Pijenja po Danima\n(Koeficijent Varijacije, najmanja razlika u dnevnoj konzumaciji)', fontsize=14, fontweight='bold')
ax.set_xlabel('Stupanj Varijacije (manji broj = veća konzistentnost, veći broj = više oscilacija)', fontsize=12)
ax.grid(axis='x', alpha=0.3)
ax.invert_yaxis()

for i, bar in enumerate(bars):
    width = bar.get_width()
    ax.text(width + 0.005, bar.get_y() + bar.get_height()/2, f'{width:.3f}',
            ha='left', va='center', fontweight='bold')

plt.tight_layout()
plt.savefig(f'{output_dir}/06_cv_top10.png', dpi=150, bbox_inches='tight')
plt.close()

# All people - Table format
create_two_column_table(df_cv, 
                       f'{output_dir}/06_cv_svi.png',
                       f'{NAZIV_TERENA} {GODINA}\nSvi - Konzistentnost Pijenja po Danima, Koeficijent Varijacije CV\n(najmanja razlika u dnevnoj konzumaciji, manji broj = veća konzistentnost, veći broj = više oscilacija)',
                       'CV')


# === 7. LINE GRAPH PO GODINAMA ===
print("Generating Chart 7: Age-based consumption line graph...")
# Calculate age and create line graph showing averages by age
from datetime import datetime

def calculate_age(birth_date_str, reference_date="2024-09-20"):
    if not isinstance(birth_date_str, str) or birth_date_str in ["N/A", "0", ""]:
        return None
    
    try:
        day, month, year = birth_date_str.split('.')
        birth_date = datetime(int(year), int(month), int(day))
        ref_year, ref_month, ref_day = reference_date.split('-')
        reference = datetime(int(ref_year), int(ref_month), int(ref_day))
        
        age = reference.year - birth_date.year
        if (reference.month, reference.day) < (birth_date.month, birth_date.day):
            age -= 1
            
        return age
    except:
        return None

# Prepare data for line graph
df_age = df.copy()
df_age['Age'] = df_age['DatumRođenja'].apply(calculate_age)
df_age['Ukupno'] = df_age.iloc[:, 3:10].sum(axis=1)

# Remove people without valid age
df_age = df_age[df_age['Age'].notna()].copy()

if len(df_age) > 0:
    # Calculate averages by age
    age_averages = df_age.groupby('Age')['Ukupno'].mean()
    age_counts = df_age.groupby('Age')['Ukupno'].count()
    
    # Get all ages from min to max (including gaps)
    min_age = int(df_age['Age'].min())
    max_age = int(df_age['Age'].max())
    all_ages = list(range(min_age, max_age + 1))
    
    # Create lists for plotting (None for missing ages)
    averages = []
    counts = []
    for age in all_ages:
        if age in age_averages.index:
            averages.append(age_averages[age])
            counts.append(age_counts[age])
        else:
            averages.append(None)
            counts.append(0)
    
    # Create line graph
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Plot line connecting only existing data points
    existing_ages = []
    existing_averages = []
    for i, (age, avg) in enumerate(zip(all_ages, averages)):
        if avg is not None:
            existing_ages.append(age)
            existing_averages.append(avg)
    
    # Plot the line connecting averages
    ax.plot(existing_ages, existing_averages, 'o-', linewidth=3, markersize=8, 
            color='darkblue', markerfacecolor='lightblue', markeredgecolor='darkblue', markeredgewidth=2)
    
    # Add sample size annotations for existing points
    for age, avg, count in zip(existing_ages, existing_averages, [age_counts[age] for age in existing_ages]):
        ax.annotate(f'n={count}', (age, avg), textcoords="offset points", 
                   xytext=(0,10), ha='center', fontsize=10, color='red', fontweight='bold')
    
    # Add legend explaining the annotations
    ax.text(0.02, 0.98, 'n = broj sudionika te dobi', transform=ax.transAxes, 
            fontsize=11, verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    # Set x-axis to show all years (including gaps)
    ax.set_xticks(all_ages)
    ax.set_xticklabels(all_ages, rotation=45)
    
    ax.set_title(f'{NAZIV_TERENA} {GODINA}\nProsjek Konzumacije Piva Po Godinama Starosti\n(Praznine = nema sudionika te dobi)', 
                fontsize=14, fontweight='bold')
    ax.set_xlabel('Godine Starosti', fontsize=14)
    ax.set_ylabel('Prosjek Popijenih Piva', fontsize=14)
    ax.grid(True, alpha=0.3)
    
    # Add a subtle background for missing ages
    for i, age in enumerate(all_ages):
        if averages[i] is None:
            ax.axvspan(age-0.4, age+0.4, alpha=0.1, color='gray')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/07_line_graph_godine.png', dpi=150, bbox_inches='tight')
    plt.close()
else:
    print("⚠️  Warning: No valid age data available for age-based line graph")

# ========== PDF COMPILATION ==========
print("\n📄 Generiranje PDF izvještaja...")

try:
    from matplotlib.backends.backend_pdf import PdfPages
    
    # List of image files to include (excluding Top 10 versions)
    pdf_images = [
        f'{output_dir}/00_overview_statistics.png',      # Overview table
        f'{output_dir}/01_piva_po_danu.png',            # Daily consumption
        f'{output_dir}/02_aktivni_ljudi_po_danu.png',   # Daily participation
        f'{output_dir}/03_ukupno_svi.png',              # Total ranking - ALL
        f'{output_dir}/04_max_piva_svi.png',            # Max single day - ALL
        f'{output_dir}/06_cv_svi.png',                  # Consistency - ALL
        f'{output_dir}/05_sekcije_piva_po_osobi.png',   # Section rankings
        f'{output_dir}/07_line_graph_godine.png'        # Age analysis
    ]
    
    # Create PDF
    pdf_filename = f'{output_dir}/{NAZIV_TERENA}_{GODINA}_Complete_Report.pdf'
    
    with PdfPages(pdf_filename) as pdf:
        for img_path in pdf_images:
            if os.path.exists(img_path):
                # Load image and preserve original dimensions
                img = plt.imread(img_path)
                img_height, img_width = img.shape[:2]
                
                # Calculate figure size in inches (assuming 150 DPI)
                fig_width = img_width / 150
                fig_height = img_height / 150
                
                # Create figure with original proportions
                fig, ax = plt.subplots(figsize=(fig_width, fig_height))
                ax.imshow(img)
                ax.axis('off')
                
                # Remove all margins to preserve exact dimensions
                fig.subplots_adjust(left=0, bottom=0, right=1, top=1)
                
                # Save with same DPI as original
                pdf.savefig(fig, bbox_inches='tight', dpi=150, 
                           facecolor='white', edgecolor='none')
                plt.close(fig)
            else:
                print(f"⚠️  Warning: {img_path} not found, skipping...")
    
    print(f"✅ PDF izvještaj kreiran: {pdf_filename}")
    print(f"📋 Uključeno {len([p for p in pdf_images if os.path.exists(p)])} grafova (sve sveobuhvatne verzije)")
    
except ImportError:
    print("⚠️  matplotlib.backends.backend_pdf not available, PDF generation skipped")
except Exception as e:
    print(f"⚠️  Error creating PDF: {e}")

print("="*60)