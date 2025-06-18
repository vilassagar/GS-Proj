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
import {
  getBlocksByDistrictId,
  getDistricts,
  getPanchayatByBlockId,
} from "@/services/preset";
import { useEffect, useState } from "react";
import toast from "react-hot-toast";

function Documents({ data }) {
  return (
    <Card>
      <CardContent className="space-y-4 pt-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {data?.documents.map((doc, index) => (
            <div key={doc?.documentTypeId} className="space-y-2">
              <div className="flex items-center space-x-2">
                <FileUpload value={doc} />
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}

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
        let blockResponse = await getBlocksByDistrictId(
          response?.data?.district?.districtId
        );
        setBlocks(blockResponse?.data);

        let panchayatResponse = await getPanchayatByBlockId(
          response?.data?.gramPanchayat?.gramPanchayatId
        );
        setPanchayats(panchayatResponse?.data);

        setGramSevak(response.data);
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
          <Documents data={gramSevak} />
        </TabsContent>
      </Tabs>
    </div>
  );
}

export default WithAuthentication(
  WithPermission("profile")(WithLayout(Profile))
);
