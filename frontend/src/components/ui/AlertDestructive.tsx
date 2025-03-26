import { TriangleAlert } from "lucide-react";
import { Alert, AlertDescription, AlertTitle } from "./alert";

interface AlertDestructiveProps {
  title: string;
  description: string;
}

export function AlertDestructive({
  title,
  description,
}: AlertDestructiveProps) {
  return (
    <Alert variant="destructive">
      <div className="flex align-center gap-1">
        <TriangleAlert className="h-4 w-4 mb-1" style={{marginTop: "-0.05rem"}} />
        <AlertTitle>{title}</AlertTitle>
      </div>
      <AlertDescription>{description}</AlertDescription>
    </Alert>
  );
}
