import numpy as np

def calculate_ks_distance(data1, data2):
    """Calculates the Kolmogorov-Smirnov distance between two datasets."""
    data1 = np.sort(data1)
    data2 = np.sort(data2)
    n1 = len(data1)
    n2 = len(data2)
    if n1 == 0 or n2 == 0:
        return 0.0  # Handle empty datasets
    d = 0.0
    i = 0
    j = 0
    while i < n1 and j < n2:
        if data1[i] <= data2[j]:
            cdf1 = (i + 1) / n1
            cdf2 = j / n2
            d = max(d, abs(cdf1 - cdf2))
            i += 1
        else:
            cdf1 = i / n1
            cdf2 = (j + 1) / n2
            d = max(d, abs(cdf1 - cdf2))
            j += 1
    while i < n1:
        cdf1 = (i + 1) / n1
        cdf2 = 1
        d = max(d, abs(cdf1 - cdf2))
        i += 1
    while j < n2:
        cdf1 = 1
        cdf2 = (j + 1) / n2
        d = max(d, abs(cdf1 - cdf2))
        j += 1
    return d

import pandas as pd
import numpy as np

def generate_synthetic_data(num_uoms, loss_events_per_uom, severity_mean_range, severity_std_range):
    """Generates synthetic operational loss data."""

    if severity_mean_range[0] > severity_mean_range[1] or any(x < 0 for x in severity_mean_range):
        raise ValueError("Invalid severity mean range.")

    if severity_std_range[0] > severity_std_range[1] or any(x < 0 for x in severity_std_range):
        raise ValueError("Invalid severity std range.")

    data = []
    for uom_id in range(num_uoms):
        for _ in range(loss_events_per_uom):
            mean = np.random.uniform(severity_mean_range[0], severity_mean_range[1])
            std = np.random.uniform(severity_std_range[0], severity_std_range[1])
            loss_amount = np.random.lognormal(mean, std)
            loss_date = pd.to_datetime('2023-01-01') + pd.to_timedelta(np.random.randint(0, 365), unit='D')
            event_type = np.random.choice(['Fraud', 'Error', 'System Failure'])
            business_line = np.random.choice(['Retail', 'Investment', 'Corporate'])
            data.append([uom_id, loss_amount, loss_date, event_type, business_line])

    df = pd.DataFrame(data, columns=['uom_id', 'loss_amount', 'loss_date', 'event_type', 'business_line'])
    return df

import pandas as pd

def group_uoms_by_business_knowledge(data, event_types_to_group):
    """Groups UoMs based on business rules (event types)."""

    data['grouped_uom_id'] = data['uom_id']  # Initialize with original uom_id

    if event_types_to_group:
        # Create a combined group ID for specified event types
        mask = data['event_type'].isin(event_types_to_group)
        if mask.any():  # Only group if there are matching event types
            group_id = hash(tuple(sorted(event_types_to_group)))  # Consistent ID based on event types
            data.loc[mask, 'grouped_uom_id'] = group_id

        # Ensure unique IDs for remaining ungrouped UoMs
        else:
            data['grouped_uom_id'] = data['uom_id']
    
    return data

import pandas as pd
from scipy.stats import kstest
import numpy as np

def assess_homogeneity(data):
    """Evaluates homogeneity within each grouped UoM using KS test.
    Args:
        data: DataFrame with uom_id, loss_amount, grouped_uom_id.
    Returns:
        Dictionary of homogeneity metrics for each grouped_uom_id.
    """
    if not isinstance(data, pd.DataFrame):
        raise TypeError("Input data must be a Pandas DataFrame.")

    if data.empty:
        return {}

    if 'grouped_uom_id' not in data.columns:
        raise KeyError("The 'grouped_uom_id' column is missing.")

    if 'loss_amount' not in data.columns:
        raise KeyError("The 'loss_amount' column is missing.")

    if not pd.api.types.is_numeric_dtype(data['loss_amount']):
        raise TypeError("The 'loss_amount' column must be numeric.")

    grouped_data = data.groupby('grouped_uom_id')['loss_amount'].apply(list)
    results = {}

    for group_id, losses in grouped_data.items():
        if len(losses) < 2:
            results[group_id] = np.nan  # Not enough data for KS test
            continue

        # Compare each group to a standard normal distribution
        ks_statistic, p_value = kstest(losses, 'norm', args=(np.mean(losses), np.std(losses)))
        results[group_id] = ks_statistic

    return results