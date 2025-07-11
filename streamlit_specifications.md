
# Streamlit Application Requirements Specification

## 1. Application Overview

The "UoM Homogeneity & Clustering Explorer" Streamlit application aims to provide an interactive platform for users to understand and experiment with the critical initial step in operational risk modeling: defining appropriate Units of Measure (UoMs) and grouping diverse operational risks into homogenous units. It allows users to generate synthetic operational loss data and apply different clustering and grouping strategies, observing their impact on data homogeneity.

**Objectives:**
*   To enable users to generate synthetic operational loss data with customizable characteristics.
*   To provide interactive controls for selecting and applying UoM grouping strategies, including business knowledge-based grouping and statistical clustering.
*   To visualize the statistical homogeneity of grouped UoMs using the Kolmogorov-Smirnov (KS) test and empirical Cumulative Distribution Functions (CDFs).
*   To demonstrate the impact of UoM definition on data homogeneity, aligning with concepts from the PRMIA Operational Risk Manager Handbook [1].
*   To highlight the trade-offs between practical grouping rules and statistical homogeneity.

## 2. User Interface Requirements

### Layout and Navigation Structure
The application will follow a standard Streamlit layout:
*   **Main Content Area:** Will display the application overview, generated data, homogeneity assessment results, and visualizations.
*   **Sidebar:** Will house all input widgets and controls for data generation parameters and UoM grouping strategy selection.
*   **Sections:** The main content will be logically divided into "Data Generation," "UoM Grouping Strategy," "Homogeneity Assessment," and "Visualizations."

### Input Widgets and Controls

All input widgets will be placed in the sidebar. Each control will have inline help text or tooltips as described in the user requirements.

*   **Data Generation Parameters (under a section like "Synthetic Data Generation"):**
    *   **Number of Raw UoMs:** `st.sidebar.slider` or `st.sidebar.number_input` (e.g., 2 to 20, default 5).
        *   *Tooltip/Help Text:* "Number of initial 'raw' Units of Measure to simulate loss data for."
    *   **Loss Events per UoM:** `st.sidebar.slider` or `st.sidebar.number_input` (e.g., 10 to 1000, default 100).
        *   *Tooltip/Help Text:* "Number of loss events to generate for each raw UoM."
    *   **Severity Mean Range (Log-normal $\mu$):** `st.sidebar.slider` with two handles (e.g., (1, 10), default (5, 7)).
        *   *Tooltip/Help Text:* "Range for the mean parameter ($\mu$) of the underlying normal distribution for log-normal loss severity. Controls the average loss amount."
    *   **Severity Std Dev Range (Log-normal $\sigma$):** `st.sidebar.slider` with two handles (e.g., (0.1, 5.0), default (1.0, 2.0)).
        *   *Tooltip/Help Text:* "Range for the standard deviation parameter ($\sigma$) of the underlying normal distribution for log-normal loss severity. Controls the dispersion of loss amounts."

*   **UoM Grouping Strategy Selection (under a section like "UoM Grouping Strategy"):**
    *   **Strategy Selection:** `st.sidebar.radio` or `st.sidebar.selectbox` with options:
        *   "No Grouping (Raw UoMs)"
        *   "Business Knowledge Grouping"
        *   "Statistical Clustering (K-means)" (Future Enhancement - requires additional code)
        *   "Combined Approach" (Future Enhancement - requires additional code)
        *   *Tooltip/Help Text:* "Choose how raw UoMs should be grouped into homogenous units."

    *   **If "Business Knowledge Grouping" is selected:**
        *   **Event Types to Group:** `st.sidebar.multiselect` (options: 'Fraud', 'Error', 'System Failure').
            *   *Tooltip/Help Text:* "Select event types to combine into a single grouped UoM, based on business rules."

    *   **If "Statistical Clustering (K-means)" is selected (Future Enhancement):**
        *   **Number of Clusters (K):** `st.sidebar.slider` or `st.sidebar.number_input` (e.g., 2 to `num_uoms`, default 3).
            *   *Tooltip/Help Text:* "Specify the desired number of clusters for the K-means algorithm, based on KS distance."

    *   **If "Combined Approach" is selected (Future Enhancement):**
        *   (Specific controls for defining business knowledge overrides or weight adjustments for statistical clustering, e.g., checkboxes for specific groupings like 'Damage to Physical Assets' to adjust KS distances.)
            *   *Tooltip/Help Text:* "Combine business knowledge with statistical clustering, e.g., by adjusting KS distances for specific business categories."

