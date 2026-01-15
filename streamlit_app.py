# streamlit_app.py
import streamlit as st
import json
from docx import Document

st.set_page_config(page_title="Weekly Lesson Plan Generator", layout="wide")
st.title("📄 Weekly Lesson Plan Generator")

# -----------------------------
# Function to replace placeholders safely
# -----------------------------
def replace_placeholder_in_paragraph(p, placeholder, value):
    """Replace placeholder even if Word splits text into multiple runs."""
    full_text = "".join(run.text for run in p.runs)
    if f"{{{{{placeholder}}}}}" in full_text:
        new_text = full_text.replace(f"{{{{{placeholder}}}}}", str(value))
        # clear old runs
        for run in p.runs:
            run.text = ""
        # put new text in first run
        p.runs[0].text = new_text

# -----------------------------
# Function to populate Word template
# -----------------------------
def populate_lesson_plan(json_data, template_path, output_path):
    doc = Document(template_path)

    # Top-level placeholders
    top_fields = ["Teacher","Year/Class","Subject","Unit/Topic","Week number","Date"]
    for field in top_fields:
        if field in json_data:
            for p in doc.paragraphs:
                replace_placeholder_in_paragraph(p, field, json_data[field])
            for table in doc.tables:
                for row in table.rows:
                    for cell in row.cells:
                        for p in cell.paragraphs:
                            replace_placeholder_in_paragraph(p, field, json_data[field])

    # Nested Classes
    if "Classes" in json_data:
        for class_key, class_obj in json_data["Classes"].items():
            for placeholder, value in class_obj.items():
                for p in doc.paragraphs:
                    replace_placeholder_in_paragraph(p, placeholder, value)
                for table in doc.tables:
                    for row in table.rows:
                        for cell in row.cells:
                            for p in cell.paragraphs:
                                replace_placeholder_in_paragraph(p, placeholder, value)

    # Flattened placeholders
    for placeholder, value in json_data.items():
        if placeholder not in top_fields and placeholder != "Classes":
            for p in doc.paragraphs:
                replace_placeholder_in_paragraph(p, placeholder, value)
            for table in doc.tables:
                for row in table.rows:
                    for cell in row.cells:
                        for p in cell.paragraphs:
                            replace_placeholder_in_paragraph(p, placeholder, value)

    doc.save(output_path)
    return output_path

# -----------------------------
# Streamlit UI
# -----------------------------
st.write("Upload your lesson plan JSON file or paste JSON data to populate your 5-day Word template.")

uploaded_file = st.file_uploader("Upload JSON", type="json")
if uploaded_file:
    try:
        lesson_json = json.load(uploaded_file)
        output_file = populate_lesson_plan(lesson_json, "templates/WLPT.docx", "WeeklyLessonPlan_output.docx")
        st.success(f"Lesson plan generated successfully!")
        st.download_button("Download Lesson Plan", output_file, file_name="WeeklyLessonPlan_output.docx")
    except Exception as e:
        st.error(f"Error processing file: {e}")

json_input = st.text_area("Or paste JSON here:")
if st.button("Generate from pasted JSON") and json_input:
    try:
        lesson_json = json.loads(json_input)
        output_file = populate_lesson_plan(lesson_json, "templates/WLPT.docx", "WeeklyLessonPlan_output.docx")
        st.success(f"Lesson plan generated successfully!")
        st.download_button("Download Lesson Plan", output_file, file_name="WeeklyLessonPlan_output.docx")
    except Exception as e:
        st.error(f"Error parsing JSON: {e}")
