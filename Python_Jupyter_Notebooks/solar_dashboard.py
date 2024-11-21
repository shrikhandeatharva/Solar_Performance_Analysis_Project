import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Color Palette
COLOR_PALETTE = {
    'energy_line': '#1E90FF',  # Dodger Blue
    'energy_anomaly': '#FF4500',  # Orange Red
    'power_factor_normal': '#2E8B57',  # Sea Green
    'power_factor_anomaly': '#FF6347',  # Tomato
    'voltage_normal': '#4169E1',  # Royal Blue
    'voltage_anomaly': '#DC143C',  # Crimson
    'phase_a': '#1E90FF',  # Dodger Blue
    'phase_b': '#32CD32',  # Lime Green
    'phase_c': '#FF4500',  # Orange Red
    'bar_sites': ['#1E90FF', '#32CD32', '#FF4500']  # Consistent site colors
}

# Load Data
@st.cache_data
def load_data():
    site1_df = pd.read_csv(r"E:\Delphi Analytics Project Work\cleaned_solar_data_Site_1.csv", parse_dates=['indregTC1_timestamp'], dayfirst=True)
    site2_df = pd.read_csv(r"E:\Delphi Analytics Project Work\cleaned_solar_data_Site_2.csv", parse_dates=['indregTC2_timestamp'], dayfirst=True)
    site3_df = pd.read_csv(r"E:\Delphi Analytics Project Work\cleaned_solar_data_Site_3.csv", parse_dates=['indregTC3_timestamp'], dayfirst=True)
    return site1_df, site2_df, site3_df

site1_df, site2_df, site3_df = load_data()

# Streamlit UI Setup
st.sidebar.title("Solar Performance Analytics Dashboard")
site_choice = st.sidebar.radio("Choose a site:", ["Site 1", "Site 2", "Site 3", "All Sites"])

# Date Range Filter
st.sidebar.subheader("Filter by Date Range")
min_date = min(site1_df['indregTC1_timestamp'].min(), 
               site2_df['indregTC2_timestamp'].min(),
               site3_df['indregTC3_timestamp'].min())
max_date = max(site1_df['indregTC1_timestamp'].max(),
               site2_df['indregTC2_timestamp'].max(), 
               site3_df['indregTC3_timestamp'].max())

start_date = st.sidebar.date_input('Start Date', min_date)
end_date = st.sidebar.date_input('End Date', max_date)

# Daily View Checkbox
st.sidebar.subheader("Daily View")
daily_view = st.sidebar.checkbox("Show Daily Data")

# Anomaly Detection Function
def calculate_anomalies(df, column, n_std=3):
    mean_value = df[column].mean()
    std_dev = df[column].std()
    lower_threshold = mean_value - n_std * std_dev
    upper_threshold = mean_value + n_std * std_dev
    
    anomalies = df[(df[column] < lower_threshold) | (df[column] > upper_threshold)]
    
    return {
        'mean': mean_value,
        'std_dev': std_dev,
        'lower_threshold': lower_threshold,
        'upper_threshold': upper_threshold,
        'anomalies': anomalies,
        'anomaly_count': len(anomalies)
    }

# Site Selection Logic
if site_choice == "Site 1":
    data = site1_df[(site1_df['indregTC1_timestamp'] >= pd.to_datetime(start_date)) & 
                    (site1_df['indregTC1_timestamp'] < pd.to_datetime(end_date) + pd.Timedelta(days=1))]
    timestamp_column = 'indregTC1_timestamp'
    energy_column = 'indregTC1_Energy_kWh_sum'
    power_factor_column = 'indregTC1_Power_Factor_avg_avg'
    voltage_column = 'indregTC1_Voltage_LL_V_avg'
    current_a = data['indregTC1_Current_Phase_A_A_avg']
    current_b = data['indregTC1_Current_Phase_B_A_avg']
    current_c = data['indregTC1_Current_Phase_C_A_avg']

elif site_choice == "Site 2":
    data = site2_df[(site2_df['indregTC2_timestamp'] >= pd.to_datetime(start_date)) & 
                    (site2_df['indregTC2_timestamp'] < pd.to_datetime(end_date) + pd.Timedelta(days=1))]
    timestamp_column = 'indregTC2_timestamp'
    energy_column = 'indregTC2_Energy_kWh_sum'
    power_factor_column = 'indregTC2_Power_Factor_avg_avg'
    voltage_column = 'indregTC2_Voltage_LL_V_avg'
    current_a = data['indregTC2_Current_Phase_A_A_avg']
    current_b = data['indregTC2_Current_Phase_B_A_avg']
    current_c = data['indregTC2_Current_Phase_C_A_avg']

elif site_choice == "Site 3":
    data = site3_df[(site3_df['indregTC3_timestamp'] >= pd.to_datetime(start_date)) & 
                    (site3_df['indregTC3_timestamp'] < pd.to_datetime(end_date) + pd.Timedelta(days=1))]
    timestamp_column = 'indregTC3_timestamp'
    energy_column = 'indregTC3_Energy_kWh_sum'
    power_factor_column = 'indregTC3_Power_Factor_avg_avg'
    voltage_column = 'indregTC3_Voltage_LL_V_avg'
    current_a = data['indregTC3_Current_Phase_A_A_avg']
    current_b = data['indregTC3_Current_Phase_B_A_avg']
    current_c = data['indregTC3_Current_Phase_C_A_avg']

