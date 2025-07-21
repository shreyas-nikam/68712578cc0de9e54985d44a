id: 68712578cc0de9e54985d44a_documentation
summary: Module 5 - Lab 1 Documentation
feedback link: https://docs.google.com/forms/d/e/1FAIpQLSfWkOK-in_bMMoHSZfcIvAeO58PAH9wrDqcxnJABHaxiDqhSA/viewform?usp=sf_link
environments: Web
status: Published
# UoM Homogeneity & Clustering Explorer Codelab

## 1. Understanding Operational Risk Homogeneity and the Application's Purpose
Duration: 00:10:00

In the domain of financial risk management, specifically operational risk, accurately quantifying potential losses is critical. This often involves modeling loss events, but a fundamental challenge is ensuring that the data used for these models is statistically "homogeneous." Homogeneity implies that the loss events grouped together share similar underlying statistical distributions. If data is not homogeneous, models built upon it can be inaccurate, leading to misestimation of capital requirements or risk exposure.

This Streamlit application, the **UoM Homogeneity & Clustering Explorer**, provides an interactive platform to understand and explore this concept. It focuses on the initial, crucial steps in operational risk modeling: defining appropriate **Units of Measure (UoMs)** and grouping diverse operational risks into statistically homogenous units.

<aside class="positive">
<b>Why is homogeneity important?</b> For robust risk modeling (e.g., using Loss Distribution Approach - LDA), the assumption is that losses within a defined UoM are drawn from a single distribution. If this assumption is violated due to heterogeneous data, the model's predictions (like Value-at-Risk or Expected Shortfall) will be unreliable.
</aside>

**Key Concepts Explored:**

*   **Units of Measure (UoMs):** These are the fundamental categories used for collecting and organizing operational risk loss data. They can be defined by factors like business line, event type, or a combination thereof.
*   **Homogeneity:** The degree to which loss data within a specific UoM exhibits similar statistical characteristics (e.g., mean, variance, distribution shape).
*   **Grouping Strategies:** Methods employed to combine raw UoMs into larger, more statistically homogenous groups. This often involves a trade-off between practical business definitions and statistical rigor.
*   **Kolmogorov-Smirnov (KS) Test:** A non-parametric statistical test used to determine if two samples are drawn from the same continuous distribution. In this application, it measures the statistical similarity between loss distributions of different UoMs or within a grouped UoM.

The application is structured into three interconnected pages:

1.  **Data Generation:** Allows you to create synthetic operational loss data with customizable parameters. This provides a controlled environment to simulate different risk profiles.
2.  **UoM Grouping:** Enables the application of various grouping strategies to the generated raw UoMs, including business knowledge-based grouping. It also visualizes the statistical distances between raw UoMs.
3.  **Homogeneity Assessment:** Visualizes the statistical homogeneity of the grouped UoMs using the Kolmogorov-Smirnov (KS) test results and empirical Cumulative Distribution Functions (CDFs).

The concepts and methods demonstrated are inspired by the PRMIA Operational Risk Manager Handbook [1], emphasizing the practical challenges and statistical considerations in defining UoMs.

**Mathematical Formulae for KS D-statistic:**

The Kolmogorov-Smirnov (KS) D-statistic ($D$) between two empirical distributions $F_n(x)$ and $F(x)$ (where $F_n(x)$ is the empirical CDF of the sample and $F(x)$ is the theoretical CDF or empirical CDF of another sample) is defined as:
$$ D = \sup_x |F_n(x) - F(x)| $$
This formula represents the largest vertical distance between the two CDFs. A smaller $D$ value indicates greater similarity between the distributions.

The PRMIA handbook also references a scaled version for distance $d_{ij}$ between two UoMs $i$ and $j$ with sample sizes $n_i$ and $n_j$ and empirical CDFs $F_i(x)$ and $F_j(x)$:
$$ \displaystyle d_{ij}=\frac{n_i n_j}{n_i+n_j}\sup_X |F_i(x)-F_j(x)| $$
The Python functions within this application compute the unscaled $D$-statistic.

**Application Architecture and Flow:**

The Streamlit application uses a multi-page structure, managed by `st.sidebar.selectbox`. Data is passed between pages primarily through `st.session_state`.

