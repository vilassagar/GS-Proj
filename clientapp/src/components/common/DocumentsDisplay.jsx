/* eslint-disable react/prop-types */
import { FileText, ExternalLink } from "lucide-react";
import { Button } from "@/components/ui/button";
function DocumentsDisplay({ documents }) {
  console.log("Documents:", documents);
  if (!documents || documents.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        <FileText className="h-12 w-12 mx-auto mb-2 opacity-50" />
        <p>कोणतेही कागदपत्रे उपलब्ध नाहीत</p>
      </div>
    );
  }

  const handleViewDocument = (url) => {
    if (url) {
      window.open(url, "_blank");
    }
  };

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-1 gap-4">
        {documents.map((doc, index) => (
          <div
            key={index}
            className="border rounded-lg p-4 hover:bg-slate-50 transition-colors"
          >
            <div className="flex items-start justify-between">
              <div className="flex items-start gap-3 flex-1">
                <div className="p-2 bg-blue-100 rounded-lg">
                  <FileText className="h-5 w-5 text-blue-600" />
                </div>
                <div className="flex-1 min-w-0">
                  <h4 className="font-medium text-sm text-gray-900 mb-1">
                    {doc.documentName || doc.documentTypeName || "दस्तऐवज"}
                  </h4>
                  {doc.documentType && (
                    <p className="text-xs text-gray-500 mb-1">
                      प्रकार: {doc.documentType}
                    </p>
                  )}
                  {doc.uploadedAt && (
                    <p className="text-xs text-gray-500">
                      अपलोड केले:{" "}
                      {new Date(doc.uploadedAt).toLocaleDateString("mr-IN")}
                    </p>
                  )}
                  {doc.fileSize && (
                    <p className="text-xs text-gray-500">
                      आकार: {(doc.fileSize / 1024).toFixed(2)} KB
                    </p>
                  )}
                  {doc.status && (
                    <p className="text-xs text-gray-500">
                      स्थिती: {doc.submissionStatus || doc.status}
                    </p>
                  )}
                </div>
              </div>
              <div className="flex gap-2 ml-4">
                {doc.documentUrl && (
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => handleViewDocument(doc.documentUrl)}
                    className="gap-2"
                  >
                    <ExternalLink className="h-4 w-4" />
                    पहा
                  </Button>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
export default DocumentsDisplay;
