import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path


def html(s):
    """Strip indentation and blank lines so Markdown doesn't treat HTML as a code block."""
    return "\n".join(line.strip() for line in s.splitlines() if line.strip())


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="PIXEL VOLT | NIE EEE",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================================================
# PIXEL VOLT THEME
# ==================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Space+Mono:wght@400;700&display=swap');

:root {
    --bg: #11191b;
    --panel: #1b292b;
    --panel2: #223436;
    --teal: #8bd3c7;
    --lavender: #c6b8e8;
    --pink: #e9b8c8;
    --cream: #f0eadb;
    --muted: #a8b9b4;
}

.stApp {
    background-color: var(--bg);
    background-image:
        linear-gradient(rgba(139,211,199,.035) 1px, transparent 1px),
        linear-gradient(90deg, rgba(139,211,199,.035) 1px, transparent 1px);
    background-size: 24px 24px;
    color: var(--cream);
    font-family: 'Space Mono', monospace;
}

[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stSidebar"] {
    background: #182426;
    border-right: 2px solid #46615d;
}

[data-testid="stSidebar"] * {
    color: var(--cream);
    font-family: 'Space Mono', monospace;
}

h1, h2, h3 {
    color: var(--teal) !important;
    font-family: 'Space Mono', monospace !important;
}

.pixel-title {
    font-family: 'Press Start 2P', monospace;
    color: var(--teal);
    font-size: clamp(17px, 2.5vw, 27px);
    line-height: 1.8;
    text-shadow: 3px 3px 0 #344b48;
}

.subtitle {
    color: var(--lavender);
    font-size: 12px;
    letter-spacing: 2px;
}

.college-header {
    background: #1b292b;
    border: 2px solid #55736d;
    padding: 18px;
    text-align: center;
    margin-bottom: 20px;
    box-shadow: 5px 5px 0 #0b1112;
}

.college-name {
    color: #8bd3c7;
    font-size: 17px;
    font-weight: bold;
}

.department {
    color: #c6b8e8;
    font-size: 13px;
    margin-top: 7px;
}

.project-info {
    color: #e9b8c8;
    font-size: 11px;
    margin-top: 10px;
}

.pixel-card {
    background: var(--panel);
    border: 2px solid #55736d;
    border-radius: 0;
    padding: 17px;
    box-shadow: 5px 5px 0 #0b1112;
    min-height: 112px;
}

.metric-label {
    color: var(--muted);
    font-size: 11px;
    letter-spacing: 1px;
}

.metric-value {
    color: var(--teal);
    font-size: 24px;
    font-weight: bold;
    margin-top: 10px;
}

.metric-note {
    color: var(--pink);
    font-size: 10px;
    margin-top: 5px;
}

.section-tag {
    color: var(--lavender);
    font-size: 12px;
    letter-spacing: 2px;
    border-bottom: 1px dashed #718b83;
    padding-bottom: 8px;
    margin: 25px 0 14px 0;
}

.team-card {
    background: #1b292b;
    border: 1px solid #55736d;
    padding: 15px;
    margin-top: 10px;
    color: #f0eadb;
    font-size: 12px;
    line-height: 2;
}

div[data-testid="stPlotlyChart"] {
    background: var(--panel);
    border: 1px solid #46615d;
    padding: 8px;
}

.stButton button, .stDownloadButton button {
    background: #8bd3c7;
    color: #142120;
    border: 2px solid #d3eee5;
    border-radius: 0;
    font-family: 'Space Mono', monospace;
    font-weight: bold;
}

.stButton button:hover, .stDownloadButton button:hover {
    background: #c6b8e8;
    color: #142120;
}

div[data-baseweb="select"] > div {
    background: #223436;
    border-color: #55736d;
}

[data-testid="stDataFrame"] {
    border: 1px solid #55736d;
}

hr {
    border-color: #46615d;
}

footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)


# ==================================================
# DATASET LOADING
# ==================================================

