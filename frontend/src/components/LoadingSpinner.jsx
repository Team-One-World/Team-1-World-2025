import React from 'react';

export default function LoadingSpinner({ size = 64 }) {
  return (
    <div className="flex items-center justify-center">
      <div
        style={{ width: size, height: size }}
        className="animate-spin rounded-full border-4 border-t-4 border-gray-200 border-t-indigo-600"
      ></div>
    </div>
  );
}