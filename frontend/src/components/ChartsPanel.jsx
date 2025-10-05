import React from "react";
import Plot from "react-plotly.js";

export default function ChartsPanel({ sampleStars = [], samplePlanets = [] }) {
  // Prepare data for both charts
  const periodData = samplePlanets
    .map((p, i) => ({
      index: i + 1,
      name: p.name || `P${i + 1}`,
      value: Number(p.orbital_period) || null,
    }))
    .filter(d => d.value !== null);

  const radiusData = sampleStars
    .map((s, i) => ({
      index: i + 1,
      name: s.name || `S${i + 1}`,
      value: Number(s.star_radius) || null,
    }))
    .filter(d => d.value !== null);

  const chartLayout = (xTitle, yTitle) => ({
    autosize: true,
    margin: { t: 40, l: 50, r: 20, b: 50 }, // top margin for mode bar
    xaxis: { title: xTitle, color: "#9ca3af" },
    yaxis: { title: yTitle, color: "#9ca3af" },
    plot_bgcolor: "rgba(31, 41, 55, 0.9)",
    paper_bgcolor: "rgba(31, 41, 55, 0.9)",
    font: { color: "#9ca3af" },
  });

  const plotConfig = { responsive: true, displayModeBar: true };

  return (
    <div className="space-y-6">
      {/* Header Stats */}
      <div className="grid grid-cols-2 gap-4 mb-6">
        <div className="bg-gradient-to-br from-purple-500/10 to-purple-600/5 border border-purple-500/30 rounded-xl p-4 backdrop-blur-sm">
          <div className="text-purple-300 text-sm font-medium mb-1">Total Data Points</div>
          <div className="text-3xl font-bold text-white">{periodData.length}</div>
        </div>
        <div className="bg-gradient-to-br from-pink-500/10 to-pink-600/5 border border-pink-500/30 rounded-xl p-4 backdrop-blur-sm">
          <div className="text-pink-300 text-sm font-medium mb-1">Valid Measurements</div>
          <div className="text-3xl font-bold text-white">{radiusData.length}</div>
        </div>
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Orbital Period Chart */}
        <div className="flex flex-col h-80 bg-gradient-to-br from-gray-900/90 to-gray-800/90 border border-purple-500/30 rounded-2xl p-6 shadow-2xl backdrop-blur-sm hover:border-purple-400/50 transition-all duration-300">
          <div className="flex items-center justify-between mb-4">
            <h4 className="text-xl font-bold bg-gradient-to-r from-purple-400 to-purple-600 bg-clip-text text-transparent">
              Planetary Orbital Period
            </h4>
            <span className="text-xs text-purple-300 bg-purple-500/10 px-3 py-1 rounded-full">
              {samplePlanets.length} planets
            </span>
          </div>
          <div className="flex-1">
            <Plot
              data={[
                {
                  x: periodData.map(d => d.index),
                  y: periodData.map(d => d.value),
                  text: periodData.map(d => d.name),
                  type: "scatter",
                  mode: "lines+markers",
                  line: { color: "#a78bfa", width: 2 },
                  marker: { color: "#a78bfa", size: 6 },
                  fill: "tozeroy",
                  fillcolor: "rgba(167, 139, 250, 0.3)",
                  hovertemplate: "<b>%{text}</b><br>Period: %{y:.3f} days<extra></extra>",
                },
              ]}
              layout={chartLayout("Planet Index", "Period (days)")}
              useResizeHandler={true}
              style={{ width: "100%", height: "100%" }}
              config={plotConfig}
            />
          </div>
        </div>

        {/* Stellar Radius Chart */}
        <div className="flex flex-col h-80 bg-gradient-to-br from-gray-900/90 to-gray-800/90 border border-pink-500/30 rounded-2xl p-6 shadow-2xl backdrop-blur-sm hover:border-pink-400/50 transition-all duration-300">
          <div className="flex items-center justify-between mb-4">
            <h4 className="text-xl font-bold bg-gradient-to-r from-pink-400 to-pink-600 bg-clip-text text-transparent">
              Stellar Radius
            </h4>
            <span className="text-xs text-pink-300 bg-pink-500/10 px-3 py-1 rounded-full">
              {radiusData.length} stars
            </span>
          </div>
          <div className="flex-1">
            <Plot
              data={[
                {
                  x: radiusData.map(d => d.index),
                  y: radiusData.map(d => d.value),
                  text: radiusData.map(d => d.name),
                  type: "scatter",
                  mode: "lines+markers",
                  line: { color: "#f472b6", width: 2 },
                  marker: { color: "#f472b6", size: 6 },
                  fill: "tozeroy",
                  fillcolor: "rgba(244, 114, 182, 0.3)",
                  hovertemplate: "<b>%{text}</b><br>Radius: %{y:.3f} solar radii<extra></extra>",
                },
              ]}
              layout={chartLayout("Star Index", "Radius (solar radii)")}
              useResizeHandler={true}
              style={{ width: "100%", height: "100%" }}
              config={plotConfig}
            />
          </div>
        </div>
      </div>
    </div>
  );
}
