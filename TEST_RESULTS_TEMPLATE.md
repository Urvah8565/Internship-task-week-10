# Test Results

The InsightAI prototype was tested using the sample sales dataset with multiple natural-language queries.

| Test ID | Input Question | Expected Behavior | Actual Result | Status |
|---|---|---|---|---|
| T1 | What is the total revenue? | Calculate total from Revenue column | Total Revenue: **4,380,000.00** |  Pass |
| T2 | What is the average revenue? | Calculate average Revenue | Average Revenue: **438,000.00** |  Pass |
| T3 | Which region has the highest revenue? | Identify region with highest grouped revenue | **South — 1,670,000.00** |  Pass |
| T4 | Which region has the highest quantity? | Identify region with highest grouped quantity | **South — 51** |  Pass |
| T5 | How many rows are there? | Return dataset row count | **10 rows** |  Pass |

## Automated Validation

The core Pandas analysis functions were validated using automated tests.

```bash
pytest -q