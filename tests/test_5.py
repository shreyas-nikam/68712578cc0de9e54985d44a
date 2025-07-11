import pytest
import pandas as pd
from definition_1d1afbcbb99f4f5b83f34517f6327d99 import assess_homogeneity

@pytest.fixture
def sample_data():
    data = pd.DataFrame({
        'uom_id': [1, 2, 3, 4, 5, 6],
        'loss_amount': [100, 150, 200, 300, 350, 400],
        'grouped_uom_id': [1, 1, 2, 2, 2, 3]
    })
    return data

def test_assess_homogeneity_empty_data():
    data = pd.DataFrame({'uom_id': [], 'loss_amount': [], 'grouped_uom_id': []})
    result = assess_homogeneity(data)
    assert isinstance(result, dict)
    assert len(result) == 0

def test_assess_homogeneity_single_group(sample_data):
    data = sample_data.copy()
    data['grouped_uom_id'] = 1
    result = assess_homogeneity(data)
    assert isinstance(result, dict)
    assert len(result) == 1
    assert 1 in result

def test_assess_homogeneity_multiple_groups(sample_data):
    result = assess_homogeneity(sample_data)
    assert isinstance(result, dict)
    assert len(result) == 3
    assert 1 in result
    assert 2 in result
    assert 3 in result

def test_assess_homogeneity_non_numeric_loss_amount():
    data = pd.DataFrame({
        'uom_id': [1, 2],
        'loss_amount': ['a', 'b'],
        'grouped_uom_id': [1, 1]
    })
    with pytest.raises(TypeError):
        assess_homogeneity(data)

def test_assess_homogeneity_missing_grouped_uom_id(sample_data):
    data = sample_data.drop('grouped_uom_id', axis=1)
    with pytest.raises(KeyError):
         assess_homogeneity(data)

