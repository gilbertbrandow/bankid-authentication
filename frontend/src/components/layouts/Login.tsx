import React, { ReactNode } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { Avatar, AvatarImage, AvatarFallback } from "../ui/avatar";
import { Outlet } from "react-router-dom";
import { Github, ArrowLeft } from "lucide-react";
import Logo from "../icons/Logo";
import { Button } from "../ui/button";

interface LoginLayoutProps {
  children?: ReactNode;
}

const LoginLayout: React.FC<LoginLayoutProps> = ({ children }) => {
  const navigate = useNavigate();
  const location = useLocation();

  return (
    <div className="flex h-screen">
      <div className="relative w-2/5 h-full flex items-center justify-center py-12">
        <header className="absolute top-0 w-full flex justify-between items-center p-8">
          <Logo size={32} color="#000000" className="mt-1" />
          {location.pathname !== "/login" && (
            <Button
              variant="link"
              className="pl-2 pr-0 flex items-center gap-2"
              onClick={() => navigate(-1)}
            >
              <ArrowLeft className="h-4 w-4" />
              Back
            </Button>
          )}
        </header>
        <Outlet />
        <footer className="absolute bottom-0 w-full text-sm text-muted-foreground p-10">
          <hr className="border-gray-300 mb-4" />
          <div className="flex justify-between">
            <a
              href="https://github.com/gilbertbrandow"
              className="underline flex items-center gap-1"
            >
              <Github className="h-4 w-4" />
              gilbertbrandow
            </a>
            <span>Copyright © {new Date().getFullYear()} </span>
          </div>
        </footer>
      </div>
      <div className="relative w-3/5 h-full p-4">
        <video
          src="/painting.mp4"
          autoPlay
          loop
          muted
          className="object-cover w-full h-full rounded-lg"
        />
        <div className="absolute bottom-8 left-8 bg-white bg-opacity-20 backdrop-filter backdrop-blur-lg text-white pl-2 pr-4 py-2 rounded-lg flex items-center gap-2">
          <Avatar className="h-8 w-8">
            <AvatarImage
              src="https://images.pexels.com/users/avatars/649765/yaroslav-shuraev-169.jpeg?auto=compress&fit=crop&h=130&w=130&dpr=2"
              alt="Yaroslav Shuraev"
            />
            <AvatarFallback>YS</AvatarFallback>
          </Avatar>
          <span>
            Video by{" "}
            <a href="" className="underline">
              Yaroslav Sharaev
            </a>
          </span>
        </div>
      </div>
    </div>
  );
};

export default LoginLayout;
