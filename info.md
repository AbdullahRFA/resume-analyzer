## Resume-to-Job Fit & Skill Gap Analyzer
**Real-world problem:** Applicants don't know why they get rejected; recruiters drown in mismatched resumes.
**Why it is important:** Democratizes hiring by telling applicants exactly what skills they are missing.
**Target users:** Job seekers, university career centers.
**Machine Learning task:** NLP / Recommendation.
**Dataset source:** Kaggle Resume Dataset and scraped LinkedIn/Indeed job descriptions.
**Features:** TF-IDF vectors, word embeddings, skill entities.
**ML algorithms:** Cosine Similarity, Spacy (NER), BERT embeddings.
**Expected accuracy:** Not strictly applicable; evaluated by Mean Reciprocal Rank (MRR) or human validation.
**Difficulty:** Medium.
**Estimated completion time:** 2.5 weeks.
**Future improvements:** Generating a personalized learning path to cover the skill gap.
Why this project is unique: It provides actionable feedback rather than just a binary "hired/rejected" classification.
Why my teacher will be impressed: Highly relevant to university students; excellent use of NLP for semantic matching.




```
resume-analyzer/
├── data/                      # Local data (Will be hidden from GitHub)
│   ├── resumes/               # Put sample PDF resumes here
│   └── job_descriptions/      # Put sample text files of JDs here
├── notebooks/                 # For Jupyter notebook experiments
│   ├── 01_pdf_testing.ipynb   # Test PyPDF2 here first
│   └── 02_spacy_testing.ipynb # Test your NER model here
├── app/                       # Your final, clean application code
│   ├── __init__.py            # Tells Python this is a module (leave empty)
│   ├── main.py                # The Streamlit UI file (run this to start the app)
│   ├── parser.py              # Functions to extract text from PDFs
│   └── engine.py              # The ML functions (Spacy and BERT logic)
├── .gitignore                 # Tells Git which files to ignore (like the data folder)
├── requirements.txt           # List of your Python libraries
└── README.md                  # Project description for your professor/recruiters
```


# 1. Create the virtual environment named 'env'
python3 -m venv env

# 2. Activate the virtual environment
source env/bin/activate

# 3. Install all the libraries from your requirements file
pip install -r requirements.txt

# 4. Download the base English NLP model for Spacy
python3 -m spacy download en_core_web_sm

# for runnig strealit
streamlit run main.py