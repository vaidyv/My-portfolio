from turtle import st

import cols
import rows

from app import df

var = {
    "rows": len(df),
    "columns": len(df.columns),
    "missing_values": ...
}

st.metrics("Rows", rows)
st.metrics("Columns", cols)


