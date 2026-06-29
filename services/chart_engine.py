# import plotly.express as px
# from narwhals.selectors import categorical, numeric
# from pandas import col
#
#
# def recommend_chart(df):
#     charts = []
#
#     for cols in df.columns:
#         if df[col].dtype == "object":
#             category_col = col
#         elif df[col].dtype in ["int64", "float64"]:
#             numeric_col = col
#
#     return charts
#
# if categorical and numeric:
#     chart_type = "bar"
#
# if date_column and numeric:
#     chart_type = "line"
#
# def generate_bar_chart(df, x, y):
#     return {
#         "type": "bar",
#         "x": df[x].tolist(),
#         "y": df[y].tolist()
#     }
#
# def generate_charts(df):
#     charts = []
#
#     numeric_cols = df.select_dtypes(include="number").columns
#     cat_cols = df.select_dtypes(include="object").columns
#
#     if len(cat_cols) > 0 and len(numeric_cols) > 0:
#         charts.append({
#             "type": "bar",
#             "x": cat_cols[0],
#             "y": numeric_cols[0]
#         })
#
#     return charts


import plotly.express as px
import pandas as pd


def recommend_chart(df):
    """
    Analyses a dataframe and returns a list of recommended chart configurations
    based on the column types present.
    """
    charts = []

    # Identify column types
    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
    cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
    date_cols = df.select_dtypes(include=["datetime64"]).columns.tolist()

    # Bar chart: categorical + numeric
    if len(cat_cols) > 0 and len(numeric_cols) > 0:
        charts.append({
            "type": "bar",
            "x": cat_cols[0],
            "y": numeric_cols[0],
            "description": f"Bar chart of {numeric_cols[0]} by {cat_cols[0]}"
        })

    # Line chart: date + numeric
    if len(date_cols) > 0 and len(numeric_cols) > 0:
        charts.append({
            "type": "line",
            "x": date_cols[0],
            "y": numeric_cols[0],
            "description": f"Line chart of {numeric_cols[0]} over time"
        })

    # Scatter chart: two numeric columns
    if len(numeric_cols) >= 2:
        charts.append({
            "type": "scatter",
            "x": numeric_cols[0],
            "y": numeric_cols[1],
            "description": f"Scatter plot of {numeric_cols[0]} vs {numeric_cols[1]}"
        })

    # Histogram: single numeric column
    if len(numeric_cols) >= 1:
        charts.append({
            "type": "histogram",
            "x": numeric_cols[0],
            "description": f"Distribution of {numeric_cols[0]}"
        })

    return charts


def generate_bar_chart(df, x, y):
    """
    Generates a Plotly bar chart figure from a dataframe.
    Returns both a raw data dict and a Plotly figure.
    """
    fig = px.bar(df, x=x, y=y, title=f"{y} by {x}")

    return {
        "type": "bar",
        "x": df[x].tolist(),
        "y": df[y].tolist(),
        "figure": fig
    }


def generate_line_chart(df, x, y):
    """
    Generates a Plotly line chart figure from a dataframe.
    """
    fig = px.line(df, x=x, y=y, title=f"{y} over {x}")

    return {
        "type": "line",
        "x": df[x].tolist(),
        "y": df[y].tolist(),
        "figure": fig
    }


def generate_scatter_chart(df, x, y):
    """
    Generates a Plotly scatter chart figure from a dataframe.
    """
    fig = px.scatter(df, x=x, y=y, title=f"{x} vs {y}")

    return {
        "type": "scatter",
        "x": df[x].tolist(),
        "y": df[y].tolist(),
        "figure": fig
    }


def generate_charts(df):
    """
    Master function — recommends charts and generates Plotly figures
    for each recommendation automatically.
    """
    recommendations = recommend_chart(df)
    charts = []

    for rec in recommendations:
        chart_type = rec["type"]

        if chart_type == "bar":
            chart = generate_bar_chart(df, rec["x"], rec["y"])

        elif chart_type == "line":
            chart = generate_line_chart(df, rec["x"], rec["y"])

        elif chart_type == "scatter":
            chart = generate_scatter_chart(df, rec["x"], rec["y"])

        elif chart_type == "histogram":
            fig = px.histogram(df, x=rec["x"], title=f"Distribution of {rec['x']}")
            chart = {
                "type": "histogram",
                "x": df[rec["x"]].tolist(),
                "figure": fig
            }

        else:
            continue

        chart["description"] = rec["description"]
        charts.append(chart)

    return charts


# ── Example usage ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Sample dataframe to test all chart types
    sample_data = {
        "category": ["Electronics", "Clothing", "Food", "Toys", "Sports"],
        "revenue": [45000, 32000, 28000, 19000, 37000],
        "units_sold": [1200, 3400, 8900, 2300, 1800],
        "date": pd.to_datetime([
            "2024-01-01", "2024-02-01", "2024-03-01",
            "2024-04-01", "2024-05-01"
        ])
    }

    df = pd.DataFrame(sample_data)

    print("Generating charts...\n")
    charts = generate_charts(df)

    for chart in charts:
        print(f"✅ {chart['type'].upper()} — {chart['description']}")
        if "figure" in chart:
            chart["figure"].show()