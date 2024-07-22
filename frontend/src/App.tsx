import { Button } from "../src/components/ui/button";
import { Toaster } from "../src/components/ui/sonner";
import { toast } from "sonner"

const App = () => {

  return (
    <>
      <Button
        variant="outline"
        onClick={() => {
          toast("Toast has been created", {
            description: "Just now",
            action: {
              label: "Undo",
            },
          })
        }}
      >
        Create sonner toaster
      </Button>
      <Toaster />
    </>
  );
};

export default App;
