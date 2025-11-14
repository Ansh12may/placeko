
from langchain_openai import ChatOpenAI
from config import OPENAI_API_KEY, LLM_MODEL


class ResumeAgent:
    """Agent for analyzing and improving resumes with detailed feedback."""

    def __init__(self):
        self.api_key = OPENAI_API_KEY
        self.model = LLM_MODEL

    def analyze_resume(self, resume_data):
        """Analyze a resume and provide improvement suggestions."""
        skills = resume_data.get("skills", [])
        education = resume_data.get("education", [])
        experience = resume_data.get("experience", [])

        if not self.api_key:
            return self._generate_basic_analysis(resume_data)

        try:
            client = ChatOpenAI(
                openai_api_key=self.api_key,
                model=self.model,
                temperature=0.7
            )

            prompt = f"""
            Analyze this resume information and provide specific, actionable suggestions 
            for improvement to make it more competitive in the job market.

            === RESUME DATA ===
            Skills: {", ".join(skills)}

            Education: 
            {chr(10).join([f"- {edu}" for edu in education])}

            Experience:
            {chr(10).join([f"- {exp}" for exp in experience])}

            === ANALYSIS INSTRUCTIONS ===
            (same structured analysis sections as before)
            """

            response = client.invoke(prompt)
            return response.content.strip()

        except Exception as e:
            print(f"Error in resume analysis: {e}")
            return self._generate_basic_analysis(resume_data)

    def _generate_basic_analysis(self, resume_data):
        """Generate basic resume analysis when OpenAI is not available."""
        skills = resume_data.get("skills", [])
        education = resume_data.get("education", [])
        experience = resume_data.get("experience", [])

        analysis = "OVERALL ASSESSMENT\n\n"
        strengths = []
        if len(skills) >= 5:
            strengths.append("Good range of technical skills")
        if len(experience) >= 3:
            strengths.append("Solid work experience")
        if any("machine learning" in skill.lower() or "ai" in skill.lower() for skill in skills):
            strengths.append("Valuable AI/ML skills that are in high demand")

        analysis += "Strengths:\n" + "".join(f"• {s}\n" for s in strengths or ["Resume contains some relevant skills"])

        weaknesses = []
        if len(skills) < 5:
            weaknesses.append("Limited range of technical skills listed")
        if not any("python" in skill.lower() for skill in skills):
            weaknesses.append("Python (a widely used programming language) not explicitly listed")

        analysis += "\nWeaknesses:\n" + "".join(f"• {w}\n" for w in weaknesses or ["Consider adding more specific technical skills"])

        analysis += "\nCONTENT IMPROVEMENTS\n\n• Consider quantifying your achievements with specific metrics\n"
        analysis += "• Organize skills by category (programming languages, frameworks, tools)\n"
        analysis += "• Focus on highlighting relevant skills for your target roles\n"
        analysis += "\nFORMAT SUGGESTIONS\n\n• Use a clean, ATS-friendly format with clear section headings\n"
        analysis += "• Ensure consistent formatting (bullet points, dates, etc.)\n"
        analysis += "• Keep resume to 1-2 pages maximum\n"
        analysis += "\nATS OPTIMIZATION\n\n• Use keywords from job descriptions in your resume\n"
        analysis += "• Save your resume as a PDF to maintain formatting\n"
        analysis += "• Avoid tables, headers/footers, and images that can confuse ATS systems\n"

        return analysis
