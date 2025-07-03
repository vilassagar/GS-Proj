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
} from "lucide-react";

const DocumentUploadForm = () => {
  const [documentTypes, setDocumentTypes] = useState([]);
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
    address_proof: <FileText className="w-5 h-5" />,
    caste_category: <FileText className="w-5 h-5" />,
    medical: <FileText className="w-5 h-5" />,
  };

  // Sample document types data (would come from API)
  useEffect(() => {
    const sampleDocumentTypes = [
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
        },
      },
    ];
    setDocumentTypes(sampleDocumentTypes);
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

  return (
    <div className="max-w-4xl mx-auto p-6 bg-white rounded-lg shadow-lg">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">Document Upload</h2>

      {/* Document Type Selection */}
      <div className="mb-6">
        <h3 className="text-lg font-semibold text-gray-700 mb-3">
          Select Document Type
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {documentTypes.map((docType) => (
            <div
              key={docType.documentTypeId}
              onClick={() => {
                setSelectedDocType(docType);
                setFieldValues({});
                setValidationResult(null);
              }}
              className={`p-4 border rounded-lg cursor-pointer transition-all hover:shadow-md ${
                selectedDocType?.documentTypeId === docType.documentTypeId
                  ? "border-blue-500 bg-blue-50"
                  : "border-gray-200 hover:border-gray-300"
              }`}
            >
              <div className="flex items-center mb-2">
                {categoryIcons[docType.category]}
                <span className="ml-2 font-medium text-gray-800">
                  {docType.nameEnglish}
                </span>
                {docType.isMandatory && (
                  <span className="ml-2 bg-red-100 text-red-800 text-xs px-2 py-1 rounded">
                    Required
                  </span>
                )}
              </div>
              <p className="text-sm text-gray-600">{docType.name}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Document Details Form */}
      {selectedDocType && (
        <div className="border-t pt-6">
          <h3 className="text-lg font-semibold text-gray-700 mb-3">
            {selectedDocType.nameEnglish} Details
          </h3>

          <div className="bg-blue-50 p-4 rounded-lg mb-6">
            <div className="flex items-start">
              <AlertCircle className="w-5 h-5 text-blue-600 mr-2 mt-0.5" />
              <p className="text-sm text-blue-800">
                {selectedDocType.instructions}
              </p>
            </div>
          </div>

          {/* Field Inputs */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
            {Object.entries(selectedDocType.fieldDefinitions).map(
              ([fieldName, fieldDef]) => renderField(fieldName, fieldDef)
            )}
          </div>

          {/* File Upload */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Upload Document File
            </label>
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
              <input
                type="file"
                onChange={(e) => setSelectedFile(e.target.files[0])}
                className="hidden"
                id="file-upload"
                accept=".pdf,.jpg,.jpeg,.png,.doc,.docx"
              />
              <label htmlFor="file-upload" className="cursor-pointer">
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
                    validationResult.valid ? "text-green-800" : "text-red-800"
                  }`}
                >
                  {validationResult.valid
                    ? "All fields are valid!"
                    : "Please fix the following errors:"}
                </span>
              </div>
              {!validationResult.valid && (
                <ul className="text-sm text-red-700 list-disc list-inside">
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
              className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isValidating ? "Validating..." : "Validate Fields"}
            </button>

            <button
              onClick={handleUpload}
              disabled={
                !validationResult?.valid || !selectedFile || isUploading
              }
              className="px-6 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isUploading ? "Uploading..." : "Upload Document"}
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default DocumentUploadForm;
