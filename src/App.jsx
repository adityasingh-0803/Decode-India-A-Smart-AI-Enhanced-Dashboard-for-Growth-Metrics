import React from 'react';
import CityDashboard from './components/CityDashboard';
import AIInsight from './components/AIInsight';
import ForecastGraph from './components/ForecastGraph';
import ClusterView from './components/ClusterView';
import TwinCity from './components/TwinCity';
import ExportTools from './components/ExportTools';
import CorrelationMatrix from './components/CorrelationMatrix';
import SDGRadar from './components/SDGRadar';

function App() {
  return (
    <div className="min-h-screen p-4 bg-gray-100 text-gray-900">
      <h1 className="text-3xl font-bold mb-6">Decode India Dashboard 🇮🇳</h1>
      <ExportTools />
      <CityDashboard />
      <AIInsight />
      <ForecastGraph />
      <ClusterView />
      <TwinCity />
      <CorrelationMatrix />
      <SDGRadar />
    </div>
  );
}

export default App;
