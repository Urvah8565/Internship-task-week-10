
import pandas as pd
from tools.analysis_tool import analyze

def make_df():
    return pd.DataFrame({
        "Product": ["Laptop","Phone","Laptop","Tablet"],
        "Region": ["North","South","South","West"],
        "Quantity": [10,20,8,15],
        "Revenue": [500000,400000,400000,450000],
    })

def test_total():
    r = analyze(make_df(), "What is the total revenue?", None)
    assert "1,750,000.00" in r["summary"]

def test_average():
    r = analyze(make_df(), "What is the average revenue?", None)
    assert "437,500.00" in r["summary"]

def test_highest_region():
    r = analyze(make_df(), "Which region has the highest revenue?", None)
    assert "South" in r["summary"]

def test_count():
    r = analyze(make_df(), "How many rows are there?", None)
    assert "4" in r["summary"]
