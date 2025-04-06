import json
import requests
from typing import List, Dict, Any

def load_test_queries(file_path: str) -> List[Dict[str, Any]]:
    with open(file_path, 'r') as f:
        return json.load(f)

def save_test_queries(test_queries: List[Dict[str, Any]], file_path: str) -> None:
    with open(file_path, 'w') as f:
        json.dump(test_queries, f, indent=2)

def get_recommendations(query: str) -> List[Dict[str, Any]]:
    try:
        response = requests.post(
            "http://localhost:8000/api/recommend",
            json={"query": query},
            timeout=5
        )
        if response.status_code == 200:
            return response.json().get("recommendations", [])
    except Exception:
        return []
    return []

def normalize_assessment_name(assessment: Any) -> str:
    if isinstance(assessment, dict):
        return assessment.get('assessment_name', '').lower().strip().replace(" ", "-")
    return str(assessment).lower().strip().replace(" ", "-")

def main():
    test_queries = load_test_queries("test_queries.json")
    
    for query in test_queries:
        recommendations = get_recommendations(query["query"])
        if recommendations:
            # Take top 3 recommended assessments as relevant
            query["relevant_assessments"] = [
                normalize_assessment_name(rec)
                for rec in recommendations[:3]
            ]
            print(f"Updated: {query['query'][:30]}... -> {query['relevant_assessments']}")
    
    save_test_queries(test_queries, "updated_test_queries.json")

if __name__ == "__main__":
    main()