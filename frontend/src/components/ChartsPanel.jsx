import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';

export default function ChartsPanel({ sampleStars = [] }) {
  // Prepare data for both charts with ALL data points
  const periodData = sampleStars
    .map((s, i) => ({
      index: i + 1,
      name: s.name || `S${i + 1}`,
      value: Number(s.orbital_period) || null
    }))
    .filter(d => d.value !== null);

  const radiusData = sampleStars
    .map((s, i) => ({
      index: i + 1,
      name: s.name || `S${i + 1}`,
      value: Number(s.star_radius) || null
    }))
    .filter(d => d.value !== null);

  // Custom tooltip with better styling
  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-gray-900/95 border border-purple-500/50 rounded-lg p-3 shadow-xl backdrop-blur-sm">
          <p className="text-purple-300 font-semibold text-sm">{payload[0].payload.name}</p>
          <p className="text-white font-bold text-base">
            {payload[0].value.toFixed(3)}
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="space-y-6">
      {/* Header Stats */}
      <div className="grid grid-cols-2 gap-4 mb-6">
        <div className="bg-gradient-to-br from-purple-500/10 to-purple-600/5 border border-purple-500/30 rounded-xl p-4 backdrop-blur-sm">
          <div className="text-purple-300 text-sm font-medium mb-1">Total Data Points</div>
          <div className="text-3xl font-bold text-white">{sampleStars.length}</div>
        </div>
        <div className="bg-gradient-to-br from-pink-500/10 to-pink-600/5 border border-pink-500/30 rounded-xl p-4 backdrop-blur-sm">
          <div className="text-pink-300 text-sm font-medium mb-1">Valid Measurements</div>
          <div className="text-3xl font-bold text-white">
            {periodData.length} / {radiusData.length}
          </div>
        </div>
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Orbital Period Chart */}
        <div className="bg-gradient-to-br from-gray-900/90 to-gray-800/90 border border-purple-500/30 rounded-2xl p-6 shadow-2xl backdrop-blur-sm hover:border-purple-400/50 transition-all duration-300">
          <div className="flex items-center justify-between mb-4">
            <h4 className="text-xl font-bold bg-gradient-to-r from-purple-400 to-purple-600 bg-clip-text text-transparent">
              Orbital Period
            </h4>
            <span className="text-xs text-purple-300 bg-purple-500/10 px-3 py-1 rounded-full">
              {periodData.length} stars
            </span>
          </div>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={periodData} margin={{ top: 5, right: 10, left: 10, bottom: 5 }}>
              <defs>
                <linearGradient id="purpleGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#a78bfa" stopOpacity={0.3} />
                  <stop offset="95%" stopColor="#a78bfa" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" opacity={0.3} />
              <XAxis 
                dataKey="index" 
                stroke="#9ca3af" 
                tick={{ fill: '#9ca3af', fontSize: 12 }}
                label={{ value: 'Star Index', position: 'insideBottom', offset: -5, fill: '#9ca3af' }}
              />
              <YAxis 
                stroke="#9ca3af" 
                tick={{ fill: '#9ca3af', fontSize: 12 }}
                label={{ value: 'Period (days)', angle: -90, position: 'insideLeft', fill: '#9ca3af' }}
              />
              <Tooltip content={<CustomTooltip />} />
              <Line 
                type="monotone" 
                dataKey="value" 
                stroke="#a78bfa" 
                strokeWidth={2}
                dot={{ fill: '#a78bfa', r: 3 }}
                activeDot={{ r: 6, fill: '#c4b5fd' }}
                fill="url(#purpleGradient)"
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Stellar Radius Chart */}
        <div className="bg-gradient-to-br from-gray-900/90 to-gray-800/90 border border-pink-500/30 rounded-2xl p-6 shadow-2xl backdrop-blur-sm hover:border-pink-400/50 transition-all duration-300">
          <div className="flex items-center justify-between mb-4">
            <h4 className="text-xl font-bold bg-gradient-to-r from-pink-400 to-pink-600 bg-clip-text text-transparent">
              Stellar Radius
            </h4>
            <span className="text-xs text-pink-300 bg-pink-500/10 px-3 py-1 rounded-full">
              {radiusData.length} stars
            </span>
          </div>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={radiusData} margin={{ top: 5, right: 10, left: 10, bottom: 5 }}>
              <defs>
                <linearGradient id="pinkGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#f472b6" stopOpacity={0.3} />
                  <stop offset="95%" stopColor="#f472b6" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" opacity={0.3} />
              <XAxis 
                dataKey="index" 
                stroke="#9ca3af" 
                tick={{ fill: '#9ca3af', fontSize: 12 }}
                label={{ value: 'Star Index', position: 'insideBottom', offset: -5, fill: '#9ca3af' }}
              />
              <YAxis 
                stroke="#9ca3af" 
                tick={{ fill: '#9ca3af', fontSize: 12 }}
                label={{ value: 'Radius (solar radii)', angle: -90, position: 'insideLeft', fill: '#9ca3af' }}
              />
              <Tooltip content={<CustomTooltip />} />
              <Line 
                type="monotone" 
                dataKey="value" 
                stroke="#f472b6" 
                strokeWidth={2}
                dot={{ fill: '#f472b6', r: 3 }}
                activeDot={{ r: 6, fill: '#fbbf24' }}
                fill="url(#pinkGradient)"
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}