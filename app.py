import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# ================================================================================
# PAGE CONFIG
# ================================================================================
st.set_page_config(page_title="ABUAD Student Performance", layout="wide")

# ================================================================================
# DATA LOADING
# ================================================================================
@st.cache_data
def load_data():
    """Load and clean Excel data"""
    excel_path = Path("data/Student_Analytics_Excel_1000.xlsx")
    
    if not excel_path.exists():
        st.error(f"❌ Data file not found: {excel_path}")
        st.stop()
    
    try:
        df = pd.read_excel(excel_path)
        
        # Strip newlines from column names
        df.columns = df.columns.str.replace('\n', ' ').str.strip()
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.stop()

# Load data
df = load_data()

# ================================================================================
# HEADER
# ================================================================================
st.title("📊 ABUAD Student Performance Dashboard")
st.markdown("---")
st.markdown("**Data Analytics for Predicting Students' Academic Performance**")
st.markdown("*Final Year Project | Afe Babalola University Ado-Ekiti*")
st.markdown("---")

# ================================================================================
# SIDEBAR FILTERS
# ================================================================================
st.sidebar.title("🔍 Filters")

# Get unique values for filters
colleges = sorted(df['College'].unique()) if 'College' in df.columns else []
departments = sorted(df['Department'].unique()) if 'Department' in df.columns else []

# Filter widgets
selected_college = st.sidebar.multiselect("📍 College", options=colleges, default=colleges)
selected_dept = st.sidebar.multiselect("🏢 Department", options=departments, default=departments)

# Apply filters
filtered_df = df[
    (df['College'].isin(selected_college)) & 
    (df['Department'].isin(selected_dept))
]

st.sidebar.metric("📈 Total Students Displayed", len(filtered_df))

# ================================================================================
# TAB NAVIGATION
# ================================================================================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Overview",
    "🏫 By College",
    "🎓 By Department",
    "👥 Demographics",
    "⚠️ At-Risk Students",
    "💡 Interventions"
])

# ================================================================================
# TAB 1: OVERVIEW
# ================================================================================
with tab1:
    st.header("📊 Dashboard Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Students", len(filtered_df))
    
    with col2:
        if 'Grade Point' in filtered_df.columns:
            avg_gpa = filtered_df['Grade Point'].mean()
            st.metric("Avg Grade Point", f"{avg_gpa:.2f}")
    
    with col3:
        if 'Risk Score' in filtered_df.columns:
            at_risk = len(filtered_df[filtered_df['Risk Score'] < 45])
            st.metric("At-Risk Students", at_risk)
    
    with col4:
        if 'Risk Score' in filtered_df.columns:
            on_track = len(filtered_df[filtered_df['Risk Score'] >= 70])
            st.metric("On-Track Students", on_track)
    
    st.markdown("---")
    
    # Risk Distribution
    st.subheader("Risk Category Distribution")
    if 'Risk Category' in filtered_df.columns:
        risk_counts = filtered_df['Risk Category'].value_counts()
        fig = px.bar(x=risk_counts.index, y=risk_counts.values, 
                     labels={'x': 'Risk Category', 'y': 'Count'},
                     color=risk_counts.index,
                     title="Student Risk Distribution")
        st.plotly_chart(fig, use_container_width=True)

# ================================================================================
# TAB 2: BY COLLEGE
# ================================================================================
with tab2:
    st.header("🏫 Performance by College")
    
    if 'College' in filtered_df.columns:
        college_stats = filtered_df.groupby('College').agg({
            'Student ID': 'count',
            'Grade Point': 'mean' if 'Grade Point' in filtered_df.columns else 'size'
        }).round(2)
        college_stats.columns = ['Total Students', 'Avg Grade Point']
        
        st.dataframe(college_stats, use_container_width=True)
        
        # Visualization
        if 'Grade Point' in filtered_df.columns:
            fig = px.box(filtered_df, x='College', y='Grade Point',
                        title="Grade Point Distribution by College",
                        color='College')
            st.plotly_chart(fig, use_container_width=True)

