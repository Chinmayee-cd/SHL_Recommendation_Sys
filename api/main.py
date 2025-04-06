from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import google.generativeai as genai
from dotenv import load_dotenv
import os
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI(
    title="SHL Assessment Recommender API",
    description="API for recommending SHL assessments based on job descriptions",
    version="1.0.0"
)

class RecommendationRequest(BaseModel):
    query: str
    max_duration: Optional[int] = None
    min_duration: Optional[int] = None

class Assessment(BaseModel):
    assessment_name: str
    url: str
    remote_testing: bool
    adaptive_irt: bool  # Changed to match the JSON key
    duration: int      # Changed to match the JSON key
    test_type: str   

class RecommendationResponse(BaseModel):
    recommendations: List[Assessment]
    query_analysis: dict
@app.get("/")
async def root():
    return {"message": "Welcome to the SHL Assessment Recommender API"}
@app.post("/api/recommend", response_model=RecommendationResponse)
async def get_recommendations(request: RecommendationRequest):
    e=None
    try:
        model_list = genai.list_models()
        available_models = [model.name for model in model_list if 'generateContent' in model.supported_generation_methods]
        # Initialize Gemini model
        model = genai.GenerativeModel('models/gemini-1.5-flash')
        
        # Construct the prompt
        prompt = f"""
        Given the following job description or query, recommend the most relevant SHL assessments.

        Query: {request.query}

        Additional constraints:
        - Maximum duration: {request.max_duration} minutes
        - Minimum duration: {request.min_duration} minutes

        Please analyze the query and recommend up to 10 most relevant SHL assessments.
        For each assessment, provide:
        1. assessment_name (string)
        2. url (string)
        3. remote_testing (boolean)
        4. adaptive_irt (boolean)
        5. duration (integer)
        6. test_type (string)

        Format the response as a **single, plain JSON object** with the following structure and **nothing else, including no comments**:
        {{
        "query_analysis": {{ ... }},
        "recommendations": [ {{ ... }}, {{ ... }}, ... ]
        }}
        Ensure the JSON is valid and directly parsable. Do not include any markdown formatting, comments, or extra text outside of this JSON structure.
        """
        
        # Get response from Gemini
        response = model.generate_content(prompt)
        logging.info(f"Gemini API Response Text: {response.text}")  # Log the raw response
        cleaned_response_text = response.text.replace("```json", "").replace("```", "").strip()
        # Parse the response
        try:
            result = json.loads(cleaned_response_text)
            return RecommendationResponse(**result)
        except json.JSONDecodeError as json_e:
            e=json_e
            logging.error(f"JSONDecodeError after cleaning: {e}")
            logging.error(f"Failed to parse cleaned response: {cleaned_response_text}")
            raise HTTPException(status_code=500, detail="Failed to parse model response")
            
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"} 