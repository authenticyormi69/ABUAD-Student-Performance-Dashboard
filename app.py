import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# ============================================================================
# PAGE CONFIG
# ============================================================================
st.set_page_config(page_title="ABUAD Student Performance", layout="wide")

# ============================================================================
# DATA LOADING & COMPREHENSIVE CLEANING
# ============================================================================
@st.cache_data
def load_and_clean_data():
    """Load Excel data and clean/fix all issues"""
    excel_path = Path("data/Student_Analytics_Excel_1000.xlsx")
    
    if not excel_path.exists():
        st.error(f"❌ Data file not found: {excel_path}")
        st.stop()
    
    # Load Excel
    df = pd.read_excel(excel_path)
    
    # Step 1: Strip newline characters from column names
    df.columns = df.columns.str.replace('\n', '', regex=False).str.strip()
    
    # Step 2: Convert key columns to numeric
    numeric_cols = ['Grade Point', 'Avg Attendance %', 'Avg CA Score (Max 40)', 
                    'Avg Exam Score (Max 60)', 'Avg Total Score', 'Risk Score',
                    'Study Hrs/Week', 'Assignment Completion %']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Step 3: PROPER GRADE POINT CALCULATION
    # If Grade Point is mostly zero, recalculate from actual scores
    zero_count = (df['Grade Point'] == 0).sum()
    if zero_count > len(df) * 0.3:  # More than 30% are zero
        # Method 1: Use Total Score
        if 'Avg Total Score' in df.columns:
            df['Grade Point'] = (df['Avg Total Score'] / 100 * 5).round(2)
        # Method 2: Use CA + Exam
        elif 'Avg CA Score (Max 40)' in df.columns and 'Avg Exam Score (Max 60)' in df.columns:
            # Normalize: CA (0-40) + Exam (0-60) = Total (0-100)
            ca_norm = (df['Avg CA Score (Max 40)'] / 40 * 100)
            exam_norm = (df['Avg Exam Score (Max 60)'] / 60 * 100)
            total_score = (ca_norm + exam_norm) / 2  # Average of both
            df['Grade Point'] = (total_score / 100 * 5).round(2)
        
        df['Grade Point'] = df['Grade Point'].fillna(0)
    
    # Ensure Grade Point is in 0-5 range
    df['Grade Point'] = df['Grade Point'].clip(0, 5)
    
    # Step 4: FIX RISK CATEGORY
    # If Risk Category is broken, recalculate from Risk Score
    if 'Risk Category' in df.columns:
        unique_cats = df['Risk Category'].unique()
        if len(unique_cats) == 1 and 'Risk Category' in str(unique_cats[0]):
            # Column is broken, recalculate
            def assign_risk(score):
                if score < 45:
                    return 'At Risk'
                elif score < 70:
                    return 'Needs Monitoring'
                else:
                    return 'On Track'
            
            df['Risk Category'] = df['Risk Score'].apply(assign_risk)
    
    # Step 5: Fill any NaN values
    df['Grade Point'] = df['Grade Point'].fillna(0)
    df['Avg Attendance %'] = df['Avg Attendance %'].fillna(0)
    df['Risk Score'] = df['Risk Score'].fillna(0)
    if 'Risk Category' not in df.columns:
        df['Risk Category'] = 'Unknown'
    
    return df

# Load data
df = load_and_clean_data()

# ============================================================================
# PROFESSIONAL HEADER WITH PROJECT TITLE
# ============================================================================
st.markdown("""
    <style>
        .header-main {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 40px;
            border-radius: 15px;
            color: white;
            text-align: center;
            margin-bottom: 30px;
        }
        .header-title {
            font-size: 2.8em;
            margin: 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            font-weight: bold;
        }
        .project-topic {
            font-size: 1.3em;
            margin-top: 15px;
            margin-bottom: 20px;
            opacity: 0.95;
            font-style: italic;
            border-top: 2px solid rgba(255,255,255,0.3);
            padding-top: 15px;
        }
        .header-credits {
            font-size: 1.05em;
            margin-top: 15px;
            opacity: 0.9;
        }
    </style>
    <div class="header-main">
        <div class="header-title">📊 ABUAD Student Performance Dashboard</div>
        <div class="project-topic">
            <b>Project:</b> "Data Analytics for Predicting Students' Academic Performance"
        </div>
        <div class="header-credits">
            <b>Supervised by:</b> Dr. Josephine Mebawondu<br>
            <b>Developer:</b> AGBELEKALE TOHEEB ORIYOMI (AUTHENTIC)
        </div>
    </div>
""", unsafe_allow_html=True)

