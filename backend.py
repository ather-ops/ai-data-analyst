import pandas as pd
import numpy as np
import re

def analysis(df):
    """Fill missing values in dataframe"""
    df = df.copy()
    
    for col in df.columns:
        # Check if column should be numeric (based on column name)
        if col == 'release_year' or 'year' in col.lower():
            # Convert to numeric
            df[col] = pd.to_numeric(df[col], errors='coerce')
            # Fill with median (better for years)
            median_val = df[col].median()
            if pd.isna(median_val):
                median_val = 0
            df[col] = df[col].fillna(median_val)
            df[col] = df[col].astype(int)
        else:
            # All other columns are text - fill with "unknown"
            df[col] = df[col].fillna("unknown")
            df[col] = df[col].replace([0, "0", "nan", "NaN"], "unknown")
    
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
                    'count': int(stats['count']),
                    'mean': float(stats['mean']),
                    'std': float(stats['std']),
                    'min': float(stats['min']),
                    '25%': float(stats['25%']),
                    '50%': float(stats['50%']),
                    '75%': float(stats['75%']),
                    'max': float(stats['max'])
                }
            else:
                statistics[col] = {
                    'type': 'text',
                    'count': int(df[col].count()),
                    'unique': int(df[col].nunique()),
                    'most_common': str(df[col].mode().iloc[0]) if len(df[col].mode()) > 0 else 'none'
                }
        except:
            statistics[col] = {'type': 'unknown', 'count': 0}
    
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