@st.cache_data
def load_data(uploaded_file=None):

    if uploaded_file is not None:

        name = uploaded_file.name.lower()

        if name.endswith((".xlsx", ".xls")):
            return pd.read_excel(uploaded_file)

        return pd.read_csv(uploaded_file)

    possible_files = [
        Path("ev_charging_patterns.csv"),
        Path("ev_charging_patterns.xlsx"),
        Path("ev_charging_patterns.xls")
    ]

    data_file = next(
        (file for file in possible_files if file.exists()),
        None
    )

    if data_file is None:
        return None

    if data_file.suffix.lower() in [".xlsx", ".xls"]:
        return pd.read_excel(data_file)

    return pd.read_csv(data_file)


# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.markdown("## ⚡ PIXEL VOLT")
st.sidebar.caption("EV CHARGING ANALYTICS SYSTEM")
st.sidebar.markdown("---")

uploaded_file = st.sidebar.file_uploader(
    "UPLOAD CHARGING DATA",
    type=["csv", "xlsx", "xls"]
)

df = load_data(uploaded_file)

if df is None:

    st.markdown(
        '<div class="pixel-title">PIXEL VOLT ⚡</div>',
        unsafe_allow_html=True
    )

    st.warning(
        "Dataset not found. Place ev_charging_patterns.csv "
        "in the same folder as app.py or upload it using the sidebar."
    )

    st.stop()


# ==================================================
# DATA PREPARATION
# ==================================================

df.columns = df.columns.str.strip()

required_columns = [
    "Energy Consumed (kWh)",
    "Charging Duration (hours)",
    "Charging Cost (USD)",
    "Charger Type",
    "Time of Day",
    "Day of Week"
]

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:

    st.error(
        "Missing required columns: " + ", ".join(missing_columns)
    )

    st.stop()


numeric_columns = [
    "Energy Consumed (kWh)",
    "Charging Duration (hours)",
    "Charging Cost (USD)",
    "Battery Capacity (kWh)",
    "Charging Rate (kW)",
    "Temperature (°C)",
    "Vehicle Age (years)"
]

for column in numeric_columns:

    if column in df.columns:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

if "Charging Start Time" in df.columns:

    df["Charging Start Time"] = pd.to_datetime(
        df["Charging Start Time"],
        errors="coerce"
    )

df = df.dropna(
    subset=["Energy Consumed (kWh)"]
).copy()


# ==================================================
# COLLEGE AND PROJECT HEADER
# ==================================================

st.markdown(html("""
<div class="college-header">

    <div class="college-name">
        THE NATIONAL INSTITUTE OF ENGINEERING, MYSURU
    </div>

    <div class="department">
        DEPARTMENT OF ELECTRICAL AND ELECTRONICS ENGINEERING
    </div>

    <div class="project-info">
        DATA ANALYTICS MINI PROJECT
        <br>
        EV CHARGING SESSION ANALYSIS
    </div>

</div>
"""), unsafe_allow_html=True)


# ==================================================
# DASHBOARD TITLE
# ==================================================

st.markdown(
    '<div class="pixel-title">⚡ PIXEL VOLT</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'EV CHARGING SESSION ANALYSIS // DATA TERMINAL 01'
    '</div>',
    unsafe_allow_html=True
)

st.markdown("---")


# ==================================================
# SIDEBAR FILTERS
# ==================================================

st.sidebar.markdown("### DATA FILTERS")

filtered = df.copy()

filter_columns = [
    ("Charger Type", "CHARGER TYPE"),
    ("Time of Day", "TIME OF DAY"),
    ("Day of Week", "DAY OF WEEK"),
    ("User Type", "USER TYPE")
]

for column, label in filter_columns:

    if column in filtered.columns:

        options = sorted(
            filtered[column].dropna().astype(str).unique()
        )

        selected = st.sidebar.multiselect(
            label,
            options,
            default=options
        )

        filtered = filtered[
            filtered[column].astype(str).isin(selected)
        ]

if filtered.empty:

    st.warning(
        "No sessions match the selected filters."
    )

    st.stop()


# ==================================================
# SYSTEM OVERVIEW / KPI CARDS
# ==================================================

