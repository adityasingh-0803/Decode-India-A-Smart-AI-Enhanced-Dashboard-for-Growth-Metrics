import React from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

const data = [
  { year: 2018, HDI: 0.68 },
  { year: 2019, HDI: 0.7 },
  { year: 2020, HDI: 0.71 },
  { year: 2021, HDI: 0.72 },
  { year: 2022, HDI: 0.74 },
];

const CityDashboard = () => (
  <div className="bg-white rounded-xl p-4 shadow mb-6">
    <h2 className="text-xl font-semibold mb-2">City: Mumbai – HDI Over Time</h2>
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={data}>
        <XAxis dataKey="year" />
        <YAxis domain={[0.6, 1]} />
        <Tooltip />
        <Line type="monotone" dataKey="HDI" stroke="#8884d8" strokeWidth={3} />
      </LineChart>
    </ResponsiveContainer>
  </div>
);

export default CityDashboard;
