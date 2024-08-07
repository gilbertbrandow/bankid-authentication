import React from "react";

interface FlagProps {
  country: "sv" | "en";
  size?: number;
  className?: string;
}

const Flag: React.FC<FlagProps> = ({ country, size = 2, className = "" }) => {
  const sizeInRem = `${size}rem`;

  if (country === "sv") {
    return (
      <svg
        version="1.1"
        id="fi_555606"
        xmlns="http://www.w3.org/2000/svg"
        x="0px"
        y="0px"
        viewBox="0 0 512 512"
        width={sizeInRem}
        height={sizeInRem}
        fill="currentColor"
        className={className}
      >
        <rect y="85.333" fill="#0052B4" width="512" height="341.337"></rect>
        <polygon
          fill="#FFDA44"
          points="192,85.33 128,85.33 128,223.996 0,223.996 0,287.996 128,287.996 128,426.662 192,426.662 
            192,287.996 512,287.996 512,223.996 192,223.996 "
        ></polygon>
      </svg>
    );
  } else if (country === "en") {
    return (
      <svg
        version="1.1"
        id="fi_555417"
        xmlns="http://www.w3.org/2000/svg"
        x="0px"
        y="0px"
        viewBox="0 0 512 512"
        width={sizeInRem}
        height={sizeInRem}
        fill="currentColor"
        className={className}
      >
        <rect y="85.333" fill="#F0F0F0" width="512" height="341.337"></rect>
        <polygon
          fill="#D80027"
          points="288,85.33 224,85.33 224,223.996 0,223.996 0,287.996 224,287.996 224,426.662 288,426.662 
        288,287.996 512,287.996 512,223.996 288,223.996 "
        ></polygon>
        <g>
          <polygon
            fill="#0052B4"
            points="393.785,315.358 512,381.034 512,315.358 	"
          ></polygon>
          <polygon
            fill="#0052B4"
            points="311.652,315.358 512,426.662 512,395.188 368.307,315.358 	"
          ></polygon>
          <polygon
            fill="#0052B4"
            points="458.634,426.662 311.652,344.998 311.652,426.662 	"
          ></polygon>
        </g>
        <polygon
          fill="#F0F0F0"
          points="311.652,315.358 512,426.662 512,395.188 368.307,315.358 "
        ></polygon>
        <polygon
          fill="#D80027"
          points="311.652,315.358 512,426.662 512,395.188 368.307,315.358 "
        ></polygon>
        <g>
          <polygon
            fill="#0052B4"
            points="90.341,315.356 0,365.546 0,315.356 	"
          ></polygon>
          <polygon
            fill="#0052B4"
            points="200.348,329.51 200.348,426.661 25.491,426.661 	"
          ></polygon>
        </g>
        <polygon
          fill="#D80027"
          points="143.693,315.358 0,395.188 0,426.662 0,426.662 200.348,315.358 "
        ></polygon>
        <g>
          <polygon
            fill="#0052B4"
            points="118.215,196.634 0,130.958 0,196.634 	"
          ></polygon>
          <polygon
            fill="#0052B4"
            points="200.348,196.634 0,85.33 0,116.804 143.693,196.634 	"
          ></polygon>
          <polygon
            fill="#0052B4"
            points="53.366,85.33 200.348,166.994 200.348,85.33 	"
          ></polygon>
        </g>
        <polygon
          fill="#F0F0F0"
          points="200.348,196.634 0,85.33 0,116.804 143.693,196.634 "
        ></polygon>
        <polygon
          fill="#D80027"
          points="200.348,196.634 0,85.33 0,116.804 143.693,196.634 "
        ></polygon>
        <g>
          <polygon
            fill="#0052B4"
            points="421.659,196.636 512,146.446 512,196.636 	"
          ></polygon>
          <polygon
            fill="#0052B4"
            points="311.652,182.482 311.652,85.331 486.509,85.331 	"
          ></polygon>
        </g>
        <polygon
          fill="#D80027"
          points="368.307,196.634 512,116.804 512,85.33 512,85.33 311.652,196.634 "
        ></polygon>
      </svg>
    );
  } else {
    return null;
  }
};

export default Flag;
