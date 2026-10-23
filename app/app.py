
import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from frontend import apply_theme, render_sidebar, render_header,render_kpis,render_analysis_result
import plotly.express as px

apply_theme()
render_sidebar()
render_header()

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
from tools.analysis_tool import analyze

load_dotenv()

st.set_page_config(page_title="InsightAI", page_icon="📊", layout="wide")

st.markdown("""
<style>
    :root {
        --bg: #0B0F19;
        --panel: #111827;
        --border: #253247;
        --blue: #60A5FA;
        --muted: #94A3B8;
        --text: #F1F5F9;
    }

    .stApp {
        background: var(--bg);
        color: var(--text);
    }

    [data-testid="stSidebar"] {
        background: #0D1422;
        border-right: 1px solid var(--border);
    }

    [data-testid="stSidebar"] h1 {
        color: var(--blue);
        font-size: 1.5rem;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1500px;
    }

    .insight-header {
        padding: 1.4rem 1.6rem;
        border: 1px solid var(--border);
        border-radius: 16px;
        background: linear-gradient(120deg, #111827, #152238);
        margin-bottom: 1.5rem;
    }

    .insight-header h1 {
        margin: 0;
        font-size: 2rem;
        color: #F8FAFC;
    }

    .insight-header p {
        margin: 0.55rem 0 0;
        color: var(--muted);
        font-size: 0.95rem;
    }

    [data-testid="stMetric"] {
        background: var(--panel);
        border: 1px solid var(--border);
        padding: 1rem 1.1rem;
        border-radius: 14px;
    }

    [data-testid="stMetricLabel"] {
        color: var(--muted);
    }

    [data-testid="stMetricValue"] {
        color: var(--blue);
    }

    div[data-testid="stFileUploader"] {
        background: var(--panel);
        border: 1px dashed #3B82F6;
        border-radius: 14px;
        padding: 0.75rem;
    }

    .stTextInput input {
        background: var(--panel);
        border: 1px solid var(--border);
        border-radius: 10px;
    }

    .stButton button[kind="primary"] {
        background: #2563EB;
        border: 1px solid #3B82F6;
        border-radius: 10px;
        font-weight: 600;
    }

    .stButton button[kind="primary"]:hover {
        background: #1D4ED8;
        border-color: #60A5FA;
    }

    [data-testid="stDataFrame"] {
        border: 1px solid var(--border);
        border-radius: 12px;
        overflow: hidden;
    }

    hr {
        border-color: var(--border);
    }
</style>
""", unsafe_allow_html=True)

uploaded = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx", "xls"])

