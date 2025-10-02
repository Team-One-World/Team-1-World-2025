import React from 'react';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';
ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

export default function ChartsPanel({ sampleStars = [] }) {
  // prepare two simple charts using star properties
  const labels = sampleStars.slice(0, 30).map((s, i) => s.name || `S${i+1}`);
  const periodData = sampleStars.slice(0, 30).map(s => Number(s.orbital_period) || null);
  const radiusData = sampleStars.slice(0, 30).map(s => Number(s.star_radius) || null);

  const periodChart = {
    labels,
    datasets: [{ label: 'Orbital period (sample)', data: periodData, tension: 0.3 }]
  };

  const radiusChart = {
    labels,
    datasets: [{ label: 'Stellar radius (sample)', data: radiusData, tension: 0.3 }]
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div className="bg-gray-800 p-4 rounded"> 
        <h4 className="text-sm font-semibold mb-2">Orbital period (sample)</h4>
        <Line data={periodChart} />
      </div>
      <div className="bg-gray-800 p-4 rounded"> 
        <h4 className="text-sm font-semibold mb-2">Stellar radius (sample)</h4>
        <Line data={radiusChart} />
      </div>
    </div>
  );
}