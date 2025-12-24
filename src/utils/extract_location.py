import pandas as pd
import re

def extract_province_from_address(address):
    if pd.isna(address) or address == '':
        return None
    
    address_str = str(address)
    parts = address_str.split(',')
    
    if len(parts) > 0:
        last_part = parts[-1].strip()
        return last_part
    
    return None

def get_unique_provinces(df, address_col='Address'):
    if address_col not in df.columns:
        return []
    
    provinces = df[address_col].apply(extract_province_from_address)
    unique_provinces = sorted(provinces.dropna().unique().tolist())
    return unique_provinces