st.divider()

# ============================================================================
# SIDEBAR FILTERS
# ============================================================================
st.sidebar.markdown("""
    <h2 style="color: #2c3e50; text-align: center; font-size: 1.5em;">
    🔍 Filter Students
    </h2>
""", unsafe_allow_html=True)

# College filter
colleges = ['All'] + sorted(df['College'].dropna().unique().tolist())
selected_colleges = st.sidebar.multiselect("College", colleges, default=['All'])
if 'All' not in selected_colleges and selected_colleges:
    df_filtered = df[df['College'].isin(selected_colleges)].copy()
else:
    df_filtered = df.copy()

# Department filter
departments = ['All'] + sorted(df_filtered['Department'].dropna().unique().tolist())
selected_depts = st.sidebar.multiselect("Department", departments, default=['All'])
if 'All' not in selected_depts and selected_depts:
    df_filtered = df_filtered[df_filtered['Department'].isin(selected_depts)]

# Study Level filter
levels = ['All'] + sorted(df_filtered['Level'].dropna().unique().tolist())
selected_levels = st.sidebar.multiselect("Study Level", levels, default=['All'])
if 'All' not in selected_levels and selected_levels:
    df_filtered = df_filtered[df_filtered['Level'].isin(selected_levels)]

# Risk Category filter
risk_cats = ['All'] + sorted(df_filtered['Risk Category'].dropna().unique().tolist())
selected_risks = st.sidebar.multiselect("Risk Category", risk_cats, default=['All'])
if 'All' not in selected_risks and selected_risks:
    df_filtered = df_filtered[df_filtered['Risk Category'].isin(selected_risks)]

# Grade Point Range filter
gp_min, gp_max = st.sidebar.slider("Grade Point Range", 0.0, 5.0, (0.0, 5.0), step=0.1)
df_filtered = df_filtered[(df_filtered['Grade Point'] >= gp_min) & (df_filtered['Grade Point'] <= gp_max)]

# Attendance Range filter
att_min, att_max = st.sidebar.slider("Attendance Range (%)", 0, 100, (0, 100), step=5)
df_filtered = df_filtered[(df_filtered['Avg Attendance %'] >= att_min) & (df_filtered['Avg Attendance %'] <= att_max)]

# Gender filter
genders = st.sidebar.multiselect("Gender", df_filtered['Gender'].dropna().unique(), 
                                  default=df_filtered['Gender'].dropna().unique().tolist())
df_filtered = df_filtered[df_filtered['Gender'].isin(genders)]

# Display filter results
st.sidebar.divider()
st.sidebar.metric("📊 Filtered Results", f"{len(df_filtered)} students")

# ============================================================================
# TABS
# ============================================================================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    ["📊 Overview", "🏫 By College", "📚 By Department", "👥 Demographics", "⚠️ At-Risk Students", "💡 Interventions"]
)

