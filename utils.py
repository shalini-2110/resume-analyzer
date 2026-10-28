import re
import pdfplumber
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from skills import SKILLS, ALIASES

def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text  = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9+#.\-\s]", " ",text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def extract_skills(text):
    text = clean_text(text)
    found = set()

    # 1. Check the main skill names
    for skill in SKILLS:
        pattern = r"(?<![a-z0-9])" + re.escape(skill) + r"(?![a-z0-9])"
        if re.search(pattern, text):
            found.add(skill)

    # 2. Check aliases and add the standard skill name they map to
    for alias, skill in ALIASES.items():
        pattern = r"(?<![a-z0-9])" + re.escape(alias) + r"(?![a-z0-9])"
        if re.search(pattern, text):
            found.add(skill)

    return found


def skill_gap(resume_text, jd_text):
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)
    matched = resume_skills & jd_skills
    missing = jd_skills - resume_skills
    skill_score = (len(matched) / len(jd_skills) * 100) if jd_skills else 0
    return sorted(matched), sorted(missing), round(skill_score, 2)


def calculate_match_score(resume_text, jd_text):
    resume_clean = clean_text(resume_text)
    jd_clean = clean_text(jd_text)
    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform([resume_clean, jd_clean])
    score = cosine_similarity(vectors[0], vectors[1])[0][0]
    return round(score * 100, 2)


SECTIONS = ["education", "projects", "experience", "skills",
            "certifications", "achievements"]


def check_sections(resume_text):
    text = resume_text.lower()
    return {section: (section in text) for section in SECTIONS}
    

