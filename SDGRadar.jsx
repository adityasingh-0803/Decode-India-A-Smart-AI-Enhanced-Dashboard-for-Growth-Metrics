import React from 'react';
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer } from 'recharts';

const data = [
  { goal: 'No Poverty', score: 85 },
  { goal: 'Good Health', score: 78 },
  { goal: 'Quality Education', score: 90 },
  { goal: 'Clean Water', score: 70 },
  { goal: 'Affordable Energy', score: 65 },
  { goal: 'Climate Action', score: 75 },
];

const SDGRadar = () => (
  <div className="bg-white p-4 rounded-xl shadow mb-6">
    <h2 className="text-xl font-semibold mb-2">🌐 SDG Radar View</h2>
    <ResponsiveContainer width="100%" height={400}>
      <RadarChart data={data}>
        <PolarGrid />
        <PolarAngleAxis dataKey="goal" />
        <PolarRadiusAxis angle={30} domain={[0, 100]} />
        <Radar name="Score" dataKey="score" stroke="#3b82f6" fill="#3b82f6" fillOpacity={0.6} />
      </RadarChart>
    </ResponsiveContainer>
  </div>
);

export default SDGRadar;
