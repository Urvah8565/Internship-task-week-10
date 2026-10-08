
import re
import pandas as pd

def _find_col(df, name):
    if not name:
        return None
    exact = {str(c).lower(): c for c in df.columns}
    if str(name).lower() in exact:
        return exact[str(name).lower()]
    for c in df.columns:
        if str(name).lower() in str(c).lower():
            return c
    return None

def _rule_based_plan(df, question):
    q = question.lower()
    numeric = df.select_dtypes(include="number").columns.tolist()
    text = df.select_dtypes(exclude="number").columns.tolist()

    metric = None
    for c in numeric:
        if str(c).lower() in q:
            metric = c
            break
    if metric is None and numeric:
        # common business metric preference
        for preferred in ["revenue", "sales", "amount", "price", "quantity"]:
            for c in numeric:
                if preferred in str(c).lower():
                    metric = c
                    break
            if metric is not None:
                break
        metric = metric or numeric[0]

    group = None
    for c in text:
        if str(c).lower() in q:
            group = c
            break
    if group is None:
        for preferred in ["region", "product", "category", "department"]:
            for c in text:
                if preferred in str(c).lower():
                    group = c
                    break
            if group is not None:
                break

    if "how many" in q or "count" in q:
        intent = "count_by"
    elif "average" in q or "mean" in q:
        intent = "average"
    elif "highest" in q or "maximum" in q or "most" in q:
        intent = "max"
    elif "lowest" in q or "minimum" in q or "least" in q:
        intent = "sum_by"
    elif "total" in q or "sum" in q:
        intent = "total"
    else:
        intent = "total"

    return {"intent": intent, "metric": metric, "group_by": group, "date_column": None}

def analyze(df, question, plan=None):
    if plan is None:
        plan = _rule_based_plan(df, question)

    intent = plan.get("intent")
    metric = _find_col(df, plan.get("metric"))
    group = _find_col(df, plan.get("group_by"))

    if intent in {"total", "average", "max"} and metric is None:
        raise ValueError("I could not identify a numeric column for this question.")

    if intent == "total":
        value = float(df[metric].sum())
        return {"summary": f"Total {metric}: {value:,.2f}", "table": None,
                "explanation": f"Calculated directly from the uploaded dataset using Pandas."}

    if intent == "average":
        value = float(df[metric].mean())
        return {"summary": f"Average {metric}: {value:,.2f}", "table": None,
                "explanation": "Calculated directly from the uploaded dataset using Pandas."}

    if intent == "max":
        if group is not None:
            table = df.groupby(group, dropna=False)[metric].sum().reset_index()
            table = table.sort_values(metric, ascending=False)
            winner = table.iloc[0]
            return {
                "summary": f"{winner[group]} has the highest total {metric}: {winner[metric]:,.2f}",
                "table": table,
                "explanation": "The values were grouped and calculated with Pandas; the LLM only interprets the question."
            }
        value = float(df[metric].max())
        return {"summary": f"Maximum {metric}: {value:,.2f}", "table": None,
                "explanation": "Calculated directly from the uploaded dataset using Pandas."}

    if intent == "sum_by":
        if group is None:
            raise ValueError("A grouping column is required for this question.")
        table = df.groupby(group, dropna=False)[metric].sum().reset_index()
        table = table.sort_values(metric, ascending=False)
        return {"summary": f"Grouped total {metric} calculated by {group}.", "table": table,
                "explanation": "Grouped aggregation performed with Pandas."}

    if intent == "count_by":
        if "row" in question.lower() or "record" in question.lower():
            value = int(len(df))
            return {"summary": f"Row count: {value:,}", "table": None,
                    "explanation": "Count calculated directly with Pandas."}
        if group is None:
            value = int(len(df))
            return {"summary": f"Row count: {value:,}", "table": None,
                    "explanation": "Count calculated directly with Pandas."}
        table = df[group].value_counts(dropna=False).reset_index()
        table.columns = [group, "count"]
        return {"summary": f"Count calculated by {group}.", "table": table,
                "explanation": "Counts calculated directly with Pandas."}

    if intent == "trend":
        raise ValueError("Trend analysis is planned for the next prototype iteration.")

    raise ValueError(f"Unsupported analysis intent: {intent}")
