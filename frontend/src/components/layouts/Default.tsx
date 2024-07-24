import React from "react";
import { Outlet } from "react-router-dom";

const DefaultLayout: React.FC = () => {
  return (
    <div className="">
      <header className="">Default Header</header>
      <main className="">
        <Outlet />
      </main>
      <footer className="">Default Footer</footer>
    </div>
  );
};

export default DefaultLayout;