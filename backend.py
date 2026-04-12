import pandas as pd
import numpy as np
import re

def convert_to_numeric(val):
    """Convert string numbers like 'two hundred' to actual numbers"""
    if pd.isna(val) or val == "NaN" or val == "unknown" or val == "":
        return np.nan
    
    if isinstance(val, (int, float)):
        return val
    
    if isinstance(val, str):
        # Remove extra spaces and lowercase
        val = val.lower().strip()
        
        # Handle common text numbers
        word_to_num = {
            'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4,
            'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9,
            'ten': 10, 'eleven': 11, 'twelve': 12, 'thirteen': 13,
            'fourteen': 14, 'fifteen': 15, 'sixteen': 16, 'seventeen': 17,
            'eighteen': 18, 'nineteen': 19, 'twenty': 20, 'thirty': 30,
            'forty': 40, 'fifty': 50, 'sixty': 60, 'seventy': 70,
            'eighty': 80, 'ninety': 90, 'hundred': 100, 'thousand': 1000
        }
        
        # Check if it's a text number like "two hundred"
        words = val.split()
        if len(words) > 1:
            total = 0
            current = 0
            for word in words:
                if word in word_to_num:
                    num = word_to_num[word]
                    if num == 100 or num == 1000:
                        if current == 0:
                            current = 1
                        total += current * num
                        current = 0
                    else:
                        current += num
                else:
                    return np.nan
            total += current
            return total
        
        # Check if it's a single word number
        if val in word_to_num:
            return word_to_num[val]
        
        # Try to extract numbers from string like "123"
        numbers = re.findall(r'\d+', val)
        if numbers:
            return int(numbers[0])
    
    return np.nan

def analysis(df):
    """Fill missing values in dataframe"""
    df = df.copy()
    
    for col in df.columns:
        # Check if column should be numeric (based on column name or content)
        numeric_keywords = ['quantity', 'price', 'year', 'id', 'count', 'amount', 'qty']
        is_numeric_col = any(keyword in col.lower() for keyword in numeric_keywords)
        
        # Try to detect if column contains numeric data
        sample = df[col].dropna().head(10)
        numeric_ratio = 0
        
        if len(sample) > 0:
            # Count how many values can be converted to numbers
            numeric_count = 0
            for val in sample:
                converted = convert_to_numeric(val)
                if not pd.isna(converted):
                    numeric_count += 1
            numeric_ratio = numeric_count / len(sample)
        
        # If column name suggests numeric OR more than 50% values are numeric
        if is_numeric_col or numeric_ratio > 0.5:
            # Convert to numeric
            df[col] = df[col].apply(convert_to_numeric)
            
            # Fill missing values
            if 'year' in col.lower():
                median_val = df[col].median()
                if pd.isna(median_val):
                    median_val = 0
                df[col] = df[col].fillna(median_val)
            else:
                mean_val = df[col].mean()
                if pd.isna(mean_val):
                    mean_val = 0
                df[col] = df[col].fillna(mean_val)
            
            # Convert to int if all values are whole numbers
            if df[col].notna().all() and (df[col].dropna() % 1 == 0).all():
                df[col] = df[col].astype(int)
        else:
            # Text column - keep original values, fill missing with "unknown"
            # Don't convert text to numbers
            df[col] = df[col].fillna("unknown")
            # Clean up any NaN strings
            df[col] = df[col].replace("nan", "unknown")
            df[col] = df[col].replace("NaN", "unknown")
    
    return df

def get_statistics(df):
    """Generate statistics for each column"""
    statistics = {}
    
    for col in df.columns:
        try:
            if df[col].dtype in ['int64', 'float64']:
                stats = df[col].describe()
                statistics[col] = {
                    'type': 'numeric',
                    'count': int(stats['count']) if not pd.isna(stats['count']) else 0,
                    'mean': float(stats['mean']) if not pd.isna(stats['mean']) else 0,
                    'std': float(stats['std']) if not pd.isna(stats['std']) else 0,
                    'min': float(stats['min']) if not pd.isna(stats['min']) else 0,
                    '25%': float(stats['25%']) if not pd.isna(stats['25%']) else 0,
                    '50%': float(stats['50%']) if not pd.isna(stats['50%']) else 0,
                    '75%': float(stats['75%']) if not pd.isna(stats['75%']) else 0,
                    'max': float(stats['max']) if not pd.isna(stats['max']) else 0
                }
            else:
                # Text column statistics
                unique_vals = df[col].nunique()
                most_common = df[col].mode().iloc[0] if len(df[col].mode()) > 0 else 'none'
                statistics[col] = {
                    'type': 'text',
                    'count': int(df[col].count()),
                    'unique': int(unique_vals),
                    'most_common': str(most_common)
                }
        except Exception as e:
            statistics[col] = {
                'type': 'unknown',
                'count': 0,
                'error': str(e)
            }
    
    return statistics

def analyze_dataframe(df):
    """Complete analysis pipeline"""
    missing_before = df.isnull().sum().sum()
    cleaned_df = analysis(df.copy())
    missing_after = cleaned_df.isnull().sum().sum()
    statistics = get_statistics(cleaned_df)
    
    return {
        'cleaned_df': cleaned_df,
        'statistics': statistics,
        'missing_before': int(missing_before),
        'missing_after': int(missing_after),
        'rows': int(len(cleaned_df)),
        'columns': int(len(cleaned_df.columns)),
        'fixed_values': int(missing_before - missing_after)
    }
