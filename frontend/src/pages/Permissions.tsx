import React, { useEffect, useState } from "react";
import { useApiRequest } from "../lib/api";
import { Permission } from "../types/permissions";
import { toast } from "sonner";

const Permissions: React.FC = () => {
  const [permissions, setPermissions] = useState<Permission[]>([]);
  const apiRequest = useApiRequest();

  const fetchPermissions = async () => {
    try {
      const data: Permission[] = await apiRequest("permissions", { method: "GET" });
      setPermissions(data);
    } catch (error: any) {
      toast.error("Error", {
        description: error.message,
      });
    }
  };
  
  useEffect(() => {
    fetchPermissions();
  }, []);

  return (
    <div>
      <h1>Permissions</h1>
      <ul>
        {permissions.map((permission) => (
          <li key={permission.id}>{permission.name}</li>
        ))}
      </ul>
    </div>
  );
};

export default Permissions;
