# UoM Homogeneity & Clustering Explorer

## Project Title

**UoM Homogeneity & Clustering Explorer: A Streamlit Application for Operational Risk Lab**

## Description

This Streamlit application serves as an interactive lab project designed to explore critical concepts in operational risk modeling, specifically the definition of Units of Measure (UoMs) and the grouping of diverse operational risks into statistically homogenous units.

The application allows users to:
*   Generate synthetic operational loss data with customizable characteristics.
*   Apply different UoM grouping strategies, including business knowledge-based approaches.
*   Visualize and assess the impact of these strategies on data homogeneity using statistical tests and empirical Cumulative Distribution Functions (CDFs).

The core objective is to understand how different UoM definitions and grouping strategies affect the statistical homogeneity of resulting loss data, which is crucial for accurate risk modeling and capital calculations. The application demonstrates the practical trade-offs between intuitive business grouping rules and statistical homogeneity, drawing on concepts from the PRMIA Operational Risk Manager Handbook.

## Features

The application is structured into three main pages, accessible via the sidebar navigation:

1.  **Data Generation:**
    *   Generate synthetic operational loss data based on user-defined parameters:
        *   Number of raw UoMs.
        *   Loss events per UoM.
        *   Ranges for log-normal severity mean ($\mu$) and standard deviation ($\sigma$).
    *   Display a sample of the generated data and counts per raw UoM.

2.  **UoM Grouping:**
    *   Select and apply various UoM grouping strategies:
        *   **No Grouping:** Retain original raw UoMs.
        *   **Business Knowledge Grouping:** Combine UoMs based on selected event types (e.g., 'Fraud', 'Error') into a single "grouped" UoM.
        *   **Statistical Clustering (K-means):** (Future Enhancement) Group UoMs based on statistical similarities (e.g., Kolmogorov-Smirnov distance).
        *   **Combined Approach:** (Future Enhancement) Integrate business knowledge with statistical clustering.
    *   Display a sample of the grouped data and counts per grouped UoM.
    *   Visualize the **Kolmogorov-Smirnov (KS) Distance Matrix** between all initial raw UoMs using a heatmap, illustrating their statistical similarity.

3.  **Homogeneity Assessment:**
    *   Assess the statistical homogeneity within each grouped UoM using the **Kolmogorov-Smirnov (KS) test**.
        *   A lower KS statistic (closer to 0) indicates greater homogeneity within the group, implying the losses are drawn from a similar distribution.
    *   Visualize **Empirical Cumulative Distribution Functions (CDFs)** for loss amounts within each grouped UoM. This allows for a visual inspection of how similar the distributions of raw UoMs are after grouping.

**Key Concepts Explored:**

*   **Units of Measure (UoMs):** Basic categories for collecting operational risk data.
*   **Homogeneity:** The statistical similarity of loss data within a UoM or grouped UoM.
*   **Grouping Strategies:** Methods for combining raw UoMs into more homogenous groups.
*   **Kolmogorov-Smirnov (KS) Test:** A non-parametric statistical test to measure the maximum difference between two empirical (or one empirical and one theoretical) cumulative distribution functions. The application uses the D-statistic to compare distributions.

## Getting Started

Follow these instructions to set up and run the application on your local machine.

### Prerequisites

*   Python 3.8+
*   `pip` (Python package installer)

### Installation

1.  **Clone the repository (or download the code):**
    ```bash
    git clone https://github.com/yourusername/uom-risk-explorer.git # Replace with actual repo URL
    cd uom-risk-explorer
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    # On Windows
    .\venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    The `requirements.txt` file should contain:
    ```
    streamlit>=1.0
    pandas>=1.0
    numpy>=1.20
    scipy>=1.5
    plotly>=5.0
    ```

## Usage

1.  **Run the Streamlit application:**
    Ensure your virtual environment is active, then execute:
    ```bash
    streamlit run app.py
    ```
    This command will open the application in your default web browser (usually at `http://localhost:8501`).

2.  **Navigate the Application:**
    *   Use the sidebar on the left to navigate between the "Data Generation", "UoM Grouping", and "Homogeneity Assessment" pages.
    *   **Start with "Data Generation"** to create your synthetic dataset. Adjust the parameters in the sidebar and observe the generated data.
    *   **Proceed to "UoM Grouping"** to select and apply a grouping strategy. The KS distance matrix will provide insights into the similarity of raw UoMs.
    *   **Finally, visit "Homogeneity Assessment"** to view the homogeneity metrics (KS statistics) for your grouped UoMs and visualize their Empirical CDFs.

## Project Structure

The project is organized into a main application file and a directory for modular page components:

```
.
├── app.py                      # Main Streamlit application entry point
├── requirements.txt            # List of Python dependencies
└── application_pages/
    ├── __init__.py             # Makes application_pages a Python package
    ├── data_generation.py      # Logic for the data generation page
    ├── uom_grouping.py         # Logic for the UoM grouping page
    └── homogeneity_assessment.py # Logic for the homogeneity assessment page
```

*   `app.py`: This file orchestrates the Streamlit application, sets up the page configuration, displays the main introduction, and handles navigation between the different functional pages.
*   `application_pages/`: This directory contains separate Python files for each distinct page of the application, promoting modularity and easier maintenance.

## Technology Stack

*   **Python 3.x**: The core programming language.
*   **Streamlit**: For rapidly building and deploying data applications.
*   **Pandas**: For data manipulation and analysis.
*   **NumPy**: For numerical operations, especially array manipulation.
*   **SciPy**: For scientific computing, specifically the Kolmogorov-Smirnov test (`scipy.stats.kstest`).
*   **Plotly**: For interactive data visualizations (heatmaps, CDF plots).

## Contributing

Contributions are welcome! If you have suggestions for improvements, new features, or bug fixes, please feel free to:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/your-feature-name`).
3.  Make your changes.
4.  Commit your changes (`git commit -m 'Add new feature'`).
5.  Push to the branch (`git push origin feature/your-feature-name`).
6.  Open a Pull Request.

Please ensure your code adheres to standard Python best practices and includes appropriate documentation and tests where applicable.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details (though not explicitly provided, this is a common open-source license).
