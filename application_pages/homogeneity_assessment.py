
import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import kstest
import plotly.graph_objects as go
import plotly.express as px

# Re-define calculate_ks_distance here because it's used by create_ks_distance_matrix and assess_homogeneity
def calculate_ks_distance(data1, data2):
    """Calculates the Kolmogorov-Smirnov distance (D-statistic) between two datasets."""
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
        ks_statistic, p_value = kstest(losses, 'norm', args=(np.mean(losses), np.std(losses)))
        results[group_id] = ks_statistic
    return results

def plot_cdfs(data, grouped_uom_id_col='grouped_uom_id'):
    """Plots Empirical CDFs of losses for each raw UoM within its grouped UoM."""
    fig = go.Figure()
    unique_grouped_uoms = data[grouped_uom_id_col].unique()

    # Define a color-blind-friendly palette
    colors = px.colors.qualitative.Plotly  # Or other suitable palette like D3, Safe, Pastel

    for i, grouped_id in enumerate(unique_grouped_uoms):
        group_data = data[data[grouped_uom_id_col] == grouped_id]
        unique_raw_uoms_in_group = sorted(group_data['uom_id'].unique())

        for j, raw_uom_id in enumerate(unique_raw_uoms_in_group):
            losses = group_data[group_data['uom_id'] == raw_uom_id]['loss_amount'].values
            if len(losses) > 1:
                sorted_losses = np.sort(losses)
                y_cdf = np.arange(1, len(sorted_losses) + 1) / len(sorted_losses)
                # Assign a distinct color for each raw UoM within the group, cycling through colors
                # Use a combination of group_id and raw_uom_id for consistent naming
                trace_color = colors[(i * len(unique_raw_uoms_in_group) + j) % len(colors)]
                fig.add_trace(go.Scatter(x=sorted_losses, y=y_cdf,
                                          mode='lines',
                                          name=f'Group {grouped_id} - Raw UoM {raw_uom_id}',
                                          line=dict(color=trace_color),
                                          hovertemplate=f"Raw UoM: {raw_uom_id}<br>Loss Amount: %{{x}}<br>CDF: %{{y:.2f}}<extra></extra>"))

    fig.update_layout(title='Empirical CDFs of Losses per Grouped UoM',
                      xaxis_title='Loss Amount',
                      yaxis_title='CDF',
                      legend_title='UoMs',
                      hovermode='x unified',
                      font=dict(size=12))  # Ensure font size >= 12 pt
    return fig
def run_homogeneity_assessment():
    # ---------- Page title ----------
    st.header("Homogeneity Assessment")

    st.markdown(r"""
    **What does “homogeneity” mean here?**

    After grouping Units of Measure (UoMs) you want every loss inside a group to
    “look” as if it came from the same distribution.  
    We check this in two complementary ways:

    * **Kolmogorov–Smirnov (KS) test** – a formal test that compares your data with a normal reference built from the sample mean and standard deviation.  
      A smaller KS statistic hints the group behaves like one coherent population.
    * **Empirical Cumulative Distribution Functions (ECDFs)** – visual evidence.  
      If the ECDFs of raw UoMs in the same group overlap closely, the grouping is working.

    Use the table first for a quick numeric check, then scan the ECDF plot for patterns that numbers alone may miss.
    """)

    # ---------- Guard clause ----------
    if 'grouped_data' not in st.session_state:
        st.info(
            "Please generate synthetic data on the **Data Generation** page and group UoMs "
            "on the **UoM Grouping** page first."
        )
        return

    grouped_data = st.session_state['grouped_data']

    # ---------- KS table ----------
    st.subheader("1. KS statistics by group")
    st.markdown(r"""
    *Each row shows the KS statistic for one `grouped_uom_id`.*

    * **Rule of thumb:**  
      KS < 0.1 → very homogeneous  
      0.1 ≤ KS < 0.2 → acceptable  
      KS ≥ 0.2 → investigate outliers or consider re‑grouping
    """)
    try:
        homogeneity_results = assess_homogeneity(grouped_data)
        if homogeneity_results:
            ks_df = (
                pd.DataFrame.from_dict(
                    homogeneity_results,
                    orient="index",
                    columns=["KS statistic"]
                )
                .sort_index()
            )
            st.dataframe(ks_df)
        else:
            st.info(
                "Not enough observations in some groups. "
                "Each group must have at least two loss events for the KS test."
            )
    except Exception as e:
        st.error(f"Error during homogeneity assessment: {e}")

    # ---------- ECDF plot ----------
    st.subheader("2. Overlay of ECDFs inside each group")
    st.markdown(r"""
    *How to read this plot*

    * Lines of the **same colour family** belong to the same `grouped_uom_id`.
    * Tight, overlapping lines → raw UoMs share similar loss patterns.  
    * Widely separated lines → the group may still mix distinct risks.

    Hover to see exact UoM and CDF values.
    """)
    try:
        fig = plot_cdfs(grouped_data)
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error plotting ECDFs: {e}")

if __name__ == "__main__":
    run_homogeneity_assessment()
