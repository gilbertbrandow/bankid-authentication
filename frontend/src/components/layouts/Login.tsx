import React, { ReactNode } from "react";
import { Avatar, AvatarImage, AvatarFallback } from "../ui/avatar";

interface LayoutProps {
  children: ReactNode;
}

const Login: React.FC<LayoutProps> = ({ children }) => {
  return (
    <div className="flex h-screen">
      <div className="w-2/5 h-full flex items-center justify-center py-12">
        {children}
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

export default Login;
