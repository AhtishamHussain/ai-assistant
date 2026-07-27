from app_target import calculate_project_metrics

def test_metrics_empty_list():
    # This intentionally triggers the division-by-zero bug
    result = calculate_project_metrics([])
    assert result == 0
