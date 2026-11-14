import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from scipy import stats

st.set_page_config(page_title="CosmoTensor - Earth System Trend Detective", layout="wide")

st.title("🌍 Earth System Trend Detective")
st.markdown("**Team CosmoTensor** | NASA Space Apps Challenge 2026")
st.markdown("Analyze how Earth science variables change over time and test if regional climate shifts are statistically significant using NASA open data.")

# Sidebar parameters for user selection
st.sidebar.header("🔍 Trend Detective Controls")
lat = st.sidebar.number_input("Latitude", value=28.6139, format="%.4f")
lon = st.sidebar.number_input("Longitude", value=77.2090, format="%.4f")
start_year = st.sidebar.slider("Start Year", 2015, 2023, 2018)
end_year = st.sidebar.slider("End Year", 2024, 2025, 2024)

# NASA POWER API endpoint for daily meteorological / climate variables
@st.cache_data
def fetch_nasa_data(lat, lon, start_y, end_y):
    url = f"https://power.larc.nasa.gov/api/temporal/daily/point?parameters=T2M,PRECTOTCORR&community=RE&longitude={lon}&latitude={lat}&start={start_y}0101&end={end_y}1231&format=JSON"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        properties = data.get("properties", {}).get("parameter", {})
        df = pd.DataFrame(properties)
        df.index = pd.to_datetime(df.index, format='%Y%m%d')
        return df
    else:
        return None

if st.button("Run Trend Detective Analysis"):
    with st.spinner("Fetching data from NASA POWER API..."):
        df_nasa = fetch_nasa_data(lat, lon, start_year, end_year)
        
        if df_nasa is not None and not df_nasa.empty:
            df_nasa = df_nasa.reset_index().rename(columns={'index': 'Date'})
            
            # Clean data (NASA uses -999 for missing values)
            df_nasa = df_nasa[(df_nasa['T2M'] > -100) & (df_nasa['PRECTOTCORR'] > -100)]
            
            # Resample to monthly averages using 'ME' for newer pandas versions
            df_nasa.set_index('Date', inplace=True)
            df_monthly = df_nasa.resample('ME').mean().reset_index()
            
            st.success("Data successfully retrieved from NASA!")
            
            # Display interactive metric charts
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🌡️ Surface Temperature Trend (T2M)")
                fig_temp = px.scatter(df_monthly, x='Date', y='T2M', trendline="ols", 
                                      title="Monthly Mean Temperature (°C)",
                                      labels={'T2M': 'Temperature (°C)'})
                st.plotly_chart(fig_temp, use_container_width=True)
                
                # Statistical Significance Calculation for Temperature
                slope, intercept, r_value, p_value, std_err = stats.linregress(df_monthly.index, df_monthly['T2M'])
                st.metric("Temperature Trend Slope", f"{slope:.5f} °C/month")
                st.write(f"**Statistical Significance (p-value):** `{p_value:.4e}`")
                if p_value < 0.05:
                    st.success("Result: The temperature trend is statistically significant ($p < 0.05$).")
                else:
                    st.info("Result: The temperature trend is not statistically significant.")

            with col2:
                st.subheader("🌧️ Precipitation Trend (PRECTOTCORR)")
                fig_precip = px.scatter(df_monthly, x='Date', y='PRECTOTCORR', trendline="ols", 
                                        title="Monthly Precipitation (mm/day)",
                                        labels={'PRECTOTCORR': 'Precipitation (mm/day)'})
                st.plotly_chart(fig_precip, use_container_width=True)
                
                # Statistical Significance Calculation for Precipitation
                slope_p, intercept_p, r_val_p, p_val_p, std_err_p = stats.linregress(df_monthly.index, df_monthly['PRECTOTCORR'])
                st.metric("Precipitation Trend Slope", f"{slope_p:.5f} mm/day per month")
                st.write(f"**Statistical Significance (p-value):** `{p_val_p:.4e}`")
                if p_val_p < 0.05:
                    st.success("Result: The precipitation trend is statistically significant ($p < 0.05$).")
                else:
                    st.info("Result: The precipitation trend is not statistically significant.")
        else:
            st.error("Failed to fetch data from NASA API. Please try different coordinates.")