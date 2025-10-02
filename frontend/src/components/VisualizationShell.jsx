import React, { useState, useCallback } from 'react';
import Galaxy from './Galaxy';
import LoadingSpinner from './LoadingSpinner';

export default function VisualizationShell({ stars, fetchPlanetsForStar, isFullscreen, onEnter, onExit }) {
  const [loading, setLoading] = useState(false);

  const handleFetchPlanetsForStar = useCallback(async (starData) => {
    setLoading(true);
    try {
      return await fetchPlanetsForStar(starData);
    } finally {
      setLoading(false);
    }
  }, [fetchPlanetsForStar, setLoading]);

  return (
    <div className={isFullscreen ? 'fixed inset-0 z-50 bg-black' : ''}>
      {!isFullscreen && (
        <div className="flex items-center justify-between mb-4">
          <button onClick={onEnter} className="bg-indigo-600 px-4 py-2 rounded">Enter Visualization</button>
          <p className="text-sm text-gray-400">Tip: click a star to load its system</p>
        </div>
      )}

      <div style={{width:'100%', height: isFullscreen ? '100vh' : '600px'}} className="rounded overflow-hidden">
        {loading && (
          <div className="absolute inset-0 z-40 flex items-center justify-center">
            <LoadingSpinner size={96} />
          </div>
        )}
        <Galaxy stars={stars} fetchPlanetsForStar={handleFetchPlanetsForStar} isFullscreen={isFullscreen} onRequestExit={onExit} />
      </div>

      {isFullscreen && (
        <div className="absolute top-4 right-4 z-50">
          <button onClick={onExit} className="bg-red-600 text-white px-3 py-2 rounded">Exit Visualization</button>
        </div>
      )}
    </div>
  );
}