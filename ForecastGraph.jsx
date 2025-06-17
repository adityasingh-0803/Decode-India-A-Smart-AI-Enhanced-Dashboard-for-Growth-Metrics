import React from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

const forecastData = [
  { year: 2023, GDP: 310 },
  { year: 2024, GDP: 340 },
  { year: 2025, GDP: 370 },
];

const ForecastGraph = () => (
  <div className="bg-white p-4 rounded-xl shadow mb-6">
    <h2 className="text-xl font-semibold mb-2">📈 GDP Forecast – Delhi</h2>
    <ResponsiveContainer width="100%" height={250}>
      <LineChart data={forecastData}>
        <XAxis dataKey="year" />
        <YAxis />
        <Tooltip />
        <Line type="monotone" dataKey="GDP" stroke="#34d399" strokeWidth={3} />
      </LineChart>
    </ResponsiveContainer>
  </div>
);

export default ForecastGraph;
