import { Label } from "@radix-ui/react-label";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";

const EmailLogin = () => {
  return (
    <div className="mx-auto grid w-[400px] gap-4">
      <h1 className="text-3xl font-bold mb-4 text-center">
        Sign in to Waves
        <span className="align-super text-sm"> ©</span>
      </h1>
      <div className="grid gap-4">
        <div className="grid gap-2">
          <Label htmlFor="email">Email</Label>
          <Input id="email" type="email" placeholder="m@example.com" required />
        </div>
        <div className="grid gap-2">
          <div className="flex items-center">
            <Label htmlFor="password">Password</Label>
            <div className="ml-auto inline-block text-xs underline">
              Forgot your password?
            </div>
          </div>
          <Input id="password" type="password" placeholder="*******" required />
        </div>
        <Button type="submit" variant="outline" className="w-full">
          Login
        </Button>
      </div>
    </div>
  );
};

export default EmailLogin;
