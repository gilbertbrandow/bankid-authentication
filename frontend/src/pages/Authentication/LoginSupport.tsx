import { useTranslation } from "react-i18next";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "../../components/ui/accordion";

const LoginSupport = () => {
  const { t } = useTranslation();

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
            <AccordionItem value={"item-" + index}>
              <AccordionTrigger>{entry.question}</AccordionTrigger>
              <AccordionContent>{entry.answers}</AccordionContent>
            </AccordionItem>
          );
        })}
      </Accordion>
    </div>
  );
};

export default LoginSupport;
