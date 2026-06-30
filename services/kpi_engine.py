from turtle import st

from app import df

numeric_cols = df.select_dtypes(
    include="number"
)

st.metric()



