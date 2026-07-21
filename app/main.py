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
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Custom CSS for better styling ---
st.markdown("""
<style>
    .skill-pill {
        display: inline-block;
        background-color: #e0e0ef;
        color: #333;
        border-radius: 15px;
        padding: 4px 12px;
        margin: 4px;
        font-size: 14px;
        font-weight: 500;
    }
    .skill-pill-success { background-color: #d4edda; color: #155724; }
    .skill-pill-danger { background-color: #f8d7da; color: #721c24; }
</style>
""", unsafe_allow_html=True)

# Helper function to render pills
def render_pills(skill_list, css_class="skill-pill"):
    if not skill_list:
        st.write("None detected.")
        return
    
    html = ""
    for skill in skill_list:
        html += f'<span class="{css_class}">{skill.title()}</span>'
    st.markdown(html, unsafe_allow_html=True)


# --- Application Header ---
st.title("🎯 ML Resume-to-Job Fit Analyzer")
st.markdown("""
Upload your resume and paste the target job description. Our NLP engine uses **Spacy NER** to extract technical entities 
and **BERT Word Embeddings** to calculate the semantic similarity between your experience and the job requirements.
""")
st.divider()

# --- Input Section (Two Columns) ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("📄 1. Upload Resume")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

with col2:
    st.subheader("🏢 2. Target Job Description")
    job_description = st.text_area("Paste the job description here...", height=200, placeholder="E.g., We are looking for a Software Engineer with 3+ years of experience in Python, AWS, and Docker...")

# --- Processing Section ---
st.divider()
analyze_button = st.button("🚀 Analyze Fit & Generate Report", type="primary", use_container_width=True)

if analyze_button:
    if uploaded_file is None:
        st.warning("Please upload a Resume PDF.")
    elif not job_description.strip():
        st.warning("Please paste a Job Description.")
    else:
        with st.spinner("Initializing NLP models and extracting entities..."):
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
                temp_pdf.write(uploaded_file.read())
                temp_pdf_path = temp_pdf.name
            
            try:
                # 1. Extraction & Cleaning
                raw_resume = extract_text_from_pdf(temp_pdf_path)
                clean_resume = clean_text(raw_resume)
                clean_jd = clean_text(job_description)
                
                # 2. NER Extraction
                resume_skills = extract_skills(clean_resume)
                jd_skills = extract_skills(clean_jd)
                
                # 3. BERT Similarity
                match_score = float(calculate_match_score(clean_resume, clean_jd))
                
                # 4. Gap Analysis
                gap_data = analyze_skill_gap(resume_skills, jd_skills)
                
                # ==========================================
                #               DISPLAY RESULTS
                # ==========================================
                
                st.header("📊 Analysis Report")
                
                # --- The Main Score ---
                score_col1, score_col2 = st.columns([1, 3])
                with score_col1:
                    st.metric(label="Semantic Match Score", value=f"{match_score}%", 
                              delta="Strong Fit" if match_score >= 70 else "Needs Improvement" if match_score < 40 else "Moderate Fit")
                with score_col2:
                    st.write("Match Confidence:")
                    st.progress(match_score / 100)
                    if match_score >= 70:
                        st.success("High probability of passing automated ATS screening.")
                    elif match_score >= 40:
                        st.warning("Moderate fit. You may need to highlight specific missing keywords in your cover letter.")
                    else:
                        st.error("Low fit. Heavy resume tailoring is required before applying.")

                st.divider()

                # --- Extraction Transparency (What the model saw) ---
                st.subheader("🔍 Entity Extraction Breakdown")
                st.markdown("Here is exactly what the NLP model recognized from both texts based on the lexicon.")
                
                ext_col1, ext_col2 = st.columns(2)
                with ext_col1:
                    st.write(f"**Skills Found in Resume ({len(resume_skills)}):**")
                    render_pills(resume_skills)
                    
                with ext_col2:
                    st.write(f"**Skills Required by Job ({len(jd_skills)}):**")
                    render_pills(jd_skills)

                st.divider()

                # --- Gap Analysis (The actionable part) ---
                st.subheader("🎯 Skill Gap Analysis")
                
                gap_col1, gap_col2 = st.columns(2)
                
                with gap_col1:
                    st.write(f"**✅ Overlapping Skills ({len(gap_data['matching'])}):**")
                    st.caption("You have these. Make sure they are prominent on your resume.")
                    render_pills(gap_data['matching'], "skill-pill skill-pill-success")
                        
                with gap_col2:
                    st.write(f"**❌ Missing Skills ({len(gap_data['missing'])}):**")
                    st.caption("The JD asks for these, but they weren't found in your resume.")
                    render_pills(gap_data['missing'], "skill-pill skill-pill-danger")

                # --- Actionable Recommendations ---
                if gap_data['missing']:
                    st.subheader("💡 Actionable Recommendations")
                    st.info(f"To improve your ATS score, consider updating your resume to include: **{', '.join([s.title() for s in gap_data['missing'][:5]])}** (if you possess these skills).")
                    
                    # Basic mocked learning path feature
                    st.markdown("**Suggested Learning Paths to close the gap:**")
                    for skill in gap_data['missing'][:3]: # Suggest up to 3 courses
                        st.markdown(f"- [Learn {skill.title()} on Coursera](https://www.coursera.org/search?query={skill})")
                        
            except Exception as e:
                st.error(f"An error occurred during processing: {e}")
                
            finally:
                if os.path.exists(temp_pdf_path):
                    os.remove(temp_pdf_path)


