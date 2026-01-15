# streamlit_app.py
# WLPT Template Filler – Stable Version

import streamlit as st
from docx import Document
import json
import os

# --------------------------------------------------
# Helper: Populate WLPT template
# --------------------------------------------------
def populate_template(lesson_plan_json):
    template_path = os.path.join("templates", "WLPT.docx")

    if not os.path.exists(template_path):
        st.error("❌ WLPT.docx not found in the templates folder.")
        return None

    doc = Document(template_path)

    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for key, value in lesson_plan_json.items():
                    placeholder = f"{{{{{key}}}}}"
                    if placeholder in cell.text:
                        cell.text = cell.text.replace(placeholder, str(value))

    output_path = "WLPT_Populated.docx"
    doc.save(output_path)
    return output_path


# --------------------------------------------------
# Main App
# --------------------------------------------------
def main():
    st.set_page_config(
        page_title="5-Day AI Lesson Plan Generator",
        layout="wide"
    )

    st.title("5-Day AI Lesson Plan Generator")
    st.write(
        """
        Paste or upload a **WLPT-compatible JSON lesson plan**.
        The app will populate the official **WLPT Word template**
        while preserving logos and table formatting.
        """
    )

    st.divider()

    # ---------------------------
    # OPTION 1: Upload JSON file
    # ---------------------------
    st.subheader("Option 1: Upload JSON file")
    uploaded_file = st.file_uploader(
        "Upload AI-generated JSON",
        type="json"
    )

    # ---------------------------
    # OPTION 2: Paste JSON
    # ---------------------------
    st.subheader("Option 2: Paste JSON")
    pasted_json = st.text_area(
        "Paste your WLPT JSON here",
        height=320,
        placeholder="""
{
  "Class1_LearningObjective": "Students will...",
  "Class1_SuccessCriteria": "Students can...",
  "Class1_Vocabulary": "...",
  "Class1_KeyQuestions": "...",
  "Class1_StarterActivity": "...",
  "Class1_MainTeaching": "...",
  "Class1_DifferentiatedActivities": "...",
  "Class1_Plenary": "...",
  "Class1_Reflection": "",
  "Class1_Homework": ""
}
"""
    )

    st.divider()

    # ---------------------------
    # Process input
    # ---------------------------
    if uploaded_file or pasted_json.strip():

        try:
            if uploaded_file:
                lesson_plan_json = json.load(uploaded_file)
            else:
                lesson_plan_json = json.loads(pasted_json)

            output_path = populate_template(lesson_plan_json)

            if output_path:
                st.success("✅ Lesson plan generated successfully.")

                with open(output_path, "rb") as f:
                    st.download_button(
                        label="⬇ Download WLPT Lesson Plan",
                        data=f,
                        file_name="WLPT_Lesson_Plan.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )

        except json.JSONDecodeError:
            st.error("❌ Invalid JSON format. Please check commas, quotes, and brackets.")

        except Exception as e:
            st.error(f"❌ An error occurred: {e}")

    else:
        st.info("ℹ️ Upload or paste WLPT-compatible JSON to continue.")


# --------------------------------------------------
# Entry point
# --------------------------------------------------
if __name__ == "__main__":
    main()
