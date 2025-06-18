import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { useEffect, useState } from "react";

import WithLayout from "@/components/layout/WithLayout";
import { Combobox } from "@/components/ui/comboBox";
import RButton from "@/components/ui/rButton";
import { toast } from "@/components/ui/use-toast";

import { getBlockAdmins, getUsers, updateBlockAdmin } from "@/services/block";
import { produce } from "immer";
import { FilePenIcon } from "lucide-react";
import WithAuthentication from "@/components/hoc/withAuthentication";
import WithPermission from "@/components/hoc/withPermissions";

function BlockAdmins() {
  const [blocks, setBlocks] = useState([]);
  const [admins, setAdmins] = useState([]);

  useEffect(() => {
    (async () => {
      let params = new URLSearchParams(window.location.search);
      let districtId = params.get("districtId");

      let response = await getBlockAdmins(districtId);
      setBlocks(response?.data);
    })();
  }, []);

  const handleEditBlockAdmin = (blockIndex) => async (e) => {
    const block = blocks[blockIndex];

    let nextState = produce(blocks, (draft) => {
      if (draft[blockIndex].hasOwnProperty("isEditMode")) {
        draft[blockIndex]["isEditMode"] = !draft[blockIndex]["isEditMode"];
      } else {
        draft[blockIndex]["isEditMode"] = true;
      }
    });

    let adminResponse = await getUsers(block?.blockId);
    setAdmins(adminResponse.data);

    setBlocks(nextState);
  };

  const handleSetBlockAdmin = (index) => async (e) => {
    const block = blocks[index];
    let response = await updateBlockAdmin(block?.blockId, e);

    if (response.status === "success") {
      let nextState = produce(blocks, (draft) => {
        draft[index]["admin"] = e;
        draft[index]["isEditMode"] = false;
      });

      setBlocks(nextState);
    } else {
      toast.error("ब्लॉक प्रशासक अद्यतनित करू शकत नाही");
    }
  };

  return (
    <div>
      <div className="flex justify-between ">
        <h1 className="text-2xl font-bold mb-5">ब्लॉक व्यवस्थापन</h1>
      </div>

      <div className="border rounded-lg shadow-lg border-0">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead className="p-2">ब्लॉकचे नाव</TableHead>
              <TableHead className="p-2">ब्लॉक प्रशासक</TableHead>
              <TableHead className="w-[150px] p-2">क्रिया</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {blocks?.length ? (
              blocks?.map((block, index) => (
                <TableRow key={block?.blockId}>
                  <TableCell className="p-2">{block.blockName}</TableCell>
                  <TableCell className="p-2">
                    {block?.isEditMode ? (
                      <Combobox
                        options={admins}
                        labelProperty="userName"
                        valueProperty="userId"
                        value={block?.admin ?? null}
                        onChange={handleSetBlockAdmin(index)}
                      />
                    ) : (
                      <div>{block?.admin?.userName ?? ""}</div>
                    )}
                  </TableCell>
                  <TableCell className="p-2">
                    <div className="flex">
                      <RButton
                        variant="ghost"
                        className="flex items-center gap-2 "
                        onClick={handleEditBlockAdmin(index)}
                      >
                        <FilePenIcon className="h-4 w-4" />
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
  WithPermission("blockAdmins")(WithLayout(BlockAdmins))
);
