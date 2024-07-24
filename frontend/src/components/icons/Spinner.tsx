import React from 'react';

interface SpinnerProps {
  color?: string;
  size?: number;
}

const Spinner: React.FC<SpinnerProps> = ({ color = '#000', size = 2 }) => {
  const spinnerSize = `${size}rem`;
  const spinnerBorderSize = `${size / 10}rem`;

  return (
    <div className="spinner" style={{ width: spinnerSize, height: spinnerSize }}>
      <style>{`
        .spinner {
          position: relative;
          display: inline-block;
          border: ${spinnerBorderSize} solid rgba(0, 0, 0, 0.1);
          border-top: ${spinnerBorderSize} solid ${color};
          border-radius: 50%;
          animation: spin 1s linear infinite;
        }

        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
};

export default Spinner;
