import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from backend import analyze_dataframe

# Page configuration
st.set_page_config(
    page_title="AI Data Analyst",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .main-header h1 {
        color: white;
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }
    .main-header p {
        color: white;
        font-size: 1.2rem;
        opacity: 0.9;
    }
    .stat-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
        width: 100%;
    }
    .stButton button:hover {
        transform: translateY(-2px);
        transition: 0.3s;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="main-header">
        <h1>AI Data Analyst</h1>
        <p>Turn Any Data Into Insights Instantly</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("## Analysis Features")
    st.markdown("""
    - Auto Data Cleaning
    - Missing Value Detection
    - Statistical Analysis
    - Column-wise Statistics
    - Download Cleaned Data
    """)
    
    st.markdown("---")
    st.markdown("## Supported Formats")
    st.markdown("""
    - CSV Files
    - Excel Files (xlsx, xls)
    - JSON Files
    """)
    
    st.markdown("---")
    st.markdown("## How It Works")
    st.markdown("""
    1. Upload your file
    2. AI detects data types
    3. Auto-fills missing values
    4. Generates statistics
    5. Download cleaned data
    """)
    
    st.markdown("---")
    st.markdown("### Data Cleaning Rules")
    st.markdown("""
    - **Numeric columns**: Filled with mean
    - **Year columns**: Filled with median
    - **Text columns**: Filled with 'unknown'
    """)

# File upload section
st.markdown("## Upload Your Data File")

uploaded_file = st.file_uploader(
    "Choose a file",
    type=['csv', 'xlsx', 'xls', 'json'],
    help="Supported formats: CSV, Excel, JSON"
)

if uploaded_file is not None:
    # Read file based on extension
    file_extension = uploaded_file.name.split('.')[-1].lower()
    
    with st.spinner('Reading file...'):
        if file_extension == 'csv':
            df = pd.read_csv(uploaded_file)
        elif file_extension in ['xlsx', 'xls']:
            df = pd.read_excel(uploaded_file)
        elif file_extension == 'json':
            df = pd.read_json(uploaded_file)
        else:
            st.error("Unsupported file format")
            st.stop()
    
    # Display basic info
    st.markdown("## File Information")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="stat-box">', unsafe_allow_html=True)
        st.metric("Total Rows", len(df), delta=None)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="stat-box">', unsafe_allow_html=True)
        st.metric("Total Columns", len(df.columns), delta=None)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="stat-box">', unsafe_allow_html=True)
        st.metric("Missing Values", df.isnull().sum().sum(), delta=None)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="stat-box">', unsafe_allow_html=True)
        st.metric("Data Types", len(df.dtypes.unique()), delta=None)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Show missing values before cleaning
    missing_before_df = pd.DataFrame({
        'Column': df.columns,
        'Data Type': df.dtypes.values,
        'Missing Values': df.isnull().sum().values,
        'Missing Percentage': (df.isnull().sum().values / len(df)) * 100
    })
    missing_before_df = missing_before_df[missing_before_df['Missing Values'] > 0]
    
    if not missing_before_df.empty:
        st.markdown("## Missing Values Detected")
        st.dataframe(missing_before_df, use_container_width=True)
        
        # Create bar chart for missing values
        fig = px.bar(
            missing_before_df,
            x='Column',
            y='Missing Values',
            title='Missing Values by Column',
            color='Missing Values',
            color_continuous_scale='reds'
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.success("No missing values found in your data")
    
    # Show data preview
    with st.expander("View Original Data Preview"):
        st.dataframe(df.head(20), use_container_width=True)
    
    # Analyze button
    st.markdown("---")
    st.markdown("## Data Analysis & Cleaning")
    
    if st.button("Analyze Data", use_container_width=True):
        with st.spinner('AI is analyzing your data...'):
            # Call backend analysis function
            result = analyze_dataframe(df)
            
            cleaned_df = result['cleaned_df']
            statistics = result['statistics']
            
            # Show success message
            st.success(f"Analysis Complete! Fixed {result['missing_before'] - result['missing_after']} missing values")
            
            # Display statistics table for each column
            st.markdown("## Column Statistics")
            st.markdown("Basic statistics for each column in your dataset")
            
            # Create statistics display for each column
            for col_name, stats in statistics.items():
                with st.expander(f"Column: {col_name} (Type: {stats['type']})"):
                    if stats['type'] == 'numeric':
                        # Create statistics dataframe for numeric column
                        stats_df = pd.DataFrame({
                            'Statistic': ['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max'],
                            'Value': [
                                stats['count'],
                                f"{stats['mean']:.2f}",
                                f"{stats['std']:.2f}",
                                f"{stats['min']:.2f}",
                                f"{stats['25%']:.2f}",
                                f"{stats['50%']:.2f}",
                                f"{stats['75%']:.2f}",
                                f"{stats['max']:.2f}"
                            ]
                        })
                        st.dataframe(stats_df, use_container_width=True)
                        
                        # Create histogram for numeric column
                        fig = px.histogram(
                            cleaned_df,
                            x=col_name,
                            title=f"Distribution of {col_name}",
                            color_discrete_sequence=['#667eea']
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        # Create statistics dataframe for text column
                        stats_df = pd.DataFrame({
                            'Statistic': ['count', 'unique', 'most_common'],
                            'Value': [
                                stats['count'],
                                stats['unique'],
                                stats['most_common']
                            ]
                        })
                        st.dataframe(stats_df, use_container_width=True)
                        
                        # Show top values for text column
                        top_values = cleaned_df[col_name].value_counts().head(10)
                        if len(top_values) > 0:
                            fig = px.bar(
                                x=top_values.values,
                                y=top_values.index,
                                orientation='h',
                                title=f"Top 10 Values in {col_name}",
                                color_discrete_sequence=['#764ba2']
                            )
                            fig.update_layout(xaxis_title="Count", yaxis_title="Value")
                            st.plotly_chart(fig, use_container_width=True)
            
            # Show cleaned data preview
            st.markdown("## Cleaned Data Preview")
            st.dataframe(cleaned_df.head(20), use_container_width=True)
            
            # Download section
            st.markdown("## Download Cleaned Data")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Download as CSV
                csv_data = cleaned_df.to_csv(index=False)
                st.download_button(
                    label="Download as CSV",
                    data=csv_data,
                    file_name="cleaned_data.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            with col2:
                # Download as Excel
                import io
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    cleaned_df.to_excel(writer, sheet_name='Cleaned Data', index=False)
                excel_data = output.getvalue()
                st.download_button(
                    label="Download as Excel",
                    data=excel_data,
                    file_name="cleaned_data.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
            
            # Summary statistics
            st.markdown("## Analysis Summary")
            summary_df = pd.DataFrame({
                'Metric': ['Total Rows', 'Total Columns', 'Missing Values Before', 'Missing Values After', 'Values Fixed'],
                'Value': [
                    result['rows'],
                    result['columns'],
                    result['missing_before'],
                    result['missing_after'],
                    result['missing_before'] - result['missing_after']
                ]
            })
            st.dataframe(summary_df, use_container_width=True)

else:
    # Show info when no file uploaded
    st.info("Please upload a CSV, Excel, or JSON file to begin analysis")
    
    # Sample data option
    st.markdown("---")
    st.markdown("## Try with Sample Data")
    
    sample_file = st.file_uploader("Or upload a sample file", type=['csv'], key="sample")
    if sample_file is not None:
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: gray; padding: 2rem;">
        AI Data Analyst | Powered by Streamlit, Pandas & Plotly | Auto Data Cleaning Enabled
    </div>
""", unsafe_allow_html=True)
