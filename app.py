import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os
import re
import tempfile
import fitz  # PyMuPDF
import shutil
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy import sparse
# Add this near the top with your other imports
import os
try:
    from jobsearch import get_job_recommendations, score_job_relevance
except ImportError:
    st.error("jobsearch.py file missing. Please create it to enable job recommendations.")
    
    # Create simple dummy implementations if the file is missing
    def get_job_recommendations(job_category, location="remote", num_listings=5):
        return []
        
    def score_job_relevance(resume_text, job_listing):
        return 0.5

# Set page configuration
st.set_page_config(
    page_title="💼 JOBI Match - 🎯 Smart Resume Screening & 🔍 Job Recommendation",
    page_icon="📄",
    layout="wide"
)

# Fix for Windows file handling
def extract_text_from_pdf(pdf_file):
    """Extract text with better Windows file handling"""
    # Create temp file with a unique name
    temp_dir = tempfile.mkdtemp()
    temp_path = os.path.join(temp_dir, "resume.pdf")
    
    try:
        # Save uploaded file to the temp location
        with open(temp_path, "wb") as f:
            f.write(pdf_file.getbuffer())
        
        # Extract text
        doc = fitz.open(temp_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    except Exception as e:
        st.error(f"Error processing PDF: {e}")
        return ""
    finally:
        # Clean up - make sure to close file handles first
        try:
            os.remove(temp_path)
        except:
            pass
        try:
            shutil.rmtree(temp_dir)
        except:
            pass

# Function to detect model feature count
def get_model_feature_count(model):
    """Detect the number of features a model expects"""
    if hasattr(model, 'n_features_in_'):
        return model.n_features_in_
    elif hasattr(model, 'coef_') and hasattr(model.coef_, 'shape'):
        return model.coef_.shape[1]
    elif hasattr(model, 'feature_importances_') and hasattr(model.feature_importances_, 'shape'):
        return model.feature_importances_.shape[0]
    else:
        return None

# Cache the model loading
@st.cache_resource
def load_models(models_dir):
    """Load all models and artifacts with auto feature detection"""
    try:
        models = {}
        auto_model_info = {}
        
        # Verify models directory exists
        if not os.path.exists(models_dir):
            st.error(f"Models directory not found: {models_dir}")
            return {}, []
        
        # Load label encoder
        encoder_path = os.path.join(models_dir, 'label_encoder.pkl')
        if not os.path.exists(encoder_path):
            st.error(f"Label encoder not found at: {encoder_path}")
            return {}, []
            
        with open(encoder_path, 'rb') as f:
            models['label_encoder'] = pickle.load(f)
        
        # Load available classification models
        model_files = [
            f for f in os.listdir(models_dir) 
            if f.endswith('.pkl') and 
            not f.startswith('tfidf_') and 
            not f.startswith('bow_') and 
            not f.startswith('count_') and
            not f.startswith('label_encoder') and
            not 'vectorizer' in f.lower()
        ]
        
        for model_file in model_files:
            with open(os.path.join(models_dir, model_file), 'rb') as f:
                models[model_file] = pickle.load(f)
        
        # Load vectorizers
        vectorizer_files = [
            f for f in os.listdir(models_dir)
            if 'vectorizer' in f.lower() and f.endswith('.pkl')
        ]
        
        for vec_file in vectorizer_files:
            with open(os.path.join(models_dir, vec_file), 'rb') as f:
                models[vec_file] = pickle.load(f)
        
        # Auto-detect feature dimensions
        for model_name in [m for m in models.keys() if m.endswith('.pkl') and not 'vectorizer' in m.lower() and not 'label_encoder' in m.lower()]:
            if 'pipeline' in model_name.lower():
                # Mark this as a pipeline that takes raw text
                auto_model_info[model_name] = {'is_pipeline': True}
            else:
                feature_count = get_model_feature_count(models[model_name])
                if feature_count:
                    auto_model_info[model_name] = {
                        'vectorizer': 'tfidf_vectorizer.pkl', 
                        'features': feature_count,
                        'is_pipeline': False
                    }
        
        return models, model_files, auto_model_info
    except Exception as e:
        st.error(f"Error loading models: {str(e)}")
        return {}, [], {}

# Clean text
def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Adjust feature dimensions if needed
def adjust_feature_dimensions(features, expected_features):
    if expected_features is None:
        return features
        
    current_features = features.shape[1]
    
    if current_features == expected_features:
        return features
    
    if current_features > expected_features:
        return features[:, :expected_features]
    else:
        padding = sparse.csr_matrix((features.shape[0], expected_features - current_features))
        return sparse.hstack([features, padding])

# MODEL-VECTORIZER MAPPING - FALLBACK IF AUTO-DETECTION FAILS
MODEL_INFO = {
    'naive_bayes_model.pkl': {'vectorizer': 'tfidf_vectorizer.pkl', 'features': 3000, 'is_pipeline': False},
    'linear_svm_model.pkl': {'vectorizer': 'tfidf_vectorizer.pkl', 'features': 661, 'is_pipeline': False},
    'ensemble_model.pkl': {'vectorizer': 'tfidf_vectorizer.pkl', 'features': 661, 'is_pipeline': False},
    'ensemble_pipeline.pkl': {'is_pipeline': True},  # Mark as a pipeline that takes raw text
    'realistic_naive_bayes.pkl': {'vectorizer': 'bow_vectorizer.pkl', 'features': None, 'is_pipeline': False}
}

# Function to classify resume
def classify_resume(resume_text, model, model_name, loaded_models, model_info):
    try:
        # Create category mapping
        label_encoder = loaded_models['label_encoder']
        categories = label_encoder.classes_
        category_names = {i: cat for i, cat in enumerate(categories)}
        
        # Check if this is a pipeline model
        is_pipeline = False
        
        # First check auto-detected info
        if model_name in model_info:
            model_specs = model_info[model_name]
            is_pipeline = model_specs.get('is_pipeline', False)
        # Fall back to predefined
        elif model_name in MODEL_INFO:
            is_pipeline = MODEL_INFO[model_name].get('is_pipeline', False)
        # Default to not a pipeline
        else:
            is_pipeline = False
            
        # Special check for names containing "pipeline"
        if 'pipeline' in model_name.lower():
            is_pipeline = True
            
        # Log for debugging
        st.sidebar.write(f"Model: {model_name}")
        st.sidebar.write(f"Is pipeline: {is_pipeline}")
        
        if is_pipeline:
            # PIPELINE MODE: Pass raw text directly to the model
            try:
                # Try with raw text first
                prediction = model.predict([resume_text])[0]
            except:
                # If that fails, try with cleaned text
                cleaned_text = clean_text(resume_text)
                prediction = model.predict([cleaned_text])[0]
                
            # Get predicted category
            if isinstance(prediction, str):
                predicted_category = prediction
            else:
                predicted_category = category_names[prediction]
                
            # Get probabilities if available
            if hasattr(model, 'predict_proba'):
                try:
                    probabilities = model.predict_proba([resume_text])[0]
                except:
                    probabilities = model.predict_proba([clean_text(resume_text)])[0]
                    
                top_indices = probabilities.argsort()[-3:][::-1]
                top_categories = [(category_names[idx], float(probabilities[idx])) for idx in top_indices]
            else:
                top_categories = [(predicted_category, 1.0)]
                
        else:
            # STANDARD MODEL MODE: Vectorize text first
            cleaned_text = clean_text(resume_text)
            
            # Get model info - first try auto-detected, then fall back to predefined
            if model_name in model_info and not model_info[model_name].get('is_pipeline', False):
                model_specs = model_info[model_name]
            else:
                model_specs = MODEL_INFO.get(model_name, {
                    'vectorizer': 'tfidf_vectorizer.pkl', 
                    'features': None,
                    'is_pipeline': False
                })
            
            vectorizer_name = model_specs.get('vectorizer', 'tfidf_vectorizer.pkl')
            expected_features = model_specs.get('features', None)
            
            # Log for debugging
            st.sidebar.write(f"Using vectorizer: {vectorizer_name}")
            st.sidebar.write(f"Expected features: {expected_features}")
            
            # Get vectorizer
            vectorizer = loaded_models[vectorizer_name]
            
            # Transform text
            features = vectorizer.transform([cleaned_text])
            st.sidebar.write(f"Actual features: {features.shape[1]}")
            
            # Adjust features if needed
            if expected_features is not None:
                features = adjust_feature_dimensions(features, expected_features)
            
            # Predict
            prediction = model.predict(features)[0]
            predicted_category = category_names[prediction]
            
            # Get probabilities or decision scores
            if hasattr(model, 'predict_proba'):
                probabilities = model.predict_proba(features)[0]
                top_indices = probabilities.argsort()[-3:][::-1]
                top_categories = [(category_names[idx], float(probabilities[idx])) for idx in top_indices]
            else:
                # Fall back to decision function if available
                if hasattr(model, 'decision_function'):
                    decision_scores = model.decision_function(features)[0]
                    top_indices = np.argsort(decision_scores)[-3:][::-1]
                    
                    # Normalize scores to appear like probabilities
                    scores = decision_scores[top_indices]
                    if len(scores) > 0:
                        max_score = max(abs(score) for score in scores)
                        normalized_scores = [(score + max_score) / (2 * max_score) for score in scores]
                        top_categories = [(category_names[idx], float(score)) for idx, score in zip(top_indices, normalized_scores)]
                    else:
                        top_categories = [(predicted_category, 1.0)]
                else:
                    top_categories = [(predicted_category, 1.0)]
        
        return predicted_category, top_categories
        
    except Exception as e:
        st.error(f"Error during classification: {str(e)}")
        return "Classification Error", [("Error", 0.0)]

# Main app
def main():
    st.title("📄 Resume Job Category Classifier")
    st.write("Upload a resume to classify it into the most suitable job category")
    
    # Add sidebar API information
    with st.sidebar.expander("Job API Settings"):
        st.write("""
        ### Adzuna API Setup
        
        To enable real job listings:
        
        1. Register at [Adzuna API](https://developer.adzuna.com/)
        2. Get your App ID and Key (free tier: 100 calls/day)
        3. Add them to your Streamlit secrets
        """)
        
        # Show API status
        adzuna_configured = bool(st.secrets.get("ADZUNA_APP_ID", os.environ.get("ADZUNA_APP_ID", "")))
        st.write(f"- Adzuna API: {'✅ Configured' if adzuna_configured else '❌ Not configured'}")
    
    # Path to models (change this to your models folder path)
    models_dir = './models'  # IMPORTANT: Update this path to where your models are stored
    
    # Show actual path for debugging
    st.sidebar.write(f"Looking for models in: {os.path.abspath(models_dir)}")
    
    # Load models with auto-detection of features
    loaded_models, model_files, auto_model_info = load_models(models_dir)
    
    if not model_files:
        st.error("No models found! Please check the models directory.")
        
        # Help users find the correct path
        st.write("### Troubleshooting:")
        st.write("1. Make sure you have a folder named 'models' in the same directory as this script.")
        st.write("2. The models folder should contain your .pkl files.")
        st.write("3. If your models are in a different location, update the 'models_dir' variable in the code.")
        
        # Let user select a different models directory
        new_models_dir = st.text_input("Enter full path to models directory:", 
                                       value=os.path.abspath(models_dir))
        if st.button("Try this directory"):
            loaded_models, model_files, auto_model_info = load_models(new_models_dir)
            if model_files:
                st.success(f"Found {len(model_files)} models in {new_models_dir}!")
                models_dir = new_models_dir
            else:
                st.error(f"No models found in {new_models_dir}")
        
        return
    
    # DEFINE MODEL OPTIONS
    model_options = {
        'naive_bayes_model.pkl': 'Naive Bayes Classifier',
        'linear_svm_model.pkl': 'Linear SVM Classifier',
        'ensemble_model.pkl': 'Ensemble Classifier',
        'ensemble_pipeline.pkl': 'Ensemble Pipeline (recommended)',
        'realistic_naive_bayes.pkl': 'Realistic Naive Bayes'
    }
    
    # Default to ensemble pipeline if available
    default_model = 'ensemble_pipeline.pkl' if 'ensemble_pipeline.pkl' in model_files else (
        'ensemble_model.pkl' if 'ensemble_model.pkl' in model_files else model_files[0]
    )
    
    # Model selection
    selected_model_name = st.selectbox(
        "Select Classification Model:",
        options=model_files,
        format_func=lambda x: model_options.get(x, x),
        index=model_files.index(default_model) if default_model in model_files else 0
    )
    
    selected_model = loaded_models[selected_model_name]
    
    # File uploader
    uploaded_file = st.file_uploader("Upload Resume (PDF format)", type=["pdf"])
    
    if uploaded_file is not None:
        with st.spinner("Extracting text from PDF..."):
            resume_text = extract_text_from_pdf(uploaded_file)
        
        if not resume_text:
            st.error("Could not extract text from the PDF. Please try a different file.")
            return
            
        # Preview the extracted text
        with st.expander("Resume Text Preview"):
            st.text(resume_text[:1000] + "..." if len(resume_text) > 1000 else resume_text)
        
        # Classify button
        if st.button("Classify Resume"):
            with st.spinner("Classifying..."):
                # Fixed function call - pass auto_model_info as the fifth argument
                predicted_category, top_categories = classify_resume(
                    resume_text, selected_model, selected_model_name, loaded_models, auto_model_info
                )
            
            # Show results
            st.success(f"Predicted Job Category: **{predicted_category}**")
            
            # Display top categories
            st.subheader("Top Job Categories:")
            
            # Progress bars for top categories
            for category, prob in top_categories:
                st.write(f"{category}")
                st.progress(min(float(prob), 1.0))
                st.write(f"Confidence: {prob:.2f}")
            
            # Recommendations based on category
            st.subheader("Recommendations:")
            
            # Add category-specific advice
            if predicted_category in ["Data Science", "Machine Learning Engineering"]:
                st.info("Consider highlighting your experience with Python, machine learning libraries, and data analysis projects.")
            elif predicted_category in ["Frontend Development", "UI/UX Design"]:
                st.info("Emphasize your portfolio and experience with modern frameworks like React, Angular, or Vue.")
            elif predicted_category in ["Backend Development", "Full Stack Development"]:
                st.info("Make sure to showcase your API development skills and database knowledge.")
            elif predicted_category in ["Software Development", "Software Engineering"]:
                st.info("Highlight your programming languages, frameworks, and software development methodologies.")
            elif predicted_category in ["DevOps Engineering", "Cloud Architecture"]:
                st.info("Emphasize your experience with cloud platforms, containerization, and automation tools.")
            else:
                st.info("Ensure your resume highlights relevant technical skills and experience for this role.")
            
            # Job Recommendations Section - MOVED THIS INSIDE the classification button click
            if predicted_category != "Classification Error":
                # Job Recommendations Section
                st.subheader("🔍 Recommended Jobs Based on Your Resume")
                
                # Let user select location
                col1, col2 = st.columns([3, 1])
                with col1:
                    location_options = ["Remote", "United States", "India", "United Kingdom", "Canada", "Australia", "Germany"]
                    selected_location = st.selectbox("Select location for jobs:", location_options)
                
                with col2:
                    num_jobs = st.selectbox("Number of jobs:", [5, 10, 15], index=0)
                
                # Get job recommendations
                with st.spinner("Finding relevant jobs..."):
                    job_listings = get_job_recommendations(predicted_category, selected_location, num_jobs)
                
                # Calculate relevance scores
                if resume_text and job_listings:
                    scored_jobs = []
                    for job in job_listings:
                        relevance = score_job_relevance(resume_text, job)
                        scored_jobs.append((job, relevance))
                    
                    # Sort by relevance
                    scored_jobs.sort(key=lambda x: x[1], reverse=True)
                    
                    # Display jobs with relevance bars
                    if scored_jobs:
                        st.write(f"Found {len(scored_jobs)} job opportunities matching your profile:")
                        for i, (job, relevance) in enumerate(scored_jobs):
                            with st.expander(f"{i+1}. {job['title']} at {job['company']}"):
                                col1, col2 = st.columns([3, 1])
                                
                                with col1:
                                    st.write(f"**Company:** {job['company']}")
                                    st.write(f"**Location:** {job['location']}")
                                    if job['salary'] != "Not specified":
                                        st.write(f"**Salary:** {job['salary']}")
                                
                                with col2:
                                    st.write("**Match Score:**")
                                    st.progress(relevance)
                                    st.write(f"{int(relevance * 100)}% match")
                                
                                st.write("**Description:**")
                                st.write(job['description'])
                                
                                st.markdown(f"[Apply Now]({job['link']})", unsafe_allow_html=True)
                    else:
                        st.info("No job listings found. Try changing the location or try again later.")
                else:
                    st.info("Job recommendations could not be retrieved. Please try again.")

if __name__ == "__main__":
    main()