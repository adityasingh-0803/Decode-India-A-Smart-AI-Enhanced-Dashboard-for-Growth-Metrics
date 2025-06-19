# 🇮🇳 Decode India: Smart AI-Enhanced Dashboard for Growth Metrics

A powerful interactive dashboard that visualizes and analyzes growth metrics for 35 major Indian cities using AI, time series forecasting, and cluster-based insights.

---

## 🚀 Features

- 📊 **Compare Development Metrics**: Visual comparisons between cities on metrics like health, education, infrastructure, etc.
- 🔁 **Time Series Forecasting**: Uses ARIMA models to predict future values for selected indicators.
- 🌐 **Radar Chart Visualization**: View cities' SDG performance across multiple indicators.
- 🧠 **AI-Powered Insights**: Automatically highlights strongest and weakest areas for each city.
- 🌍 **Twin City Matching**: Suggests cities with similar developmental patterns.
- 🎯 **Clustering**: KMeans-based segmentation to group cities with similar development profiles.
- 🧮 **Correlation Analysis**: Examine relationships between key indicators.

---

## 📁 Project Structure
```
Decode-India/
│
├── app.py # Main Dash application
├── data/
│ ├── india_growth_metrics.csv # City-wide metrics data
│ └── timeseries.csv # Year-wise data (2015–2023) for forecasting
└── README.md # Instructions and documentation
```

---

## ⚙️ How to Run the Dashboard Locally

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/Decode-India.git
cd Decode-India
```
### Create & Activate a Virtual Environment
python -m venv .venv
# Activate the environment:
# On Windows
```bash
.venv\Scripts\activate
```
# On macOS/Linux
```bash
source .venv/bin/activate
```
### Install Required Dependencies
```bash
pip install -r requirements.txt
```
Or install individually:
```bash
pip install dash pandas plotly numpy scikit-learn statsmodels
```
### Add the Data Files
Place the following files in the data/ folder:

india_growth_metrics.csv – Contains city-wise growth indicators.

timeseries.csv – Contains yearly data for each city for time series analysis (2015–2023)

### Run the Application
```bash
python app.py
```

### View in Browser
Visit: 

```bash
http://127.0.0.1:8050/
```
