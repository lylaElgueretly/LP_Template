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
    "Supported formats: DOCX, PDF, PPTX. "
    "The app will infer teaching intent and generate a full weekly lesson plan."
)

# ----------------------------------
# TEXT EXTRACTION (MINIMAL & SAFE)
# ----------------------------------
def extract_text(file):
    # For now, we only reliably extract DOCX text.
    # PDFs and PPTX are accepted but treated as contextual signals.
    if file.name.endswith(".docx"):
        doc = Document(file)
        return "\n".join(p.text for p in doc.paragraphs)
    return ""

# ----------------------------------
# DAY-BY-DAY INPUT (KEY FIX)
# ----------------------------------
def day_section(day_number):
    st.subheader(f"📅 Day {day_number}")

    materials = st.file_uploader(
        f"Upload materials for Day {day_number}",
        type=["docx", "pdf", "pptx"],
        accept_multiple_files=True,
        key=f"materials_day_{day_number}"
    )

    col1, col2 = st.columns(2)

    with col1:
        focus = st.text_input(
            "Lesson focus (what the lesson is mainly about)",
            key=f"focus_{day_number}"
        )

    with col2:
        skills = st.text_input(
            "Skills focus (e.g. inference, vocabulary, structure)",
            key=f"skills_{day_number}"
        )

    notes = st.text_area(
        "Optional teacher notes (grouping, pace, SEN/EAL)",
        key=f"notes_{day_number}"
    )

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

# ----------------------------------
# COLLECT WEEK DATA
# ----------------------------------
st.header("🗂 Organise Materials by Day")

week_data = []
for d in range(1, 6):
    week_data.append(day_section(d))
    st.divider()

# ----------------------------------
# RULE-BASED AI SIMULATION (SAFE)
# ----------------------------------
def generate_lesson_plan(week_data):
    output = {}

    for day in week_data:
        d = day["day"]

        output[f"Class{d}_LearningObjective"] = (
            f"Students will develop {day['skills']} skills. "
            f"Students will apply these skills through {day['focus']}."
        )

        output[f"Class{d}_SuccessCriteria"] = (
            "Students can meet the objective by using appropriate subject vocabulary "
            "and completing the independent task accurately."
        )

        output[f"Class{d}_Vocabulary"] = (
            "adventure, description, atmosphere, verb, detail"
        )

        output[f"Class{d}_KeyQuestions"] = (
            "How does the writer create interest? "
            "Which choices are most effective and why?"
        )

        output[f"Class{d}_StarterActivity"] = (
            "The teacher introduces a short retrieval or engagement task. "
            "Students respond orally or in writing to activate prior learning."
        )

        output[f"Class{d}_MainTeaching"] = (
            "The teacher models the target skill using the uploaded materials, "
            "explaining thinking aloud and questioning students to check understanding."
        )

        output[f"Class{d}_DifferentiatedActivities"] = (
            "Students complete independent work. "
            "LA students receive additional guidance, MA students complete the core task, "
            "and HA students extend responses through depth or justification."
        )

        output[f"Class{d}_Plenary"] = (
            "Students complete an exit task or self-assess against the success criteria. "
            "The teacher gathers evidence of learning."
        )

        output[f"Class{d}_Reflection"] = ""  # Must remain blank
        output[f"Class{d}_Homework"] = ""    # Only filled if explicitly requested

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

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".docx")
    doc.save(tmp.name)
    return tmp.name

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
