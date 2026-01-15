import streamlit as st
import json
from docx import Document
from io import BytesIO

st.set_page_config(page_title="Lesson Plan Generator", page_icon="📚", layout="wide")

st.title("📚 Weekly Lesson Plan Template Generator")
st.markdown("Upload your JSON file to populate the WLPT template and download it.")

# File uploader for JSON
uploaded_json = st.file_uploader("Upload JSON File", type=['json'])

# File uploader for template (or you can hardcode the path)
uploaded_template = st.file_uploader("Upload WLPT.docx Template", type=['docx'])

if uploaded_json and uploaded_template:
    try:
        # Read JSON data
        json_data = json.load(uploaded_json)
        st.success("✅ JSON file loaded successfully!")
        
        # Show preview of JSON data
        with st.expander("📄 View JSON Data"):
            st.json(json_data)
        
        # Load the Word template
        doc = Document(uploaded_template)
        
        # Function to replace placeholders in the document
        def replace_placeholder(doc, placeholder, value):
            """Replace placeholder text in all tables and paragraphs"""
            # Replace in paragraphs
            for paragraph in doc.paragraphs:
                if placeholder in paragraph.text:
                    for run in paragraph.runs:
                        if placeholder in run.text:
                            run.text = run.text.replace(placeholder, str(value))
            
            # Replace in tables
            for table in doc.tables:
                for row in table.rows:
                    for cell in row.cells:
                        if placeholder in cell.text:
                            for paragraph in cell.paragraphs:
                                for run in paragraph.runs:
                                    if placeholder in run.text:
                                        run.text = run.text.replace(placeholder, str(value))
        
        # Replace all placeholders with JSON data
        for key, value in json_data.items():
            placeholder = "{{" + key + "}}"
            replace_placeholder(doc, placeholder, value if value else "")
        
        # Save to BytesIO object
        docx_buffer = BytesIO()
        doc.save(docx_buffer)
        docx_buffer.seek(0)
        
        st.success("✅ Template populated successfully!")
        
        # Download button
        st.download_button(
            label="📥 Download Populated Template",
            data=docx_buffer,
            file_name="Weekly_Lesson_Plan_Populated.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        
    except json.JSONDecodeError:
        st.error("❌ Invalid JSON file. Please upload a valid JSON file.")
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

else:
    st.info("👆 Please upload both your JSON file and WLPT.docx template to get started.")
    
    # Instructions
    with st.expander("📖 Instructions"):
        st.markdown("""
        ### How to use:
        1. **Upload your JSON file** containing the lesson plan data
        2. **Upload the WLPT.docx template** file
        3. The app will automatically populate the template with your data
        4. Click **Download Populated Template** to get your completed Word document
        
        ### Expected JSON format:
        ```json
        {
          "Teacher": "John Doe",
          "YearClass": "Year 5",
          "Subject": "English",
          "WeekNumber": "Week 1",
          "Date": "January 2026",
          "Topic": "Adventure",
          "Class1_LearningObjective": "Students will...",
          "Class1_SuccessCriteria": "Students can...",
          "Class1_Vocabulary": "adventure, journey, explore",
          "Class1_KeyQuestions": "What is an adventure?",
          "Class1_StarterActivity": "Discuss favorite adventures",
          "Class1_MainTeaching": "Read adventure story...",
          "Class1_DifferentiatedActivities": "Group work, individual tasks",
          "Class1_Plenary": "Share findings",
          "Class1_Reflection": "What did we learn?",
          "Class1_Homework": "Write adventure paragraph",
          ... (repeat for Class2 through Class5)
        }
        ```
        """)
