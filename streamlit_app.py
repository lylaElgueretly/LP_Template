# streamlit_app.py
import streamlit as st
from docx import Document
import json
import io
import os

st.set_page_config(page_title="Weekly Lesson Plan Generator", layout="wide")
st.title("📄 Weekly Lesson Plan Generator")

st.markdown(
    """
    Upload your lesson plan JSON file or paste JSON data to populate your 5-day Word template.
    You can also generate a **sample JSON** for all 5 days to use as a starting point.
    """
)

# Path to Word template
TEMPLATE_PATH = os.path.join("templates", "LessonPlanTemplate.docx")

if not os.path.exists(TEMPLATE_PATH):
    st.error(f"Template not found at {TEMPLATE_PATH}. Please check the templates folder.")
    st.stop()

# JSON input
json_file = st.file_uploader("Upload your lesson plan JSON file", type=["json"])
json_text = st.text_area("Or paste JSON here:")

# Optional: Generate sample JSON for all 5 days
if st.button("Generate Sample JSON for 5 Days"):
    sample_json = {
        f"Class{i}_{field}": f"Sample {field} for Class {i}" 
        for i in range(1, 6) 
        for field in [
            "LearningObjective", "SuccessCriteria", "Vocabulary", "KeyQuestions",
            "StarterActivity", "MainTeaching", "DifferentiatedActivities",
            "Plenary", "Reflection", "Homework"
        ]
    }
    st.code(json.dumps(sample_json, indent=4), language="json")
    st.stop()  # Stop here so user can copy the sample JSON

# Proceed if JSON is provided
if json_file or json_text:
    try:
        if json_file:
            data = json.load(json_file)
        else:
            data = json.loads(json_text)
    except Exception as e:
        st.error(f"Invalid JSON: {e}")
        st.stop()

    # Load Word template
    doc = Document(TEMPLATE_PATH)

    # Flatten nested JSON if needed
    def flatten_json(d, parent_key='', sep='_'):
        items = {}
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.update(flatten_json(v, new_key, sep=sep))
            else:
                items[new_key] = v
        return items

    flat_data = flatten_json(data)

    # Replace placeholders in paragraphs
    for paragraph in doc.paragraphs:
        for key, value in flat_data.items():
            placeholder = f"{{{{{key}}}}}"
            if placeholder in paragraph.text:
                paragraph.text = paragraph.text.replace(placeholder, str(value))

    # Replace placeholders in tables
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for key, value in flat_data.items():
                    placeholder = f"{{{{{key}}}}}"
                    if placeholder in cell.text:
                        cell.text = cell.text.replace(placeholder, str(value))

    # Save populated document to memory
    output = io.BytesIO()
    doc.save(output)
    output.seek(0)

    st.success("✅ Lesson plan generated successfully!")
    st.download_button(
        label="📥 Download Populated Lesson Plan",
        data=output,
        file_name="Weekly_Lesson_Plan.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
else:
    st.info("Please provide JSON data (file or paste) to generate the lesson plan.")
