import pandas as pd
import numpy as np

def analyze_dataframe(df):
    """
    Pure backend logic for data analysis
    Returns: cleaned_df, statistics_dict
    """
    # Store original missing values count
    missing_before = df.isnull().sum().sum()
    
    # Create a copy to avoid modifying original
    cleaned_df = df.copy()
    
    # Analysis function to fill missing values
    for col in cleaned_df.columns:
        if cleaned_df[col].dtype in ['int64', 'float64']:
            # For year columns, use median instead of mean
            if 'year' in col.lower():
                cleaned_df[col] = cleaned_df[col].fillna(cleaned_df[col].median())
            else:
                cleaned_df[col] = cleaned_df[col].fillna(cleaned_df[col].mean())
        else:
            cleaned_df[col] = cleaned_df[col].fillna("unknown")
    
    # Calculate missing values after
    missing_after = cleaned_df.isnull().sum().sum()
    
    # Generate statistics for each column
    statistics = {}
    for col in cleaned_df.columns:
        if cleaned_df[col].dtype in ['int64', 'float64']:
            # Numeric column statistics
            statistics[col] = {
                'type': 'numeric',
                'count': int(cleaned_df[col].count()),
                'mean': float(cleaned_df[col].mean()) if not pd.isna(cleaned_df[col].mean()) else 0,
                'std': float(cleaned_df[col].std()) if not pd.isna(cleaned_df[col].std()) else 0,
                'min': float(cleaned_df[col].min()) if not pd.isna(cleaned_df[col].min()) else 0,
                '25%': float(cleaned_df[col].quantile(0.25)) if not pd.isna(cleaned_df[col].quantile(0.25)) else 0,
                '50%': float(cleaned_df[col].quantile(0.50)) if not pd.isna(cleaned_df[col].quantile(0.50)) else 0,
                '75%': float(cleaned_df[col].quantile(0.75)) if not pd.isna(cleaned_df[col].quantile(0.75)) else 0,
                'max': float(cleaned_df[col].max()) if not pd.isna(cleaned_df[col].max()) else 0
            }
        else:
            # Text column statistics
            statistics[col] = {
                'type': 'text',
                'count': int(cleaned_df[col].count()),
                'unique': int(cleaned_df[col].nunique()),
                'most_common': str(cleaned_df[col].mode().iloc[0]) if len(cleaned_df[col].mode()) > 0 else 'none'
            }
    
    return {
        'cleaned_df': cleaned_df,
        'statistics': statistics,
        'missing_before': missing_before,
        'missing_after': missing_after,
        'rows': len(cleaned_df),
        'columns': len(cleaned_df.columns)
    }
