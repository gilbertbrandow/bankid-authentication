import { Label } from "@radix-ui/react-label";
import BankIDLogo from "./components/icons/BankIDLogo";
import { Button } from "./components/ui/button";
import { Input } from "./components/ui/input";

const App = () => {
  return (
    <div className="flex h-screen">
      {/* Left Side - Content */}
      <div className="w-2/5 h-full flex items-center justify-center py-12">
        <div className="mx-auto grid w-[400px] gap-4">
          <p className="text-balance text-muted-foreground text-center">Login to</p>
          <h1 className="text-3xl font-bold mb-4 text-center">
            Authentication
            <span className="align-super text-sm"> ©</span>
          </h1>
          <Button className="w-full bg-[#193E4F] text-white flex items-center justify-center">
            <BankIDLogo color="#ffffff" size={36}/>
            Login with mobile BankID
          </Button>
          <Button variant="outline" className="w-full">
            <BankIDLogo color="#000" size={36}/>
            Login with BankID on this device
          </Button>
          <div className="flex items-center mt-4">
            <div className="flex-grow border-t border-gray-300"></div>
            <span className="mx-4 text-gray-500">or</span>
            <div className="flex-grow border-t border-gray-300"></div>
          </div>
          <div className="grid gap-4">
            <div className="grid gap-2">
              <Label htmlFor="email">Email</Label>
              <Input id="email" type="email" placeholder="m@example.com" required />
            </div>
            <div className="grid gap-2">
              <div className="flex items-center">
                <Label htmlFor="password">Password</Label>
                <div className="ml-auto inline-block text-sm underline">
                  Forgot your password?
                </div>
              </div>
              <Input id="password" type="password" placeholder="*******" required />
            </div>
            <Button type="submit" variant="outline" className="w-full">
              Login
            </Button>
          </div>
          <div className="mt-4 text-center text-sm">
            Don&apos;t have an account? <div className="underline">Sign up</div>
          </div>
        </div>
      </div>
      {/* Right Side - Video */}
      <div className="w-3/5 h-full p-4">
        <video
          src="/painting.mp4"
          autoPlay
          loop
          muted
          className="object-cover w-full h-full rounded-lg"
        />
      </div>
    </div>
  );
};

export default App;