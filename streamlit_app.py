# streamlit_app.py
import streamlit as st
import json
from docx import Document
import re
import tempfile

st.set_page_config(page_title="Weekly Lesson Plan Generator", layout="wide")
st.title("📄 Weekly Lesson Plan Generator")

# -----------------------------
# Function to populate Word template
# -----------------------------
def populate_lesson_plan(json_data, template_path):
    """
    Populates a Word template with lesson plan JSON data.
    Replaces placeholders in both paragraphs and tables.
    Returns path to a safe temporary output file.
    """
    doc = Document(template_path)
    
    def replace_text_in_paragraphs(paragraphs, placeholder, value):
        for p in paragraphs:
            if "{{" + placeholder + "}}" in p.text:
                inline = p.runs
                for i in range(len(inline)):
                    if "{{" + placeholder + "}}" in inline[i].text:
                        inline[i].text = inline[i].text.replace("{{" + placeholder + "}}", str(value))

    def replace_text_in_tables(tables, placeholder, value):
        for table in tables:
            for row in table.rows:
                for cell in row.cells:
                    replace_text_in_paragraphs(cell.paragraphs, placeholder, value)

    # --- Top-level placeholders ---
    top_fields = ["Teacher","Year/Class","Subject","Unit/Topic","Week number","Date"]
    for field in top_fields:
        if field in json_data:
            replace_text_in_paragraphs(doc.paragraphs, field, json_data[field])
            replace_text_in_tables(doc.tables, field, json_data[field])

    # --- Nested Classes ---
    if "Classes" in json_data:
        for class_key, class_obj in json_data["Classes"].items():
            for placeholder, value in class_obj.items():
                replace_text_in_paragraphs(doc.paragraphs, placeholder, value)
                replace_text_in_tables(doc.tables, placeholder, value)

    # --- Flattened placeholders ---
    for placeholder, value in json_data.items():
        if placeholder not in top_fields and placeholder != "Classes":
            replace_text_in_paragraphs(doc.paragraphs, placeholder, value)
            replace_text_in_tables(doc.tables, placeholder, value)

    # Save to a safe temporary file
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".docx")
    doc.save(tmp_file.name)
    return tmp_file.name

# -----------------------------
# Streamlit UI
# -----------------------------
st.write("Upload your lesson plan JSON file or paste JSON data to populate your 5-day Word template.")

# Upload JSON file
uploaded_file = st.file_uploader("Upload JSON", type="json")
if uploaded_file:
    try:
        lesson_json = json.load(uploaded_file)
        output_file = populate_lesson_plan(lesson_json, "templates/WLPT.docx")
        st.success(f"Lesson plan generated successfully!")
        st.download_button("Download Lesson Plan", output_file, file_name="WeeklyLessonPlan_output.docx")
    except Exception as e:
        st.error(f"Error processing JSON: {e}")

# Or paste JSON directly
json_input = st.text_area("Or paste JSON here:")
if st.button("Generate from pasted JSON") and json_input:
    try:
        lesson_json = json.loads(json_input)
        output_file = populate_lesson_plan(lesson_json, "templates/WLPT.docx")
        st.success(f"Lesson plan generated successfully!")
        st.download_button("Download Lesson Plan", output_file, file_name="WeeklyLessonPlan_output.docx")
    except Exception as e:
        st.error(f"Error parsing JSON: {e}")
