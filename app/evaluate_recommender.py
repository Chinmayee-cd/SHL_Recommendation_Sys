import json
import requests
from typing import List, Dict, Any
from evaluation_metrics import evaluate_recommendation_system
headers = {
    'Cache-Control': 'no-cache',
    'Pragma': 'no-cache'
}
def load_test_queries(file_path: str) -> List[Dict[str, Any]]:
    with open(file_path, 'r') as f:
        return json.load(f)

def get_recommendations(query: str, min_duration: int = 0, max_duration: int = 60) -> List[Any]:
    payload = {
        "query": query,
        "min_duration": min_duration,
        "max_duration": max_duration
    }

    try:
        response = requests.post(
            "http://localhost:8000/api/recommend",  # Replace with your API endpoint
            json=payload
        )

        if response.status_code == 200:
            data = response.json()
            # Handle both list of dictionaries and list of strings
            if isinstance(data.get("recommendations"), list):
                return data["recommendations"]
            else:
                print("Unexpected response format. Expected 'recommendations' to be a list.")
                return []
        else:
            print(f"Error getting recommendations: {response.status_code}")
            print(f"Response: {response.text}")
            return []
    except Exception as e:
        print(f"Exception when getting recommendations: {str(e)}")
        return []

def main():
    # Load test queries
    test_queries = load_test_queries("test_queries.json")  # Create this file

    # Collect recommendations and relevant assessments
    all_recommendations = []
    all_relevant_assessments = []

    for test_query in test_queries:
        query_text = test_query["query"]
        relevant_assessments = test_query["relevant_assessments"]

        #print(f"\nProcessing query: {query_text[:50]}...")

        # Get recommendations from the API
        recommendations = get_recommendations(query_text)
        print(f"\nRecommendations: {recommendations}")
        # Extract assessment names, handling different response formats
        if recommendations and isinstance(recommendations[0], dict):
            assessment_names = [rec.get('assessment_name', '') for rec in recommendations]  # Corrected line
        else:
            assessment_names = recommendations  # Assuming recommendations are already strings

        all_recommendations.append(assessment_names)
        all_relevant_assessments.append(relevant_assessments)

    # Evaluate the recommendation system
    k_values = [3]  # As per the assignment requirement
    results = evaluate_recommendation_system(
        all_recommendations,
        all_relevant_assessments,
        k_values
    )

    # Print results
    print("\nEvaluation Results:")
    print("==================")

    for metric_name, metric_values in results.items():  # Correct iteration
        for k, value in metric_values.items():
            print(f"\nK = {k}:")
            if metric_name == 'recall_at_k':
                print(f"  Mean Recall@K: {value:.4f}")
            elif metric_name == 'map_at_k':
                print(f"  MAP@K: {value:.4f}")

if __name__ == "__main__":
    main()