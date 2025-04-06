# SHL Assessment Recommender Evaluation

This document explains how to evaluate the performance of the SHL Assessment Recommender using standard information retrieval metrics.

## Evaluation Metrics

The evaluation framework implements two key metrics:

1. **Mean Recall@K**: Measures how many of the relevant assessments were retrieved in the top K recommendations, averaged across all test queries.

   ```
   Recall@K = Number of relevant assessments in top K / Total relevant assessments for the query
   Mean Recall@K = (1/N) * Σ(Recall@K_i) for i=1 to N
   ```

   where N is the total number of test queries.

2. **Mean Average Precision@K (MAP@K)**: Evaluates both the relevance and ranking order of retrieved assessments by calculating Precision@k at each relevant result and averaging it over all queries.

   ```
   AP@K = (1/min(K,R)) * Σ(P(k) * rel(k)) for k=1 to min(K,R)
   MAP@K = (1/N) * Σ(AP@K_i) for i=1 to N
   ```

   where:

   - R = total relevant assessments for the query
   - P(k) = precision at position k
   - rel(k) = 1 if the result at position k is relevant, otherwise 0
   - N = total number of test queries

## How to Run the Evaluation

1. Make sure your SHL Assessment Recommender API is running on `http://localhost:8000`.

2. Prepare your test queries in a JSON file with the following format:

   ```json
   [
     {
       "query": "Your test query text",
       "relevant_assessments": ["assessment_id1", "assessment_id2", ...]
     },
     ...
   ]
   ```

3. Run the evaluation script:

   ```
   python evaluate_recommender.py
   ```

4. The script will:
   - Process each test query through your recommendation API
   - Calculate Recall@K and MAP@K for different K values (default: 5, 10, 20)
   - Print the results to the console
   - Save the detailed results to `evaluation_results.json`

## Interpreting the Results

- Higher Mean Recall@K values indicate that your system is retrieving more of the relevant assessments in the top K recommendations.
- Higher MAP@K values indicate that your system is not only retrieving relevant assessments but also ranking them higher in the results.

## Customizing the Evaluation

You can modify the following parameters in the evaluation script:

- `k_values`: Change the K values used for evaluation
- Test queries: Update the `test_queries.json` file with your own test cases
- API endpoint: Modify the `get_recommendations` function if your API is hosted elsewhere

## Example Results

```
Evaluation Results:
==================

K = 5:
  Mean Recall@K: 0.6000
  MAP@K: 0.4500

K = 10:
  Mean Recall@K: 0.8000
  MAP@K: 0.5500

K = 20:
  Mean Recall@K: 0.9000
  MAP@K: 0.6000
```

These results would indicate that:

- At K=5, the system retrieves 60% of relevant assessments on average
- At K=10, the system retrieves 80% of relevant assessments on average
- At K=20, the system retrieves 90% of relevant assessments on average

The MAP@K values show how well the system ranks the relevant assessments within the top K results.
