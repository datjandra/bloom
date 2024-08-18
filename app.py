import streamlit as st
import os
import random
import plotly.graph_objects as go
from fpdf import FPDF
import io

SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT")
INPUT_PROMPT = os.getenv("INPUT_PROMPT")

# Function to save radar chart as PDF
def save_pdf(fig, data, integrity, sustainability, community):
    pdf = FPDF()
    pdf.add_page()
    
    # Add title
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Personal Evaluation Report", ln=True, align='C')

    return pdf.output(dest='S')

def main():
    # Set up the Streamlit page
    st.title("Value Alignment Evaluation")
    
    # Text inputs
    st.subheader("User")
    name = st.text_input("Name", value="John")
    gender = st.selectbox("Gender", ["Male", "Female"])
    age = st.number_input("Age", min_value=1, max_value=120, value=18, step=1, format="%d")
    action = st.text_input("Action", value="switching to a remote job")
    
    # Real number inputs for Integrity, Sustainability, Community with at most one decimal point
    st.subheader("Values")
    integrity = st.number_input("Integrity", min_value=0.0, max_value=1.0, step=0.1, format="%.1f", value=round(random.uniform(0, 1), 1))
    sustainability = st.number_input("Sustainability", min_value=0.0, max_value=1.0, step=0.1, format="%.1f", value=round(random.uniform(0, 1), 1))
    community = st.number_input("Community", min_value=0.0, max_value=1.0, step=0.1, format="%.1f", value=round(random.uniform(0, 1), 1))
    
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
        
        # JSON data
        data = {
            "stress_level": 0.4,
            "stress_level_rationale": "Lower stress due to reduced commute and work-life balance",
            "happiness": 0.6,
            "happiness_rationale": "Increased happiness due to flexibility and reduced office distractions",
            "financial_stability": 0.9,
            "financial_stability_rationale": "Higher financial stability due to reduced living expenses and flexible work schedule",
            "social_connections": 0.3,
            "social_connections_rationale": "Potential decrease in social connections due to reduced face-to-face interactions"
        }
        
        # Extract values for the radar chart
        categories = ['Stress Level', 'Happiness', 'Financial Stability', 'Social Connections']
        values = [
            data['stress_level'],
            data['happiness'],
            data['financial_stability'],
            data['social_connections']
        ]
        
        # Create radar chart using Plotly
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name='Evaluation'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                )
            ),
            showlegend=False,
            title="Personal Evaluation Report"
        )
        
        # Display radar chart in Streamlit
        st.plotly_chart(fig)
        
        # Display rationales
        st.write("### Summary")
        st.write(f"**Stress Level:** {data['stress_level_rationale']}")
        st.write(f"**Happiness:** {data['happiness_rationale']}")
        st.write(f"**Financial Stability:** {data['financial_stability_rationale']}")
        st.write(f"**Social Connections:** {data['social_connections_rationale']}")

        pdf_output = save_pdf(fig, data, integrity, sustainability, community)
        st.download_button(
            label="Download PDF",
            data=pdf_output,
            file_name="personal_evaluation.pdf",
            mime="application/pdf"
        )

if __name__ == "__main__":
    main()