### Visualization Components

*   **Data Table:** Display of the `synthetic_data.head()` and counts of original and grouped UoM IDs. `st.dataframe` or `st.table`.
*   **Homogeneity Assessment Table:** Display of results from `assess_homogeneity` (Grouped UoM ID, KS Statistic). `st.dataframe` or `st.table`.
*   **Distance Matrix/Heatmap:**
    *   A heatmap visualizing the Kolmogorov-Smirnov distances between all initial raw UoMs.
    *   `plotly.express.imshow` or similar for interactivity, color-blind-friendly palette.
    *   *Title:* "Kolmogorov-Smirnov Distance Matrix Between Raw UoMs"
    *   *Axis Labels:* Labeled with "UoM ID" on both axes.
    *   *Interactivity:* Tooltips showing exact distance on hover.
*   **Homogeneity Visualization (CDFs):**
    *   Line plots displaying the Empirical Cumulative Distribution Functions (ECDFs) of the underlying raw UoMs for each *resulting grouped UoM*.
    *   `plotly.graph_objects.Figure` for interactivity.
    *   *Title:* "Empirical CDFs of Losses per Grouped UoM"
    *   *Axis Labels:* "Loss Amount" (X-axis), "CDF" (Y-axis).
    *   *Legends:* Clear legends indicating "Group ID - Raw UoM ID".
    *   *Interactivity:* Hover details showing raw UoM, loss amount, and CDF value.
    *   *Color Palette:* Adopt a color-blind-friendly palette.

### Interactive Elements and Feedback Mechanisms
*   All input changes will trigger automatic re-execution of the relevant analysis and updates to displayed data and visualizations, providing a responsive user experience.
*   Informative `st.info` or `st.warning` messages for conditions like insufficient data for KS tests.
*   Error messages (e.g., from `ValueError` in `generate_synthetic_data`) will be displayed using `st.error`.

## 3. Additional Requirements

*   **Real-time Updates and Responsiveness:** The Streamlit framework inherently supports real-time updates. Changes to any input widget will automatically re-run the relevant parts of the script and update the displayed output immediately.
*   **Annotation and Tooltip Specifications:**
    *   **Input Widgets:** As specified in Section 2.2, all input widgets will have descriptive tooltips or inline help text to guide the user.
    *   **Charts/Graphs:** All plots will have clear titles, labeled axes, and legends as per visualization requirements. Hover tooltips will provide detailed data points.
    *   **Explanations:** Markdown text will be used to explain the meaning of KS statistics (e.g., "A lower KS statistic (closer to 0) indicates greater homogeneity/similarity to the reference distribution.").

## 4. Notebook Content and Code Requirements

This section details the Python functions extracted from the Jupyter notebook and their integration into the Streamlit application. Theoretical explanations and formulas from the notebook will be presented as Streamlit markdown (`st.markdown`) or LaTeX (`st.latex`) components in the main application view to provide context and learning outcomes.

### 4.1. Core Functions

#### `calculate_ks_distance` Function
*   **Purpose:** Calculates the Kolmogorov-Smirnov (KS) D-statistic, which quantifies the maximum absolute difference between the empirical cumulative distribution functions (ECDFs) of two datasets. A smaller distance indicates greater similarity between distributions.
*   **Relevant LaTeX/Mathematical Content:**
    The KS D-statistic ($D$) between two empirical distributions $F_n(x)$ and $F(x)$ is defined as:
    $$ D = \sup_x |F_n(x) - F(x)| $$
    The handbook also references a scaled version for distance $d_{ij}$ between two UoMs $i$ and $j$ with sample sizes $n_i$ and $n_j$ and empirical CDFs $F_i(x)$ and $F_j(x)$:
    $$ \displaystyle d_{ij}=\frac{n_i n_j}{n_i+n_j}\sup_X |F_i(x)-F_j(x)| $$
    The Python function below computes the unscaled $D$-statistic.
