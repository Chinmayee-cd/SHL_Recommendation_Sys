from typing import List, Dict, Any
import numpy as np

def calculate_recall_at_k(relevant_items: List[str], recommended_items: List[str], k: int) -> float:
    """
    Calculate Recall@K metric.
    
    Args:
        relevant_items: List of relevant item IDs
        recommended_items: List of recommended item IDs
        k: Number of top recommendations to consider
        
    Returns:
        float: Recall@K score
    """
    if not relevant_items:
        return 0.0
        
    top_k_recommendations = recommended_items[:k]
    relevant_in_top_k = sum(1 for item in top_k_recommendations if item in relevant_items)
    
    return relevant_in_top_k / len(relevant_items)

def calculate_precision_at_k(relevant_items: List[str], recommended_items: List[str], k: int) -> float:
    """
    Calculate Precision@K metric.
    
    Args:
        relevant_items: List of relevant item IDs
        recommended_items: List of recommended item IDs
        k: Number of top recommendations to consider
        
    Returns:
        float: Precision@K score
    """
    if not recommended_items[:k]:
        return 0.0
        
    top_k_recommendations = recommended_items[:k]
    relevant_in_top_k = sum(1 for item in top_k_recommendations if item in relevant_items)
    
    return relevant_in_top_k / k

def calculate_map_at_k(queries: List[Dict[str, Any]], k: int) -> float:
    """
    Calculate Mean Average Precision@K (MAP@K) metric.
    
    Args:
        queries: List of dictionaries containing query results
                Each dict should have 'relevant_items' and 'recommended_items' keys
        k: Number of top recommendations to consider
        
    Returns:
        float: MAP@K score
    """
    if not queries:
        return 0.0
        
    ap_scores = []
    
    for query in queries:
        relevant_items = query['relevant_items']
        recommended_items = query['recommended_items']
        
        if not relevant_items:
            continue
            
        # Calculate precision at each position where we find a relevant item
        precisions = []
        relevant_count = 0
        
        for i, item in enumerate(recommended_items[:k]):
            if item in relevant_items:
                relevant_count += 1
                precision = relevant_count / (i + 1)
                precisions.append(precision)
                
        # Calculate average precision for this query
        if precisions:
            ap = sum(precisions) / len(relevant_items)
            ap_scores.append(ap)
            
    return np.mean(ap_scores) if ap_scores else 0.0

def evaluate_recommendations(
    test_queries: List[Dict[str, Any]],
    k: int = 3
) -> Dict[str, float]:
    """
    Evaluate recommendation system using multiple metrics.
    
    Args:
        test_queries: List of test queries with ground truth
        k: Number of top recommendations to consider
        
    Returns:
        Dict containing evaluation metrics
    """
    recall_scores = []
    map_score = calculate_map_at_k(test_queries, k)
    
    for query in test_queries:
        recall = calculate_recall_at_k(
            query['relevant_items'],
            query['recommended_items'],
            k
        )
        recall_scores.append(recall)
        
    mean_recall = np.mean(recall_scores)
    
    return {
        f"recall@{k}": mean_recall,
        f"map@{k}": map_score
    } 