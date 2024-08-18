import streamlit as st
import os

SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT")
INPUT_PROMPT = os.getenv("INPUT_PROMPT")

# Set up the Streamlit page
st.title("Value Alignment Evaluation")

# Text inputs
name = st.text_input("Name", value="John")
gender = st.selectbox("Gender", ["Male", "Female"])
action = st.text_input("Action", placeholder="e.g., switch to a remote job or volunteer")

# Whole number input for age
age = st.number_input("Age", min_value=1, max_value=120, value=18, step=1, format="%d")

# Real number inputs for Integrity, Sustainability, Community with at most one decimal point
integrity = st.number_input("Integrity", min_value=0.0, max_value=1.0, step=0.1, format="%.1f")
sustainability = st.number_input("Sustainability", min_value=0.0, max_value=1.0, step=0.1, format="%.1f")
community = st.number_input("Community", min_value=0.0, max_value=1.0, step=0.1, format="%.1f")

# Submit button
if st.button("Submit"):
    # Process the inputs
    # Determine gender-specific terms
    if gender == "Male":
        gender_subject = "He"
        gender_possessive = "His"
    elif gender == "Female":
        gender_subject = "She"
        gender_possessive = "Her"
    else:
        # Handle the case where gender is not recognized
        gender_subject = "They"
        gender_possessive = "Their"

    input_prompt = INPUT_PROMPT.format(name=name, age=age, gender_subject=gender_subject, gender_possessive=gender_possessive, action=action, integrity=integrity, sustainability=sustainability, community=community)
    prompt_template = f'''<|begin_of_text|><|start_header_id|>system<|end_header_id|>
    {SYSTEM_PROMPT}<|eot_id|><|start_header_id|>user<|end_header_id|>
    {input_prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>'''
    
    st.write("Submitted Information:")
    st.write(prompt_template)
