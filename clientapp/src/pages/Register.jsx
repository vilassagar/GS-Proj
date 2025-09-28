import { userDesignations } from "@/common/constants";
import WithAuthLayout from "@/components/layout/WithAuthLayout";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import RSelect from "@/components/ui/RSelect";
import { getRegistrationPayload } from "@/lib/helperFunctions";
import { register } from "@/services/auth";
import {
  getBlocksByDistrictId,
  getDesignations,
  getDistricts,
  getPanchayatByBlockId,
} from "@/services/preset";
import { produce } from "immer";
import { useEffect, useState } from "react";
import toast from "react-hot-toast";
import { useNavigate } from "react-router-dom";

function Register() {
  const navigate = useNavigate();
  const [designations, setDesignations] = useState([]);
  const [districts, setDistricts] = useState([]);
  const [blocks, setBlocks] = useState([]);
  const [panchayats, setPanchayats] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [formData, setFormData] = useState({
    firstName: "",
    lastName: "",
    designation: null,
    currentZillaParishad: null,
    currentPanchayatSamiti: null,
    currentGramPanchayatName: null,
    mobileNumber: "",
    whatsappMobileNumber: "",
    emailId: "",
  });

  useEffect(() => {
    const fetchInitialData = async () => {
      try {
        setIsLoading(true);
        const [districtsResponse] = await Promise.all([getDistricts()]);

        setDesignations(userDesignations);

        if (districtsResponse?.status === "success") {
          setDistricts(districtsResponse.data);
        } else {
          toast.error("जिल्हे मिळवू शकत नाही");
        }
      } catch (error) {
        console.error("Error fetching initial data:", error);
        toast.error("प्रारंभिक डेटा लोड करताना त्रुटी");
      } finally {
        setIsLoading(false);
      }
    };

    fetchInitialData();
  }, []);

  const handleChange = (name) => async (e) => {
    let nextState = produce(formData, (draft) => {
      switch (name) {
        case "firstName":
        case "lastName":
        case "emailId":
        case "whatsappMobileNumber":
          draft[name] = e.target.value;
          break;
        case "designation":
        case "currentZillaParishad":
        case "currentPanchayatSamiti":
        case "currentGramPanchayatName":
          draft[name] = e;
          break;
        case "mobileNumber":
          // Only store the 10-digit number, not with +91 prefix
          const number = e.target.value.replace(/\D/g, ""); // Remove non-digits
          if (number.length <= 10) {
            draft[name] = number;
          }
          break;
        default:
          break;
      }
    });
    setFormData(nextState);

    // Fetch blocks when district changes
    if (name === "currentZillaParishad" && e?.districtId) {
      try {
        const response = await getBlocksByDistrictId(e.districtId);
        if (response?.status === "success") {
          setBlocks(response.data);
          // Reset dependent fields
          setFormData((prev) =>
            produce(prev, (draft) => {
              draft.currentPanchayatSamiti = null;
              draft.currentGramPanchayatName = null;
            })
          );
          setPanchayats([]);
        } else {
          toast.error("ब्लॉक मिळवू शकत नाही");
        }
      } catch (error) {
        console.error("Error fetching blocks:", error);
        toast.error("ब्लॉक लोड करताना त्रुटी");
      }
    }

    // Fetch panchayats when block changes
    if (name === "currentPanchayatSamiti" && e?.blockId) {
      try {
        const response = await getPanchayatByBlockId(e.blockId);
        if (response?.status === "success") {
          setPanchayats(response.data);
          // Reset dependent field
          setFormData((prev) =>
            produce(prev, (draft) => {
              draft.currentGramPanchayatName = null;
            })
          );
        } else {
          toast.error("ग्राम पंचायत मिळवू शकत नाही");
        }
      } catch (error) {
        console.error("Error fetching panchayats:", error);
        toast.error("ग्राम पंचायत लोड करताना त्रुटी");
      }
    }
  };

  const validateForm = () => {
    const errors = [];

    if (!formData.firstName.trim()) errors.push("पहिले नाव आवश्यक आहे");
    if (!formData.lastName.trim()) errors.push("आडनाव आवश्यक आहे");
    if (!formData.designation) errors.push("पदनाम निवडा");
    if (!formData.currentZillaParishad) errors.push("जिल्हा परिषद निवडा");
    if (!formData.currentPanchayatSamiti) errors.push("पंचायत समिती निवडा");
    if (!formData.currentGramPanchayatName) errors.push("ग्राम पंचायत निवडा");

    // Mobile number validation
    if (!formData.mobileNumber || formData.mobileNumber.length !== 10) {
      errors.push("10 अंकी मोबाईल नंबर आवश्यक आहे");
    }

    if (!formData.whatsappMobileNumber.trim()) {
      errors.push("व्हॉट्सअॅप नंबर आवश्यक आहे");
    }

    // Email validation
    if (!formData.emailId.trim()) {
      errors.push("ई-मेल आवश्यक आहे");
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.emailId)) {
      errors.push("वैध ई-मेल पत्ता प्रविष्ट करा");
    }

    return errors;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const validationErrors = validateForm();
    if (validationErrors.length > 0) {
      validationErrors.forEach((error) => toast.error(error));
      return;
    }

    try {
      setIsSubmitting(true);

      // Prepare payload with +91 prefix for mobile number
      const payloadData = {
        ...formData,
        mobileNumber: `+91${formData.mobileNumber}`,
      };

      const payload = getRegistrationPayload(payloadData);
      const response = await register(payload);

      if (response?.status === "success") {
        toast.success("नोंदणी यशस्वी झाली");
        navigate("/login");
      } else {
        toast.error(
          response?.message || "नोंदणी करू शकत नाही, कृपया पुन्हा प्रयत्न करा"
        );
      }
    } catch (error) {
      console.error("Registration error:", error);
      toast.error("नोंदणी करताना त्रुटी आली");
    } finally {
      setIsSubmitting(false);
    }
  };

  if (isLoading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">लोड करत आहे...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex justify-center items-center min-h-screen p-4">
      <Card className="w-full max-w-2xl">
        <CardHeader>
          <CardTitle>नोंदणी फॉर्म</CardTitle>
          <CardDescription>कृपया आवश्यक सर्व माहिती भरा.</CardDescription>
        </CardHeader>
        <form onSubmit={handleSubmit}>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="firstName">
                  पहिले नाव <span className="text-red-500 ml-1">*</span>
                </Label>
                <Input
                  id="firstName"
                  name="firstName"
                  value={formData.firstName}
                  onChange={handleChange("firstName")}
                  required
                  lang="mr"
                  placeholder="पहिले नाव प्रविष्ट करा"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="lastName">
                  आडनाव <span className="text-red-500 ml-1">*</span>
                </Label>
                <Input
                  id="lastName"
                  name="lastName"
                  value={formData.lastName}
                  onChange={handleChange("lastName")}
                  required
                  lang="mr"
                  placeholder="आडनाव प्रविष्ट करा"
                />
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="designation">
                पदनाम <span className="text-red-500 ml-1">*</span>
              </Label>
              <RSelect
                id="designation"
                options={designations}
                nameProperty="designationName"
                valueProperty="designationId"
                value={formData.designation}
                onChange={handleChange("designation")}
                placeholder="पदनाम निवडा"
                isRequired={true}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="currentZillaParishad">
                वर्तमान जिल्हा परिषद{" "}
                <span className="text-red-500 ml-1">*</span>
              </Label>
              <RSelect
                id="ditrictName"
                options={districts}
                nameProperty="districtName"
                valueProperty="districtId"
                value={formData.currentZillaParishad}
                onChange={handleChange("currentZillaParishad")}
                placeholder="जिल्हा निवडा"
                isRequired={true}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="currentPanchayatSamiti">
                वर्तमान पंचायत समिती{" "}
                <span className="text-red-500 ml-1">*</span>
              </Label>
              <RSelect
                id="blocks"
                options={blocks}
                nameProperty="blockName"
                valueProperty="blockId"
                value={formData.currentPanchayatSamiti}
                onChange={handleChange("currentPanchayatSamiti")}
                placeholder="पंचायत समिती निवडा"
                isDisabled={!formData.currentZillaParishad}
                isRequired={true}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="currentGramPanchayatName">
                वर्तमान ग्राम पंचायत नाव{" "}
                <span className="text-red-500 ml-1">*</span>
              </Label>
              <RSelect
                id="panchayat"
                options={panchayats}
                nameProperty="gramPanchayatName"
                valueProperty="gramPanchayatId"
                value={formData.currentGramPanchayatName}
                onChange={handleChange("currentGramPanchayatName")}
                placeholder="ग्राम पंचायत निवडा"
                isDisabled={!formData.currentPanchayatSamiti}
                isRequired={true}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="mobileNumber">
                मोबाईल नंबर <span className="text-red-500 ml-1">*</span>
              </Label>
              <div className="relative">
                <span className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500 text-sm font-medium">
                  +91
                </span>
                <Input
                  id="mobileNumber"
                  name="mobileNumber"
                  type="tel"
                  value={formData.mobileNumber}
                  onChange={handleChange("mobileNumber")}
                  required
                  maxLength={10}
                  pattern="[0-9]{10}"
                  placeholder="1234567890"
                  className="pl-12"
                />
              </div>
              <p className="text-xs text-gray-500">
                10 अंकी मोबाईल नंबर प्रविष्ट करा
              </p>
            </div>

            <div className="space-y-2">
              <Label htmlFor="whatsappMobileNumber">
                व्हॉट्सअॅप मोबाईल नंबर{" "}
                <span className="text-red-500 ml-1">*</span>
              </Label>
              <Input
                id="whatsappMobileNumber"
                name="whatsappMobileNumber"
                type="tel"
                value={formData.whatsappMobileNumber}
                onChange={handleChange("whatsappMobileNumber")}
                required
                placeholder="व्हॉट्सअॅप नंबर प्रविष्ट करा"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="emailId">
                ई-मेल आयडी <span className="text-red-500 ml-1">*</span>
              </Label>
              <Input
                id="emailId"
                name="emailId"
                type="email"
                value={formData.emailId}
                onChange={handleChange("emailId")}
                required
                placeholder="example@email.com"
              />
            </div>
          </CardContent>

          <CardFooter>
            <Button type="submit" className="w-full" disabled={isSubmitting}>
              {isSubmitting ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                  नोंदणी करत आहे...
                </>
              ) : (
                "नोंदणी करा"
              )}
            </Button>
          </CardFooter>
        </form>
      </Card>
    </div>
  );
}

export default WithAuthLayout(Register);