# ============================================================================
# TAB 1: OVERVIEW
# ============================================================================
with tab1:
    st.markdown("""
        <style>
            .overview-header {
                background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
                padding: 20px;
                border-radius: 8px;
                color: white;
                margin-bottom: 20px;
            }
            .overview-header h2 {
                margin: 0;
                font-size: 1.8em;
            }
        </style>
        <div class="overview-header">
            <h2>📈 Dashboard Overview</h2>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("👥 Total Students", len(df_filtered), delta=None)
    col2.metric("📚 Avg Grade Point", f"{df_filtered['Grade Point'].mean():.2f}/5", delta=None)
    col3.metric("📅 Avg Attendance %", f"{df_filtered['Avg Attendance %'].mean():.1f}%", delta=None)
    col4.metric("⚡ Avg Risk Score", f"{df_filtered['Risk Score'].mean():.2f}", delta=None)
    
    col1, col2 = st.columns(2)
    
    with col1:
        risk_counts = df_filtered['Risk Category'].value_counts()
        if len(risk_counts) > 0:
            fig = px.pie(risk_counts, values=risk_counts.values, names=risk_counts.index,
                         title="Risk Category Distribution",
                         color_discrete_map={'On Track': '#2ecc71', 'Needs Monitoring': '#f39c12', 'At Risk': '#e74c3c'})
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        if len(df_filtered) > 0:
            fig = px.histogram(df_filtered, x='Grade Point', nbins=20, title="Grade Point Distribution",
                             color_discrete_sequence=['#3498db'])
            st.plotly_chart(fig, use_container_width=True)
    
    if len(df_filtered) > 0:
        fig = px.scatter(df_filtered, x='Avg Attendance %', y='Grade Point', 
                         color='Risk Category', title="Attendance vs Grade Point",
                         color_discrete_map={'On Track': '#2ecc71', 'Needs Monitoring': '#f39c12', 'At Risk': '#e74c3c'})
        st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# TAB 2: BY COLLEGE
# ============================================================================
with tab2:
    st.markdown("""
        <style>
            .college-header {
                background: linear-gradient(135deg, #16a085 0%, #117a65 100%);
                padding: 20px;
                border-radius: 8px;
                color: white;
                margin-bottom: 20px;
            }
            .college-header h2 {
                margin: 0;
                font-size: 1.8em;
            }
        </style>
        <div class="college-header">
            <h2>🏫 Performance by College</h2>
        </div>
    """, unsafe_allow_html=True)
    
    if len(df_filtered) > 0:
        college_stats = df_filtered.groupby('College').agg({
            'Grade Point': 'mean',
            'Avg Attendance %': 'mean',
            'Risk Score': 'mean'
        }).round(2).reset_index()
        
        st.dataframe(college_stats, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(college_stats, x='College', y='Grade Point', 
                         title="Avg Grade Point by College",
                         color_discrete_sequence=['#16a085'])
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.bar(college_stats, x='College', y='Avg Attendance %', 
                         title="Avg Attendance by College",
                         color_discrete_sequence=['#16a085'])
            st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# TAB 3: BY DEPARTMENT
# ============================================================================
with tab3:
    st.markdown("""
        <style>
            .dept-header {
                background: linear-gradient(135deg, #8e44ad 0%, #6c3483 100%);
                padding: 20px;
                border-radius: 8px;
                color: white;
                margin-bottom: 20px;
            }
            .dept-header h2 {
                margin: 0;
                font-size: 1.8em;
            }
        </style>
        <div class="dept-header">
            <h2>📚 Performance by Department</h2>
        </div>
    """, unsafe_allow_html=True)
    
    if len(df_filtered) > 0:
        dept_stats = df_filtered.groupby('Department').agg({
            'Grade Point': 'mean',
            'Avg Attendance %': 'mean',
            'Risk Score': 'mean'
        }).round(2).reset_index()
        
        st.dataframe(dept_stats, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(dept_stats, x='Department', y='Grade Point', 
                         title="Avg Grade Point by Department",
                         color_discrete_sequence=['#8e44ad'])
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.bar(dept_stats, x='Department', y='Avg Attendance %', 
                         title="Avg Attendance by Department",
                         color_discrete_sequence=['#8e44ad'])
            st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# TAB 4: DEMOGRAPHICS
# ============================================================================
with tab4:
    st.markdown("""
        <style>
            .demo-header {
                background: linear-gradient(135deg, #c0392b 0%, #a93226 100%);
                padding: 20px;
                border-radius: 8px;
                color: white;
                margin-bottom: 20px;
            }
            .demo-header h2 {
                margin: 0;
                font-size: 1.8em;
            }
        </style>
        <div class="demo-header">
            <h2>👥 Demographic Analysis</h2>
        </div>
    """, unsafe_allow_html=True)
    
    if len(df_filtered) > 0:
        col1, col2 = st.columns(2)
        
        with col1:
            gender_stats = df_filtered.groupby('Gender').agg({
                'Grade Point': 'mean',
                'Avg Attendance %': 'mean'
            }).round(2).reset_index()
            st.dataframe(gender_stats, use_container_width=True)
            
            if len(gender_stats) > 0:
                fig = px.bar(gender_stats, x='Gender', y='Grade Point', 
                             title="Avg Grade Point by Gender",
                             color_discrete_sequence=['#c0392b'])
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            level_stats = df_filtered.groupby('Level').agg({
                'Grade Point': 'mean',
                'Avg Attendance %': 'mean'
            }).round(2).reset_index()
            st.dataframe(level_stats, use_container_width=True)
            
            if len(level_stats) > 0:
                fig = px.bar(level_stats, x='Level', y='Grade Point', 
                             title="Avg Grade Point by Study Level",
                             color_discrete_sequence=['#c0392b'])
                st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# TAB 5: COMPREHENSIVE AT-RISK ANALYSIS WITH DETAILED CONTEXT
# ============================================================================
with tab5:
    st.markdown("""
        <style>
            .risk-header {
                background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
                padding: 20px;
                border-radius: 8px;
                color: white;
                margin-bottom: 20px;
            }
            .risk-header h2 {
                margin: 0;
                font-size: 1.8em;
            }
        </style>
        <div class="risk-header">
            <h2>⚠️ Student Risk Analysis & Intervention Framework</h2>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📊 Risk Category Summary")
    col1, col2, col3 = st.columns(3)
    
    risk_breakdown = df_filtered['Risk Category'].value_counts()
    
    colors = {
        'At Risk': '#e74c3c',
        'Needs Monitoring': '#f39c12',
        'On Track': '#2ecc71',
    }
    
    for idx, (category, count) in enumerate(risk_breakdown.items()):
        if idx < 3:
            with [col1, col2, col3][idx]:
                color = colors.get(category, '#95a5a6')
                st.markdown(f"""
                    <div style="background: {color}; padding: 20px; border-radius: 8px; color: white; text-align: center;">
                        <h3 style="margin: 0; font-size: 2em;">{count}</h3>
                        <p style="margin: 5px 0 0 0; font-size: 1.1em;">{category}</p>
                    </div>
                """, unsafe_allow_html=True)
    
    st.divider()
    
    st.markdown("### 🔍 Detailed Student Analysis by Risk Category")
    if len(risk_breakdown) > 0:
        selected_category = st.selectbox(
            "Select Risk Category to Analyze:",
            options=risk_breakdown.index.tolist(),
            index=0
        )
        
        category_df = df_filtered[df_filtered['Risk Category'] == selected_category].copy()
        
        st.markdown(f"#### 📊 {selected_category} Students - Key Metrics")
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("👥 Count", len(category_df))
        col2.metric("📊 %", f"{(len(category_df)/len(df_filtered)*100):.1f}%" if len(df_filtered) > 0 else "0%")
        col3.metric("📈 Avg Grade", f"{category_df['Grade Point'].mean():.2f}" if len(category_df) > 0 else "N/A")
        col4.metric("📅 Avg Attend", f"{category_df['Avg Attendance %'].mean():.1f}%" if len(category_df) > 0 else "N/A")
        col5.metric("⚡ Avg Score", f"{category_df['Risk Score'].mean():.2f}" if len(category_df) > 0 else "N/A")
        
        st.divider()
        
        if len(category_df) > 0:
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.histogram(category_df, x='Risk Score', nbins=15, 
                                 title=f"Risk Score Distribution ({selected_category})",
                                 color_discrete_sequence=['#3498db'])
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                dept_data = category_df['Department'].value_counts().reset_index()
                dept_data.columns = ['Department', 'Count']
                if len(dept_data) > 0:
                    fig = px.bar(dept_data, x='Department', y='Count',
                                title=f"{selected_category} Students by Department",
                                color_discrete_sequence=['#9b59b6'])
                    st.plotly_chart(fig, use_container_width=True)
            
            college_data = category_df['College'].value_counts().reset_index()
            college_data.columns = ['College', 'Count']
            if len(college_data) > 0:
                fig = px.bar(college_data, x='College', y='Count',
                            title=f"{selected_category} Students by College",
                            color_discrete_sequence=['#e67e22'])
                st.plotly_chart(fig, use_container_width=True)
            
            # COMPREHENSIVE STUDENT DETAILS TABLE
            st.markdown(f"""
            ### 📋 {selected_category} Students Details Table
            
            **Why These Students Are {selected_category}:**
            - **Grade Point**: Overall academic performance (0-5 scale)
            - **CA Score**: Continuous Assessment (Max 40)
            - **Exam Score**: Examination performance (Max 60)
            - **Attendance**: Class attendance percentage
            - **Study Hours**: Weekly study commitment
            - **Engagement**: Participation level (0-5 scale)
            - **Risk Score**: Weighted formula: R = 0.4×Grade + 0.3×CA + 0.2×Attendance + 0.1×Engagement
            """)
            
            # Build comprehensive display columns - reorder to show most important first
            # Define priority order for columns
            priority_cols = [
                'Full Name', 'Grade Point', 'Risk Score', 'Avg Attendance %', 
                'Study Hrs/Week', 'College', 'Department', 'Level'
            ]
            
            # Add all other columns not in priority list
            other_cols = [col for col in category_df.columns if col not in priority_cols]
            display_cols = priority_cols + other_cols
            
            # Filter to only columns that exist
            display_cols = [col for col in display_cols if col in category_df.columns]
            
            # Create display dataframe with better formatting
            display_df = category_df[display_cols].copy()
            display_df = display_df.sort_values('Risk Score')
            
            st.dataframe(display_df, use_container_width=True)
        else:
            st.info(f"ℹ️ No students in '{selected_category}' category with current filters")

# ============================================================================
# TAB 6: INTERVENTIONS & SUPPORT
# ============================================================================
with tab6:
    st.markdown("""
        <style>
            .intervention-header {
                background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%);
                padding: 25px;
                border-radius: 10px;
                color: white;
                margin-bottom: 20px;
            }
            .intervention-header h2 {
                margin: 0;
                font-size: 2em;
            }
        </style>
        <div class="intervention-header">
            <h2>💡 Interventions & Support Framework</h2>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    ### 🎯 Risk-Level Specific Interventions
    
    #### 🔴 At-Risk Students (Risk Score < 45)
    **Status:** Critical intervention required  
    **Immediate Actions:**
    - One-on-one academic counseling sessions
    - Mandatory peer tutoring programs
    - Enhanced monitoring of attendance
    - Special study group assignments
    - Review of study techniques and time management
    
    **Support Services:**
    - Academic Dean's office intervention
    - Mental health counseling referral
    - Financial aid review (if applicable)
    - Course load adjustment consultation
    
    ---
    
    #### 🟡 Needs Monitoring (45 ≤ Risk Score < 70)
    **Status:** Preventive intervention required  
    **Preventive Measures:**
    - Bi-weekly check-ins with academic advisor
    - Optional tutoring services
    - Study skills workshops
    - Time management seminars
    - Regular progress assessments
    
    **Support Services:**
    - Library research assistance
    - Writing center support
    - Peer mentoring programs
    - Lab/practical work guidance
    
    ---
    
    #### 🟢 On Track (Risk Score ≥ 70)
    **Status:** Maintain current performance  
    **Maintenance & Growth:**
    - Regular progress monitoring
    - Advanced course recommendations
    - Research project opportunities
    - Leadership development programs
    
    **Enrichment:**
    - Internship/industry placements
    - Conference presentation opportunities
    - Scholarship opportunities
    - Graduate program preparation
    
    ---
    
    ### 📞 Key Support Resources
    
    | Service | Purpose | Contact Point |
    |---------|---------|---------------|
    | **Academic Affairs** | Course planning & academic standing | Dean's Office |
    | **Advising & Progression** | Career guidance & progression planning | Student Affairs/Services |
    | **Counseling Services** | Mental health & wellbeing support | Student Health |
    | **Library Services** | Research & information literacy | Learning Commons |
    | **Writing Center** | Essay & writing assistance | Academic Support |
    
    """)