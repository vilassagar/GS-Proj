/* eslint-disable react-refresh/only-export-components */
/* eslint-disable react/prop-types */
import WithLayout from "@/components/layout/WithLayout";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { userDesignations } from "@/common/constants";
import WithAuthentication from "@/components/hoc/withAuthentication";
import WithPermission from "@/components/hoc/withPermissions";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import RSelect from "@/components/ui/RSelect";
import { userStore } from "@/lib/store";
import { getProfileData } from "@/services/profile";
import {
  getBlocksByDistrictId,
  getDistricts,
  getPanchayatByBlockId,
} from "@/services/preset";
import { useEffect, useState } from "react";
import toast from "react-hot-toast";
import DocumentUpload from "./DocumentUpload_";

function BasicDetails({ data, designations, districts, blocks, panchayats }) {
  return (
    <Card>
      <CardContent className="space-y-4 pt-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="space-y-2">
            <Label htmlFor="firstName">पहिले नाव</Label>
            <Input
              id="firstName"
              name="firstName"
              value={data.basicDetails?.firstName || ""}
              required
              lang="mr"
              readOnly
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="lastName">आडनाव</Label>
            <Input
              id="lastName"
              name="lastName"
              value={data.basicDetails?.lastName || ""}
              required
              lang="mr"
              readOnly
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="designation">हुद्दा</Label>
            <RSelect
              id="designation"
              options={designations}
              nameProperty="designationName"
              valueProperty="designationId"
              value={designations.find(
                (d) => d.designationName === data.basicDetails?.designation
              )}
              disabled
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="currentZillaParishad">सध्याची जिल्हा परिषद</Label>
            <RSelect
              id="ditrictName"
              options={districts}
              nameProperty="districtName"
              valueProperty="districtId"
              value={data.basicDetails?.district}
              disabled
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="currentPanchayatSamiti">सध्याची पंचायत समिती</Label>
            <RSelect
              id="blocks"
              options={blocks}
              nameProperty="blockName"
              valueProperty="blockId"
              value={data.basicDetails?.block}
              disabled
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
              value={data.basicDetails?.gramPanchayat}
              disabled
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="mobileNumber">मोबाईल क्रमांक</Label>
            <Input
              id="mobileNumber"
              name="mobileNumber"
              type="tel"
              value={data.basicDetails?.mobileNumber || ""}
              required
              readOnly
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
              value={data.basicDetails?.whatsappNumber || ""}
              required
              readOnly
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="emailId">ईमेल आयडी</Label>
            <Input
              id="emailId"
              name="emailId"
              type="email"
              value={data.basicDetails?.email || ""}
              required
              readOnly
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
  const [profileData, setProfileData] = useState(null);
  const [profileDocData, setProfileDocData] = useState(null);

  const [loading, setLoading] = useState(true);
  const user = userStore((state) => state.user);

  useEffect(() => {
    (async () => {
      try {
        setLoading(true);

        // Fetch profile data from the new endpoint
        const profileResponse = await getProfileData();

        if (profileResponse) {
          console.log("Profile response:", profileResponse.data.data);
          const profileInfo = profileResponse.data.data.basicDetails;
          setProfileData(profileInfo);
          const docData = profileResponse.data.data.allDocuments;
          setProfileDocData(docData);

          const basicDetails = profileResponse.data.data;
          setGramSevak(basicDetails);

          // Load districts
          const res2 = await getDistricts();
          setDesignations(userDesignations);
          setDistricts(res2?.data || []);

          // Load blocks if district exists
          if (basicDetails.basicDetails?.district?.districtId) {
            const blockResponse = await getBlocksByDistrictId(
              basicDetails.basicDetails?.district?.districtId || 0
            );
            setBlocks(blockResponse?.data || []);
          }

          // Load panchayats if block exists
          if (basicDetails.basicDetails?.block?.blockId) {
            const panchayatResponse = await getPanchayatByBlockId(
              basicDetails.basicDetails?.block?.blockId || 0
            );
            setPanchayats(panchayatResponse?.data || []);
          }
        } else {
          toast.error("प्रोफाइल माहिती मिळवू शकत नाही");
        }
      } catch (error) {
        console.error("Error fetching profile:", error);
        toast.error("प्रोफाइल लोड करताना त्रुटी आली");
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">प्रोफाइल लोड करत आहे...</p>
        </div>
      </div>
    );
  }

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
            <CardContent className="pt-6">
              {profileData && (
                <DocumentUpload
                  userId={user?.userId}
                  isProfileMode={true}
                  uploadedDocuments={profileDocData || []}
                  documentStatistics={profileData.documentStatistics}
                />
              )}
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
