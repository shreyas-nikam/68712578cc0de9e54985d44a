import pytest
import pandas as pd
from definition_803ad15182574b249f5ce4bafe009245 import group_uoms_combined_approach

@pytest.fixture
def sample_data():
    data = pd.DataFrame({
        'uom_id': [1, 2, 3, 4, 5, 6],
        'loss_amount': [100, 200, 150, 300, 250, 400],
        'event_type': ['Fraud', 'IT Failure', 'Fraud', 'Operational', 'IT Failure', 'Fraud']
    })
    return data

def test_group_uoms_combined_approach_empty_data(sample_data):
    empty_data = pd.DataFrame({'uom_id': [], 'loss_amount': [], 'event_type': []})
    event_types_to_group = ['Fraud']
    n_clusters = 2
    result = group_uoms_combined_approach(empty_data, event_types_to_group, n_clusters)
    assert isinstance(result, pd.DataFrame)
    assert 'grouped_uom_id' in result.columns

def test_group_uoms_combined_approach_no_event_types_to_group(sample_data):
    event_types_to_group = []
    n_clusters = 2
    result = group_uoms_combined_approach(sample_data, event_types_to_group, n_clusters)
    assert isinstance(result, pd.DataFrame)
    assert 'grouped_uom_id' in result.columns

def test_group_uoms_combined_approach_single_event_type(sample_data):
    event_types_to_group = ['Fraud']
    n_clusters = 2
    result = group_uoms_combined_approach(sample_data, event_types_to_group, n_clusters)
    assert isinstance(result, pd.DataFrame)
    assert 'grouped_uom_id' in result.columns

def test_group_uoms_combined_approach_multiple_event_types(sample_data):
    event_types_to_group = ['Fraud', 'IT Failure']
    n_clusters = 2
    result = group_uoms_combined_approach(sample_data, event_types_to_group, n_clusters)
    assert isinstance(result, pd.DataFrame)
    assert 'grouped_uom_id' in result.columns

def test_group_uoms_combined_approach_invalid_n_clusters(sample_data):
    event_types_to_group = ['Fraud']
    n_clusters = 0
    with pytest.raises(ValueError):
        group_uoms_combined_approach(sample_data, event_types_to_group, n_clusters)