*   **Extracted Code:**
    ```python
    import numpy as np

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
    ```
*   **Streamlit Integration:**
    This function will be used internally to compute the distance matrix for visualization and for any future statistical clustering implementation. It will not have direct user interaction, but its results will underpin interactive visualizations (e.g., heatmap).

#### `generate_synthetic_data` Function
*   **Purpose:** Creates a Pandas DataFrame of synthetic operational loss events, mimicking real-world diversity in frequency and severity characteristics across different 'raw' UoMs, event types, and business lines. Loss amounts are drawn from a log-normal distribution.
*   **Relevant LaTeX/Mathematical Content:**
    The probability density function of the log-normal distribution is:
    $$ f(x; \mu, \sigma) = \frac{1}{x\sigma\sqrt{2\pi}} e^{-\frac{(\ln x - \mu)^2}{2\sigma^2}} $$
    The mean ($E[X]$) and standard deviation ($SD[X]$) of the log-normal distribution, based on the parameters $\mu$ (mean of the logarithm) and $\sigma$ (standard deviation of the logarithm) passed to `np.random.lognormal`, are:
    $$ E[X] = e^{\mu + \frac{\sigma^2}{2}} $$
    $$ SD[X] = \sqrt{(e^{\sigma^2}-1)e^{2\mu+\sigma^2}} $$
*   **Extracted Code:**
    ```python
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
    ```
*   **Streamlit Integration:**
    This function will be called whenever the user adjusts parameters in the "Synthetic Data Generation" section of the sidebar. The returned DataFrame will be stored in `st.session_state` and displayed using `st.dataframe`. The number of unique UoM IDs and their counts will also be displayed using `st.write` and `value_counts()`.

#### `group_uoms_by_business_knowledge` Function
*   **Purpose:** Groups raw UoMs based on predefined business rules (e.g., combining specific event types) by assigning a common `grouped_uom_id`.
*   **Relevant LaTeX/Mathematical Content:** None directly associated with this function's logic.
*   **Extracted Code:**
    ```python
    import pandas as pd

    def group_uoms_by_business_knowledge(data, event_types_to_group):
        """Groups UoMs based on business rules (event types)."""
        data_copy = data.copy()  # Work on a copy to avoid modifying original data
        data_copy['grouped_uom_id'] = data_copy['uom_id']  # Initialize with original uom_id

        if event_types_to_group:
            mask = data_copy['event_type'].isin(event_types_to_group)
            if mask.any():  # Only group if there are matching event types
                group_id = hash(tuple(sorted(event_types_to_group)))  # Consistent ID based on event types
                data_copy.loc[mask, 'grouped_uom_id'] = group_id
        return data_copy
    ```
*   **Streamlit Integration:**
    This function will be called when "Business Knowledge Grouping" is selected and `event_types_to_group` are chosen by the user in the sidebar. The resulting DataFrame with the `grouped_uom_id` column will then be used for homogeneity assessment and visualization.

