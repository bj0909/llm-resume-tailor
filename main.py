import os
import openai
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI


def initialize_agents(api_key):
    openai.api_key = api_key
    os.environ["OPENAI_API_KEY"] = api_key
    return ChatOpenAI(model_name="gpt-4-turbo", temperature=0.3, openai_api_key=api_key)


def read_text_file(file_path: str) -> str:
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        print(f"Error reading {file_path}: {str(e)}")
        return ""

def validate_output(content: str) -> bool:
    return len(content.strip()) > 100  # Minimum viable content length

def save_text_file(file_path: str, content: str) -> bool:
    try:
        if not validate_output(content):
            print(f"Invalid content for {file_path}")
            return False

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        return True
    except Exception as e:
        print(f"Error saving {file_path}: {str(e)}")
        return False


def setup_agents(model):
    return [
        Agent(
            role='Job Description Analyst',
            goal='Extract key requirements from job descriptions',
            backstory='Expert in parsing and analyzing job postings',
            verbose=True,
            allow_delegation=False,
            llm=model,
            constraints=[
                "Never modify original job description content",
                "Identify key skills, technologies, and requirements",
                "Output should be a bullet-point list of key qualifications"
            ]
        ),
        Agent(
            role='CV Tailoring Expert',
            goal='Modify CV content to match job requirements without changing personal information',
            backstory='Professional resume writer with technical expertise',
            verbose=True,
            allow_delegation=False,
            llm=model,
            constraints=[
                "Preserve all personal information (name, contact, education dates)",
                "Maintain original LaTeX formatting",
                "Only modify work experience and skills sections",
                "Output must be complete LaTeX code",
                "ALWAYS return complete LaTeX documents between ```latex markers",
                "NEVER include markdown formatting",
                "PRESERVE original LaTeX headers and footers"
            ]
        ),
        Agent(
            role='Cover Letter Specialist',
            goal='Adapt cover letter to match job requirements',
            backstory='Experienced in crafting targeted cover letters',
            verbose=True,
            allow_delegation=False,
            llm=model,
            constraints=[
                "Maintain original structure and formatting",
                "Keep same overall length",
                "Focus on modifying body paragraphs",
                "Output must be complete LaTeX code",
                "ALWAYS return complete LaTeX documents between ```latex markers",
                "NEVER include markdown formatting",
                "PRESERVE original LaTeX headers and footers",
                "ONLY modify specified sections",
                "MAINTAIN original personal information"
            ]
        )
    ]


def create_tasks(jd_content, cv_content, cover_content):
    return [
        Task(
            description=f"Analyze this job description:\n{jd_content}",
            agent=agents[0],
            expected_output="Bullet list of key requirements and qualifications",
            output_file="job_analysis.txt"
        ),
        Task(
            description=f"""Modify CV to match these requirements:\n{{context}}\nCurrent CV:\n{cv_content}""",
            agent=agents[1],
            expected_output="Full LaTeX CV code with modified work experience/skills",
            output_file="CV_updated.txt"
        ),
        Task(
            description=f"""Adjust cover letter for these requirements:\n{{context}}\nCurrent Cover:\n{cover_content}""",
            agent=agents[2],
            expected_output="Full LaTeX cover letter with modified body paragraphs",
            output_file="Cover_Letter_updated.txt"
        )
    ]


# Execution flow
api_key = input("Enter your OpenAI API key: ")
model = initialize_agents(api_key)
agents = setup_agents(model)

# Read files
jd_content = read_text_file('JD.txt')
cv_content = read_text_file('CV.txt')
cover_content = read_text_file('Cover Letter.txt')

if not all([jd_content, cv_content, cover_content]):
    print("Error: Missing required file content")
    exit()

tasks = create_tasks(jd_content, cv_content, cover_content)

crew = Crew(
    agents=agents,
    tasks=tasks,
    verbose=True  # This is the corrected line
)

try:
    results = crew.kickoff()

    # Save results using proper TaskOutput attributes
    cv_output = tasks[1].output.raw if tasks[1].output else ""
    cover_output = tasks[2].output.raw if tasks[2].output else ""

    # Add before saving
    print("\n=== OUTPUT PREVIEW ===")
    print("CV Output Start:", cv_output[:100].replace('\n', ' ') if cv_output else "Empty")
    print("Cover Output Start:", cover_output[:100].replace('\n', ' ') if cover_output else "Empty")

    # Save files with validation
    if cv_output.strip():
        save_text_file('CV_updated.txt', str(cv_output))
        print(f"CV saved with {len(cv_output)} characters")
    else:
        print("CV output is empty!")

    if cover_output.strip():
        save_text_file('Cover_Letter_updated.txt', str(cover_output))
        print(f"Cover letter saved with {len(cover_output)} characters")
    else:
        print("Cover letter output is empty!")

except Exception as e:
    print(f"Error during processing: {str(e)}")