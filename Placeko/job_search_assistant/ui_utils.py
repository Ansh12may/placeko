
import streamlit as st
from config import COLORS

def display_resume_analysis_summary(resume_data):
    """
    Display a summary of the resume analysis with improved visibility.
    
    Args:
        resume_data (dict): The parsed resume data dictionary
    """
    if not resume_data:
        st.warning("Resume data is not available. Please upload your resume.")
        return
    
    # Extract skills and experience
    skills = resume_data.get("skills", [])
    experience = resume_data.get("experience", [])
    
    # Define technical categories
    tech_categories = {
        "Programming": ["python", "java", "javascript", "c++", "ruby", "go"],
        "Data Science": ["ml", "ai", "machine learning", "data science", "scikit", "numpy", "pandas"],
        "Cloud & DevOps": ["aws", "azure", "gcp", "cloud", "ci/cd", "git", "docker"],
        "Databases": ["sql", "mysql", "postgresql", "mongodb", "nosql"],
        "Web & Mobile": ["react", "angular", "vue", "node", "android", "ios"],
        "Other": []
    }
    
    # Categorize skills
    categorized_skills = {cat: [] for cat in tech_categories}
    for skill in skills:
        skill_lower = skill.lower()
        found = False
        for category, keywords in tech_categories.items():
            if any(keyword in skill_lower for keyword in keywords):
                categorized_skills[category].append(skill)
                found = True
                break
        if not found:
            categorized_skills["Other"].append(skill)
    
    # Create summary
    st.subheader("Resume Analysis Summary")
    

    
    # Strengths and areas to improve
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""<h4 style="color: {COLORS['primary']}; margin-bottom: 15px; font-weight: 700;">✨ Strengths</h4>""", unsafe_allow_html=True)
        strengths = []
        # Identify strengths based on skills and experience
        if any(len(categorized_skills[cat]) > 0 for cat in ["Programming", "Data Science"]):
            strengths.append("Strong technical skills in programming and/or data science")
        if any("aws" in skill.lower() or "cloud" in skill.lower() for skill in skills):
            strengths.append("Cloud platform experience")
        if any("ml" in skill.lower() or "ai" in skill.lower() for skill in skills):
            strengths.append("Machine learning knowledge")
        
        # Display strengths with light, readable styling
        if strengths:
            for strength in strengths:
                st.markdown(
                    f"""<div style="background: {COLORS['gradient_light4']}; color: {COLORS['text_dark']}; padding: 16px; 
                    border-radius: 12px; margin-bottom: 12px; font-weight: 500; border-left: 4px solid {COLORS['success']}; 
                    box-shadow: 0 2px 8px {COLORS['shadow']};">
                    <span style="color: {COLORS['success']}; font-weight: 600; margin-right: 8px;">✅</span>{strength}</div>""", 
                    unsafe_allow_html=True
                )
        else:
            st.markdown(
                f"""<div style="background: {COLORS['card_bg']}; color: {COLORS['text_medium']}; padding: 16px; 
                border-radius: 12px; border: 2px solid {COLORS['border']}; box-shadow: 0 2px 8px {COLORS['shadow']};">
                Not enough information to determine strengths</div>""", 
                unsafe_allow_html=True
            )
    
    with col2:
        st.markdown(f"""<h4 style="color: {COLORS['warning']}; margin-bottom: 15px; font-weight: 700;">📈 Areas to Improve</h4>""", unsafe_allow_html=True)
        improvements = []
        # Identify improvement areas
        if not any("git" in skill.lower() for skill in skills):
            improvements.append("Version control experience (Git)")
        if not any(db in "".join(skills).lower() for db in ["sql", "database"]):
            improvements.append("Database knowledge")
        if not any(cloud in "".join(skills).lower() for cloud in ["aws", "azure", "gcp", "cloud"]):
            improvements.append("Cloud platform experience")
        
        # Display improvement areas with readable styling
        if improvements:
            for improvement in improvements:
                st.markdown(
                    f"""<div style="background: {COLORS['gradient_light2']}; color: {COLORS['text_dark']}; padding: 16px; 
                    border-radius: 12px; margin-bottom: 12px; font-weight: 500; border-left: 4px solid {COLORS['warning']}; 
                    box-shadow: 0 2px 8px {COLORS['shadow']};">
                    <span style="color: {COLORS['warning']}; font-weight: 600; margin-right: 8px;">⚠️</span>{improvement}</div>""", 
                    unsafe_allow_html=True
                )
        else:
            st.markdown(
                f"""<div style="background: {COLORS['gradient_light4']}; color: {COLORS['text_dark']}; padding: 16px; 
                border-radius: 12px; border-left: 4px solid {COLORS['success']}; box-shadow: 0 2px 8px {COLORS['shadow']};">
                No obvious improvement areas identified</div>""", 
                unsafe_allow_html=True
            )


def clean_and_organize_experience(experience_items):
    """Helper function to organize experience into categories."""
    categories = {
        "Programming Experience": [],
        "Machine Learning & AI": [],
        "Cloud Computing": [],
        "Data Analysis": [],
        "Companies & Roles": []
    }
    
    # Simple keyword-based categorization
    for item in experience_items:
        item_lower = item.lower()
        if any(kw in item_lower for kw in ["program", "develop", "code", "software"]):
            categories["Programming Experience"].append(item)
        elif any(kw in item_lower for kw in ["machine", "learning", "ai", "neural", "model"]):
            categories["Machine Learning & AI"].append(item)
        elif any(kw in item_lower for kw in ["cloud", "aws", "azure", "gcp"]):
            categories["Cloud Computing"].append(item)
        elif any(kw in item_lower for kw in ["data", "analytics", "analysis", "statistics"]):
            categories["Data Analysis"].append(item)
        else:
            categories["Companies & Roles"].append(item)
    
    return categories

def display_extracted_information(resume_data):
    """
    Display extracted resume information with better visibility.
    
    Args:
        resume_data (dict): The parsed resume data dictionary
    """
    if not resume_data:
        st.warning("Resume data is not available. Please upload your resume.")
        return
    
    st.subheader("Extracted Information")
    
    # Create columns for different information types
    info_col1, info_col2 = st.columns(2)
    
    with info_col1:
        # Display contact info with readable styling
        st.markdown(f"""<h4 style="color: {COLORS['text_dark']}; margin-bottom: 12px; font-weight: 700;">📞 Contact Information</h4>""", unsafe_allow_html=True)
        contact_info = resume_data.get("contact_info", {})
        contact_html = f"""<div style="background: {COLORS['card_bg']}; color: {COLORS['text_dark']}; padding: 20px; border-radius: 12px; margin-bottom: 18px; border: 1px solid {COLORS['border']}; box-shadow: 0 2px 12px {COLORS['shadow']};">"""
        
        if contact_info and (contact_info.get("email") or contact_info.get("phone")):
            if contact_info.get("email"):
                contact_html += f"<p style='margin: 10px 0; font-weight: 500; color: {COLORS['text_dark']};'><span style='color: {COLORS['primary']}; font-weight: 600; margin-right: 8px;'>📧 Email:</span> <span style='color: {COLORS['text_medium']};'>{contact_info['email']}</span></p>"
            if contact_info.get("phone"):
                contact_html += f"<p style='margin: 10px 0; font-weight: 500; color: {COLORS['text_dark']};'><span style='color: {COLORS['primary']}; font-weight: 600; margin-right: 8px;'>📱 Phone:</span> <span style='color: {COLORS['text_medium']};'>{contact_info['phone']}</span></p>"
        else:
            contact_html += f"<p style='margin: 0; color: {COLORS['text_medium']};'>No contact information detected.</p>"
        
        contact_html += "</div>"
        st.markdown(contact_html, unsafe_allow_html=True)
        
        # Display education with readable styling
        st.markdown(f"""<h4 style="color: {COLORS['text_dark']}; margin-bottom: 12px; font-weight: 700;">🎓 Education</h4>""", unsafe_allow_html=True)
        education = resume_data.get("education", [])
        education_html = f"""<div style="background: {COLORS['card_bg']}; color: {COLORS['text_dark']}; padding: 20px; border-radius: 12px; border: 1px solid {COLORS['border']}; box-shadow: 0 2px 12px {COLORS['shadow']};">"""
        
        if education:
            for edu in education:
                education_html += f"<p style='margin: 10px 0; font-weight: 500; color: {COLORS['text_dark']};'><span style='color: {COLORS['secondary']}; margin-right: 8px;'>🎓</span>{edu}</p>"
        else:
            education_html += f"<p style='margin: 0; color: {COLORS['text_medium']};'>No education information detected.</p>"
        
        education_html += "</div>"
        st.markdown(education_html, unsafe_allow_html=True)
    
    with info_col2:
        # Display skills with readable, colorful badges
        st.markdown(f"""<h4 style="color: {COLORS['text_dark']}; margin-bottom: 12px; font-weight: 700;">🛠️ Skills</h4>""", unsafe_allow_html=True)
        skills = resume_data.get("skills", [])
        
        if skills:
            # Create a flex container for horizontal layout
            skills_html = """<div style="display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 18px;">"""
            
            # Add each skill with colorful but readable backgrounds
            skill_colors = [
                f"background: {COLORS['primary']}; color: white;",
                f"background: {COLORS['secondary']}; color: white;",
                f"background: {COLORS['tertiary']}; color: white;",
                f"background: {COLORS['quaternary']}; color: white;",
                f"background: {COLORS['accent1']}; color: white;",
            ]
            for i, skill in enumerate(skills):
                color_style = skill_colors[i % len(skill_colors)]
                skills_html += f"""<div style="{color_style} 
                padding: 10px 18px; border-radius: 20px; font-weight: 500; margin-bottom: 8px; 
                box-shadow: 0 2px 8px {COLORS['shadow']}; font-size: 0.9rem; display: inline-block;">
                {skill}</div>"""
            
            skills_html += "</div>"
            st.markdown(skills_html, unsafe_allow_html=True)
        else:
            st.markdown(
                f"""<div style="background: {COLORS['card_bg']}; color: {COLORS['text_medium']}; padding: 18px; 
                border-radius: 12px; border: 1px solid {COLORS['border']}; box-shadow: 0 2px 8px {COLORS['shadow']};">
                No skills detected.</div>""", 
                unsafe_allow_html=True
            )
        
        # Display experience using the organized categories function
        st.markdown(f"""<h4 style="color: {COLORS['accent']}; margin-bottom: 12px; font-weight: 700;">💼 Experience</h4>""", unsafe_allow_html=True)
        experience = resume_data.get("experience", [])
        
        if experience:
            # Organize the experience items
            organized_exp = clean_and_organize_experience(experience)
            
            # Display each category in an accordion-like structure
            for category, items in organized_exp.items():
                if items:
                    # Set category-specific colors (readable)
                    if "Programming" in category:
                        bg_color = COLORS['primary']
                        bg_light = COLORS['gradient_light3']
                    elif "Machine Learning" in category or "AI" in category:
                        bg_color = COLORS['secondary']
                        bg_light = COLORS['gradient_light1']
                    elif "Cloud" in category:
                        bg_color = COLORS['quaternary']
                        bg_light = COLORS['gradient_light4']
                    elif "Data" in category:
                        bg_color = COLORS['tertiary']
                        bg_light = COLORS['gradient_light2']
                    elif "Companies" in category:
                        bg_color = COLORS['accent2']
                        bg_light = COLORS['gradient_light1']
                    else:
                        bg_color = COLORS['primary']
                        bg_light = COLORS['gradient_light3']
                    
                    # Create category header
                    st.markdown(
                        f"""<div style="background: {bg_color}; color: white; padding: 14px; 
                        border-radius: 12px 12px 0 0; font-weight: 600; margin-top: 12px; 
                        box-shadow: 0 2px 8px {COLORS['shadow']};">
                        {category} ({len(items)})</div>""", 
                        unsafe_allow_html=True
                    )
                    
                    # Create flex container for items with light background
                    items_html = f"""<div style="background: {bg_light}; color: {COLORS['text_dark']}; 
                    padding: 16px; border-radius: 0 0 12px 12px; margin-bottom: 12px; 
                    box-shadow: 0 2px 8px {COLORS['shadow']}; border: 1px solid {COLORS['border']};">
                    <div style="display: flex; flex-wrap: wrap; gap: 8px;">"""
                    
                    for item in items:
                        items_html += f"""<div style="background-color: {COLORS['card_bg']}; 
                        padding: 10px 16px; border-radius: 20px; margin-bottom: 6px; font-weight: 500; 
                        color: {COLORS['text_dark']}; border: 1px solid {COLORS['border_light']}; 
                        box-shadow: 0 1px 4px {COLORS['shadow']};">
                        {item}</div>"""
                    
                    items_html += "</div></div>"
                    st.markdown(items_html, unsafe_allow_html=True)
        else:
            st.markdown(
                f"""<div style="background: {COLORS['card_bg']}; color: {COLORS['text_medium']}; padding: 18px; 
                border-radius: 12px; border: 1px solid {COLORS['border']}; box-shadow: 0 2px 8px {COLORS['shadow']};">
                No experience information detected.</div>""", 
                unsafe_allow_html=True
            )

def display_formatted_analysis(analysis):
    """
    Format and display the resume analysis in a structured way with improved visibility.
    
    Args:
        analysis (str): The resume analysis text
    """
    if not analysis:
        return
    
    # Extract sections using typical patterns
    sections = {
        "Overall Assessment": "",
        "Content Improvements": "",
        "Skills": "",
        "Format Suggestions": "",
        "ATS Optimization": ""
    }
    
    current_section = None
    lines = analysis.split('\n')
    
    for line in lines:
        # Check if this line is a section header
        for section in sections.keys():
            if section.lower() in line.lower() or "strength" in line.lower() or "weakness" in line.lower():
                current_section = section
                break
        
        # Add content to the current section
        if current_section and line:
            sections[current_section] += line + "\n"
    
    # Display each section with readable light backgrounds
    section_styles = {
        "Overall Assessment": {"bg": COLORS['gradient_light1'], "border": COLORS['primary']},
        "Content Improvements": {"bg": COLORS['gradient_light2'], "border": COLORS['tertiary']},
        "Skills": {"bg": COLORS['gradient_light3'], "border": COLORS['accent1']},
        "Format Suggestions": {"bg": COLORS['gradient_light4'], "border": COLORS['quaternary']},
        "ATS Optimization": {"bg": COLORS['gradient_light1'], "border": COLORS['secondary']}
    }
    
    for section, content in sections.items():
        if content.strip():
            st.subheader(section)
            style = section_styles.get(section, {"bg": COLORS['card_bg'], "border": COLORS['primary']})
            st.markdown(
                f"""<div style='background: {style["bg"]}; color: {COLORS['text_dark']}; 
                padding: 24px; border-radius: 12px; margin-top: 15px; 
                font-size: 15px; line-height: 1.8; box-shadow: 0 2px 12px {COLORS['shadow']}; 
                font-weight: 400; border-left: 4px solid {style["border"]};'>{content}</div>""", 
                unsafe_allow_html=True
            )

