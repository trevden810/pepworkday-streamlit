import streamlit as st
import pandas as pd

st.title("Test Streamlit App")
st.write("Hello, this is a test app to verify Streamlit installation.")

# Create a sample DataFrame
data = {'Column 1': [1, 2, 3],
        'Column 2': ['A', 'B', 'C']}
df = pd.DataFrame(data)

# Display the DataFrame
st.write("Sample DataFrame:")
st.dataframe(df)
