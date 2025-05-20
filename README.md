# 🤖 LLM-Powered Resume Tailoring Tool

This project automates the process of tailoring LaTeX-formatted CVs and cover letters to match a specific job description using OpenAI GPT-4 and the CrewAI agent framework.

It includes three intelligent agents:
- 🕵️‍♂️ **Job Description Analyst** – Extracts key requirements from job postings
- 🧑‍💼 **CV Tailoring Expert** – Modifies LaTeX CVs to align with the job description
- ✉️ **Cover Letter Specialist** – Adjusts the cover letter to emphasize relevant experience

---

## 🗂️ Project Structure

| File | Description |
|------|-------------|
| `main.py` | Main script to run the agent-based tailoring pipeline |
| `JD.txt` | Input job description (manually copied from a job posting) |
| `CV.txt` | Original LaTeX-format CV |
| `Cover Letter.txt` | Original LaTeX-format cover letter |
| `CV_updated.txt` | Output: tailored LaTeX CV |
| `Cover_Letter_updated.txt` | Output: tailored LaTeX cover letter |
| `job_analysis.txt` | Output: bullet list of extracted job requirements |

---

## 🧠 How It Works

1. **Input**: Manually paste the job description into `JD.txt`.
2. **Run**: Execute `main.py`. It reads the input files and runs three CrewAI agents.
3. **Output**: Updated `CV` and `cover letter` are generated and saved as `.txt`.

Each agent runs independently but uses shared context. All outputs preserve LaTeX formatting and only modify allowed sections.

---

