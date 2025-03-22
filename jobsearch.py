# jobsearch.py - Place this file in the same folder as your main app
import requests
import re
import os
import streamlit as st
from datetime import datetime
from collections import Counter

@st.cache_data(ttl=3600)
def get_adzuna_jobs(job_title, location="gb", limit=10):
    """
    Get job listings from Adzuna API
    
    Args:
        job_title: Job title to search for
        location: Country code (gb, us, au, etc.)
        limit: Number of results to return
        
    Returns:
        List of job dictionaries
    """
    try:
        # Adzuna API credentials - store these securely
        ADZUNA_APP_ID = st.secrets.get("", os.environ.get("ADZUNA_APP_ID", ""))
        ADZUNA_API_KEY = st.secrets.get("ADZUNA_API_KEY", os.environ.get("ADZUNA_API_KEY", ""))
        
        if not ADZUNA_APP_ID or not ADZUNA_API_KEY:
            st.sidebar.warning("Adzuna API keys not configured. Using sample data.")
            return get_dummy_jobs(job_title, limit)
            
        # Convert common location names to country codes
        location_map = {
            "united states": "us",
            "usa": "us",
            "uk": "gb",
            "united kingdom": "gb",
            "australia": "au",
            "canada": "ca",
            "germany": "de",
            "india": "in",
            "remote": "gb"  # Default to GB for remote
        }
        
        country_code = location_map.get(location.lower(), "gb")
        
        # API endpoint
        base_url = f"https://api.adzuna.com/v1/api/jobs/{country_code}/search/1"
        
        # Parameters
        params = {
            "app_id": ADZUNA_APP_ID,
            "app_key": ADZUNA_API_KEY,
            "results_per_page": limit,
            "what": job_title,
            "content-type": "application/json"
        }
        
        # Make the request
        response = requests.get(base_url, params=params)
        
        if response.status_code != 200:
            st.sidebar.warning(f"Adzuna API error: {response.status_code}")
            return get_dummy_jobs(job_title, limit)
        
        # Parse the response
        data = response.json()
        
        # Extract job listings
        jobs = []
        for result in data.get("results", []):
            # Format salary if available
            salary_info = result.get("salary_is_predicted", "0") 
            salary_text = "Not specified"
            if salary_info == "0" and "salary_min" in result and "salary_max" in result:
                min_salary = result.get("salary_min", 0)
                max_salary = result.get("salary_max", 0)
                if min_salary and max_salary:
                    salary_text = f"{min_salary:,.0f} - {max_salary:,.0f} {result.get('salary_currency', '')}/year"
            
            jobs.append({
                "title": result.get("title", "No title"),
                "company": result.get("company", {}).get("display_name", "No company"),
                "location": result.get("location", {}).get("display_name", "No location"),
                "salary": salary_text,
                "link": result.get("redirect_url", "#"),
                "description": result.get("description", "No description available"),
                "source": "Adzuna"
            })
        
        return jobs if jobs else get_dummy_jobs(job_title, limit)
        
    except Exception as e:
        st.sidebar.warning(f"Error fetching Adzuna jobs: {str(e)}")
        return get_dummy_jobs(job_title, limit)

