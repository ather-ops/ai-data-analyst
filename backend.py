import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set style
sns.set_theme(style="whitegrid")
primary_green = "#2ECC71"
secondary_green = "#27AE60"
dark_slate = "#2C3E50"

def clean_column_types(df):
    """Convert columns to proper types (numeric or text)"""
    df = df.copy()
    
    for col in df.columns:
        # First try to convert to numeric (text like "123" becomes 123)
        converted = pd.to_numeric(df[col], errors='coerce')
        
        # Check if more than 50% values became numeric after conversion
        numeric_ratio = converted.notna().sum() / len(df)
        
        if numeric_ratio > 0.5:
            # Column is mostly numeric, keep as numeric
            df[col] = converted
        else:
            # Column is mostly text, keep as text but fill NaN with "unknown"
            df[col] = df[col].fillna("unknown")
            # Convert any numeric values that look like numbers to string
            df[col] = df[col].astype(str)
    
    return df

def analysis(df):
    """Fill missing values in dataframe"""
    # First clean column types
    df = clean_column_types(df)
    
    for col in df.columns:
        if df[col].dtype in ['int64', 'float64']:
            # Numeric column - fill missing values
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
            # Text column - fill with "unknown"
            df[col] = df[col].fillna("unknown")
    
    return df

def graph_1_pie(df):
    """Graph 1: Distribution pie plot (Movies vs TV shows)"""
    fig, ax = plt.subplots(figsize=(8,6))
    type_counts = df["type"].value_counts()
    ax.pie(type_counts.values, labels=type_counts.index, autopct='%1.1f%%')
    ax.set_title("Content Type: Movies vs TV shows", fontweight="bold", color=dark_slate)
    return fig

def graph_2_bar_top_countries(df):
    """Graph 2: Top 10 content producing countries"""
    fig, ax = plt.subplots(figsize=(10,6))
    # Filter out "unknown" values
    country_data = df[df["country"] != "unknown"]["country"].value_counts().head(10)
    sns.barplot(x=country_data.values, y=country_data.index, palette="Greens", ax=ax)
    ax.set_title('Top 10 Content-Producing Countries', fontweight='bold', color=dark_slate)
    ax.set_xlabel('Number of Titles')
    return fig

def graph_3_genre_bar(df):
    """Graph 3: Top 10 most popular genres"""
    fig, ax = plt.subplots(figsize=(10,6))
    genres = df["listed_in"].str.split(',').explode()
    genre_counts = genres.value_counts().head(10)
    sns.barplot(x=genre_counts.values, y=genre_counts.index, color=secondary_green, ax=ax)
    ax.set_title('Top 10 Most Popular Genres', fontweight='bold', color=dark_slate)
    ax.set_xlabel('Count')
    return fig

def graph_4_time_series(df):
    """Graph 4: Content release growth over years"""
    fig, ax = plt.subplots(figsize=(12, 6))
    yearly_counts = df.groupby('release_year')['show_id'].count().reset_index()
    sns.lineplot(data=yearly_counts, x='release_year', y='show_id', marker='o', 
                 color=primary_green, linewidth=3, ax=ax)
    ax.fill_between(yearly_counts['release_year'], yearly_counts['show_id'], 
                    color=primary_green, alpha=0.15)
    ax.set_title('Content Release Growth Over the Years', fontweight='bold', color=dark_slate)
    ax.set_xlabel('Year')
    ax.set_ylabel('Total Titles')
    return fig

def graph_5_rating_plot(df):
    """Graph 5: Audience rating distribution"""
    fig, ax = plt.subplots(figsize=(10, 6))
    rating_order = df['rating'].value_counts().index
    sns.countplot(data=df, x='rating', order=rating_order, color=primary_green, ax=ax)
    ax.set_title('Audience Segment Distribution', fontweight='bold', color=dark_slate)
    ax.set_xlabel('Rating Category')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    return fig

def generate_all_graphs(df):
    """Generate all 5 graphs"""
    graphs = []
    graphs.append(graph_1_pie(df))
    graphs.append(graph_2_bar_top_countries(df))
    graphs.append(graph_3_genre_bar(df))
    graphs.append(graph_4_time_series(df))
    graphs.append(graph_5_rating_plot(df))
    return graphs

def analyze_dataframe(df):
    """Complete analysis pipeline"""
    missing_before = df.isnull().sum().sum()
    cleaned_df = analysis(df.copy())
    missing_after = cleaned_df.isnull().sum().sum()
    
    return {
        'cleaned_df': cleaned_df,
        'missing_before': int(missing_before),
        'missing_after': int(missing_after),
        'rows': int(len(cleaned_df)),
        'columns': int(len(cleaned_df.columns)),
        'fixed_values': int(missing_before - missing_after),
        'graphs': generate_all_graphs(cleaned_df)
    }
