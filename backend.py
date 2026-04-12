import pandas as pd
import numpy as np

def analysis(df):
    """
    Main analysis function to fill missing values
    Automatically converts numeric columns and fills based on type
    """
    # Make a copy to avoid warnings
    df = df.copy()
    
    # First convert all columns to appropriate types
    for col in df.columns:
        try:
            # Try to convert to numeric
            df[col] = pd.to_numeric(df[col], errors='ignore')
        except:
            # If conversion fails, keep as is
            pass
    
    # Fill missing values based on column type
    for col in df.columns:
        try:
            if df[col].dtype in ['int64', 'float64']:
                # Agar column 'year' hai, toh mean nahi, median use karo
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
            else:
                df[col] = df[col].fillna("unknown")
        except:
            # If any error occurs, fill with unknown
            df[col] = df[col].fillna("unknown")
    
    return df

def get_statistics(df):
    """
    Generate statistics for each column in the dataframe
    Returns dictionary with column statistics
    """
    statistics = {}
    
    for col in df.columns:
        try:
            if df[col].dtype in ['int64', 'float64']:
                # Numeric column statistics
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
                statistics[col] = {
                    'type': 'text',
                    'count': int(df[col].count()) if not pd.isna(df[col].count()) else 0,
                    'unique': int(df[col].nunique()) if not pd.isna(df[col].nunique()) else 0,
                    'most_common': str(df[col].mode().iloc[0]) if len(df[col].mode()) > 0 else 'none'
                }
        except:
            # If any error occurs, return basic info
            statistics[col] = {
                'type': 'unknown',
                'count': 0,
                'error': 'Could not process this column'
            }
    
    return statistics

def analyze_dataframe(df):
    """
    Complete analysis pipeline
    Returns cleaned dataframe and statistics
    """
    # Store original missing count
    missing_before = df.isnull().sum().sum()
    
    # Make a copy to avoid modifying original
    cleaned_df = df.copy()
    
    # Apply analysis to clean the data
    cleaned_df = analysis(cleaned_df)
    
    # Calculate missing after cleaning
    missing_after = cleaned_df.isnull().sum().sum()
    
    # Get statistics for each column
    statistics = get_statistics(cleaned_df)
    
    # Return all results
    return {
        'cleaned_df': cleaned_df,
        'statistics': statistics,
        'missing_before': int(missing_before),
        'missing_after': int(missing_after),
        'rows': int(len(cleaned_df)),
        'columns': int(len(cleaned_df.columns)),
        'fixed_values': int(missing_before - missing_after)
    }
