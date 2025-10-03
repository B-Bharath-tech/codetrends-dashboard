import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# Page setup
st.set_page_config(
    page_title="CodeTrends Analytics Pro", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Modern CSS with background simulation and clean design
st.markdown("""
<style>
    /* Main background with gradient animation */
    .stApp {
        background: linear-gradient(-45deg, #667eea, #764ba2, #f093fb, #f5576c);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        padding: 1rem;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Main content container */
    .main-block {
        background: rgba(255, 255, 255, 0.92);
        backdrop-filter: blur(20px);
        border-radius: 24px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
        margin: 0 auto;
        padding: 3rem;
        max-width: 1400px;
    }

    .main-header {
        font-size: 3.5rem !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
        font-weight: 800;
        text-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }

    .sub-header {
        text-align: center;
        color: #6c757d !important;
        margin-bottom: 3rem;
        font-size: 1.3rem;
        font-weight: 500;
    }

    /* Enhanced metric cards */
    .metric-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(255,255,255,0.8) 100%);
        padding: 1.5rem;
        border-radius: 20px;
        color: #2c3e50;
        text-align: center;
        margin: 0.5rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.4);
        backdrop-filter: blur(15px);
        transition: all 0.3s ease;
    }

    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.2);
    }

    .metric-value {
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        margin: 0.5rem 0 !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .metric-label {
        font-size: 0.9rem !important;
        color: #6c757d !important;
        margin-bottom: 0.5rem !important;
        font-weight: 600;
    }

    /* Clean section styling */
    .section-header {
        color: #2c3e50;
        font-weight: 700;
        margin: 2.5rem 0 1.5rem 0;
        font-size: 1.8rem;
        position: relative;
        padding-bottom: 0.8rem;
    }

    .section-header::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 60px;
        height: 4px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 2px;
    }

    /* Clean filter area */
    .filter-area {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(15px);
        padding: 1.5rem;
        border-radius: 16px;
        margin: 1.5rem 0;
        border: 1px solid rgba(255,255,255,0.4);
        box-shadow: 0 8px 32px rgba(0,0,0,0.08);
    }

    /* Clean cards */
    .content-card {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(15px);
        border-radius: 16px;
        border: 1px solid rgba(255,255,255,0.3);
        box-shadow: 0 8px 32px rgba(0,0,0,0.08);
        padding: 1.5rem;
        margin: 1rem 0;
    }

    .insight-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(15px);
        border-radius: 12px;
        border-left: 4px solid #667eea;
        padding: 1.2rem;
        margin: 0.8rem 0;
        box-shadow: 0 4px 16px rgba(0,0,0,0.06);
        transition: all 0.3s ease;
    }

    .insight-card:hover {
        transform: translateX(5px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.1);
    }

    /* Tech ecosystem styling */
    .tech-section {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(15px);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        border: 1px solid rgba(255,255,255,0.3);
        box-shadow: 0 8px 32px rgba(0,0,0,0.08);
    }

    .tech-badge {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.6rem 1.2rem;
        border-radius: 20px;
        margin: 0.4rem;
        font-size: 0.85rem;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
    }

    .tech-badge:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }

    .tech-category {
        color: #667eea;
        font-weight: 700;
        margin-bottom: 1rem;
        font-size: 1.1rem;
        position: relative;
        padding-left: 0.8rem;
    }

    .tech-category::before {
        content: '';
        position: absolute;
        left: 0;
        top: 50%;
        transform: translateY(-50%);
        width: 3px;
        height: 16px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 2px;
    }

    /* Chart styling */
    .stPlotlyChart {
        border-radius: 12px;
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        padding: 1rem;
        border: 1px solid rgba(255,255,255,0.3);
    }

    /* Recommendation styling */
    .recommendation-text {
        color: #2c3e50;
        font-weight: 600;
        margin: 0.5rem 0;
        line-height: 1.6;
        font-size: 0.95rem;
    }

    /* Clean footer */
    .clean-footer {
        text-align: center;
        color: rgba(108, 117, 125, 0.8);
        margin-top: 3rem;
        padding-top: 2rem;
        border-top: 1px solid rgba(255,255,255,0.3);
        font-size: 0.9rem;
    }

    /* Remove Streamlit default styling */
    .stButton > button {
        border-radius: 12px !important;
        border: 1px solid rgba(255,255,255,0.3) !important;
        background: rgba(255,255,255,0.9) !important;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.1);
    }

    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
    }

    ::-webkit-scrollbar-track {
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

def get_advanced_trends():
    """Generate comprehensive language trends with multiple metrics"""
    current_year = datetime.now().year
    start_year = 2018
    
    # Enhanced data with multiple metrics
    trends = {
        "Python": {
            "popularity": {"2018": 75, "2019": 80, "2020": 85, "2021": 90, "2022": 95, "2023": 100, "2024": 105},
            "demand": 95, "learning": 90, "salary": 120000, "ecosystem": 95, "growth": 4.5
        },
        "JavaScript": {
            "popularity": {"2018": 80, "2019": 82, "2020": 84, "2021": 86, "2022": 88, "2023": 90, "2024": 92},
            "demand": 92, "learning": 85, "salary": 110000, "ecosystem": 98, "growth": 2.0
        },
        "Java": {
            "popularity": {"2018": 85, "2019": 80, "2020": 75, "2021": 70, "2022": 65, "2023": 60, "2024": 55},
            "demand": 78, "learning": 70, "salary": 105000, "ecosystem": 90, "growth": -3.0
        },
        "C++": {
            "popularity": {"2018": 65, "2019": 63, "2020": 60, "2021": 58, "2022": 55, "2023": 52, "2024": 50},
            "demand": 70, "learning": 60, "salary": 115000, "ecosystem": 85, "growth": -2.0
        },
        "Go": {
            "popularity": {"2018": 25, "2019": 30, "2020": 40, "2021": 50, "2022": 60, "2023": 68, "2024": 75},
            "demand": 65, "learning": 75, "salary": 130000, "ecosystem": 70, "growth": 8.0
        },
        "Rust": {
            "popularity": {"2018": 15, "2019": 20, "2020": 25, "2021": 35, "2022": 45, "2023": 55, "2024": 65},
            "demand": 60, "learning": 50, "salary": 140000, "ecosystem": 65, "growth": 12.0
        },
        "TypeScript": {
            "popularity": {"2018": 30, "2019": 40, "2020": 55, "2021": 65, "2022": 75, "2023": 82, "2024": 88},
            "demand": 85, "learning": 80, "salary": 125000, "ecosystem": 90, "growth": 10.0
        },
        "Kotlin": {
            "popularity": {"2018": 20, "2019": 30, "2020": 45, "2021": 55, "2022": 65, "2023": 72, "2024": 78},
            "demand": 75, "learning": 85, "salary": 118000, "ecosystem": 80, "growth": 9.0
        }
    }
    
    # Build comprehensive data structure - separate years from metrics
    years_data = {"Language": list(trends.keys())}
    metrics_data = {"Language": list(trends.keys())}
    
    # Add popularity data for all years
    for year in range(start_year, current_year + 1):
        year_data = []
        for lang in trends.keys():
            if str(year) in trends[lang]["popularity"]:
                year_data.append(trends[lang]["popularity"][str(year)])
            else:
                # Project future trends
                last_known_year = 2024
                years_diff = year - last_known_year
                base_value = trends[lang]["popularity"][str(last_known_year)]
                growth = trends[lang]["growth"]
                projected_value = max(5, min(100, base_value + (growth * years_diff)))
                year_data.append(round(projected_value))
        years_data[str(year)] = year_data
    
    # Add additional metrics
    metrics = ["demand", "learning", "salary", "ecosystem", "growth"]
    for metric in metrics:
        metrics_data[metric] = [trends[lang][metric] for lang in trends.keys()]
    
    return years_data, metrics_data, trends

def create_radar_chart(trends_data, languages):
    """Create radar chart for language comparison"""
    categories = ['Popularity', 'Demand', 'Learning', 'Salary', 'Ecosystem']
    
    fig = go.Figure()
    
    for lang in languages:
        values = [
            trends_data[lang]['popularity']['2024'],
            trends_data[lang]['demand'],
            trends_data[lang]['learning'],
            trends_data[lang]['salary'] / 150000 * 100,  # Normalize salary
            trends_data[lang]['ecosystem']
        ]
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name=lang
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=True,
        title="Language Capabilities Radar Chart",
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

# Header Section
current_year = datetime.now().year
start_year = 2018

st.markdown('<div class="main-block">', unsafe_allow_html=True)

st.markdown('<h1 class="main-header">🚀 CodeTrends Analytics Pro</h1>', unsafe_allow_html=True)
st.markdown(f'<p class="sub-header">Advanced Programming Language Intelligence & Market Insights {start_year}-{current_year}</p>', unsafe_allow_html=True)

# Load advanced data
years_data, metrics_data, trends_data = get_advanced_trends()

# Top Metrics Row
st.markdown('<div class="section-header">📈 Executive Summary</div>', unsafe_allow_html=True)

metric_cols = st.columns(4)

with metric_cols[0]:
    current_popularity = [years_data[str(current_year)][i] for i in range(len(years_data["Language"]))]
    current_leader = years_data["Language"][np.argmax(current_popularity)]
    leader_score = max(current_popularity)
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">🔥 Current Leader</div>
        <div class="metric-value">{current_leader}</div>
        <div>Score: {leader_score}</div>
    </div>
    """, unsafe_allow_html=True)

with metric_cols[1]:
    lowest_trend = years_data["Language"][np.argmin(current_popularity)]
    lowest_score = min(current_popularity)
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">📉 Lowest Trend</div>
        <div class="metric-value">{lowest_trend}</div>
        <div>Score: {lowest_score}</div>
    </div>
    """, unsafe_allow_html=True)

with metric_cols[2]:
    fastest_growing = metrics_data["Language"][np.argmax(metrics_data["growth"])]
    growth_rate = max(metrics_data["growth"])
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">🚀 Fastest Growing</div>
        <div class="metric-value">{fastest_growing}</div>
        <div>+{growth_rate:.1f}% annual growth</div>
    </div>
    """, unsafe_allow_html=True)

