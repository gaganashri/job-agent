from src.resume_parser import pdf_to_text
from src.job_scraper import load_jobs
from src.jd_parser import parse_jd
from src.matcher import JobMatcher

class JobAgent:
    def __init__(self, resume_path):
        print("[1] Extracting resume...")
        self.resume_text = pdf_to_text(resume_path)

        print("[2] Loading jobs...")
        self.jobs = load_jobs()

        print("[3] Preparing matcher...")
        self.matcher = JobMatcher()

        print("[4] Adding JDs to FAISS index...")
        for job in self.jobs:
            self.matcher.add_job(job["id"], job["description"])

        print("[5] Resume loaded and indexed. Agent ready!\n")

    def match_jobs(self, top_k=3):
        print("[6] Finding best matches for your resume...")
        matches = self.matcher.search(self.resume_text, top_k=top_k)

        results = []
        for job_id, score in matches:
            job = next(j for j in self.jobs if j["id"] == job_id)
            results.append({
                "id": job["id"],
                "title": job["title"],
                "company": job["company"],
                "location": job["location"],
                "score": float(score)
            })

        return results

    def explain_match(self, job_id):
        job = next(j for j in self.jobs if j["id"] == job_id)
        parsed = parse_jd(job["description"])
        return parsed
    def skill_gap(self, job_id):
        job = next(j for j in self.jobs if j["id"] == job_id)
        parsed = parse_jd(job["description"])

        required_skills = set(parsed.get("skills", []))
        resume_text_lower = self.resume_text.lower()

        missing = []
        for skill in required_skills:
            if skill.lower() not in resume_text_lower:
                missing.append(skill)

        return {
            "job_title": parsed.get("title"),
            "required_skills": list(required_skills),
            "missing_skills": missing
        }
    def generate_cover_letter(self, job_id):
        job = next(j for j in self.jobs if j["id"] == job_id)
        job_title = job["title"]
        company = job["company"]

        prompt = f"""
Write a professional, concise cover letter for the job '{job_title}' at '{company}'.

The letter should be based on:
1. The candidate's resume text below  
2. The job description  
3. The required skills

Resume:
\"\"\"{self.resume_text}\"\"\"

Job Description:
\"\"\"{job["description"]}\"\"\"
"""

        from openai import OpenAI
        from src.config import OPENAI_API_KEY, BASE_URL
        client = OpenAI(api_key=OPENAI_API_KEY, base_url=BASE_URL)

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
                max_tokens=400
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating cover letter: {e}"
    def improve_resume(self):
        prompt = f"""
You are an expert resume reviewer.

Analyze the following resume and provide:
1. A list of weaknesses  
2. Missing technical skills
3. Points to improve  
4. Strong areas to highlight  
5. A rewritten improved version of the resume summary section  

Resume:
\"\"\"{self.resume_text}\"\"\"
"""

        from openai import OpenAI
        from src.config import OPENAI_API_KEY, BASE_URL
        client = OpenAI(api_key=OPENAI_API_KEY, base_url=BASE_URL)

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=400,
                temperature=0
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error improving resume: {e}"
    def job_summary(self, top_k=3):
        top = self.match_jobs(top_k=top_k)

        output = "### 📌 Best Jobs for You Today\n\n"
        for job in top:
            explanation = self.explain_match(job["id"])
            output += f"**{job['title']} — {job['company']} ({job['location']})**\n"
            output += f"- Match Score: `{job['score']}`\n"
            output += f"- Required Skills: {', '.join(explanation.get('skills', []))}\n"
            output += f"- Summary: {explanation.get('summary')}\n\n"

        return output




# TEST
if __name__ == "__main__":
    agent = JobAgent("data/resumes/my_resume.pdf")

    print("\nTop Recommended Jobs:")
    top_jobs = agent.match_jobs(top_k=3)
    for job in top_jobs:
        print(job)

    print("\n\nExplanation for Top Match:")
    explanation = agent.explain_match(top_jobs[0]["id"])
    print(explanation)
