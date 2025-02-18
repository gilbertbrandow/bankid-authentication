import { ArrowLeft } from "lucide-react";
import { useTranslation } from "react-i18next";
import { useNavigate } from "react-router-dom";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "../../components/ui/accordion";
import { Button } from "../../components/ui/button";

const LoginSupport = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();

  const questions = [
    {
      question: t("Is it accessible?"),
      answers:
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
    },
    {
      question: t("I can't access my BankID?"),
      answers:
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
    },
    {
      question: t("I can't access my BankID?"),
      answers:
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
    },
  ];

  return (
    <div className="mx-auto grid w-[400px] gap-4">
      <h1 className="text-3xl font-bold mb-4 text-center">
        {t("Common Questions")}
      </h1>
      <Accordion type="single" collapsible className="w-full">
        {questions.map((entry, index) => {
          return (
            <AccordionItem key={index} value={"item-" + index}>
              <AccordionTrigger>{entry.question}</AccordionTrigger>
              <AccordionContent>{entry.answers}</AccordionContent>
            </AccordionItem>
          );
        })}
      </Accordion>
      <Button
        variant="link"
        className="mt-2 text-xs flex justify-center items-center text-muted-foreground text-center"
        onClick={() => navigate("/login")}
      >
        <ArrowLeft className="h-3 w-3 mr-1" />
        {t("To sign in")}
      </Button>
    </div>
  );
};

export default LoginSupport;
