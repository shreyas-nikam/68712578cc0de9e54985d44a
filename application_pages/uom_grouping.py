
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
    # ---------- Page title ----------
    st.header("UoM Grouping Strategy")

    st.markdown(r"""
    **Purpose of this page**

    In operational‑risk models we often collect loss data under many *Units of Measure (UoMs)*.  
    Unfortunately, some UoMs have very few observations, while others mix several risk drivers.
    Grouping them can reduce noise and create cleaner, more stable loss distributions.

    Below you will:

    1. Select a *grouping strategy* (business logic, statistical clustering, or a hybrid).
    2. Inspect how your choice changes the UoM labels.
    3. Visualize similarity across raw UoMs with a Kolmogorov–Smirnov (KS) distance heat‑map.
    """)

    # ---------- Guard clause ----------
    if 'synthetic_data' not in st.session_state:
        st.info("Please generate synthetic data on the **Data Generation** page first.")
        return

    synthetic_data = st.session_state['synthetic_data'].copy()  # safety copy

    # ---------- Sidebar controls ----------
    st.sidebar.subheader("Step 1 – Choose a grouping strategy")
    grouping_strategy = st.sidebar.radio(
        "Strategy",
        options=[
            "No Grouping (Raw UoMs)",
            "Business Knowledge Grouping",
            "Statistical Clustering (K‑means) (Coming Soon)",
            "Combined Approach (Coming Soon)"
        ],
        help="How should raw UoMs be merged into more homogeneous groups?"
    )

    grouped_data = synthetic_data.copy()  # default: no grouping

    # ---------- Strategy: none ----------
    if grouping_strategy == "No Grouping (Raw UoMs)":
        grouped_data['grouped_uom_id'] = grouped_data['uom_id']
        st.success("Showing raw UoMs with **no** grouping. "
                   "Use this as a baseline for comparison.")

    # ---------- Strategy: business rules ----------
    elif grouping_strategy == "Business Knowledge Grouping":
        st.sidebar.markdown("""
        **Step 2 – Pick event types to combine**

        When your domain experts know that certain loss events share a common root cause,
        you can force them into one bucket regardless of statistical distance.
        """)
        event_types_to_group = st.sidebar.multiselect(
            "Event types to merge",
            options=['Fraud', 'Error', 'System Failure'],
            default=['Fraud', 'Error']
        )

        grouped_data = group_uoms_by_business_knowledge(
            synthetic_data,
            event_types_to_group
        )

        st.info(
            f"Business override in action. "
            f"The selected event types **{', '.join(event_types_to_group)}** are now labelled "
            f"`grouped_uom_id = 9999` so they can be analysed as one unit."
        )

    # ---------- Strategy: future statistical clustering ----------
    elif grouping_strategy.startswith("Statistical Clustering"):
        st.sidebar.slider(
            "Desired number of clusters (K)",
            min_value=2,
            max_value=len(synthetic_data['uom_id'].unique()),
            value=3
        )
        st.warning(
            "Statistical clustering will group UoMs that *look* alike statistically "
            "using KS distance as the similarity metric. "
            "This feature is not yet implemented."
        )
        grouped_data['grouped_uom_id'] = grouped_data['uom_id']  # no change yet

    # ---------- Strategy: future combined approach ----------
    elif grouping_strategy.startswith("Combined Approach"):
        st.sidebar.checkbox(
            "Apply business override inside clustering",
            help="Example: halve the KS distance for predefined categories so they are more likely to cluster."
        )
        st.warning(
            "The combined approach will let you blend domain knowledge with clustering by "
            "adjusting distances before running K‑means. Not implemented yet."
        )

        st.markdown(r"""
        **Illustration of a distance adjustment**

        $$\tilde{d}_{ij} =
        \begin{cases}
        \frac{1}{2}\, d_{ij} & \text{if both units belong to the predefined DPA category} \\
        d_{ij} & \text{otherwise}
        \end{cases}$$

        Cutting the distance in half makes the algorithm treat these pairs as *closer*,
        increasing the chance they fall into the same cluster.
        """)
        grouped_data['grouped_uom_id'] = grouped_data['uom_id']  # no change yet

    # ---------- Show grouped data ----------
    st.subheader("Preview of grouped data")
    st.markdown("""
    The table below shows the first few rows after applying your chosen strategy.
    Use it to verify that IDs changed as expected.
    """)
    st.dataframe(grouped_data.head())

    st.markdown("""
    **Count of observations per `grouped_uom_id`**  
    A jump in the count for ID 9999 confirms that several raw UoMs were merged.
    """)
    st.write(grouped_data['grouped_uom_id'].value_counts().sort_index())

    st.session_state['grouped_data'] = grouped_data  # store result

    # ---------- KS distance heat‑map ----------
    st.subheader("Similarity between raw UoMs (KS distance)")
    st.markdown(r"""
    The **Kolmogorov–Smirnov distance** $d_{ij}$ measures the maximum vertical
    gap between the cumulative distribution functions of two loss samples.
    * Smaller values (darker squares) mean the two UoMs have similar loss behaviour.
    * Larger values (lighter squares) suggest the loss patterns differ.

    **How to read the heat‑map**

    * The matrix is symmetric.  
    * Zeros on the diagonal indicate each UoM compared with itself.  
    * Dark clusters imply candidates for grouping if you are following a data‑driven approach.
    """)
    try:
        ks_dist_matrix = create_ks_distance_matrix(synthetic_data)
        fig = px.imshow(
            ks_dist_matrix,
            text_auto=".2f",
            labels=dict(x="UoM ID", y="UoM ID", color="KS distance"),
            x=ks_dist_matrix.columns,
            y=ks_dist_matrix.index,
            color_continuous_scale=px.colors.sequential.Viridis_r
        )
        fig.update_layout(
            title_text="Kolmogorov–Smirnov Distance Matrix (raw UoMs)",
            font=dict(size=12)
        )
        fig.update_xaxes(side="top")
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Could not compute or display KS matrix: {e}")

if __name__ == "__main__":
    run_uom_grouping()