# ================================================================================
# TAB 3: BY DEPARTMENT
# ================================================================================
with tab3:
    st.header("🎓 Performance by Department")
    
    if 'Department' in filtered_df.columns:
        dept_stats = filtered_df.groupby('Department').agg({
            'Student ID': 'count',
            'Grade Point': 'mean' if 'Grade Point' in filtered_df.columns else 'size'
        }).round(2)
        dept_stats.columns = ['Total Students', 'Avg Grade Point']
        
        st.dataframe(dept_stats, use_container_width=True)
        
        # Visualization
        if 'Grade Point' in filtered_df.columns:
            fig = px.bar(filtered_df.groupby('Department')['Grade Point'].mean().sort_values(ascending=False),
                        title="Average Grade Point by Department",
                        labels={'value': 'Avg Grade Point', 'index': 'Department'})
            st.plotly_chart(fig, use_container_width=True)

# ================================================================================
# TAB 4: DEMOGRAPHICS
# ================================================================================
with tab4:
    st.header("👥 Student Demographics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'Gender' in filtered_df.columns:
            gender_counts = filtered_df['Gender'].value_counts()
            fig = px.pie(values=gender_counts.values, names=gender_counts.index,
                        title="Gender Distribution")
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        if 'Level' in filtered_df.columns:
            level_counts = filtered_df['Level'].value_counts()
            fig = px.pie(values=level_counts.values, names=level_counts.index,
                        title="Level Distribution")
            st.plotly_chart(fig, use_container_width=True)

# ================================================================================
# TAB 5: AT-RISK STUDENTS
# ================================================================================
with tab5:
    st.header("⚠️ At-Risk Students Analysis")
    
    if 'Risk Score' in filtered_df.columns:
        at_risk_df = filtered_df[filtered_df['Risk Score'] < 45].copy()
        
        st.metric("Total At-Risk Students", len(at_risk_df))
        
        if len(at_risk_df) > 0:
            st.subheader("At-Risk Student Details")
            
            # Display columns if they exist
            display_cols = ['Student ID', 'Name', 'College', 'Department', 'Risk Score']
            existing_cols = [col for col in display_cols if col in at_risk_df.columns]
            
            st.dataframe(at_risk_df[existing_cols].head(50), use_container_width=True)
            
            # Risk score distribution
            fig = px.histogram(at_risk_df, x='Risk Score', nbins=20,
                             title="Risk Score Distribution (At-Risk Students)")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.success("✅ No at-risk students in current selection!")

# ================================================================================
# TAB 6: INTERVENTIONS
# ================================================================================
with tab6:
    st.header("💡 Recommended Interventions")
    
    st.markdown("""
    ### Support Services Available at ABUAD
    
    | Service | Purpose | Contact Point |
    |---------|---------|---------------|
    | **Academic Affairs** | Course planning & academic standing | Dean's Office |
    | **Advising & Progression** | Career guidance & progression planning | Student Affairs |
    | **Counseling Services** | Mental health & wellbeing support | Student Health |
    | **Library Services** | Research & information literacy | Learning Commons |
    | **Writing Center** | Essay & writing assistance | Academic Support |
    
    ### Intervention Recommendations
    
    Based on risk scores:
    - **At Risk (<45):** Intensive tutoring, mentoring, academic counseling
    - **Needs Monitoring (45-69):** Study groups, peer tutoring, progress tracking
    - **On Track (≥70):** Maintain current study habits, explore advanced coursework
    """)

# ================================================================================
# FOOTER
# ================================================================================
st.markdown("---")
st.markdown("""
**Project Information:**
- Supervised by: Dr. Josephine Mebawondu
- Institution: Afe Babalola University Ado-Ekiti
- Dataset: 1,000 student records | 5 Colleges | 10 Departments
""")