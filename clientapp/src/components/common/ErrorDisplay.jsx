/* eslint-disable react/prop-types */
import React from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { AlertCircle } from "lucide-react";

// Using named export instead of default export
export const ErrorDisplay = ({
  error,
  title = "Error loading data",
  showIcon = true,
  variant = "destructive",
}) => {
  const errorMessage = error instanceof Error ? error.message : error;

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>
          <Alert variant={variant}>
            <div className="flex items-center gap-2">
              {showIcon && <AlertCircle className="h-4 w-4" />}
              <AlertTitle>{title}</AlertTitle>
            </div>
            <AlertDescription className="mt-2">{errorMessage}</AlertDescription>
          </Alert>
        </CardTitle>
      </CardHeader>
      <CardContent>
        {/* Optional: Add retry button or additional error details here */}
      </CardContent>
    </Card>
  );
};

// Example usage with named import:
// import { ErrorDisplay } from '@/components/ui/common/ErrorDisplay';
