import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import numpy as np
import statsmodels.api as sm

# Load main metrics
df = pd.read_csv("data/india_growth_metrics.csv")
df.columns = df.columns.str.strip()
cities = df['City'].unique()
metrics = df.columns[1:-1]  # Exclude City and Gini Coefficient

# Cluster setup
scaler = StandardScaler()
cluster_data = scaler.fit_transform(df[metrics])
kmeans = KMeans(n_clusters=4, random_state=0).fit(cluster_data)
df['Cluster'] = kmeans.labels_

app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server
app.title = "India Growth Metrics Dashboard"

app.layout = html.Div([
    html.H1("India Growth Metrics Dashboard", style={'textAlign': 'center'}),

    html.Div([
        html.Label("Select Cities:"),
        dcc.Dropdown(
            id='city-selector',
            options=[{'label': c, 'value': c} for c in cities],
            value=list(cities[:3]),
            multi=True
        )
    ], style={'width': '48%', 'display': 'inline-block'}),

    html.Div([
        html.Label("Select Metric:"),
        dcc.Dropdown(
            id='metric-selector',
            options=[{'label': m, 'value': m} for m in metrics],
            value=metrics[0]
        )
    ], style={'width': '48%', 'display': 'inline-block'}),

    dcc.Graph(id='bar-chart'),
    dcc.Graph(id='radar-chart'),
    dcc.Graph(id='correlation-matrix'),
    html.Div(id='ai-insight'),
    html.Div(id='twin-city'),

    html.Div([
        html.Label("Select City for Time Series:"),
        dcc.Dropdown(
            id='time-series-city-selector',
            options=[{'label': c, 'value': c} for c in cities],
            value=cities[0]
        )
    ], style={'width': '48%'}),

    dcc.Graph(id='time-series'),
    dcc.Graph(id='cluster-view')
])

@app.callback(
    Output('bar-chart', 'figure'),
    Input('city-selector', 'value'),
    Input('metric-selector', 'value')
)
def update_bar_chart(selected_cities, selected_metric):
    filtered = df[df['City'].isin(selected_cities)]
    fig = px.bar(filtered, x='City', y=selected_metric, color='City', title=f"{selected_metric} Comparison")
    return fig

@app.callback(
    Output('radar-chart', 'figure'),
    Input('city-selector', 'value')
)
def update_radar_chart(selected_cities):
    radar_df = df[df['City'].isin(selected_cities)].set_index('City')
    melted = radar_df[metrics].reset_index().melt(id_vars='City', var_name='Metric', value_name='Value')
    fig = px.line_polar(melted, r='Value', theta='Metric', color='City', line_close=True, title="Radar View")
    fig.update_traces(fill='toself')
    return fig

@app.callback(
    Output('correlation-matrix', 'figure'),
    Input('city-selector', 'value')
)
def update_correlation(selected_cities):
    corr = df[df['City'].isin(selected_cities)][metrics].corr()
    fig = px.imshow(corr, text_auto=True, title="Correlation Matrix")
    return fig

@app.callback(
    Output('ai-insight', 'children'),
    Input('city-selector', 'value')
)
def generate_ai_insight(selected_cities):
    insights = []
    for city in selected_cities:
        city_data = df[df['City'] == city]
        highest = city_data[metrics].idxmax(axis=1).values[0]
        lowest = city_data[metrics].idxmin(axis=1).values[0]
        insights.append(f"{city} excels in {highest} but needs improvement in {lowest}.")
    return html.Div([
        html.H4("AI-Powered Insights:"),
        html.Ul([html.Li(i) for i in insights])
    ])

@app.callback(
    Output('twin-city', 'children'),
    Input('city-selector', 'value')
)
def find_twin_city(selected_cities):
    twin_info = []
    for city in selected_cities:
        city_vec = df[df['City'] == city][metrics].values
        df['distance'] = np.linalg.norm(df[metrics].values - city_vec, axis=1)
        nearest = df[df['City'] != city].sort_values('distance').iloc[0]['City']
        twin_info.append(f"{city}'s most similar city is {nearest}.")
    return html.Div([
        html.H4("Twin City Recommendations:"),
        html.Ul([html.Li(i) for i in twin_info])
    ])

@app.callback(
    Output('time-series', 'figure'),
    Input('metric-selector', 'value'),
    Input('time-series-city-selector', 'value')
)
def show_forecast(selected_metric, selected_city):
    time_df = pd.read_csv("data/timeseries.csv", encoding='utf-8-sig')
    time_df.columns = time_df.columns.str.strip()
    time_df['City'] = time_df['City'].str.strip()
    fig = go.Figure()
    city_df = time_df[time_df['City'] == selected_city].sort_values('Year')
    city_df['Year'] = pd.to_datetime(city_df['Year'], format='%Y')

    if selected_metric in city_df.columns:
        ts = city_df.set_index('Year')[selected_metric]
        fig.add_trace(go.Scatter(x=ts.index, y=ts.values, mode='lines+markers', name=selected_metric))
        try:
            model = sm.tsa.ARIMA(ts, order=(1, 1, 0)).fit()
            forecast = model.get_forecast(steps=3)
            forecast_index = pd.date_range(start=ts.index[-1] + pd.offsets.YearBegin(), periods=3, freq='YS')
            forecast_series = pd.Series(forecast.predicted_mean.values, index=forecast_index)
            fig.add_trace(go.Scatter(x=forecast_series.index, y=forecast_series.values,
                                     mode='lines+markers', name=f"{selected_metric} Forecast",
                                     line=dict(dash='dash')))
        except:
            pass

    fig.update_layout(title=f"Time Series Forecast: {selected_metric} in {selected_city}", xaxis_title='Year')
    return fig

@app.callback(
    Output('cluster-view', 'figure'),
    Input('metric-selector', 'value')
)
def show_clusters(metric):
    fig = px.scatter(df, x=metric, y='Gini Coefficient', color='Cluster',
                     hover_data=['City'], title="City Clustering")
    return fig

if __name__ == '__main__':
    app.run(debug=True)
