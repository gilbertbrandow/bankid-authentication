import React, { useEffect, useState } from "react";
import { useApiRequest } from "../lib/api";
import { Permission } from "../types/permissions";

const Permissions: React.FC = () => {
  const [permissions, setPermissions] = useState<Permission[]>([]);
  const [error, setError] = useState<string | null>(null);
  const apiRequest = useApiRequest();

  useEffect(() => {
    const fetchPermissions = async () => {
      try {
        const data: Permission[] = await apiRequest("permissions");
        setPermissions(data);
      } catch (error: any) {
        setError(error.message);
      }
    };

    fetchPermissions();
  }, []);

  return (
    <div>
      <h1>Permissions</h1>
      {error && <p>Error: {error}</p>}
      <ul>
        {permissions.map((permission) => (
          <li key={permission.id}>{permission.name}</li>
        ))}
      </ul>
    </div>
  );
};

export default Permissions;
