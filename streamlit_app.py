# LP_Template_app.py
import streamlit as st
from docx import Document
from pptx import Presentation
import pdfplumber
import io
import os
import json

# =========================
# Helper functions
# =========================

def extract_text(file):
    """Extract text safely from DOCX, PPTX, or PDF"""
    try:
        if file.name.endswith(".docx"):
            doc = Document(file)
            return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
        elif file.name.endswith(".pptx"):
            prs = Presentation(file)
            slides_text = []
            for slide in prs.slides:
                for shape in slide.shapes:
                    if hasattr(shape, "text") and shape.text.strip():
                        slides_text.append(shape.text)
            return "\n".join(slides_text)
        elif file.name.endswith(".pdf"):
            text = ""
            with pdfplumber.open(file) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            return text
        else:
            return ""
    except Exception as e:
        st.warning(f"Could not extract text from {file.name}: {e}")
        return ""

def generate_lesson_plan_json(materials_texts):
    """
    Generate a structured lesson plan JSON using extracted content.
    This is a placeholder for your AI integration (e.g., OpenAI API).
    """
    lesson_plan = {
        "Teacher": "Lyla El-Gueretly",
        "Weekly Lesson Plan": "",
        "Week number": "",
        "Year/Class": "",
        "Date": "",
        "Subject": "English",
        "Unit / Topic": "Adventure",
    }

    for day_num, content in enumerate(materials_texts, start=1):
        lesson_plan[f"Class{day_num}_LearningObjective"] = (
            f"Students will develop comprehension and writing skills through activities using examples from the material."
        )
        lesson_plan[f"Class{day_num}_SuccessCriteria"] = (
            f"Students can analyse examples and answer questions demonstrating understanding."
        )
        lesson_plan[f"Class{day_num}_Vocabulary"] = extract_keywords(content)
        lesson_plan[f"Class{day_num}_KeyQuestions"] = extract_questions(content)
        lesson_plan[f"Class{day_num}_StarterActivity"] = (
            f"Starter (5 min): Students respond to a short engagement task based on the material."
        )
        lesson_plan[f"Class{day_num}_MainTeaching"] = (
            f"Teacher models examples and annotations from the material; students follow and discuss."
        )
        lesson_plan[f"Class{day_num}_DifferentiatedActivities"] = (
            f"LA: basic identification tasks; MA: annotate and explain effects; HA: extended analytical paragraphs."
        )
        lesson_plan[f"Class{day_num}_Plenary"] = (
            f"Exit ticket or formative assessment summarising key learning."
        )
        lesson_plan[f"Class{day_num}_Reflection"] = ""
        lesson_plan[f"Class{day_num}_Homework"] = ""
    
    return lesson_plan

def extract_keywords(text):
    """Very basic keyword extraction from text"""
    words = text.split()
    keywords = list(set([w.strip(".,:;!?").lower() for w in words if len(w) > 4]))
    return ", ".join(keywords[:15])  # top 15 keywords

def extract_questions(text):
    """Extract sentences ending with ? or generate placeholders"""
    sentences = [s.strip() for s in text.split("\n") if s.strip()]
    questions = [s for s in sentences if s.endswith("?")]
    if not questions:
        return "What questions can we ask from this material?"
    return " | ".join(questions[:5])

def populate_word_template(lesson_json, template_path, output_path):
    """Populate the WLPT Word template with lesson JSON"""
    doc = Document(template_path)
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for key, value in lesson_json.items():
                    if f"{{{{{key}}}}}" in cell.text:
                        cell.text = cell.text.replace(f"{{{{{key}}}}}", str(value))
    doc.save(output_path)
    return output_path

# =========================
# Streamlit App
# =========================

st.title("5-Day AI Lesson Plan Generator")
st.write("Upload your student-facing materials (DOCX, PDF, PPTX). The app will analyze the content and automatically create a complete 5-day lesson plan in your WLPT Word template.")

uploaded_files = st.file_uploader(
    "Upload materials",
    type=["docx", "pdf", "pptx"],
    accept_multiple_files=True
)

template_file = st.file_uploader("Upload WLPT Word template (.dot/.docx)", type=["dot", "docx"])

if uploaded_files and template_file:
    st.info("Processing files...")
    
    materials_texts = [extract_text(f) for f in uploaded_files]
    
    # Generate structured lesson plan JSON
    lesson_json = generate_lesson_plan_json(materials_texts)
    
    st.success("Lesson plan JSON generated successfully!")
    
    # Save JSON for reference
    json_path = "lesson_plan.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(lesson_json, f, ensure_ascii=False, indent=4)
    
    st.download_button("Download lesson plan JSON", json_path, file_name="lesson_plan.json")
    
    # Populate Word template
    output_path = "WLPT_Populated.docx"
    with io.BytesIO(template_file.read()) as temp_template:
        populated_path = populate_word_template(lesson_json, temp_template, output_path)
    
    st.success("WLPT template populated successfully!")
    st.download_button("Download populated Word template", populated_path, file_name="WLPT_Populated.docx")
else:
    st.info("Please upload at least one student-facing material file and the WLPT template to proceed.")