def format_job_description(description):
    """
    Format the job description for better readability with high contrast.
    
    Args:
        description (str): Job description text
        
    Returns:
        str: Formatted HTML for the job description
    """
    if not description:
        return f"""<div style="background: {COLORS['card_bg']}; color: {COLORS['text_medium']}; padding: 24px; 
                border-radius: 12px; margin-top: 15px; border: 1px solid {COLORS['border']}; 
                box-shadow: 0 2px 12px {COLORS['shadow']};">No description available</div>"""
    
    # Clean up any problematic formatting
    description = description.replace('\n\n', '<br><br>').replace('\n', '<br>')
    
    # Wrap the description in a readable styled div
    formatted_description = f"""
    <div style="background: {COLORS['card_bg']}; color: {COLORS['text_dark']}; padding: 24px; 
    border-radius: 12px; margin-top: 15px; line-height: 1.8; font-size: 15px; 
    border: 1px solid {COLORS['border']}; box-shadow: 0 2px 12px {COLORS['shadow']};">
        {description}
    </div>
    """
    
    return formatted_description

def display_matching_skills(skills, job_description):
    """
    Display skills that match a job description with high-contrast styling.
    
    Args:
        skills (list): List of skills from resume
        job_description (str): Job description text
    """
    if not skills or not job_description:
        st.markdown(
            """<div style="background-color: #455A64; color: white; padding: 12px; 
            border-radius: 6px;">No matching skills could be determined.</div>""", 
            unsafe_allow_html=True
        )
        return
    
    job_desc = job_description.lower()
    
    matching_skills = []
    for skill in skills:
        if skill.lower() in job_desc:
            matching_skills.append(skill)
    
    if matching_skills:
        st.markdown(f"""<h4 style="color: {COLORS['text_dark']}; margin-bottom: 12px; font-weight: 700;">✅ Skills Matching Job Description</h4>""", unsafe_allow_html=True)
        skills_html = """<div style="display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 18px;">"""
        
        for skill in matching_skills[:5]:  # Show top 5 matching skills
            skills_html += f"""<div style="background: {COLORS['success']}; color: white; 
            padding: 10px 18px; border-radius: 25px; font-weight: 500; margin-bottom: 8px; 
            box-shadow: 0 2px 8px {COLORS['shadow']};">
            ✅ {skill}</div>"""
        
        skills_html += "</div>"
        st.markdown(skills_html, unsafe_allow_html=True)
    else:
        st.markdown(
            f"""<div style="background: {COLORS['card_bg']}; color: {COLORS['text_medium']}; padding: 16px; 
            border-radius: 12px; border: 1px solid {COLORS['border']}; box-shadow: 0 2px 8px {COLORS['shadow']};">
            No matching skills detected in the job description.</div>""", 
            unsafe_allow_html=True
        )
    
    # Identify missing skills
    missing_skills = []
    common_tech_skills = [
        "python", "java", "javascript", "sql", "aws", "azure", 
        "react", "node", "docker", "kubernetes", "machine learning",
        "data science", "agile", "scrum", "git", "ci/cd"
    ]
    
    for tech in common_tech_skills:
        if tech in job_desc and not any(tech.lower() in s.lower() for s in skills):
            missing_skills.append(tech)
    
    if missing_skills:
        st.markdown(f"""<h4 style="color: {COLORS['text_dark']}; margin-bottom: 12px; font-weight: 700;">⚠️ Skills to Emphasize or Develop</h4>""", unsafe_allow_html=True)
        missing_html = """<div style="display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 18px;">"""
        
        for skill in missing_skills[:5]:  # Show top 5 missing skills
            missing_html += f"""<div style="background: {COLORS['warning']}; color: white; 
            padding: 10px 18px; border-radius: 25px; font-weight: 500; margin-bottom: 8px; 
            box-shadow: 0 2px 8px {COLORS['shadow']};">
            ⚠️ {skill.title()}</div>"""
        
        missing_html += "</div>"
        st.markdown(missing_html, unsafe_allow_html=True)

