
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Re-define calculate_ks_distance here because it's used by create_ks_distance_matrix
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

def group_uoms_by_business_knowledge(data, event_types_to_group):
    """Groups UoMs based on business rules (event types)."""
    data_copy = data.copy()  # Work on a copy to avoid modifying original data
    data_copy['grouped_uom_id'] = data_copy['uom_id']  # Initialize with original uom_id

    if event_types_to_group:
        mask = data_copy['event_type'].isin(event_types_to_group)
        if mask.any():  # Only group if there are matching event types
            # Use a consistent ID for the grouped UoM, e.g., a hash of sorted event types
            # Or simply assign a distinct, non-conflicting ID
            # For simplicity, let's just make them all group 9999 if selected
            data_copy.loc[mask, 'grouped_uom_id'] = 9999 # A distinct ID for combined group
    return data_copy

def create_ks_distance_matrix(data):
    """Creates a symmetric matrix of KS distances between all raw UoMs."""
    uom_ids = sorted(data['uom_id'].unique())
    num_uoms = len(uom_ids)
    ks_matrix = np.zeros((num_uoms, num_uoms))
    uom_losses = {uid: data[data['uom_id'] == uid]['loss_amount'].values for uid in uom_ids}

    for i in range(num_uoms):
        for j in range(i, num_uoms):
            uom_i_data = uom_losses[uom_ids[i]]
            uom_j_data = uom_losses[uom_ids[j]]
            distance = calculate_ks_distance(uom_i_data, uom_j_data)
            ks_matrix[i, j] = distance
            ks_matrix[j, i] = distance # Symmetric matrix
    return pd.DataFrame(ks_matrix, index=[f"UoM {uid}" for uid in uom_ids], columns=[f"UoM {uid}" for uid in uom_ids])


def run_uom_grouping():
    st.header("UoM Grouping Strategy")
    st.markdown("""
    Select a strategy to group the raw Units of Measure (UoMs) into potentially more homogenous units.
    The goal is to reduce internal variability within each group.
    """)

    if 'synthetic_data' not in st.session_state:
        st.info("Please generate synthetic data on the 'Data Generation' page first.")
        return

    synthetic_data = st.session_state['synthetic_data'].copy() # Work with a copy

    st.sidebar.subheader("UoM Grouping Strategy")
    grouping_strategy = st.sidebar.radio(
        "Strategy Selection",
        options=["No Grouping (Raw UoMs)", "Business Knowledge Grouping", "Statistical Clustering (K-means) (Future)", "Combined Approach (Future)"],
        help="Choose how raw UoMs should be grouped into homogenous units."
    )

    grouped_data = synthetic_data.copy() # Initialize with no grouping

    if grouping_strategy == "No Grouping (Raw UoMs)":
        grouped_data['grouped_uom_id'] = grouped_data['uom_id']
        st.info("Currently displaying raw UoMs without any grouping.")
    elif grouping_strategy == "Business Knowledge Grouping":
        event_types_to_group = st.sidebar.multiselect(
            "Event Types to Group",
            options=['Fraud', 'Error', 'System Failure'],
            default=['Fraud', 'Error'],
            help="Select event types to combine into a single grouped UoM, based on business rules."
        )
        grouped_data = group_uoms_by_business_knowledge(synthetic_data, event_types_to_group)
        st.info(f"Grouping based on business knowledge. Selected event types: {', '.join(event_types_to_group)}")
        if 9999 in grouped_data['grouped_uom_id'].unique():
            st.markdown(r"Note: Event types selected for grouping have been assigned to 'Group 9999'. Other UoMs retain their original IDs.")

    elif grouping_strategy == "Statistical Clustering (K-means) (Future)":
        st.sidebar.slider("Number of Clusters (K)", min_value=2, max_value=len(synthetic_data['uom_id'].unique()), value=3,
                            help="Specify the desired number of clusters for the K-means algorithm, based on KS distance.")
        st.warning("Statistical Clustering (K-means) is a future enhancement and not yet implemented. It would group UoMs based on KS distances.")
        grouped_data['grouped_uom_id'] = grouped_data['uom_id'] # Revert to no grouping for now
    elif grouping_strategy == "Combined Approach (Future)":
        st.sidebar.checkbox("Apply Business Override (e.g., specific event types)", help="Combine business knowledge with statistical clustering, e.g., by adjusting KS distances for specific business categories.")
        st.warning("Combined Approach is a future enhancement and not yet implemented. It would allow combining business rules with statistical clustering.")
        st.markdown(r"""
        For instance, a combined approach might adjust KS distances $\tilde{{d}}_{{ij}}$ as follows:
        $$ \tilde{{d}}_{{ij}} = \begin{{cases}} \frac{{1}}{{2}}d_{{ij}} & \text{{if units }} i \text{{ and }} j \text{{ are DPA}} \\ d_{{ij}} & \text{{otherwise}} \end{{cases}} $$
        """)
        grouped_data['grouped_uom_id'] = grouped_data['uom_id'] # Revert to no grouping for now

    st.subheader("Grouped Data Sample")
    st.dataframe(grouped_data.head())
    st.write("Counts of Grouped UoM IDs:")
    st.write(grouped_data['grouped_uom_id'].value_counts().sort_index())

    st.session_state['grouped_data'] = grouped_data # Store the (potentially) grouped data

    st.subheader("Kolmogorov-Smirnov Distance Matrix Between Raw UoMs")
    st.markdown("""
    This heatmap visualizes the Kolmogorov-Smirnov distances between all pairs of initial raw UoMs.
    A smaller distance (closer to 0, darker color) indicates greater similarity between the distributions of loss amounts for those UoMs.
    """)
    try:
        if not synthetic_data.empty:
            ks_dist_matrix = create_ks_distance_matrix(synthetic_data)
            fig = px.imshow(ks_dist_matrix,
                            text_auto=".2f",
                            labels=dict(x="UoM ID", y="UoM ID", color="KS Distance"),
                            x=ks_dist_matrix.columns,
                            y=ks_dist_matrix.index,
                            color_continuous_scale=px.colors.sequential.Viridis_r) # Reverse Viridis for darker=closer to 0
            fig.update_layout(title_text='Kolmogorov-Smirnov Distance Matrix Between Raw UoMs', font=dict(size=12))
            fig.update_xaxes(side="top")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No synthetic data available to compute KS distance matrix.")
    except Exception as e:
        st.error(f"Error computing or displaying KS distance matrix: {e}")

if __name__ == "__main__":
    run_uom_grouping()
