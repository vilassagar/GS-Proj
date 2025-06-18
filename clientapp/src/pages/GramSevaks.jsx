import { Button } from "@/components/ui/button";
import { useEffect, useState } from "react";
import WithLayout from "@/components/layout/WithLayout";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Dialog, DialogContent, DialogTrigger } from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import RSelect from "@/components/ui/RSelect";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import {
  changeStatus,
  getGramSevakById,
  getgramsevakList,
} from "@/services/gramsevak";
import { CheckIcon, CrossIcon, EyeIcon, Search, X } from "lucide-react";
import WithAuthentication from "@/components/hoc/withAuthentication";
import WithPermission from "@/components/hoc/withPermissions";
import toast from "react-hot-toast";
import { userStore } from "@/lib/store";

function GramSevakTable({ data, onEdit, onApprove }) {
  const [editingGramSevak, setEditingGramSevak] = useState(null);
  const [currentGramSevak, setCurrentGramSevak] = useState(null);
  const user = userStore((state) => state.user);

  const handleEditSubmit = (e) => {
    e.preventDefault();
    if (editingGramSevak) {
      onEdit(editingGramSevak.id, editingGramSevak);
      setEditingGramSevak(null);
    }
  };

  const handleApprove = (index, status) => async (e) => {
    let gramSevak = data[index];
    let payload = {
      gramsevakId: gramSevak.id,
      status: status,
    };

    onApprove(payload);
  };

  const handleViewGramsevak = (index) => async (e) => {
    let gramsevakId = data[index]?.id;

    let response = await getGramSevakById(gramsevakId);
    if (response?.status === "success") {
      setCurrentGramSevak(response?.data);
    } else {
      toast.error("ग्रामसेवकाची माहिती मिळू शकली नाही");
    }
  };

  return (
    <div className="border rounded-lg shadow-lg border-0">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>पहिले नाव</TableHead>
            <TableHead>आडनाव</TableHead>
            <TableHead>ई-मेल</TableHead>
            <TableHead>ब्लॉक</TableHead>
            <TableHead>जिल्हा</TableHead>
            <TableHead>सेवा आयडी</TableHead>
            <TableHead>स्थिती</TableHead>
            <TableHead>क्रिया</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {data?.map((gramSevak, index) => (
            <TableRow key={gramSevak.id}>
              <TableCell>{gramSevak.firstName}</TableCell>
              <TableCell>{gramSevak.lastName}</TableCell>
              <TableCell>{gramSevak.email}</TableCell>
              <TableCell>{gramSevak.block}</TableCell>
              <TableCell>{gramSevak.district}</TableCell>
              <TableCell>{gramSevak.serviceId}</TableCell>
              <TableCell>
                {gramSevak.isApproved ? "मंजूर" : "प्रलंबित"}
              </TableCell>
              <TableCell>
                {gramSevak?.isApproved ? null : (
                  <div className="flex">
                    <Button
                      variant="outline"
                      className="mr-2"
                      onClick={handleApprove(index, "APPROVED")}
                    >
                      <CheckIcon />
                    </Button>

                    <Button
                      variant="outline"
                      onClick={handleApprove(index, "REJECTED")}
                    >
                      <X />
                    </Button>
                  </div>
                )}
                <Dialog>
                  <DialogTrigger asChild>
                    <Button
                      variant="outline"
                      className="mx-5"
                      onClick={handleViewGramsevak(index)}
                    >
                      <EyeIcon />
                    </Button>
                  </DialogTrigger>
                  <DialogContent>
                    <Card>
                      <CardHeader>
                        <CardTitle>वापरकर्ता माहिती</CardTitle>
                      </CardHeader>
                      <CardContent className="space-y-4">
                        <div>
                          <h3 className="font-semibold">वैयक्तिक तपशील</h3>
                          <p>
                            नाव: {currentGramSevak?.firstName}{" "}
                            {currentGramSevak?.lastName}
                          </p>
                          <p>
                            पदनाम:{" "}
                            {currentGramSevak?.designation.designationName}
                          </p>
                          <p>मोबाईल: {currentGramSevak?.mobileNumber}</p>
                          <p>व्हॉट्सअॅप: {currentGramSevak?.whatsappNumber}</p>
                          <p>ई-मेल: {currentGramSevak?.email}</p>
                        </div>
                      </CardContent>
                    </Card>
                  </DialogContent>
                </Dialog>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
}
function GramSevaks() {
  const [gramSevaks, setGramSevaks] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [statusOptions, setStatusOptions] = useState([
    { id: 1, name: "ALL" },
    { id: 2, name: "APPROVED" },
    { id: 3, name: "PENDING" },
    { id: 4, name: "REJECTED" },
  ]);
  const [statusValue, setStatusValue] = useState({ id: 1, name: "ALL" });

  useEffect(() => {
    (async () => {
      let response = await getgramsevakList(
        searchTerm,
        statusValue?.name || ""
      );
      setGramSevaks(response?.data);
    })();
  }, [statusValue, searchTerm]);

  const handleApprove = async (payload) => {
    let response = await changeStatus(payload);
    if (response.status === "success") {
      setStatusValue({ id: 1, name: "ALL" });
      toast.success("ग्रामसेवक यशस्वीरित्या मंजूर झाला!");
    } else {
      toast.error("अपडेट करू शकत नाही, कृपया पुन्हा प्रयत्न करा.");
    }
  };

  return (
    <div>
      <h1 className="text-2xl font-bold mb-5">ग्रामसेवक व्यवस्थापन</h1>
      <div className="flex justify-between items-center mb-5">
        <div className="relative flex-1 mr-10">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-500" />
          <Input
            placeholder="Search documents..."
            className="pl-10"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>

        <RSelect
          options={statusOptions}
          valueProperty="id"
          nameProperty="name"
          value={statusValue}
          onChange={(e) => setStatusValue(e)}
        />
      </div>
      <GramSevakTable
        data={gramSevaks}
        onEdit={() => {}}
        onApprove={handleApprove}
      />
    </div>
  );
}

export default WithAuthentication(
  WithPermission("gramSevaks")(WithLayout(GramSevaks))
);
