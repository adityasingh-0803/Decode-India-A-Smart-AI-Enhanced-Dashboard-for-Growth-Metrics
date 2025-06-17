import React from 'react';

const ExportTools = () => (
  <div className="bg-white p-4 rounded-xl shadow mb-6 flex gap-4">
    <button className="bg-blue-500 text-white px-4 py-2 rounded">📤 Export PDF</button>
    <button className="bg-green-500 text-white px-4 py-2 rounded">📥 Export CSV</button>
  </div>
);

export default ExportTools;
