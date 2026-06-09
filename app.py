import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from backend import analyze_dataframe
import io
import time

# Page configuration
st.set_page_config(
    page_title="AI Data Analyst Pro",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with Glassmorphism and ChatGPT-inspired theme
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Main container styling */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Glassmorphism effect for cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        background: rgba(255, 255, 255, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    }
    
    /* Animated gradient header */
    .main-header {
        text-align: center;
        padding: 3rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #f5576c 75%, #4facfe 100%);
        background-size: 200% 200%;
        border-radius: 20px;
        margin-bottom: 2rem;
        animation: gradientShift 5s ease infinite;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .main-header h1 {
        color: white;
        font-size: 3.5rem;
        margin-bottom: 0.5rem;
        font-weight: 800;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .main-header p {
        color: white;
        font-size: 1.3rem;
        opacity: 0.95;
    }
    
    /* Stats boxes with glass effect */
    .stat-box {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.2), rgba(118, 75, 162, 0.2));
        backdrop-filter: blur(10px);
        padding: 1.2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
    }
    
    .stat-box:hover {
        transform: scale(1.05);
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.3), rgba(118, 75, 162, 0.3));
    }
    
    /* Button styling with gradient */
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        background-size: 200% 200%;
        color: white;
        font-weight: bold;
        font-size: 1rem;
        padding: 0.75rem;
        border: none;
        border-radius: 10px;
        transition: all 0.3s ease;
        animation: buttonGradient 3s ease infinite;
    }
    
    @keyframes buttonGradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Loading animation */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .loading-text {
        text-align: center;
        color: white;
        font-size: 1.2rem;
        animation: pulse 2s ease-in-out infinite;
    }
    
    /* Dataframe styling */
    .dataframe {
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(5px) !important;
        border-radius: 10px !important;
        color: white !important;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: rgba(0, 0, 0, 0.3) !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* Metric styling */
    [data-testid="stMetricValue"] {
        color: white !important;
        font-size: 2rem !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: rgba(255, 255, 255, 0.8) !important;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(5px) !important;
        color: white !important;
        border-radius: 10px !important;
    }
    
    /* Info/Warning/Success boxes */
    .stAlert {
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        color: white !important;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2, #f093fb);
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea, #764ba2);
    }
    
    /* Code block styling */
    .stCodeBlock {
        background: rgba(0, 0, 0, 0.3) !important;
        border-radius: 10px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Animated loading component
def animated_loading(message="AI is analyzing your data..."):
    loading_placeholder = st.empty()
    dots = 0
    for _ in range(30):
        dots = (dots + 1) % 4
        loading_placeholder.markdown(f"""
            <div style="text-align: center; padding: 2rem;">
                <div class="glass-card">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">🧠</div>
                    <div class="loading-text">{message}{'.' * dots}</div>
                    <div style="margin-top: 1rem;">
                        <div style="width: 100%; height: 2px; background: linear-gradient(90deg, #667eea, #764ba2, #f093fb, #f5576c); border-radius: 2px; animation: gradientShift 2s ease infinite; background-size: 200% 200%;"></div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        time.sleep(0.1)
    loading_placeholder.empty()

# Header
st.markdown("""
    <div class="main-header">
        <h1>✨ AI Data Analyst Pro ✨</h1>
        <p>Your Intelligent Data Companion | Turn Raw Data Into Actionable Insights</p>
        <p style="font-size: 1rem; margin-top: 1rem;">Powered by Advanced Machine Learning Algorithms</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar with glass effect
with st.sidebar:
    st.markdown("""
        <div class="glass-card" style="margin-bottom: 1rem;">
            <h3 style="color: white; margin-bottom: 1rem;">🎯 Advanced Features</h3>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    - 🔍 **Smart Data Profiling**
    - 🧹 **Intelligent Data Cleaning**
    - 📊 **Automated Visualization**
    - 🤖 **AI-Powered Insights**
    - 📈 **Predictive Analytics**
    - 🔄 **Real-time Processing**
    """)
    
    st.markdown("---")
    
    st.markdown("""
        <div class="glass-card">
            <h4 style="color: white;">📁 Supported Formats</h4>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    - CSV Files
    - Excel Files (xlsx, xls)
    - JSON Files
    - Parquet Files
    """)
    
    st.markdown("---")
    
    st.markdown("""
        <div class="glass-card">
            <h4 style="color: white;">⚙️ Processing Pipeline</h4>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    1. **Upload** your file
    2. **Analyze** data structure
    3. **Clean** missing values
    4. **Generate** statistics
    5. **Visualize** insights
    6. **Export** results
    """)
    
    st.markdown("---")
    
    st.markdown("""
        <div class="glass-card">
            <h4 style="color: white;">🎨 Smart Cleaning Rules</h4>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    - **Numeric**: Mean/Median imputation
    - **Categorical**: Mode imputation
    - **DateTime**: Forward fill
    - **Text**: Smart default values
    - **Outlier**: IQR detection
    """)

# File upload section
st.markdown("""
    <div class="glass-card">
        <h2 style="color: white; margin-bottom: 1rem;">📤 Upload Your Data File</h2>
    </div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Choose a file",
    type=['csv', 'xlsx', 'xls', 'json', 'parquet'],
    help="Supported formats: CSV, Excel, JSON, Parquet"
)

if uploaded_file is not None:
    # Read file based on extension
    file_extension = uploaded_file.name.split('.')[-1].lower()
    
    with st.spinner('📂 Reading file...'):
        if file_extension == 'csv':
            df = pd.read_csv(uploaded_file)
        elif file_extension in ['xlsx', 'xls']:
            df = pd.read_excel(uploaded_file)
        elif file_extension == 'json':
            df = pd.read_json(uploaded_file)
        elif file_extension == 'parquet':
            df = pd.read_parquet(uploaded_file)
        else:
            st.error("Unsupported file format")
            st.stop()
    
    # Display basic info in glass cards
    st.markdown("""
        <div class="glass-card">
            <h2 style="color: white; margin-bottom: 1rem;">📊 File Information</h2>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="stat-box">', unsafe_allow_html=True)
        st.metric("Total Rows", f"{len(df):,}", delta=None)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="stat-box">', unsafe_allow_html=True)
        st.metric("Total Columns", len(df.columns), delta=None)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="stat-box">', unsafe_allow_html=True)
        missing_count = df.isnull().sum().sum()
        st.metric("Missing Values", f"{missing_count:,}", delta=None)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="stat-box">', unsafe_allow_html=True)
        st.metric("Data Types", len(df.dtypes.unique()), delta=None)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Data quality metrics
    st.markdown("""
        <div class="glass-card">
            <h3 style="color: white;">📈 Data Quality Overview</h3>
        </div>
    """, unsafe_allow_html=True)
    
    quality_col1, quality_col2, quality_col3 = st.columns(3)
    with quality_col1:
        completeness = ((len(df) - missing_count) / (len(df) * len(df.columns))) * 100
        st.metric("Data Completeness", f"{completeness:.1f}%")
    with quality_col2:
        duplicate_count = df.duplicated().sum()
        st.metric("Duplicate Rows", f"{duplicate_count:,}")
    with quality_col3:
        memory_usage = df.memory_usage(deep=True).sum() / 1024**2
        st.metric("Memory Usage", f"{memory_usage:.2f} MB")
    
    # Show missing values before cleaning
    missing_before_df = pd.DataFrame({
        'Column': df.columns,
        'Data Type': df.dtypes.values,
        'Missing Values': df.isnull().sum().values,
        'Missing Percentage': (df.isnull().sum().values / len(df)) * 100
    })
    missing_before_df = missing_before_df[missing_before_df['Missing Values'] > 0]
    
    if not missing_before_df.empty:
        st.markdown("""
            <div class="glass-card">
                <h3 style="color: white;">⚠️ Missing Values Detected</h3>
            </div>
        """, unsafe_allow_html=True)
        st.dataframe(missing_before_df, use_container_width=True)
        
        # Create interactive bar chart for missing values
        fig = px.bar(
            missing_before_df,
            x='Column',
            y='Missing Values',
            title='Missing Values by Column',
            color='Missing Values',
            color_continuous_scale='Viridis',
            template='plotly_dark'
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.success("🎉 No missing values found in your data! Your dataset is clean!")
    
    # Show data preview with tabs
    st.markdown("""
        <div class="glass-card">
            <h3 style="color: white;">🔍 Data Preview</h3>
        </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📋 Data Sample", "📊 Statistical Summary", "🔢 Data Types"])
    
    with tab1:
        st.dataframe(df.head(20), use_container_width=True)
    
    with tab2:
        st.dataframe(df.describe(), use_container_width=True)
    
    with tab3:
        dtype_df = pd.DataFrame({
            'Column Name': df.columns,
            'Data Type': df.dtypes.astype(str),
            'Unique Values': [df[col].nunique() for col in df.columns]
        })
        st.dataframe(dtype_df, use_container_width=True)
    
    # Analyze button
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        analyze_button = st.button("🚀 Start AI Analysis", use_container_width=True)
    
    if analyze_button:
        # Animated loading
        animated_loading("AI is analyzing your data...")
        
        with st.spinner('🔄 Processing data...'):
            # Call backend analysis function
            result = analyze_dataframe(df)
            
            cleaned_df = result['cleaned_df']
            statistics = result['statistics']
            
            # Show success message with confetti effect
            st.balloons()
            st.success(f"✨ Analysis Complete! Successfully fixed {result['missing_before'] - result['missing_after']:,} missing values ✨")
            
            # Create tabs for different analysis views
            analysis_tab1, analysis_tab2, analysis_tab3, analysis_tab4 = st.tabs([
                "📊 Column Statistics", 
                "📈 Visualizations", 
                "🧹 Cleaned Data",
                "💾 Export Options"
            ])
            
            with analysis_tab1:
                st.markdown("""
                    <div class="glass-card">
                        <h4 style="color: white;">Detailed Column Analysis</h4>
                    </div>
                """, unsafe_allow_html=True)
                
                # Create statistics display for each column
                for col_name, stats in statistics.items():
                    with st.expander(f"📊 Column: {col_name} (Type: {stats['type']})"):
                        if stats['type'] == 'numeric':
                            # Create statistics dataframe for numeric column
                            stats_df = pd.DataFrame({
                                'Statistic': ['Count', 'Mean', 'Std Dev', 'Min', '25%', 'Median', '75%', 'Max', 'Range'],
                                'Value': [
                                    f"{stats['count']:,}",
                                    f"{stats['mean']:.2f}",
                                    f"{stats['std']:.2f}",
                                    f"{stats['min']:.2f}",
                                    f"{stats['25%']:.2f}",
                                    f"{stats['50%']:.2f}",
                                    f"{stats['75%']:.2f}",
                                    f"{stats['max']:.2f}",
                                    f"{stats['max'] - stats['min']:.2f}"
                                ]
                            })
                            st.dataframe(stats_df, use_container_width=True)
                            
                            # Create histogram
                            fig = px.histogram(
                                cleaned_df,
                                x=col_name,
                                title=f"Distribution of {col_name}",
                                color_discrete_sequence=['#667eea'],
                                template='plotly_dark',
                                nbins=30
                            )
                            fig.update_layout(
                                plot_bgcolor='rgba(0,0,0,0)',
                                paper_bgcolor='rgba(0,0,0,0)',
                                font_color='white'
                            )
                            st.plotly_chart(fig, use_container_width=True)
                            
                            # Box plot for outlier detection
                            fig_box = px.box(
                                cleaned_df,
                                y=col_name,
                                title=f"Box Plot of {col_name} (Outlier Detection)",
                                color_discrete_sequence=['#764ba2'],
                                template='plotly_dark'
                            )
                            fig_box.update_layout(
                                plot_bgcolor='rgba(0,0,0,0)',
                                paper_bgcolor='rgba(0,0,0,0)',
                                font_color='white'
                            )
                            st.plotly_chart(fig_box, use_container_width=True)
                        else:
                            # Create statistics dataframe for text column
                            stats_df = pd.DataFrame({
                                'Statistic': ['Count', 'Unique Values', 'Most Common'],
                                'Value': [
                                    f"{stats['count']:,}",
                                    f"{stats['unique']:,}",
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
                                    color=top_values.values,
                                    color_continuous_scale='Viridis',
                                    template='plotly_dark'
                                )
                                fig.update_layout(
                                    xaxis_title="Count",
                                    yaxis_title="Value",
                                    plot_bgcolor='rgba(0,0,0,0)',
                                    paper_bgcolor='rgba(0,0,0,0)',
                                    font_color='white'
                                )
                                st.plotly_chart(fig, use_container_width=True)
            
            with analysis_tab2:
                st.markdown("""
                    <div class="glass-card">
                        <h4 style="color: white;">Interactive Visualizations</h4>
                    </div>
                """, unsafe_allow_html=True)
                
                # Correlation heatmap for numeric columns
                numeric_cols = cleaned_df.select_dtypes(include=['number']).columns
                if len(numeric_cols) > 1:
                    st.subheader("Correlation Heatmap")
                    corr_matrix = cleaned_df[numeric_cols].corr()
                    fig_corr = go.Figure(data=go.Heatmap(
                        z=corr_matrix,
                        x=corr_matrix.columns,
                        y=corr_matrix.columns,
                        colorscale='Viridis',
                        text=corr_matrix.round(2).values,
                        texttemplate='%{text}',
                        textfont={"size": 10, "color": "white"}
                    ))
                    fig_corr.update_layout(
                        title="Feature Correlation Matrix",
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font_color='white'
                    )
                    st.plotly_chart(fig_corr, use_container_width=True)
                
                # Pairplot for first few numeric columns
                if len(numeric_cols) >= 2 and len(numeric_cols) <= 5:
                    st.subheader("Scatter Plot Matrix")
                    fig_matrix = px.scatter_matrix(
                        cleaned_df[numeric_cols[:4]],
                        title="Pairwise Relationships",
                        template='plotly_dark'
                    )
                    fig_matrix.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font_color='white'
                    )
                    st.plotly_chart(fig_matrix, use_container_width=True)
                
                # Data completeness gauge
                st.subheader("Data Quality Dashboard")
                completeness_score = completeness
                fig_gauge = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = completeness_score,
                    title = {'text': "Data Completeness Score", 'font': {'color': 'white'}},
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    gauge = {
                        'axis': {'range': [None, 100], 'tickcolor': "white"},
                        'bar': {'color': "#667eea"},
                        'steps': [
                            {'range': [0, 50], 'color': "rgba(255, 85, 85, 0.3)"},
                            {'range': [50, 75], 'color': "rgba(255, 193, 7, 0.3)"},
                            {'range': [75, 100], 'color': "rgba(40, 167, 69, 0.3)"}
                        ],
                        'threshold': {
                            'line': {'color': "white", 'width': 4},
                            'thickness': 0.75,
                            'value': 90
                        }
                    }
                ))
                fig_gauge.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='white'
                )
                st.plotly_chart(fig_gauge, use_container_width=True)
            
            with analysis_tab3:
                st.markdown("""
                    <div class="glass-card">
                        <h4 style="color: white;">Cleaned Data Preview</h4>
                    </div>
                """, unsafe_allow_html=True)
                st.dataframe(cleaned_df.head(20), use_container_width=True)
                
                # Show data shape after cleaning
                st.markdown(f"**Data Shape:** {cleaned_df.shape[0]} rows × {cleaned_df.shape[1]} columns")
            
            with analysis_tab4:
                st.markdown("""
                    <div class="glass-card">
                        <h4 style="color: white;">Download Cleaned Data</h4>
                    </div>
                """, unsafe_allow_html=True)
                
                export_col1, export_col2 = st.columns(2)
                
                with export_col1:
                    # Download as CSV
                    csv_data = cleaned_df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download as CSV",
                        data=csv_data,
                        file_name="cleaned_data.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
                
                with export_col2:
                    # Download as Excel
                    output = io.BytesIO()
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        cleaned_df.to_excel(writer, sheet_name='Cleaned Data', index=False)
                    excel_data = output.getvalue()
                    st.download_button(
                        label="📥 Download as Excel",
                        data=excel_data,
                        file_name="cleaned_data.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
                
                # Download as JSON
                json_data = cleaned_df.to_json(orient='records', indent=2)
                st.download_button(
                    label="📥 Download as JSON",
                    data=json_data,
                    file_name="cleaned_data.json",
                    mime="application/json",
                    use_container_width=True
                )
            
            # Summary statistics
            st.markdown("""
                <div class="glass-card">
                    <h4 style="color: white;">📋 Analysis Summary Report</h4>
                </div>
            """, unsafe_allow_html=True)
            
            summary_df = pd.DataFrame({
                'Metric': [
                    'Total Rows', 
                    'Total Columns', 
                    'Missing Values (Before)', 
                    'Missing Values (After)', 
                    'Values Fixed',
                    'Data Completeness',
                    'Duplicate Rows'
                ],
                'Value': [
                    f"{result['rows']:,}",
                    f"{result['columns']:,}",
                    f"{result['missing_before']:,}",
                    f"{result['missing_after']:,}",
                    f"{result['missing_before'] - result['missing_after']:,}",
                    f"{completeness:.1f}%",
                    f"{duplicate_count:,}"
                ]
            })
            st.dataframe(summary_df, use_container_width=True)
            
            # AI Insights
            st.markdown("""
                <div class="glass-card">
                    <h4 style="color: white;">🤖 AI-Generated Insights</h4>
                </div>
            """, unsafe_allow_html=True)
            
            insights = []
            if len(numeric_cols) > 0:
                insights.append(f"• 📊 Your dataset contains {len(numeric_cols)} numeric columns suitable for statistical analysis")
            if missing_count > 0:
                insights.append(f"• 🔍 Successfully cleaned {missing_count:,} missing values from your dataset")
            if duplicate_count > 0:
                insights.append(f"• 🔄 Found and can remove {duplicate_count:,} duplicate rows for better data quality")
            if completeness_score < 80:
                insights.append("• ⚠️ Data completeness is below 80%. Consider collecting more data for better insights")
            else:
                insights.append("• ✅ Excellent data quality! Your dataset has high completeness")
            
            for insight in insights:
                st.markdown(insight)

else:
    # Show info when no file uploaded
    st.markdown("""
        <div class="glass-card" style="text-align: center;">
            <h3 style="color: white;">🚀 Ready to Analyze Your Data?</h3>
            <p style="color: white; margin-top: 1rem;">Upload a CSV, Excel, JSON, or Parquet file to begin your AI-powered data analysis journey</p>
            <p style="color: rgba(255,255,255,0.7); margin-top: 1rem;">💡 Pro tip: Try our intelligent data cleaning and visualization features</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Sample data option
    st.markdown("---")
    st.markdown("""
        <div class="glass-card">
            <h4 style="color: white;">📝 Try with Sample Data</h4>
        </div>
    """, unsafe_allow_html=True)
    
    sample_file = st.file_uploader("Upload a sample file to get started", type=['csv'], key="sample")
    if sample_file is not None:
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; padding: 2rem;">
        <p style="color: rgba(255,255,255,0.7);">
            ✨ AI Data Analyst Pro | Powered by Streamlit, Pandas, Plotly & Advanced ML ✨<br>
            🚀 Real-time Analysis | Smart Data Cleaning | Interactive Visualizations 🚀
        </p>
    </div>
""", unsafe_allow_html=True)
