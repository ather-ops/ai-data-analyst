import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from backend import analyze_dataframe
import io
import time

# Page configuration
st.set_page_config(
    page_title="AI Data Analyst",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with Liquid Glass effect
st.markdown("""
    <style>
    /* Import */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Main container */
    .stApp {
        background: radial-gradient(circle at 20% 50%, rgba(10, 20, 40, 0.98), rgba(5, 10, 20, 0.99));
        font-family: 'Inter', sans-serif;
    }
    
    /* Liquid Glass effect */
    .glass-panel {
        background: rgba(20, 30, 45, 0.35);
        backdrop-filter: blur(12px);
        border-radius: 24px;
        border: 1px solid rgba(80, 120, 200, 0.25);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .glass-panel:hover {
        border-color: rgba(80, 120, 200, 0.5);
        box-shadow: 0 12px 48px 0 rgba(0, 0, 0, 0.3);
        background: rgba(25, 40, 60, 0.45);
    }
    
    /* Header */
    .header-container {
        text-align: center;
        padding: 2.5rem;
        background: linear-gradient(135deg, rgba(30, 50, 80, 0.4), rgba(20, 35, 60, 0.4));
        backdrop-filter: blur(12px);
        border-radius: 28px;
        border: 1px solid rgba(80, 120, 200, 0.3);
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    }
    
    .header-container h1 {
        color: #ffffff;
        font-size: 2.8rem;
        font-weight: 600;
        letter-spacing: -0.02em;
        background: linear-gradient(135deg, #ffffff, #a0b8e0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .header-container p {
        color: rgba(180, 200, 240, 0.85);
        font-size: 1.1rem;
        font-weight: 400;
    }
    
    /* Stat boxes */
    .stat-card {
        background: rgba(25, 35, 55, 0.4);
        backdrop-filter: blur(8px);
        padding: 1.2rem;
        border-radius: 18px;
        border: 1px solid rgba(80, 120, 200, 0.2);
        text-align: center;
        transition: transform 0.2s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-2px);
        border-color: rgba(80, 120, 200, 0.4);
        background: rgba(30, 45, 70, 0.5);
    }
    
    /* Button */
    .stButton > button {
        background: linear-gradient(135deg, rgba(40, 70, 120, 0.8), rgba(30, 55, 100, 0.8));
        backdrop-filter: blur(8px);
        color: white;
        font-weight: 500;
        border: 1px solid rgba(80, 120, 200, 0.4);
        border-radius: 12px;
        padding: 0.6rem 1.2rem;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, rgba(50, 85, 140, 0.9), rgba(40, 70, 120, 0.9));
        border-color: rgba(100, 150, 230, 0.6);
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        color: white !important;
        font-size: 1.8rem !important;
        font-weight: 600 !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: rgba(180, 200, 240, 0.8) !important;
        font-size: 0.85rem !important;
    }
    
    /* Dataframe */
    .dataframe {
        background: rgba(15, 25, 40, 0.6) !important;
        backdrop-filter: blur(4px) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(80, 120, 200, 0.2) !important;
        color: #e0e8f0 !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(25, 40, 65, 0.5) !important;
        backdrop-filter: blur(8px);
        border-radius: 12px !important;
        border: 1px solid rgba(80, 120, 200, 0.2);
        color: white !important;
        font-weight: 500;
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(35, 55, 85, 0.6) !important;
        border-color: rgba(80, 120, 200, 0.4);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: rgba(20, 30, 50, 0.4);
        backdrop-filter: blur(8px);
        border-radius: 12px;
        padding: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: rgba(200, 215, 240, 0.8);
        border-radius: 8px;
        padding: 0.4rem 1rem;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(40, 80, 140, 0.8), rgba(30, 65, 120, 0.8));
        color: white;
    }
    
    /* Alert boxes */
    .stAlert {
        background: rgba(25, 40, 65, 0.5) !important;
        backdrop-filter: blur(8px);
        border: 1px solid rgba(80, 120, 200, 0.3) !important;
        border-radius: 12px !important;
        color: white !important;
    }
    
    /* Loading animation */
    .loading-wave {
        display: inline-block;
        position: relative;
        width: 80px;
        height: 80px;
    }
    
    .loading-wave div {
        position: absolute;
        border: 4px solid rgba(80, 120, 200, 0.8);
        opacity: 1;
        border-radius: 50%;
        animation: ripple 1.5s cubic-bezier(0, 0.2, 0.8, 1) infinite;
    }
    
    .loading-wave div:nth-child(2) {
        animation-delay: -0.5s;
    }
    
    @keyframes ripple {
        0% { top: 36px; left: 36px; width: 0; height: 0; opacity: 1; }
        100% { top: 0px; left: 0px; width: 72px; height: 72px; opacity: 0; }
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: rgba(10, 20, 35, 0.6);
        backdrop-filter: blur(12px);
        border-right: 1px solid rgba(80, 120, 200, 0.2);
    }
    
    /* Code blocks */
    .stCodeBlock {
        background: rgba(0, 0, 0, 0.3) !important;
        border-radius: 10px !important;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(20, 30, 50, 0.5);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(80, 120, 200, 0.5);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(80, 120, 200, 0.7);
    }
    
    /* Dividers */
    hr {
        border-color: rgba(80, 120, 200, 0.2);
        margin: 1.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Loading component
def show_loading():
    loading_placeholder = st.empty()
    loading_placeholder.markdown("""
        <div style="text-align: center; padding: 3rem;">
            <div style="background: rgba(20, 30, 50, 0.5); backdrop-filter: blur(12px); border-radius: 24px; padding: 2rem; border: 1px solid rgba(80, 120, 200, 0.3);">
                <div class="loading-wave">
                    <div></div>
                    <div></div>
                </div>
                <p style="color: rgba(200, 215, 240, 0.9); margin-top: 1.5rem; font-size: 1rem;">Processing data</p>
                <p style="color: rgba(160, 180, 220, 0.6); font-size: 0.85rem; margin-top: 0.5rem;">AI analysis in progress</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    time.sleep(1.5)
    loading_placeholder.empty()

# Header
st.markdown("""
    <div class="header-container">
        <h1>AI Data Analyst</h1>
        <p>Intelligent data processing and analysis platform</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("""
        <div style="padding: 1rem 0;">
            <h3 style="color: white; font-weight: 500; margin-bottom: 1rem;">Analysis Suite</h3>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    - Data profiling
    - Missing value treatment
    - Statistical analysis
    - Column insights
    - Export capabilities
    """)
    
    st.markdown("---")
    
    st.markdown("""
        <div style="margin-top: 1rem;">
            <h4 style="color: white; font-weight: 500;">Supported formats</h4>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    - CSV
    - Excel (xlsx, xls)
    - JSON
    - Parquet
    """)
    
    st.markdown("---")
    
    st.markdown("""
        <div style="margin-top: 1rem;">
            <h4 style="color: white; font-weight: 500;">Processing pipeline</h4>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    1. File validation
    2. Structure analysis
    3. Missing data detection
    4. Automated cleaning
    5. Statistical computation
    6. Results export
    """)
    
    st.markdown("---")
    
    st.markdown("""
        <div style="margin-top: 1rem;">
            <h4 style="color: white; font-weight: 500;">Cleaning rules</h4>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    - Numeric columns: mean imputation
    - Temporal data: median fill
    - Categorical: mode replacement
    - Text fields: standard values
    """)

# File upload
st.markdown("""
    <div class="glass-panel" style="padding: 1.5rem; margin-bottom: 1.5rem;">
        <h3 style="color: white; font-weight: 500; margin-bottom: 1rem;">Data source</h3>
    </div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Select file",
    type=['csv', 'xlsx', 'xls', 'json', 'parquet'],
    help="CSV, Excel, JSON, or Parquet format"
)

if uploaded_file is not None:
    # Read file
    file_extension = uploaded_file.name.split('.')[-1].lower()
    
    with st.spinner('Loading file...'):
        if file_extension == 'csv':
            df = pd.read_csv(uploaded_file)
        elif file_extension in ['xlsx', 'xls']:
            df = pd.read_excel(uploaded_file)
        elif file_extension == 'json':
            df = pd.read_json(uploaded_file)
        elif file_extension == 'parquet':
            df = pd.read_parquet(uploaded_file)
        else:
            st.error("Unsupported format")
            st.stop()
    
    # File information
    st.markdown("""
        <div class="glass-panel" style="padding: 1.5rem; margin-bottom: 1.5rem;">
            <h3 style="color: white; font-weight: 500; margin-bottom: 1rem;">Dataset overview</h3>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="stat-card">', unsafe_allow_html=True)
        st.metric("Rows", f"{len(df):,}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="stat-card">', unsafe_allow_html=True)
        st.metric("Columns", len(df.columns))
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="stat-card">', unsafe_allow_html=True)
        missing_count = df.isnull().sum().sum()
        st.metric("Missing values", f"{missing_count:,}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="stat-card">', unsafe_allow_html=True)
        st.metric("Data types", len(df.dtypes.unique()))
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Quality metrics
    completeness = ((len(df) - missing_count) / (len(df) * len(df.columns))) * 100
    duplicates = df.duplicated().sum()
    memory_mb = df.memory_usage(deep=True).sum() / 1024**2
    
    qual_col1, qual_col2, qual_col3 = st.columns(3)
    with qual_col1:
        st.metric("Data completeness", f"{completeness:.1f}%")
    with qual_col2:
        st.metric("Duplicate rows", f"{duplicates:,}")
    with qual_col3:
        st.metric("Memory usage", f"{memory_mb:.2f} MB")
    
    # Missing values report
    missing_df = pd.DataFrame({
        'Column': df.columns,
        'Type': df.dtypes.values,
        'Missing': df.isnull().sum().values,
        'Percentage': (df.isnull().sum().values / len(df)) * 100
    })
    missing_df = missing_df[missing_df['Missing'] > 0]
    
    if not missing_df.empty:
        st.markdown("""
            <div class="glass-panel" style="padding: 1.5rem; margin: 1rem 0;">
                <h4 style="color: white; font-weight: 500;">Missing values detected</h4>
            </div>
        """, unsafe_allow_html=True)
        st.dataframe(missing_df, use_container_width=True)
        
        fig = px.bar(
            missing_df,
            x='Column',
            y='Missing',
            title='Missing values by column',
            color='Missing',
            color_continuous_scale='Blues',
            template='plotly_dark'
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.success("No missing values found")
    
    # Data preview
    with st.expander("View data sample"):
        st.dataframe(df.head(20), use_container_width=True)
    
    # Analysis button
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        analyze = st.button("Run analysis", use_container_width=True)
    
    if analyze:
        show_loading()
        
        with st.spinner('Processing...'):
            result = analyze_dataframe(df)
            cleaned_df = result['cleaned_df']
            statistics = result['statistics']
            
            st.success(f"Analysis complete | Fixed {result['missing_before'] - result['missing_after']:,} missing values")
            
            # Results tabs
            tab_stats, tab_viz, tab_clean, tab_export = st.tabs([
                "Statistics", "Visualizations", "Cleaned data", "Export"
            ])
            
            with tab_stats:
                st.markdown("""
                    <div class="glass-panel" style="padding: 1rem; margin-bottom: 1rem;">
                        <h4 style="color: white;">Column analysis</h4>
                    </div>
                """, unsafe_allow_html=True)
                
                for col_name, stats in statistics.items():
                    with st.expander(f"{col_name} ({stats['type']})"):
                        if stats['type'] == 'numeric':
                            stats_table = pd.DataFrame({
                                'Metric': ['Count', 'Mean', 'Std Dev', 'Min', 'Q1', 'Median', 'Q3', 'Max'],
                                'Value': [
                                    f"{stats['count']:,}",
                                    f"{stats['mean']:.2f}",
                                    f"{stats['std']:.2f}",
                                    f"{stats['min']:.2f}",
                                    f"{stats['25%']:.2f}",
                                    f"{stats['50%']:.2f}",
                                    f"{stats['75%']:.2f}",
                                    f"{stats['max']:.2f}"
                                ]
                            })
                            st.dataframe(stats_table, use_container_width=True)
                        else:
                            stats_table = pd.DataFrame({
                                'Metric': ['Count', 'Unique values', 'Most common'],
                                'Value': [
                                    f"{stats['count']:,}",
                                    f"{stats['unique']:,}",
                                    stats['most_common']
                                ]
                            })
                            st.dataframe(stats_table, use_container_width=True)
            
            with tab_viz:
                st.markdown("""
                    <div class="glass-panel" style="padding: 1rem; margin-bottom: 1rem;">
                        <h4 style="color: white;">Data visualizations</h4>
                    </div>
                """, unsafe_allow_html=True)
                
                numeric_cols = cleaned_df.select_dtypes(include=['number']).columns
                
                if len(numeric_cols) > 0:
                    # Distributions
                    for col in numeric_cols[:3]:
                        fig = px.histogram(
                            cleaned_df,
                            x=col,
                            title=f"{col} distribution",
                            nbins=30,
                            template='plotly_dark',
                            color_discrete_sequence=['#3b82f6']
                        )
                        fig.update_layout(
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            font_color='white'
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    
                    # Correlation matrix
                    if len(numeric_cols) > 1:
                        corr = cleaned_df[numeric_cols].corr()
                        fig_corr = go.Figure(data=go.Heatmap(
                            z=corr,
                            x=corr.columns,
                            y=corr.columns,
                            colorscale='Blues',
                            text=corr.round(2),
                            texttemplate='%{text}'
                        ))
                        fig_corr.update_layout(
                            title='Correlation matrix',
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            font_color='white'
                        )
                        st.plotly_chart(fig_corr, use_container_width=True)
            
            with tab_clean:
                st.markdown("""
                    <div class="glass-panel" style="padding: 1rem; margin-bottom: 1rem;">
                        <h4 style="color: white;">Cleaned dataset</h4>
                    </div>
                """, unsafe_allow_html=True)
                st.dataframe(cleaned_df.head(20), use_container_width=True)
                st.caption(f"Shape: {cleaned_df.shape[0]} rows, {cleaned_df.shape[1]} columns")
            
            with tab_export:
                st.markdown("""
                    <div class="glass-panel" style="padding: 1rem; margin-bottom: 1rem;">
                        <h4 style="color: white;">Export options</h4>
                    </div>
                """, unsafe_allow_html=True)
                
                col_a, col_b = st.columns(2)
                
                with col_a:
                    csv_data = cleaned_df.to_csv(index=False)
                    st.download_button(
                        label="CSV format",
                        data=csv_data,
                        file_name="cleaned_data.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
                
                with col_b:
                    output = io.BytesIO()
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        cleaned_df.to_excel(writer, sheet_name='Cleaned Data', index=False)
                    st.download_button(
                        label="Excel format",
                        data=output.getvalue(),
                        file_name="cleaned_data.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
            
            # Summary
            st.markdown("""
                <div class="glass-panel" style="padding: 1rem; margin-top: 1rem;">
                    <h4 style="color: white;">Analysis summary</h4>
                </div>
            """, unsafe_allow_html=True)
            
            summary_data = pd.DataFrame({
                'Metric': ['Total rows', 'Total columns', 'Missing before', 'Missing after', 'Values fixed'],
                'Value': [
                    f"{result['rows']:,}",
                    f"{result['columns']:,}",
                    f"{result['missing_before']:,}",
                    f"{result['missing_after']:,}",
                    f"{result['missing_before'] - result['missing_after']:,}"
                ]
            })
            st.dataframe(summary_data, use_container_width=True)

else:
    st.markdown("""
        <div class="glass-panel" style="padding: 2rem; text-align: center;">
            <p style="color: rgba(200, 215, 240, 0.8); font-size: 1rem;">Upload a CSV, Excel, JSON, or Parquet file to begin analysis</p>
            <p style="color: rgba(160, 180, 220, 0.5); font-size: 0.85rem; margin-top: 0.5rem;">The system will automatically detect data types and suggest cleaning strategies</p>
        </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; padding: 1rem;">
        <p style="color: rgba(160, 180, 220, 0.5); font-size: 0.8rem;">AI Data Analyst | Automated processing pipeline</p>
    </div>
""", unsafe_allow_html=True)
