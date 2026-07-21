# app/engine.py
import spacy
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# 1. Initialize Spacy
print("Loading Spacy NLP model...")
nlp = spacy.load("en_core_web_sm")

# Define our tech lexicon
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

# Inject the custom Entity Ruler
if "entity_ruler" not in nlp.pipe_names:
    ruler = nlp.add_pipe("entity_ruler", before="ner")
else:
    ruler = nlp.get_pipe("entity_ruler")

patterns = [{"label": "SKILL", "pattern": skill} for skill in tech_skills]
ruler.add_patterns(patterns)

# 2. Initialize the Sentence Transformer (BERT)
# This model converts sentences into high-dimensional numerical vectors
print("Loading Sentence Transformer model (this may take a moment on first run)...")
embedder = SentenceTransformer('all-MiniLM-L6-v2')


def extract_skills(text):
    """Passes text through Spacy and extracts recognized skills."""
    doc = nlp(text)
    extracted_skills = []
    
    for ent in doc.ents:
        if ent.label_ == "SKILL":
            extracted_skills.append(ent.text)
            
    return sorted(list(set(extracted_skills)))

def calculate_match_score(resume_text, jd_text):
    """
    Calculates the cosine similarity between the Resume and Job Description.
    Args:
        resume_text (str): Cleaned resume text.
        jd_text (str): Cleaned job description text.
    Returns:
        float: A percentage score (e.g., 85.5) representing the match.
    """
    # Convert texts into vectors
    # We put them in lists because the embedder expects a list of sentences
    embeddings = embedder.encode([resume_text, jd_text])
    
    resume_vector = embeddings[0]
    jd_vector = embeddings[1]
    
    # Calculate cosine similarity. 
    # It returns a 2D array, so we access [0][0] to get the raw float value.
    # We reshape the vectors to 1D arrays to avoid sklearn warnings
    similarity_matrix = cosine_similarity(resume_vector.reshape(1, -1), jd_vector.reshape(1, -1))
    
    raw_score = similarity_matrix[0][0]
    
    # Convert to a clean percentage (e.g., 0.8543 -> 85.4)
    percentage = round(raw_score * 100, 1)
    
    # Ensure it doesn't go below 0 or above 100
    return max(0.0, min(100.0, percentage))

def analyze_skill_gap(resume_skills, jd_skills):
    """
    Finds missing and matching skills using Set Mathematics.
    """
    # Convert lists to sets for fast comparison
    resume_set = set(resume_skills)
    jd_set = set(jd_skills)
    
    # Missing: What is in the JD, but NOT in the Resume?
    missing_skills = list(jd_set - resume_set)
    
    # Matching: What is in BOTH?
    matching_skills = list(jd_set.intersection(resume_set))
    
    return {
        "missing": sorted(missing_skills),
        "matching": sorted(matching_skills)
    }
