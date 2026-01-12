def extract_text(file):
    """
    Extract text from DOCX, PPTX, PDF
    """
    if file.name.endswith(".docx"):
        doc = Document(file)
        return "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    elif file.name.endswith(".pptx"):
        from pptx import Presentation
        prs = Presentation(file)
        slides_text = []
        for slide in prs.slides:
            for shape in slide.shapes:
                if hasattr(shape, "text"):
                    slides_text.append(shape.text)
        return "\n".join(slides_text)
    elif file.name.endswith(".pdf"):
        # Optional: use PyPDF2 or pdfplumber
        return f"[PDF content from {file.name}]"  
    else:
        return ""

def generate_lesson_plan(week_data):
    """
    Generate high-fidelity lesson plan using extracted material text
    """
    plan = {}
    for day in week_data:
        content = day["materials_text"]  # extracted text
        focus = day["focus"] or "English language analysis"
        skills = day["skills"] or "reading and comprehension"

        # Example: Simple extraction-based enhancement
        vocab = extract_keywords(content)
        questions = extract_questions(content)
        examples = extract_examples(content)

        plan[f"Class{day['day']}_LearningObjective"] = (
            f"Students will develop {skills} skills through {focus} activities. "
            f"They will analyse and apply their understanding using examples such as '{examples[:60]}...'."
        )
        plan[f"Class{day['day']}_SuccessCriteria"] = (
            f"Students can demonstrate understanding by annotating, discussing, or answering questions such as '{questions[:60]}...'."
        )
        plan[f"Class{day['day']}_Vocabulary"] = ", ".join(vocab or ["Key terms from material"])
        plan[f"Class{day['day']}_KeyQuestions"] = questions or "Questions based on material"
        # And continue with Starter, Main, Differentiated, Plenary...