else:  # All Sites Comparison
    st.header("Total Energy Yield Across Sites")
    site1_total = site1_df['indregTC1_Energy_kWh_sum'].sum()
    site2_total = site2_df['indregTC2_Energy_kWh_sum'].sum()
    site3_total = site3_df['indregTC3_Energy_kWh_sum'].sum()

    st.metric(label="Site 1 Total Energy (kWh)", value=round(site1_total, 2))
    st.metric(label="Site 2 Total Energy (kWh)", value=round(site2_total, 2))
    st.metric(label="Site 3 Total Energy (kWh)", value=round(site3_total, 2))

    fig = go.Figure(data=[
        go.Bar(name="Site 1", x=["Total Energy"], y=[site1_total], marker_color=COLOR_PALETTE['bar_sites'][0]),
        go.Bar(name="Site 2", x=["Total Energy"], y=[site2_total], marker_color=COLOR_PALETTE['bar_sites'][1]),
        go.Bar(name="Site 3", x=["Total Energy"], y=[site3_total], marker_color=COLOR_PALETTE['bar_sites'][2]),
    ])
    fig.update_layout(title="Energy Yield Comparison", barmode='group')
    st.plotly_chart(fig)
    st.stop()

# Energy Generation Metrics
st.header("Energy Generation")
total_energy = data[energy_column].sum()
st.metric(label="Total Energy Generated (kWh)", value=round(total_energy, 2))

# Energy Anomalies
energy_anomalies = calculate_anomalies(data, energy_column)
st.metric(label="Energy Anomalies", value=energy_anomalies['anomaly_count'])

# Energy Time-Series Plot
fig_energy = px.line(data, x=timestamp_column, y=energy_column, 
                     title='Energy Generation Over Time',
                     labels={timestamp_column: 'Timestamp', energy_column: 'Energy Generated (kWh)'},
                     color_discrete_sequence=[COLOR_PALETTE['energy_line']])
fig_energy.update_layout(xaxis_rangeslider_visible=True)
st.plotly_chart(fig_energy)

# Energy Anomalies Scatter Plot
fig_energy_anomalies = px.scatter(data, x=timestamp_column, y=energy_column,
                                   color=data[energy_column].apply(
                                       lambda x: "Anomaly" if (x < energy_anomalies['lower_threshold'] or x > energy_anomalies['upper_threshold']) else "Normal"
                                   ),
                                   color_discrete_map={"Anomaly": COLOR_PALETTE['energy_anomaly'], "Normal": COLOR_PALETTE['energy_line']},
                                   title="Energy Generation Anomalies")
fig_energy_anomalies.add_hline(y=energy_anomalies['lower_threshold'], line_dash="dash", line_color="red", annotation_text="Lower Threshold")
fig_energy_anomalies.add_hline(y=energy_anomalies['upper_threshold'], line_dash="dash", line_color="red", annotation_text="Upper Threshold")
st.plotly_chart(fig_energy_anomalies)

# Power Factor Analysis
st.header("Power Factor Analysis")
power_factor_anomalies = calculate_anomalies(data, power_factor_column)
st.metric(label="Average Power Factor", value=round(power_factor_anomalies['mean'], 2))
st.metric(label="Power Factor Anomalies", value=power_factor_anomalies['anomaly_count'])

# Power Factor Anomalies Visualization
fig_power_factor = px.scatter(data, x=timestamp_column, y=power_factor_column,
                               color=data[power_factor_column].apply(
                                   lambda x: "Anomaly" if (x < power_factor_anomalies['lower_threshold'] or x > power_factor_anomalies['upper_threshold']) else "Normal"
                               ),
                               color_discrete_map={"Anomaly": COLOR_PALETTE['power_factor_anomaly'], "Normal": COLOR_PALETTE['power_factor_normal']},
                               title="Power Factor Anomalies")
fig_power_factor.add_hline(y=power_factor_anomalies['lower_threshold'], line_dash="dash", line_color="red", annotation_text="Lower Threshold")
fig_power_factor.add_hline(y=power_factor_anomalies['upper_threshold'], line_dash="dash", line_color="red", annotation_text="Upper Threshold")
st.plotly_chart(fig_power_factor)

# Voltage Stability Analysis
st.header("Voltage Stability Anomaly Detection")
voltage_anomalies = calculate_anomalies(data, voltage_column)
st.metric(label="Number of Voltage Anomalies", value=voltage_anomalies['anomaly_count'])

# Voltage Anomalies Visualization
fig_voltage_anomalies = px.scatter(data, x=timestamp_column, y=voltage_column,
                                   color=data[voltage_column].apply(
                                       lambda x: "Anomaly" if (x < voltage_anomalies['lower_threshold'] or x > voltage_anomalies['upper_threshold']) else "Normal"
                                   ),
                                   color_discrete_map={"Anomaly": COLOR_PALETTE['voltage_anomaly'], "Normal": COLOR_PALETTE['voltage_normal']},
                                   title="Voltage Stability Anomalies",
                                   labels={voltage_column: "Voltage (V)", timestamp_column: "Timestamp"})
