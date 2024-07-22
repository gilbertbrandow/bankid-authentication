import { Button } from "../src/components/ui/button";
import { Toaster } from "../src/components/ui/sonner";
import { toast } from "sonner"

const App = () => {

  return (
    <>
      <Button
        variant="outline"
        onClick={() => {
          toast("Event has been created", {
            description: "Sunday, December 03, 2023 at 9:00 AM",
            action: {
              label: "Undo",
              onClick: () => console.log("Undo"),
            },
          })
        }}
      >
        Add to calendar
      </Button>
      <Toaster />
    </>
  );
};

export default App;
