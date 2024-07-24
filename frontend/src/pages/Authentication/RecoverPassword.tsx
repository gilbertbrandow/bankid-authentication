import { Label } from "@radix-ui/react-label";
import { Button } from "../../components/ui/button";
import { Input } from "../../components/ui/input";

const RecoverPassword = () => {
  return (
    <div className="mx-auto grid w-[400px] gap-4">
      <div className="grid gap-4">
        <div className="grid gap-2">
          <Label htmlFor="email">Email</Label>
          <Input id="email" type="email" placeholder="m@example.com" required />
        </div>
        <Button type="submit" variant="outline" className="w-full">
          Send link to reset password
        </Button>
      </div>
    </div>
  );
};

export default RecoverPassword;
