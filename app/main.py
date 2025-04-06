import streamlit as st
import requests
import json
from typing import Optional

# Configure the page
st.set_page_config(
    page_title="SHL Assessment Recommender",
    page_icon="🎯",
    layout="wide"
)

# Title and description
st.title("🎯 SHL Assessment Recommender")
st.markdown("""
This tool helps you find the most relevant SHL assessments based on your job description or requirements.
Simply enter your query or job description, and we'll recommend the best assessments for your needs.
""")

# Input form
with st.form("recommendation_form"):
    query = st.text_area(
        "Enter your job description or requirements",
        placeholder="Example: Looking for Java developers who can collaborate effectively with business teams..."
    )
    
    col1, col2 = st.columns(2)
    with col1:
        min_duration = st.number_input(
            "Minimum Duration (minutes)",
            min_value=0,
            max_value=180,
            value=0
        )
    with col2:
        max_duration = st.number_input(
            "Maximum Duration (minutes)",
            min_value=0,
            max_value=180,
            value=60
        )
    
    submit_button = st.form_submit_button("Get Recommendations")

# Process the form submission
if submit_button and query:
    try:
        # Prepare the request
        payload = {
            "query": query,
            "min_duration": min_duration,
            "max_duration": max_duration
        }
        
        # Show loading spinner
        with st.spinner("Analyzing your requirements..."):
            # Make API request
            response = requests.post(
                "http://localhost:8000/api/recommend",
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Display recommendations
                st.subheader("Recommended Assessments")
                
                for idx, assessment in enumerate(data["recommendations"], 1):
                    with st.expander(f"{idx}. {assessment['assessment_name']}", expanded=True):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown(f"**Duration:** {assessment['duration']} minutes")
                            st.markdown(f"**Test Type:** {assessment['test_type']}")
                        
                        with col2:
                            st.markdown(f"**Remote Testing:** {'✅' if assessment['remote_testing'] else '❌'}")
                            st.markdown(f"**Adaptive/IRT:** {'✅' if assessment['adaptive_irt'] else '❌'}")
                        
                        st.markdown(f"[View Assessment Details]https://www.shl.com/solutions/products/product-catalog/")
                
                # Display query analysis
                st.subheader("Query Analysis")
                st.json(data["query_analysis"])
                
            else:
                st.error("Failed to get recommendations. Please try again.")
                
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# Add footer
st.markdown("---")