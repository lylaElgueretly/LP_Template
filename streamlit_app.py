# -----------------------------
# Streamlit App: Lesson Plan Template Filler
# -----------------------------

import streamlit as st
import json
from docx import Document
from io import BytesIO

st.set_page_config(page_title="Lesson Plan Template Generator", layout="wide")

st.title("Lesson Plan Template Generator")
st.markdown("""
Paste your lesson plan JSON below and click 'Generate Word Document'.  
Your Word template should have placeholders like `{{Teacher}}`, `{{LearningObjective}}`, etc.
""")

# -----------------------------
# Upload Word template
# -----------------------------
template_file = st.file_uploader("Upload your Word template (.docx)", type="docx")

# Paste JSON
lesson_plan_input = st.text_area("Paste your lesson plan JSON here:")

# -----------------------------
# Logic to replace placeholders
# -----------------------------
def replace_placeholders(doc, lesson_plan):
    """
    Replaces placeholders in a Word doc with values from the JSON lesson plan.
    Handles both top-level fields and class-level fields.
    """
    # Top-level fields
    for field in ["Teacher","Year/Class","Subject","Unit/Topic","Week number","Date"]:
        if field in lesson_plan:
            for p in doc.paragraphs:
                if f"{{{{{field}}}}}" in p.text:
                    inline = p.runs
                    for i in range(len(inline)):
                        inline[i].text = inline[i].text.replace(f"{{{{{field}}}}}", lesson_plan[field])

    # Class-level fields
    if "Classes" in lesson_plan:
        for class_key, class_obj in lesson_plan["Classes"].items():
            for placeholder, value in class_obj.items():
                for p in doc.paragraphs:
                    if f"{{{{{placeholder}}}}}" in p.text:
                        inline = p.runs
                        for i in range(len(inline)):
                            inline[i].text = inline[i].text.replace(f"{{{{{placeholder}}}}}", value)
    return doc

# -----------------------------
# Button to generate Word document
# -----------------------------
if st.button("Generate Word Document"):
    if not template_file:
        st.error("Please upload a Word template file.")
    elif not lesson_plan_input.strip():
        st.error("Please paste valid JSON.")
    else:
        try:
            lesson_plan_json = json.loads(lesson_plan_input)
            doc = Document(template_file)
            doc = replace_placeholders(doc, lesson_plan_json)

            # Save to in-memory file
            output = BytesIO()
            doc.save(output)
            output.seek(0)

            st.download_button(
                label="Download Populated Template",
                data=output,
                file_name="Lesson_Plan.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

            st.success("Template populated successfully!")

        except json.JSONDecodeError as e:
            st.error(f"Invalid JSON: {e}")
        except Exception as e:
            st.error(f"Error generating document: {e}")
