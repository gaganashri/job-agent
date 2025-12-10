import gradio as gr
from src.agent import JobAgent

agent = None   # will hold the loaded agent

def load_resume(resume_file):
    global agent
    agent = JobAgent(resume_file.name)
    return "Resume uploaded successfully! Choose an action."

def recommend_jobs():
    global agent
    if agent is None:
        return "Please upload a resume first."
    matches = agent.match_jobs(top_k=3)
    text = "### 🔥 Top Job Recommendations\n"
    for job in matches:
        text += f"- **{job['title']}** at **{job['company']}** ({job['location']}) — Score `{job['score']}`\n"
    return text

def skill_gap():
    global agent
    if agent is None:
        return "Please upload a resume first."
    top = agent.match_jobs(top_k=1)
    gap = agent.skill_gap(top[0]["id"])
    return f"""
### 🧩 Skill Gap Analysis  
**Job Title:** {gap['job_title']}  

**Required Skills:**  
{", ".join(gap['required_skills'])}  

**Missing Skills:**  
{", ".join(gap['missing_skills']) if gap['missing_skills'] else "None — You match very well!"}  
"""

def cover_letter():
    global agent
    if agent is None:
        return "Please upload a resume first."
    top = agent.match_jobs(top_k=1)
    job_id = top[0]["id"]
    letter = agent.generate_cover_letter(job_id)
    return f"### ✉️ Auto-Generated Cover Letter\n\n{letter}"

def improve_resume():
    global agent
    if agent is None:
        return "Please upload a resume first."
    result = agent.improve_resume()
    return f"### 📄 Resume Improvement Suggestions\n\n{result}"

def summary():
    global agent
    if agent is None:
        return "Please upload a resume first."
    result = agent.job_summary(top_k=3)
    return result


with gr.Blocks(title="AI Job Agent") as ui:
    gr.Markdown("# 🧠 AI Career Assistant\nUpload your resume to get personalized job insights!")

    resume_input = gr.File(label="📄 Upload Resume (PDF)")
    load_btn = gr.Button("Load Resume")

    out = gr.Markdown()

    load_btn.click(load_resume, inputs=resume_input, outputs=out)

    gr.Markdown("---")
    gr.Markdown("## Select an Action")

    with gr.Row():
        job_btn = gr.Button("🔥 Recommend Top Jobs")
        gap_btn = gr.Button("🧩 Skill Gap Analysis")
        cover_btn = gr.Button("✉️ Generate Cover Letter")
        improve_btn = gr.Button("📄 Improve Resume")
        summary_btn = gr.Button("📌 Job Summary Report")

    out2 = gr.Markdown()

    job_btn.click(recommend_jobs, outputs=out2)
    gap_btn.click(skill_gap, outputs=out2)
    cover_btn.click(cover_letter, outputs=out2)
    improve_btn.click(improve_resume, outputs=out2)
    summary_btn.click(summary, outputs=out2)

ui.launch()
