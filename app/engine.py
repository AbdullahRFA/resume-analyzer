# app/engine.py
import spacy
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import re

# 1. Initialize Spacy
print("Loading Spacy NLP model...")
nlp = spacy.load("en_core_web_sm")

tech_skills = [
    "python", "java", "c++", "c#", "javascript", "typescript", "golang", "rust", "php", "ruby", "sql", "html", "css",
    "react", "angular", "vue", "django", "fastapi", "flask", "spring boot", "node.js", "express", "pandas", "numpy",
    "scikit-learn", "tensorflow", "keras", "pytorch", "opencv", "matplotlib", "seaborn",
    "postgresql", "mysql", "mongodb", "redis", "cassandra", "oracle", "elasticsearch",
    "aws", "azure", "gcp", "docker", "kubernetes", "jenkins", "github actions", "gitlab ci", "terraform", "ansible",
    "linux", "bash", "git",
    "machine learning", "deep learning", "natural language processing", "nlp", "computer vision", "data analysis",
    "agile", "scrum", "rest api", "graphql", "microservices", "ci/cd"
]

if "entity_ruler" not in nlp.pipe_names:
    ruler = nlp.add_pipe("entity_ruler", before="ner")
else:
    ruler = nlp.get_pipe("entity_ruler")

patterns = [{"label": "SKILL", "pattern": skill} for skill in tech_skills]
ruler.add_patterns(patterns)

# 2. Initialize BERT Embedder
print("Loading Sentence Transformer model...")
embedder = SentenceTransformer('all-MiniLM-L6-v2')


def extract_skills(text):
    """Passes text through Spacy and extracts recognized skills."""
    doc = nlp(text)
    extracted_skills = []
    for ent in doc.ents:
        if ent.label_ == "SKILL":
            extracted_skills.append(ent.text)
    return sorted(list(set(extracted_skills)))


def analyze_quantitative_impact(text):
    """
    Factor 2: Experience & Impact
    Scans text for numerical metrics, percentages, and scale indicators.
    Returns a score out of 100 and a list of found metrics.
    """
    metric_patterns = re.findall(r'\b\d+(?:,\d+)*(?:\.\d+)?(?:\%|\+|\s*(?:users|clients|requests|ms|seconds|x|fold|dollars|\$|k|m))\b', text, re.IGNORECASE)
    
    unique_metrics = list(set(metric_patterns))
    score = min(100, len(unique_metrics) * 25) # 4 distinct metrics max out the score
    
    return {
        "score": score,
        "metrics_found": unique_metrics
    }


def analyze_format_and_scannability(text):
    """
    Factor 4: Format & Structure
    Evaluates text length, paragraph density, and structural cues.
    """
    words = text.split()
    word_count = len(words)
    
    length_score = 100
    if word_count < 200:
        length_score = 40 # Too sparse
    elif word_count > 1000:
        length_score = 60 # Too dense / multi-page wall of text
        
    return {
        "word_count": word_count,
        "length_score": length_score,
        "is_scannable": 300 <= word_count <= 900
    }


def calculate_comprehensive_score(resume_text, jd_text, resume_skills, jd_skills):
    """
    Combines Skills, Projects/Semantics, Experience Impact, and Format into a holistic score.
    """
    # 1. Semantic Match (BERT)
    embeddings = embedder.encode([resume_text, jd_text])
    similarity = cosine_similarity(embeddings[0].reshape(1, -1), embeddings[1].reshape(1, -1))[0][0]
    semantic_score = float(max(0.0, min(100.0, similarity * 100)))
    
    # 2. Skill Coverage Score
    if jd_skills:
        matched_skills = set(resume_skills).intersection(set(jd_skills))
        skill_coverage = (len(matched_skills) / len(jd_skills)) * 100
    else:
        skill_coverage = 50.0
        
    # 3. Impact Score
    impact_data = analyze_quantitative_impact(resume_text)
    
    # 4. Format Score
    format_data = analyze_format_and_scannability(resume_text)
    
    # Weighted Final Score Formula (Industry standard weighting)
    # Skills: 35%, Semantics/Projects: 35%, Quantitative Impact: 20%, Format: 10%
    final_score = (
        (skill_coverage * 0.35) +
        (semantic_score * 0.35) +
        (impact_data["score"] * 0.20) +
        (format_data["length_score"] * 0.10)
    )
    
    return {
        "final_score": round(final_score, 1),
        "breakdown": {
            "skills": round(skill_coverage, 1),
            "semantics": round(semantic_score, 1),
            "impact": impact_data["score"],
            "format": format_data["length_score"]
        },
        "metrics_found": impact_data["metrics_found"],
        "word_count": format_data["word_count"]
    }


def analyze_skill_gap(resume_skills, jd_skills):
    resume_set = set(resume_skills)
    jd_set = set(jd_skills)
    return {
        "missing": sorted(list(jd_set - resume_set)),
        "matching": sorted(list(jd_set.intersection(resume_set)))
    }