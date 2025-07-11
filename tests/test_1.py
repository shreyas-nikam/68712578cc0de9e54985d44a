import pytest
import pandas as pd
import numpy as np
from definition_3c376f5b7ba641d8b9cc125720d7f8c7 import generate_synthetic_data

@pytest.fixture
def valid_severity_ranges():
    return (1, 5), (0.5, 1.5)  # Example mean and std ranges


def test_generate_synthetic_data_positive(valid_severity_ranges):
    num_uoms = 3
    loss_events_per_uom = 10
    severity_mean_range, severity_std_range = valid_severity_ranges
    df = generate_synthetic_data(num_uoms, loss_events_per_uom, severity_mean_range, severity_std_range)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == num_uoms * loss_events_per_uom
    assert all(col in df.columns for col in ['uom_id', 'loss_amount', 'loss_date', 'event_type', 'business_line'])


def test_generate_synthetic_data_zero_uoms(valid_severity_ranges):
    num_uoms = 0
    loss_events_per_uom = 10
    severity_mean_range, severity_std_range = valid_severity_ranges
    df = generate_synthetic_data(num_uoms, loss_events_per_uom, severity_mean_range, severity_std_range)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 0

def test_generate_synthetic_data_zero_events(valid_severity_ranges):
    num_uoms = 3
    loss_events_per_uom = 0
    severity_mean_range, severity_std_range = valid_severity_ranges
    df = generate_synthetic_data(num_uoms, loss_events_per_uom, severity_mean_range, severity_std_range)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 0


def test_generate_synthetic_data_invalid_severity_range():
    num_uoms = 3
    loss_events_per_uom = 10
    severity_mean_range = (5, 1) # Invalid range
    severity_std_range = (0.5, 1.5)
    with pytest.raises(ValueError):
        generate_synthetic_data(num_uoms, loss_events_per_uom, severity_mean_range, severity_std_range)

def test_generate_synthetic_data_negative_severity_range():
    num_uoms = 3
    loss_events_per_uom = 10
    severity_mean_range = (-1, 5)
    severity_std_range = (0.5, 1.5)
    with pytest.raises(ValueError):
        generate_synthetic_data(num_uoms, loss_events_per_uom, severity_mean_range, severity_std_range)
