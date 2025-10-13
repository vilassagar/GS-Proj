/* eslint-disable react/prop-types */

import {
  FileText,
  ExternalLink,
  CheckCircle,
  Clock,
  XCircle,
  User,
  GraduationCap,
  Briefcase,
  Home,
  Heart,
  Award,
  Download,
} from "lucide-react";
import {
  Accordion,
  AccordionItem,
  AccordionTrigger,
  AccordionContent,
} from "@/components/ui/accordion";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

function DocumentsDisplay({ documents }) {
  console.log("Documents:", documents);

  // Category icons mapping (same as DocumentUpload)
  const categoryIcons = {
    identity_proof: <User className="w-5 h-5" />,
    educational: <GraduationCap className="w-5 h-5" />,
    professional: <Briefcase className="w-5 h-5" />,
    address_proof: <Home className="w-5 h-5" />,
    caste_category: <Award className="w-5 h-5" />,
    income_proof: <FileText className="w-5 h-5" />,
    medical: <Heart className="w-5 h-5" />,
    other: <FileText className="w-5 h-5" />,
  };

  // Category labels in Marathi (same as DocumentUpload)
  const categoryLabels = {
    identity_proof: "ओळख पुरावा",
    address_proof: "पत्ता पुरावा",
    educational: "शैक्षणिक",
    caste_category: "जात प्रमाण",
    income_proof: "उत्पन्न पुरावा",
    professional: "व्यावसायिक",
    medical: "वैद्यकीय",
    other: "इतर",
  };

  // Verification status config
  const verificationStatusConfig = {
    PENDING: {
      label: "तपासणी प्रलंबित",
      color: "text-yellow-600",
      bg: "bg-yellow-50",
      border: "border-yellow-200",
      icon: <Clock className="w-4 h-4" />,
    },
    APPROVED: {
      label: "मंजूर",
      color: "text-green-600",
      bg: "bg-green-50",
      border: "border-green-200",
      icon: <CheckCircle className="w-4 h-4" />,
    },
    REJECTED: {
      label: "नाकारले",
      color: "text-red-600",
      bg: "bg-red-50",
      border: "border-red-200",
      icon: <XCircle className="w-4 h-4" />,
    },
  };

  if (!documents || documents.length === 0) {
    return (
      <div className="text-center py-12 text-gray-500">
        <FileText className="h-16 w-16 mx-auto mb-4 opacity-50" />
        <p className="text-lg font-medium">कोणतेही कागदपत्रे उपलब्ध नाहीत</p>
        <p className="text-sm mt-2">कागदपत्रे अपलोड केल्यावर येथे दिसतील</p>
      </div>
    );
  }

  // Filter only submitted documents
  const submittedDocuments = documents.filter(
    (doc) => doc.submissionStatus === "SUBMITTED"
  );

  if (submittedDocuments.length === 0) {
    return (
      <div className="text-center py-12 text-gray-500">
        <FileText className="h-16 w-16 mx-auto mb-4 opacity-50" />
        <p className="text-lg font-medium">
          कोणतीही सबमिट केलेली कागदपत्रे नाहीत
        </p>
      </div>
    );
  }

  // Group documents by category
  const groupedDocuments = submittedDocuments.reduce((acc, doc) => {
    if (!acc[doc.category]) {
      acc[doc.category] = [];
    }
    acc[doc.category].push(doc);
    return acc;
  }, {});

  const handleViewDocument = (filePath) => {
    if (filePath) {
      // Construct the full URL - adjust the base URL as needed
      const baseUrl = import.meta.env.VITE_API_BASE_URL || "";
      const documentUrl = `${baseUrl}/${filePath}`;
      window.open(documentUrl, "_blank");
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return "N/A";
    const date = new Date(dateString);
    return date.toLocaleDateString("mr-IN", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
    });
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h3 className="text-xl font-semibold text-gray-700">
          सबमिट केलेली कागदपत्रे
        </h3>
        <div className="text-sm text-gray-600">
          एकूण: {submittedDocuments.length} कागदपत्रे
        </div>
      </div>

      <Accordion type="single" collapsible className="w-full space-y-4">
        {Object.entries(groupedDocuments).map(([category, docs]) => (
          <AccordionItem key={category} value={category}>
            <AccordionTrigger className="bg-slate-100 rounded-md gap-4 px-4">
              <div className="flex items-center gap-2">
                {categoryIcons[category]}
                <span>{categoryLabels[category] || category}</span>
                <span className="text-sm text-gray-500">
                  ({docs.length} कागदपत्रे)
                </span>
              </div>
            </AccordionTrigger>
            <AccordionContent>
              <div className="space-y-3 p-4">
                {docs.map((doc) => {
                  const statusConfig =
                    verificationStatusConfig[doc.verificationStatus] ||
                    verificationStatusConfig.PENDING;

                  return (
                    <div
                      key={doc.documentTypeId}
                      className={cn(
                        "border rounded-lg p-4 transition-all hover:shadow-md",
                        statusConfig.border,
                        statusConfig.bg
                      )}
                    >
                      <div className="flex items-start justify-between">
                        <div className="flex items-start gap-3 flex-1">
                          <div className="p-2 bg-white rounded-lg shadow-sm">
                            <FileText className="h-5 w-5 text-blue-600" />
                          </div>
                          <div className="flex-1 min-w-0">
                            <div className="flex items-center gap-2 mb-2">
                              <h4 className="font-semibold text-gray-900">
                                {doc.documentTypeNameEnglish}
                              </h4>
                              <div
                                className={cn(
                                  "flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium",
                                  statusConfig.color,
                                  statusConfig.bg
                                )}
                              >
                                {statusConfig.icon}
                                <span>{statusConfig.label}</span>
                              </div>
                            </div>
                            <p className="text-sm text-gray-600 mb-2">
                              {doc.documentTypeName}
                            </p>

                            <div className="grid grid-cols-2 gap-2 text-xs text-gray-600">
                              <div>
                                <span className="font-medium">
                                  अपलोड तारीख:
                                </span>{" "}
                                {formatDate(doc.uploadedAt)}
                              </div>
                              {doc.lastUpdatedAt && (
                                <div>
                                  <span className="font-medium">
                                    शेवटचा बदल:
                                  </span>{" "}
                                  {formatDate(doc.lastUpdatedAt)}
                                </div>
                              )}
                            </div>

                            {/* Display field values if present */}
                            {doc.fieldValues &&
                              Object.keys(doc.fieldValues).length > 0 && (
                                <div className="mt-3 pt-3 border-t border-gray-200">
                                  <p className="text-xs font-medium text-gray-700 mb-2">
                                    कागदपत्र तपशील:
                                  </p>
                                  <div className="grid grid-cols-2 gap-2">
                                    {Object.entries(doc.fieldValues).map(
                                      ([key, value]) => (
                                        <div
                                          key={key}
                                          className="text-xs text-gray-600"
                                        >
                                          <span className="font-medium capitalize">
                                            {key.replace(/_/g, " ")}:
                                          </span>{" "}
                                          {value}
                                        </div>
                                      )
                                    )}
                                  </div>
                                </div>
                              )}

                            {/* Admin comments if any */}
                            {doc.adminComments && (
                              <div className="mt-3 pt-3 border-t border-gray-200">
                                <p className="text-xs font-medium text-gray-700 mb-1">
                                  प्रशासकीय टिप्पणी:
                                </p>
                                <p className="text-xs text-gray-600 italic">
                                  {doc.adminComments}
                                </p>
                              </div>
                            )}
                          </div>
                        </div>

                        <div className="flex flex-col gap-2 ml-4">
                          {doc.filePath && (
                            <>
                              <Button
                                variant="outline"
                                size="sm"
                                onClick={() => handleViewDocument(doc.filePath)}
                                className="gap-2"
                              >
                                <ExternalLink className="h-4 w-4" />
                                पहा
                              </Button>
                              <Button
                                variant="outline"
                                size="sm"
                                onClick={() => handleViewDocument(doc.filePath)}
                                className="gap-2"
                              >
                                <Download className="h-4 w-4" />
                                डाउनलोड
                              </Button>
                            </>
                          )}
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </AccordionContent>
          </AccordionItem>
        ))}
      </Accordion>
    </div>
  );
}

export default DocumentsDisplay;
