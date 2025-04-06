import pytest
from utils.metrics import evaluate_recommendations

# Sample test cases
TEST_QUERIES = [
    {
        "query": "I am hiring for Java developers who can also collaborate effectively with my business teams. Looking for an assessment(s) that can be completed in 40 minutes.",
        "relevant_items": [
            "java-programming-test",
            "collaboration-skills-assessment",
            "technical-communication-test"
        ],
        "recommended_items": [
            "java-programming-test",
            "collaboration-skills-assessment",
            "technical-communication-test",
            "problem-solving-assessment"
        ]
    },
    {
        "query": "Looking to hire mid-level professionals who are proficient in Python, SQL and Java Script. Need an assessment package that can test all skills with max duration of 60 minutes.",
        "relevant_items": [
            "python-programming-test",
            "sql-skills-assessment",
            "javascript-test",
            "full-stack-assessment"
        ],
        "recommended_items": [
            "full-stack-assessment",
            "python-programming-test",
            "sql-skills-assessment",
            "javascript-test",
            "web-development-test"
        ]
    },
    {
        "query": "I am hiring for an analyst and wants applications to screen using Cognitive and personality tests, what options are available within 45 mins.",
        "relevant_items": [
            "cognitive-ability-test",
            "personality-assessment",
            "analytical-thinking-test"
        ],
        "recommended_items": [
            "cognitive-ability-test",
            "personality-assessment",
            "analytical-thinking-test",
            "data-analysis-test"
        ]
    }
]

def test_evaluation_metrics():
    """Test the evaluation metrics calculation."""
    metrics = evaluate_recommendations(TEST_QUERIES, k=3)
    
    # Check that metrics are calculated correctly
    assert "recall@3" in metrics
    assert "map@3" in metrics
    assert 0 <= metrics["recall@3"] <= 1
    assert 0 <= metrics["map@3"] <= 1
    
    # For our test data, we expect perfect recall since all relevant items
    # are in the top 3 recommendations
    assert metrics["recall@3"] == 1.0
    
    # MAP should also be high since relevant items are ranked first
    assert metrics["map@3"] > 0.8

def test_empty_queries():
    """Test evaluation with empty query list."""
    metrics = evaluate_recommendations([], k=3)
    assert metrics["recall@3"] == 0.0
    assert metrics["map@3"] == 0.0

def test_partial_relevance():
    """Test evaluation with partially relevant recommendations."""
    test_case = [{
        "query": "Test query",
        "relevant_items": ["item1", "item2", "item3"],
        "recommended_items": ["item1", "item4", "item5", "item2", "item3"]
    }]
    
    metrics = evaluate_recommendations(test_case, k=3)
    
    # Only one relevant item in top 3
    assert metrics["recall@3"] == 1/3
    assert metrics["map@3"] < 1.0 