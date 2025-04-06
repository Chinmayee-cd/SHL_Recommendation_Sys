import numpy as np
from typing import List, Dict, Any, Union

def recall_at_k(recommendations: List[Any], relevant_assessments: List[str], k: int) -> float:
    """
    Calculate Recall@K for a single query.

    Args:
        recommendations: List of recommended assessments (can be strings or dictionaries)
        relevant_assessments: List of relevant assessment IDs
        k: Number of top recommendations to consider

    Returns:
        Recall@K value
    """
    if not relevant_assessments:
        return 0.0

    # Get the top k recommendations
    top_k = recommendations[:k]

    # Count how many of the top k recommendations are relevant
    relevant_count = 0
    for rec in top_k:
        # Handle both string and dictionary recommendations
        if isinstance(rec, str):
            rec_name = rec
        else:
            rec_name = rec.get('assessment_name', '')

        if rec_name in relevant_assessments:
            relevant_count += 1

    # Calculate recall
    recall = relevant_count / len(relevant_assessments)

    return recall

def precision_at_k(recommendations: List[Any], relevant_assessments: List[str], k: int) -> float:
    """
    Calculate Precision@K for a single query.

    Args:
        recommendations: List of recommended assessments (can be strings or dictionaries)
        relevant_assessments: List of relevant assessment IDs
        k: Number of top recommendations to consider

    Returns:
        Precision@K value
    """
    if k == 0:
        return 0.0

    # Get the top k recommendations
    top_k = recommendations[:k]

    # Count how many of the top k recommendations are relevant
    relevant_count = 0
    for rec in top_k:
        # Handle both string and dictionary recommendations
        if isinstance(rec, str):
            rec_name = rec
        else:
            rec_name = rec.get('assessment_name', '')

        if rec_name in relevant_assessments:
            relevant_count += 1

    # Calculate precision
    precision = relevant_count / k

    return precision

def average_precision_at_k(recommendations: List[Any], relevant_assessments: List[str], k: int) -> float:
    """
    Calculate Average Precision@K for a single query.

    Args:
        recommendations: List of recommended assessments (can be strings or dictionaries)
        relevant_assessments: List of relevant assessment IDs
        k: Number of top recommendations to consider

    Returns:
        Average Precision@K value
    """
    if not relevant_assessments:
        return 0.0

    # Get the top k recommendations
    top_k = recommendations[:k]

    # Calculate precision at each position where a relevant item is found
    precisions = []
    relevant_count = 0

    for i, rec in enumerate(top_k):
        # Handle both string and dictionary recommendations
        if isinstance(rec, str):
            rec_name = rec
        else:
            rec_name = rec.get('assessment_name', '')

        if rec_name in relevant_assessments:
            relevant_count += 1
            precision_at_i = relevant_count / (i + 1)
            precisions.append(precision_at_i)

    # Calculate average precision
    if precisions:
        ap = sum(precisions) / min(k, len(relevant_assessments))
    else:
        ap = 0.0

    return ap

def mean_recall_at_k(all_recommendations: List[List[Any]],
                     all_relevant_assessments: List[List[str]],
                     k: int) -> float:
    """
    Calculate Mean Recall@K across all queries.

    Args:
        all_recommendations: List of recommendation lists, one for each query
        all_relevant_assessments: List of relevant assessment lists, one for each query
        k: Number of top recommendations to consider

    Returns:
        Mean Recall@K value
    """
    if not all_recommendations or not all_relevant_assessments:
        return 0.0

    recalls = []
    for recommendations, relevant_assessments in zip(all_recommendations, all_relevant_assessments):
        recall = recall_at_k(recommendations, relevant_assessments, k)
        recalls.append(recall)

    mean_recall = sum(recalls) / len(recalls)
    return mean_recall

def mean_average_precision_at_k(all_recommendations: List[List[Any]],
                               all_relevant_assessments: List[List[str]],
                               k: int) -> float:
    """
    Calculate Mean Average Precision@K across all queries.

    Args:
        all_recommendations: List of recommendation lists, one for each query
        all_relevant_assessments: List of relevant assessment lists, one for each query
        k: Number of top recommendations to consider

    Returns:
        Mean Average Precision@K value
    """
    if not all_recommendations or not all_relevant_assessments:
        return 0.0

    aps = []
    for recommendations, relevant_assessments in zip(all_recommendations, all_relevant_assessments):
        ap = average_precision_at_k(recommendations, relevant_assessments, k)
        aps.append(ap)

    map_k = sum(aps) / len(aps)
    return map_k

def evaluate_recommendation_system(all_recommendations: List[List[Any]],
                                   all_relevant_assessments: List[List[str]],
                                   k_values: List[int] = [5, 10, 20]) -> Dict[str, Dict[int, float]]:
    """
    Evaluate a recommendation system using multiple metrics at different K values.

    Args:
        all_recommendations: List of recommendation lists, one for each query
        all_relevant_assessments: List of relevant assessment lists, one for each query
        k_values: List of K values to evaluate

    Returns:
        Dictionary containing evaluation metrics
    """
    results = {
        "recall_at_k": {},
        "map_at_k": {}
    }

    for k in k_values:
        recall = mean_recall_at_k(all_recommendations, all_relevant_assessments, k)
        map_k = mean_average_precision_at_k(all_recommendations, all_relevant_assessments, k)

        results["recall_at_k"][k] = recall
        results["map_at_k"][k] = map_k

    return results