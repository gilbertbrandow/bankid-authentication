import {
  Drawer,
  DrawerTrigger,
  DrawerContent,
  DrawerHeader,
  DrawerTitle,
  DrawerDescription,
  DrawerFooter,
  DrawerClose,
} from "./ui/drawer";
import { Button } from "./ui/button";
import { useTranslation } from "react-i18next";
import { Send } from "lucide-react";

const SignUpDrawer = () => {
  const { t } = useTranslation();

  return (
    <div>
      <Drawer>
        <DrawerTrigger asChild>
          <Button className="px-1 text-xs" variant="link">
            {t("Read about signing up")}
          </Button>
        </DrawerTrigger>
        <DrawerContent>
          <div className="mx-auto w-full max-w-sm">
            <DrawerHeader>
              <DrawerTitle>
                <h1 className="text-3xl my-4 font-bold text-center">
                  {t("So you would like to no more.")}
                </h1>
              </DrawerTitle>
              <DrawerDescription className="flex justify-center">
                <div className="max-w-[500px] text-center">
                  Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed
                  do eiusmod tempor incididunt ut labore et dolore magna aliqua.
                  Ut enim ad minim veniam.
                </div>
              </DrawerDescription>
            </DrawerHeader>
            <DrawerFooter>
              <Button><Send size={16} className="mr-2"/>{t("Contact us")}</Button>
              <DrawerClose asChild>
                <Button variant="outline">{t("Cancel")}</Button>
              </DrawerClose>
            </DrawerFooter>
          </div>
        </DrawerContent>
      </Drawer>
    </div>
  );
};

export default SignUpDrawer;
