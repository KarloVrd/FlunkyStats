import pandas as pd

# load csv file 
filename = 'jesen.csv'
df = pd.read_csv('data/' + filename)

NA_symbol = "N/A"

# Strip whitespaces from every cell in the dataframe
df = df.map(lambda x: x.strip() if isinstance(x, str) else x)
# Remove empty rows
df = df.dropna(how='all')
# Remove empty columns
df = df.dropna(axis=1, how='all')
# replace empty Sekcija, ImePrezime, or DatumRođenja with NaN
df['Sekcija'] = df['Sekcija'].replace('', NA_symbol)
df['ImePrezime'] = df['ImePrezime'].replace('', NA_symbol)
df['DatumRođenja'] = df['DatumRođenja'].replace('', NA_symbol)
df['Sekcija'] = df['Sekcija'].fillna(NA_symbol)
df['ImePrezime'] = df['ImePrezime'].fillna(NA_symbol)
df['DatumRođenja'] = df['DatumRođenja'].fillna(NA_symbol)

# replace NaN with 0 only in numeric columns (not in Sekcija, ImePrezime, DatumRođenja)
numeric_columns = df.select_dtypes(include=['number']).columns
df[numeric_columns] = df[numeric_columns].fillna(0)
# Convert numeric columns to integers to avoid decimal points
df[numeric_columns] = df[numeric_columns].astype(int)
# Make first letter uppercase only for Sekcija (keep rest unchanged)
df['Sekcija'] = df['Sekcija'].apply(lambda x: x[0].upper() + x[1:] if isinstance(x, str) and len(x) > 0 and x != '0' else x)
# Make first letter uppercase only for ImePrezime (keep rest unchanged)
df['ImePrezime'] = df['ImePrezime'].apply(lambda x: x[0].upper() + x[1:] if isinstance(x, str) and len(x) > 0 and x != '0' else x)

# Normalize DatumRođenja to dd.mm.yyyy format
def normalize_date(date_str):
    if not isinstance(date_str, str) or date_str in [NA_symbol, '0', '']:
        return date_str
    
    # Remove any extra spaces and trailing dots
    date_str = date_str.strip().rstrip('.')
    
    # Replace multiple spaces with single space, then remove all spaces around dots
    import re
    date_str = re.sub(r'\s+', ' ', date_str)  # Replace multiple spaces with single space
    date_str = re.sub(r'\s*\.\s*', '.', date_str)  # Remove spaces around dots
    
    # Handle different separators (., /, -)
    for sep in ['.', '/', '-']:
        if sep in date_str:
            parts = date_str.split(sep)
            # Filter out empty parts that might result from trailing separators
            parts = [part.strip() for part in parts if part.strip()]
            if len(parts) == 3:
                day, month, year = parts
                # Ensure day and month are 2 digits, year is 4 digits
                try:
                    day = str(int(day)).zfill(2)
                    month = str(int(month)).zfill(2)
                    year = str(int(year))
                    # Handle 2-digit years (assume 1900s or 2000s)
                    if len(year) == 2:
                        year_int = int(year)
                        if year_int > 50:  # assume 1950-1999
                            year = f"19{year}"
                        else:  # assume 2000-2049
                            year = f"20{year}"
                    elif len(year) == 4:
                        pass  # year is already 4 digits
                    else:
                        return date_str  # invalid year format
                    
                    return f"{day}.{month}.{year}"
                except ValueError:
                    return date_str  # invalid date components
            break
    
    return date_str  # return original if no separator found

df['DatumRođenja'] = df['DatumRođenja'].apply(normalize_date)

# save cleaned csv
df.to_csv('data/cleaned_' + filename, index=False)