# streamlit_app.py
import streamlit as st
import json
from docx import Document
import re

st.set_page_config(page_title="Weekly Lesson Plan Generator", layout="wide")
st.title("📄 Weekly Lesson Plan Generator")

# -----------------------------
# Function to populate Word template
# -----------------------------
def populate_lesson_plan(json_data, template_path, output_path):
    """
    Populates a Word template with lesson plan JSON data.
    Supports both nested 'Classes' JSON and flat JSON.
    """
    doc = Document(template_path)
    
    def escape_for_regex(text):
        if not text:
            return ""
        return re.escape(str(text))
    
    # --- Top-level placeholders ---
    top_fields = ["Teacher","Year/Class","Subject","Unit/Topic","Week number","Date"]
    for field in top_fields:
        if field in json_data:
            for p in doc.paragraphs:
                p.text = re.sub(r"\{\{" + field + r"\}\}", escape_for_regex(json_data[field]), p.text)

    # --- Nested Classes ---
    if "Classes" in json_data:
        for class_key, class_obj in json_data["Classes"].items():
            for placeholder, value in class_obj.items():
                for p in doc.paragraphs:
                    p.text = re.sub(r"\{\{" + placeholder + r"\}\}", escape_for_regex(value), p.text)

    # --- Flattened placeholders ---
    for placeholder, value in json_data.items():
        if placeholder not in top_fields and placeholder != "Classes":
            for p in doc.paragraphs:
                p.text = re.sub(r"\{\{" + placeholder + r"\}\}", escape_for_regex(value), p.text)

    doc.save(output_path)
    return output_path

# -----------------------------
# Streamlit UI
# -----------------------------
st.write("Upload your lesson plan JSON file or paste JSON data to populate your 5-day Word template.")

# Upload JSON file
uploaded_file = st.file_uploader("Upload JSON", type="json")
if uploaded_file:
    lesson_json = json.load(uploaded_file)
    output_file = populate_lesson_plan(lesson_json, "templates/WLPT.docx", "WeeklyLessonPlan_output.docx")
    st.success(f"Lesson plan generated: {output_file}")
    st.download_button("Download Lesson Plan", output_file, file_name="WeeklyLessonPlan_output.docx")

# Or paste JSON directly
json_input = st.text_area("Or paste JSON here:")
if st.button("Generate from pasted JSON") and json_input:
    try:
        lesson_json = json.loads(json_input)
        output_file = populate_lesson_plan(lesson_json, "templates/WLPT.docx", "WeeklyLessonPlan_output.docx")
        st.success(f"Lesson plan generated: {output_file}")
        st.download_button("Download Lesson Plan", output_file, file_name="WeeklyLessonPlan_output.docx")
    except Exception as e:
        st.error(f"Error parsing JSON: {e}")
