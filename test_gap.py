from src.agent import JobAgent

agent = JobAgent("data/resumes/my_resume.pdf")

top_jobs = agent.match_jobs(top_k=1)
job_id = top_jobs[0]["id"]

gap = agent.skill_gap(job_id)
print("\nSkill Gap Analysis:\n")
print(gap)
