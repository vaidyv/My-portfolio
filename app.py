import streamlit as st
import pandas as pd
import plotly.express as px
from plotly import colors
from utils.insights import generate_insight

#st.set_page_config(page_title="Filtered Sales Dashboard", layout="wide")
#st.title("📊 Filtered Sales Dashboard")
df = pd.read_csv("data/sales_data.csv")

st.set_page_config(
    page_title="Sales Data",
    page_icon="🌦️",
    layout="wide",
)

#uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

# Load data
#if uploaded_file is None:
   # st.info("Please upload a CSV to continue.")
   # st.stop()

#try:
    #df = pd.read_csv(uploaded_file)
    #st.success("✅ CSV loaded successfully")
#except Exception as e:
    #st.error(f"❌ Something went wrong: {e}")
    #st.stop()

# Sidebar filters
st.sidebar.header("Filters")
#region_options = ["All"] + sorted(df['region'].unique().tolist())
region_options = ["All"] + sorted(df['region'].unique().tolist())
region = st.sidebar.selectbox("Choose Region", region_options, index=0)

product_options = ["All"] + sorted(df['product'].unique().tolist())
product = st.sidebar.multiselect("Choose Product", product_options, default=["All"])

# Filter data
if region == "All" and ("All" in product or len(product) == 0):
    filtered_df = df
elif region == "All" and "All" not in product:
    filtered_df = df[df['product'].isin(product)]
elif region != "All" and ("All" in product or len(product) == 0):
    filtered_df = df[df['region'] == region]
else:
    filtered_df = df[(df['region'] == region) & (df['product'].isin(product))]

# Show filtered table
st.subheader(f" Sales Data for Region: {region}")
st.dataframe(filtered_df)

cols = st.columns(2)

# Bar chart: total sales by region
with cols[0].container(border=True, height="stretch"):
    if region != "All":
        st.subheader(f"Total Sales by Region: {region}")
    else:
        st.subheader(f"Total Sales by Region")
    if filtered_df.empty:
        st.warning("No data available for the selected filters.")
    else:
        agg_df = (
            filtered_df.groupby('region', as_index=False)['total_sales']
            .sum()
            .sort_values('total_sales')
        )

        # Custom navy gradient shades like the reference image
        color_sequence = ['#2E5266', '#1B3A57', '#235D7A', '#1A4A63', '#4A90B8']

        fig = px.funnel(
            agg_df,
            x='total_sales',
            y='region',
            color='region',
            color_discrete_sequence=color_sequence,
            labels={
                'region': 'Region',
                'total_sales': 'Total Sales'
            }
        )

        fig.update_traces(
            texttemplate='%{value:,.0f}K',
            textposition='inside',
            textfont=dict(size=13, color='white', family='Arial Black'),
            connector=dict(visible=False),
            opacity=1
        )

        fig.update_layout(
            showlegend=False,
            xaxis_title=None,
            yaxis_title=None,
            xaxis_visible=False,
            yaxis=dict(
                tickfont=dict(size=15, color='black', family='Arial'),
                automargin=True
            ),
            margin=dict(l=10, r=10, t=10, b=10),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, use_container_width=True)

# Bar chart: total sales by product
with cols[1].container(border=True, height="stretch"):
    if region != "All":
        st.subheader(f"📦 Total Sales by Product in {region}")
    else:
        st.subheader(f"Total Sales by Product")
    if filtered_df.empty:
        st.warning("No data available for the selected filters.")
    else:
        if 'status' in filtered_df.columns:
            agg_df = (
                filtered_df.groupby(['product', 'status'], as_index=False)['total_sales']
                .sum()
            )
            color_col = 'status'
        else:
            agg_df = (
                filtered_df.groupby('product', as_index=False)['total_sales']
                .sum()
            )
            color_col = None

        sorted_products = (
            agg_df.groupby('product')['total_sales']
            .sum()
            .sort_values(ascending=False)
            .index
        )

        # Muted, professional status colors
        status_colors = {
            "Cancelled": "#C0504D",   # muted red
            "Pending": "#4F81BD",     # muted blue
            "Completed": "#77933C"    # muted green
        }

        fig = px.bar(
            agg_df,
            x='product',
            y='total_sales',
            color=color_col,
            category_orders={'product': sorted_products},
            color_discrete_map=status_colors if color_col else None,
        )

        fig.update_traces(textposition='none', opacity=0.85)

        fig.update_layout(
            xaxis_title=None,
            yaxis_title=None,
            yaxis_visible=False,
            xaxis=dict(tickfont=dict(size=13, color='black', family='Arial'))
        )

        totals = agg_df.groupby('product')['total_sales'].sum().reindex(sorted_products)

        for product, total in totals.items():
            fig.add_annotation(
                x=product,
                y=total,
                text=f"{total:,.0f}K",
                showarrow=False,
                yshift=15,
                font=dict(size=12, color='black', family='Arial Black')
            )
        st.plotly_chart(fig, use_container_width=True)

cols = st.columns(2)

# Bar chart: unit price by sales rep
with cols[0].container(border=True, height="stretch"):
    st.subheader("Total Sales by Sales Rep")
    if filtered_df.empty:
        st.warning("No data available for the selected filters.")
    else:
        agg_df = (
            filtered_df.groupby('sales_rep', as_index=False)['total_sales']
            .mean()
        )

        sorted_reps = (
            agg_df.groupby('sales_rep')['total_sales']
            .mean()
            .sort_values(ascending=False)
            .index
        )

        fig = px.bar(
            agg_df,
            x='sales_rep',
            y='total_sales',
            category_orders={'sales_rep': sorted_reps},
            labels={
                'sales_rep': 'Sales Rep',
                'total_sales': 'Total Sales'
            },
            text='total_sales'
        )

        fig.update_traces(
            texttemplate='%{text:,.0f}K',
            textposition='inside',
            textfont=dict(size=12, color='black', family='Arial Black'),
            marker_color='#4F81BD'
        )

        fig.update_layout(
            xaxis_title=None,
            yaxis_title=None,
            yaxis_visible=False,
            xaxis=dict(tickfont=dict(size=12, color='black', family='Arial'))
        )

        st.plotly_chart(fig, use_container_width=True)

# Line chart: quantity ordered over time
with cols[1].container(border=True, height="stretch"):
    if region != 'All':
        st.subheader(f"📈 Quantity Ordered Over Time in {region}")
    else:
        st.subheader(f"📈 Quantity Ordered Over Time")
    if filtered_df.empty:
        st.warning("No data available for the selected filters.")
    else:
        filtered_df['order_date'] = pd.to_datetime(filtered_df['order_date'])

        qty_by_date = (
            filtered_df.groupby('order_date', as_index=False)['quantity']
            .sum()
            .sort_values('order_date')
        )

        fig_qty = px.line(
            qty_by_date,
            x='order_date',
            y='quantity',
            markers=True,
            labels={
                'order_date': 'Order Date',
                'quantity': 'Quantity Ordered'
            }
        )

        fig_qty.update_traces(
            line=dict(width=2),
            marker=dict(size=6)
        )
        fig_qty.update_layout(
            xaxis_title=None,
            yaxis_title=None,
            yaxis_visible=False,
            xaxis=dict(tickfont=dict(size=12, color='black', family='Arial'))
        )

        st.plotly_chart(fig_qty, use_container_width=True)
# AI Insight
st.subheader("🔍 AI Insight")
st.info(generate_insight(filtered_df))