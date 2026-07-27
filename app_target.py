def calculate_project_metrics(scores):
    # ⚠️ INTENTIONAL BUG: This crashes with a ZeroDivisionError if scores list is empty
    return sum(scores) / len(scores)
