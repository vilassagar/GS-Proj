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
    (async () => {
      let res2 = await getDistricts();

      setDesignations(userDesignations);
      setDistricts(res2?.data);
    })();
  }, []);

  const handleChange = (name) => async (e) => {
    let nextState = produce(formData, (draft) => {
      switch (name) {
        case "firstName":
        case "lastName":
          draft[name] = e.target.value;
          break;
        case "designation":
          draft[name] = e;
          break;
        case "currentZillaParishad":
          draft[name] = e;
          break;
        case "currentPanchayatSamiti":
          draft[name] = e;
          break;
        case "currentGramPanchayatName":
          draft[name] = e;
          break;
        case "mobileNumber":
          const number = e.target.value;
          draft[name] = `+91${number}`;
          break;
        case "whatsappMobileNumber":
          draft[name] = e.target.value;
          break;
        case "emailId":
          draft[name] = e.target.value;
          break;

        default:
          break;
      }
    });
    setFormData(nextState);

    // पं. स. मिळवा
    if (name === "currentZillaParishad" && e) {
      let response = await getBlocksByDistrictId(e?.districtId);
      setBlocks(response?.data);
    }

    // ग्राम पंचायत मिळवा
    if (name === "currentPanchayatSamiti" && e) {
      let response = await getPanchayatByBlockId(e?.blockId);
      setPanchayats(response?.data);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    let payload = getRegistrationPayload(formData);

    let response = await register(payload);
    if (response?.status === "success") {
      navigate("/login");
      toast.success("नोंदणी यशस्वी झाली");
    } else {
      toast.error("नोंदणी करू शकत नाही, कृपया पुन्हा प्रयत्न करा");
    }
  };

  return (
    <div className="flex justify-center items-center min-h-screen ">
      <Card className="w-full max-w-2xl">
        <CardHeader>
          <CardTitle>नोंदणी फॉर्म</CardTitle>
          <CardDescription>कृपया आवश्यक सर्व माहिती भरा.</CardDescription>
        </CardHeader>
        <form onSubmit={handleSubmit}>
          <CardContent className="space-y-4">
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
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="designation">
                पदनाम <span className="text-red-500 ml-1">*</span>
              </Label>
              <RSelect
                id="designation"
                options={designations}
                nameProperty="designationName"
                required
                valueProperty="designationId"
                value={formData.designation}
                onChange={handleChange("designation")}
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
                required
                valueProperty="districtId"
                value={formData.currentZillaParishad}
                onChange={handleChange("currentZillaParishad")}
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
                required
                nameProperty="blockName"
                valueProperty="blockId"
                value={formData.currentPanchayatSamiti}
                onChange={handleChange("currentPanchayatSamiti")}
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
                required
                nameProperty="gramPanchayatName"
                valueProperty="gramPanchayatId"
                value={formData.currentGramPanchayatName}
                onChange={handleChange("currentGramPanchayatName")}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="mobileNumber">
                मोबाईल नंबर <span className="text-red-500 ml-1">*</span>
              </Label>
              <div
                style={{
                  position: "relative",
                  width: "100%",
                }}
              >
                <span
                  style={{
                    position: "absolute",
                    left: "12px",
                    top: "50%",
                    transform: "translateY(-50%)",
                    color: "#555",
                    fontSize: "16px",
                    pointerEvents: "none",
                  }}
                >
                  +91
                </span>
                <Input
                  id="mobileNumber"
                  name="mobileNumber"
                  type="tel"
                  required
                  value={formData.mobileNumber}
                  onChange={handleChange("mobileNumber")}
                  style={{
                    width: "100%",
                    padding: "10px 10px 10px 45px",
                    fontSize: "16px",
                    border: "1px solid #ccc",
                    borderRadius: "4px",
                  }}
                />
              </div>
            </div>
            <div className="space-y-2">
              <Label htmlFor="whatsappMobileNumber">
                {" "}
                व्हॉट्सअॅप मोबाईल नंबर
                <span className="text-red-500 ml-1">*</span>
              </Label>
              <Input
                id="whatsappMobileNumber"
                name="whatsappMobileNumber"
                type="tel"
                required
                value={formData.whatsappMobileNumber}
                onChange={handleChange("whatsappMobileNumber")}
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
                required
                value={formData.emailId}
                onChange={handleChange("emailId")}
              />
            </div>
          </CardContent>
          <CardFooter>
            <Button type="submit" className="w-full">
              नोंदणी करा
            </Button>
          </CardFooter>
        </form>
      </Card>
    </div>
  );
}

export default WithAuthLayout(Register);
