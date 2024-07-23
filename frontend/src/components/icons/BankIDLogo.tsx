import React from 'react';

interface BankIDLogoProps {
  color: string;
  size?: number;
}

const BankIDLogo: React.FC<BankIDLogoProps> = ({ color, size = 24 }) => (
  <svg
    version="1.1"
    id="Lager_1"
    xmlns="http://www.w3.org/2000/svg"
    xmlnsXlink="http://www.w3.org/1999/xlink"
    x="0px"
    y="0px"
    viewBox="0 0 619.2 513"
    xmlSpace="preserve"
    className="mr-2"
    width={size}
    height={size}
    fill={color}
  >
    <style type="text/css">
      {`.st0{fill: currentColor;}
        .st1{fill:none;}`}
    </style>
    <g>
      <path className="st0" d="M251.3,263.4l13.2-83.2c-5.2,0-14.1,0-14.1,0c-6.6,0-15.1-3.7-17.6-10.5c-0.8-2.3-2.7-10.2,8.2-17.9
            c3.9-2.7,6.4-5.7,6.9-8c0.5-2.4-0.1-4.5-1.8-6.1c-2.4-2.3-7.1-3.6-13.1-3.6c-10.1,0-17.2,5.8-17.9,10c-0.5,3.1,1.9,5.6,4,7.2
            c6.3,4.7,7.8,11.5,3.9,17.9c-4,6.6-12.7,10.9-22,11c0,0-9.2,0-14.4,0c-1.2,8.1-20.8,132.3-22.3,142.1h77.8
            C242.8,318,246.4,294.5,251.3,263.4L251.3,263.4z" />
      <g>
        <path className="st0" d="M160.1,351.1H192c13.6,0,16.9,6.9,15.9,13.2c-0.8,5.1-4.3,8.9-10.3,11.4c7.6,2.9,10.6,7.4,9.5,14.5
            c-1.4,8.9-9.1,15.5-19.2,15.5h-36.3L160.1,351.1z M181.2,373.7c6.2,0,9.1-3.3,9.7-7.2c0.6-4.2-1.3-7.1-7.5-7.1h-5.5l-2.2,14.3
            H181.2z M177.8,397.2c6.4,0,10.1-2.6,11-7.9c0.7-4.6-1.9-7.3-8.1-7.3h-6.2l-2.4,15.3H177.8z" />
        <path className="st0" d="M251.8,406.1c-8.3,0.6-12.3-0.3-14.3-3.9c-4.4,2.7-9.3,4.1-14.5,4.1c-9.4,0-12.7-4.9-11.8-10.3
            c0.4-2.6,1.9-5.1,4.3-7.2c5.2-4.5,18-5.1,23-8.5c0.4-3.8-1.1-5.2-5.8-5.2c-5.5,0-10.1,1.8-18,7.2l1.9-12.4
            c6.8-4.9,13.4-7.2,21-7.2c9.7,0,18.3,4,16.7,14.6l-1.9,12c-0.7,4.2-0.5,5.5,4.2,5.6L251.8,406.1z M237.4,387.2
            c-4.4,2.8-12.6,2.3-13.5,8.1c-0.4,2.7,1.3,4.7,4,4.7c2.6,0,5.8-1.1,8.4-2.9c-0.2-1-0.1-2,0.2-3.9L237.4,387.2z" />
        <path className="st0" d="M267.3,363.4h16.6l-0.9,5.5c5.3-4.5,9.3-6.2,14.5-6.2c9.3,0,13.6,5.7,12.1,15l-4.3,27.9h-16.6l3.6-23.1
            c0.7-4.2-0.6-6.2-3.8-6.2c-2.6,0-5,1.4-7.3,4.5l-3.8,24.7h-16.6L267.3,363.4z" />
        <path className="st0" d="M322.6,351.1h16.6l-4.2,26.8l15.9-14.5h20.5l-20.4,18l16.4,24.2h-20.9L333.9,386h-0.2l-3,19.5h-16.6
            L322.6,351.1z" />
      </g>
      <path className="st0" d="M381.3,351.1h19.1l-8.4,54.5h-19.1L381.3,351.1z" />
      <path className="st0" d="M409.7,351.1H437c21.1,0,27.2,15.3,25.2,28c-1.9,12.4-11.7,26.5-30.2,26.5h-30.8L409.7,351.1z M427.4,392.6
        c9.3,0,14.4-4.6,15.9-14.3c1.1-7.2-1.1-14.3-11.4-14.3h-5.1l-4.4,28.6H427.4z" />
      <path className="st0" d="M355.9,107.5h-79.5l-10.6,67.3l13.5,0c7.4,0,14.4-3.4,17.4-8.3c1-1.6,1.4-3,1.4-4.3c0-2.8-1.9-4.9-3.8-6.3
            c-5.2-3.9-6.3-8-6.3-10.9c0-0.6,0-1.1,0.1-1.6c1.1-7.1,10.7-14.8,23.4-14.8c7.6,0,13.4,1.8,16.9,5.1c3.1,2.9,4.3,7,3.4,11.3
            c-1.1,5.1-6.2,9.3-9.1,11.4c-7.7,5.4-6.7,10.1-6.2,11.5c1.6,4.2,7.7,6.9,12.4,6.9h20.6c0,0,0,0,0,0.1c28,0.2,43,13.1,38.3,43.1
            c-4.4,27.9-25.8,39.9-51.3,40.1l-10.1,64.4h14.9c62.9,0,114.3-40.4,124.4-104.2C478.2,139.1,427.9,107.5,355.9,107.5z" />
    </g>
    <rect className="st1" width="619.2" height="513" />
  </svg>
);

export default BankIDLogo;