total_sessions = len(filtered)

avg_energy = filtered["Energy Consumed (kWh)"].mean()

avg_duration = filtered["Charging Duration (hours)"].mean()

avg_cost = filtered["Charging Cost (USD)"].mean()

st.markdown(
    '<div class="section-tag">01 // SYSTEM OVERVIEW</div>',
    unsafe_allow_html=True
)

k1, k2, k3, k4 = st.columns(4)

metrics = [
    (
        k1,
        "TOTAL SESSIONS",
        f"{total_sessions:,}",
        "CHARGING RECORDS"
    ),
    (
        k2,
        "AVG ENERGY",
        f"{avg_energy:.2f} kWh",
        "ENERGY PER SESSION"
    ),
    (
        k3,
        "AVG DURATION",
        f"{avg_duration:.2f} hrs",
        "SESSION LENGTH"
    ),
    (
        k4,
        "AVG COST",
        f"${avg_cost:.2f}",
        "COST PER SESSION"
    )
]

for col, label, value, note in metrics:

    with col:

        st.markdown(html(f"""
        <div class="pixel-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-note">{note}</div>
        </div>
        """), unsafe_allow_html=True)


# ==================================================
# CHART STYLING
# ==================================================

chart_colors = [
    "#8bd3c7",
    "#c6b8e8",
    "#e9b8c8",
    "#e7d9a8"
]

def style_chart(fig, height=350):

    fig.update_layout(
        height=height,
        paper_bgcolor="#1b292b",
        plot_bgcolor="#1b292b",
        font=dict(
            family="Space Mono",
            color="#f0eadb",
            size=11
        ),
        title_font=dict(
            color="#8bd3c7",
            size=15
        ),
        margin=dict(
            l=20,
            r=20,
            t=55,
            b=35
        ),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(color="#f0eadb")
        ),
        xaxis=dict(
            gridcolor="#344b48",
            linecolor="#55736d",
            zerolinecolor="#55736d"
        ),
        yaxis=dict(
            gridcolor="#344b48",
            linecolor="#55736d",
            zerolinecolor="#55736d"
        )
    )

    return fig


# ==================================================
# CHARGER PERFORMANCE
# ==================================================

st.markdown(
    '<div class="section-tag">02 // CHARGER PERFORMANCE</div>',
    unsafe_allow_html=True
)

left, right = st.columns(2)

charger_summary = filtered.groupby(
    "Charger Type"
).agg(
    Sessions=("Energy Consumed (kWh)", "count"),
    Average_Energy=("Energy Consumed (kWh)", "mean"),
    Average_Duration=("Charging Duration (hours)", "mean"),
    Average_Cost=("Charging Cost (USD)", "mean")
).reset_index()

with left:

    fig = px.bar(
        charger_summary,
        x="Charger Type",
        y="Average_Energy",
        color="Charger Type",
        color_discrete_sequence=chart_colors,
        title="AVERAGE ENERGY BY CHARGER"
    )

    st.plotly_chart(
        style_chart(fig),
        use_container_width=True
    )

with right:

    fig = px.pie(
        charger_summary,
        names="Charger Type",
        values="Sessions",
        hole=0.55,
        color_discrete_sequence=chart_colors,
        title="SESSION DISTRIBUTION"
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent+label"
    )

    st.plotly_chart(
        style_chart(fig),
        use_container_width=True
    )


# ==================================================
# TIME ANALYSIS
# ==================================================

st.markdown(
    '<div class="section-tag">03 // CHARGING TIME PATTERNS</div>',
    unsafe_allow_html=True
)

time_order = [
    "Morning",
    "Afternoon",
    "Evening",
    "Night"
]

time_summary = filtered.groupby(
    "Time of Day"
).agg(
    Average_Energy=("Energy Consumed (kWh)", "mean"),
    Sessions=("Energy Consumed (kWh)", "count")
).reset_index()

time_summary["Time of Day"] = pd.Categorical(
    time_summary["Time of Day"],
    categories=time_order,
    ordered=True
)

time_summary = time_summary.sort_values(
    "Time of Day"
)

