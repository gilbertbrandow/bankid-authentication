import { Label } from "@radix-ui/react-label";
import { Button } from "../../components/ui/button";
import { Input } from "../../components/ui/input";
import { useNavigate } from "react-router-dom";

const EmailLogin = () => {
  const navigate = useNavigate();

  return (
    <div className="mx-auto grid w-[400px] gap-4">
      <div className="grid gap-4">
        <div className="grid gap-2">
          <Label htmlFor="email">Email</Label>
          <Input id="email" type="email" placeholder="m@example.com" required />
        </div>
        <div className="grid gap-2">
          <div className="flex items-center">
            <Label htmlFor="password">Password</Label>
            <Button
              variant="link"
              className="ml-auto pl-2 pr-0 text-muted-foreground hover:text-current flex items-center gap-2 inline-block text-xs underline"
              onClick={() => navigate("/recover-password")}
            >
              Forgot your password?
            </Button>
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
