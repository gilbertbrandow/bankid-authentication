import React from "react";
import { Outlet } from "react-router-dom";
import { Button } from "../ui/button";
import { useLogout } from "../../lib/useLogout";

const DefaultLayout: React.FC = () => {
  const logout = useLogout();

  return (
    <div className="">
      <header className="">Default Header</header>
      <Button variant="outline" onClick={() => logout()}>Logout</Button>
      <main className="">
        <Outlet />
      </main>
      <footer className="">Default Footer</footer>
    </div>
  );
};

export default DefaultLayout;