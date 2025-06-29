import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { cn } from "@/lib/utils";
import { CloudUploadIcon } from "lucide-react";
import PropTypes from "prop-types";
import { useEffect, useState } from "react";
import { Input } from "../ui/input";

export default function FileUpload({
  onChange,
  value,
  error,
  accept,
  isImage,
}) {
  const [doc, setDoc] = useState({
    id: 0,
    name: "",
    file: null,
    url: "",
  });

  useEffect(() => {
    (async () => {
      if (value !== null) {
        setDoc(value);
      }
    })();
  }, [value]);

  const handleChange = (event) => {
    const input = event.target;

    if (input?.files?.length) {
      const file = input.files[0];
      const newDoc = {
        id: 0,
        name: file.name,
        file,
        url: "",
      };
      setDoc(newDoc);
      onChange(newDoc);

      // ✅ Allow same file to be picked again
      input.value = null;
    } else {
      setDoc(null);
      onChange(null);
    }
  };

  const handleBadgeClick = (base64Data) => async (event) => {
    const byteCharacters = atob(base64Data);
    const byteNumbers = new Uint8Array(byteCharacters.length);
    for (let i = 0; i < byteCharacters.length; i++) {
      byteNumbers[i] = byteCharacters.charCodeAt(i);
    }
    const blob = new Blob([byteNumbers], { type: "application/pdf" });
    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = "document.pdf"; // File name
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <Card
      className={cn(
        error?.length && `border-red-600`,
        "border-dashed shadow-none"
      )}
    >
      <CardContent className="p-2">
        <div className="flex flex-col items-start space-y-1">
          {/* ✅ Show uploaded file name if available */}
          {doc?.file || doc?.document || doc?.url ? (
            <>
              <span className="text-sm text-gray-700 font-medium">
                Uploaded File:
              </span>
              <span className="text-sm text-blue-600 break-all">
                {doc?.file instanceof File
                  ? doc.file.name
                  : doc?.name || "फाईल"}
              </span>
            </>
          ) : (
            <span className="text-sm text-gray-500">No file uploaded</span>
          )}

          {/* ✅ Always show the Upload/Replace button */}
          <div className="mt-2 group relative">
            <Button variant="outline" size="sm">
              <CloudUploadIcon className="h-4 w-4 mr-2" />
              {doc?.file ? "Replace File" : "Upload File"}
            </Button>
            <Input
              type="file"
              className="absolute inset-0 h-full w-full cursor-pointer opacity-0"
              onChange={handleChange}
              accept={accept}
            />
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

FileUpload.defaultProps = {
  onChange: () => {},
  value: null,
  error: "",
  accept: "",
  isImage: false,
};

FileUpload.propTypes = {
  onChange: PropTypes.func,
  value: PropTypes.object,
  error: PropTypes.string,
  accept: PropTypes.string,
  isImage: PropTypes.bool,
};
