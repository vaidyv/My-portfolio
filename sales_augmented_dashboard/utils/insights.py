import random

def generate_insight(agg_df):
    if agg_df.empty:
        return "No data available for this region."

    top_product = agg_df.groupby("product")["total_sales"].sum().idxmax()
    total = agg_df["total_sales"].sum()
    avg_order = agg_df["total_sales"].mean()
    best_sales_rep = agg_df.groupby("sales_rep")["total_sales"].sum().idxmax()

    insights = [
        f"💰 Total sales in this region: ${total:.2f}",
        f"🔥 Best-seller: {top_product}",
        f"📦 Average sales in this region: ${avg_order:.2f}",
        f"👤 Sales rep with maximum sales in this region: {best_sales_rep}"
    ]
    return "\n".join(f"- {i}" for i in insights)