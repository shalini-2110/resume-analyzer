# Resume Analyzer & Job Match Scorer

A web app that compares a resume with a job description using NLP and shows a match score, skill gaps and resume section checks.

**Live Demo:** PASTE_YOUR_STREAMLIT_LINK_HERE

## Features
- PDF resume text extraction
- TF-IDF and cosine similarity match score
- Skill extraction using word-boundary regex matching
- Matched vs. missing skills
- Resume section checker
- Downloadable report

## Tech Stack
Python, Streamlit, scikit-learn, pdfplumber, regex

## How It Works
1. Extract and clean text from the resume and job description
2. Compute TF-IDF vectors and cosine similarity
3. Detect skills from a curated list and compute skill overlap
4. Final score = 40% text similarity + 60% skill match

## Run Locally
```
git clone https://github.com/shalini-2110/resume-analyzer.git
cd resume-analyzer
pip install -r requirements.txt
streamlit run app.py
```

## Limitations
- No semantic understanding of synonyms
- Cannot read scanned or image PDFs

## Future Scope
- Sentence embeddings (BERT) for semantic matching
- OCR for scanned resumes