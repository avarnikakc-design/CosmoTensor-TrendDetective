# 🌍 Earth System Trend Detective
**Team CosmoTensor | NASA Space Apps Challenge 2026**

> An interactive web application designed to decode Earth's interconnected environmental systems by selecting variables, visualizing long-term changes, and evaluating statistical significance using NASA open data.

---

### 🚀 About the Project
Change is constant across Earth's climate systems, but regional shifts can vary drastically even under the same driving forces. **Earth System Trend Detective** empowers users to select geographical coordinates and climate variables to instantly analyze historical trends and determine whether environmental changes are statistically significant ($p < 0.05$).

### 🛠️ Tech Stack
* **Language:** Python 3.14+
* **Framework:** Streamlit (Interactive UI)
* **Data Processing:** Pandas, SciPy, Statsmodels
* **Data Visualization:** Plotly Express
* **Data Source:** [NASA POWER API](https://power.larc.nasa.gov/) (Surface Temperature `T2M` & Precipitation `PRECTOTCORR`)

### 📊 Key Features
1. **Coordinate Selector:** Input any latitude and longitude globally.
2. **Time-Series Analysis:** View monthly resampled trends with OLS regression trendlines.
3. **Statistical Significance Engine:** Automatically computes linear regression slopes and outputs precise $p$-values to evaluate climate shifts.

---

### 🌐 Live Demo
* Access the live application here: [Insert Live Streamlit URL Here]
