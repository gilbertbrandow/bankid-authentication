import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { z } from "zod";
import { LoginFormSchema } from "../../schemas/formSchemas";
import { Button } from "../../components/ui/button";
import { Input } from "../../components/ui/input";
import { Form, FormControl, FormDescription, FormField, FormItem, FormLabel, FormMessage } from "../../components/ui/form";
import { apiRequest } from "../../lib/api";

type FormData = z.infer<typeof LoginFormSchema>;

const EmailLogin = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();

  const form = useForm<FormData>({
    resolver: zodResolver(LoginFormSchema),
    defaultValues: {
      email: "",
      password: "",
    },
  });

  const onSubmit = async (values: FormData) => {
    try {
      const data = await apiRequest('authentication/login/', {
        method: 'POST',
        body: JSON.stringify(values),
      });
      console.log(data);
    } catch (error) {
      console.error('There was a problem with the login request:', error);
    }
  };

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="mx-auto grid w-[400px] gap-4">
        <FormField
          control={form.control}
          name="email"
          render={({ field }) => (
            <FormItem>
              <FormLabel htmlFor="email">{t("Email")}</FormLabel>
              <FormControl>
                <Input id="email" type="email" placeholder="m@example.com" required {...field} />
              </FormControl>
              <FormDescription>{/* Optional description */}</FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="password"
          render={({ field }) => (
            <FormItem>
              <div className="flex items-center">
                <FormLabel htmlFor="password">{t("Password")}</FormLabel>
                <Button
                  variant="link"
                  className="ml-auto pl-2 pr-0 text-muted-foreground hover:text-current flex items-center gap-2 inline-block text-xs underline"
                  onClick={() => navigate("/recover-password")}
                >
                  {t("Forgot your password?")}
                </Button>
              </div>
              <FormControl>
                <Input id="password" type="password" placeholder="*******" required {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit" className="w-full">
          {t("Login")}
        </Button>
      </form>
    </Form>
  );
};

export default EmailLogin;