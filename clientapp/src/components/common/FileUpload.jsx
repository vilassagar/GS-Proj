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
    let newDoc = { ...doc };
    if (event?.target?.files?.length) {
      // set file name
      // set file
      // remove url
      let file = event.target.files[0];
      newDoc["name"] = file.name;
      newDoc["file"] = file;
      newDoc["url"] = "";
    } else {
      // remove file, name , url
      newDoc = null;
    }

    setDoc(newDoc);
    onChange(newDoc);
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
      <CardContent className="p-2 ">
        {doc?.file || doc?.document || doc?.url ? (
          <div className="flex flex column justify-between items-start ">
            {isImage ? (
              <img
                src={
                  doc?.url?.length
                    ? doc?.fileData
                    : URL.createObjectURL(doc?.file)
                }
                alt="Documents Preview"
                style={{ maxWidth: "300px", marginTop: "10px" }}
              />
            ) : (
              <div
                onClick={handleBadgeClick(doc?.document)}
                className="cursor-pointer"
              >
                {doc?.documentType}
              </div>
            )}
          </div>
        ) : (
          <div className=" border-red-500">
            <div className="group relative ">
              <Button variant="outline" size="sm">
                <CloudUploadIcon className="h-4 w-4 mr-2" />
                Upload File
              </Button>
              <Input
                type="file"
                className="absolute inset-0 h-full w-full cursor-pointer opacity-0"
                onChange={handleChange}
                accept={accept}
              />
            </div>
          </div>
        )}
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