def apply_styling():
    """Apply custom CSS styling to make it look like a modern website."""
    st.markdown(f"""
    <style>
        /* Hide Streamlit default elements */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}
        
        /* Global font styling - Modern website typography */
        * {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif !important;
        }}
        
        /* Website-like container with proper spacing */
        .main .block-container {{
            max-width: 1200px !important;
            padding: 2rem 3rem !important;
            padding-top: 1rem !important;
        }}
        
        /* Fix Streamlit's default spacing issues */
        .main > div {{
            padding-top: 0 !important;
        }}
        
        /* Ensure proper flow */
        div[data-testid="stVerticalBlock"] {{
            gap: 1.5rem !important;
        }}
        
        /* Fix for Streamlit columns */
        [data-testid="stHorizontalBlock"] {{
            gap: 1rem !important;
            margin-bottom: 1.5rem !important;
        }}
        
        /* Modern website header/navbar style */
        .stApp {{
            background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%) !important;
        }}
        
        /* Website-style headers with proper spacing */
        h1 {{
            color: {COLORS['text_dark']} !important;
            font-size: 2.5rem !important;
            font-weight: 700 !important;
            margin-top: 0 !important;
            margin-bottom: 1.5rem !important;
            line-height: 1.2 !important;
            padding: 0 !important;
        }}
        
        h2 {{
            color: {COLORS['text_dark']} !important;
            font-size: 2rem !important;
            font-weight: 600 !important;
            margin-top: 2rem !important;
            margin-bottom: 1rem !important;
            padding: 0 !important;
        }}
        
        h3 {{
            color: {COLORS['text_dark']} !important;
            font-size: 1.5rem !important;
            font-weight: 600 !important;
            margin-top: 1.5rem !important;
            margin-bottom: 1rem !important;
            padding: 0 !important;
        }}
        
        h4 {{
            color: {COLORS['text_dark']} !important;
            font-size: 1.25rem !important;
            font-weight: 600 !important;
            margin-top: 1.25rem !important;
            margin-bottom: 0.75rem !important;
            padding: 0 !important;
        }}
        
        /* Fix subheader spacing */
        [data-testid="stHeader"] {{
            margin-bottom: 1rem !important;
            padding: 0 !important;
        }}
        
        /* Fix subheader text */
        .stSubheader {{
            margin-top: 1.5rem !important;
            margin-bottom: 1rem !important;
            padding: 0 !important;
        }}
        
        /* Header panels with gradients */
        div[style*="background-color: {COLORS['primary']}"],
        div[style*="background: linear-gradient"],
        [data-testid="stForm"] h3,
        .blue-header {{
            color: white !important;
            font-size: 1.3rem !important;
            font-weight: 700 !important;
            text-shadow: 0 2px 4px rgba(0,0,0,0.2) !important;
            padding: 18px !important;
            border-radius: 12px !important;
            margin-bottom: 18px !important;
            background: {COLORS['gradient1']} !important;
            box-shadow: 0 4px 15px rgba(99, 102, 241, 0.25) !important;
        }}
        
        /* Fix for text in colored panels */
        div[style*="background-color: {COLORS['primary']}"] p,
        div[style*="background: linear-gradient"] p,
        div[style*="background-color: {COLORS['primary']}"] span,
        div[style*="background: linear-gradient"] span,
        div[style*="background-color: {COLORS['primary']}"] h3,
        div[style*="background: linear-gradient"] h3,
        div[style*="background-color: {COLORS['primary']}"] h4,
        div[style*="background: linear-gradient"] h4 {{
            color: white !important;
            font-weight: 600 !important;
        }}
        
        /* Form inputs - Modern styling */
        input, select, textarea, 
        [data-baseweb="input"], 
        [data-baseweb="select"], 
        [data-baseweb="textarea"] {{
            color: {COLORS['text_dark']} !important;
            background-color: white !important;
            border: 2px solid {COLORS['border']} !important;
            border-radius: 10px !important;
            padding: 10px 14px !important;
            transition: all 0.3s ease !important;
        }}
        
        input:focus, select:focus, textarea:focus {{
            border-color: {COLORS['primary']} !important;
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1) !important;
        }}
        
        /* Website-style buttons */
        .stButton>button,
        button[kind="primary"] {{
            background: {COLORS['primary']} !important;
            color: white !important;
            font-weight: 500 !important;
            border-radius: 8px !important;
            padding: 0.75rem 2rem !important;
            border: none !important;
            box-shadow: 0 2px 4px rgba(0, 122, 255, 0.2) !important;
            transition: all 0.2s ease !important;
            width: auto !important;
            font-size: 1rem !important;
            height: auto !important;
            min-height: 44px !important;
            text-transform: none !important;
            cursor: pointer !important;
        }}
        
        .stButton>button:hover,
        button[kind="primary"]:hover {{
            background: {COLORS['primary_dark']} !important;
            box-shadow: 0 4px 8px rgba(0, 122, 255, 0.3) !important;
            transform: translateY(-1px) !important;
        }}
        
        .stButton>button:active {{
            transform: translateY(0) !important;
        }}
        
        /* Website-style tables */
        table, .dataframe, [data-testid="stTable"] {{
            width: 100% !important;
            border-collapse: separate !important;
            border-spacing: 0 !important;
            margin-bottom: 2rem !important;
            border-radius: 8px !important;
            overflow: hidden !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
            background: white !important;
            border: 1px solid {COLORS['border']} !important;
        }}
        
        /* Table headers */
        th, thead tr th {{
            background: {COLORS['primary']} !important;
            color: white !important;
            font-weight: 600 !important;
            padding: 1rem !important;
            text-align: left !important;
            border: none !important;
            font-size: 0.875rem !important;
            letter-spacing: 0.3px !important;
        }}
        
        /* Table cells */
        td, tbody tr td {{
            padding: 1rem !important;
            border-bottom: 1px solid {COLORS['border_light']} !important;
            background-color: white !important;
            color: {COLORS['text_dark']} !important;
        }}
        
        /* Alternate row styling */
        tbody tr:nth-child(even) td {{
            background-color: #fafafa !important;
        }}
        
        tbody tr:hover td {{
            background-color: rgba(0, 122, 255, 0.05) !important;
            transition: background-color 0.15s ease !important;
        }}
        
        tbody tr:last-child td {{
            border-bottom: none !important;
        }}
        
        /* Website-style navigation tabs */
        div[data-baseweb="tab-list"] {{
            gap: 0 !important;
            background: transparent !important;
            padding: 0 !important;
            border-bottom: 2px solid {COLORS['border']} !important;
            display: flex !important;
            justify-content: flex-start !important;
            width: 100% !important;
            margin-bottom: 3rem !important;
            box-shadow: none !important;
        }}
        
        div[data-baseweb="tab-list"] button {{
            flex: none !important;
            text-align: center !important;
            margin: 0 !important;
            margin-right: 2rem !important;
            padding: 1rem 1.5rem !important;
            height: auto !important;
            font-size: 1rem !important;
            font-weight: 500 !important;
            background: transparent !important;
            color: {COLORS['text_medium']} !important;
            border-radius: 0 !important;
            border: none !important;
            border-bottom: 3px solid transparent !important;
            transition: all 0.2s ease !important;
            box-shadow: none !important;
        }}
        
        div[data-baseweb="tab-list"] button:hover {{
            background: transparent !important;
            color: {COLORS['primary']} !important;
            border-bottom-color: {COLORS['primary']} !important;
            transform: none !important;
        }}
        
        div[data-baseweb="tab-list"] button[aria-selected="true"] {{
            background: transparent !important;
            color: {COLORS['primary']} !important;
            border-bottom-color: {COLORS['primary']} !important;
            font-weight: 600 !important;
            box-shadow: none !important;
            transform: none !important;
        }}
        
        /* Website-style backgrounds */
        body {{
            background: #ffffff !important;
        }}
        
        .stApp {{
            background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%) !important;
        }}
        
        /* Fix overlapping issues - Remove problematic card styling */
        /* [data-testid="stVerticalBlock"] > div {{
            background: white !important;
            border-radius: 8px !important;
            padding: 1.5rem !important;
            margin-bottom: 1.5rem !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
            border: 1px solid {COLORS['border_light']} !important;
        }} */
        
        /* Ensure proper spacing between elements */
        .element-container {{
            margin-bottom: 1.5rem !important;
            padding: 0 !important;
        }}
        
        .stMarkdown {{
            margin-bottom: 1rem !important;
        }}
        
        /* Fix column spacing */
        [data-testid="column"] {{
            padding: 0 0.75rem !important;
        }}
        
        /* Ensure proper spacing for forms */
        [data-testid="stForm"] {{
            margin-bottom: 2rem !important;
        }}
        
        /* Fix spacing for file uploader */
        [data-testid="stFileUploader"] {{
            margin-bottom: 1.5rem !important;
        }}
        
        /* Make file uploader label text black and bold */
        [data-testid="stFileUploader"] + label,
        label[data-testid*="uploader"],
        div[data-testid="stFileUploader"] ~ label,
        .stFileUploader + label {{
            color: {COLORS['text_dark']} !important;
            font-weight: 700 !important;
            font-size: 1.1rem !important;
        }}
        
        /* Fix spacing for selectboxes and inputs */
        [data-baseweb="select"],
        [data-baseweb="input"],
        [data-baseweb="textarea"] {{
            margin-bottom: 1rem !important;
        }}
        
        /* Fix spacing for buttons */
        .stButton {{
            margin-bottom: 1rem !important;
        }}
        
        /* Fix spacing for columns */
        .stColumns {{
            margin-bottom: 2rem !important;
        }}
        
        /* Ensure no negative margins */
        * {{
            margin-top: 0 !important;
        }}
        
        /* Fix for Streamlit containers */
        .block-container {{
            padding-top: 1rem !important;
            padding-bottom: 2rem !important;
        }}
        
        /* Form inputs - Website style */
        [data-baseweb="input"] {{
            border-radius: 6px !important;
            border: 1px solid {COLORS['border']} !important;
        }}
        
        [data-baseweb="input"]:focus {{
            border-color: {COLORS['primary']} !important;
            box-shadow: 0 0 0 3px rgba(0, 122, 255, 0.1) !important;
        }}
        
        /* Select boxes */
        [data-baseweb="select"] {{
            border-radius: 6px !important;
        }}
        
        /* Headers inside panels */
        .stExpander h3, .stForm h3 {{
            color: {COLORS['primary']} !important;
            font-weight: 700 !important;
        }}
        
        /* Website-style expandable sections with proper spacing */
        .stExpander {{
            border: 1px solid {COLORS['border']} !important;
            border-radius: 8px !important;
            overflow: hidden !important;
            margin-top: 0 !important;
            margin-bottom: 1.5rem !important;
            margin-left: 0 !important;
            margin-right: 0 !important;
            background: white !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.08) !important;
            transition: all 0.2s ease !important;
            position: relative !important;
            z-index: 1 !important;
        }}
        
        .stExpander:hover {{
            box-shadow: 0 2px 8px rgba(0,0,0,0.12) !important;
            border-color: {COLORS['primary']} !important;
        }}
        
        .stExpander details {{
            padding: 0 !important;
            margin: 0 !important;
        }}
        
        .stExpander summary {{
            padding: 1.25rem 1.5rem !important;
            background: white !important;
            font-weight: 500 !important;
            color: {COLORS['text_dark']} !important;
            font-size: 1rem !important;
            cursor: pointer !important;
            margin: 0 !important;
        }}
        
        .stExpander summary:hover {{
            background: #f8f9fa !important;
        }}
        
        /* Fix content inside expanders */
        .stExpander > div {{
            padding: 1.5rem !important;
            margin: 0 !important;
        }}
        
        /* File uploader styling */
        [data-testid="stFileUploader"] {{
            border: 2px dashed {COLORS['primary']} !important;
            border-radius: 12px !important;
            padding: 20px !important;
            background: {COLORS['panel_bg']} !important;
        }}
        
        /* File uploader label - Make it black and visible - Comprehensive targeting */
        [data-testid="stFileUploader"] label,
        [data-testid="stFileUploader"] p,
        [data-testid="stFileUploader"] div,
        [data-testid="stFileUploader"] span,
        [data-testid="stFileUploader"] *,
        label[for*="resume"],
        label[for*="uploader"],
        .stFileUploader label,
        .stFileUploader > label,
        .stFileUploader > div > label,
        .stFileUploader > div > div > label,
        [data-testid="stFileUploader"] > div > label,
        [data-testid="stFileUploader"] > div > div > label,
        [data-testid="stFileUploader"] > div > div > div > label {{
            color: {COLORS['text_dark']} !important;
            font-weight: 700 !important;
            font-size: 1.1rem !important;
        }}
        
        /* Make all text in file uploader visible */
        [data-testid="stFileUploader"] *,
        [data-testid="stFileUploader"] p *,
        [data-testid="stFileUploader"] div *,
        [data-testid="stFileUploader"] span * {{
            color: {COLORS['text_dark']} !important;
        }}
        
        /* File uploader status text */
        [data-testid="stFileUploaderStatus"],
        [data-testid="stFileUploaderStatus"] * {{
            color: {COLORS['text_dark']} !important;
            font-weight: 500 !important;
        }}
        
        /* Target the actual label text that Streamlit generates */
        .element-container:has([data-testid="stFileUploader"]) label,
        .element-container:has([data-testid="stFileUploader"]) > label,
        div:has([data-testid="stFileUploader"]) label {{
            color: {COLORS['text_dark']} !important;
            font-weight: 700 !important;
            font-size: 1.1rem !important;
        }}
        
        /* Success/Error/Info messages with visible text */
        .stSuccess {{
            background: rgba(16, 185, 129, 0.15) !important;
            border-left: 4px solid {COLORS['success']} !important;
            border-radius: 8px !important;
            padding: 1rem 1.25rem !important;
        }}
        
        .stSuccess > div {{
            color: {COLORS['text_dark']} !important;
            font-weight: 600 !important;
            font-size: 1rem !important;
        }}
        
        .stSuccess p,
        .stSuccess div,
        .stSuccess span {{
            color: {COLORS['text_dark']} !important;
            font-weight: 500 !important;
        }}
        
        /* Success message icon and text - comprehensive styling */
        [data-testid="stSuccess"],
        [data-testid="stSuccess"] *,
        [data-testid="stSuccess"] > div,
        [data-testid="stSuccess"] > div > div,
        [data-testid="stSuccess"] p,
        [data-testid="stSuccess"] div,
        [data-testid="stSuccess"] span,
        [data-testid="stSuccess"] label {{
            color: {COLORS['text_dark']} !important;
            font-weight: 600 !important;
        }}
        
        /* Target all nested elements in success messages */
        .stSuccess * {{
            color: {COLORS['text_dark']} !important;
        }}
        
        /* Ensure icon visibility */
        .stSuccess svg {{
            color: {COLORS['success']} !important;
        }}
        
        .stError {{
            background: rgba(239, 68, 68, 0.15) !important;
            border-left: 4px solid {COLORS['error']} !important;
            border-radius: 8px !important;
            padding: 1rem 1.25rem !important;
        }}
        
        .stError > div,
        .stError p,
        .stError div,
        .stError span {{
            color: {COLORS['text_dark']} !important;
            font-weight: 500 !important;
        }}
        
        .stWarning {{
            background: rgba(245, 158, 11, 0.15) !important;
            border-left: 4px solid {COLORS['warning']} !important;
            border-radius: 8px !important;
            padding: 1rem 1.25rem !important;
        }}
        
        .stWarning > div,
        .stWarning p,
        .stWarning div,
        .stWarning span {{
            color: {COLORS['text_dark']} !important;
            font-weight: 500 !important;
        }}
        
        .stInfo {{
            background: rgba(59, 130, 246, 0.15) !important;
            border-left: 4px solid {COLORS['info']} !important;
            border-radius: 8px !important;
            padding: 1rem 1.25rem !important;
        }}
        
        .stInfo > div,
        .stInfo p,
        .stInfo div,
        .stInfo span {{
            color: {COLORS['text_dark']} !important;
            font-weight: 500 !important;
        }}
        
        /* Scrollbar styling */
        ::-webkit-scrollbar {{
            width: 10px;
            height: 10px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: {COLORS['background']};
            border-radius: 10px;
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: {COLORS['gradient1']};
            border-radius: 10px;
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: {COLORS['primary']};
        }}
    </style>
    """, unsafe_allow_html=True)