import streamlit as st
from docx import Document
import tempfile

# ----------------------------------
# LOCKED MASTER AI PROMPT (GOVERNOR)
# ----------------------------------
MASTER_AI_PROMPT = """
You are an expert UK secondary English curriculum designer.

You receive student-facing teaching materials for five days.
These materials are not lesson plans.

You must infer pedagogical intent and reconstruct a coherent
five-day lesson sequence.

NON-NEGOTIABLE RULES:
- Learning objectives: 1–2 short, child-friendly, starting with 'Students will...'
- Write in third person (teacher does / students do / when)
- Success criteria must be measurable
- Lesson structure MUST be:
  1. Starter activity
  2. Teacher modelling (main activity using provided materials)
  3. Differentiated independent work (LA / MA / HA without new materials)
- Differentiation through grouping, scaffolding, seating, teacher guidance only
- Plenary must act as formative assessment
- Reflection MUST be left blank
- Homework ONLY if explicitly requested; otherwise leave blank
- Ensure clear progression across the five days
- Day 5 prioritises application or assessment
- Keep week date, week number, year/class, and teacher details EMPTY
- Use British spelling
"""

# ----------------------------------
# APP CONFIG
# ----------------------------------
st.set_page_config(
    page_title="5-Day AI Lesson Plan Generator",
    layout="wide"
)

st.title("📘 5-Day AI Lesson Plan Generator")
st.markdown(
    "Upload **student-facing materials** for each day. "
    "The system will infer teaching intent and generate a professional weekly lesson plan."
)

# ----------------------------------
# FILE TEXT EXTRACTION (DOCX ONLY FOR NOW)
# ----------------------------------
def extract_docx_text(file):
    doc = Document(file)
    return "\n".join(p.text for p in doc.paragraphs)

def extract_text(file):
    if file and file.name.endswith(".docx"):
        return extract_docx_text(file)
    return ""

# ----------------------------------
# DAY INPUT SECTION
# ----------------------------------
def day_input(day_number):
    st.subheader(f"📅 Day {day_number}")

    col1, col2 = st.columns(2)

    with col1:
        materials = st.file_uploader(
            f"Day {day_number} materials (PowerPoint / Worksheet / Text)",
            type=["docx"],
            accept_multiple_files=True,
            key=f"materials_{day_number}"
        )

    with col2:
        focus = st.text_input(
            "Lesson focus (e.g. analysing language, planning, drafting)",
            key=f"focus_{day_number}"
        )

        skills = st.text_input(
            "Skills emphasis (e.g. inference, vocabulary, structure)",
            key=f"skills_{day_number}"
        )

        notes = st.text_area(
            "Optional class notes (pace, grouping, SEN/EAL)",
            key=f"notes_{day_number}"
        )

    extracted_text = ""
    if materials:
        for file in materials:
            extracted_text += extract_text(file) + "\n"

    return {
        "day": day_number,
        "focus": focus,
        "skills": skills,
        "notes": notes,
        "materials_text": extracted_text.strip()
    }

# ----------------------------------
# COLLECT WEEK DATA
# ----------------------------------
st.header("🗂 Upload Materials by Day")

week_data = []
for d in range(1, 6):
    week_data.append(day_input(d))
    st.divider()

# ----------------------------------
# SIMULATED AI INFERENCE (RULE-BASED)
# ----------------------------------
def generate_lesson_plan(week_data):
    """
    This simulates AI output while strictly following the locked prompt.
    It will be replaced later by a real LLM call.
    """

    output = {}

    for day in week_data:
        d = day["day"]

        output[f"Class{d}_LearningObjective"] = (
            f"Students will develop {day['skills']} skills. "
            f"Students will apply these skills during {day['focus']}."
        )

        output[f"Class{d}_SuccessCriteria"] = (
            "Students can demonstrate understanding through accurate responses, "
            "use of subject vocabulary, and completed independent work."
        )

        output[f"Class{d}_KeyVocabulary"] = (
            "adventure, description, tension, verb, atmosphere"
        )

        output[f"Class{d}_KeyQuestions"] = (
            "How does the writer engage the reader? "
            "Which language choices are most effective?"
        )

        output[f"Class{d}_StarterActivity"] = (
            "The teacher introduces a short retrieval or discussion task linked "
            "to prior learning. Students respond orally or in writing."
        )

        output[f"Class{d}_MainTeaching"] = (
            "The teacher models the target skill using the uploaded materials, "
            "thinking aloud and questioning students to check understanding."
        )

        output[f"Class{d}_DifferentiatedActivities"] = (
            "Students complete independent work based on the modelled example. "
            "LA students receive guided prompts, MA students complete the core task, "
            "and HA students extend responses through depth or justification."
        )

        output[f"Class{d}_Plenary"] = (
            "Students complete an exit task or self-check against success criteria. "
            "The teacher gathers evidence of learning through responses."
        )

        output[f"Class{d}_Reflection"] = ""  # MUST remain blank
        output[f"Class{d}_Homework"] = ""    # Left blank unless explicitly requested

    return output

# ----------------------------------
# WORD TEMPLATE POPULATION
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

    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".docx")
    doc.save(tmp_file.name)
    return tmp_file.name

# ----------------------------------
# GENERATE BUTTON
# ----------------------------------
if st.button("✨ Generate Weekly Lesson Plan"):
    with st.spinner("Analysing materials and generating lesson plan..."):
        lesson_data = generate_lesson_plan(week_data)
        output_path = populate_template("templates/WLPT.docx", lesson_data)

    st.success("Weekly lesson plan generated successfully.")

    with open(output_path, "rb") as f:
        st.download_button(
            "⬇ Download Lesson Plan",
            f,
            file_name="Weekly_Lesson_Plan.docx"
        )
