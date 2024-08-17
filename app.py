import streamlit as st

# Set up the Streamlit page
st.title("Value Alignment Evaluation")

# Text inputs
name = st.text_input("Name")
gender = st.selectbox("Gender", ["Male", "Female"])
action = st.text_input("Action", placeholder="e.g., switch to a remote job or volunteer")

# Whole number input for age
age = st.number_input("Age", min_value=0, max_value=120, step=1, format="%d")

# Real number inputs for Integrity, Sustainability, Community with at most one decimal point
integrity = st.number_input("Integrity", min_value=0.0, max_value=1.0, step=0.1, format="%.1f")
sustainability = st.number_input("Sustainability", min_value=0.0, max_value=1.0, step=0.1, format="%.1f")
community = st.number_input("Community", min_value=0.0, max_value=1.0, step=0.1, format="%.1f")

# Submit button
if st.button("Submit"):
    # Process the inputs
    st.write("Submitted Information:")
    st.write(f"Name: {name}")
    st.write(f"Gender: {gender}")
    st.write(f"Age: {age}")
    st.write(f"Action: {action}")
    st.write(f"Integrity: {integrity}")
    st.write(f"Sustainability: {sustainability}")
    st.write(f"Community: {community}")
