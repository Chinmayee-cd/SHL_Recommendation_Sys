# SHL Assessment Recommender

An intelligent recommendation system that helps hiring managers find the most relevant SHL assessments based on job descriptions or natural language queries.

## Features

- Natural language query processing
- Job description analysis
- Intelligent assessment recommendations
- Support for both API and web interface
- Evaluation metrics tracking (Recall@K, MAP@K)

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your Google Gemini API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

## Running the Application

### API Server

```bash
uvicorn api.main:app --reload
```

### Web Interface

```bash
streamlit run app/main.py
```

## Project Structure

```
shl-assessment-recommender/
├── api/                 # FastAPI backend
├── app/                 # Streamlit frontend
├── data/               # Data storage
├── models/             # ML models and utilities
├── tests/              # Test cases
└── utils/              # Utility functions
```

## API Documentation

The API provides endpoints for:

- `/api/recommend` - Get assessment recommendations
- `/api/evaluate` - Evaluate recommendation quality

## Evaluation Metrics

- Mean Recall@K
- Mean Average Precision@K (MAP@K)

## License

MIT License
