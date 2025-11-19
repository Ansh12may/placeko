
import os
from dotenv import load_dotenv

load_dotenv()

# API keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

# Model settings
LLM_MODEL = "gpt-3.5-turbo" 

# Job search settings
DEFAULT_JOB_COUNT = 5
JOB_PLATFORMS = ["LinkedIn", "Indeed", "Glassdoor", "ZipRecruiter", "Monster"]


COLORS = {
    # Primary palette - Professional and elegant (Apple-inspired)
    "primary": "#007AFF",       # iOS Blue - professional and trustworthy
    "primary_dark": "#0051D5",  # Darker blue for hover states
    "secondary": "#5856D6",     # Purple - elegant accent
    "tertiary": "#FF9500",      # Orange - warm and inviting
    "quaternary": "#34C759",    # Green - success and growth
    
    # Accent colors - Subtle and refined
    "accent": "#FF9500",        # Orange for CTAs
    "accent1": "#5AC8FA",       # Light blue - fresh
    "accent2": "#AF52DE",       # Purple - creative
    "accent3": "#FF3B30",       # Red - attention
    
    # Subtle gradient combinations (lighter, more readable)
    "gradient1": "linear-gradient(135deg, #007AFF 0%, #5856D6 100%)",  # Blue to purple
    "gradient2": "linear-gradient(135deg, #FF9500 0%, #FF3B30 100%)",  # Orange to red
    "gradient3": "linear-gradient(135deg, #5AC8FA 0%, #007AFF 100%)",  # Light blue to blue
    "gradient4": "linear-gradient(135deg, #34C759 0%, #30D158 100%)",  # Green gradient
    "gradient5": "linear-gradient(135deg, #AF52DE 0%, #5856D6 100%)",  # Purple gradient
    
    # Light backgrounds with gradients (for cards)
    "gradient_light1": "linear-gradient(135deg, #E3F2FD 0%, #E8EAF6 100%)",  # Light blue-purple
    "gradient_light2": "linear-gradient(135deg, #FFF3E0 0%, #FFEBEE 100%)",  # Light orange-red
    "gradient_light3": "linear-gradient(135deg, #E0F7FA 0%, #E3F2FD 100%)",  # Light cyan-blue
    "gradient_light4": "linear-gradient(135deg, #E8F5E9 0%, #F1F8E9 100%)",  # Light green
    
    # Functional colors - Clear and accessible
    "success": "#34C759",       # Green for success
    "warning": "#FF9500",       # Orange for warnings
    "error": "#FF3B30",         # Red for errors
    "info": "#007AFF",          # Blue for information
    
    # Background and text - High contrast for readability
    "background": "#F5F5F7",    # Light gray (Apple-style)
    "card_bg": "#FFFFFF",       # Pure white for cards
    "card_bg_alt": "#FAFAFA",  # Slightly off-white for variety
    "text": "#000000",         # White for text on dark backgrounds
    "text_dark": "#1D1D1F",     # Almost black for maximum readability
    "text_medium": "#424245",  # Medium gray for secondary text
    "text_light": "#000000",   # Light gray for tertiary text
    "text_primary": "#007AFF",  # Primary blue for links/accents
    "panel_bg": "#F5F5F7",      # Light gray for panels
    "panel_bg_alt": "#FFFFFF",  # White for alternate panels
    "border": "#D2D2D7",        # Light border
    "border_light": "#E5E5EA", # Very light border
    "shadow": "rgba(0, 0, 0, 0.1)",  # Subtle shadow
    "shadow_medium": "rgba(0, 0, 0, 0.15)",  # Medium shadow
}





    