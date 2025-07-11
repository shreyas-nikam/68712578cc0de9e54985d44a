import pytest
import pandas as pd
from definition_a08be6ea7a0d49b6a54a75bddcb8664e import group_uoms_by_business_knowledge

@pytest.fixture
def sample_data():
    data = pd.DataFrame({
        'uom_id': [1, 2, 3, 4, 5],
        'event_type': ['Fraud', 'IT Failure', 'Fraud', 'Damage', 'IT Failure'],
        'business_line': ['Retail', 'Corporate', 'Retail', 'Retail', 'Corporate']
    })
    return data

def test_group_uoms_by_business_knowledge_empty_event_types(sample_data):
    result = group_uoms_by_business_knowledge(sample_data, [])
    assert 'grouped_uom_id' in result.columns
    assert result['grouped_uom_id'].nunique() == len(sample_data)  # No grouping

def test_group_uoms_by_business_knowledge_single_event_type(sample_data):
    result = group_uoms_by_business_knowledge(sample_data, ['Fraud'])
    assert 'grouped_uom_id' in result.columns
    assert result['grouped_uom_id'].nunique() == 4
    fraud_group = result[result['event_type'] == 'Fraud']['grouped_uom_id'].unique()
    assert len(fraud_group) == 1
    assert result[result['uom_id'].isin([1,3])]['grouped_uom_id'].iloc[0] == result[result['uom_id'].isin([1,3])]['grouped_uom_id'].iloc[1]


def test_group_uoms_by_business_knowledge_multiple_event_types(sample_data):
    result = group_uoms_by_business_knowledge(sample_data, ['Fraud', 'IT Failure'])
    assert 'grouped_uom_id' in result.columns
    assert result['grouped_uom_id'].nunique() == 2
    grouped_fraud_it = result[result['event_type'].isin(['Fraud', 'IT Failure'])]['grouped_uom_id'].unique()
    assert len(grouped_fraud_it) == 1

def test_group_uoms_by_business_knowledge_all_event_types(sample_data):
    event_types = sample_data['event_type'].unique().tolist()
    result = group_uoms_by_business_knowledge(sample_data, event_types)
    assert 'grouped_uom_id' in result.columns
    assert result['grouped_uom_id'].nunique() == 1

def test_group_uoms_by_business_knowledge_no_matching_event_types(sample_data):
    result = group_uoms_by_business_knowledge(sample_data, ['NonExistent'])
    assert 'grouped_uom_id' in result.columns
    assert result['grouped_uom_id'].nunique() == len(sample_data)
