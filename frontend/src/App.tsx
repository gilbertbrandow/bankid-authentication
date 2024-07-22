import { Button } from "../src/components/ui/button";
import { useToast } from "../src/components/ui/use-toast";
import { Toaster } from "../src/components/ui/toaster";
import { ToastAction } from "../src/components/ui/toast";

const App = () => {
  const { toast } = useToast();

  return (
    <>
      <Button
        variant="outline"
        onClick={() => {
          toast({
            title: "Scheduled: Catch up ",
            description: "Friday, February 10, 2023 at 5:45 PM",
            action: (
              <ToastAction altText="Goto schedule to undo">Undo</ToastAction>
            ),
          });
        }}
      >
        Add to calendar
      </Button>
      <Toaster />
    </>
  );
};

export default App;
