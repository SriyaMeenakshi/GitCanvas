"""
AI Service for generating GitHub profile compliments
Supports both OpenAI and Google Gemini APIs
"""

import random
import requests
from typing import Dict, Optional
from config.settings import get_settings
try:
    import google.generativeai as genai  # type: ignore
    _HAS_GENAI = True
except Exception:
    genai = None
    _HAS_GENAI = False
from openai import OpenAI

from utils.logger import setup_logger

logger = setup_logger(__name__)

# Get API keys from environment
_cfg = get_settings()
OPENAI_API_KEY = _cfg.openai_api_key_value()
GEMINI_API_KEY = _cfg.gemini_api_key_value()

# Initialize APIs
if GEMINI_API_KEY:
    if _HAS_GENAI:
        try:
            genai.configure(api_key=GEMINI_API_KEY)
        except Exception as e:
            logger.error(f"Failed to configure Google Generative AI client: {e}")
    else:
        logger.warning("Google Generative AI client not installed; Gemini support disabled.")

if OPENAI_API_KEY:
    openai_client = OpenAI(api_key=OPENAI_API_KEY)


def create_compliment_prompt(profile_data: Dict) -> str:
    """Create the prompt for AI based on profile data"""
    username = profile_data.get('username', 'Unknown')
    top_languages = profile_data.get('top_languages', [])
    total_commits = profile_data.get('total_commits', 0)
    public_repos = profile_data.get('public_repos', 0)
    followers = profile_data.get('followers', 0)
    stars = profile_data.get('stars', 0)
    
    # Format languages
    languages_str = ', '.join([lang['name'] for lang in top_languages[:3]]) if top_languages else 'various languages'
    
    prompt = f"""Generate a single enthusiastic, genuine compliment for this amazing GitHub developer:

Username: {username}
Top Languages: {languages_str}
Total Commits: {total_commits}
Public Repositories: {public_repos}
Followers: {followers}
Total Stars: {stars}

Be OVERLY POSITIVE, encouraging, and hyped-like a biggest fan writing about them. 
Celebrate their contributions and skill. Examples of the style:
- "Python wizard with {total_commits} commits of pure inspiration - you're a code legend!"
- "An absolute GitHub rockstar with the dedication to back it up!"
- "Your {public_repos} repos are like works of art - you're crushing it!"
- "Commits like your's show the heart of a true developer - inspiring stuff!"
- "Your follower count doesn't do justice to your talent - absolute gem!"

Generate ONE enthusiastic compliment line now (no quotes, just the text):"""
    
    return prompt


def generate_compliment_with_openai(profile_data: Dict) -> str:
    """Generate compliment using OpenAI GPT"""
    if not OPENAI_API_KEY:
        raise ValueError("OpenAI API key not configured")
    
    prompt = create_compliment_prompt(profile_data)
    
    try:
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are an enthusiastic tech supporter and biggest fan of GitHub developers. You love celebrating achievements and highlighting talent. Be overly positive, genuine, and hype-man energy. Keep it to one line only."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=100,
            temperature=0.9
        )
        
        compliment = response.choices[0].message.content.strip()
        # Remove quotes if present
        compliment = compliment.strip('"').strip("'")
        return compliment
        
    except Exception as e:
        logger.error(f"OpenAI API error: {e}")
        raise


def generate_compliment_with_gemini(profile_data: Dict) -> str:
    """Generate compliment using Google Gemini"""
    if not GEMINI_API_KEY:
        raise ValueError("Gemini API key not configured")
    if not _HAS_GENAI:
        raise ImportError("google.generativeai is not installed")
    
    prompt = create_compliment_prompt(profile_data)
    
    try:
        model = genai.GenerativeModel('gemini-pro')
        
        system_prompt = "You are an enthusiastic tech fan and biggest supporter of GitHub developers. Celebrate their contributions generously! Generate ONE enthusiastic compliment. Keep it genuine and hyped. Return ONLY the compliment text, no quotes or explanation.\n\n"
        
        response = model.generate_content(
            system_prompt + prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.9,
                max_output_tokens=100,
            )
        )
        
        compliment = response.text.strip()
        # Remove quotes and take first line only
        compliment = compliment.strip('"').strip("'").split('\n')[0]
        return compliment
        
    except Exception as e:
        logger.error(f"Gemini API error: {e}")
        raise


def get_fallback_compliment(profile_data: Dict) -> str:
    """Get a fallback compliment when AI services are unavailable"""
    top_languages = profile_data.get('top_languages', [])
    total_commits = profile_data.get('total_commits', 0)
    public_repos = profile_data.get('public_repos', 0)
    
    top_lang = top_languages[0]['name'] if top_languages else 'Code'
    
    fallback_compliments = [
        f"Your {total_commits} commits show dedication that's truly inspiring - you're a GitHub champion!",
        "The code you share with the world makes it a better place - you're awesome!",
        f"A {top_lang} expert with {public_repos} repositories of pure excellence!",
        f"With {total_commits} commits, you're not just coding - you're building legacies!",
        "Your GitHub profile is a testament to your skill and passion - absolutely stellar!",
        f"Contributors like you make open source amazing - {top_lang} wizard alert!",
        "Your consistency and output put you in the top tier of developers - truly impressive!",
        f"{public_repos} amazing repositories that showcase your incredible talent!",
        "Your commits are like breadcrumbs of brilliance - every one tells a story of excellence!",
        "The tech community is better because of developers like you - keep being amazing!"
    ]
    
    return random.choice(fallback_compliments)


def generate_profile_compliment(profile_data: Dict) -> Dict:
    """
    Main function to generate compliment with fallback mechanism
    Returns dict with compliment and metadata
    """
    compliment_text = None
    source = None
    
    # Try OpenAI first if available
    if OPENAI_API_KEY:
        try:
            compliment_text = generate_compliment_with_openai(profile_data)
            source = "openai"
        except Exception as e:
            logger.warning(f"OpenAI failed: {e}")
    
    # Try Gemini if OpenAI failed or not available
    if not compliment_text and GEMINI_API_KEY:
        try:
            compliment_text = generate_compliment_with_gemini(profile_data)
            source = "gemini"
        except Exception as e:
            logger.warning(f"Gemini failed: {e}")
    
    # Use fallback if all AI services failed
    if not compliment_text:
        compliment_text = get_fallback_compliment(profile_data)
        source = "fallback"
    
    return {
        "compliment": compliment_text,
        "source": source,
        "username": profile_data.get('username'),
        "success": True
    }


# For testing
if __name__ == "__main__":
    # Test data
    test_profile = {
        "username": "testuser",
        "top_languages": [
            {"name": "Python", "count": 10},
            {"name": "JavaScript", "count": 5}
        ],
        "total_commits": 500,
        "public_repos": 25,
        "followers": 100,
        "stars": 250
    }
    
    result = generate_profile_compliment(test_profile)
    logger.info(f"Compliment: {result['compliment']}")
    logger.info(f"Source: {result['source']}")
