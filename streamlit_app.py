import streamlit as st
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Set page configuration
st.set_page_config(
    page_title="EduPro Learner Intelligence Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for Premium Aesthetics
st.markdown("""
    <style>
        .main-header {
            font-size: 2.2rem;
            color: #1F4E79;
            font-weight: 700;
            margin-bottom: 0.5rem;
            text-align: left;
        }
        .subheader {
            font-size: 1.2rem;
            color: #555555;
            margin-bottom: 2rem;
        }
        .metric-card {
            background-color: #F8F9FA;
            border-radius: 8px;
            padding: 15px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            border-left: 5px solid #4E79A7;
            text-align: center;
        }
        .metric-value {
            font-size: 1.8rem;
            font-weight: bold;
            color: #1F4E79;
        }
        .metric-label {
            font-size: 0.9rem;
            color: #666666;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
    </style>
""", unsafe_allow_html=True)

# Custom color dict
colors = {
    'primary': '#4E79A7',
    'secondary': '#F28E2B',
    'accent1': '#E15759',
    'accent2': '#76B7B2',
    'accent3': '#59A14F',
    'female': '#F28E2B',
    'male': '#4E79A7'
}

# Determine Excel file path or uploaded file
current_dir = os.path.dirname(os.path.abspath(__file__))
paths_to_check = [
    os.path.join(current_dir, "data", "EduPro Online Platform.xlsx"),
    os.path.join(current_dir, "EduPro Online Platform.xlsx"),
    r"C:\Users\Vishal K\Downloads\EduPro Online Platform.xlsx"
]

file_source = None
for p in paths_to_check:
    if os.path.exists(p):
        file_source = p
        break

# Process data function
def process_data(users, courses, transactions, teachers):
    def get_age_band(age):
        if age < 18: return '<18'
        elif age <= 25: return '18–25'
        elif age <= 35: return '26–35'
        elif age <= 45: return '36–45'
        else: return '45+'
    
    users['AgeGroup'] = users['Age'].apply(get_age_band)
    merged = transactions.merge(users, on='UserID', how='inner').merge(courses, on='CourseID', how='inner')
    merged['AgeGroup'] = merged['Age'].apply(get_age_band)
    return users, courses, transactions, teachers, merged

# Load data helper with caching
@st.cache_data
def load_data_from_path(path):
    users_df = pd.read_excel(path, sheet_name='Users')
    courses_df = pd.read_excel(path, sheet_name='Courses')
    transactions_df = pd.read_excel(path, sheet_name='Transactions')
    teachers_df = pd.read_excel(path, sheet_name='Teachers')
    return process_data(users_df, courses_df, transactions_df, teachers_df)

users = None
courses = None
transactions = None
teachers = None
merged = None

if file_source is not None:
    try:
        users, courses, transactions, teachers, merged = load_data_from_path(file_source)
    except Exception as e:
        st.error(f"Error reading dataset: {e}")
        st.stop()
else:
    # Setup premium layout headers before stop
    st.markdown('<div class="main-header">EduPro Learner Intelligence Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="subheader">Descriptive insights into learner demographics, course preferences, and enrollment behaviors.</div>', unsafe_allow_html=True)
    
    st.warning("⚠️ Dataset file 'EduPro Online Platform.xlsx' was not found automatically in the repository or local directories.")
    st.info("To activate the dashboard, please upload the Excel database spreadsheet below:")
    uploaded_file = st.file_uploader("Upload EduPro Online Platform.xlsx", type=["xlsx"])
    
    if uploaded_file is not None:
        try:
            users_df = pd.read_excel(uploaded_file, sheet_name='Users')
            courses_df = pd.read_excel(uploaded_file, sheet_name='Courses')
            transactions_df = pd.read_excel(uploaded_file, sheet_name='Transactions')
            teachers_df = pd.read_excel(uploaded_file, sheet_name='Teachers')
            users, courses, transactions, teachers, merged = process_data(users_df, courses_df, transactions_df, teachers_df)
        except Exception as e:
            st.error(f"Failed to parse uploaded Excel file. Ensure it is the original 'EduPro Online Platform.xlsx'. Details: {e}")
            st.stop()
    else:
        st.stop()

# --- SIDEBAR FILTERS ---
st.sidebar.image("https://img.icons8.com/fluent/96/000000/diploma.png", width=80)
st.sidebar.markdown("## Interactive Filters")
st.sidebar.markdown("Use the controls below to segment the analytics dashboard in real time.")

# Age Group filter
age_options = sorted(list(merged['AgeGroup'].unique()))
selected_age_groups = st.sidebar.multiselect(
    "Select Age Groups",
    options=age_options,
    default=age_options
)

# Gender filter
gender_options = list(merged['Gender'].unique())
selected_genders = st.sidebar.multiselect(
    "Select Genders",
    options=gender_options,
    default=gender_options
)

# Course Category filter
cat_options = sorted(list(merged['CourseCategory'].unique()))
selected_categories = st.sidebar.multiselect(
    "Select Course Categories",
    options=cat_options,
    default=cat_options
)

# Course Level filter
level_options = list(merged['CourseLevel'].unique())
selected_levels = st.sidebar.multiselect(
    "Select Course Levels",
    options=level_options,
    default=level_options
)

# Pricing Type filter
pricing_options = list(merged['CourseType'].unique())
selected_pricing = st.sidebar.multiselect(
    "Select Course Pricing Type",
    options=pricing_options,
    default=pricing_options
)

# Apply filters
filtered_df = merged[
    (merged['AgeGroup'].isin(selected_age_groups)) &
    (merged['Gender'].isin(selected_genders)) &
    (merged['CourseCategory'].isin(selected_categories)) &
    (merged['CourseLevel'].isin(selected_levels)) &
    (merged['CourseType'].isin(selected_pricing))
]

# --- MAIN DASHBOARD INTERFACE ---
st.markdown('<div class="main-header">EduPro Learner Intelligence Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="subheader">Descriptive insights into learner demographics, course preferences, and enrollment behaviors.</div>', unsafe_allow_html=True)

# Warning if dataset is empty
if len(filtered_df) == 0:
    st.warning("No records match the selected filters. Please adjust your selections in the sidebar.")
    st.stop()

# --- KPI METRICS CARD RIBBON ---
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{len(filtered_df):,}</div>
            <div class="metric-label">Total Enrollments</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    unique_users_count = filtered_df['UserID'].nunique()
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{unique_users_count:,}</div>
            <div class="metric-label">Active Learners</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    avg_courses = len(filtered_df) / unique_users_count if unique_users_count > 0 else 0
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{avg_courses:.2f}</div>
            <div class="metric-label">Avg. Courses/User</div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    fem_pct = (filtered_df['Gender'] == 'Female').sum() / len(filtered_df) * 100 if len(filtered_df) > 0 else 0
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{fem_pct:.1f}%</div>
            <div class="metric-label">Female Enrollments</div>
        </div>
    """, unsafe_allow_html=True)

with col5:
    free_pct = (filtered_df['CourseType'] == 'Free').sum() / len(filtered_df) * 100 if len(filtered_df) > 0 else 0
    st.markdown(f"""
        <div class="metric-card" style="border-left-color: #59A14F;">
            <div class="metric-value">{free_pct:.1f}%</div>
            <div class="metric-label">Free Enrollments</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- MODULE 1: DEMOGRAPHICS OVERVIEW ---
st.markdown("### 📊 Learner Demographic Profile")
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    st.markdown("#### Age Group Enrollment Breakdown")
    age_counts = filtered_df['AgeGroup'].value_counts().reindex(['<18', '18–25', '26–35', '36–45', '45+']).fillna(0)
    # Drop rows that are completely 0
    age_counts = age_counts[age_counts > 0]
    
    if len(age_counts) > 0:
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(x=age_counts.index, y=age_counts.values, hue=age_counts.index, palette="Blues_d", legend=False, ax=ax)
        ax.set_ylabel("Number of Enrollments")
        ax.set_xlabel("Age Group")
        # Add labels
        for p in ax.patches:
            ax.annotate(f"{int(p.get_height()):,}", (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center', xytext=(0, 5), textcoords='offset points', fontsize=10)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
    else:
        st.info("No age data matching selection.")

with row1_col2:
    st.markdown("#### Gender Distribution (Enrollments)")
    gender_counts = filtered_df['Gender'].value_counts()
    if len(gender_counts) > 0:
        fig, ax = plt.subplots(figsize=(6, 5))
        ax.pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%', startangle=90, 
               colors=[colors['female'], colors['male']], textprops={'fontsize': 11},
               wedgeprops={'edgecolor': 'white', 'linewidth': 1.5})
        ax.axis('equal')
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
    else:
        st.info("No gender data matching selection.")

# --- MODULE 2: COURSE POPULARITY & PREFERENCES ---
st.markdown("### 📚 Course Popularity & Selection Analytics")
row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    st.markdown("#### Course Category Popularity")
    cat_popularity = filtered_df['CourseCategory'].value_counts().sort_values(ascending=True)
    if len(cat_popularity) > 0:
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x=cat_popularity.values, y=cat_popularity.index, hue=cat_popularity.index, palette="viridis", legend=False, ax=ax)
        ax.set_xlabel("Enrollments")
        ax.set_ylabel("Category")
        for p in ax.patches:
            width = p.get_width()
            ax.annotate(f"{int(width):,}", (width, p.get_y() + p.get_height() / 2.),
                        ha='left', va='center', xytext=(3, 0), textcoords='offset points', fontsize=9)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
    else:
        st.info("No category data matching selection.")

with row2_col2:
    st.markdown("#### Course Level Preference Distribution")
    level_counts = filtered_df['CourseLevel'].value_counts().reindex(['Beginner', 'Intermediate', 'Advanced']).fillna(0)
    if level_counts.sum() > 0:
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(x=level_counts.index, y=level_counts.values, hue=level_counts.index, palette="plasma", legend=False, ax=ax)
        ax.set_xlabel("Skill Level")
        ax.set_ylabel("Enrollments")
        for p in ax.patches:
            ax.annotate(f"{int(p.get_height()):,}", (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center', xytext=(0, 5), textcoords='offset points', fontsize=10)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
    else:
        st.info("No course level data matching selection.")

# --- MODULE 3: DEMOGRAPHICS X PREFERENCE CROSS-TABS ---
st.markdown("### 🔀 Demographic × Course Preference Overlaps")
row3_col1, row3_col2 = st.columns(2)

with row3_col1:
    st.markdown("#### Enrollment Heatmap: Age Bands vs Course Categories")
    age_cat_ct = pd.crosstab(filtered_df['AgeGroup'], filtered_df['CourseCategory']).astype(int)
    if len(age_cat_ct) > 0:
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.heatmap(age_cat_ct, annot=True, fmt="d", cmap="YlGnBu", cbar=True, ax=ax)
        ax.set_ylabel("Age Group")
        ax.set_xlabel("Course Category")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
    else:
        st.info("Insufficient overlap data.")

with row3_col2:
    st.markdown("#### Course Level Preference by Gender (%)")
    gender_level_pct = pd.crosstab(filtered_df['Gender'], filtered_df['CourseLevel'], normalize='index') * 100
    if len(gender_level_pct) > 0:
        gender_level_pct = gender_level_pct.reset_index().melt(id_vars='Gender', value_name='Percentage', var_name='CourseLevel')
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(data=gender_level_pct, x='CourseLevel', y='Percentage', hue='Gender', palette=[colors['female'], colors['male']], ax=ax)
        ax.set_ylabel("Percentage of Genders")
        ax.set_xlabel("Course Level")
        for p in ax.patches:
            height = p.get_height()
            if height > 0:
                ax.annotate(f"{height:.1f}%", (p.get_x() + p.get_width() / 2., height),
                            ha='center', va='center', xytext=(0, 5), textcoords='offset points', fontsize=9)
        ax.set_ylim(0, 50)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
    else:
        st.info("Insufficient gender-level data.")

# --- MODULE 4: BEHAVIORAL INSIGHTS ---
st.markdown("### 🧠 Learner Engagement Depth & Concentration")
row4_col1, row4_col2 = st.columns(2)

with row4_col1:
    st.markdown("#### Distribution of Courses per Learner")
    courses_per_user = filtered_df.groupby('UserID').size()
    
    if len(courses_per_user) > 0:
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.histplot(courses_per_user, discrete=True, kde=False, color=colors['primary'], edgecolor='white', ax=ax)
        ax.set_xlabel("Number of Courses Enrolled")
        ax.set_ylabel("Number of Learners")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
        
        # Display summary table of percentiles
        percentile_df = pd.DataFrame({
            "Percentile": ["50% (Median)", "75%", "90%", "95%", "99%"],
            "Courses Enrolled": [
                courses_per_user.quantile(0.50),
                courses_per_user.quantile(0.75),
                courses_per_user.quantile(0.90),
                courses_per_user.quantile(0.95),
                courses_per_user.quantile(0.99)
            ]
        })
        st.table(percentile_df)
    else:
        st.info("No enrollment depth data matching selection.")

with row4_col2:
    st.markdown("#### Activity Concentration Summary")
    total_enr = len(filtered_df)
    active_users = filtered_df['UserID'].nunique()
    
    # Concentation metrics
    top_10_pct_count = max(1, int(0.10 * active_users))
    top_users_enrollments = courses_per_user.sort_values(ascending=False).head(top_10_pct_count).sum()
    concentration_pct = (top_users_enrollments / total_enr * 100) if total_enr > 0 else 0
    
    st.info(f"""
        **Activity Focus Metrics:**
        - **Total Platform Transactions:** {total_enr:,}
        - **Unique Participating Citizens:** {active_users:,}
        - **Cohort Activity Concentration:** The top 10% of active users ({top_10_pct_count:,} learners) account for **{top_users_enrollments:,} enrollments**, representing **{concentration_pct:.2f}%** of all platform activity.
        
        **Business Action Takeaways:**
        - *High Churn After Trial 1:* Since the median course count is 1.0, half of the learners leave after their first course. EduPro must trigger retention emails immediately after Course 1.
        - *Leverage Power-Users:* Highly engaged learners represent a valuable peer-tutor group or potential advocates for community study networks.
    """)
