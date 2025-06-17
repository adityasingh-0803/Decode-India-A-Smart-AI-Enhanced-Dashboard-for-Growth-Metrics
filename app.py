import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import numpy as np
import statsmodels.api as sm

df = pd.read_csv("data/india_growth_metrics.csv")
cities = df['City'].unique()
metrics = df.columns[1:]

scaler = StandardScaler()
cluster_data = scaler.fit_transform(df[metrics])
kmeans = KMeans(n_clusters=4, random_state=0).fit(cluster_data)
df['Cluster'] = kmeans.labels_

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Decoding Development: India Growth Dashboard", style={'textAlign': 'center'}),

    html.Div([
        html.Label("Select Cities:"),
        dcc.Dropdown(
            id='city-selector',
            options=[{'label': city, 'value': city} for city in cities],
            value=[cities[0], cities[1]],
            multi=True
        )
    ], style={'width': '48%', 'display': 'inline-block', 'padding': '10px'}),

    html.Div([
        html.Label("Select Metric:"),
        dcc.Dropdown(
            id='metric-selector',
            options=[{'label': metric, 'value': metric} for metric in metrics],
            value=metrics[0]
        )
    ], style={'width': '48%', 'display': 'inline-block', 'padding': '10px'}),

    html.Div([
        html.Label("Select City for Time Series:"),
        dcc.Dropdown(
            id='time-series-city-selector',
            options=[{'label': city, 'value': city} for city in cities],
            value=cities[0]
        )
    ], style={'width': '48%', 'padding': '10px'}),

    dcc.Graph(id='bar-chart'),
    dcc.Graph(id='radar-chart'),
    dcc.Graph(id='correlation-matrix'),
    html.Div(id='ai-insight'),
    html.Div(id='twin-city'),
    dcc.Graph(id='time-series'),
    dcc.Graph(id='cluster-view')
])

@app.callback(
    Output('bar-chart', 'figure'),
    Input('city-selector', 'value'),
    Input('metric-selector', 'value')
)
def update_bar_chart(selected_cities, selected_metric):
    filtered_df = df[df['City'].isin(selected_cities)]
    fig = px.bar(filtered_df, x='City', y=selected_metric, color='City', title=f"{selected_metric} Comparison")
    return fig

@app.callback(
    Output('radar-chart', 'figure'),
    Input('city-selector', 'value')
)
def update_radar_chart(selected_cities):
    radar_df = df[df['City'].isin(selected_cities)].set_index('City')
    fig = px.line_polar(
        radar_df.T.reset_index().melt(id_vars='index', var_name='City', value_name='Value'),
        r='Value', theta='index', color='City', line_close=True,
        title="SDG Radar View (All Metrics)"
    )
    fig.update_traces(fill='toself')
    return fig

@app.callback(
    Output('correlation-matrix', 'figure'),
    Input('city-selector', 'value')
)
def update_correlation(selected_cities):
    corr_df = df[df['City'].isin(selected_cities)][metrics].corr()
    fig = px.imshow(corr_df, title="Correlation Matrix")
    return fig

@app.callback(
    Output('ai-insight', 'children'),
    Input('city-selector', 'value')
)
def generate_ai_insight(selected_cities):
    insights = []
    for city in selected_cities:
        city_data = df[df['City'] == city]
        highest = city_data[metrics].T.idxmax()[0]
        lowest = city_data[metrics].T.idxmin()[0]
        insights.append(f"{city} excels in {highest} but needs improvement in {lowest}.")
    return html.Div([html.H4("AI-Powered Insights:"), html.Ul([html.Li(i) for i in insights])])

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
        twin_info.append(f"{city}'s most similar city is {nearest} based on all development metrics.")
    return html.Div([html.H4("Twin City Recommendations:"), html.Ul([html.Li(i) for i in twin_info])])

@app.callback(
    Output('time-series', 'figure'),
    Input('metric-selector', 'value'),
    Input('time-series-city-selector', 'value')
)
def show_forecast(metric, selected_city):
    time_df = pd.read_csv("data/timeseries.csv")
    city_df = time_df[time_df['City'] == selected_city].sort_values('Year')
    city_df['Year'] = pd.to_datetime(city_df['Year'], format='%Y')

    fig = go.Figure()
    ts_metrics = ['PopulationGrowth', 'IndustrialOutput', 'EducationIndex', 'HealthIndex', 'InfrastructureScore']

    for m in ts_metrics:
        if m in city_df.columns:
            ts = city_df.set_index('Year')[m]
            fig.add_trace(go.Scatter(x=ts.index, y=ts.values, mode='lines+markers', name=m))

    if metric in ts_metrics and metric in city_df.columns:
        try:
            ts = city_df.set_index('Year')[metric]
            model = sm.tsa.ARIMA(ts, order=(1, 1, 0)).fit()
            forecast = model.get_forecast(steps=3)
            forecast_index = pd.date_range(start=ts.index[-1] + pd.offsets.YearBegin(), periods=3, freq='YS')
            forecast_series = pd.Series(forecast.predicted_mean.values, index=forecast_index)
            fig.add_trace(go.Scatter(x=forecast_series.index, y=forecast_series.values,
                                     mode='lines+markers', name=f"{metric} Forecast", line=dict(dash='dash')))
        except Exception:
            pass

    fig.update_layout(title=f"Time Series for {selected_city}", xaxis_title='Year')
    return fig

@app.callback(
    Output('cluster-view', 'figure'),
    Input('metric-selector', 'value')
)
def show_clusters(metric):
    fig = px.scatter(df, x=metric, y='Gini Coefficient', color='Cluster', symbol='Cluster', hover_data=['City'],
                     title="City Clustering Based on Metrics")
    return fig

if __name__ == '__main__':
    app.run(debug=True)