```mermaid
graph TD
    A[app.py - Main Application] --> B(st.sidebar.selectbox);
    B --> C{Navigation Choice};
    C -- "Data Generation" --> D[application_pages/data_generation.py];
    D -- Generates Data --> E[st.session_state['synthetic_data']];
    C -- "UoM Grouping" --> F[application_pages/uom_grouping.py];
    F -- Reads 'synthetic_data' --> E;
    F -- Applies Grouping --> G[st.session_state['grouped_data']];
    C -- "Homogeneity Assessment" --> H[application_pages/homogeneity_assessment.py];
    H -- Reads 'grouped_data' --> G;
    H -- Assesses & Visualizes --> I[Display Results];
```

<aside class="positive">
<b>Session State:</b> Streamlit's `st.session_state` is a powerful feature that allows you to store and persist variables across user interactions and page reloads. In this application, it's crucial for passing the generated synthetic data and subsequently the grouped data between the different logical pages.
</aside>

<button>
  [Download PRMIA Handbook (External Link)](https://www.prmia.org/download/publications/Operational-Risk-Manager-Handbook)
</button>

## 2. Setting up the Development Environment
Duration: 00:05:00

Before you can run the application, you need to set up your Python environment and organize the project files.

### Prerequisites

*   Python 3.7+
*   `pip` (Python package installer)

### Project Structure

Create the following directory and file structure:

```
.
├── app.py
└── application_pages/
    ├── __init__.py
    ├── data_generation.py
    ├── uom_grouping.py
    └── homogeneity_assessment.py
```

### 2.1. Create Project Files

1.  **Create the `application_pages` directory:**
    ```console
    mkdir application_pages
    ```
2.  **Create an empty `__init__.py` inside `application_pages`:**
    ```console
    touch application_pages/__init__.py
    ```
    This makes `application_pages` a Python package, allowing you to import modules from it.
3.  **Create `app.py`:** Copy the content provided for `app.py` into this file.
4.  **Create `application_pages/data_generation.py`:** Copy the content provided for `application_pages/data_generation.py` into this file.
5.  **Create `application_pages/uom_grouping.py`:** Copy the content provided for `application_pages/uom_grouping.py` into this file.
6.  **Create `application_pages/homogeneity_assessment.py`:** Copy the content provided for `application_pages/homogeneity_assessment.py` into this file.

### 2.2. Install Dependencies

It's good practice to use a virtual environment to manage your project's dependencies.

1.  **Create a virtual environment (if you don't have one):**
    ```console
    python -m venv venv
    ```
2.  **Activate the virtual environment:**
    *   On macOS/Linux:
        ```console
        source venv/bin/activate
        ```
    *   On Windows:
        ```console
        venv\Scripts\activate
        ```
3.  **Install the required Python packages:**
    ```console
    pip install streamlit pandas numpy scipy plotly
    ```

### 2.3. Run the Application

Once all files are in place and dependencies are installed, you can run the Streamlit application from your project's root directory:

```console
streamlit run app.py
```

This command will open the application in your default web browser, typically at `http://localhost:8501`.

## 3. Data Generation
Duration: 00:08:00

The first step in exploring UoM homogeneity is to generate some data. This page simulates operational loss events with configurable characteristics, allowing you to create diverse datasets for experimentation.

### 3.1. Understanding the `run_data_generation` Function

Open `application_pages/data_generation.py`. The core logic resides in the `run_data_generation` function.

```python
# application_pages/data_generation.py
import streamlit as st
import pandas as pd
import numpy as np

def generate_synthetic_data(num_uoms, loss_events_per_uom, severity_mean_range, severity_std_range):
    """Generates synthetic operational loss data."""
    # ... (input validation) ...
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

def run_data_generation():
    st.header("Synthetic Data Generation")
    st.markdown("""
    This page allows you to generate synthetic operational loss data with customizable characteristics.
    Adjust the parameters in the sidebar to control the number of UoMs, loss events per UoM, and the severity distribution.
    The generated data will be displayed below.
    """)

    num_uoms = st.sidebar.slider("Number of Raw UoMs", min_value=2, max_value=20, value=5,
                                    help="Number of initial 'raw' Units of Measure to simulate loss data for.")
    loss_events_per_uom = st.sidebar.slider("Loss Events per UoM", min_value=10, max_value=1000, value=100,
                                            help="Number of loss events to generate for each raw UoM.")
    severity_mean_range = st.sidebar.slider("Severity Mean Range (Log-normal $\mu$)", min_value=1.0, max_value=10.0, value=(5.0, 7.0),
                                            help="Range for the mean parameter ($\mu$) of the underlying normal distribution for log-normal loss severity. Controls the average loss amount.")
    severity_std_range = st.sidebar.slider("Severity Std Dev Range (Log-normal $\sigma$)", min_value=0.1, max_value=5.0, value=(1.0, 2.0),
                                            help="Range for the standard deviation parameter ($\sigma$) of the underlying normal distribution for log-normal loss severity. Controls the dispersion of loss amounts.")

    try:
        synthetic_data = generate_synthetic_data(num_uoms, loss_events_per_uom, severity_mean_range, severity_std_range)
        st.dataframe(synthetic_data.head())
        st.write("Counts of original UoM IDs:")
        st.write(synthetic_data['uom_id'].value_counts())
        st.session_state['synthetic_data'] = synthetic_data  # Store in session state
    except ValueError as e:
        st.error(f"Error: {e}")
```

Key aspects:
*   **`generate_synthetic_data`**: This function is responsible for creating a Pandas DataFrame of synthetic loss events.
    *   It iterates through a specified number of `uom_id`s.
    *   For each `uom_id`, it generates `loss_events_per_uom` loss amounts.
    *   `loss_amount` is drawn from a **log-normal distribution**. This distribution is commonly used for operational loss modeling due to its right-skewed nature, which aligns with real-world loss data. The `mean` ($\mu$) and `std` ($\sigma$) parameters of the underlying normal distribution are randomly chosen within specified ranges for each UoM, simulating heterogeneity among raw UoMs.
    *   Additional categorical features like `event_type` and `business_line` are randomly assigned.
*   **Streamlit Widgets**: Sliders are used for `num_uoms`, `loss_events_per_uom`, `severity_mean_range`, and `severity_std_range`. These are placed in the `st.sidebar` for easy access.
*   **`st.session_state['synthetic_data']`**: The generated DataFrame is stored in Streamlit's session state. This makes the `synthetic_data` accessible to other pages (UoM Grouping and Homogeneity Assessment) without needing to regenerate it each time the page changes.

### 3.2. Hands-on: Generate Your Data

1.  Navigate to the "Data Generation" page in the Streamlit application (it's the default page).
2.  In the left sidebar, adjust the following parameters:
    *   **Number of Raw UoMs**: Start with `5`.
    *   **Loss Events per UoM**: Keep it at `100` for now.
    *   **Severity Mean Range (Log-normal $\mu$)**: Set this to a narrow range, e.g., `(5.0, 5.5)`, to simulate more homogenous raw UoMs, or a wider range, e.g., `(3.0, 8.0)`, for more heterogeneous UoMs.
    *   **Severity Std Dev Range (Log-normal $\sigma$)**: Similarly, adjust this range.
3.  Observe the `synthetic_data` DataFrame preview and the "Counts of original UoM IDs" below it. Each raw UoM should have approximately the `Loss Events per UoM` count.

<aside class="positive">
Experiment with different ranges for $\mu$ and $\sigma$. A wider range for these parameters will create raw UoMs that are inherently more distinct from each other, making the grouping challenge more evident.
</aside>

## 4. UoM Grouping
Duration: 00:15:00

Once you have generated synthetic data, the next step is to explore different strategies for grouping these raw UoMs into potentially more homogeneous units. This page allows you to apply such strategies and visualize the initial statistical distances between raw UoMs.

### 4.1. Understanding the Grouping Logic

Open `application_pages/uom_grouping.py`.

```python
# application_pages/uom_grouping.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# calculate_ks_distance function definition (repeated for self-contained file)
def calculate_ks_distance(data1, data2):
    """Calculates the Kolmogorov-Smirnov distance (D-statistic) between two datasets."""
    # ... (implementation) ...
    return d

def group_uoms_by_business_knowledge(data, event_types_to_group):
    """Groups UoMs based on business rules (event types)."""
    data_copy = data.copy()
    data_copy['grouped_uom_id'] = data_copy['uom_id'] # Initialize with original uom_id

    if event_types_to_group:
        mask = data_copy['event_type'].isin(event_types_to_group)
        if mask.any():
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
    # ... (Streamlit UI and logic) ...
    if 'synthetic_data' not in st.session_state:
        st.info("Please generate synthetic data on the 'Data Generation' page first.")
        return

    synthetic_data = st.session_state['synthetic_data'].copy()

    # ... (Sidebar radio buttons for strategy selection) ...

    if grouping_strategy == "No Grouping (Raw UoMs)":
        grouped_data['grouped_uom_id'] = grouped_data['uom_id']
    elif grouping_strategy == "Business Knowledge Grouping":
        # ... (multiselect for event types) ...
        grouped_data = group_uoms_by_business_knowledge(synthetic_data, event_types_to_group)
    # ... (Future strategies handled) ...

    st.session_state['grouped_data'] = grouped_data # Store the (potentially) grouped data

    # ... (Display KS distance matrix) ...
```

Key functionalities:
*   **`calculate_ks_distance`**: This function is crucial. It computes the KS D-statistic between two arrays of loss amounts. As mentioned, this is the unscaled version, representing the maximum absolute difference between the two empirical CDFs. A value of 0 indicates identical distributions.
    <aside class="negative">
    The `calculate_ks_distance` function is duplicated across `uom_grouping.py` and `homogeneity_assessment.py`. In a larger application, it would be best practice to define this utility function in a separate shared module (e.g., `utils.py`) and import it where needed to avoid redundancy and potential inconsistencies.
    </aside>
*   **`group_uoms_by_business_knowledge`**: This function simulates a simple business-rule-based grouping. It takes a list of `event_type`s and assigns a new `grouped_uom_id` (here, `9999`) to all loss events that fall under any of the selected types. Other UoMs retain their original `uom_id`.
*   **`create_ks_distance_matrix`**: This function calculates the KS distance between every pair of *raw* UoMs present in the `synthetic_data`. This matrix is then visualized as a heatmap.
*   **Grouping Strategies**: The sidebar allows selecting different strategies:
    *   **No Grouping (Raw UoMs)**: Each `uom_id` becomes its own `grouped_uom_id`.
    *   **Business Knowledge Grouping**: Applies the `group_uoms_by_business_knowledge` logic.
    *   **Statistical Clustering (K-means) (Future)** and **Combined Approach (Future)**: These are placeholders for future enhancements, indicating where more advanced clustering algorithms or hybrid approaches could be integrated.
*   **KS Distance Matrix Visualization**: A `plotly.express` heatmap is used to visually represent the `create_ks_distance_matrix` output. Darker colors (closer to 0) indicate UoMs with more similar loss distributions.

### 4.2. Hands-on: Explore Grouping Strategies

1.  Navigate to the "UoM Grouping" page in the Streamlit application.
2.  If you haven't already, ensure you've generated synthetic data on the "Data Generation" page.
3.  Observe the **Kolmogorov-Smirnov Distance Matrix Between Raw UoMs**. This heatmap shows the initial relationships between your generated raw UoMs.
    *   Look for cells with values close to 0 (darker colors) – these raw UoMs are statistically similar.
    *   Look for cells with higher values (lighter colors) – these raw UoMs are more dissimilar.
    *   The diagonal will always be 0 because a UoM is identical to itself.
4.  In the left sidebar, under "UoM Grouping Strategy," select **"Business Knowledge Grouping."**
5.  Below that, you'll see a multi-select box for "Event Types to Group."
    *   By default, 'Fraud' and 'Error' are selected. Try selecting only 'Fraud', or all three event types.
    *   Observe the "Grouped Data Sample" and "Counts of Grouped UoM IDs" below. Notice how selecting event types groups all associated loss events under the new `grouped_uom_id` of `9999`.
6.  Try selecting "No Grouping (Raw UoMs)" to see how the `grouped_uom_id` column reverts to the original `uom_id`.

<aside class="positive">
Think about the real-world implications: business knowledge grouping is often based on internal definitions, which might not always align with statistical homogeneity. This application helps visualize that trade-off. For example, 'Fraud' and 'Error' might be grouped together based on a business decision, but their underlying loss distributions could be very different, as you'll see in the next step.
</aside>

## 5. Homogeneity Assessment
Duration: 00:12:00

The final and most crucial step is to assess the homogeneity of the UoMs after applying a grouping strategy. This page uses the Kolmogorov-Smirnov (KS) test and visualizes Empirical Cumulative Distribution Functions (CDFs) to help you understand the statistical similarity within your grouped UoMs.

### 5.1. Understanding the Assessment Logic

Open `application_pages/homogeneity_assessment.py`.

```python
# application_pages/homogeneity_assessment.py
import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import kstest
import plotly.graph_objects as go
import plotly.express as px

# calculate_ks_distance function definition (repeated for self-contained file)
def calculate_ks_distance(data1, data2):
    """Calculates the Kolmogorov-Smirnov distance (D-statistic) between two datasets."""
    # ... (implementation) ...
    return d

def assess_homogeneity(data):
    """Evaluates homogeneity within each grouped UoM using KS test."""
    # ... (input validation) ...
    grouped_data = data.groupby('grouped_uom_id')['loss_amount'].apply(list)
    results = {}

    for group_id, losses in grouped_data.items():
        if len(losses) < 2:
            results[group_id] = np.nan # Not enough data for KS test
            continue
        # KS test against a normal distribution with the group's mean and std
        ks_statistic, p_value = kstest(losses, 'norm', args=(np.mean(losses), np.std(losses)))
        results[group_id] = ks_statistic
    return results

def plot_cdfs(data, grouped_uom_id_col='grouped_uom_id'):
    """Plots Empirical CDFs of losses for each raw UoM within its grouped UoM."""
    fig = go.Figure()
    unique_grouped_uoms = data[grouped_uom_id_col].unique()

    colors = px.colors.qualitative.Plotly # Or other suitable palette

    for i, grouped_id in enumerate(unique_grouped_uoms):
        group_data = data[data[grouped_uom_id_col] == grouped_id]
        unique_raw_uoms_in_group = sorted(group_data['uom_id'].unique())

        for j, raw_uom_id in enumerate(unique_raw_uoms_in_group):
            losses = group_data[group_data['uom_id'] == raw_uom_id]['loss_amount'].values
            if len(losses) > 1:
                sorted_losses = np.sort(losses)
                y_cdf = np.arange(1, len(sorted_losses) + 1) / len(sorted_losses)
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
                      font=dict(size=12))
    return fig

def run_homogeneity_assessment():
    # ... (Streamlit UI and logic) ...
    if 'grouped_data' not in st.session_state:
        st.info("Please generate synthetic data on the 'Data Generation' page and group UoMs on the 'UoM Grouping' page first.")
        return

    grouped_data = st.session_state['grouped_data']

    st.subheader("Homogeneity Assessment Table")
    # ... (Display homogeneity results) ...

    st.subheader("Empirical CDFs of Losses per Grouped UoM")
    # ... (Display CDF plots) ...
```

Key functionalities:
*   **`assess_homogeneity`**: This function calculates the Kolmogorov-Smirnov (KS) statistic for each `grouped_uom_id`.
    *   It groups the data by `grouped_uom_id`.
    *   For each group, it performs a `scipy.stats.kstest`. Crucially, it tests the empirical distribution of losses within that group against a *normal distribution* whose mean and standard deviation are derived from the group's own loss data.
    *   The output is a dictionary mapping each `grouped_uom_id` to its KS statistic. A smaller KS statistic (closer to 0) suggests that the group's loss distribution is more similar to a normal distribution, implying higher internal homogeneity *relative to a normal distribution*.
*   **`plot_cdfs`**: This function generates an interactive Plotly graph showing the Empirical Cumulative Distribution Functions (CDFs) for each *raw* UoM, categorized by their *grouped_uom_id*.
    *   An Empirical CDF shows the proportion of data points that are less than or equal to a given value.
    *   When multiple raw UoMs are part of the same grouped UoM, their individual CDFs are plotted. If these CDFs are closely aligned, it visually indicates strong homogeneity within that grouped UoM. If they are widely separated, it suggests heterogeneity.
*   **`st.session_state['grouped_data']`**: This page relies on the `grouped_data` DataFrame populated by the "UoM Grouping" page.

### 5.2. Hands-on: Assess Homogeneity

1.  Navigate to the "Homogeneity Assessment" page in the Streamlit application.
2.  Ensure you have generated data and applied a grouping strategy on the previous pages.
3.  **Homogeneity Assessment Table**:
    *   Observe the "KS Statistic" for each `grouped_uom_id`.
    *   Recall that a lower KS statistic (closer to 0) indicates greater similarity. If you used "No Grouping," you'll see a KS statistic for each original UoM. If you used "Business Knowledge Grouping," you'll see a KS statistic for `Group 9999` (if it was created) and any ungrouped original UoMs.
4.  **Empirical CDFs of Losses per Grouped UoM**:
    *   This plot is key to understanding homogeneity visually.
    *   **"No Grouping" Scenario**: Each `raw UoM` will likely have its own distinct CDF curve. If you set a wide `severity_mean_range` during data generation, you'll see these curves spread out horizontally, indicating significant differences in average loss amounts.
    *   **"Business Knowledge Grouping" Scenario**:
        *   Focus on `Group 9999`. If you grouped 'Fraud' and 'Error' event types, this group will contain loss data from multiple original UoMs that had these event types.
        *   Observe the CDFs within `Group 9999`. Are they tightly clustered or widely spread?
        *   If the individual CDFs within `Group 9999` are far apart, it suggests that despite being grouped by business knowledge, the underlying loss distributions are still very different, implying low homogeneity for this group.
        *   Compare this to any `raw UoM` that was *not* grouped (e.g., `Group X - Raw UoM Y`). Its CDF will represent only itself.

<aside class="positive">
<b>Interpreting CDFs:</b> If two or more CDF lines for raw UoMs within the *same* grouped UoM are very close to each other, it implies those raw UoMs are statistically similar in their loss distribution, thus contributing to a homogeneous grouped UoM. If they are far apart, the grouped UoM is heterogeneous.
</aside>

<aside class="negative">
The KS test implemented here compares the empirical distribution of a group against a *normal distribution* parameterized by the group's own mean and standard deviation. While this provides a measure of "normality," it does not directly test if *different raw UoMs within a group* are from the same distribution. The visual inspection of CDFs is more direct for that purpose. For a more rigorous statistical test of homogeneity *between* multiple samples, one might use a multi-sample KS test or other goodness-of-fit tests.
</aside>

## 6. Conclusion and Further Exploration
Duration: 00:05:00

This codelab has guided you through a Streamlit application designed to illustrate the critical concepts of Units of Measure (UoMs) and homogeneity in operational risk modeling. You've learned how to:

*   Generate synthetic operational loss data with controlled heterogeneity.
*   Apply different UoM grouping strategies, specifically a business knowledge-based approach.
*   Assess the statistical homogeneity of the resulting UoMs using the Kolmogorov-Smirnov (KS) test and visual inspection of Empirical Cumulative Distribution Functions (CDFs).

The application highlights the inherent trade-offs between practical business definitions of UoMs and the statistical homogeneity required for robust quantitative risk modeling. Often, a UoM defined purely by business rules might aggregate loss events from underlying distributions that are statistically very different, leading to heterogeneous data.

### Key Takeaways

*   **Homogeneity is paramount:** For accurate operational risk modeling, ensuring that loss data within each UoM is statistically homogeneous is crucial.
*   **KS Test as a metric:** The Kolmogorov-Smirnov D-statistic provides a quantitative measure of distance between distributions, aiding in assessing homogeneity.
*   **CDFs for visual insights:** Empirical CDF plots offer an intuitive visual way to compare loss distributions and identify heterogeneity within grouped UoMs.
*   **Business vs. Statistical Grouping:** Business considerations often drive UoM definitions, but these should be validated and, if necessary, refined using statistical methods to ensure homogeneity.

### Further Exploration and Enhancements

The application provides placeholders for future enhancements, suggesting areas for deeper investigation:

*   **Statistical Clustering (K-means):** Implementing K-means clustering on the KS distance matrix could automatically group raw UoMs based on their statistical similarity. This would involve calculating the KS distance between all pairs of raw UoMs (as already visualized in the heatmap) and then applying a clustering algorithm to these distances.
*   **Combined Approach:** A more sophisticated approach would integrate both business knowledge and statistical measures. For example, business rules could define initial broad categories, and then statistical clustering could be applied within these categories, or KS distances could be adjusted (as suggested by the formula in `uom_grouping.py`) to reflect business preferences.
*   **Advanced Goodness-of-Fit Tests:** Explore other statistical tests for homogeneity or goodness-of-fit, such as the Anderson-Darling test, which is often more sensitive in the tails of distributions, important for extreme loss events.
*   **Different Loss Distributions:** Extend the data generation to include other common operational loss distributions like Generalized Pareto Distribution (GPD) or Weibull.
*   **Optimization Algorithms:** Implement algorithms that aim to find the "optimal" grouping of UoMs that maximizes homogeneity while satisfying certain constraints (e.g., minimum number of loss events per group).

This application serves as a foundational tool for understanding and experimenting with UoM definition and homogeneity, empowering developers and risk professionals to build more robust operational risk models.
