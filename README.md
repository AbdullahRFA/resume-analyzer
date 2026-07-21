# 🚀 Resume Analyzer

![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)
![spaCy](https://img.shields.io/badge/NLP-spaCy-F9C352.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Build](https://img.shields.io/badge/build-passing-brightgreen.svg)

**Resume Analyzer** is an intelligent, NLP-driven application designed to automate the extraction, parsing, and analysis of candidate resumes. Built with Python 3.11, it utilizes natural language processing (spaCy) and advanced PDF parsing techniques to convert unstructured resume data into structured, actionable insights.

---

## 🌟 Key Features

* **Intelligent PDF Parsing:** Robust extraction of text and metadata from resume documents using a dedicated parsing module.
* **NLP & Entity Recognition:** Leverages `spaCy` to identify critical entities such as skills, education, experience, and contact information.
* **Modular Architecture:** Cleanly separated concerns with distinct parsing, processing engine, and application layers.
* **Research-Ready:** Includes Jupyter notebooks for transparent testing and model evaluation before deploying into the core application.
* **Cloud & Deployment Ready:** Configured with standard runtime profiles (`runtime.txt`, `setup.sh`, `packages.txt`) for immediate deployment to PaaS providers like Heroku or Render.

---

## 📂 Project Structure

```text
resume-analyzer/
├── app/                        # Core application package
│   ├── __init__.py
│   ├── engine.py               # Main NLP processing and analysis logic
│   ├── main.py                 # Application entry point / API routing
│   ├── parser.py               # Document extraction and parsing utilities
├── notebooks/                  # Experimental and testing environment
│   ├── 01_pdf_testing.ipynb    # PDF extraction benchmarks and tests
│   ├── 02_spacy_testing.ipynb  # spaCy NLP model training and NER tests
├── .python-version             # Specifies Python 3.11
├── info.md                     # General project information and context
├── knowledge.md                # Domain knowledge and logic documentation
├── packages.txt                # System-level dependencies
├── requirements.txt            # Python dependencies
├── runtime.txt                 # Runtime configuration (python-3.11)
└── setup.sh                    # Environment setup and initialization script
```

---

## ⚙️ Installation & Setup

### Prerequisites
* **Python:** `3.11` (Strictly enforced via `.python-version`)
* **pip:** Python package installer

### 1. Clone the Repository
```bash
git clone https://github.com/your-org/resume-analyzer.git
cd resume-analyzer
```

### 2. Environment Setup
We recommend using a virtual environment to manage dependencies:
```bash
python3.11 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

Alternatively, you can run the provided setup script which handles system dependencies and initialization:
```bash
bash setup.sh
```

### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```
*(Note: If the application requires system-level packages, refer to `packages.txt` for `apt-get` or `brew` equivalents).*

---

## 🚀 Usage

### Running the Application Core
To execute the main analyzer pipeline, run the entry point script:

```bash
python -m app.main
```

### Exploring the Notebooks
If you are developing new NLP rules or testing PDF parsing accuracy, spin up Jupyter Lab:

```bash
jupyter lab
```
*   **`01_pdf_testing.ipynb`**: Use this to validate how well `app.parser` handles varied PDF formats.
*   **`02_spacy_testing.ipynb`**: Use this to visualize Named Entity Recognition (NER) and tweak spaCy pipelines.

---

## 🧠 System Architecture

1. **Parser (`app/parser.py`):** Ingests raw PDF/Docx files, sanitizes the text, and normalizes the format.
2. **Engine (`app/engine.py`):** Takes the sanitized text and applies NLP models (spaCy) to categorize data into buckets (Skills, Experience, Education, Certifications).
3. **Main (`app/main.py`):** Orchestrates the workflow, handling I/O, user requests, and returning structured JSON or reports.

*(For deeper context into the architectural logic, please refer to `knowledge.md` and `info.md`).*

---

## 🤝 Contributing

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
