from src.agent import JobAgent

agent = JobAgent("data/resumes/my_resume.pdf")

# Match jobs and pick the best one
top = agent.match_jobs(top_k=1)
job_id = top[0]["id"]

print("\nGenerating cover letter...\n")
letter = agent.generate_cover_letter(job_id)
print(letter)