# Fallback implementation
def get_dummy_jobs(job_title, num_listings=5):
    """Return dummy job listings when API fails"""
    current_date = datetime.now().strftime("%Y-%m-%d")
    return [
        {
            "title": f"{job_title} Engineer",
            "company": "Tech Solutions Inc.",
            "location": "Remote",
            "salary": "$100K-150K",
            "link": "https://example.com/job1",
            "description": "Looking for an experienced professional with skills in programming and problem-solving.",
            "source": "Sample Data",
            "date_posted": current_date
        },
        {
            "title": f"Senior {job_title} Developer",
            "company": "Global Systems",
            "location": "New York, NY",
            "salary": "$130K-180K",
            "link": "https://example.com/job2",
            "description": "Join our team to work on cutting-edge technologies and innovative solutions.",
            "source": "Sample Data",
            "date_posted": current_date
        },
        {
            "title": f"{job_title} Consultant",
            "company": "Consulting Partners",
            "location": "San Francisco, CA",
            "salary": "Not specified",
            "link": "https://example.com/job3",
            "description": "Help our clients transform their businesses with your expertise.",
            "source": "Sample Data",
            "date_posted": current_date
        },
        {
            "title": f"Junior {job_title} Specialist",
            "company": "Startup Innovations",
            "location": "Remote",
            "salary": "$70K-90K",
            "link": "https://example.com/job4",
            "description": "Great opportunity for recent graduates to gain experience in a fast-paced environment.",
            "source": "Sample Data",
            "date_posted": current_date
        },
        {
            "title": f"{job_title} Team Lead",
            "company": "Enterprise Solutions",
            "location": "Chicago, IL",
            "salary": "$140K-180K",
            "link": "https://example.com/job5",
            "description": "Lead a team of professionals in developing cutting-edge solutions.",
            "source": "Sample Data", 
            "date_posted": current_date
        }
    ][:num_listings]

# Master function to get jobs from Adzuna
def get_job_recommendations(job_category, location="remote", num_listings=5):
    """Get job recommendations from Adzuna"""
    try:
        # Map job categories to search terms
        search_terms = {
            "Data Science": "Data Scientist",
            "Machine Learning Engineering": "Machine Learning Engineer", 
            "Frontend Development": "Frontend Developer",
            "Backend Development": "Backend Developer",
            "UI/UX Design": "UI UX Designer",
            "Full Stack Development": "Full Stack Developer",
            "DevOps Engineering": "DevOps Engineer",
            "Software Engineering": "Software Engineer",
            "Software Development": "Software Developer",
            "Cloud Architecture": "Cloud Architect"
        }
        
        # Get appropriate search term
        search_term = search_terms.get(job_category, job_category)
        
        # Get jobs from Adzuna
        with st.spinner(f"Finding {search_term} jobs..."):
            jobs = get_adzuna_jobs(search_term, location, num_listings)
            return jobs
    
    except Exception as e:
        st.warning(f"Error fetching job listings: {str(e)}")
        return get_dummy_jobs(job_category, num_listings)

# Relevance scoring function
def score_job_relevance(resume_text, job_listing):
    """Score the relevance of a job listing to a resume"""
    
    # Clean and normalize text
    resume_text = resume_text.lower()
    
    # Combine job title, company, and description for matching
    job_text = f"{job_listing['title']} {job_listing['company']} {job_listing['description']}".lower()
    
    # Remove common punctuation
    resume_text = re.sub(r'[^\w\s]', ' ', resume_text)
    job_text = re.sub(r'[^\w\s]', ' ', job_text)
    
    # Extract words (excluding common stop words)
    stop_words = {'a', 'an', 'the', 'and', 'or', 'but', 'is', 'are', 'in', 'to', 'for', 'with', 'on', 'at', 'from', 'by'}
    resume_words = [word for word in re.findall(r'\b\w+\b', resume_text) if word not in stop_words]
    job_words = [word for word in re.findall(r'\b\w+\b', job_text) if word not in stop_words]
    
    # Convert to frequency Counter
    resume_counter = Counter(resume_words)
    job_counter = Counter(job_words)
    
    # Calculate TF-IDF like score for matching
    common_words = set(resume_counter.keys()) & set(job_counter.keys())
    
    if not common_words:
        return 0.0
    
    # Calculate weighted score based on frequency
    score = 0
    for word in common_words:
        word_score = min(resume_counter[word], job_counter[word]) / max(resume_counter[word], job_counter[word])
        # Bonus for technical skills and keywords
        if len(word) > 3:  # Skip short words
            score += word_score
    
    # Normalize score
    max_possible = min(len(set(resume_counter.keys())), len(set(job_counter.keys())))
    normalized_score = min(score / max_possible if max_possible > 0 else 0, 1.0)
    
    return normalized_score