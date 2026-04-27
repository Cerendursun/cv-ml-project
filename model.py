import pickle
import os

if not os.path.exists("model.pkl"):
    raise Exception("model.pkl yok! önce train.py çalıştır")

model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))


def predict_score(text):
    vec = vectorizer.transform([text])
    return int(model.predict(vec)[0])


def analyze_cv(sections):

    skills_list = [
        "python","sql","machine learning","deep learning",
        "flask","django","react","docker","aws","git"
    ]

    text = " ".join(sections["skills"]).lower()

    found_skills = [s for s in skills_list if s in text]

    analysis = {
        "skills_found": found_skills,
        "skill_score": round(len(found_skills) / len(skills_list) * 100),
        "experience_count": len(sections["experience"]),
        "experience_summary": sections["experience"][:5],
    }

    return analysis


def cv_level(score):
    if score < 40:
        return "🟤 Junior"
    elif score < 70:
        return "🟡 Intermediate"
    elif score < 90:
        return "🟢 Advanced"
    else:
        return "🔥 Senior"


def cv_feedback(sections, analysis):
    tips = []

    if len(analysis["skills_found"]) < 3:
        tips.append("Daha fazla teknik skill eklemelisin")

    if "github" not in " ".join(sections["other"]).lower():
        tips.append("GitHub projeleri çok önemli")

    if len(sections["experience"]) == 0:
        tips.append("Deneyim kısmı eksik görünüyor")

    if "sql" not in " ".join(sections["skills"]).lower():
        tips.append("SQL öğrenmek seni öne çıkarır")

    return tips


def final_score(analysis):
    score = 0
    score += analysis["skill_score"] * 0.5
    score += min(analysis["experience_count"] * 10, 40)
    return min(round(score), 100)