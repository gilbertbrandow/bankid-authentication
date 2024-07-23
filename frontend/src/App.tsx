import { Label } from "@radix-ui/react-label";
import BankIDLogo from "./components/icons/BankIDLogo";
import { Avatar, AvatarImage, AvatarFallback } from "./components/ui/avatar";
import { Button } from "./components/ui/button";
import { Input } from "./components/ui/input";

const App = () => {
  return (
    <div className="flex h-screen">
      {/* Left Side - Content */}
      <div className="w-2/5 h-full flex items-center justify-center py-12">
        <div className="mx-auto grid w-[400px] gap-4">
          <h1 className="text-3xl font-bold mb-4 text-center">
            Sign in to Waves
            <span className="align-super text-sm"> ©</span>
          </h1>
          <Button className="w-full bg-[#193E4F] text-white flex items-center justify-center">
            <BankIDLogo color="#ffffff" size={36} />
            Login with mobile BankID
          </Button>
          <Button variant="outline" className="w-full">
            <BankIDLogo color="#000" size={36} />
            Login with BankID on this device
          </Button>
          <div className="flex items-center mt-4">
            <div className="flex-grow border-t border-gray-300"></div>
            <span className="mx-4 text-gray-500">or login with</span>
            <div className="flex-grow border-t border-gray-300"></div>
          </div>
          <div className="grid gap-4">
            <div className="grid gap-2">
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                placeholder="m@example.com"
                required
              />
            </div>
            <div className="grid gap-2">
              <div className="flex items-center">
                <Label htmlFor="password">Password</Label>
                <div className="ml-auto inline-block text-xs underline">
                  Forgot your password?
                </div>
              </div>
              <Input
                id="password"
                type="password"
                placeholder="*******"
                required
              />
            </div>
            <Button type="submit" variant="outline" className="w-full">
              Login
            </Button>
          </div>
        </div>
      </div>
      {/* Right Side - Video */}
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
              alt="Yaroslav Shuraev
"
            />
            <AvatarFallback>YS</AvatarFallback>
          </Avatar>
          <span>
            Video by{" "}
            <a href="" className="underline">
              Yaroslav Shuraev
            </a>
          </span>
        </div>
      </div>
    </div>
  );
};

export default App;
