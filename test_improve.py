from src.agent import JobAgent

agent = JobAgent("data/resumes/my_resume.pdf")

print("\nImproving resume...\n")
print(agent.improve_resume())
