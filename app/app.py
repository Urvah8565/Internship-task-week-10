
import os, json, re
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

from tools.analysis_tool import analyze

load_dotenv()

st.set_page_config(page_title="InsightAI", page_icon="📊", layout="wide")
st.title("📊 InsightAI — AI-Powered Data Analysis Agent")
st.caption("Prototype: natural-language questions → AI interpretation → Pandas computation → explanation")

uploaded = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx", "xls"])

if uploaded:
    try:
        if uploaded.name.lower().endswith(".csv"):
            df = pd.read_csv(uploaded)
        else:
            df = pd.read_excel(uploaded)

        st.success(f"Loaded {len(df):,} rows × {len(df.columns)} columns")
        with st.expander("Dataset preview"):
            st.dataframe(df.head(10), use_container_width=True)

        st.write("**Columns:**", ", ".join(map(str, df.columns)))

        question = st.text_input(
            "Ask a question about your data",
            placeholder="Which region generated the highest revenue?"
        )

        if st.button("Analyze", type="primary") and question:
            api_key = os.getenv("GROQ_API_KEY")

            if not api_key:
                st.warning("GROQ_API_KEY is not set. Using the built-in rule-based prototype parser.")
                plan = None
            else:
                from agents.data_agent import create_analysis_plan
                try:
                    plan = create_analysis_plan(question, df.columns.tolist(), api_key)
                except Exception as e:
                    st.error(f"LLM planning failed: {e}")
                    plan = None

            try:
                result = analyze(df, question, plan)
                st.subheader("Result")
                st.metric("Analysis", result["summary"])
                if result.get("table") is not None:
                    st.dataframe(result["table"], use_container_width=True)
                if result.get("explanation"):
                    st.info(result["explanation"])
            except Exception as e:
                st.error(f"Could not analyze the question: {e}")
    except Exception as e:
        st.error(f"Could not load the uploaded file: {e}")
else:
    st.info("Upload a CSV or Excel file to begin.")
