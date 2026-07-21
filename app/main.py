# app/main.py
import streamlit as st
import os
import tempfile

# Import our custom modules
from parser import extract_text_from_pdf, clean_text
from engine import extract_skills, calculate_match_score, analyze_skill_gap

# --- UI Configuration ---
st.set_page_config(
    page_title="Resume Fit Analyzer",
    page_icon="🎯",
    layout="wide"
)

# --- Application Header ---
st.title("🎯 ML Resume-to-Job Fit Analyzer")
st.markdown("""
Upload a resume (PDF) and paste a job description. The NLP engine will calculate the semantic match 
and extract specific skill gaps to help you tailor your application.
""")
st.divider()

# --- Input Section (Two Columns) ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Upload Resume (PDF)")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

with col2:
    st.subheader("2. Job Description")
    job_description = st.text_area("Paste the job description here...", height=200)

# --- Processing Section ---
st.divider()
analyze_button = st.button("Analyze Fit", type="primary", use_container_width=True)

if analyze_button:
    if uploaded_file is None:
        st.error("Please upload a Resume PDF.")
    elif not job_description.strip():
        st.error("Please paste a Job Description.")
    else:
        with st.spinner("Analyzing semantics and extracting entities..."):
            
            # 1. Handle the uploaded PDF safely
            # Streamlit uploads files to memory. We need to save it to a temporary file 
            # so pdfplumber can open it via a file path.
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
                temp_pdf.write(uploaded_file.read())
                temp_pdf_path = temp_pdf.name
            
            try:
                # 2. Extract and Clean Text
                raw_resume = extract_text_from_pdf(temp_pdf_path)
                clean_resume = clean_text(raw_resume)
                clean_jd = clean_text(job_description)
                
                # 3. Extract Skills (NER)
                resume_skills = extract_skills(clean_resume)
                jd_skills = extract_skills(clean_jd)
                
                # 4. Calculate Semantic Similarity (BERT)
                # Force the output to be a standard Python float to prevent Streamlit UI errors
                match_score = float(calculate_match_score(clean_resume, clean_jd))
                
                # 5. Gap Analysis (Set Math)
                gap_data = analyze_skill_gap(resume_skills, jd_skills)
                
                # --- DISPLAY RESULTS ---
                
                st.header("Analysis Results")
                
                # Metric display for the score
                st.metric(label="Semantic Match Score", value=f"{match_score}%")
                
                # Progress bar for visual impact
                st.progress(match_score / 100)
                
                st.subheader("Skill Gap Analysis")
                
                res_col1, res_col2 = st.columns(2)
                
                with res_col1:
                    st.success(f"✅ Matching Skills Found ({len(gap_data['matching'])})")
                    if gap_data['matching']:
                        for skill in gap_data['matching']:
                            st.write(f"- {skill.title()}")
                    else:
                        st.write("No direct skill matches found based on the lexicon.")
                        
                with res_col2:
                    st.error(f"❌ Missing Skills ({len(gap_data['missing'])})")
                    if gap_data['missing']:
                        for skill in gap_data['missing']:
                            st.write(f"- {skill.title()}")
                    else:
                        st.write("No missing skills detected! You have everything they asked for.")
                
            except Exception as e:
                st.error(f"An error occurred during processing: {e}")
                
            finally:
                # Clean up the temporary PDF file so we don't clog up the hard drive
                if os.path.exists(temp_pdf_path):
                    os.remove(temp_pdf_path)
