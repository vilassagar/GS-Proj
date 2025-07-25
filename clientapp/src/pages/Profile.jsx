import WithLayout from "@/components/layout/WithLayout";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { userDesignations } from "@/common/constants";
import FileUpload from "@/components/common/FileUpload";
import WithAuthentication from "@/components/hoc/withAuthentication";
import WithPermission from "@/components/hoc/withPermissions";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import RSelect from "@/components/ui/RSelect";
import { userStore } from "@/lib/store";
import { getGramSevakById } from "@/services/gramsevak";
import { documentMasterList } from "@/common/constants";
import {
  getBlocksByDistrictId,
  getDistricts,
  getPanchayatByBlockId,
} from "@/services/preset";
import { useEffect, useState } from "react";
import toast from "react-hot-toast";
import DocumentUpload from "./DocumentUpload";

const DocumentUploadSection = ({ doc }) => {
  const [file, setFile] = useState(null);
  const [inputFields, setInputFields] = useState({});

  const handleFileChange = (f) => {
    setFile(f);
  };

  const handleFieldChange = (name, value) => {
    setInputFields((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = () => {
    if (!file) {
      return toast.error(`कृपया "${doc.marathiName}" साठी फाईल अपलोड करा.`);
    }

    if (doc.fields) {
      for (const field of doc.fields) {
        if (field.required && !inputFields[field.name]) {
          return toast.error(`कृपया "${field.label}" भरावे.`);
        }
      }
    }

    const formData = new FormData();
    formData.append("file", file);
    doc.fields?.forEach((f) => {
      formData.append(f.name, inputFields[f.name] || "");
    });
    formData.append("documentType", doc.englishName);

    const formPayload = {
      documentType: doc.englishName,
      file: {
        id: 0,
        name: file?.name || "",
        file: file || {},
      },
    };

    // Add dynamic input fields
    doc.fields?.forEach((f) => {
      formPayload[f.name] = inputFields[f.name] || "";
    });

    // Now log the object
    console.log("Form Payload:", formPayload, file);

    toast.success(`${doc.marathiName} यशस्वीरित्या सबमिट झाले.`);
  };

  return (
    <div className="border rounded-lg p-4 shadow-md bg-white space-y-2">
      <h2 className="font-bold text-lg text-gray-800">
        {doc.marathiName}{" "}
        {doc.required && <span className="text-red-500">*</span>}
      </h2>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* File Upload */}
        <div className="space-y-2">
          <Label>
            अपलोड करा {doc.required && <span className="text-red-500">*</span>}
          </Label>
          <FileUpload value={file} onChange={handleFileChange} />
        </div>

        {/* Dynamic Input Fields */}
        {doc.fields?.map((field) => {
          return (
            <div className="space-y-1" key={field.name}>
              <Label>
                {field.label}{" "}
                {field.required && <span className="text-red-500">*</span>}
              </Label>

              {field.type === "text" && (
                <Input
                  placeholder={field.placeholder}
                  value={inputFields[field.name] || ""}
                  onChange={(e) =>
                    handleFieldChange(field.name, e.target.value)
                  }
                />
              )}

              {field.type === "select" && (
                <select
                  className="border p-2 rounded w-full"
                  value={inputFields[field.name] || ""}
                  onChange={(e) =>
                    handleFieldChange(field.name, e.target.value)
                  }
                >
                  <option value="">-- निवडा --</option>
                  {field.options.map((opt, i) => (
                    <option key={i} value={opt}>
                      {opt}
                    </option>
                  ))}
                </select>
              )}

              {field.type === "radio" && (
                <div className="flex space-x-4">
                  {field.options.map((opt, i) => (
                    <label key={i} className="flex items-center space-x-1">
                      <input
                        type="radio"
                        name={field.name}
                        value={opt}
                        checked={inputFields[field.name] === opt}
                        onChange={(e) =>
                          handleFieldChange(field.name, e.target.value)
                        }
                      />
                      <span>{opt}</span>
                    </label>
                  ))}
                </div>
              )}
            </div>
          );
        })}
      </div>

      <div className="text-right pt-2">
        <button
          onClick={handleSubmit}
          className="bg-blue-600 text-white px-6 py-2 rounded-lg"
        >
          सबमिट करा
        </button>
      </div>
    </div>
  );
};

function BasicDetails({ data, designations, districts, blocks, panchayats }) {
  useEffect(() => {
    (() => {})();
  }, [data]);

  return (
    <Card>
      <CardContent className="space-y-4 pt-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="space-y-2">
            <Label htmlFor="firstName">पहिले नाव</Label>
            <Input
              id="firstName"
              name="firstName"
              value={data?.firstName}
              required
              lang="mr"
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="lastName">आडनाव</Label>
            <Input
              id="lastName"
              name="lastName"
              value={data?.lastName}
              required
              lang="mr"
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="designation">हुद्दा</Label>
            <RSelect
              id="designation"
              options={designations}
              nameProperty="designationName"
              valueProperty="designationId"
              value={data?.designation}
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="currentZillaParishad">सध्याची जिल्हा परिषद</Label>
            <RSelect
              id="ditrictName"
              options={districts}
              nameProperty="districtName"
              valueProperty="districtId"
              value={data?.district}
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="currentPanchayatSamiti">सध्याची पंचायत समिती</Label>
            <RSelect
              id="blocks"
              options={blocks}
              nameProperty="blockName"
              valueProperty="blockId"
              value={data?.block}
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="currentGramPanchayatName">
              सध्याचे ग्रामपंचायत नाव
            </Label>
            <RSelect
              id="panchayat"
              options={panchayats}
              nameProperty="gramPanchayatName"
              valueProperty="gramPanchayatId"
              value={data?.gramPanchayat}
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="mobileNumber">मोबाईल क्रमांक</Label>
            <Input
              id="mobileNumber"
              name="mobileNumber"
              type="tel"
              value={data?.mobileNumber}
              required
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="whatsappMobileNumber">
              व्हॉट्सअॅप मोबाईल क्रमांक
            </Label>
            <Input
              id="whatsappMobileNumber"
              name="whatsappMobileNumber"
              type="tel"
              value={data?.whatsappNumber}
              required
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="emailId">ईमेल आयडी</Label>
            <Input
              id="emailId"
              name="emailId"
              type="email"
              value={data?.email}
              required
            />
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

function Profile() {
  const [gramSevak, setGramSevak] = useState(null);
  const [designations, setDesignations] = useState([]);
  const [districts, setDistricts] = useState([]);
  const [blocks, setBlocks] = useState([]);
  const [panchayats, setPanchayats] = useState([]);
  const user = userStore((state) => state.user);

  useEffect(() => {
    (async () => {
      let res2 = await getDistricts();

      setDesignations(userDesignations);
      setDistricts(res2?.data);
      let response = await getGramSevakById(user?.userId);
      if (response.status === "success") {
        var basicDetails = response.data.basicDetails;
        console.log("Basic Details:", basicDetails);
        let blockResponse = await getBlocksByDistrictId(
          basicDetails?.district?.districtId
        );
        setBlocks(blockResponse?.data);

        let panchayatResponse = await getPanchayatByBlockId(
          basicDetails?.gramPanchayat?.gramPanchayatId
        );
        setPanchayats(panchayatResponse?.data);

        setGramSevak(basicDetails);
      } else {
        toast.error("Unable to get gramsevak details");
      }
    })();
  }, []);

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">प्रोफाईल</h1>
      <Tabs defaultValue="basic-details" className="w-full">
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="basic-details">मूलभूत माहिती</TabsTrigger>
          <TabsTrigger value="documents">कागदपत्रे</TabsTrigger>
        </TabsList>
        <TabsContent value="basic-details">
          <BasicDetails
            data={gramSevak}
            designations={designations}
            districts={districts}
            blocks={blocks}
            panchayats={panchayats}
          />
        </TabsContent>
        <TabsContent value="documents">
          <Card>
            <CardContent className=" pt-6 gap-4">
              {/* {documentMasterList.map((doc) => (
                <DocumentUploadSection key={doc.id} doc={doc} />
              ))} */}
              <DocumentUpload />
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
export default WithAuthentication(
  WithPermission("profile")(WithLayout(Profile))
);
