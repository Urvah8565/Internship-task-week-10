from pathlib import Path

readme = """# InsightAI — AI-Powered Data Analysis Agent

InsightAI is an AI-powered data analysis application that enables users to upload datasets, ask questions in natural language, and explore data-driven insights through an interactive dashboard.

The application combines Groq-powered question interpretation with Python and Pandas for numerical computation, and Plotly for interactive visualizations.

## Live Application

> **Try InsightAI:** [Open the live application](https://insightai-mvp-urvah-mansuri.streamlit.app/)

## Features

- **CSV and Excel Upload:** Upload datasets in CSV or Excel format.
- **Natural-Language Queries:** Ask questions about your dataset using everyday language.
- **AI-Powered Question Interpretation:** Use the Groq API to interpret data-analysis requests.
- **Pandas-Based Analysis:** Perform numerical calculations and grouped data analysis using Python and Pandas.
- **Dataset Preview:** Inspect uploaded data before analyzing it.
- **Statistical Operations:** Support available totals, averages, aggregations, and other implemented analyses.
- **Interactive Visualizations:** Generate bar charts, pie/donut charts, and line charts.
- **Interactive Dashboard:** Explore analysis results through a Streamlit interface.

**Important design principle:** The LLM interprets the user's question and helps determine the requested operation. Pandas performs the numerical calculations, rather than relying on the LLM to calculate the results directly.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| Streamlit | Interactive web interface |
| Pandas | Data processing and numerical analysis |
| Groq API | Natural-language question interpretation |
| Plotly Express | Interactive data visualizations |
| OpenPyXL | Excel file support |
| python-dotenv | Local environment-variable configuration |
| Pytest | Automated testing |

## Project Structure

```text
InsightAI/
├── agents/
│   └── data_agent.py
├── app/
│   ├── app.py
│   └── frontend.py
├── data/
├── tests/
├── tools/
├── .gitignore
├── requirements.txt
└── README.md
```

The structure above describes the main project directories and files. Additional files may exist in the repository.

## Getting Started

### Prerequisites

- Python installed on your system
- Git
- A Groq API key for AI-powered question interpretation

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd <YOUR_PROJECT_FOLDER>
```

Replace the placeholders with your actual repository URL and folder name.

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\\.venv\\Scripts\\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure the API key

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```
Replace the placeholder with your own API key.

### 5. Run the application

From the project root, run:

```bash
streamlit run app/app.py
```

## How It Works

1. The user uploads a CSV or Excel dataset.
2. InsightAI loads the dataset and provides a preview.
3. The user submits a natural-language question.
4. The Groq-powered component interprets the requested analysis.
5. Python and Pandas perform the supported calculations on the dataset.
6. InsightAI presents the result and, when requested, a visualization.

## Testing

The project uses Pytest for automated tests.

Run the test suite from the project root:

```bash
pytest
```

The test results depend on the current test suite and execution environment.

## Current Scope and Limitations

InsightAI is an MVP focused on tabular data analysis.

- Supported analyses depend on the implemented operations and the structure of the uploaded dataset.
- Results depend on data quality, column types, and the analysis request.
- AI-powered interpretation requires a valid Groq API key.
- The current application should not be considered a production-grade analytics platform without further security, reliability, and deployment testing.

## Future Enhancements

Potential improvements include:

- Automatic chart recommendations based on the user's question.
- More advanced statistical analysis and data-quality checks.
- Improved handling of missing values and large datasets.
- Downloadable analysis reports.
- Additional visualization types.
- Deployment and performance improvements.

## Author

**Urvah Mansuri**

## Project Status

InsightAI is an MVP under development. Features and documentation may evolve as the project improves.
"""
