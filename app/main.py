# app/main.py
import streamlit as st
import os
import tempfile

# Import our custom modules
from parser import extract_text_from_pdf, clean_text
from engine import (
    extract_skills, 
    calculate_comprehensive_score, 
    analyze_skill_gap, 
    analyze_quantitative_impact, 
    analyze_format_and_scannability
)

# --- UI Configuration ---
st.set_page_config(
    page_title="Enterprise ML Resume Engine",
    page_icon="⚡",
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
st.title("⚡ Enterprise-Grade Resume & Impact Analyzer")
st.markdown("""
Moving beyond simple keyword matching. This engine evaluates **Technical Stack Coverage**, **Semantic Project Relevance**, 
**Quantitative Business Impact (Metrics)**, and **ATS Scannability**.
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
analyze_button = st.button("🚀 Run Multi-Factor Evaluation", type="primary", use_container_width=True)

if analyze_button:
    if uploaded_file is None:
        st.warning("Please upload a Resume PDF.")
    elif not job_description.strip():
        st.warning("Please paste a Job Description.")
    else:
        with st.spinner("Executing multi-dimensional NLP and heuristic evaluation..."):
            
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
                
                # 3. Comprehensive Multi-Factor Evaluation Engine
                evaluation = calculate_comprehensive_score(clean_resume, clean_jd, resume_skills, jd_skills)
                gap_data = analyze_skill_gap(resume_skills, jd_skills)
                format_info = analyze_format_and_scannability(clean_resume)
                
                final_score = float(evaluation['final_score'])
                
                # ==========================================
                #               DISPLAY RESULTS
                # ==========================================
                
                st.header("📊 Multi-Factor Recruitment Audit")
                
                # --- Overall Metrics ---
                score_col1, score_col2, score_col3 = st.columns(3)
                with score_col1:
                    st.metric(label="Overall ATS Fit Score", value=f"{final_score:.1f}%", 
                              delta="Strong Fit" if final_score >= 70 else "Needs Improvement" if final_score < 40 else "Moderate Fit")
                with score_col2:
                    st.metric(label="Word Count (Scannability)", value=f"{evaluation['word_count']} words", 
                              delta="Optimal (300-900)" if format_info['is_scannable'] else "Review Length")
                with score_col3:
                    st.metric(label="Quantitative Metrics Found", value=f"{len(evaluation['metrics_found'])} detected")

                st.divider()

                # --- Core Factor Breakdown Sub-Metrics ---
                st.subheader("⚙️ Core Factor Breakdown")
                breakdown = evaluation['breakdown']
                
                b_col1, b_col2, b_col3, b_col4 = st.columns(4)
                with b_col1:
                    st.metric("Skill Stack Match", f"{breakdown['skills']}%")
                with b_col2:
                    st.metric("Semantic Relevance", f"{breakdown['semantics']}%")
                with b_col3:
                    st.metric("Quantitative Impact", f"{breakdown['impact']}%")
                with b_col4:
                    st.metric("Format Optimization", f"{breakdown['format']}%")

                st.divider()

                # --- Experience & Impact Audit ---
                st.subheader("📈 Experience & Impact Audit")
                if evaluation['metrics_found']:
                    st.success(f"Great job! The model detected real quantitative markers in your text: **{', '.join(evaluation['metrics_found'])}**.")
                    st.caption("Recruiters look for numbers to prove business impact rather than boring daily operational lists.")
                else:
                    st.warning("⚠️ **Impact Warning:** No clear quantitative metrics (e.g., percentages, scale, user volume) were found.")
                    st.markdown("*Tip: Change phrases like 'Managed server infrastructure' to 'Optimized system reliability, reducing crash frequency by 35%'.*")

                st.divider()

                # --- Entity Extraction Transparency ---
                st.subheader("🔍 Entity Extraction Breakdown")
                st.markdown("Here is what the NLP entity extraction model recognized from your text files:")
                
                ext_col1, ext_col2 = st.columns(2)
                with ext_col1:
                    st.write(f"**Skills Found in Resume ({len(resume_skills)}):**")
                    render_pills(resume_skills)
                    
                with ext_col2:
                    st.write(f"**Skills Required by Job ({len(jd_skills)}):**")
                    render_pills(jd_skills)

                st.divider()

                # --- Skill Gap Analysis ---
                st.subheader("🎯 Skill Gap & Recommendations")
                
                gap_col1, gap_col2 = st.columns(2)
                
                with gap_col1:
                    st.write(f"**✅ Matching Technical Stack ({len(gap_data['matching'])}):**")
                    render_pills(gap_data['matching'], "skill-pill skill-pill-success")
                        
                with gap_col2:
                    st.write(f"**❌ Missing Technical Stack ({len(gap_data['missing'])}):**")
                    render_pills(gap_data['missing'], "skill-pill skill-pill-danger")

                # --- Actionable Recommendations ---
                if gap_data['missing']:
                    st.subheader("💡 Actionable Upskilling Path")
                    st.info(f"To bridge your stack gap, consider gaining proficiency in: **{', '.join([s.title() for s in gap_data['missing'][:5]])}**.")
                    
                    st.markdown("**Suggested Learning Paths to close the gap:**")
                    for skill in gap_data['missing'][:3]:
                        st.markdown(f"- [Master {skill.title()} via Structured Labs](https://www.google.com/search?q=learn+{skill}+tutorial)")
                        
            except Exception as e:
                st.error(f"An error occurred during processing: {e}")
                
            finally:
                if os.path.exists(temp_pdf_path):
                    os.remove(temp_pdf_path)