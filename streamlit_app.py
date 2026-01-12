import streamlit as st
from docx import Document
import tempfile

# ----------------------------------
# MASTER PROMPT / RULES (LOCKED)
# ----------------------------------
MASTER_AI_PROMPT = """
You are an expert UK secondary English curriculum designer.
Output a weekly lesson plan in the exact WLPT template style.

Rules:
- Produce third person: Teacher does / Students do
- Include timings for each activity
- Starter → Main teaching → Differentiated independent work → Plenary
- LA / MA / HA differentiation
- Key Vocabulary + Key Questions
- Success criteria: measurable outcomes
- Reflection blank
- Homework only if provided
- Keep week/date/teacher/year empty
- Use British spelling
- Preserve example sentences or extracts from materials if possible
"""

# ----------------------------------
# APP CONFIG
# ----------------------------------
st.set_page_config(page_title="5-Day AI Lesson Plan Generator", layout="wide")
st.title("📘 5-Day AI Lesson Plan Generator")
st.markdown("""
Upload **student-facing materials** for each day. 
Supported formats: DOCX, PDF, PPTX. 
The app will generate a **full weekly lesson plan** in your WLPT Word template format.
""")

# ----------------------------------
# TEXT EXTRACTION
# ----------------------------------
def extract_text(file):
    if file.name.endswith(".docx"):
        doc = Document(file)
        return "\n".join(p.text for p in doc.paragraphs)
    # For simplicity, PDFs and PPTX can be handled later or as notes
    return f"[Content from {file.name}]"

# ----------------------------------
# DAY-BY-DAY INPUT
# ----------------------------------
def day_section(day_number):
    st.subheader(f"📅 Day {day_number}")
    
    materials = st.file_uploader(
        f"Upload materials for Day {day_number}", 
        type=["docx","pdf","pptx"], 
        accept_multiple_files=True,
        key=f"materials_day_{day_number}"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        focus = st.text_input(f"Lesson Focus for Day {day_number}", key=f"focus_{day_number}")
    with col2:
        skills = st.text_input(f"Skills Focus for Day {day_number}", key=f"skills_{day_number}")
    
    notes = st.text_area(f"Optional Teacher Notes for Day {day_number}", key=f"notes_{day_number}")
    
    extracted = ""
    if materials:
        for file in materials:
            extracted += extract_text(file) + "\n"
    
    return {
        "day": day_number,
        "focus": focus,
        "skills": skills,
        "notes": notes,
        "materials_text": extracted.strip()
    }

week_data = []
st.header("🗂 Organise Materials by Day")
for d in range(1,6):
    week_data.append(day_section(d))
    st.divider()

# ----------------------------------
# SIMULATED AI LESSON PLAN GENERATION
# ----------------------------------
def generate_lesson_plan(week_data):
    plan = {}
    
    for day in week_data:
        d = day["day"]
        
        plan[f"Class{d}_LearningObjective"] = (
            f"Students will develop {day['skills']} skills through {day['focus']} activities. "
            f"They will analyse and apply their understanding using the provided materials."
        )
        
        plan[f"Class{d}_SuccessCriteria"] = (
            "Students can demonstrate understanding through annotation, discussion, or written tasks, "
            "and meet the objectives specified for the lesson."
        )
        
        plan[f"Class{d}_Vocabulary"] = (
            "adventure, description, atmosphere, verb, figurative language, tone, mood, suspense"
        )
        
        plan[f"Class{d}_KeyQuestions"] = (
            "What effect does the language have on the reader? "
            "Which choices create tension or mood? "
            "How does sentence structure affect pacing?"
        )
        
        # Starter / Main / Differentiated with examples and timing
        plan[f"Class{d}_StarterActivity"] = (
            "Starter (5 min): Teacher introduces a short engagement task using an example from the material. "
            "Students respond orally or in writing to activate prior learning."
        )
        
        plan[f"Class{d}_MainTeaching"] = (
            "Teacher Input / Modelling (10-15 min): Teacher models skills using extracts from the uploaded materials. "
            "Students follow along, annotate examples, and engage in think-aloud analysis."
        )
        
        plan[f"Class{d}_DifferentiatedActivities"] = (
            "Independent / Guided Work (15-20 min):\n"
            "LA: Complete basic identification tasks with scaffolding.\n"
            "MA: Annotate examples and explain effects in 2-3 sentences.\n"
            "HA: Produce extended analytical paragraphs using examples, vocabulary, and reasoning."
        )
        
        plan[f"Class{d}_Plenary"] = (
            "Plenary (5 min): Exit ticket or formative assessment. Students summarise key learning and teacher collects evidence."
        )
        
        plan[f"Class{d}_Reflection"] = ""  # Leave blank
        plan[f"Class{d}_Homework"] = ""     # Optional, empty if not specified
    
    return plan

# ----------------------------------
# POPULATE WLPT TEMPLATE
# ----------------------------------
def populate_template(template_path, data):
    doc = Document(template_path)
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for key, value in data.items():
                    placeholder = f"{{{{{key}}}}}"
                    if placeholder in cell.text:
                        cell.text = cell.text.replace(placeholder, value)
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".docx")
    doc.save(tmp.name)
    return tmp.name

# ----------------------------------
# GENERATE BUTTON
# ----------------------------------
if st.button("✨ Generate Weekly Lesson Plan"):
    with st.spinner("Generating high-fidelity lesson plan..."):
        lesson_data = generate_lesson_plan(week_data)
        output_path = populate_template("templates/WLPT.docx", lesson_data)
    
    st.success("✅ Lesson plan generated successfully!")
    with open(output_path, "rb") as f:
        st.download_button(
            "⬇ Download Weekly Lesson Plan",
            f,
            file_name="Weekly_Lesson_Plan.docx"
        )
