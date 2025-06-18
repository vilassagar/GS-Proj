import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { useEffect, useState } from "react";

import WithAuthentication from "@/components/hoc/withAuthentication";
import WithLayout from "@/components/layout/WithLayout";
import { Combobox } from "@/components/ui/comboBox";
import RButton from "@/components/ui/rButton";
import { toast } from "@/components/ui/use-toast";
import {
  getDistrictAdmins,
  getUsers,
  updateDistrictAdmin,
} from "@/services/district";
import { produce } from "immer";
import { EyeIcon, FilePenIcon } from "lucide-react";
import { useNavigate } from "react-router-dom";
import WithPermission from "@/components/hoc/withPermissions";

function DistrictAdmins() {
  const [districts, setDistricts] = useState([]);
  const [admins, setAdmins] = useState([]);

  const navigate = useNavigate();

  useEffect(() => {
    (async () => {
      let response = await getDistrictAdmins();
      setDistricts(response?.data);
    })();
  }, []);

  const handleEditDistrictAdmin = (districtIndex) => async (e) => {
    let district = districts[districtIndex];

    let nextState = produce(districts, (draft) => {
      if (draft[districtIndex].hasOwnProperty("isEditMode")) {
        draft[districtIndex]["isEditMode"] =
          !draft[districtIndex]["isEditMode"];
      } else {
        draft[districtIndex]["isEditMode"] = true;
      }
    });

    let adminResponse = await getUsers(district?.districtId);
    setAdmins(adminResponse.data);

    setDistricts(nextState);
  };

  const handleViewBlocks = (index) => (e) => {
    const districtId = districts[index]["districtId"];

    //ब्लॉक व्यवस्थापन पृष्ठावर जा
    navigate(`/block-admins?districtId=${districtId}`);
  };

  const handleSetDistrictAdmin = (index) => async (e) => {
    let district = districts[index];
    let response = await updateDistrictAdmin(district?.districtId, e);

    if (response.status === "success") {
      let nextState = produce(districts, (draft) => {
        draft[index]["admin"] = e;
        draft[index]["isEditMode"] = false;
      });

      setDistricts(nextState);
    } else {
      toast.error("जिल्हा प्रशासक अद्यतनित करू शकत नाही");
    }
  };

  return (
    <div>
      <div className="flex justify-between ">
        <h1 className="text-2xl font-bold mb-5">जिल्हा व्यवस्थापन</h1>
      </div>

      <div className="border rounded-lg shadow-lg border-0">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead className="p-2">जिल्ह्याचे नाव</TableHead>
              <TableHead className="p-2">जिल्हा प्रशासक</TableHead>
              <TableHead className="w-[150px] p-2">क्रिया</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {districts?.length ? (
              districts?.map((district, index) => (
                <TableRow key={district?.districtId}>
                  <TableCell className="p-2">{district.districtName}</TableCell>
                  <TableCell className="p-2">
                    {district?.isEditMode ? (
                      <Combobox
                        options={admins}
                        labelProperty="userName"
                        valueProperty="userId"
                        value={district?.admin ?? null}
                        onChange={handleSetDistrictAdmin(index)}
                      />
                    ) : (
                      <div>{district?.admin?.userName ?? ""}</div>
                    )}
                  </TableCell>
                  <TableCell className="p-2">
                    <div className="flex">
                      <RButton
                        variant="ghost"
                        className="flex items-center gap-2 "
                        onClick={handleEditDistrictAdmin(index)}
                      >
                        <FilePenIcon className="h-4 w-4" />
                      </RButton>

                      <RButton
                        variant="ghost"
                        className="flex items-center gap-2 "
                        onClick={handleViewBlocks(district?.districtId)}
                      >
                        <EyeIcon className="h-4 w-4" />
                      </RButton>
                    </div>
                  </TableCell>
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell colSpan={7} className="h-24 text-center">
                  कोणतेही परिणाम नाहीत.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}

export default WithAuthentication(
  WithPermission("districtAdmins")(WithLayout(DistrictAdmins))
);
