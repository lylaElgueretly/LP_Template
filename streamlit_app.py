# streamlit_app.py
import streamlit as st
import json
from docx import Document

st.set_page_config(page_title="Weekly Lesson Plan Generator", layout="wide")
st.title("📄 Weekly Lesson Plan Generator")

# -----------------------------
# Helper function to replace placeholders safely
# -----------------------------
def replace_placeholder_in_paragraph(paragraph, placeholder, value):
    """
    Replaces a placeholder in a paragraph, even if it's split across multiple runs.
    """
    full_text = "".join(run.text for run in paragraph.runs)
    placeholder_tag = f"{{{{{placeholder}}}}}"
    if placeholder_tag in full_text:
        # Clear all runs
        for run in paragraph.runs:
            run.text = ""
        # Assign new text to the first run
        paragraph.runs[0].text = full_text.replace(placeholder_tag, str(value))

def replace_placeholder_in_doc(doc, placeholder, value):
    """
    Replaces a placeholder in the entire document: paragraphs + tables.
    """
    # Replace in paragraphs
    for paragraph in doc.paragraphs:
        replace_placeholder_in_paragraph(paragraph, placeholder, value)
    # Replace in tables
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    replace_placeholder_in_paragraph(paragraph, placeholder, value)

# -----------------------------
# Function to populate Word template
# -----------------------------
def populate_lesson_plan(json_data, template_path, output_path):
    doc = Document(template_path)
    
    # Top-level placeholders
    top_fields = ["Teacher", "Year/Class", "Subject", "Unit/Topic", "Week number", "Date"]
    for field in top_fields:
        if field in json_data:
            replace_placeholder_in_doc(doc, field, json_data[field])
    
    # Nested Classes placeholders
    if "Classes" in json_data:
        for class_key, class_obj in json_data["Classes"].items():
            for placeholder, value in class_obj.items():
                replace_placeholder_in_doc(doc, placeholder, value)
    
    # Flattened JSON (in case placeholders are not nested)
    for placeholder, value in json_data.items():
        if placeholder not in top_fields and placeholder != "Classes":
            replace_placeholder_in_doc(doc, placeholder, value)
    
    doc.save(output_path)
    return output_path

# -----------------------------
# Streamlit UI
# -----------------------------
st.write("Upload your lesson plan JSON file or paste JSON data to populate your 5-day Word template.")

# Upload JSON file
uploaded_file = st.file_uploader("Upload JSON", type="json")
if uploaded_file:
    try:
        lesson_json = json.load(uploaded_file)
        output_file = populate_lesson_plan(lesson_json, "templates/WLPT.docx", "WeeklyLessonPlan_output.docx")
        st.success("✅ Lesson plan generated successfully!")
        st.download_button("Download Lesson Plan", output_file, file_name="WeeklyLessonPlan_output.docx")
    except Exception as e:
        st.error(f"Error parsing JSON: {e}")

# Or paste JSON directly
json_input = st.text_area("Or paste JSON here:")
if st.button("Generate from pasted JSON") and json_input:
    try:
        lesson_json = json.loads(json_input)
        output_file = populate_lesson_plan(lesson_json, "templates/WLPT.docx", "WeeklyLessonPlan_output.docx")
        st.success("✅ Lesson plan generated successfully!")
        st.download_button("Download Lesson Plan", output_file, file_name="WeeklyLessonPlan_output.docx")
    except Exception as e:
        st.error(f"Error parsing JSON: {e}")
