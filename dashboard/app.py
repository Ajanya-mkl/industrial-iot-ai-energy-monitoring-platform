# Advanced Factory AI Monitoring Dashboard (10 Monitoring Panels)


import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time

st.set_page_config(
    page_title="⚡ Factory AI Monitoring",
    page_icon="⚡",
    layout="wide"
)

# =============================
# CUSTOM CSS
# =============================
st.markdown(
    """
    <style>
    .main {
        background-color: #0E1117;
    }

    .metric-card {
        background-color: #1E1E1E;
        padding: 15px;
        border-radius: 15px;
        box-shadow: 0px 0px 10px rgba(0,255,255,0.2);
        text-align: center;
    }

    .metric-title {
        font-size: 18px;
        color: #A0A0A0;
    }

    .metric-value {
        font-size: 28px;
        font-weight: bold;
        color: #00FFFF;
    }

    .status-normal {
        color: #00FF7F;
        font-weight: bold;
    }

    .status-anomaly {
        color: red;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =============================
# TITLE
# =============================
st.title("🏭 Real-Time Factory AI Monitoring System")
st.markdown("### Kafka + Spark Streaming + ML Anomaly Detection")

# =============================
# LOAD DATA
# =============================

def load_data():

    try:
        df = pd.read_csv(
            "dashboard/live_data.csv",
            names=[
                "voltage",
                "current",
                "temperature",
                "machine_status",
                "power",
                "prediction",
                "status"
            ]
        )

        return df

    except:
        return pd.DataFrame()

# =============================
# LIVE LOOP
# =============================

placeholder = st.empty()

while True:

    df = load_data()

    with placeholder.container():

        if len(df) > 0:

            latest = df.tail(10).reset_index()

            st.subheader("⚡ Live Machine Monitoring")

            # =============================
            # 10 MONITORING CARDS
            # =============================

            cols = st.columns(5)

            for i in range(min(10, len(latest))):

                row = latest.iloc[i]

                status_class = (
                    "status-anomaly"
                    if row['status'] == 'ANOMALY'
                    else "status-normal"
                )

                with cols[i % 5]:

                    st.markdown(
                        f"""
                        <div class="metric-card">
                            <div class="metric-title">
                                Machine {i+1}
                            </div>
                            <hr>
                            <div class="metric-value">
                                {round(row['power'],2)} W
                            </div>
                            <br>
                            Voltage: {row['voltage']} V<br>
                            Current: {round(row['current'],2)} A<br>
                            Temp: {round(row['temperature'],2)} °C<br>
                            <br>
                            <span class="{status_class}">
                                {row['status']}
                            </span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            st.markdown("---")

            # =============================
            # CHARTS
            # =============================

            col1, col2 = st.columns(2)

            with col1:

                st.subheader("📈 Power Consumption Trend")

                fig = px.line(
                    df.tail(50),
                    y="power",
                    title="Real-Time Power Usage"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            with col2:

                st.subheader("🌡 Temperature Monitoring")

                fig2 = px.line(
                    df.tail(50),
                    y="temperature",
                    title="Machine Temperature"
                )

                st.plotly_chart(
                    fig2,
                    use_container_width=True
                )

            # =============================
            # ANOMALY COUNTER
            # =============================

            anomaly_count = len(
                df[df['status'] == 'ANOMALY']
            )

            normal_count = len(
                df[df['status'] == 'NORMAL']
            )

            c1, c2 = st.columns(2)

            with c1:
                st.metric(
                    "🚨 Total Anomalies",
                    anomaly_count
                )

            with c2:
                st.metric(
                    "✅ Normal Records",
                    normal_count
                )

            # =============================
            # LIVE TABLE
            # =============================

            st.subheader("📋 Live Streaming Data")

            st.dataframe(
                df.tail(20),
                use_container_width=True
            )

        else:

            st.warning("Waiting for streaming data...")

    time.sleep(2)

