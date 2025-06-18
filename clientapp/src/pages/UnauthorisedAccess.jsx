import RButton from "@/components/ui/rButton";
import { userStore } from "@/lib/store";
import { HomeIcon, LockIcon, LogOut } from "lucide-react";

export default function UnauthorisedAccess() {
  const user = userStore((state) => state.user);
  const removeUser = userStore((state) => state.removeUser);

  const isRetiree = user?.userType?.name?.toLowerCase().trim() === "pensioner";

  return (
    <div className="flex min-h-[100dvh] flex-col items-center justify-center bg-background px-4 py-12 sm:px-6 lg:px-8">
      <div className="mx-auto max-w-md text-center">
        <LockIcon className="mx-auto h-12 w-12 text-primary" />
        <h1 className="mt-4 text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
          Unauthorized Access
        </h1>
        <p className="mt-4 text-muted-foreground">
          You are not authorized to access this page. Please contact an
          administrator if you believe this is an error.
        </p>
        <div className="mt-6">
          <RButton
            onClick={() => {
              if (isRetiree) {
                window.location.href = "/";
              } else {
                window.location.href = "/";
              }
            }}
            className="inline-flex items-center rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground shadow-sm transition-colors hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2"
          >
            <span className="flex items-center">
              <HomeIcon className="mr-2 h-4 w-4" />
              Go to Homepage
            </span>
          </RButton>

          <RButton
            onClick={() => {
              removeUser();
              window.location.href = "/login";
            }}
            className=" ml-10 inline-flex items-center rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground shadow-sm transition-colors hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2"
          >
            <span className="flex items-center">
              <LogOut className="h-4 w-4 mr-2" />
              Logout
            </span>
          </RButton>
        </div>
      </div>
    </div>
  );
}
