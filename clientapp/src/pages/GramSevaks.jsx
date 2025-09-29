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
import { CheckIcon, EyeIcon, Search, X } from "lucide-react";
import WithAuthentication from "@/components/hoc/withAuthentication";
import WithPermission from "@/components/hoc/withPermissions";
import toast from "react-hot-toast";
import { userStore } from "@/lib/store";

function GramSevakTable({ data, onApprove, onView }) {
  return (
    <div className="border rounded-lg shadow-sm overflow-hidden">
      <div className="overflow-x-auto">
        <Table>
          <TableHeader>
            <TableRow className="bg-slate-100">
              <TableHead className="font-semibold">पहिले</TableHead>
              <TableHead className="font-semibold">ई-मेल</TableHead>
              <TableHead className="font-semibold">ग्राम पंचायत</TableHead>
              <TableHead className="font-semibold">ब्लॉक</TableHead>
              <TableHead className="font-semibold">जिल्हा</TableHead>
              <TableHead className="font-semibold">सेवा आयडी</TableHead>
              <TableHead className="font-semibold">स्थिती</TableHead>
              <TableHead className="font-semibold text-center">
                क्रिया
              </TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {data && data.length > 0 ? (
              data.map((gramSevak, index) => (
                <TableRow
                  key={gramSevak.id || index}
                  className="hover:bg-slate-50"
                >
                  <TableCell className="font-medium">
                    {gramSevak.firstName || "-"} {gramSevak.lastName || "-"}
                  </TableCell>
                  {/* <TableCell>{gramSevak.lastName || "-"}</TableCell> */}
                  <TableCell>{gramSevak.email || "-"}</TableCell>
                  <TableCell>{gramSevak.gramPanchayat || "-"}</TableCell>
                  <TableCell>{gramSevak.block || "-"}</TableCell>
                  <TableCell>{gramSevak.district || "-"}</TableCell>
                  <TableCell>{gramSevak.serviceId || "-"}</TableCell>
                  <TableCell>
                    <span
                      className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                        gramSevak.isApproved
                          ? "bg-green-100 text-green-800"
                          : "bg-yellow-100 text-yellow-800"
                      }`}
                    >
                      {gramSevak.isApproved ? "मंजूर" : "प्रलंबित"}
                    </span>
                  </TableCell>
                  <TableCell>
                    <div className="flex items-center justify-center gap-2">
                      {!gramSevak.isApproved && (
                        <>
                          <Button
                            variant="outline"
                            size="sm"
                            className="h-8 w-8 p-0 text-green-600 hover:text-green-700 hover:bg-green-50"
                            onClick={() => onApprove(index, "APPROVED")}
                            title="मंजूर करा"
                          >
                            <CheckIcon className="h-4 w-4" />
                          </Button>
                          <Button
                            variant="outline"
                            size="sm"
                            className="h-8 w-8 p-0 text-red-600 hover:text-red-700 hover:bg-red-50"
                            onClick={() => onApprove(index, "REJECTED")}
                            title="नाकारा"
                          >
                            <X className="h-4 w-4" />
                          </Button>
                        </>
                      )}
                      <Button
                        variant="outline"
                        size="sm"
                        className="h-8 w-8 p-0 text-blue-600 hover:text-blue-700 hover:bg-blue-50"
                        onClick={() => onView(index)}
                        title="तपशील पहा"
                      >
                        <EyeIcon className="h-4 w-4" />
                      </Button>
                    </div>
                  </TableCell>
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell
                  colSpan={8}
                  className="h-24 text-center text-gray-500"
                >
                  कोणतेही परिणाम नाहीत
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}

function GramSevaks() {
  const [gramSevaks, setGramSevaks] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [statusValue, setStatusValue] = useState({ id: 1, name: "ALL" });
  const [loading, setLoading] = useState(true);
  const [currentGramSevak, setCurrentGramSevak] = useState(null);
  const [isDialogOpen, setIsDialogOpen] = useState(false);

  const statusOptions = [
    { id: 1, name: "ALL" },
    { id: 2, name: "APPROVED" },
    { id: 3, name: "PENDING" },
    { id: 4, name: "REJECTED" },
  ];

  const fetchGramSevaks = async () => {
    try {
      setLoading(true);
      const response = await getgramsevakList(
        searchTerm,
        statusValue?.name || ""
      );

      if (response?.status === "success") {
        setGramSevaks(response.data || []);
      } else {
        toast.error("ग्रामसेवक माहिती मिळू शकली नाही");
      }
    } catch (error) {
      console.error("Error fetching gram sevaks:", error);
      toast.error("डेटा लोड करताना त्रुटी");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchGramSevaks();
  }, [statusValue]);

  const handleSearch = () => {
    fetchGramSevaks();
  };

  const handleClear = () => {
    setSearchTerm("");
    setStatusValue({ id: 1, name: "ALL" });
  };

  const handleApprove = async (index, status) => {
    const gramSevak = gramSevaks[index];
    const payload = {
      gramsevakId: gramSevak.id,
      status: status,
    };

    try {
      const response = await changeStatus(payload);
      if (response.status === "success") {
        toast.success(
          status === "APPROVED"
            ? "ग्रामसेवक यशस्वीरित्या मंजूर झाला!"
            : "ग्रामसेवक नाकारला"
        );
        fetchGramSevaks(); // Refresh the list
      } else {
        toast.error("अपडेट करू शकत नाही, कृपया पुन्हा प्रयत्न करा.");
      }
    } catch (error) {
      console.error("Error updating status:", error);
      toast.error("स्थिती अपडेट करताना त्रुटी");
    }
  };

  const handleViewGramsevak = async (index) => {
    const gramsevakId = gramSevaks[index]?.id;

    try {
      const response = await getGramSevakById(gramsevakId);
      if (response?.status === "success") {
        setCurrentGramSevak(response.data);
        setIsDialogOpen(true);
      } else {
        toast.error("ग्रामसेवकाची माहिती मिळू शकली नाही");
      }
    } catch (error) {
      console.error("Error fetching gram sevak details:", error);
      toast.error("तपशील लोड करताना त्रुटी");
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">लोड करत आहे...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-gray-900">
          ग्रामसेवक व्यवस्थापन
        </h1>
        <div className="text-sm text-gray-500">
          एकूण: {gramSevaks.length} ग्रामसेवक
        </div>
      </div>

      {/* Search and Filter Section */}
      <div className="flex flex-col sm:flex-row gap-4">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-500" />
          <Input
            placeholder="नाव, ई-मेल किंवा जिल्हा शोधा..."
            className="pl-10"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            onKeyPress={(e) => e.key === "Enter" && handleSearch()}
          />
        </div>

        <div className="w-full sm:w-48">
          <RSelect
            options={statusOptions}
            valueProperty="id"
            nameProperty="name"
            value={statusValue}
            onChange={(e) => setStatusValue(e)}
            placeholder="स्थिती निवडा"
          />
        </div>

        <div className="flex gap-2">
          <Button onClick={handleSearch} className="whitespace-nowrap">
            शोधा
          </Button>
          <Button
            variant="outline"
            onClick={handleClear}
            className="whitespace-nowrap"
          >
            साफ करा
          </Button>
        </div>
      </div>

      {/* Table Section */}
      <GramSevakTable
        data={gramSevaks}
        onApprove={handleApprove}
        onView={handleViewGramsevak}
      />

      {/* View Details Dialog */}
      <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
        <DialogContent className="max-w-2xl">
          <Card>
            <CardHeader>
              <CardTitle>ग्रामसेवक तपशील</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {currentGramSevak ? (
                <>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <h3 className="font-semibold text-sm text-gray-500">
                        वैयक्तिक माहिती
                      </h3>
                      <div className="mt-2 space-y-2">
                        <p className="text-sm">
                          <span className="font-medium">नाव:</span>{" "}
                          {currentGramSevak.firstName}{" "}
                          {currentGramSevak.lastName}
                        </p>
                        <p className="text-sm">
                          <span className="font-medium">पदनाम:</span>{" "}
                          {currentGramSevak.designation?.designationName || "-"}
                        </p>
                        <p className="text-sm">
                          <span className="font-medium">मोबाईल:</span>{" "}
                          {currentGramSevak.mobileNumber || "-"}
                        </p>
                        <p className="text-sm">
                          <span className="font-medium">व्हॉट्सअॅप:</span>{" "}
                          {currentGramSevak.whatsappNumber || "-"}
                        </p>
                        <p className="text-sm">
                          <span className="font-medium">ई-मेल:</span>{" "}
                          {currentGramSevak.email || "-"}
                        </p>
                      </div>
                    </div>
                    <div>
                      <h3 className="font-semibold text-sm text-gray-500">
                        कार्यक्षेत्र
                      </h3>
                      <div className="mt-2 space-y-2">
                        <p className="text-sm">
                          <span className="font-medium">जिल्हा:</span>{" "}
                          {currentGramSevak.district || "-"}
                        </p>
                        <p className="text-sm">
                          <span className="font-medium">ब्लॉक:</span>{" "}
                          {currentGramSevak.block || "-"}
                        </p>
                        <p className="text-sm">
                          <span className="font-medium">ग्राम पंचायत:</span>{" "}
                          {currentGramSevak.gramPanchayat || "-"}
                        </p>
                        <p className="text-sm">
                          <span className="font-medium">स्थिती:</span>{" "}
                          <span
                            className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium ${
                              currentGramSevak.isApproved
                                ? "bg-green-100 text-green-800"
                                : "bg-yellow-100 text-yellow-800"
                            }`}
                          >
                            {currentGramSevak.isApproved ? "मंजूर" : "प्रलंबित"}
                          </span>
                        </p>
                      </div>
                    </div>
                  </div>
                </>
              ) : (
                <p className="text-center text-gray-500">
                  माहिती लोड करत आहे...
                </p>
              )}
            </CardContent>
          </Card>
        </DialogContent>
      </Dialog>
    </div>
  );
}

export default WithAuthentication(
  WithPermission("gramSevaks")(WithLayout(GramSevaks))
);
