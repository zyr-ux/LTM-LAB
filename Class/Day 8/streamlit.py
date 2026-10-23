import streamlit as st

st.title('This is my 1st Streamlit app')
st.write('Hello World')
st.error('I NEED YOUR NAME')


name = st.text_input("Enter your name")

if name != "":
    st.warning(f"{name.title()} you failed. SHAME ON YOU")