"""Synthetic example for static inspection, not an executed experiment."""

def build_index(records):
    return [{"question": r["question"], "text": r["gold_answer"]} for r in records]

def reported_score(seed_scores):
    # The manuscript labels this quantity as the mean.
    return max(seed_scores)