fig_voltage_anomalies.add_hline(y=voltage_anomalies['lower_threshold'], line_dash="dash", line_color="red", annotation_text="Lower Threshold")
fig_voltage_anomalies.add_hline(y=voltage_anomalies['upper_threshold'], line_dash="dash", line_color="red", annotation_text="Upper Threshold")
st.plotly_chart(fig_voltage_anomalies)

# Current Distribution Across Phases
st.header("Current Distribution Across Phases")

# Calculate phase imbalance
phase_average = (current_a.mean() + current_b.mean() + current_c.mean()) / 3
phase_imbalance = ((max(current_a.mean(), current_b.mean(), current_c.mean()) -
                   min(current_a.mean(), current_b.mean(), current_c.mean())) / phase_average) * 100

# Display Phase Imbalance Metric
st.metric(label="Phase Imbalance (%)", value=f"{phase_imbalance:.2f}")

# Visualize Phase Currents
st.subheader("Phase Currents Over Time")
fig_phase_currents = go.Figure()
fig_phase_currents.add_trace(go.Scatter(x=data[timestamp_column], y=current_a, mode='lines', name='Phase A', line=dict(color=COLOR_PALETTE['phase_a'])))
fig_phase_currents.add_trace(go.Scatter(x=data[timestamp_column], y=current_b, mode='lines', name='Phase B', line=dict(color=COLOR_PALETTE['phase_b'])))
fig_phase_currents.add_trace(go.Scatter(x=data[timestamp_column], y=current_c, mode='lines', name='Phase C', line=dict(color=COLOR_PALETTE['phase_c'])))
fig_phase_currents.update_layout(title="Phase Currents Over Time",
                                  xaxis_title="Timestamp",
                                  yaxis_title="Current (A)",
                                  legend_title="Phase")
st.plotly_chart(fig_phase_currents)

# Visualize Current Distribution Histogram
st.subheader("Current Distribution Across Phases")
fig_distribution = go.Figure()
fig_distribution.add_trace(go.Histogram(x=current_a, name='Phase A', marker_color=COLOR_PALETTE['phase_a'], opacity=0.7))
fig_distribution.add_trace(go.Histogram(x=current_b, name='Phase B', marker_color=COLOR_PALETTE['phase_b'], opacity=0.7))
fig_distribution.add_trace(go.Histogram(x=current_c, name='Phase C', marker_color=COLOR_PALETTE['phase_c'], opacity=0.7))
fig_distribution.update_layout(title="Current Distribution Across Phases",
                                xaxis_title="Current (A)",
                                yaxis_title="Frequency",
                                barmode='overlay',
                                legend_title="Phase")
fig_distribution.update_traces(opacity=0.7)
st.plotly_chart(fig_distribution)


# Daily View Option
if daily_view:
    data['Date'] = data[timestamp_column].dt.date
    numeric_data = data.select_dtypes(include=['number'])
    daily_data = numeric_data.groupby(data['Date']).sum()

    st.header("Daily Energy Generation")
    fig_daily = px.bar(daily_data, x=daily_data.index, y=energy_column, 
                       title="Daily Energy Generation", labels={"index": "Date"})
    st.plotly_chart(fig_daily)

# Site Comparison (Optional)
st.header("Comparison Across Sites")
comparison_df = pd.DataFrame({
    "Metric": ["Total Energy", "Average Power Factor", "Voltage Stability"],
    "Site 1": [site1_df['indregTC1_Energy_kWh_sum'].sum(), site1_df['indregTC1_Power_Factor_avg_avg'].mean(), site1_df['indregTC1_Voltage_LL_V_avg'].std()],
    "Site 2": [site2_df['indregTC2_Energy_kWh_sum'].sum(), site2_df['indregTC2_Power_Factor_avg_avg'].mean(), site2_df['indregTC2_Voltage_LL_V_avg'].std()],
    "Site 3": [site3_df['indregTC3_Energy_kWh_sum'].sum(), site3_df['indregTC3_Power_Factor_avg_avg'].mean(), site3_df['indregTC3_Voltage_LL_V_avg'].std()],
}).set_index("Metric")
st.table(comparison_df)


# Anomaly Details
st.header("Anomaly Details")
with st.expander("Energy Anomalies"):
    if not energy_anomalies['anomalies'].empty:
        st.dataframe(energy_anomalies['anomalies'][[timestamp_column, energy_column]])
    else:
        st.write("No energy anomalies detected.")

with st.expander("Power Factor Anomalies"):
    if not power_factor_anomalies['anomalies'].empty:
        st.dataframe(power_factor_anomalies['anomalies'][[timestamp_column, power_factor_column]])
    else:
        st.write("No power factor anomalies detected.")

with st.expander("Voltage Anomalies"):
    if not voltage_anomalies['anomalies'].empty:
        st.dataframe(voltage_anomalies['anomalies'][[timestamp_column, voltage_column]])
    else:
        st.write("No voltage anomalies detected.")
