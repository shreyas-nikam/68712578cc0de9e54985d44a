
import streamlit as st
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

if __name__ == "__main__":
    run_data_generation()