if uploaded:
    try:
        if uploaded.name.lower().endswith(".csv"):
            df = pd.read_csv(uploaded)
        else:
            df = pd.read_excel(uploaded)

        st.success(f"Loaded {len(df):,} rows × {len(df.columns)} columns")

        render_kpis(df)

        with st.expander("Dataset preview"):
            st.dataframe(df.head(10), use_container_width=True)

        st.write("**Columns:**", ", ".join(map(str, df.columns)))

        question = st.text_input(
            "Ask a question about your data",
            placeholder="Which region generated the highest revenue?"
        )


        if st.button("Analyze", type="primary") and question:
            api_key = os.getenv("GROQ_API_KEY")
            plan = None

            if api_key:
                from agents.data_agent import create_analysis_plan
                try:
                    plan = create_analysis_plan(
                        question, df.columns.tolist(), api_key
                    )
                except Exception as e:
                    st.warning(f"LLM planning failed: {e}")
            else:
                st.warning(
                    "GROQ_API_KEY is not set. Using rule-based analysis."
                )

            try:
                result = analyze(df, question, plan)
                st.session_state["analysis_result"] = result
                st.session_state["analysis_question"] = question
            except Exception as e:
                st.error(f"Could not analyze the question: {e}")

        # Show the saved result after Streamlit reruns
        if "analysis_result" in st.session_state:
            result = st.session_state["analysis_result"]

            render_analysis_result(result)

            # Visualization controls
            st.divider()
            st.subheader("📊 Data Visualization")

            chart_type = st.selectbox(
                "Choose chart type",
                ["Bar Chart", "Pie Chart", "Line Chart"],
                key="chart_type"
            )

            columns = df.columns.tolist()
            numeric_columns = df.select_dtypes(
                include="number"
            ).columns.tolist()

            if numeric_columns:
                x_column = st.selectbox(
                    "Select category or X-axis",
                    columns,
                    key="viz_x"
                )
                y_column = st.selectbox(
                    "Select numeric column",
                    numeric_columns,
                    key="viz_y"
                )

                if st.button("Generate Visualization"):
                    chart_data = (
                        df.groupby(x_column, dropna=False)[y_column]
                        .sum()
                        .reset_index()
                    )


                    if chart_type == "Bar Chart":
                        import plotly.express as px

                        fig = px.bar(
                            chart_data,
                            x=x_column,
                            y=y_column,
                            title=f"{y_column} by {x_column}",
                            template="plotly_dark",
                            labels={
                                x_column: x_column,
                                y_column: y_column,
                            },
                        )

                        fig.update_layout(
                            paper_bgcolor="#0B0F19",
                            plot_bgcolor="#111827",
                            font_color="#F1F5F9",
                            title_x=0.02,
                            margin=dict(l=20, r=20, t=60, b=40),
                        )

                        st.plotly_chart(fig, use_container_width=True)

                    elif chart_type == "Pie Chart":

                       fig = px.pie(
                            chart_data,
                            names=x_column,
                            values=y_column,
                            title=f"{y_column} by {x_column}",
                            template="plotly_dark",
                            hole=0.4,
                        )

                       fig.update_traces(
                        textposition="inside",
                        textinfo="percent",
                        hovertemplate=(
                            "<b>%{label}</b><br>"
                            + y_column
                            + ": %{value:,.0f}<br>"
                            + "Share: %{percent}<extra></extra>"
                        ),
                        marker=dict(line=dict(color="#0B0F19", width=2)),
                     )

                       fig.update_layout(
                        paper_bgcolor="#0B0F19",
                        plot_bgcolor="#111827",
                        font_color="#F1F5F9",
                        title_x=0.02,
                        showlegend=True,
                        legend=dict(orientation="v", x=1.02, y=0.5),
                        margin=dict(l=20, r=140, t=65, b=25),
                     )
                       st.plotly_chart(fig,use_container_width=True)

                    elif chart_type == "Line Chart":
                        chart_data = df[[x_column, y_column]].copy()
                        chart_data[x_column] = pd.to_datetime(
                            chart_data[x_column], errors="coerce"
                        )

                        chart_data = chart_data.dropna(subset=[x_column])

                        if not chart_data.empty:
                            chart_data = (
                                chart_data.groupby(x_column, as_index=False)[y_column]
                                .sum()
                                .sort_values(x_column)
                            )

                            fig = px.line(
                                chart_data,
                                x=x_column,
                                y=y_column,
                                title=f"{y_column} Over Time",
                                markers=True,
                                template="plotly_dark",
                            )

                            fig.update_traces(
                                line=dict(color="#60A5FA", width=3),
                                marker=dict(size=7, color="#93C5FD"),
                                hovertemplate=(
                                    "%{x|%b %d, %Y}<br>"
                                    + y_column
                                    + ": %{y:,.2f}<extra></extra>"
                                ),
                            )

                            fig.update_layout(
                                paper_bgcolor="#0B0F19",
                                plot_bgcolor="#111827",
                                font_color="#F1F5F9",
                                title_x=0.02,
                                margin=dict(l=20, r=20, t=65, b=45),
                                hovermode="x unified",
                            )

                            fig.update_xaxes(
                                tickformat="%b %d",
                                tickangle=-35,
                                title="Date",
                                showgrid=False,
                            )
                            fig.update_yaxes(
                                title=y_column,
                                gridcolor="#253247",
                                zeroline=False,
                            )

                            st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.warning("No valid dates were found in the selected X-axis column.")


    except Exception as e:
        st.error(f"Could not load the uploaded file: {e}")
else:
    st.info("Upload a CSV or Excel file to begin.")