day_order = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]

day_summary = filtered.groupby(
    "Day of Week"
).agg(
    Average_Energy=("Energy Consumed (kWh)", "mean"),
    Sessions=("Energy Consumed (kWh)", "count")
).reset_index()

day_summary["Day of Week"] = pd.Categorical(
    day_summary["Day of Week"],
    categories=day_order,
    ordered=True
)

day_summary = day_summary.sort_values(
    "Day of Week"
)

left, right = st.columns(2)

with left:

    fig = px.bar(
        time_summary,
        x="Time of Day",
        y="Average_Energy",
        color="Time of Day",
        color_discrete_sequence=chart_colors,
        title="ENERGY BY TIME OF DAY"
    )

    st.plotly_chart(
        style_chart(fig),
        use_container_width=True
    )

with right:

    fig = px.bar(
        day_summary,
        x="Day of Week",
        y="Average_Energy",
        color="Average_Energy",
        color_continuous_scale=[
            "#c6b8e8",
            "#8bd3c7"
        ],
        title="ENERGY BY DAY OF WEEK"
    )

    st.plotly_chart(
        style_chart(fig),
        use_container_width=True
    )


# ==================================================
# ENERGY RELATIONSHIPS
# ==================================================

st.markdown(
    '<div class="section-tag">04 // ENERGY RELATIONSHIPS</div>',
    unsafe_allow_html=True
)

left, right = st.columns(2)

relationship_data = filtered.dropna(
    subset=[
        "Charging Duration (hours)",
        "Energy Consumed (kWh)"
    ]
)

with left:

    fig = px.density_heatmap(
        relationship_data,
        x="Charging Duration (hours)",
        y="Energy Consumed (kWh)",
        nbinsx=25,
        nbinsy=25,
        color_continuous_scale=[
            "#223436",
            "#c6b8e8",
            "#8bd3c7"
        ],
        title="CHARGING DENSITY MAP"
    )

    st.plotly_chart(
        style_chart(fig),
        use_container_width=True
    )

with right:

    fig = px.box(
        filtered,
        x="Charger Type",
        y="Energy Consumed (kWh)",
        color="Charger Type",
        color_discrete_sequence=chart_colors,
        points=False,
        title="ENERGY DISTRIBUTION BY CHARGER"
    )

    st.plotly_chart(
        style_chart(fig),
        use_container_width=True
    )


# ==================================================
# VEHICLE AND BATTERY INSIGHTS
# ==================================================

if "Battery Capacity (kWh)" in filtered.columns:

    st.markdown(
        '<div class="section-tag">05 // VEHICLE & BATTERY INSIGHTS</div>',
        unsafe_allow_html=True
    )

    left, right = st.columns(2)

    with left:

        battery_data = filtered.dropna(
            subset=["Battery Capacity (kWh)"]
        )

        fig = px.box(
            battery_data,
            x="Charger Type",
            y="Battery Capacity (kWh)",
            color="Charger Type",
            color_discrete_sequence=chart_colors,
            title="BATTERY CAPACITY BY CHARGER",
            points="outliers"
        )

        st.plotly_chart(
            style_chart(fig),
            use_container_width=True
        )

    with right:

        if "Vehicle Model" in filtered.columns:

            vehicle_summary = (
                filtered.groupby("Vehicle Model")[
                    "Energy Consumed (kWh)"
                ]
                .mean()
                .sort_values(ascending=False)
                .head(10)
                .reset_index()
            )

            fig = px.bar(
                vehicle_summary,
                x="Energy Consumed (kWh)",
                y="Vehicle Model",
                orientation="h",
                color="Energy Consumed (kWh)",
                color_continuous_scale=[
                    "#c6b8e8",
                    "#8bd3c7"
                ],
                title="TOP 10 VEHICLES BY AVG ENERGY"
            )

            fig.update_layout(
                yaxis={"categoryorder": "total ascending"}
            )

            st.plotly_chart(
                style_chart(fig),
                use_container_width=True
            )


