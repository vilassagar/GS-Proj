import { Loader2 } from "lucide-react";
export const LoadingSpinner = () => (
  <div className="flex min-h-screen flex-col items-center justify-center">
    <Loader2 className="h-8 w-8 text-primary animate-spin" />
    <p className="mt-4 text-muted-foreground text-lg">Loading...</p>
  </div>
);