with metric_cols[3]:
    popular_lang = current_leader
    popular_score = leader_score
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">⭐ Most Popular</div>
        <div class="metric-value">{popular_lang}</div>
        <div>Score: {popular_score}</div>
    </div>
    """, unsafe_allow_html=True)

# Interactive Filters
st.markdown('<div class="section-header">🎛️ Data Controls</div>', unsafe_allow_html=True)

st.markdown('<div class="filter-area">', unsafe_allow_html=True)
filter_col1, filter_col2, filter_col3 = st.columns(3)

with filter_col1:
    years = list(range(start_year, current_year + 1))
    selected_years = st.multiselect(
        "**Select Years**", 
        years, 
        default=[2018, 2020, 2022, 2024, current_year],
        key="years_filter"
    )

with filter_col2:
    all_languages = years_data["Language"]
    selected_languages = st.multiselect(
        "**Select Languages**",
        all_languages,
        default=["Python", "JavaScript", "TypeScript", "Go", "Rust"],
        key="lang_filter"
    )

with filter_col3:
    chart_type = st.selectbox(
        "**Chart Type**",
        ["Bar Chart", "Line Chart", "Area Chart", "Heatmap"],
        key="chart_type"
    )
st.markdown('</div>', unsafe_allow_html=True)

# Main Visualization
st.markdown('<div class="section-header">📊 Language Popularity Trends</div>', unsafe_allow_html=True)

if not selected_languages or not selected_years:
    st.warning("⚠️ Please select at least one language and year")
else:
    # Filter data - only include year columns and Language
    year_columns = [str(year) for year in selected_years]
    filtered_data = {"Language": years_data["Language"]}
    
    for year_col in year_columns:
        if year_col in years_data:
            filtered_data[year_col] = years_data[year_col]
    
    filtered_df = pd.DataFrame(filtered_data)
    filtered_df = filtered_df[filtered_df["Language"].isin(selected_languages)]
    
    # Prepare data for plotting
    df_melted = filtered_df.melt(id_vars="Language", var_name="Year", value_name="Popularity")
    
    # Create chart based on selection
    if chart_type == "Bar Chart":
        fig = px.bar(
            df_melted, 
            x="Language", 
            y="Popularity", 
            color="Year", 
            barmode="group",
            color_discrete_sequence=px.colors.qualitative.Vivid
        )
    elif chart_type == "Line Chart":
        fig = px.line(
            df_melted, 
            x="Year", 
            y="Popularity", 
            color="Language",
            markers=True,
            color_discrete_sequence=px.colors.qualitative.Vivid
        )
    elif chart_type == "Area Chart":
        fig = px.area(
            df_melted, 
            x="Year", 
            y="Popularity", 
            color="Language",
            color_discrete_sequence=px.colors.qualitative.Vivid
        )
    else:  # Heatmap
        pivot_df = df_melted.pivot(index="Language", columns="Year", values="Popularity")
        fig = px.imshow(
            pivot_df,
            aspect="auto",
            color_continuous_scale="Viridis"
        )
    
    fig.update_layout(
        height=500,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12),
        showlegend=True
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Advanced Analytics Section
st.markdown('<div class="section-header">🔬 Advanced Analytics</div>', unsafe_allow_html=True)

analytics_col1, analytics_col2 = st.columns(2)

with analytics_col1:
    st.markdown("### 📈 Growth Analysis")
    
    growth_data = []
    for i, lang in enumerate(years_data["Language"]):
        if lang in selected_languages:
            start_val = years_data["2018"][i]
            end_val = years_data[str(current_year)][i]
            growth_pct = ((end_val - start_val) / start_val) * 100 if start_val > 0 else 0
            growth_data.append({
                "Language": lang,
                "Growth %": growth_pct,
                "Start": start_val,
                "End": end_val
            })
    
    if growth_data:
        growth_df = pd.DataFrame(growth_data)
        fig_growth = px.bar(
            growth_df, 
            x="Language", 
            y="Growth %",
            color="Growth %",
            color_continuous_scale="RdYlGn"
        )
        fig_growth.update_layout(height=400, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_growth, use_container_width=True)

with analytics_col2:
    st.markdown("### 🎯 Language Comparison")
    
    if len(selected_languages) >= 2:
        radar_fig = create_radar_chart(trends_data, selected_languages[:4])
        st.plotly_chart(radar_fig, use_container_width=True)
    else:
        st.info("Select at least 2 languages for comparison")

# Market Insights
st.markdown('<div class="section-header">💡 Market Insights & Recommendations</div>', unsafe_allow_html=True)

insights_col1, insights_col2 = st.columns(2)

with insights_col1:
    st.markdown("### <span style='color:#667eea;'>🏆 Top Performers</span>", unsafe_allow_html=True)
    
    performance_data = []
    for i, lang in enumerate(years_data["Language"]):
        if lang in selected_languages:
            score = (years_data[str(current_year)][i] * 0.3 + 
                    metrics_data["demand"][i] * 0.3 + 
                    metrics_data["salary"][i] / 150000 * 100 * 0.2 +
                    metrics_data["growth"][i] * 0.2)
            performance_data.append((lang, score))
    
    performance_data.sort(key=lambda x: x[1], reverse=True)
    
    for lang, score in performance_data[:5]:
        lang_idx = years_data["Language"].index(lang)
        st.markdown(f"""
        <div class="insight-card">
            <strong style='color:#2c3e50;'>{lang}</strong> - <span style='color:#667eea; font-weight:600;'>Overall Score: {score:.1f}</span>
            <br><small style='color:#6c757d;'>Popularity: {years_data[str(current_year)][lang_idx]} | 
            Demand: {metrics_data['demand'][lang_idx]}% | 
            Growth: +{metrics_data['growth'][lang_idx]:.1f}%</small>
        </div>
        """, unsafe_allow_html=True)

with insights_col2:
    st.markdown("### <span style='color:#667eea;'>📋 Quick Recommendations</span>", unsafe_allow_html=True)
    
    recommendations = [
        "<span class='recommendation-text'>🚀 For Beginners: Start with Python or JavaScript for wide applicability</span>",
        "<span class='recommendation-text'>💼 For Job Seekers: Focus on TypeScript and Go for high growth opportunities</span>", 
        "<span class='recommendation-text'>⚡ For Performance: Consider Rust or C++ for system-level programming</span>",
        "<span class='recommendation-text'>📱 For Mobile: Kotlin for Android, Swift for iOS development</span>",
        "<span class='recommendation-text'>🔮 Future Proof: Invest in Rust and Go for emerging trends</span>"
    ]
    
    for rec in recommendations:
        st.markdown(f"<div class='content-card'>{rec}</div>", unsafe_allow_html=True)

# Technology Stack Overview
st.markdown('<div class="section-header">🛠️ Technology Ecosystem</div>', unsafe_allow_html=True)

st.markdown('<div class="tech-section">', unsafe_allow_html=True)
tech_cols = st.columns(4)
categories = {
    "🌐 Web Development": ["JavaScript", "TypeScript", "Python", "PHP"],
    "📱 Mobile Development": ["Kotlin", "Java", "Swift", "Dart"],
    "⚡ Systems Programming": ["Rust", "C++", "Go", "C"],
    "📊 Data & AI": ["Python", "R", "Julia", "Scala"]
}

for col, (category, langs) in zip(tech_cols, categories.items()):
    with col:
        st.markdown(f"<div class='tech-category'>{category}</div>", unsafe_allow_html=True)
        for lang in langs:
            if lang in years_data["Language"]:
                st.markdown(f'<div class="tech-badge">{lang}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="tech-badge" style="background: #6c757d;">{lang}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Clean footer
st.markdown('</div>', unsafe_allow_html=True)  # Close main-block

st.markdown(
    f"<div class='clean-footer'>"
    f"🚀 Advanced Language Analytics • {start_year}-{current_year} Trends"
    f"</div>",
    unsafe_allow_html=True
)
