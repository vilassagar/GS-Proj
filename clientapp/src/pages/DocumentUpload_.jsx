import React, { useState, useEffect } from "react";
import {
  Upload,
  CheckCircle,
  XCircle,
  AlertCircle,
  FileText,
  User,
  GraduationCap,
  Briefcase,
  Home,
  Heart,
  Award,
} from "lucide-react";
import {
  Accordion,
  AccordionItem,
  AccordionTrigger,
  AccordionContent,
} from "@/components/ui/accordion";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { cn } from "@/lib/utils";
import { produce } from "immer";
import toast from "react-hot-toast";
import { userStore } from "@/lib/store";
import { docUpload } from "@/services/gramsevak";
import { getDocuments } from "@/services/upload";
import { useNavigate } from "react-router-dom";
import WithAuthentication from "@/components/hoc/withAuthentication";
import WithPermission from "@/components/hoc/withPermissions";
import WithHeadLayout from "@/components/layout/WithHeadLayout";

const DocumentUpload = () => {
  const navigate = useNavigate();
  const user = userStore((state) => state.user);
  const markDocumentUploadComplete = userStore(
    (state) => state.markDocumentUploadComplete
  );

  const [documentTypes, setDocumentTypes] = useState([]);
  const [activeCategory, setActiveCategory] = useState(null);
  const [selectedDocType, setSelectedDocType] = useState(null);
  const [fieldValues, setFieldValues] = useState({});
  const [validationResult, setValidationResult] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);
  const [isValidating, setIsValidating] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [loading, setLoading] = useState(true);
  const [uploadedDocuments, setUploadedDocuments] = useState(new Set());

  // Category icons mapping
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

  // Category labels in Marathi
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

  // Load document types from API
  useEffect(() => {
    const fetchDocuments = async () => {
      try {
        setLoading(true);
        const response = await getDocuments();

        if (response.status === "success") {
          setDocumentTypes(response.data.documentTypes || []);
        } else {
          toast.error("कागदपत्रे मिळवू शकत नाही");
        }
      } catch (error) {
        console.error("Error fetching documents:", error);
        toast.error("कागदपत्रे लोड करताना त्रुटी आली");
      } finally {
        setLoading(false);
      }
    };

    fetchDocuments();
  }, []);

  const handleFieldChange = (fieldName, value) => {
    const newFieldValues = { ...fieldValues, [fieldName]: value };
    setFieldValues(newFieldValues);

    // Clear previous validation when user changes fields
    if (validationResult) {
      setValidationResult(null);
    }
  };

  const validateFields = async () => {
    if (!selectedDocType) return;

    setIsValidating(true);

    // Simulate API call for validation
    setTimeout(() => {
      const errors = [];
      const fieldResults = {};

      // Validate each field based on field definitions
      Object.entries(selectedDocType.fieldDefinitions || {}).forEach(
        ([fieldName, fieldDef]) => {
          const value = fieldValues[fieldName];
          const fieldErrors = [];

          // Required field check
          if (fieldDef.required && (!value || value.toString().trim() === "")) {
            fieldErrors.push(`${fieldDef.label} is required`);
          }

          // Pattern validation for text fields
          if (value && fieldDef.pattern) {
            const regex = new RegExp(fieldDef.pattern);
            if (!regex.test(value)) {
              fieldErrors.push(
                fieldDef.validation_message ||
                  `Invalid ${fieldDef.label} format`
              );
            }
          }

          // Number validation
          if (value && fieldDef.type === "number") {
            const numValue = parseFloat(value);
            if (isNaN(numValue)) {
              fieldErrors.push(`${fieldDef.label} must be a valid number`);
            } else {
              if (fieldDef.min !== undefined && numValue < fieldDef.min) {
                fieldErrors.push(
                  `${fieldDef.label} must be at least ${fieldDef.min}`
                );
              }
              if (fieldDef.max !== undefined && numValue > fieldDef.max) {
                fieldErrors.push(
                  `${fieldDef.label} must be at most ${fieldDef.max}`
                );
              }
            }
          }

          fieldResults[fieldName] = {
            valid: fieldErrors.length === 0,
            errors: fieldErrors,
          };

          errors.push(...fieldErrors);
        }
      );

      const result = {
        valid: errors.length === 0,
        errors,
        fieldResults,
      };

      setValidationResult(result);
      setIsValidating(false);
    }, 1000);
  };

  const handleUpload = async () => {
    if (!selectedFile || !validationResult?.valid) return;

    setIsUploading(true);

    try {
      const formData = new FormData();
      formData.append(selectedDocType.documentTypeId.toString(), selectedFile);

      // Add field values to form data
      Object.entries(fieldValues).forEach(([key, value]) => {
        formData.append(`${selectedDocType.documentTypeId}_${key}`, value);
      });

      const response = await docUpload(formData);

      if (response.status === "success") {
        toast.success(
          `${selectedDocType.documentTypeName} यशस्वीरित्या अपलोड केले!`
        );

        // Add to uploaded documents
        setUploadedDocuments(
          (prev) => new Set([...prev, selectedDocType.documentTypeId])
        );

        // Reset form
        setSelectedDocType(null);
        setFieldValues({});
        setValidationResult(null);
        setSelectedFile(null);
        setActiveCategory(null);

        // Check if all mandatory documents are uploaded
        const mandatoryDocs = documentTypes.filter((doc) => doc.isMandatory);
        const uploadedMandatory = mandatoryDocs.filter(
          (doc) =>
            uploadedDocuments.has(doc.documentTypeId) ||
            doc.documentTypeId === selectedDocType.documentTypeId
        );

        if (uploadedMandatory.length === mandatoryDocs.length) {
          markDocumentUploadComplete();
          navigate("/");
        }
      } else {
        toast.error("कागदपत्रे अपलोड करता आली नाहीत, कृपया पुन्हा प्रयत्न करा");
      }
    } catch (error) {
      console.error("Upload error:", error);
      toast.error("अपलोड करताना त्रुटी आली");
    } finally {
      setIsUploading(false);
    }
  };

  const renderField = (fieldName, fieldDef) => {
    const value = fieldValues[fieldName] || "";
    const fieldResult = validationResult?.fieldResults?.[fieldName];
    const hasError = fieldResult && !fieldResult.valid;

    const baseInputClasses = `w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
      hasError ? "border-red-500" : "border-gray-300"
    }`;

    return (
      <div key={fieldName} className="mb-4">
        <label className="block text-sm font-medium text-gray-700 mb-1">
          {fieldDef.label}
          {fieldDef.required && <span className="text-red-500 ml-1">*</span>}
        </label>
        <p className="text-xs text-gray-500 mb-2">{fieldDef.label_marathi}</p>

        {fieldDef.type === "text" && (
          <input
            type="text"
            value={value}
            placeholder={fieldDef.placeholder}
            onChange={(e) => handleFieldChange(fieldName, e.target.value)}
            className={baseInputClasses}
          />
        )}

        {fieldDef.type === "number" && (
          <input
            type="number"
            value={value}
            min={fieldDef.min}
            max={fieldDef.max}
            step={fieldDef.step}
            onChange={(e) => handleFieldChange(fieldName, e.target.value)}
            className={baseInputClasses}
          />
        )}

        {fieldDef.type === "date" && (
          <input
            type="date"
            value={value}
            onChange={(e) => handleFieldChange(fieldName, e.target.value)}
            className={baseInputClasses}
          />
        )}

        {fieldDef.type === "select" && (
          <select
            value={value}
            onChange={(e) => handleFieldChange(fieldName, e.target.value)}
            className={baseInputClasses}
          >
            <option value="">Select {fieldDef.label}</option>
            {fieldDef.options?.map((option) => (
              <option key={option} value={option}>
                {option}
              </option>
            ))}
          </select>
        )}

        {fieldDef.type === "textarea" && (
          <textarea
            value={value}
            placeholder={fieldDef.placeholder}
            onChange={(e) => handleFieldChange(fieldName, e.target.value)}
            className={baseInputClasses}
            rows={3}
          />
        )}

        {hasError && (
          <div className="mt-1 text-sm text-red-600">
            {fieldResult.errors.map((error, idx) => (
              <div key={idx} className="flex items-center">
                <XCircle className="w-4 h-4 mr-1" />
                {error}
              </div>
            ))}
          </div>
        )}
      </div>
    );
  };

  // Group documents by category
  const groupedDocuments = documentTypes.reduce((acc, docType) => {
    if (!acc[docType.category]) {
      acc[docType.category] = [];
    }
    acc[docType.category].push(docType);
    return acc;
  }, {});

  if (loading) {
    return (
      <div className="w-full flex justify-center">
        <div className="min-h-screen flex items-center justify-center">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
            <p className="mt-4 text-gray-600">कागदपत्रे लोड करत आहे...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="w-full flex justify-center">
      <div className="min-h-screen flex items-start justify-center py-8">
        <div className="w-full max-w-6xl p-8 space-y-6 bg-white rounded-lg shadow-lg">
          <div>
            <h1 className="text-3xl font-bold text-gray-800 mb-2">
              कागदपत्रे अपलोड करा
            </h1>
            <p className="text-gray-600">
              कृपया खालील कागदपत्रे अपलोड करा. तारांकन (*) असलेली कागदपत्रे
              अनिवार्य आहेत.
            </p>
          </div>

          {/* Document Type Selection by Category */}
          <div className="mb-8">
            <h3 className="text-xl font-semibold text-gray-700 mb-4">
              कागदपत्राचा प्रकार निवडा
            </h3>

            <Accordion
              type="single"
              collapsible
              value={activeCategory}
              onValueChange={(newCategory) => {
                setActiveCategory(newCategory);
                setSelectedDocType(null);
                setFieldValues({});
                setValidationResult(null);
                setSelectedFile(null);
              }}
              className="w-full space-y-4"
            >
              {Object.entries(groupedDocuments).map(([category, docs]) => (
                <AccordionItem key={category} value={category}>
                  <AccordionTrigger className="bg-slate-100 rounded-md gap-4 px-4">
                    <div className="flex items-center gap-2">
                      {categoryIcons[category]}
                      <span>{categoryLabels[category] || category}</span>
                      <span className="text-sm text-gray-500">
                        ({docs.filter((d) => d.isMandatory).length} अनिवार्य,{" "}
                        {docs.filter((d) => !d.isMandatory).length} ऐच्छिक)
                      </span>
                    </div>
                  </AccordionTrigger>
                  <AccordionContent>
                    <div className="flex flex-wrap gap-4 p-4">
                      {docs.map((docType) => {
                        const isUploaded = uploadedDocuments.has(
                          docType.documentTypeId
                        );
                        return (
                          <div
                            key={docType.documentTypeId}
                            onClick={() => {
                              if (!isUploaded) {
                                setSelectedDocType(docType);
                                setFieldValues({});
                                setValidationResult(null);
                                setSelectedFile(null);
                              }
                            }}
                            className={cn(
                              "p-4 border rounded-lg cursor-pointer transition-all hover:shadow-md relative",
                              selectedDocType?.documentTypeId ===
                                docType.documentTypeId
                                ? "border-blue-500 bg-blue-50"
                                : isUploaded
                                ? "border-green-500 bg-green-50 cursor-not-allowed"
                                : "border-gray-200 hover:border-gray-300"
                            )}
                          >
                            {isUploaded && (
                              <div className="absolute top-2 right-2">
                                <CheckCircle className="w-5 h-5 text-green-600" />
                              </div>
                            )}
                            <div className="flex items-center justify-between mb-2">
                              <span className="font-medium text-gray-800">
                                {docType.documentTypeNameEnglish}
                              </span>
                              {docType.isMandatory && (
                                <span className="bg-red-100 text-red-600 text-xs px-2 py-1 rounded">
                                  अनिवार्य
                                </span>
                              )}
                            </div>
                            <p className="text-sm text-gray-600">
                              {docType.documentTypeName}
                            </p>
                            {isUploaded && (
                              <p className="text-xs text-green-600 mt-1">
                                अपलोड झाले
                              </p>
                            )}
                          </div>
                        );
                      })}
                    </div>

                    {/* Document Details Form */}
                    {selectedDocType &&
                    activeCategory === category &&
                    selectedDocType.category === category ? (
                      <div className="border-t pt-6 mx-4">
                        <h3 className="text-xl font-semibold text-gray-700 mb-4">
                          {selectedDocType.documentTypeNameEnglish} तपशील
                        </h3>

                        <div className="bg-blue-50 p-4 rounded-lg mb-6">
                          <div className="flex items-start">
                            <AlertCircle className="w-5 h-5 text-blue-600 mr-2 mt-0.5 flex-shrink-0" />
                            <p className="text-sm text-blue-800">
                              {selectedDocType.instructions}
                            </p>
                          </div>
                        </div>

                        {/* Dynamic Field Inputs */}
                        {selectedDocType.fieldDefinitions &&
                          Object.keys(selectedDocType.fieldDefinitions).length >
                            0 && (
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                              {Object.entries(
                                selectedDocType.fieldDefinitions
                              ).map(([fieldName, fieldDef]) =>
                                renderField(fieldName, fieldDef)
                              )}
                            </div>
                          )}

                        {/* File Upload */}
                        <div className="mb-6">
                          <label className="block text-sm font-medium text-gray-700 mb-2">
                            कागदपत्र अपलोड करा
                          </label>
                          <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-gray-400 transition-colors">
                            <input
                              type="file"
                              onChange={(e) =>
                                setSelectedFile(e.target.files[0])
                              }
                              className="hidden"
                              id="file-upload"
                              accept={selectedDocType.allowedFormats
                                ?.map((format) => `.${format}`)
                                .join(",")}
                            />
                            <label
                              htmlFor="file-upload"
                              className="cursor-pointer"
                            >
                              <Upload className="w-8 h-8 text-gray-400 mx-auto mb-2" />
                              <p className="text-sm text-gray-600">
                                {selectedFile
                                  ? selectedFile.name
                                  : "फाईल निवडण्यासाठी क्लिक करा किंवा ड्रॅग अँड ड्रॉप करा"}
                              </p>
                              <p className="text-xs text-gray-500 mt-1">
                                {selectedDocType.allowedFormats
                                  ?.join(", ")
                                  .toUpperCase()}{" "}
                                (Max {selectedDocType.maxFileSizeMb}MB)
                              </p>
                            </label>
                          </div>
                        </div>

                        {/* Validation Results */}
                        {validationResult && (
                          <div
                            className={`p-4 rounded-lg mb-6 ${
                              validationResult.valid
                                ? "bg-green-50 border border-green-200"
                                : "bg-red-50 border border-red-200"
                            }`}
                          >
                            <div className="flex items-center mb-2">
                              {validationResult.valid ? (
                                <CheckCircle className="w-5 h-5 text-green-600 mr-2" />
                              ) : (
                                <XCircle className="w-5 h-5 text-red-600 mr-2" />
                              )}
                              <span
                                className={`font-medium ${
                                  validationResult.valid
                                    ? "text-green-800"
                                    : "text-red-800"
                                }`}
                              >
                                {validationResult.valid
                                  ? "सर्व फील्ड योग्य आहेत!"
                                  : "कृपया खालील त्रुटी सुधारा:"}
                              </span>
                            </div>
                            {!validationResult.valid && (
                              <ul className="text-sm text-red-700 list-disc list-inside space-y-1">
                                {validationResult.errors.map((error, idx) => (
                                  <li key={idx}>{error}</li>
                                ))}
                              </ul>
                            )}
                          </div>
                        )}

                        {/* Action Buttons */}
                        <div className="flex gap-4">
                          <button
                            onClick={validateFields}
                            disabled={isValidating}
                            className="px-6 py-3 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
                          >
                            {isValidating ? (
                              <>
                                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                                तपासत आहे...
                              </>
                            ) : (
                              "फील्ड तपासा"
                            )}
                          </button>

                          <button
                            onClick={handleUpload}
                            disabled={
                              !validationResult?.valid ||
                              !selectedFile ||
                              isUploading
                            }
                            className="px-6 py-3 bg-green-600 text-white rounded-md hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
                          >
                            {isUploading ? (
                              <>
                                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                                अपलोड करत आहे...
                              </>
                            ) : (
                              "कागदपत्र अपलोड करा"
                            )}
                          </button>

                          <button
                            onClick={() => {
                              setSelectedDocType(null);
                              setFieldValues({});
                              setValidationResult(null);
                              setSelectedFile(null);
                            }}
                            className="px-6 py-3 bg-gray-600 text-white rounded-md hover:bg-gray-700"
                          >
                            फॉर्म साफ करा
                          </button>
                        </div>
                      </div>
                    ) : (
                      activeCategory === category && (
                        <div className="text-center py-8 text-gray-500">
                          कागदपत्राचा प्रकार निवडा
                        </div>
                      )
                    )}
                  </AccordionContent>
                </AccordionItem>
              ))}
            </Accordion>
          </div>

          {/* Upload Progress Summary */}
          {documentTypes.length > 0 && (
            <div className="bg-gray-50 p-4 rounded-lg">
              <h4 className="font-semibold text-gray-700 mb-2">प्रगती</h4>
              <div className="text-sm text-gray-600">
                <p>एकूण कागदपत्रे: {documentTypes.length}</p>
                <p>
                  अनिवार्य: {documentTypes.filter((d) => d.isMandatory).length}
                </p>
                <p>अपलोड झालेली: {uploadedDocuments.size}</p>
                <p>
                  बाकी:{" "}
                  {documentTypes.filter((d) => d.isMandatory).length -
                    Array.from(uploadedDocuments).filter(
                      (id) =>
                        documentTypes.find((d) => d.documentTypeId === id)
                          ?.isMandatory
                    ).length}{" "}
                  अनिवार्य
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default WithAuthentication(
  WithPermission("uploaddocs")(WithHeadLayout(DocumentUpload))
);
