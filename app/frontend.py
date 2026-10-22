
import streamlit as st


def apply_theme():
    """Apply InsightAI's dark premium theme."""
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
        }

        .block-container {
            max-width: 1500px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        .insight-header {
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            border: 1px solid var(--border);
            border-radius: 16px;
            background: linear-gradient(120deg, #111827, #152238);
        }

        .insight-header h1 {
            margin: 0;
            color: #F8FAFC;
            font-size: 2rem;
        }

        .insight-header p {
            margin: 0.5rem 0 0;
            color: var(--muted);
        }

        [data-testid="stMetric"] {
            background: var(--panel);
            border: 1px solid var(--border);
            padding: 1rem;
            border-radius: 14px;
        }

        [data-testid="stMetricValue"] {
            color: var(--blue);
        }

        [data-testid="stFileUploader"] {
            background: var(--panel);
            border: 1px dashed #3B82F6;
            border-radius: 14px;
            padding: 0.75rem;
        }

        .stButton button[kind="primary"] {
            background: #2563EB;
            border: 1px solid #3B82F6;
            border-radius: 10px;
            font-weight: 600;
        }

        [data-testid="stDataFrame"] {
            border: 1px solid var(--border);
            border-radius: 12px;
        }

        hr {
            border-color: var(--border);
        }
    </style>
    """, unsafe_allow_html=True)


def render_sidebar():
    """Render InsightAI navigation."""
    with st.sidebar:
        st.title("📊 InsightAI")
        st.caption("AI-powered data intelligence")
        st.divider()

        st.markdown("### Workspace")
        st.markdown("📁 Dataset Analysis")
        st.markdown("📈 Visualizations")

        st.divider()
        st.caption("Powered by Groq + Pandas")


def render_header():
    """Render the main dashboard header."""
    st.markdown("""
    <div class="insight-header">
        <h1>InsightAI</h1>
        <p>
            Turn your data into insights. Upload a dataset,
            ask questions, and explore the results.
        </p>
    </div>
    """, unsafe_allow_html=True)


def render_kpis(df):
    """Display key dataset statistics."""
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Rows", f"{len(df):,}")

    with col2:
        st.metric("Total Columns", f"{len(df.columns):,}")

    with col3:
        numeric_count = len(
            df.select_dtypes(include="number").columns
        )
        st.metric("Numeric Columns", f"{numeric_count:,}")


        
def render_analysis_result(result):
    """Display analysis results in the InsightAI dashboard."""
    st.markdown("###  Analysis Results")

    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, #111827, #172554);
            border: 1px solid #2B4265;
            border-radius: 14px;
            padding: 20px 24px;
            margin: 12px 0;
        ">
            <div style="
                color: #93C5FD;
                font-size: 13px;
                font-weight: 600;
                margin-bottom: 8px;
            ">INSIGHTAI RESULT</div>
            <div style="
                color: #F8FAFC;
                font-size: 20px;
                font-weight: 600;
            ">{result["summary"]}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if result.get("table") is not None:
        st.markdown("#### Detailed results")
        st.dataframe(result["table"], use_container_width=True)

    if result.get("explanation"):
        st.caption(result["explanation"])

