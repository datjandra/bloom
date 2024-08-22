import streamlit as st
import os
import random
import plotly.graph_objects as go
from fpdf import FPDF
from fpdf.enums import XPos, YPos
import io
from clarifai.client.model import Model
import regex
import json
import time

SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT")
INPUT_PROMPT = os.getenv("INPUT_PROMPT")

# Function to save radar chart as PDF
def save_pdf(name, gender, age, decision, fig, data, integrity, sustainability, community):
    # Create a PDF
    pdf = FPDF()
    pdf.add_page()
    
    pdf.set_font("helvetica", size=12)
    pdf.cell(200, 10, text="User", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(200, 10, text=f"Name: {name}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(200, 10, text=f"Gender: {gender}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(200, 10, text=f"Age: {age}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.multi_cell(0, 10, text=f"Decision: {decision}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.ln()
    pdf.cell(200, 10, text="Values", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(200, 10, text=f"Integrity: {integrity}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(200, 10, text=f"Sustainability: {sustainability}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(200, 10, text=f"Community: {community}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    img_bytes = fig.to_image(format="png", engine="kaleido")
    image = io.BytesIO(img_bytes)
    pdf.image(image, x=10, w=180)

    pdf.ln(130)  # Move cursor to the next line
    pdf.set_font("helvetica", size=10)
    pdf.cell(200, 10, text="Explanations", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.multi_cell(0, 10, text=f"Stress Level: {data['stress_level_rationale']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.multi_cell(0, 10, text=f"Happiness: {data['happiness_rationale']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.multi_cell(0, 10, text=f"Financial Stability: {data['financial_stability_rationale']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.multi_cell(0, 10, text=f"Social Connections: {data['social_connections_rationale']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    return bytes(pdf.output())

def extract_json(text):
    # Define a regular expression pattern to match the JSON structure
    pattern = regex.compile(r'\{(?:[^{}]|(?R))*\}')
    
    # Find all matches of the JSON pattern in the input text
    matches = pattern.findall(text)
    
    # Assuming there is only one JSON structure in the input text
    json_string = matches[0] if matches else None
    
    # Parse the JSON string into a Python dictionary
    if json_string:
        try:
            json_data = json.loads(json_string)
            return json_data
        except json.JSONDecodeError as e:
            # Error decoding JSON
            return None
    else:
        # No JSON structure found
        return None

def predict_outcomes(name, gender, age, decision, integrity, sustainability, community):
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
                    
    input_prompt = INPUT_PROMPT.format(name=name, 
                                       age=age, 
                                       gender_subject=gender_subject, 
                                       gender_possessive=gender_possessive, 
                                       decision=decision, 
                                       integrity=integrity, 
                                       sustainability=sustainability, 
                                       community=community)
    prompt_template = f'''<|begin_of_text|><|start_header_id|>system<|end_header_id|>
    
    {SYSTEM_PROMPT}<|eot_id|><|start_header_id|>user<|end_header_id|>
    
    {input_prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>'''

    inference_params = dict(temperature=0.7, 
                            max_tokens=256, 
                            top_k=50, 
                            top_p= 0.95, 
                            prompt_template=prompt_template, 
                            system_prompt=SYSTEM_PROMPT)

    model_prediction = Model("https://clarifai.com/meta/Llama-3/models/llama-3_1-8b-instruct").predict_by_bytes(input_prompt.encode(), input_type="text", inference_params=inference_params)
    return model_prediction.outputs[0].data.text.raw
    
def main():
    st.set_page_config(page_title="Bloom", page_icon='🌼')
    st.title("Value Alignment Evaluation")
    
    with st.form("scenario_form"):
        st.subheader("User")
        name = st.text_input("Name", value="John Smith")
        gender = st.selectbox("Gender", ["Male", "Female"])
        age = st.number_input("Age", min_value=1, max_value=120, value=50, step=1, format="%d")
        decision = st.text_area("Decision", value="John wants to take a remote job as a software engineer. He is married with a wife, two teenage kids and a mortgage.")

        if 'value_integrity' in st.session_state:
            integrity_value = st.session_state['value_integrity']
        else:
            integrity_value = random.randint(0, 10)

        if 'value_sustainability' in st.session_state:
            sustainability_value = st.session_state['value_sustainability']
        else:
            sustainability_value = random.randint(0, 10)

        if 'value_community' in st.session_state:
            community_value = st.session_state['value_community']
        else:
            community_value = random.randint(0, 10)
        
        st.subheader("Values")
        integrity = st.slider("Integrity", min_value=0, max_value=10, step=1, value=integrity_value, key="value_integrity")
        sustainability = st.slider("Sustainability", min_value=0, max_value=10, step=1, value=sustainability_value, key="value_sustainability")
        community = st.slider("Community", min_value=0, max_value=10, step=1, value=community_value, key="value_community")
        
        submit_button = st.form_submit_button("Submit")
        if submit_button:
            with st.spinner('Report may take a few minutes to create, please wait...'):
                # Process the inputs
                start_time = time.time()
                text_raw = predict_outcomes(name, gender, age, decision, integrity, sustainability, community)
                data = extract_json(text_raw)
                end_time = time.time()
                elapsed_time = int(end_time - start_time)
                
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
                            range=[0, 10]
                        )
                    ),
                    showlegend=False,
                    title="Personal Evaluation Report"
                )
                
                # Display radar chart in Streamlit
                st.plotly_chart(fig)
                
                # Display rationales
                st.write("### Explanations")
                st.write(f"**Stress Level:** {data['stress_level_rationale']}")
                st.write(f"**Happiness:** {data['happiness_rationale']}")
                st.write(f"**Financial Stability:** {data['financial_stability_rationale']}")
                st.write(f"**Social Connections:** {data['social_connections_rationale']}")
    
                pdf_output = save_pdf(name, gender, age, decision, fig, data, integrity, sustainability, community)
                st.caption(f"Processing time: {elapsed_time} seconds")

    try:
        st.download_button(
            label="Download PDF",
            data=pdf_output,
            file_name="personal_evaluation.pdf",
            mime="application/pdf"
        )
    except:
        pass

if __name__ == "__main__":
    main()
