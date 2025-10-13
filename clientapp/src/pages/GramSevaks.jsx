/* eslint-disable react/prop-types */
import { Button } from "@/components/ui/button";
import { useEffect, useState } from "react";
import WithLayout from "@/components/layout/WithLayout";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import RSelect from "@/components/ui/RSelect";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

import {
  changeStatus,
  getGramSevakById,
  getgramsevakList,
} from "@/services/gramsevak";
import { getUserById } from "@/services/user";
import { Search } from "lucide-react";
import WithAuthentication from "@/components/hoc/withAuthentication";
import WithPermission from "@/components/hoc/withPermissions";
import toast from "react-hot-toast";
import DocumentsDisplay from "@/components/common/DocumentsDisplay";
import GramSevakTable from "@/components/tables/GramSevakTable";
// DocumentsDisplay component moved to its own file: src/components/DocumentsDisplay.jsx

function GramSevaks() {
  const [gramSevaks, setGramSevaks] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [statusValue, setStatusValue] = useState({ id: 1, name: "ALL" });
  const [loading, setLoading] = useState(true);
  const [currentGramSevak, setCurrentGramSevak] = useState(null);
  const [currentGramSevakDocs, setCurrentGramSevakDocs] = useState(null);

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
        fetchGramSevaks();
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
      const response = await getUserById(gramsevakId);
      if (response?.status === "success") {
        console.log("Gram Sevak Details:", response.data.data.basicDetails);
        setCurrentGramSevak(response.data.data.basicDetails);
        setCurrentGramSevakDocs(response.data.data.allDocuments);
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

      <GramSevakTable
        data={gramSevaks}
        onApprove={handleApprove}
        onView={handleViewGramsevak}
      />

      <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
        <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle className="text-2xl">
              ग्रामसेवक संपूर्ण तपशील
            </DialogTitle>
          </DialogHeader>

          {currentGramSevak ? (
            <Tabs defaultValue="basic-info" className="w-full">
              <TabsList className="grid w-full grid-cols-2">
                <TabsTrigger value="basic-info">मूलभूत माहिती</TabsTrigger>
                <TabsTrigger value="documents">
                  कागदपत्रे
                  {currentGramSevak.allDocuments &&
                    currentGramSevak.allDocuments.length > 0 && (
                      <span className="ml-2 bg-blue-100 text-blue-800 text-xs px-2 py-0.5 rounded-full">
                        {currentGramSevak.allDocuments.length}
                      </span>
                    )}
                </TabsTrigger>
              </TabsList>

              <TabsContent value="basic-info" className="space-y-4">
                <Card>
                  <CardHeader>
                    <CardTitle className="text-lg">वैयक्तिक माहिती</CardTitle>
                  </CardHeader>
                  <CardContent className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <p className="text-sm text-gray-500 mb-1">नाव</p>
                      <p className="font-medium">
                        {currentGramSevak.firstName} {currentGramSevak.lastName}
                      </p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-500 mb-1">पदनाम</p>
                      <p className="font-medium">
                        {currentGramSevak.designation?.designationName || "-"}
                      </p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-500 mb-1">
                        मोबाईल क्रमांक
                      </p>
                      <p className="font-medium">
                        {currentGramSevak.mobileNumber || "-"}
                      </p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-500 mb-1">
                        व्हॉट्सअॅप क्रमांक
                      </p>
                      <p className="font-medium">
                        {currentGramSevak.whatsappNumber || "-"}
                      </p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-500 mb-1">ई-मेल</p>
                      <p className="font-medium">
                        {currentGramSevak.email || "-"}
                      </p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-500 mb-1">सेवा आयडी</p>
                      <p className="font-medium">
                        {currentGramSevak.serviceId || "-"}
                      </p>
                    </div>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle className="text-lg">
                      कार्यक्षेत्र माहिती
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <p className="text-sm text-gray-500 mb-1">जिल्हा</p>
                      <p className="font-medium">
                        {currentGramSevak.district.districtName || "-"}
                      </p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-500 mb-1">ब्लॉक</p>
                      <p className="font-medium">
                        {currentGramSevak.block.blockName || "-"}
                      </p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-500 mb-1">ग्राम पंचायत</p>
                      <p className="font-medium">
                        {currentGramSevak.gramPanchayat.gramPanchayatName ||
                          "-"}
                      </p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-500 mb-1">स्थिती</p>
                      <span
                        className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${
                          currentGramSevak.status
                            ? "bg-yellow-100 text-yellow-800"
                            : "bg-green-100 text-green-800"
                        }`}
                      >
                        {currentGramSevak.status == "PENDING"
                          ? "प्रलंबित"
                          : "मंजूर"}
                      </span>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>
              <TabsContent value="documents">
                <Card>
                  <CardContent className="pt-6">
                    <DocumentsDisplay documents={currentGramSevakDocs} />
                  </CardContent>
                </Card>
              </TabsContent>
            </Tabs>
          ) : (
            <div className="text-center py-8">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
              <p className="mt-4 text-gray-600">माहिती लोड करत आहे...</p>
            </div>
          )}
        </DialogContent>
      </Dialog>
    </div>
  );
}

const GramSevaksPage = WithAuthentication(
  WithPermission("gramSevaks")(WithLayout(GramSevaks))
);

export default GramSevaksPage;
