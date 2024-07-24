import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { z } from "zod";
import { LoginFormSchema } from "../../schemas/formSchemas";
import { Button } from "../../components/ui/button";
import { Input } from "../../components/ui/input";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "../../components/ui/form";
import { apiRequest } from "../../lib/api";
import { useState } from "react";
import { AlertDestructive } from "../../components/ui/AlertDestructive";
import { useAuth } from "../../context/AuthContext";
import Spinner from "../../components/icons/Spinner";

type FormData = z.infer<typeof LoginFormSchema>;

const EmailLogin = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const { setAuthTokens } = useAuth();
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  const form = useForm<FormData>({
    resolver: zodResolver(LoginFormSchema),
    defaultValues: {
      email: "",
      password: "",
    },
  });

  const onSubmit = async (values: FormData) => {
    setErrorMessage("");
    setLoading(true);

    try {
      const data = await apiRequest("authentication/login/", {
        method: "POST",
        body: JSON.stringify(values),
      });

      setAuthTokens(data.access_token, data.refresh_token);
      navigate("/dashboard");
    } catch (error: any) {
      setErrorMessage(error.message);
      setLoading(false);
    }
  };

  return (
    <Form {...form}>
      <form
        onSubmit={form.handleSubmit(onSubmit)}
        className="mx-auto grid w-[400px] gap-4"
      >
        <FormField
          control={form.control}
          name="email"
          render={({ field }) => (
            <FormItem>
              <FormLabel htmlFor="email">{t("Email")}</FormLabel>
              <FormControl>
                <Input
                  id="email"
                  type="email"
                  placeholder="m@example.com"
                  required
                  {...field}
                  disabled={loading}
                />
              </FormControl>
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
                <Input
                  id="password"
                  type="password"
                  placeholder="********"
                  required
                  {...field}
                  disabled={loading}
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit" className="w-full gap-4" disabled={loading}>
          {loading && <Spinner size={1.2} color="primary" />} {t("Login")}
        </Button>
        {errorMessage && (
          <AlertDestructive title="Error" description={errorMessage} />
        )}
      </form>
    </Form>
  );
};

export default EmailLogin;