#### `assess_homogeneity` Function
*   **Purpose:** Evaluates the homogeneity within each `grouped_uom_id` by performing a Kolmogorov-Smirnov (KS) test, comparing the empirical distribution of loss amounts in each group to a fitted normal distribution.
*   **Relevant LaTeX/Mathematical Content:**
    The KS D-statistic ($D$), as returned by `scipy.stats.kstest`, is defined as:
    $$ D = \sup_x |F_n(x) - F(x)| $$
    Where $F_n(x)$ is the empirical cumulative distribution function of the sample and $F(x)$ is the cumulative distribution function of the theoretical distribution (here, a normal distribution parameterized by the sample's mean and standard deviation). A smaller $D$ value indicates a better fit to the theoretical distribution.
*   **Extracted Code:**
    ```python
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
    ```
*   **Streamlit Integration:**
    This function will be called after any grouping strategy is applied. The results, a dictionary of KS statistics per grouped UoM, will be displayed in a table (`st.dataframe`) and referenced in the homogeneity visualizations.

### 4.2. Visualization Helper Functions (Derived from Requirements, Not Explicitly in Notebook)

#### `create_ks_distance_matrix` Function
*   **Purpose:** Computes a symmetric matrix of Kolmogorov-Smirnov distances between all pairs of initial raw UoMs. This matrix forms the basis for the KS distance heatmap.
*   **Relevant LaTeX/Mathematical Content:** Relies on the $D$-statistic definition from `calculate_ks_distance`.
*   **Extracted Code:**
    ```python
    # Requires calculate_ks_distance function
    import pandas as pd
    import numpy as np

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
                # Use the custom calculate_ks_distance
                distance = calculate_ks_distance(uom_i_data, uom_j_data)
                ks_matrix[i, j] = distance
                ks_matrix[j, i] = distance # Symmetric matrix
        return pd.DataFrame(ks_matrix, index=[f"UoM {uid}" for uid in uom_ids], columns=[f"UoM {uid}" for uid in uom_ids])
    ```
*   **Streamlit Integration:**
    This function will be called after synthetic data generation. The resulting DataFrame will be passed to `plotly.express.imshow` or similar to display the interactive heatmap in the main content area.

#### `plot_cdfs` Function
*   **Purpose:** Generates a Plotly figure showing the Empirical Cumulative Distribution Functions (ECDFs) for the loss amounts of each raw UoM within its assigned grouped UoM.
*   **Relevant LaTeX/Mathematical Content:** None directly, it's a visualization of empirical CDFs.
*   **Extracted Code:**
    ```python
    import plotly.graph_objects as go
    import numpy as np
    import pandas as pd # Ensure pandas is imported for DataFrame operations

    def plot_cdfs(data, grouped_uom_id_col='grouped_uom_id'):
        """Plots Empirical CDFs of losses for each raw UoM within its grouped UoM."""
        fig = go.Figure()
        unique_grouped_uoms = data[grouped_uom_id_col].unique()
        
        # Define a color-blind-friendly palette
        colors = px.colors.qualitative.Plotly # Or other suitable palette like D3, Safe, Pastel

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
                          font=dict(size=12)) # Ensure font size >= 12 pt
        return fig
    ```
*   **Streamlit Integration:**
    This function will be called after any grouping strategy is applied. The returned Plotly figure will be displayed using `st.plotly_chart` in the main content area.

### 4.3. Future Enhancements / Requires Additional Implementation

The Jupyter notebook outlines certain features that are described conceptually but do not include direct Python code for their implementation. These will be noted in the Streamlit application as future enhancements or components requiring additional development.

*   **Statistical Clustering (K-means):**
    *   **Description from Notebook:** "Apply clustering algorithms (e.g., K-means) to group UoMs based on the statistical similarity of their severity distributions. The primary distance metric used will be the Kolmogorov-Smirnov distance... Users can specify the number of clusters."
    *   **Implementation Requirement:** This would require implementing K-means clustering (e.g., using `sklearn.cluster.KMeans`) and feeding it a precomputed distance matrix (from `create_ks_distance_matrix`) rather than raw feature data. This is a non-trivial addition not directly present in the provided notebook code.

*   **Combined Approach (Statistical Clustering with Business Knowledge Override):**
    *   **Description from Notebook:** "Apply a statistical clustering method with a 'business knowledge' override or weight adjustment (e.g., reducing the Kolmogorov-Smirnov distance by half for specific predefined groupings like 'Damage to Physical Assets' as suggested in the handbook [1, p. 15])."
    *   **Relevant LaTeX/Mathematical Content:**
        $$ \tilde{d}_{ij} = \begin{cases} \frac{1}{2}d_{ij} & \text{if units } i \text{ and } j \text{ are DPA} \\ d_{ij} & \text{otherwise} \end{cases} $$
    *   **Implementation Requirement:** This would involve modifying the `create_ks_distance_matrix` function to apply the distance adjustment based on user input (e.g., selected `event_types`) *before* performing statistical clustering. This also depends on the implementation of statistical clustering.

### 4.4. General Imports and Setup for Streamlit Application

The Streamlit application will require the following imports at the top of its script:

```python
import streamlit as st
import numpy as np
import pandas as pd
from scipy.stats import kstest
import plotly.express as px
import plotly.graph_objects as go
# From notebook: All other functions (calculate_ks_distance, generate_synthetic_data,
# group_uoms_by_business_knowledge, assess_homogeneity,
# create_ks_distance_matrix, plot_cdfs) should be defined.
```

