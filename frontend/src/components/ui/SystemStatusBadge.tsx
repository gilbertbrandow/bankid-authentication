import React from "react";
import { Badge } from "../ui/Badge";
import { useTranslation } from "react-i18next";

const SystemStatusBadge: React.FC<{ message: string; colorName: string }> = ({ message, colorName }) => {
    const { t } = useTranslation();
  
    return (
      <Badge
        variant="secondary"
        style={{ "--indicator-color": `hsl(var(--${colorName}))` } as React.CSSProperties}
      >
        <div className="w-2 h-2 mr-1.5 rounded-full running-indicator"></div>
        {t(message)}
      </Badge>
    );
  };
  
  export default SystemStatusBadge;
  