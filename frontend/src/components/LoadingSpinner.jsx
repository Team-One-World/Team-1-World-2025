import React from 'react';

export default function LoadingSpinner({ size = 64 }) {
  return (
    <div style={{display:'flex',alignItems:'center',justifyContent:'center'}}>
      <div className="lds-ring" style={{width:size,height:size}}>
        <div></div><div></div><div></div><div></div>
      </div>
      <style>{`
        .lds-ring{display:inline-block;position:relative}
        .lds-ring div{box-sizing:border-box;display:block;position:absolute;width:100%;height:100%;border:4px solid #4f46e5;border-radius:50%;animation:lds-ring 1.2s cubic-bezier(.5,.0,.5,1) infinite;border-color:#4f46e5 transparent transparent transparent}
        .lds-ring div:nth-child(1){animation-delay:-0.45s}
        .lds-ring div:nth-child(2){animation-delay:-0.3s}
        .lds-ring div:nth-child(3){animation-delay:-0.15s}
        @keyframes lds-ring{0%{transform:rotate(0)}100%{transform:rotate(360deg)}}
      `}</style>
    </div>
  );
}