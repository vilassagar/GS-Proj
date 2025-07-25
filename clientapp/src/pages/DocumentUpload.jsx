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
import { cn } from "@/lib/utils";

const DocumentUpload = () => {
  const [documentTypes, setDocumentTypes] = useState([]);
  const [activeCategory, setActiveCategory] = useState(null);
  const [selectedDocType, setSelectedDocType] = useState(null);
  const [fieldValues, setFieldValues] = useState({});
  const [validationResult, setValidationResult] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);
  const [isValidating, setIsValidating] = useState(false);
  const [isUploading, setIsUploading] = useState(false);

  // Category icons
  const categoryIcons = {
    identity_proof: <User className="w-5 h-5" />,
    educational: <GraduationCap className="w-5 h-5" />,
    professional: <Briefcase className="w-5 h-5" />,
    address_proof: <Home className="w-5 h-5" />,
    caste_category: <Award className="w-5 h-5" />,
    medical: <Heart className="w-5 h-5" />,
  };

  // Enhanced document types data with 3 new additional types
  useEffect(() => {
    const enhancedDocumentTypes = [
      // Original document types
      {
        documentTypeId: 1,
        name: "फोटो",
        nameEnglish: "Photo",
        category: "identity_proof",
        isMandatory: true,
        instructions:
          "पासपोर्ट साइज फोटो अपलोड करा. फोटो स्पष्ट आणि अलीकडचा असावा.",
        fieldDefinitions: {
          photo_type: {
            type: "select",
            label: "Photo Type",
            label_marathi: "फोटो प्रकार",
            options: ["Passport Size", "Official"],
            required: true,
          },
          background_color: {
            type: "select",
            label: "Background Color",
            label_marathi: "पार्श्वभूमी रंग",
            options: ["White", "Blue", "Red"],
            required: false,
          },
        },
      },
      {
        documentTypeId: 2,
        name: "आधार कार्ड",
        nameEnglish: "Aadhaar Card",
        category: "identity_proof",
        isMandatory: true,
        instructions:
          "आधार कार्डाची स्पष्ट प्रत अपलोड करा. सर्व माहिती वाचता येण्यासारखी असावी.",
        fieldDefinitions: {
          aadhaar_number: {
            type: "text",
            label: "Aadhaar Number",
            label_marathi: "आधार नंबर",
            pattern: "^[0-9]{12}$",
            placeholder: "1234 5678 9012",
            required: true,
            validation_message: "Please enter a valid 12-digit Aadhaar number",
          },
          name_on_aadhaar: {
            type: "text",
            label: "Name on Aadhaar",
            label_marathi: "आधार कार्डवरील नाव",
            required: true,
          },
          date_of_birth: {
            type: "date",
            label: "Date of Birth",
            label_marathi: "जन्म तारीख",
            required: true,
          },
          address_on_aadhaar: {
            type: "textarea",
            label: "Address on Aadhaar",
            label_marathi: "आधार कार्डवरील पत्ता",
            required: false,
          },
        },
      },
      {
        documentTypeId: 3,
        name: "पॅन कार्ड",
        nameEnglish: "PAN Card",
        category: "identity_proof",
        isMandatory: true,
        instructions:
          "पॅन कार्डाची स्पष्ट प्रत अपलोड करा. पॅन नंबर स्पष्टपणे दिसत असावा.",
        fieldDefinitions: {
          pan_number: {
            type: "text",
            label: "PAN Number",
            label_marathi: "पॅन नंबर",
            pattern: "^[A-Z]{5}[0-9]{4}[A-Z]{1}$",
            placeholder: "ABCDE1234F",
            required: true,
            validation_message:
              "Please enter a valid PAN number (e.g., ABCDE1234F)",
          },
          name_on_pan: {
            type: "text",
            label: "Name on PAN",
            label_marathi: "पॅन कार्डवरील नाव",
            required: true,
          },
          father_name: {
            type: "text",
            label: "Father's Name",
            label_marathi: "वडिलांचे नाव",
            required: true,
          },
          date_of_birth_pan: {
            type: "date",
            label: "Date of Birth (as per PAN)",
            label_marathi: "जन्म तारीख (पॅन प्रमाणे)",
            required: true,
          },
        },
      },

      // THREE NEW DOCUMENT TYPES
      {
        documentTypeId: 4,
        name: "मतदार ओळखपत्र",
        nameEnglish: "Voter ID Card",
        category: "identity_proof",
        isMandatory: false,
        instructions:
          "मतदार ओळखपत्राची स्पष्ट प्रत अपलोड करा. सर्व माहिती स्पष्टपणे दिसत असावी.",
        fieldDefinitions: {
          voter_id_number: {
            type: "text",
            label: "Voter ID Number",
            label_marathi: "मतदार ओळखपत्र क्रमांक",
            pattern: "^[A-Z]{3}[0-9]{7}$",
            placeholder: "ABC1234567",
            required: true,
            validation_message:
              "Please enter a valid Voter ID number (e.g., ABC1234567)",
          },
          name_on_card: {
            type: "text",
            label: "Name on Voter ID",
            label_marathi: "मतदार ओळखपत्रावरील नाव",
            required: true,
          },
          father_husband_name: {
            type: "text",
            label: "Father/Husband Name",
            label_marathi: "वडील/पतीचे नाव",
            required: true,
          },
          assembly_constituency: {
            type: "text",
            label: "Assembly Constituency",
            label_marathi: "विधानसभा मतदारसंघ",
            required: true,
          },
          date_of_birth_voter: {
            type: "date",
            label: "Date of Birth",
            label_marathi: "जन्म तारीख",
            required: true,
          },
        },
      },
      {
        documentTypeId: 5,
        name: "उत्पन्न दाखला",
        nameEnglish: "Income Certificate",
        category: "professional",
        isMandatory: false,
        instructions:
          "सक्षम प्राधिकाऱ्याकडून जारी केलेला उत्पन्न दाखला अपलोड करा.",
        fieldDefinitions: {
          certificate_number: {
            type: "text",
            label: "Certificate Number",
            label_marathi: "प्रमाणपत्र क्रमांक",
            required: true,
          },
          annual_income: {
            type: "number",
            label: "Annual Income (₹)",
            label_marathi: "वार्षिक उत्पन्न (₹)",
            min: 0,
            required: true,
          },
          income_source: {
            type: "select",
            label: "Income Source",
            label_marathi: "उत्पन्नाचा स्रोत",
            options: ["Agriculture", "Business", "Service", "Other"],
            required: true,
          },
          issued_date: {
            type: "date",
            label: "Issue Date",
            label_marathi: "जारी केल्याची तारीख",
            required: true,
          },
          issuing_authority: {
            type: "text",
            label: "Issuing Authority",
            label_marathi: "जारीकर्ता प्राधिकरण",
            required: true,
          },
          valid_until: {
            type: "date",
            label: "Valid Until",
            label_marathi: "वैधता",
            required: true,
          },
        },
      },
      {
        documentTypeId: 6,
        name: "रहिवास दाखला",
        nameEnglish: "Residence Certificate",
        category: "address_proof",
        isMandatory: false,
        instructions:
          "तहसीलदार किंवा सक्षम प्राधिकाऱ्याकडून जारी केलेला रहिवास दाखला अपलोड करा.",
        fieldDefinitions: {
          certificate_number: {
            type: "text",
            label: "Certificate Number",
            label_marathi: "प्रमाणपत्र क्रमांक",
            required: true,
          },
          applicant_name: {
            type: "text",
            label: "Applicant Name",
            label_marathi: "अर्जदाराचे नाव",
            required: true,
          },
          residence_address: {
            type: "textarea",
            label: "Residence Address",
            label_marathi: "राहत्या पत्त्याचा तपशील",
            required: true,
          },
          district: {
            type: "text",
            label: "District",
            label_marathi: "जिल्हा",
            required: true,
          },
          taluka: {
            type: "text",
            label: "Taluka",
            label_marathi: "तालुका",
            required: true,
          },
          village_city: {
            type: "text",
            label: "Village/City",
            label_marathi: "गाव/शहर",
            required: true,
          },
          duration_of_residence: {
            type: "number",
            label: "Duration of Residence (Years)",
            label_marathi: "निवासाचा कालावधी (वर्षे)",
            min: 0,
            required: true,
          },
          issued_date: {
            type: "date",
            label: "Issue Date",
            label_marathi: "जारी केल्याची तारीख",
            required: true,
          },
          issuing_authority: {
            type: "text",
            label: "Issuing Authority",
            label_marathi: "जारीकर्ता प्राधिकरण",
            required: true,
          },
        },
      },
    ];
    setDocumentTypes(enhancedDocumentTypes);
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
      Object.entries(selectedDocType.fieldDefinitions).forEach(
        ([fieldName, fieldDef]) => {
          const value = fieldValues[fieldName];
          const fieldErrors = [];

          // Required field check
          if (fieldDef.required && (!value || value.trim() === "")) {
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

    // Simulate upload
    setTimeout(() => {
      alert("Document uploaded successfully!");
      setIsUploading(false);
      // Reset form
      setSelectedDocType(null);
      setFieldValues({});
      setValidationResult(null);
      setSelectedFile(null);
    }, 2000);
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

  const categoryLabels = {
    identity_proof: "Identity Proof",
    address_proof: "Address Proof",
    professional: "Professional/Income",
    educational: "Educational",
    caste_category: "Caste Category",
    medical: "Medical",
  };

  return (
    <div className="max-w-6xl mx-auto p-6 bg-white rounded-lg shadow-lg">
      <h2 className="text-3xl font-bold text-gray-800 mb-6">
        Document Upload System
      </h2>

      {/* Document Type Selection by Category */}
      <div className="mb-8">
        <h3 className="text-xl font-semibold text-gray-700 mb-4">
          Select Document Type
        </h3>

        <div className="">
          <div className="w-full overflow-y-auto pr-4">
            <div className="flex-col gap-6 ">
              <Accordion
                type="single"
                collapsible
                value={activeCategory}
                onValueChange={(newCategory) => {
                  setActiveCategory(newCategory);
                  setSelectedDocType(null); // Reset selected doc when switching category
                  setFieldValues({});
                  setValidationResult(null);
                  setSelectedFile(null);
                }}
                className="w-full space-y-4"
              >
                {Object.entries(groupedDocuments).map(([category, docs]) => (
                  <AccordionItem key={category} value={category}>
                    <AccordionTrigger className=" bg-slate-100 rounded-md gap-4">
                      <div className="flex items-center gap-2 ">
                        {categoryIcons[category]}
                        <span>{categoryLabels[category]}</span>
                      </div>
                    </AccordionTrigger>
                    <AccordionContent>
                      <div className="flex flex-wrap gap-4">
                        {docs.map((docType) => (
                          <div
                            key={docType.documentTypeId}
                            onClick={() => {
                              setSelectedDocType({ ...docType, category });
                              setFieldValues({});
                              setValidationResult(null);
                            }}
                            className={cn(
                              "p-4 border rounded-lg cursor-pointer transition-all hover:shadow-md",
                              selectedDocType?.documentTypeId ===
                                docType.documentTypeId
                                ? "border-blue-500 bg-blue-50"
                                : "border-gray-200 hover:border-gray-300"
                            )}
                          >
                            <div className="flex items-center justify-between mb-2">
                              <span className="font-medium text-gray-800">
                                {docType.nameEnglish}
                              </span>
                              {docType.isMandatory && (
                                <span className="bg-red-100 text-red-600 text-xs px-2 py-1 rounded">
                                  Required
                                </span>
                              )}
                            </div>
                            <p className="text-sm text-gray-600">
                              {docType.name}
                            </p>
                          </div>
                        ))}
                      </div>

                      {/* Document Details Form */}
                      {selectedDocType &&
                      activeCategory === category &&
                      selectedDocType.category === category ? (
                        <div className="border-t pt-6 w-full overflow-y-auto pr-4">
                          <h3 className="text-xl font-semibold text-gray-700 mb-4">
                            {selectedDocType.nameEnglish} Details
                          </h3>

                          <div className="bg-blue-50 p-4 rounded-lg mb-6">
                            <div className="flex items-start">
                              <AlertCircle className="w-5 h-5 text-blue-600 mr-2 mt-0.5 flex-shrink-0" />
                              <p className="text-sm text-blue-800">
                                {selectedDocType.instructions}
                              </p>
                            </div>
                          </div>

                          {/* Field Inputs */}
                          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                            {Object.entries(
                              selectedDocType.fieldDefinitions
                            ).map(([fieldName, fieldDef]) =>
                              renderField(fieldName, fieldDef)
                            )}
                          </div>

                          {/* File Upload */}
                          <div className="mb-6">
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                              Upload Document File
                            </label>
                            <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-gray-400 transition-colors">
                              <input
                                type="file"
                                onChange={(e) =>
                                  setSelectedFile(e.target.files[0])
                                }
                                className="hidden"
                                id="file-upload"
                                accept=".pdf,.jpg,.jpeg,.png,.doc,.docx"
                              />
                              <label
                                htmlFor="file-upload"
                                className="cursor-pointer"
                              >
                                <Upload className="w-8 h-8 text-gray-400 mx-auto mb-2" />
                                <p className="text-sm text-gray-600">
                                  {selectedFile
                                    ? selectedFile.name
                                    : "Click to upload or drag and drop"}
                                </p>
                                <p className="text-xs text-gray-500 mt-1">
                                  PDF, JPG, PNG, DOC, DOCX (Max 5MB)
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
                                    ? "All fields are valid!"
                                    : "Please fix the following errors:"}
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
                                  Validating...
                                </>
                              ) : (
                                "Validate Fields"
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
                                  Uploading...
                                </>
                              ) : (
                                "Upload Document"
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
                              Clear Form
                            </button>
                          </div>
                        </div>
                      ) : (
                        // <div className="h-10 w-10 border-blue-950 text-center">
                        " No Document Selcetd"
                        // </div>
                      )}
                    </AccordionContent>
                  </AccordionItem>
                ))}
              </Accordion>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DocumentUpload;
