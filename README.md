# EduPro Learner Intelligence Dashboard 🎓

An interactive data analytics and dashboard application built with **Streamlit** to evaluate learner demographics, course popularity, and platform engagement behavior on the **EduPro** online learning platform.

This study implements *descriptive learner intelligence* to transition platform operations from intuition-driven to data-driven decision-making.

---

## 🚀 Key Features

1. **KPI Metric Ribbon:** Real-time summary metrics showing Total Enrollments, Active Learners, Average Course Count per User, and Female/Free enrollment ratios.
2. **Learner Demographic Profiles:** Insights into student age bands (<18, 18-25, 26-35) and gender participation ratios.
3. **Course Preferences:** Popularity ranks for all 12 course categories and distributions across skill levels (Beginner, Intermediate, Advanced).
4. **Demographic x Preference Overlaps:** Multi-dimensional cross-tabulations including Age vs. Category heatmap matrices and Gender vs. Skill Level comparisons.
5. **Engagement Depth & Concentration:** Pareto-style evaluation indicating course distribution counts and power-user cohort activity concentration.
6. **Dynamic Filters Panel:** Segment all metrics in real-time by Age Group, Gender, Course Category, Course Level, and Pricing Type.

---

## 🛠️ Installation & Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   cd YOUR_REPO_NAME
   ```

2. **Install Python Dependencies:**
   Ensure you have Python 3.8+ installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify the Dataset:**
   Ensure the dataset `EduPro Online Platform.xlsx` is placed in the `data/` subfolder:
   `data/EduPro Online Platform.xlsx`

4. **Launch the Dashboard:**
   ```bash
   streamlit run streamlit_app.py
   ```
   Open your browser and navigate to `http://localhost:8501` to view the live dashboard.

---

## 📄 Project Structure
```text
├── data/
│   └── EduPro Online Platform.xlsx  # Master dataset
├── streamlit_app.py                  # Streamlit application entrypoint
├── requirements.txt                  # Python dependencies
├── .gitignore                        # Git ignore patterns
└── README.md                         # Project documentation
```
