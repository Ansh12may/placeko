
import streamlit as st
import pandas as pd
import os
import json
import tempfile
import PyPDF2
import  docx
from datetime import datetime, timedelta

# Create directories if they don't exist
os.makedirs("agents", exist_ok=True)
os.makedirs("utils", exist_ok=True)
os.makedirs("saved_jobs", exist_ok=True)
os.makedirs("saved_interviews", exist_ok=True)

# Import the UI utilities for improved display
from ui_utils import (
    display_formatted_analysis, 
    display_resume_analysis_summary,
    display_extracted_information,
    format_job_description,
    display_matching_skills,
    apply_styling
)

# Import job storage functions
from utils.job_storage import (
    save_job_to_local,
    load_saved_jobs,
    remove_saved_job
)

# Import configuration
from config import COLORS, JOB_PLATFORMS

# Set page configuration with professional appearance
st.set_page_config(
    page_title="PLACEKO",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Apply custom styling from ui_utils
apply_styling()

# Initialize tools and agents
@st.cache_resource
def load_resources():
    """Load and cache all required resources."""
    from utils.resume_parser import ResumeParser
    from utils.serp_api_searcher import SerpApiSearcher
    from utils.resume_keyword_extractor import ResumeKeywordExtractor
    from agents.resume_agent import ResumeAgent
    from agents.job_search_agent import JobSearchAgent
    from agents.interview_agent import InterviewAgent
    
    resume_parser = ResumeParser()
    resume_agent = ResumeAgent()
    job_search_agent = JobSearchAgent()
    interview_agent = InterviewAgent()
    serp_api_searcher = SerpApiSearcher()
    keyword_extractor = ResumeKeywordExtractor()
    
    return {
        "resume_parser": resume_parser,
        "resume_agent": resume_agent,
        "job_search_agent": job_search_agent,
        "interview_agent": interview_agent,
        "serp_api_searcher": serp_api_searcher,
        "keyword_extractor": keyword_extractor
    }

# Load resources
resources = load_resources()

# Website-style header/navbar
st.markdown(f"""
<div style='
    background: white;
    border-bottom: 1px solid {COLORS["border"]};
    padding: 1.5rem 0;
    margin-bottom: 3rem;
    position: sticky;
    top: 0;
    z-index: 100;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
'>
    <div style='max-width: 1200px; margin: 0 auto; padding: 0 2rem; display: flex; justify-content: space-between; align-items: center;'>
        <div style='display: flex; align-items: center;'>
            <h1 style='margin: 0; font-size: 1.75rem; font-weight: 700; color: {COLORS["text_dark"]};'>
                💼 PLACEKO
            </h1>
        </div>
        <div style='display: flex; gap: 2rem; align-items: center;'>
            <span style='color: {COLORS["text_medium"]}; font-size: 0.95rem;'>AI-Powered Job Search Platform</span>
        </div>
    </div>
</div>

<div style='
    max-width: 1200px;
    margin: 0 auto 3rem auto;
    padding: 4rem 2rem;
    background: {COLORS["gradient1"]};
    border-radius: 16px;
    text-align: center;
    box-shadow: 0 4px 20px rgba(0, 122, 255, 0.15);
'>
    <h1 style='color: white; font-size: 3.5rem; margin-bottom: 1.5rem; font-weight: 700; line-height: 1.2;'>
        Find Your Dream Job
    </h1>
    <p style='color: rgba(255,255,255,0.95); font-size: 1.25rem; margin-bottom: 2rem; line-height: 1.6; max-width: 700px; margin-left: auto; margin-right: auto;'>
        AI-powered job search, resume analysis, and interview preparation all in one place
    </p>
    <div style='display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap;'>
        <div style='background: rgba(255,255,255,0.15); backdrop-filter: blur(10px); padding: 0.75rem 1.5rem; border-radius: 8px; color: white; font-weight: 500;'>
            🤖 Smart Job Matching
        </div>
        <div style='background: rgba(255,255,255,0.15); backdrop-filter: blur(10px); padding: 0.75rem 1.5rem; border-radius: 8px; color: white; font-weight: 500;'>
            📄 Resume Analysis
        </div>
        <div style='background: rgba(255,255,255,0.15); backdrop-filter: blur(10px); padding: 0.75rem 1.5rem; border-radius: 8px; color: white; font-weight: 500;'>
            🎯 Interview Prep
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Session state initialization
if "resume_data" not in st.session_state:
    st.session_state.resume_data = {}
if "job_results" not in st.session_state:
    st.session_state.job_results = []
if "selected_job" not in st.session_state:
    st.session_state.selected_job = None
if "interview_questions" not in st.session_state:
    st.session_state.interview_questions = None
if "saved_jobs" not in st.session_state:
    st.session_state.saved_jobs = load_saved_jobs()

# Create main navigation tabs
tabs = st.tabs([
    "📄 Resume Analysis", 
    "🔍 Job Search", 
    "🎯 Interview Preparation", 
    "💼 Saved Jobs"
])

# Make sure the correct tab is active if coming from another section
if hasattr(st.session_state, 'active_tab'):
    active_tab_index = st.session_state.active_tab
    # We can't directly set the active tab, so we'll rely on session state changes to indicate
    # which tab should be active when the page reruns

# Tab 1: Resume Analysis
with tabs[0]:
    st.markdown("<div style='margin-bottom: 2rem;'></div>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='color: {COLORS['text_dark']}; margin-bottom: 0.5rem;'>Resume Analysis</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: {COLORS['text_medium']}; margin-bottom: 2rem; font-size: 1.1rem;'>Upload your resume to get AI-powered analysis and insights</p>", unsafe_allow_html=True)
    
    # Create two columns for upload options
    col1, col2 = st.columns(2)
    
    with col1:
        # Resume upload section
        st.subheader("Upload Resume")
        st.markdown(f"""
        <div style="background-color: {COLORS["card_bg"]}; padding: 20px; border-radius: 8px; margin-bottom: 20px; border: 1px solid {COLORS["border"]}; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
        <p style="margin-bottom: 12px; color: {COLORS["text_dark"]}; font-size: 1rem; font-weight: 500;">📄 Upload your resume in PDF, DOCX, or TXT format.</p>
        <p style="margin: 0; color: {COLORS["text_medium"]}; font-size: 0.95rem; line-height: 1.6;">We'll analyze your resume and extract key information to help you find matching jobs.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Custom label for file uploader to ensure visibility
        st.markdown(f"""
        <div style="margin-bottom: 10px;">
            <label style="color: {COLORS['text_dark']}; font-weight: 700; font-size: 1.1rem; display: block; margin-bottom: 8px;">
                Upload your resume
            </label>
        </div>
        """, unsafe_allow_html=True)
        
        # Resume file uploader
        resume_file = st.file_uploader("", type=["pdf", "txt", "docx"], key="resume_uploader", label_visibility="collapsed")
        
        # Process uploaded resume
        if resume_file is not None:
            with st.spinner("Analyzing your resume..."):
                try:
                    # Load resume parser
                    resume_parser = resources["resume_parser"]
                    
                    # Save uploaded file to a temporary location
                    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{resume_file.name.split('.')[-1]}") as temp_file:
                        temp_file.write(resume_file.getbuffer())
                        temp_path = temp_file.name
                    
                    # Read the file content
                    try:
                        # For PDF files
                        if temp_path.endswith('.pdf'):
                            with open(temp_path, 'rb') as f:
                                pdf_reader = PyPDF2.PdfReader(f)
                                extracted_text = ""
                                for page_num in range(len(pdf_reader.pages)):
                                    page = pdf_reader.pages[page_num]
                                    extracted_text += page.extract_text() + "\n"
                        
                        # For DOCX files
                        elif temp_path.endswith('.docx'):
                            doc = docx.Document(temp_path)
                            extracted_text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
                        
                        # For TXT files
                        else:
                            with open(temp_path, 'r', encoding='utf-8', errors='ignore') as f:
                                extracted_text = f.read()
                        
                        # Clean up the temporary file
                        try:
                            os.unlink(temp_path)
                        except:
                            pass
                        
                        # If we got text, parse it
                        if extracted_text:
                            # Parse resume and extract info
                            resume_data = resume_parser.parse_resume(extracted_text)
                            
                            # Get AI analysis
                            resume_agent = resources["resume_agent"]
                            resume_analysis = resume_agent.analyze_resume(resume_data)
                            
                            # Store resume data and analysis in session state
                            st.session_state.resume_data = resume_data
                            st.session_state.resume_data["analysis"] = resume_analysis
                            st.session_state.resume_data["raw_text"] = extracted_text
                            
                            # Display highly visible success message
                            st.markdown(f"""
                            <div style="background: {COLORS['success']}; color: white; padding: 20px; 
                            border-radius: 12px; margin: 20px 0; box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
                            border-left: 6px solid #059669;">
                                <h3 style="color: white; margin: 0 0 10px 0; font-weight: 700; font-size: 1.3rem; text-shadow: 0 2px 4px rgba(0,0,0,0.2);">
                                    ✅ Resume Analysis Complete!
                                </h3>
                                <p style="color: white; margin: 0; font-size: 1.1rem; font-weight: 500; text-shadow: 0 1px 2px rgba(0,0,0,0.2);">
                                    Review the extracted information and analysis below.
                                </p>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.error("Could not extract text from the uploaded file.")
                    except Exception as file_error:
                        st.error(f"Error processing file: {str(file_error)}")
                        st.info("If the error persists, try uploading a different file format or check if the resume is properly formatted.")
                        
                except Exception as e:
                    st.error(f"Error analyzing resume: {str(e)}")
                    st.info("If the error persists, try uploading a different file format or check if the resume is properly formatted.")
    
    with col2:
        # Resume tips and advice
        st.subheader("Resume Tips")
        st.markdown(f"""
        <div style="background-color: {COLORS["accent1"]}; color: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
        <h4 style="margin-top: 0; color: white;">Key Resume Components:</h4>
        <ul style="margin-bottom: 0;">
        <li><strong>Clear contact information</strong> - Make it easy for employers to reach you</li>
        <li><strong>Relevant skills section</strong> - Highlight technical and soft skills</li>
        <li><strong>Quantified achievements</strong> - Use numbers to demonstrate impact</li>
        <li><strong>ATS-friendly format</strong> - Use standard headings and keywords</li>
        <li><strong>Consistent formatting</strong> - Maintain professional appearance</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # ATS optimization tips
        st.markdown(f"""
        <div style="background-color: {COLORS["secondary"]}; color: white; padding: 15px; border-radius: 8px; margin-top: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
        <h4 style="margin-top: 0; color: white;">ATS Optimization Tips:</h4>
        <ul style="margin-bottom: 0;">
        <li>Use keywords from the job description</li>
        <li>Avoid tables, headers/footers, and images</li>
        <li>Use standard section headings</li>
        <li>Submit in PDF format when possible</li>
        <li>Keep formatting simple and clean</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Display resume analysis results if available
    if "resume_data" in st.session_state and st.session_state.resume_data:
        st.markdown("---")
        
        # Create tabs for different views of resume data
        resume_tabs = st.tabs(["Summary", "Skills & Experience", "Analysis", "Raw Text"])
        
        # Tab 1: Summary view
        with resume_tabs[0]:
            display_resume_analysis_summary(st.session_state.resume_data)
        
        # Tab 2: Skills & Experience
        with resume_tabs[1]:
            display_extracted_information(st.session_state.resume_data)
        
        # Tab 3: Analysis
        with resume_tabs[2]:
            if "analysis" in st.session_state.resume_data:
                display_formatted_analysis(st.session_state.resume_data["analysis"])
            else:
                st.info("No detailed analysis available. Please re-upload your resume to generate an analysis.")
        
        # Tab 4: Raw Text
        with resume_tabs[3]:
            if "raw_text" in st.session_state.resume_data:
                st.text_area("Extracted Text", st.session_state.resume_data["raw_text"], height=400, disabled=True)
            else:
                st.info("Raw text not available.")
        
        # Add a section to explain resume improvement suggestions
        with st.expander("Resume Improvement Recommendations", expanded=False):
            st.markdown(f"""
            <div style="background-color: {COLORS["card_bg"]}; padding: 20px; border-radius: 8px; margin: 10px 0; border: 1px solid {COLORS["border"]}; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
            <h4 style="color: {COLORS["primary"]}; margin-top: 0; margin-bottom: 15px;">How to Improve Your Resume</h4>
            <p style="color: {COLORS["text_dark"]}; margin-bottom: 15px;">Based on our analysis, here are some suggestions to enhance your resume:</p>
            <ul style="color: {COLORS["text_dark"]}; line-height: 1.8;">
            <li style="margin-bottom: 10px;"><strong style="color: {COLORS["text_dark"]};">Keyword Optimization:</strong> <span style="color: {COLORS["text_medium"]};">Add more industry-specific keywords that appear in job descriptions you're targeting.</span></li>
            <li style="margin-bottom: 10px;"><strong style="color: {COLORS["text_dark"]};">Quantify Achievements:</strong> <span style="color: {COLORS["text_medium"]};">Add numbers and percentages to demonstrate the impact of your work.</span></li>
            <li style="margin-bottom: 10px;"><strong style="color: {COLORS["text_dark"]};">Technical Skills:</strong> <span style="color: {COLORS["text_medium"]};">Ensure all relevant technical skills are clearly listed in a dedicated section.</span></li>
            <li style="margin-bottom: 10px;"><strong style="color: {COLORS["text_dark"]};">Action Verbs:</strong> <span style="color: {COLORS["text_medium"]};">Start achievement bullets with strong action verbs like "Implemented," "Developed," or "Reduced."</span></li>
            <li style="margin-bottom: 10px;"><strong style="color: {COLORS["text_dark"]};">Formatting:</strong> <span style="color: {COLORS["text_medium"]};">Ensure consistent formatting and eliminate any complex design elements that might confuse ATS systems.</span></li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
    else:
        # Display a message when no resume is uploaded
        st.markdown(f"""
        <div style="background-color: {COLORS["background"]}; padding: 20px; border-radius: 8px; border: 1px dashed {COLORS["primary"]}; text-align: center; margin-top: 30px;">
        <img src="https://img.icons8.com/fluency/96/000000/resume.png" style="width: 64px; height: 64px; margin-bottom: 15px;">
        <h3 style="color: {COLORS["primary"]};">No Resume Uploaded</h3>
        <p>Upload your resume using the file uploader above to see the analysis.</p>
        </div>
        """, unsafe_allow_html=True)

# Tab 2: Job Search
with tabs[1]:
    st.markdown("<div style='margin-bottom: 2rem;'></div>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='color: {COLORS['text_dark']}; margin-bottom: 0.5rem;'>Job Search</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: {COLORS['text_medium']}; margin-bottom: 2rem; font-size: 1.1rem;'>Search for jobs across multiple platforms with AI-powered matching</p>", unsafe_allow_html=True)
    
    # Common job titles and locations
    common_job_titles = [
        "Data Scientist", "Software Engineer", "Product Manager", "Data Analyst",
        "Machine Learning Engineer", "Frontend Developer", "Backend Developer",
        "Full Stack Developer", "DevOps Engineer", "UX Designer", "AI Engineer",
        "Cloud Architect", "Database Administrator", "Project Manager", "Business Analyst",
        "Java Developer", "Python Developer", "React Developer", "Android Developer",
        "iOS Developer", "Node.js Developer", "Data Engineer", "Blockchain Developer",
        "Cybersecurity Analyst", "Quality Assurance Engineer"
    ]
    
    locations = [
        "Remote",
        "New York, NY", "San Francisco, CA", "Seattle, WA", "Austin, TX",
        "Boston, MA", "Chicago, IL", "Los Angeles, CA", "Atlanta, GA", "Denver, CO",
        "Bangalore, India", "Hyderabad, India", "Mumbai, India", "Delhi, India",
        "Pune, India", "Chennai, India", "London, UK", "Berlin, Germany", "Toronto, Canada"
    ]
    
    # Create search tabs
    search_tabs = st.tabs(["📄 Resume-Based Search", "🔍 Custom Search"])
    
    # Resume-Based Search Tab
    with search_tabs[0]:
        if st.session_state.resume_data:
            st.subheader("Find Jobs Matching Your Resume")
            st.markdown(f"""
            <div style="background-color: {COLORS["card_bg"]}; padding: 18px; border-radius: 8px; margin-bottom: 15px; border: 1px solid {COLORS["border"]}; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
            <p style="font-weight: 500; margin-bottom: 0; color: {COLORS["text_dark"]}; font-size: 1rem;">This will extract keywords from your resume and search for relevant jobs automatically.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Extract skills preview from resume
            skills_preview = ", ".join(st.session_state.resume_data.get("skills", [])[:5])
            if skills_preview:
                st.markdown(f"""
                <div style="background-color: {COLORS["secondary"]}; color: white; 
                padding: 10px; border-radius: 8px; margin-bottom: 1rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <p style="margin: 0; font-weight: 600; text-shadow: 1px 1px 2px rgba(0,0,0,0.2);">
                <span style="font-weight: bold;">Top Skills:</span> {skills_preview}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Create two columns for location and search button
            col1, col2 = st.columns([3, 1])
            
            with col1:
                default_location = st.selectbox(
                    "Location:",
                    locations,
                    index=0,
                    key="resume_search_location"
                )
            
            with col2:
                resume_search_button = st.button(
                    "Search Jobs",
                    key="resume_based_search"
                )
            
            if resume_search_button:
                with st.spinner("Extracting key skills and experience from your resume..."):
                    try:
                        # Use the keyword extractor
                        keyword_extractor = resources["keyword_extractor"]
                        search_keywords = keyword_extractor.extract_keywords(st.session_state.resume_data)
                        
                        # Get potential job title
                        job_title = keyword_extractor.extract_job_title(st.session_state.resume_data)
                        
                        # Join with spaces
                        resume_based_query = " ".join(search_keywords)
                        
                        # Display the extracted keywords
                        st.subheader("Extracted Search Terms")
                        
                        # Display with improved contrast
                        st.markdown(f"""
                        <div style="background-color: {COLORS["primary"]}; color: white; 
                        padding: 15px; border-radius: 8px; margin-bottom: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                            <p style="margin-bottom: 8px; font-weight: bold; font-size: 1.1rem; text-shadow: 1px 1px 2px rgba(0,0,0,0.2);">
                            <span style="font-weight: bold;">Job Title:</span> {job_title.title()}</p>
                            <p style="margin-bottom: 8px; text-shadow: 1px 1px 2px rgba(0,0,0,0.2);">
                            <span style="font-weight: bold;">Keywords:</span> {resume_based_query}</p>
                            <p style="margin-bottom: 0; text-shadow: 1px 1px 2px rgba(0,0,0,0.2);">
                            <span style="font-weight: bold;">Location:</span> {default_location}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Allow user to modify the search terms
                        with st.expander("Modify Search Terms", expanded=False):
                            modified_query = st.text_input("Edit Keywords:", value=resume_based_query)
                            modified_location = st.text_input("Edit Location:", value=default_location)
                            if st.button("Update Search Terms"):
                                resume_based_query = modified_query
                                default_location = modified_location
                                st.success("Search terms updated!")
                        
                        # Search for jobs
                        with st.spinner(f"Searching for jobs matching your resume profile..."):
                            serp_api_searcher = resources["serp_api_searcher"]
                            resume_based_jobs = []
                            
                            # Search on all platforms
                            for platform in JOB_PLATFORMS:
                                try:
                                    platform_jobs = serp_api_searcher.search_jobs(
                                        resume_based_query,
                                        default_location,
                                        platform=platform,
                                        count=5  # Limit to 5 jobs per platform
                                    )
                                    resume_based_jobs.extend(platform_jobs)
                                except Exception as e:
                                    st.error(f"Error searching jobs on {platform}: {str(e)}")
                            
                            # Update job results
                            st.session_state.job_results = resume_based_jobs
                            st.success(f"Found {len(resume_based_jobs)} jobs matching your resume profile!")
                            st.rerun()  # Refresh to show results
                    except Exception as e:
                        st.error(f"Error processing resume data: {str(e)}")
        else:
            st.warning("Please upload your resume in the Resume Analysis tab to enable resume-based job search.")
            
            st.markdown(f"""
            <div style="background-color: {COLORS["card_bg"]}; padding: 20px; border-radius: 8px; border: 1px solid {COLORS["border"]}; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
            <ol style="margin-left: 20px; margin-bottom: 0; color: {COLORS["text_dark"]}; line-height: 1.8;">
            <li style="margin-bottom: 8px; color: {COLORS["text_dark"]};">Go to the Resume Analysis tab</li>
            <li style="margin-bottom: 8px; color: {COLORS["text_dark"]};">Upload your resume (PDF, DOCX, or TXT)</li>
            <li style="margin-bottom: 0; color: {COLORS["text_dark"]};">Return to this tab to search for jobs based on your resume</li>
            </ol>
            </div>
            """, unsafe_allow_html=True)
    
    # Custom Search Tab
    with search_tabs[1]:
        # Job search form
        with st.form("job_search_form"):
            st.subheader("Search Criteria")
            
            # Create a 2-column layout for job title and location
            col1, col2 = st.columns(2)
            
            with col1:
                keywords = st.selectbox("Job Title:", common_job_titles, key="job_titles")
            
            with col2:
                location = st.selectbox("Location:", locations, key="locations")
            
            # Advanced filters accordion
            with st.expander("Advanced Filters", expanded=False):
                # Job type selection
                job_types = ["Full-time", "Part-time", "Contract", "Internship", "Remote"]
                selected_job_types = st.multiselect("Job Types (optional):", job_types, key="job_types")
                
                # Experience level
                experience_level = st.select_slider(
                    "Years of experience:",
                    options=["0-1", "1-3", "3-5", "5-10", "10+"],
                    value="1-3",
                    key="experience_level"
                )
                
                # Recency filter
                recency = st.select_slider(
                    "Show jobs posted within:",
                    options=["1 day", "3 days", "1 week", "2 weeks", "1 month", "Any time"],
                    value="1 week",
                    key="recency"
                )
                
                # Platform selection
                selected_platforms = st.multiselect(
                    "Job Platforms:",
                    options=JOB_PLATFORMS,
                    default=JOB_PLATFORMS,
                    key="platforms"
                )
                
                # Number of results
                job_count = st.slider("Jobs per platform:", 3, 20, 5, key="job_count")
                
                # Use SerpAPI option
                use_serp_api = st.checkbox("Use SerpAPI for real job listings", value=True, key="use_serp_api")
            
            submit_search = st.form_submit_button("Search Jobs")
        
        # Execute job search
        if submit_search:
            # Build the search query including job types and experience
            search_query = keywords
            
            # Add job types to query if selected
            if selected_job_types:
                search_query += f" {' '.join(selected_job_types)}"
            
            # Add experience level to query if needed
            if experience_level != "1-3":  # If not default
                search_query += f" {experience_level} years"
            
            # Convert recency to days for API
            recency_days = {
                "1 day": 1, "3 days": 3, "1 week": 7,
                "2 weeks": 14, "1 month": 30, "Any time": 365
            }
            days_ago = recency_days.get(recency, 7)
            
            if not st.session_state.resume_data:
                st.warning("Please upload and analyze your resume first for better job matching.")
            
            search_message = f"Searching for {search_query} jobs in {location}"
            search_message += f" posted within the last {recency}"
            if selected_job_types:
                search_message += f" ({', '.join(selected_job_types)})"
            
            with st.spinner(search_message):
                jobs = []
                
                if use_serp_api:
                    # Use SerpAPI to get real job listings
                    serp_api_searcher = resources["serp_api_searcher"]
                    for platform in selected_platforms:
                        try:
                            platform_jobs = serp_api_searcher.search_jobs(
                                search_query,
                                location,
                                platform=platform,
                                count=job_count,
                                days_ago=days_ago
                            )
                            jobs.extend(platform_jobs)
                        except Exception as e:
                            st.error(f"Error searching jobs on {platform}: {str(e)}")
                    
                    if not jobs:
                        st.warning("No jobs found via SerpAPI. Falling back to standard search.")
                        job_search_agent = resources["job_search_agent"]
                        try:
                            jobs = job_search_agent.search_jobs(
                                st.session_state.resume_data,
                                search_query,
                                location,
                                platforms=selected_platforms,
                                count=job_count
                            )
                        except Exception as e:
                            st.error(f"Error in job search: {str(e)}")
                else:
                    # Use standard job search
                    job_search_agent = resources["job_search_agent"]
                    try:
                        jobs = job_search_agent.search_jobs(
                            st.session_state.resume_data,
                            search_query,
                            location,
                            platforms=selected_platforms,
                            count=job_count
                        )
                    except Exception as e:
                        st.error(f"Error in job search: {str(e)}")
                
                st.session_state.job_results = jobs
    
    # Display job results (common to both search methods)
    if st.session_state.job_results:
        total_jobs = len(st.session_state.job_results)
        st.subheader(f"Job Results ({total_jobs})")
        
        # Filter options
        col1, col2 = st.columns(2)
        with col1:
            # Sort options
            sort_option = st.selectbox(
                "Sort by:",
                ["Most Recent", "Relevance", "Company Name", "Location"],
                key="sort_option"
            )
        
        with col2:
            # Filter by platform
            filter_platform = st.selectbox(
                "Filter by platform:",
                ["All Platforms"] + JOB_PLATFORMS,
                key="filter_platform"
            )
        
        # Apply platform filter
        filtered_jobs = st.session_state.job_results
        if filter_platform != "All Platforms":
            filtered_jobs = [job for job in filtered_jobs if job.get("platform", "").lower() == filter_platform.lower()]
        
        # Sort jobs based on selection
        sorted_jobs = filtered_jobs.copy()
        if sort_option == "Most Recent":
            # Try to parse dates for sorting
            for job in sorted_jobs:
                if job.get("date_posted") and isinstance(job["date_posted"], str):
                    try:
                        if "hour" in job["date_posted"].lower():
                            hours = int(''.join(filter(str.isdigit, job["date_posted"].split()[0])))
                            job["sort_date"] = datetime.now() - timedelta(hours=hours)
                        elif "day" in job["date_posted"].lower():
                            days = int(''.join(filter(str.isdigit, job["date_posted"].split()[0])))
                            job["sort_date"] = datetime.now() - timedelta(days=days)
                        elif "week" in job["date_posted"].lower():
                            weeks = int(''.join(filter(str.isdigit, job["date_posted"].split()[0])))
                            job["sort_date"] = datetime.now() - timedelta(weeks=weeks)
                        elif "month" in job["date_posted"].lower():
                            months = int(''.join(filter(str.isdigit, job["date_posted"].split()[0])))
                            job["sort_date"] = datetime.now() - timedelta(days=30 * months)
                        else:
                            job["sort_date"] = datetime.now() - timedelta(days=365)
                    except (ValueError, IndexError):
                        job["sort_date"] = datetime.now() - timedelta(days=365)
                else:
                    job["sort_date"] = datetime.now() - timedelta(days=365)
            
            sorted_jobs.sort(key=lambda x: x.get("sort_date"), reverse=False)
        elif sort_option == "Company Name":
            sorted_jobs.sort(key=lambda x: x.get("company", "").lower())
        elif sort_option == "Location":
            sorted_jobs.sort(key=lambda x: x.get("location", "").lower())
        
        if not sorted_jobs:
            st.warning(f"No jobs found for the selected platform: {filter_platform}")
        else:
            # Create a dataframe for easier display
            job_df = pd.DataFrame([
                {
                    "Title": job["title"],
                    "Company": job["company"],
                    "Location": job.get("location", "Not specified"),
                    "Platform": job.get("platform", "Unknown"),
                    "Posted": job.get("date_posted", "Recent"),
                    "Job Type": job.get("job_type", ""),
                    "Real Job": "✓" if job.get("is_real_job", False) else "?"
                }
                for job in sorted_jobs
            ])
            
            # Display jobs in a dataframe with improved styling
            st.dataframe(
                job_df,
                use_container_width=True,
                column_config={
                    "Title": st.column_config.TextColumn("Job Title"),
                    "Real Job": st.column_config.TextColumn("Verified")
                },
                hide_index=True
            )
            
            # Job selection for detailed view
            if sorted_jobs:
                st.markdown("### Job Details")
                selected_index = st.selectbox(
                    "Select a job to view details:",
                    range(len(sorted_jobs)),
                    format_func=lambda i: f"{sorted_jobs[i]['title']} at {sorted_jobs[i]['company']}",
                    key="job_selection"
                )
                
                if selected_index is not None:
                    st.session_state.selected_job = sorted_jobs[selected_index]
                    selected_job = st.session_state.selected_job
                    
                    # Job title and company with beautiful gradient styling
                    st.markdown(f"""
                    <div style='background: {COLORS["gradient1"]}; 
                    padding: 1.5rem; border-radius: 16px; margin-bottom: 1.5rem; box-shadow: 0 8px 25px rgba(99, 102, 241, 0.3);'>
                        <h3 style='color: white; margin: 0; font-weight: 700; text-shadow: 0 2px 4px rgba(0,0,0,0.3); 
                        font-size: 1.8rem;'>{selected_job['title']}</h3>
                        <p style='color: white; font-size: 1.3rem; margin: 0.8rem 0 0 0; text-shadow: 0 2px 4px rgba(0,0,0,0.2); 
                        font-weight: 600;'>{selected_job['company']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Create columns for job details
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown(f"""<div style="background: {COLORS["gradient3"]}; color: white; 
                        padding: 16px; border-radius: 12px; text-align: center; box-shadow: 0 4px 15px rgba(79, 172, 254, 0.3);">
                        <p style="margin: 0; font-weight: 700; text-shadow: 0 2px 4px rgba(0,0,0,0.2); font-size: 0.9rem; 
                        text-transform: uppercase; letter-spacing: 1px;">📍 Location</p>
                        <p style="margin: 8px 0 0 0; text-shadow: 0 2px 4px rgba(0,0,0,0.2); font-weight: 600; font-size: 1.1rem;">{selected_job.get('location', 'Not specified')}</p>
                        </div>""", unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown(f"""<div style="background: {COLORS["gradient1"]}; color: white; 
                        padding: 16px; border-radius: 12px; text-align: center; box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);">
                        <p style="margin: 0; font-weight: 700; text-shadow: 0 2px 4px rgba(0,0,0,0.2); font-size: 0.9rem; 
                        text-transform: uppercase; letter-spacing: 1px;">🌐 Platform</p>
                        <p style="margin: 8px 0 0 0; text-shadow: 0 2px 4px rgba(0,0,0,0.2); font-weight: 600; font-size: 1.1rem;">{selected_job.get('platform', 'Unknown')}</p>
                        </div>""", unsafe_allow_html=True)
                    
                    with col3:
                        st.markdown(f"""<div style="background: {COLORS["gradient4"]}; color: white; 
                        padding: 16px; border-radius: 12px; text-align: center; box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);">
                        <p style="margin: 0; font-weight: 700; text-shadow: 0 2px 4px rgba(0,0,0,0.2); font-size: 0.9rem; 
                        text-transform: uppercase; letter-spacing: 1px;">📅 Posted</p>
                        <p style="margin: 8px 0 0 0; text-shadow: 0 2px 4px rgba(0,0,0,0.2); font-weight: 600; font-size: 1.1rem;">{selected_job.get('date_posted', 'Recent')}</p>
                        </div>""", unsafe_allow_html=True)
                    
                    # Job type if available
                    if selected_job.get('job_type'):
                        st.markdown(f"""<div style="background: {COLORS["gradient5"]}; color: white; 
                        padding: 10px 20px; border-radius: 25px; display: inline-block; margin: 15px 0; 
                        box-shadow: 0 4px 12px rgba(250, 112, 154, 0.3); font-weight: 600;">
                        <span style="text-shadow: 0 2px 4px rgba(0,0,0,0.2);">{selected_job.get('job_type')}</span></div>""", unsafe_allow_html=True)
                    
                    # Apply button with beautiful gradient
                    if selected_job.get('apply_url'):
                        apply_url = selected_job['apply_url']
                        is_real_job = selected_job.get('is_real_job', False)
                        
                        st.markdown(f"""
                        <div style="background: {COLORS["gradient2"]}; padding: 18px; 
                        border-radius: 12px; margin: 20px 0; text-align: center; box-shadow: 0 6px 20px rgba(239, 68, 68, 0.4);">
                        <a href="{apply_url}" target="_blank" style="color: white; 
                        text-decoration: none; font-weight: 700; display: block; text-shadow: 0 2px 4px rgba(0,0,0,0.3); 
                        font-size: 1.2rem;">
                        {'🚀 Apply Now' if is_real_job else '👁️ View Job Details'}</a>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if is_real_job:
                            st.success("This is a real job listing from a job search platform.")
                        else:
                            st.warning("This is a generated job listing for demonstration purposes.")
                    
                    # Job description
                    if selected_job.get('description'):
                        st.subheader("Job Description")
                        st.markdown(format_job_description(selected_job['description']), unsafe_allow_html=True)
                    else:
                        st.warning("No job description available.")
                    
                    # Job match analysis if resume is available
                    if st.session_state.resume_data:
                        with st.expander("Resume Match Analysis", expanded=True):
                            with st.spinner("Analyzing match between your resume and job..."):
                                # Display skills match
                                skills = st.session_state.resume_data.get("skills", [])
                                job_description = selected_job.get('description', '')
                                
                                if skills and job_description:
                                    display_matching_skills(skills, job_description)
                                    
                                    # Get detailed match analysis
                                    job_search_agent = resources["job_search_agent"]
                                    match_analysis = job_search_agent.get_job_match_analysis(
                                        st.session_state.resume_data,
                                        selected_job
                                    )
                                    
                                    # Display match score
                                    match_score = match_analysis.get("match_score", 0)
                                    st.markdown(f"""
                                    <div style="text-align: center; margin: 20px 0;">
                                        <div style="background-color: {COLORS["primary"]}; display: inline-block; padding: 10px 20px; 
                                        border-radius: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.2);">
                                            <span style="color: white; font-size: 1.5rem; font-weight: bold; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">
                                            Match Score: {match_score}%</span>
                                        </div>
                                    </div>
                                    """, unsafe_allow_html=True)
                                    
                                    # Display key matches
                                    key_matches = match_analysis.get("key_matches", [])
                                    if key_matches:
                                        st.markdown("#### Key Matches")
                                        matches_html = """<div style="display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 15px;">"""
                                        
                                        for match in key_matches:
                                            matches_html += f"""<div style="background-color: {COLORS["success"]}; color: white; 
                                            padding: 8px 12px; border-radius: 20px; font-weight: 500; margin-bottom: 8px;">
                                            ✅ {match}</div>"""
                                        
                                        matches_html += "</div>"
                                        st.markdown(matches_html, unsafe_allow_html=True)
                                    
                                    # Display gaps
                                    gaps = match_analysis.get("gaps", [])
                                    if gaps:
                                        st.markdown("#### Gaps to Address")
                                        gaps_html = """<div style="display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 15px;">"""
                                        
                                        for gap in gaps:
                                            gaps_html += f"""<div style="background-color: {COLORS["error"]}; color: white; 
                                            padding: 8px 12px; border-radius: 20px; font-weight: 500; margin-bottom: 8px;">
                                            ⚠️ {gap}</div>"""
                                        
                                        gaps_html += "</div>"
                                        st.markdown(gaps_html, unsafe_allow_html=True)
                                    
                                    # Display recommendations
                                    recommendations = match_analysis.get("recommendations", [])
                                    if recommendations:
                                        st.markdown("#### Recommendations")
                                        for rec in recommendations:
                                            st.markdown(f"- {rec}")
                                else:
                                    st.info("Upload your resume in the Resume Analysis tab to see how well you match this job.")
                    
                    # Job actions (save, prepare for interview)
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Check if this job is already saved
                        job_title = selected_job.get('title', '')
                        job_company = selected_job.get('company', '')
                        
                        is_saved = any(
                            saved_job.get('title') == job_title and saved_job.get('company') == job_company
                            for saved_job in st.session_state.saved_jobs
                        )
                        
                        if is_saved:
                            if st.button("Remove from Saved Jobs", key="remove_job_btn"):
                                # Remove job from saved jobs
                                if remove_saved_job(job_title, job_company):
                                    # Reload saved jobs
                                    st.session_state.saved_jobs = load_saved_jobs()
                                    st.success(f"Job {job_title} at {job_company} removed from saved jobs.")
                                    st.rerun()
                                else:
                                    st.error("Failed to remove job from saved jobs.")
                        else:
                            if st.button("Save Job", key="save_job_btn"):
                                # Save job to local storage
                                saved_path = save_job_to_local(selected_job)
                                st.session_state.saved_jobs = load_saved_jobs()
                                st.success(f"Job saved successfully")
                                st.rerun()
                    
                    with col2:
                        if st.button("Prepare for Interview", key="prepare_interview_btn"):
                            st.session_state.active_tab = 2  # Store which tab to activate
                            st.rerun()

# Tab 3: Interview Preparation
with tabs[2]:
    st.markdown("<div style='margin-bottom: 2rem;'></div>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='color: {COLORS['text_dark']}; margin-bottom: 0.5rem;'>Interview Preparation</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: {COLORS['text_medium']}; margin-bottom: 2rem; font-size: 1.1rem;'>Prepare for interviews with personalized questions and answers</p>", unsafe_allow_html=True)
    
    # Check if coming from another tab
    if hasattr(st.session_state, 'active_tab') and st.session_state.active_tab == 2:
        delattr(st.session_state, 'active_tab')  # Clear the flag
    
    # Check if we have a selected job
    if st.session_state.selected_job:
        selected_job = st.session_state.selected_job
        
        # Job details display with beautiful gradient
        st.markdown(f"""
        <div style='background: {COLORS["gradient1"]}; 
        padding: 1.5rem; border-radius: 16px; margin-bottom: 1.5rem; box-shadow: 0 8px 25px rgba(99, 102, 241, 0.3);'>
            <h3 style='color: white; margin: 0; font-weight: 700; text-shadow: 0 2px 4px rgba(0,0,0,0.3); 
            font-size: 1.8rem;'>🎯 Prepare for: {selected_job['title']}</h3>
            <p style='color: white; font-size: 1.3rem; margin: 0.8rem 0 0 0; text-shadow: 0 2px 4px rgba(0,0,0,0.2); 
            font-weight: 600;'>{selected_job['company']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Create columns
        col1, col2 = st.columns(2)
        
        with col1:
            # Enhanced interview preparation options
            st.subheader("Preparation Type")
            interview_type = st.radio(
                "Select interview preparation type:",
                ["Technical Interview", "Behavioral Interview", "Coding Interview", "System Design", "Project Experience"],
                key="interview_type"
            )
            
            # Difficulty level
            difficulty = st.select_slider(
                "Interview difficulty:",
                options=["Entry Level", "Intermediate", "Advanced", "Expert"],
                value="Intermediate",
                key="interview_difficulty"
            )
            
            # Add specific focus areas based on selected interview type
            if interview_type == "Technical Interview":
                focus_areas = st.multiselect(
                    "Select focus areas:",
                    ["Algorithms", "Data Structures", "System Architecture", "Database", "Web Technologies", "DevOps", "Cloud"],
                    default=["Algorithms", "Data Structures"],
                    key="tech_focus_areas"
                )
            elif interview_type == "Coding Interview":
                focus_areas = st.multiselect(
                    "Select coding challenges:",
                    ["Array Problems", "String Manipulation", "Dynamic Programming", "Graph Algorithms", "Sorting", "Searching", "Object-Oriented Design"],
                    default=["Array Problems", "String Manipulation"],
                    key="coding_focus_areas"
                )
            elif interview_type == "Behavioral Interview":
                focus_areas = st.multiselect(
                    "Select behavioral aspects:",
                    ["Leadership", "Teamwork", "Conflict Resolution", "Problem Solving", "Time Management", "Adaptability", "Communication"],
                    default=["Leadership", "Teamwork"],
                    key="behavioral_focus_areas"
                )
            elif interview_type == "System Design":
                focus_areas = st.multiselect(
                    "Select design challenges:",
                    ["Scalability", "Database Design", "API Design", "Microservices", "Security", "Caching", "Load Balancing"],
                    default=["Scalability", "Database Design"],
                    key="design_focus_areas"
                )
            else:  # Project Experience
                focus_areas = st.multiselect(
                    "Select project aspects:",
                    ["Technical Challenges", "Project Management", "Teamwork", "Problem Solving", "Innovation", "Results", "Lessons Learned"],
                    default=["Technical Challenges", "Results"],
                    key="project_focus_areas"
                )
            
            # Number of questions
            num_questions = st.slider(
                "Number of questions:",
                5, 20, 10,
                key="num_interview_questions"
            )
            
            # Generate button
            generate_btn = st.button("Generate Interview Questions", key="generate_interview_btn")
        
        with col2:
            # Resume analysis tips
            if st.session_state.resume_data:
                st.subheader("Your Top Skills")
                
                # Get skills and experience
                skills = st.session_state.resume_data.get("skills", [])
                
                # Display skills that match the job
                if skills and selected_job.get("description"):
                    display_matching_skills(skills, selected_job["description"])
            else:
                st.warning("Upload your resume in the Resume Analysis tab for personalized interview tips.")
            
            # Interview tips based on job type and selected interview type
            st.subheader("Quick Tips")
            
            # Determine if this is a technical role
            is_technical = any(tech in selected_job['title'].lower() for tech in [
                'developer', 'engineer', 'data', 'software', 'programmer',
                'analyst', 'architect', 'devops', 'security', 'network'
            ])
            
            # Display tips based on the selected interview type
            if interview_type == "Technical Interview":
                st.markdown(f"""
                <div style="background-color: {COLORS["primary"]}; color: white; padding: 15px; 
                border-radius: 8px; margin-bottom: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                <h4 style="margin-top: 0; font-weight: 600; margin-bottom: 10px; color: white; text-shadow: 1px 1px 3px rgba(0,0,0,0.2);">Technical Interview Tips:</h4>
                <ul style="margin-bottom: 0; padding-left: 20px;">
                <li>Review fundamental concepts related to your role</li>
                <li>Research the tech stack mentioned in the job description</li>
                <li>Be prepared to discuss your previous technical challenges</li>
                <li>Practice explaining complex technical concepts simply</li>
                <li>Connect technical answers to business value</li>
                </ul>
                </div>
                """, unsafe_allow_html=True)
            elif interview_type == "Coding Interview":
                st.markdown(f"""
                <div style="background-color: {COLORS["primary"]}; color: white; padding: 15px; 
                border-radius: 8px; margin-bottom: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                <h4 style="margin-top: 0; font-weight: 600; margin-bottom: 10px; color: white; text-shadow: 1px 1px 3px rgba(0,0,0,0.2);">Coding Interview Tips:</h4>
                <ul style="margin-bottom: 0; padding-left: 20px;">
                <li>Review core data structures and algorithms</li>
                <li>Practice coding on a whiteboard or without IDE assistance</li>
                <li>Talk through your approach before coding</li>
                <li>Explain your thought process while solving the problem</li>
                <li>Test your code with examples and edge cases</li>
                <li>Consider time and space complexity</li>
                </ul>
                </div>
                """, unsafe_allow_html=True)
            elif interview_type == "Behavioral Interview":
                st.markdown(f"""
                <div style="background-color: {COLORS["primary"]}; color: white; padding: 15px; 
                border-radius: 8px; margin-bottom: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                <h4 style="margin-top: 0; font-weight: 600; margin-bottom: 10px; color: white; text-shadow: 1px 1px 3px rgba(0,0,0,0.2);">Behavioral Interview Tips:</h4>
                <ul style="margin-bottom: 0; padding-left: 20px;">
                <li>Use the STAR method (Situation, Task, Action, Result)</li>
                <li>Prepare specific examples from your experience</li>
                <li>Align your answers with the company's values</li>
                <li>Include quantifiable results whenever possible</li>
                <li>Be honest and authentic in your responses</li>
                </ul>
                </div>
                """, unsafe_allow_html=True)
            elif interview_type == "System Design":
                st.markdown(f"""
                <div style="background-color: {COLORS["primary"]}; color: white; padding: 15px; 
                border-radius: 8px; margin-bottom: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                <h4 style="margin-top: 0; font-weight: 600; margin-bottom: 10px; color: white; text-shadow: 1px 1px 3px rgba(0,0,0,0.2);">System Design Tips:</h4>
                <ul style="margin-bottom: 0; padding-left: 20px;">
                <li>Clarify requirements and constraints first</li>
                <li>Draw system diagrams to visualize your solution</li>
                <li>Start with a high-level design, then dive deeper</li>
                <li>Consider scalability, reliability, and performance</li>
                <li>Discuss tradeoffs in your design decisions</li>
                <li>Know common design patterns and when to apply them</li>
                </ul>
                </div>
                """, unsafe_allow_html=True)
            else:  # Project Experience
                st.markdown(f"""
                <div style="background-color: {COLORS["primary"]}; color: white; padding: 15px; 
                border-radius: 8px; margin-bottom: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                <h4 style="margin-top: 0; font-weight: 600; margin-bottom: 10px; color: white; text-shadow: 1px 1px 3px rgba(0,0,0,0.2);">Project Experience Tips:</h4>
                <ul style="margin-bottom: 0; padding-left: 20px;">
                <li>Highlight your specific contributions to projects</li>
                <li>Explain the challenges and how you overcame them</li>
                <li>Discuss both technical and non-technical aspects</li>
                <li>Share metrics or KPIs that demonstrate success</li>
                <li>Reflect on lessons learned and growth opportunities</li>
                </ul>
                </div>
                """, unsafe_allow_html=True)
        
        # Generate interview questions
        if generate_btn:
            with st.spinner("Generating interview questions..."):
                try:
                    interview_agent = resources["interview_agent"]
                    
                    # Get the job description
                    job_description = selected_job.get('description', '')
                    
                    # Get resume data if available
                    resume_data = st.session_state.resume_data
                    
                    # Create a more detailed prompt based on the interview type and focus areas
                    prompt_additions = f"Interview Type: {interview_type}\nDifficulty Level: {difficulty}\n"
                    if 'focus_areas' in locals():
                        prompt_additions += f"Focus Areas: {', '.join(focus_areas)}\n"
                    
                    # Create an enhanced job data object with our customizations
                    enhanced_job_data = selected_job.copy()
                    enhanced_job_data['interview_customization'] = prompt_additions
                    
                    # Generate questions based on job description and resume
                    questions = interview_agent.generate_interview_questions(
                        job_data=enhanced_job_data,
                        resume_data=resume_data,
                        question_count=num_questions
                    )
                    
                    # Store in session state
                    st.session_state.interview_questions = {
                        'job': selected_job,
                        'type': interview_type,
                        'difficulty': difficulty,
                        'focus_areas': focus_areas if 'focus_areas' in locals() else [],
                        'questions': questions
                    }
                    
                    # Rerun to refresh the page
                    st.rerun()
                except Exception as e:
                    st.error(f"Error generating interview questions: {str(e)}")
                    st.info("Try with a different interview type or reduce the number of questions.")
                    
        # Display generated questions with enhanced formatting
        if st.session_state.interview_questions:
            interview_data = st.session_state.interview_questions
            
            if interview_data['job']['title'] == selected_job['title'] and interview_data['job']['company'] == selected_job['company']:
                st.markdown(f"""
                <div style="background-color: {COLORS["secondary"]}; color: white; 
                padding: 10px 15px; border-radius: 8px; margin: 20px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.15);">
                <h3 style="margin: 0; font-weight: 600; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">{interview_data['type']} Questions ({interview_data['difficulty']})</h3>
                </div>
                """, unsafe_allow_html=True)
                
                # Create a 'Save Questions' button at the top
                save_questions = st.button("💾 Save Interview Questions", key="save_interview_questions")
                if save_questions:
                    # Save the interview questions to a file
                    import json
                    questions_data = {
                        "job_title": selected_job['title'],
                        "company": selected_job['company'],
                        "interview_type": interview_data['type'],
                        "difficulty": interview_data['difficulty'],
                        "questions": interview_data['questions'],
                        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    
                    # Create interviews directory if it doesn't exist
                    os.makedirs("saved_interviews", exist_ok=True)
                    
                    # Generate a filename
                    filename = f"interview_{selected_job['title'].replace(' ', '_')}_{selected_job['company'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
                    filepath = os.path.join("saved_interviews", filename)
                    
                    # Save to file
                    with open(filepath, 'w', encoding='utf-8') as f:
                        json.dump(questions_data, f, indent=4)
                    
                    st.success(f"Interview questions saved to {filepath}")
                
                # Create an expander for each question with space for notes
                for i, question in enumerate(interview_data['questions'], 1):
                    # Check if question is a string or dictionary
                    if isinstance(question, str):
                        # If it's a string, create a title and format the question
                        question_title = f"Question {i}"
                        question_text = question
                        
                        # Extract question title if it has a clear format (e.g. "Title: Content")
                        if ": " in question and question.index(": ") < 50:
                            parts = question.split(": ", 1)
                            question_title = f"Question {i}: {parts[0]}"
                            question_text = parts[1]
                        
                        with st.expander(question_title, expanded=i==1):
                            st.markdown(f"""<div style="background: {COLORS["gradient_light1"]}; color: {COLORS["text_dark"]}; 
                            padding: 20px; border-radius: 12px; margin-bottom: 15px; border-left: 4px solid {COLORS["primary"]}; 
                            box-shadow: 0 2px 8px {COLORS["shadow"]}; line-height: 1.7;">
                            <span style="font-weight: 500;">{question_text}</span>
                            </div>""", unsafe_allow_html=True)
                            
                            # Add note-taking area
                            note_key = f"note_{i}"
                            if note_key not in st.session_state:
                                st.session_state[note_key] = ""
                            
                            st.text_area("Your Notes:", key=note_key, height=100)
                    else:
                        # If it's a dictionary, use the structured approach
                        question_title = f"Question {i}: {question.get('question', 'Question Details')}"
                        # Shorten the title if it's too long
                        if len(question_title) > 80:
                            question_title = question_title[:77] + "..."
                            
                        with st.expander(question_title, expanded=i==1):
                            # Display full question text if it was truncated in the title
                            if len(question.get('question', '')) > 77 and "..." in question_title:
                                st.markdown(f"""<div style="background: {COLORS["gradient_light1"]}; color: {COLORS["text_dark"]}; 
                                padding: 20px; border-radius: 12px; margin-bottom: 15px; border-left: 4px solid {COLORS["primary"]}; 
                                box-shadow: 0 2px 8px {COLORS["shadow"]}; line-height: 1.7;">
                                <span style="font-weight: 500;">{question.get('question')}</span>
                                </div>""", unsafe_allow_html=True)
                            
                            # Display context if available
                            if question.get('context'):
                                st.markdown(f"""<h4 style="color: {COLORS["text_dark"]};">Question Context</h4>""", unsafe_allow_html=True)
                                st.markdown(f"""<div style="background: {COLORS["card_bg"]}; color: {COLORS["text_dark"]}; 
                                padding: 16px; border-radius: 12px; margin-bottom: 15px; border-left: 4px solid {COLORS["secondary"]}; 
                                box-shadow: 0 2px 8px {COLORS["shadow"]}; line-height: 1.7;">
                                <span style="font-weight: 400;">{question['context']}</span>
                                </div>""", unsafe_allow_html=True)
                            
                            # Display suggested approach if available
                            if question.get('approach') or question.get('suggested_approach'):
                                approach = question.get('approach', question.get('suggested_approach', ''))
                                st.markdown(f"""<h4 style="color: {COLORS["text_dark"]};">Suggested Approach</h4>""", unsafe_allow_html=True)
                                st.markdown(f"""<div style="background: {COLORS["gradient_light2"]}; color: {COLORS["text_dark"]}; 
                                padding: 18px; border-radius: 12px; margin-bottom: 15px; border-left: 4px solid {COLORS["tertiary"]}; 
                                box-shadow: 0 2px 8px {COLORS["shadow"]}; line-height: 1.7;">
                                <span style="font-weight: 400;">{approach}</span>
                                </div>""", unsafe_allow_html=True)
                            
                            # Display suggested answer if available
                            if question.get('suggested_answer') or question.get('answer'):
                                answer = question.get('suggested_answer', question.get('answer', ''))
                                st.markdown(f"""<h4 style="color: {COLORS["text_dark"]};">Suggested Answer</h4>""", unsafe_allow_html=True)
                                st.markdown(f"""<div style="background: {COLORS["gradient_light3"]}; color: {COLORS["text_dark"]}; 
                                padding: 18px; border-radius: 12px; margin-bottom: 15px; border-left: 4px solid {COLORS["primary"]}; 
                                box-shadow: 0 2px 8px {COLORS["shadow"]}; line-height: 1.7;">
                                <span style="font-weight: 400;">{answer}</span>
                                </div>""", unsafe_allow_html=True)
                            
                            # Display tips if available
                            if question.get('tips'):
                                st.markdown(f"""<h4 style="color: {COLORS["text_dark"]};">Interview Tips</h4>""", unsafe_allow_html=True)
                                st.markdown(f"""<div style="background: {COLORS["gradient_light4"]}; color: {COLORS["text_dark"]}; 
                                padding: 18px; border-radius: 12px; margin-bottom: 15px; border-left: 4px solid {COLORS["quaternary"]}; 
                                box-shadow: 0 2px 8px {COLORS["shadow"]}; line-height: 1.7;">
                                <span style="font-weight: 400;">{question['tips']}</span>
                                </div>""", unsafe_allow_html=True)
                            
                            # Display code solution for coding questions if available
                            if question.get('code_solution'):
                                st.markdown("<h4>Code Solution</h4>", unsafe_allow_html=True)
                                st.code(question['code_solution'], language="python")
                            
                            # Add note-taking area
                            note_key = f"note_{i}"
                            if note_key not in st.session_state:
                                st.session_state[note_key] = ""
                            
                            st.text_area("Your Notes:", key=note_key, height=100)
    else:
        # No job selected
        st.info("Please select a job from the Job Search or Saved Jobs tab to prepare for an interview.")
        
        # Display generic interview preparation
        st.subheader("Generic Interview Preparation")
        
        # Common interview question types with expanded options
        interview_categories = [
            "Common Behavioral Questions",
            "Technical Interview Questions",
            "Programming & Coding Questions",
            "System Design Questions",
            "Problem-Solving Questions",
            "Cultural Fit Questions",
            "Leadership & Management Questions"
        ]
        
        selected_category = st.selectbox("Select question category:", interview_categories)
        
        # Add difficulty selection for generic questions
        generic_difficulty = st.select_slider(
            "Difficulty level:",
            options=["Entry Level", "Intermediate", "Advanced", "Expert"],
            value="Intermediate",
            key="generic_difficulty"
        )
        
        # Add focus areas based on selected category
        if "Technical" in selected_category:
            generic_focus = st.multiselect(
                "Select technical focus areas:",
                ["Web Development", "Mobile Development", "Cloud Computing", "DevOps", "Data Science", "Machine Learning", "Databases", "Security"],
                default=["Web Development"],
                key="generic_tech_focus"
            )
        elif "Programming" in selected_category or "Coding" in selected_category:
            generic_focus = st.multiselect(
                "Select programming focus areas:",
                ["Algorithms", "Data Structures", "Object-Oriented Design", "Functional Programming", "Front-end", "Back-end", "API Design"],
                default=["Algorithms", "Data Structures"],
                key="generic_coding_focus"
            )
        elif "System Design" in selected_category:
            generic_focus = st.multiselect(
                "Select system design areas:",
                ["Scalability", "High Availability", "Microservices", "APIs", "Databases", "Caching", "Load Balancing"],
                default=["Scalability", "APIs"],
                key="generic_design_focus"
            )
        
        # Number of questions
        generic_count = st.slider(
            "Number of questions:",
            5, 15, 8,
            key="generic_question_count"
        )
        
        # Generate generic questions button
        if st.button("Generate Generic Questions", key="generic_questions_btn"):
            with st.spinner("Generating generic interview questions..."):
                try:
                    interview_agent = resources["interview_agent"]
                    
                    # Generate questions based on selected category
                    generic_job = {
                        "title": "Generic Interview",
                        "company": "Various Companies",
                        "description": f"Prepare for {selected_category}",
                        "interview_customization": f"Difficulty Level: {generic_difficulty}\nFocus Areas: {', '.join(generic_focus) if 'generic_focus' in locals() else 'General'}"
                    }
                    
                    questions = interview_agent.generate_interview_questions(
                        job_data=generic_job,
                        question_count=generic_count
                    )
                    
                    # Store in session state
                    st.session_state.interview_questions = {
                        'job': {'title': 'Generic', 'company': 'Various'},
                        'type': selected_category,
                        'difficulty': generic_difficulty,
                        'questions': questions
                    }
                    
                    # Refresh the page
                    st.rerun()
                except Exception as e:
                    st.error(f"Error generating interview questions: {str(e)}")
        
        # Display generated generic questions
        if st.session_state.interview_questions and st.session_state.interview_questions['job']['title'] == 'Generic':
            interview_data = st.session_state.interview_questions
            
            st.markdown(f"""
            <div style="background-color: {COLORS["secondary"]}; color: white; 
            padding: 10px 15px; border-radius: 8px; margin: 20px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.15);">
            <h3 style="margin: 0; font-weight: 600; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">{interview_data['type']}</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Save generic questions button
            save_generic = st.button("💾 Save Generic Questions", key="save_generic_questions")
            if save_generic:
                # Save the interview questions to a file
                import json
                questions_data = {
                    "interview_type": interview_data['type'],
                    "difficulty": interview_data['difficulty'],
                    "questions": interview_data['questions'],
                    "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                # Create interviews directory if it doesn't exist
                os.makedirs("saved_interviews", exist_ok=True)
                
                # Generate a filename
                filename = f"generic_{interview_data['type'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
                filepath = os.path.join("saved_interviews", filename)
                
                # Save to file
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(questions_data, f, indent=4)
                
                st.success(f"Interview questions saved to {filepath}")
            
            # Create an expander for each question with space for notes
            for i, question in enumerate(interview_data['questions'], 1):
                if isinstance(question, str):
                    # If it's a string, display it directly
                    with st.expander(f"Question {i}", expanded=i==1):
                        st.markdown(f"""<div style="background: {COLORS["gradient_light1"]}; color: {COLORS["text_dark"]}; 
                        padding: 20px; border-radius: 12px; margin-bottom: 15px; border-left: 4px solid {COLORS["primary"]}; 
                        box-shadow: 0 2px 8px {COLORS["shadow"]}; line-height: 1.7;">
                        <span style="font-weight: 500;">{question}</span>
                        </div>""", unsafe_allow_html=True)
                        
                        # Add note-taking area
                        note_key = f"generic_note_{i}"
                        if note_key not in st.session_state:
                            st.session_state[note_key] = ""
                        
                        st.text_area("Your Notes:", key=note_key, height=100)
                else:
                    # If it's a dictionary, use the structured approach
                    question_title = f"Question {i}: {question.get('question', 'Question Details')}"
                    # Shorten the title if it's too long
                    if len(question_title) > 80:
                        question_title = question_title[:77] + "..."
                        
                    with st.expander(question_title, expanded=i==1):
                        # Display full question text if it was truncated in the title
                        if len(question.get('question', '')) > 77 and "..." in question_title:
                            st.markdown(f"""<div style="background: {COLORS["gradient_light1"]}; color: {COLORS["text_dark"]}; 
                            padding: 20px; border-radius: 12px; margin-bottom: 15px; border-left: 4px solid {COLORS["primary"]}; 
                            box-shadow: 0 2px 8px {COLORS["shadow"]}; line-height: 1.7;">
                            <span style="font-weight: 500;">{question.get('question')}</span>
                            </div>""", unsafe_allow_html=True)
                        
                        # Display suggested answer if available
                        if question.get('suggested_answer'):
                            st.markdown(f"""<h4 style="color: {COLORS["text_dark"]};">Suggested Answer</h4>""", unsafe_allow_html=True)
                            st.markdown(f"""<div style="background: {COLORS["gradient_light3"]}; color: {COLORS["text_dark"]}; 
                            padding: 18px; border-radius: 12px; margin-bottom: 15px; border-left: 4px solid {COLORS["primary"]}; 
                            box-shadow: 0 2px 8px {COLORS["shadow"]}; line-height: 1.7;">
                            <span style="font-weight: 400;">{question['suggested_answer']}</span>
                            </div>""", 
                            unsafe_allow_html=True)
                        
                        # Display tips if available
                        if question.get('tips'):
                            st.markdown(f"""<h4 style="color: {COLORS["text_dark"]};">Tips</h4>""", unsafe_allow_html=True)
                            st.markdown(f"""<div style="background: {COLORS["gradient_light4"]}; color: {COLORS["text_dark"]}; 
                            padding: 18px; border-radius: 12px; margin-bottom: 15px; border-left: 4px solid {COLORS["quaternary"]}; 
                            box-shadow: 0 2px 8px {COLORS["shadow"]}; line-height: 1.7;">
                            <span style="font-weight: 400;">{question['tips']}</span>
                            </div>""", 
                            unsafe_allow_html=True)
                        
                        # Add note-taking area
                        note_key = f"generic_note_{i}"
                        if note_key not in st.session_state:
                            st.session_state[note_key] = ""
                        
                        st.text_area("Your Notes:", key=note_key, height=100)

# Tab 4: Saved Jobs
with tabs[3]:
    st.markdown("<div style='margin-bottom: 2rem;'></div>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='color: {COLORS['text_dark']}; margin-bottom: 0.5rem;'>Saved Jobs</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: {COLORS['text_medium']}; margin-bottom: 2rem; font-size: 1.1rem;'>View and manage your saved job listings</p>", unsafe_allow_html=True)
    
    # Refresh saved jobs list
    st.session_state.saved_jobs = load_saved_jobs()
    
    if not st.session_state.saved_jobs:
        st.info("You haven't saved any jobs yet. Use the Job Search tab to find and save jobs.")
    else:
        # Display count of saved jobs with beautiful gradient
        st.markdown(f"""
        <div style="background: {COLORS["gradient1"]}; color: white; 
        padding: 24px 28px; border-radius: 16px; margin-bottom: 25px; box-shadow: 0 4px 20px {COLORS["shadow_medium"]};">
        <h3 style="margin: 0; font-weight: 700; text-shadow: 0 2px 4px rgba(0,0,0,0.2); font-size: 1.6rem;">
        💼 You have {len(st.session_state.saved_jobs)} saved jobs</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Create a dataframe for saved jobs
        saved_jobs_df = pd.DataFrame([
            {
                "Title": job["title"],
                "Company": job["company"],
                "Location": job.get("location", "Not specified"),
                "Platform": job.get("platform", "Unknown"),
                "Date Saved": job.get("date_saved", "Recent")
            }
            for job in st.session_state.saved_jobs
        ])
        
        # Display saved jobs in a dataframe with improved styling
        st.dataframe(
            saved_jobs_df,
            use_container_width=True,
            column_config={
                "Title": st.column_config.TextColumn("Job Title"),
                "Date Saved": st.column_config.TextColumn("Saved On")
            },
            hide_index=True
        )
        
        # Allow selection of a saved job for detailed view
        if st.session_state.saved_jobs:
            st.markdown("### Job Details")
            selected_index = st.selectbox(
                "Select a job to view details:",
                range(len(st.session_state.saved_jobs)),
                format_func=lambda i: f"{st.session_state.saved_jobs[i]['title']} at {st.session_state.saved_jobs[i]['company']}",
                key="saved_job_selection"
            )
            
            if selected_index is not None:
                st.session_state.selected_job = st.session_state.saved_jobs[selected_index]
                selected_job = st.session_state.selected_job
                
                # Job title and company with beautiful gradient styling
                st.markdown(f"""
                <div style='background: {COLORS["gradient1"]}; 
                padding: 1.5rem; border-radius: 16px; margin-bottom: 1.5rem; box-shadow: 0 8px 25px rgba(99, 102, 241, 0.3);'>
                    <h3 style='color: white; margin: 0; font-weight: 700; text-shadow: 0 2px 4px rgba(0,0,0,0.3); 
                    font-size: 1.8rem;'>{selected_job['title']}</h3>
                    <p style='color: white; font-size: 1.3rem; margin: 0.8rem 0 0 0; text-shadow: 0 2px 4px rgba(0,0,0,0.2); 
                    font-weight: 600;'>{selected_job['company']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Create columns for job details
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"""<div style="background: {COLORS["gradient3"]}; color: white; 
                    padding: 16px; border-radius: 12px; text-align: center; box-shadow: 0 4px 15px rgba(79, 172, 254, 0.3);">
                    <p style="margin: 0; font-weight: 700; text-shadow: 0 2px 4px rgba(0,0,0,0.2); font-size: 0.9rem; 
                    text-transform: uppercase; letter-spacing: 1px;">📍 Location</p>
                    <p style="margin: 8px 0 0 0; text-shadow: 0 2px 4px rgba(0,0,0,0.2); font-weight: 600; font-size: 1.1rem;">{selected_job.get('location', 'Not specified')}</p>
                    </div>""", unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""<div style="background: {COLORS["gradient1"]}; color: white; 
                    padding: 16px; border-radius: 12px; text-align: center; box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);">
                    <p style="margin: 0; font-weight: 700; text-shadow: 0 2px 4px rgba(0,0,0,0.2); font-size: 0.9rem; 
                    text-transform: uppercase; letter-spacing: 1px;">🌐 Platform</p>
                    <p style="margin: 8px 0 0 0; text-shadow: 0 2px 4px rgba(0,0,0,0.2); font-weight: 600; font-size: 1.1rem;">{selected_job.get('platform', 'Unknown')}</p>
                    </div>""", unsafe_allow_html=True)
                
                with col3:
                    date_info = selected_job.get('date_saved', selected_job.get('date_posted', 'Recent'))
                    st.markdown(f"""<div style="background: {COLORS["gradient4"]}; color: white; 
                    padding: 16px; border-radius: 12px; text-align: center; box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);">
                    <p style="margin: 0; font-weight: 700; text-shadow: 0 2px 4px rgba(0,0,0,0.2); font-size: 0.9rem; 
                    text-transform: uppercase; letter-spacing: 1px;">📅 Date Saved</p>
                    <p style="margin: 8px 0 0 0; text-shadow: 0 2px 4px rgba(0,0,0,0.2); font-weight: 600; font-size: 1.1rem;">{date_info}</p>
                    </div>""", unsafe_allow_html=True)
                
                # Display job URL as a beautiful clickable link
                if selected_job.get('apply_url'):
                    st.markdown(f"""
                    <div style="background: {COLORS["gradient2"]}; padding: 18px; 
                    border-radius: 12px; margin: 20px 0; text-align: center; box-shadow: 0 6px 20px rgba(239, 68, 68, 0.4);">
                    <a href="{selected_job['apply_url']}" target="_blank" style="color: white; 
                    text-decoration: none; font-weight: 700; display: block; text-shadow: 0 2px 4px rgba(0,0,0,0.3); 
                    font-size: 1.2rem;">
                    🚀 Apply to this job</a>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Display job description with better formatting
                if selected_job.get('description'):
                    st.subheader("Job Description")
                    st.markdown(format_job_description(selected_job['description']), unsafe_allow_html=True)
                else:
                    st.warning("No job description available.")
                
                # Job actions
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("Remove from Saved Jobs", key="remove_saved_job_btn"):
                        # Remove job from saved jobs
                        job_title = selected_job.get('title', '')
                        job_company = selected_job.get('company', '')
                        
                        if remove_saved_job(job_title, job_company):
                            # Reload saved jobs
                            st.session_state.saved_jobs = load_saved_jobs()
                            st.success(f"Job {job_title} at {job_company} removed from saved jobs.")
                            st.rerun()
                        else:
                            st.error("Failed to remove job from saved jobs.")
                
                with col2:
                    if st.button("Prepare for Interview", key="saved_job_interview_btn"):
                        st.session_state.active_tab = 2  # Switch to Interview tab
                        st.rerun()

# Website-style footer
st.markdown("""
<div style='
    margin-top: 5rem;
    padding-top: 3rem;
    border-top: 1px solid #e5e7eb;
    background: #f8f9fa;
    padding: 3rem 2rem;
'>
    <div style='max-width: 1200px; margin: 0 auto; text-align: center;'>
        <p style='color: #6b7280; margin: 0.5rem 0; font-size: 0.95rem;'>
            <strong style='color: #1d1d1f;'>PLACEKO</strong> - AI-Powered Job Search Platform
        </p>
        <p style='color: #9ca3af; margin: 0.5rem 0; font-size: 0.875rem;'>
            Built with Streamlit | © """ + str(datetime.now().year) + """
        </p>
    </div>
</div>
""", unsafe_allow_html=True)