# ==================================================
# CHARGING ACTIVITY TIMELINE
# ==================================================

if "Charging Start Time" in filtered.columns:

    timeline = filtered.dropna(
        subset=["Charging Start Time"]
    ).copy()

    if not timeline.empty:

        timeline["Session Date"] = (
            timeline["Charging Start Time"].dt.date
        )

        daily = timeline.groupby(
            "Session Date"
        ).agg(
            Sessions=("Energy Consumed (kWh)", "count"),
            Energy=("Energy Consumed (kWh)", "sum")
        ).reset_index()

        st.markdown(
            '<div class="section-tag">06 // CHARGING ACTIVITY TIMELINE</div>',
            unsafe_allow_html=True
        )

        fig = px.line(
            daily,
            x="Session Date",
            y="Sessions",
            markers=True,
            title="DAILY CHARGING SESSION COUNT"
        )

        fig.update_traces(
            line=dict(
                color="#8bd3c7",
                width=3
            ),
            marker=dict(size=7)
        )

        st.plotly_chart(
            style_chart(fig, height=380),
            use_container_width=True
        )


# ==================================================
# MACHINE LEARNING FINDINGS
# ==================================================

st.markdown(
    '<div class="section-tag">07 // MACHINE LEARNING FINDINGS</div>',
    unsafe_allow_html=True
)

st.markdown(html("""
<div class="pixel-card">

    <div class="metric-label">
        MODEL EVALUATION
    </div>

    <div style="color:#c6b8e8; font-size:14px; margin-top:12px;">
        The evaluated regression models showed limited predictive
        performance compared with the mean baseline.
    </div>

    <div style="color:#e9b8c8; font-size:11px; margin-top:12px;">
        INSIGHT: The available dataset features have weak relationships
        with actual energy consumption. Predictions should therefore
        be interpreted cautiously.
    </div>

</div>
"""), unsafe_allow_html=True)


# ==================================================
# SESSION DATA EXPLORER
# ==================================================

st.markdown(
    '<div class="section-tag">08 // SESSION DATA EXPLORER</div>',
    unsafe_allow_html=True
)

st.caption(
    "Explore the charging records after applying your filters."
)

st.dataframe(
    filtered,
    use_container_width=True,
    height=300
)

csv_data = filtered.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="⬇ DOWNLOAD FILTERED DATASET",
    data=csv_data,
    file_name="filtered_ev_charging_data.csv",
    mime="text/csv"
)


# ==================================================
# PROJECT TEAM DETAILS
# ==================================================

st.markdown(
    '<div class="section-tag">09 // PROJECT TEAM</div>',
    unsafe_allow_html=True
)

st.markdown(html("""
<div class="team-card">

    <b style="color:#8bd3c7;">PROJECT GROUP</b>
    <br>
    GROUP NUMBER: 11

    <br><br>

    <b style="color:#c6b8e8;">TEAM MEMBERS</b>
    <br>
    01. Tejaswin MK — 4NI25EE105
    <br>
    02. Prarthana RN — 4NI25EE067
    <br>
    03. Vandana NR — 4NI25EE111

    <br><br>

    <b style="color:#e9b8c8;">SUBMITTED TO</b>
    <br>
    Assistant Professor Smrithi Vijiyan
    <br>
    Department of Electrical and Electronics Engineering
    <br>
    The National Institute of Engineering, Mysuru

</div>
"""), unsafe_allow_html=True)


# ==================================================
# FOOTER
# ==================================================

st.markdown("---")

st.markdown(html("""
<div style="
    text-align:center;
    color:#8bd3c7;
    font-size:11px;
    padding:18px;
    line-height:2;
">

    ▪ PIXEL VOLT ▪ EV CHARGING SESSION ANALYSIS ▪

    <br>

    THE NATIONAL INSTITUTE OF ENGINEERING, MYSURU

    <br>

    DEPARTMENT OF ELECTRICAL AND ELECTRONICS ENGINEERING

    <br><br>

    POWERED BY PYTHON • STREAMLIT • PLOTLY

</div>
"""), unsafe_allow_html=True)
