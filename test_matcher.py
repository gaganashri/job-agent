from src.job_scraper import load_jobs
from src.matcher import JobMatcher
from src.resume_parser import pdf_to_text

print("Loading resume...")
resume = pdf_to_text("data/resumes/my_resume.pdf")

print("Loading jobs...")
jobs = load_jobs()

print("Building matcher...")
matcher = JobMatcher()

print("Adding job descriptions to FAISS index...")
for job in jobs:
    matcher.add_job(job["id"], job["description"])

print("Searching best matches...")
matches = matcher.search(resume, top_k=3)

print("\nTop matches:")
for job_id, score in matches:
    print(f"Job ID: {job_id}, Match Score: {score}")
