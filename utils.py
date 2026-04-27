import pdfplumber

def extract_text_from_pdf(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            t = page.extract_text()
            if t:
                text += t + "\n"
    return text


def detect_sections(text):
    sections = {
        "education": [],
        "experience": [],
        "skills": [],
        "projects": [],
        "other": []
    }

    current = "other"

    for line in text.split("\n"):
        l = line.strip().lower()

        if "education" in l or "eğitim" in l:
            current = "education"
            continue

        if "experience" in l or "deneyim" in l:
            current = "experience"
            continue

        if "skill" in l or "yetenek" in l:
            current = "skills"
            continue

        if "project" in l or "proje" in l:
            current = "projects"
            continue

        if line.strip():
            sections[current].append(line.strip())

    return sections