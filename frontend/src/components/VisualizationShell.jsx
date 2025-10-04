import React, { useState, useCallback, forwardRef } from 'react';
import Galaxy from './Galaxy';
import LoadingSpinner from './LoadingSpinner';

const VisualizationShell = forwardRef(({ stars, fetchPlanetsForStar, isFullscreen, onEnter, onExit }, ref) => {
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
    <div className={isFullscreen ? 'fixed inset-0 z-50 bg-black' : 'relative'}>
      {!isFullscreen && (
        <div className="flex items-center justify-between mb-4">
          <button onClick={onEnter} className="btn-primary w-full">Enter Visualization</button>
        </div>
      )}

      <div style={{width:'100%', height: isFullscreen ? '100vh' : '600px'}} className="relative rounded overflow-hidden">
        {loading && (
          <div className="absolute inset-0 z-40 flex items-center justify-center bg-black bg-opacity-50">
            <LoadingSpinner size={96} />
          </div>
        )}
        
        <Galaxy ref={ref} stars={stars} fetchPlanetsForStar={handleFetchPlanetsForStar} isFullscreen={isFullscreen} onRequestExit={onExit} />
      </div>

      {isFullscreen && (
        <div className="absolute top-4 right-4 z-50">
          <button onClick={onExit} className="bg-red-600 text-white px-4 py-2 rounded-lg shadow-lg hover:bg-red-700 transition-colors">Exit Visualization</button>
        </div>
      )}
    </div>
  );
});

export default VisualizationShell;